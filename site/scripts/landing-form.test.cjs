const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');
const { randomUUID, webcrypto } = require('node:crypto');

const source = fs.readFileSync(
  path.join(__dirname, '../themes/bexer-hugo/assets/js/landing-form.js'), 'utf8',
);
const accepted = () => Promise.resolve({ ok: true, status: 201, json: async () => ({ accepted: true }) });

function setup({ umami, fetch = accepted, loading = false, crypto = { randomUUID } } = {}) {
  const calls = [], pixels = [], redirects = [], requests = [];
  const forms = ['gp-form-1', 'gp-form-2'].map(id => {
    const listeners = {};
    const trap = { value: '' };
    const button = { disabled: false, textContent: 'Invia richiesta' };
    const status = { hidden: true, textContent: '' };
    const attributes = {};
    return {
      id, trap, button, status, attributes, action: 'https://greenproperty.it/api/leads',
      values: { nome: 'Persona test', telefono: '+39 333 1234567', email: 'test@example.com',
        citta: 'Firenze', tipo: 'Appartamento', note: 'Note riservate', privacy: 'accettata' },
      querySelector(selector) {
        return { 'input[name="sito_web"]': trap, 'button[type="submit"]': button,
          '[data-gp-form-status]': status }[selector];
      },
      setAttribute(name, value) { attributes[name] = value; },
      removeAttribute(name) { delete attributes[name]; },
      addEventListener(type, handler) { listeners[type] = handler; },
      fire(type, name, prevented = false) {
        const event = {
          target: { name, get value() { throw Error('Analytics must not read field values'); } },
          defaultPrevented: prevented,
          preventDefault() { this.defaultPrevented = true; },
        };
        const done = Promise.resolve(listeners[type]?.(event));
        return { event, done };
      },
    };
  });
  let ready;
  const window = {
    umami: umami === undefined ? {
      track(name, data) {
        calls.push({ name, data: JSON.parse(JSON.stringify(data)) });
        return Promise.resolve();
      },
    } : umami,
    fbq(...args) { pixels.push(args); },
    crypto,
    fetch(url, options) {
      requests.push({ url, ...options, payload: JSON.parse(options.body) });
      return fetch(url, options);
    },
    location: { assign(url) { redirects.push(url); } },
  };
  const document = {
    readyState: loading ? 'loading' : 'interactive',
    querySelectorAll(selector) {
      assert.equal(selector, 'form[data-gp-form]');
      return forms;
    },
    addEventListener(type, handler) {
      assert.equal(type, 'DOMContentLoaded');
      ready = handler;
    },
  };
  class FormData {
    constructor(form) { this.form = form; }
    get(name) { return this.form.values[name] ?? null; }
  }
  vm.runInNewContext(source, { window, document, FormData, AbortController, setTimeout, clearTimeout });
  return { forms, calls, pixels, redirects, requests, window, ready: () => ready() };
}

test('one start per form; events include only static form IDs', async () => {
  const { forms, calls, requests } = setup();
  forms[0].fire('input', 'nome');
  forms[0].fire('input', 'telefono');
  forms[0].fire('change', 'privacy');
  forms[1].fire('change', 'citta');
  await forms[0].fire('submit').done;
  assert.deepEqual(calls.map(call => call.name), [
    'Inizio modulo proprietari', 'Inizio modulo proprietari',
    'Invio modulo proprietari', 'Richiesta proprietari accettata',
  ]);
  for (const call of calls) {
    assert.deepEqual(Object.keys(call.data), ['modulo']);
    assert.match(call.data.modulo, /^gp-form-[12]$/);
  }
  assert.equal(requests[0].url, 'https://greenproperty.it/api/leads');
  assert.equal(requests[0].payload.note, 'Note riservate');
  assert.equal(requests[0].payload.privacy, 'accettata');
  assert.equal(requests[0].payload.form_id, 'gp-form-1');
  assert.match(requests[0].payload.submission_id, /^[a-f0-9-]{36}$/);
});

test('confirmation and Meta Pixel wait for provider acceptance; double submit sends once', async () => {
  let resolve;
  const context = setup({ fetch: () => new Promise(done => { resolve = done; }) });
  const { forms, calls, pixels, redirects, requests } = context;
  const attempt = forms[0].fire('submit');
  assert.equal(attempt.event.defaultPrevented, true);
  assert.equal(forms[0].button.disabled, true);
  assert.equal(forms[0].attributes['aria-busy'], 'true');
  await forms[0].fire('submit').done;
  assert.equal(requests.length, 1);
  assert.deepEqual(calls.map(call => call.name), ['Inizio modulo proprietari', 'Invio modulo proprietari']);
  assert.deepEqual(pixels, []);
  assert.deepEqual(redirects, []);
  resolve(await accepted());
  await attempt.done;
  assert.deepEqual(pixels, [['track', 'Lead']]);
  assert.deepEqual(redirects, ['/advantages/grazie/']);
  assert.equal(forms[0].button.disabled, false);
});

test('honeypot submits neither email nor conversion events', async () => {
  const { forms, calls, pixels, redirects, requests } = setup();
  forms[0].trap.value = 'bot';
  forms[0].fire('input', 'sito_web');
  forms[0].fire('change', 'nome');
  await forms[0].fire('submit').done;
  assert.deepEqual(calls, []);
  assert.deepEqual(pixels, []);
  assert.deepEqual(requests, []);
  assert.deepEqual(redirects, ['/advantages/grazie/']);
});

