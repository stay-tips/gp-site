import { createHash } from "node:crypto";
import { createServer } from "node:http";
import { isIP } from "node:net";
import { pathToFileURL } from "node:url";

const MAX_BODY_BYTES = 12_288;
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const EMAIL = /^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/;
const CITIES = new Set(["Firenze", "Milano", "Bologna", "Altra città"]);
const TYPES = new Set(["Appartamento", "Villa", "Palazzina / più unità", "Altro"]);
const FIELDS = new Set([
  "nome", "telefono", "email", "citta", "tipo", "note", "privacy", "sito_web",
  "_subject", "form_id", "submission_id",
]);

class RequestError extends Error {
  constructor(status, code, fields) {
    super(code);
    this.status = status;
    this.fields = fields;
  }
}

function reply(response, status, body, headers = {}) {
  response.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff",
    ...headers,
  });
  response.end(JSON.stringify(body));
}

async function readBody(request) {
  if (Number(request.headers["content-length"]) > MAX_BODY_BYTES) {
    throw new RequestError(413, "body_too_large");
  }
  const chunks = await new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    request.on("data", (chunk) => {
      size += chunk.length;
      if (size > MAX_BODY_BYTES) {
        reject(new RequestError(413, "body_too_large"));
        return;
      }
      chunks.push(chunk);
    });
    request.on("end", () => resolve(chunks));
    request.on("error", reject);
  });
  try {
    return JSON.parse(Buffer.concat(chunks).toString("utf8"));
  } catch {
    throw new RequestError(400, "invalid_json");
  }
}

