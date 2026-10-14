import assert from "node:assert/strict";
import { randomUUID } from "node:crypto";
import { request as httpRequest } from "node:http";
import { once } from "node:events";
import { test } from "node:test";
import { createLeadServer } from "./server.mjs";

function lead(overrides = {}) {
  return {
    nome: "Test Modulo",
    telefono: "+39 000 000 0000",
    email: "test@example.invalid",
    citta: "Firenze",
    tipo: "Appartamento",
    note: "Contenuto di prova, non inviare.",
    privacy: "accettata",
    sito_web: "",
    form_id: "gp-form-1",
    submission_id: randomUUID(),
    ...overrides,
  };
}

async function fixture(t, fetchImpl = async () => Response.json({ id: "provider-receipt" }), extra = {}) {
  const calls = [];
  const logs = [];
  const server = createLeadServer({
    apiKey: "private-test-key",
    from: "Green Property <no-reply@updates.stay.tips>",
    fetchImpl: async (...args) => { calls.push(args); return fetchImpl(...args); },
    log: (line) => logs.push(line),
    ...extra,
  });
  server.listen(0, "127.0.0.1");
  await once(server, "listening");
  t.after(() => new Promise((resolve) => { server.closeAllConnections(); server.close(resolve); }));
  const url = `http://127.0.0.1:${server.address().port}/api/leads`;
  const post = (body = lead(), headers = {}) => fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", Origin: "https://greenproperty.it", "X-Real-IP": "192.0.2.1", ...headers },
    body: JSON.stringify(body),
  });
  return { calls, logs, post, url };
}

test("accepts only after provider acceptance, fixes recipient and preserves idempotency on retry", async (t) => {
  let accept;
  const upstream = new Promise((resolve) => { accept = resolve; });
  const app = await fixture(t, () => upstream);
  const data = lead({ _subject: "Untrusted subject" });
  let settled = false;
  const response = app.post(data).then((r) => { settled = true; return r; });
  while (!app.calls.length) await new Promise((resolve) => setImmediate(resolve));
  assert.equal(settled, false);
  accept(Response.json({ id: "accepted-id" }));
  assert.equal((await response).status, 201);
  assert.deepEqual(await (await response).json(), { accepted: true });
  const [url, options] = app.calls[0];
  assert.equal(url, "https://api.resend.com/emails");
  assert.equal(options.headers["Idempotency-Key"], `gp-lead/${data.submission_id}`);
  const email = JSON.parse(options.body);
  assert.deepEqual(email.to, ["info@greenproperty.it"]);
  assert.equal(email.from, "Green Property <no-reply@updates.stay.tips>");
  assert.equal(email.reply_to, data.email);
  assert.ok(email.text.includes(data.telefono));
  assert.ok(!email.subject.includes("Untrusted"));
  assert.equal("html" in email, false);
  assert.deepEqual(app.logs, ['{"event":"lead_accepted"}']);
  assert.ok(!app.logs.join().includes(data.email));
});

test("retries use the same provider key and deterministic payload", async (t) => {
  const app = await fixture(t);
  const data = lead();
  for (let i = 0; i < 2; i++) assert.equal((await app.post(data)).status, 201);
  assert.equal(app.calls[0][1].headers["Idempotency-Key"], app.calls[1][1].headers["Idempotency-Key"]);
  assert.equal(app.calls[0][1].body, app.calls[1][1].body);
});

test("honeypot never sends email or reports conversion", async (t) => {
  const app = await fixture(t);
  const response = await app.post({ sito_web: "spam.example" });
  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { accepted: false });
  assert.equal(app.calls.length, 0);
});