test('technical fields, button clicks and canceled submissions do not count', async () => {
  const { forms, calls, requests } = setup();
  for (const name of ['sito_web', '_subject', 'unapproved']) forms[0].fire('input', name);
  forms[0].fire('click');
  await forms[0].fire('submit', undefined, true).done;
  assert.deepEqual(calls, []);
  assert.deepEqual(requests, []);
});

test('failed requests preserve values and reuse the same idempotency key on retry', async () => {
  let first = true;
  const { forms, requests, calls, redirects } = setup({
    fetch: () => {
      if (first) { first = false; return Promise.reject(Error('network lost')); }
      return accepted();
    },
  });
  await forms[0].fire('submit').done;
  assert.equal(forms[0].status.hidden, false);
  assert.match(forms[0].status.textContent, /riprova/);
  assert.equal(forms[0].values.note, 'Note riservate');
  assert.deepEqual(redirects, []);
  assert.equal(calls.some(call => call.name === 'Richiesta proprietari accettata'), false);
  await forms[0].fire('submit').done;
  assert.equal(requests[0].body, requests[1].body);
  forms[0].values.telefono = '+39 333 7654321';
  await forms[0].fire('submit').done;
  assert.notEqual(requests[1].payload.submission_id, requests[2].payload.submission_id);
});

test('restored or autofilled fields still start the funnel before submission, only once', async () => {
  let first = true;
  const { forms, calls } = setup({
    fetch: () => {
      if (first) { first = false; return Promise.reject(Error('network lost')); }
      return accepted();
    },
  });
  // Fields are populated, but the browser has emitted neither input nor change.
  assert.deepEqual(calls, []);
  await forms[0].fire('submit').done;
  assert.deepEqual(calls.map(call => call.name), ['Inizio modulo proprietari', 'Invio modulo proprietari']);
  forms[0].fire('change', 'privacy');
  await forms[0].fire('submit').done;
  assert.deepEqual(calls.map(call => call.name), [
    'Inizio modulo proprietari', 'Invio modulo proprietari',
    'Invio modulo proprietari', 'Richiesta proprietari accettata',
  ]);
});

test('Web Crypto fallback generates a valid UUIDv4 and preserves it on unchanged retries', async () => {
  let randomCalls = 0;
  let first = true;
  const { forms, requests, redirects } = setup({
    crypto: { getRandomValues(bytes) { randomCalls++; return webcrypto.getRandomValues(bytes); } },
    fetch: () => {
      if (first) { first = false; return Promise.reject(Error('network lost')); }
      return accepted();
    },
  });
  await forms[0].fire('submit').done;
  await forms[0].fire('submit').done;
  assert.equal(randomCalls, 1);
  assert.equal(requests[0].payload.submission_id, requests[1].payload.submission_id);
  assert.match(requests[0].payload.submission_id, /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/);
  assert.deepEqual(redirects, ['/advantages/grazie/']);
  forms[0].values.telefono = '+39 333 7654321';
  await forms[0].fire('submit').done;
  assert.equal(randomCalls, 2);
  assert.notEqual(requests[1].payload.submission_id, requests[2].payload.submission_id);
});

test('provider errors and fake acceptance never count a conversion', async () => {
  for (const status of [200, 422, 429, 502, 503]) {
    const { forms, calls, pixels, redirects } = setup({
      fetch: async () => ({ ok: status === 200, status, json: async () => ({ accepted: false }) }),
    });
    await forms[0].fire('submit').done;
    assert.equal(forms[0].status.hidden, false);
    assert.equal(forms[0].button.disabled, false);
    assert.equal(calls.some(call => call.name === 'Richiesta proprietari accettata'), false);
    assert.deepEqual(pixels, []);
    assert.deepEqual(redirects, []);
  }
});

test('proxy rate limits show the wait message even when the response is not JSON', async () => {
  const { forms, redirects } = setup({
    fetch: async () => ({ ok: false, status: 429, json: async () => { throw Error('not JSON'); } }),
  });
  await forms[0].fire('submit').done;
  assert.match(forms[0].status.textContent, /Attendi qualche minuto/);
  assert.deepEqual(redirects, []);
});

test('missing, failing or rejected analytics cannot block an accepted lead', async () => {
  for (const umami of [null, {}, { track() { throw Error('blocked'); } },
    { track() { return Promise.reject(Error('offline')); } }, { track() { return new Promise(() => {}); } }]) {
    const { forms, pixels, redirects } = setup({ umami });
    forms[0].fire('input', 'nome');
    await forms[0].fire('submit').done;
    assert.deepEqual(pixels, [['track', 'Lead']]);
    assert.deepEqual(redirects, ['/advantages/grazie/']);
  }
  await new Promise(resolve => setImmediate(resolve));
});

test('initializes after DOM readiness and retries when tracker becomes available', () => {
  const context = setup({ loading: true, umami: null });
  context.ready();
  context.forms[0].fire('input', 'nome');
  const names = [];
  context.window.umami = { track(name) { names.push(name); } };
  context.forms[0].fire('input', 'telefono');
  context.forms[0].fire('change', 'privacy');
  assert.deepEqual(names, ['Inizio modulo proprietari']);
});