function validate(body) {
  if (!body || Array.isArray(body) || typeof body !== "object") {
    throw new RequestError(422, "invalid_fields", []);
  }
  const invalid = new Set();
  for (const [key, value] of Object.entries(body)) {
    if (!FIELDS.has(key) || typeof value !== "string") invalid.add(FIELDS.has(key) ? key : "form");
  }
  if (invalid.size) throw new RequestError(422, "invalid_fields", [...invalid]);
  const lead = Object.fromEntries([...FIELDS].map((field) => [field, (body[field] || "").trim()]));
  // The server also checks this field: disabling JavaScript must not bypass it.
  if (lead.sito_web) return null;
  if (!UUID.test(lead.submission_id)) invalid.add("submission_id");
  if (!["gp-form-1", "gp-form-2"].includes(lead.form_id)) invalid.add("form_id");
  if (lead.nome.length < 2 || lead.nome.length > 120 || /[\x00-\x1f\x7f]/.test(lead.nome)) invalid.add("nome");
  const digits = lead.telefono.replace(/\D/g, "").length;
  if (!/^[+\d ()-]{6,32}$/.test(lead.telefono) || digits < 6 || digits > 18) invalid.add("telefono");
  if (lead.email && (lead.email.length > 254 || !EMAIL.test(lead.email) || /[\r\n]/.test(lead.email))) invalid.add("email");
  if (!CITIES.has(lead.citta)) invalid.add("citta");
  if (!TYPES.has(lead.tipo)) invalid.add("tipo");
  if (lead.note.length > 2_000 || /[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/.test(lead.note)) invalid.add("note");
  if (lead.privacy !== "accettata") invalid.add("privacy");
  if (invalid.size) throw new RequestError(422, "invalid_fields", [...invalid]);
  return lead;
}

function emailFor(lead, from) {
  return {
    from,
    // Never derive the recipient, subject or sender from the public request.
    to: ["info@greenproperty.it"],
    subject: "Richiesta valutazione proprietà — Green Property",
    ...(lead.email ? { reply_to: lead.email } : {}),
    text: [
      "Richiesta dal modulo proprietari di greenproperty.it",
      `Riferimento: ${lead.submission_id}`,
      `Modulo: ${lead.form_id}`,
      "",
      `Nome: ${lead.nome}`,
      `Telefono: ${lead.telefono}`,
      `Email: ${lead.email || "Non indicata"}`,
      `Città: ${lead.citta}`,
      `Immobile: ${lead.tipo}`,
      "",
      `Note: ${lead.note || "Nessuna"}`,
      "",
      "Informativa privacy e richiesta di ricontatto: accettate.",
    ].join("\n"),
  };
}

// Fixed windows, bounded memory, no IP addresses or form values in logs/storage.
function limiter(now) {
  const clients = new Map();
  let global = { count: 0, expires: 0 };
  return (ip) => {
    const time = now();
    for (const [key, value] of clients) if (value.expires <= time) clients.delete(key);
    if (global.expires <= time) global = { count: 0, expires: time + 3_600_000 };
    const key = createHash("sha256").update(ip).digest("hex");
    const client = clients.get(key) || { count: 0, expires: time + 900_000 };
    if (client.count >= 5) return Math.ceil((client.expires - time) / 1_000);
    if (global.count >= 100 || (!clients.has(key) && clients.size >= 10_000)) {
      return Math.ceil((global.expires - time) / 1_000);
    }
    client.count++;
    global.count++;
    clients.set(key, client);
    return 0;
  };
}

export function createLeadServer({ apiKey, from, origin = "https://greenproperty.it", fetchImpl = fetch, now = Date.now, log = console.log }) {
  if (!apiKey || !from || /[\r\n]/.test(from)) throw new Error("RESEND_API_KEY and LEAD_FROM are required");
  if (new URL(origin).origin !== origin) throw new Error("PUBLIC_ORIGIN must be an exact origin");
  const rateLimit = limiter(now);
  let inFlight = 0;
  const server = createServer({ maxHeaderSize: 8_192 }, async (request, response) => {
    try {
      if (request.url === "/health" && request.method === "GET") {
        return reply(response, 200, { status: "ok" });
      }
      if (request.url !== "/api/leads") throw new RequestError(404, "not_found");
      if (request.method !== "POST") {
        return reply(response, 405, { accepted: false, error: "method_not_allowed" }, { Allow: "POST" });
      }
      if (request.headers.origin !== origin) throw new RequestError(403, "origin_not_allowed");
      if (request.headers["content-type"]?.split(";", 1)[0].trim().toLowerCase() !== "application/json") {
        throw new RequestError(415, "json_required");
      }
      // Caddy MUST overwrite this header. The service has no published host port.
      const ip = request.headers["x-real-ip"];
      if (typeof ip !== "string" || !isIP(ip)) throw new RequestError(503, "proxy_not_configured");
      const retryAfter = rateLimit(ip);
      if (retryAfter) return reply(response, 429, { accepted: false, error: "rate_limited" }, { "Retry-After": String(retryAfter) });
      const lead = validate(await readBody(request));
      if (!lead) return reply(response, 200, { accepted: false });
      if (inFlight >= 3) {
        return reply(response, 503, { accepted: false, error: "temporarily_unavailable" }, { "Retry-After": "15" });
      }
      inFlight++;
      try {
        const provider = await fetchImpl("https://api.resend.com/emails", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${apiKey}`,
            "Content-Type": "application/json",
            "Idempotency-Key": `gp-lead/${lead.submission_id}`,
          },
          body: JSON.stringify(emailFor(lead, from)),
          signal: AbortSignal.timeout(12_000),
        });
        if (!provider.ok) {
          log(JSON.stringify({ event: "lead_provider_rejected", status: provider.status }));
          // Do not return or log the provider body: it can contain form values.
          await provider.body?.cancel();
          throw new RequestError(provider.status === 409 ? 409 : 502, provider.status === 409 ? "submission_conflict" : "delivery_unavailable");
        }
        const receipt = await provider.json();
        if (typeof receipt.id !== "string" || !receipt.id) throw new RequestError(502, "delivery_unavailable");
        log(JSON.stringify({ event: "lead_accepted" }));
        // Accepted by Resend, not a guarantee of delivery to the mailbox.
        return reply(response, 201, { accepted: true });
      } finally {
        inFlight--;
      }
    } catch (error) {
      if (response.headersSent) return response.end();
      const expected = error instanceof RequestError;
      if (!expected) log(JSON.stringify({ event: "lead_request_failed" }));
      reply(response, expected ? error.status : 503, {
        accepted: false,
        error: expected ? error.message : "temporarily_unavailable",
        ...(error.fields ? { fields: error.fields } : {}),
      }, error.status === 413 ? { Connection: "close" } : {});
    }
  });
  server.requestTimeout = 15_000;
  server.headersTimeout = 10_000;
  server.keepAliveTimeout = 5_000;
  server.maxRequestsPerSocket = 50;
  server.maxConnections = 128;
  return server;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const server = createLeadServer({
    apiKey: process.env.RESEND_API_KEY,
    from: process.env.LEAD_FROM,
    origin: process.env.PUBLIC_ORIGIN || "https://greenproperty.it",
  });
  server.listen(3000, "0.0.0.0", () => console.log("Green Property lead endpoint listening"));
  for (const signal of ["SIGINT", "SIGTERM"]) process.on(signal, () => server.close());
}