test("validates consent, contact fields, enums, field types and header injection", async (t) => {
  const invalid = [
    { privacy: "" }, { nome: "" }, { telefono: "abc" }, { email: "x@example.invalid\r\nBcc: other@example.invalid" },
    { citta: "Unknown" }, { tipo: "Unknown" }, { form_id: "other" }, { submission_id: "not-a-uuid" },
    { note: "x".repeat(2_001) }, { nome: { html: "untrusted" } }, { to: "other@example.invalid" },
  ];
  const app = await fixture(t);
  for (let i = 0; i < invalid.length; i++) {
    const response = await app.post(lead(invalid[i]), { "X-Real-IP": `192.0.2.${i + 1}` });
    assert.equal(response.status, 422, JSON.stringify(invalid[i]));
    assert.equal((await response.json()).accepted, false);
  }
  assert.equal(app.calls.length, 0);
});

test("requires exact origin, JSON and trusted proxy header; ignores spoofed forwarding chains", async (t) => {
  const app = await fixture(t);
  assert.equal((await app.post(lead(), { Origin: "https://evil.example" })).status, 403);
  assert.equal((await app.post(lead(), { Origin: "https://greenproperty.it.evil.example" })).status, 403);
  assert.equal((await app.post(lead(), { "Content-Type": "application/x-www-form-urlencoded" })).status, 415);
  assert.equal((await app.post(lead(), { "X-Real-IP": "", "X-Forwarded-For": "192.0.2.200" })).status, 503);
  assert.equal(app.calls.length, 0);
});

test("enforces per-client and global budgets, and permits requests after expiration", async (t) => {
  let time = 0;
  const app = await fixture(t, undefined, { now: () => time });
  for (let i = 0; i < 5; i++) assert.equal((await app.post()).status, 201);
  const blocked = await app.post(lead(), { "X-Forwarded-For": "203.0.113.7" });
  assert.equal(blocked.status, 429);
  assert.equal(blocked.headers.get("Retry-After"), "900");
  time += 900_001;
  assert.equal((await app.post()).status, 201);
  for (let i = 0; i < 94; i++) assert.equal((await app.post(lead(), { "X-Real-IP": `192.0.2.${i + 2}` })).status, 201);
  assert.equal((await app.post(lead(), { "X-Real-IP": "198.51.100.1" })).status, 429);
  time += 3_600_000;
  assert.equal((await app.post()).status, 201);
});

test("rejects oversized bodies with Content-Length and chunked transfer", async (t) => {
  const app = await fixture(t);
  assert.equal((await app.post(lead({ note: "x".repeat(13_000) }))).status, 413);
  const response = await new Promise((resolve, reject) => {
    const request = httpRequest(app.url, {
      method: "POST",
      headers: { "Content-Type": "application/json", Origin: "https://greenproperty.it", "X-Real-IP": "192.0.2.2" },
    }, (response) => { response.resume(); resolve(response); });
    request.on("error", reject);
    request.write('{"note":"');
    request.write("x".repeat(13_000));
    request.end('"}');
  });
  assert.equal(response.statusCode, 413);
  assert.equal(app.calls.length, 0);
});

test("provider failures and timeouts never report success or expose secrets and form values", async (t) => {
  for (const status of [401, 403, 409, 429, 500]) {
    await t.test(`provider ${status}`, async (t) => {
      const app = await fixture(t, async () => Response.json({ message: "secret and test@example.invalid" }, { status }));
      const response = await app.post();
      assert.equal(response.status, status === 409 ? 409 : 502);
      const body = await response.text();
      assert.equal(JSON.parse(body).accepted, false);
      assert.ok(!body.includes("secret"));
      assert.ok(!app.logs.join().includes("test@example.invalid"));
    });
  }
  const app = await fixture(t, async () => { throw new Error("secret test@example.invalid"); });
  const response = await app.post();
  assert.equal(response.status, 503);
  assert.deepEqual(await response.json(), { accepted: false, error: "temporarily_unavailable" });
  assert.deepEqual(app.logs, ['{"event":"lead_request_failed"}']);
});

test("missing receipt is failure; runtime refuses missing credentials", async (t) => {
  const app = await fixture(t, async () => Response.json({}));
  assert.equal((await app.post()).status, 502);
  assert.throws(() => createLeadServer({ from: "x@example.invalid" }), /required/);
  assert.throws(() => createLeadServer({ apiKey: "test" }), /required/);
});
