/* Moduli proprietari: invio allo stesso dominio, conferma solo dopo accettazione
   del servizio email. Umami riceve solo eventi e l'id statico del modulo. */
(function () {
  'use strict';

  var PAGINA_GRAZIE = '/advantages/grazie/';
  var CAMPI = ['nome', 'telefono', 'email', 'citta', 'tipo', 'note', 'privacy'];

  function eTrappola(form) {
    var trappola = form.querySelector('input[name="sito_web"]');
    return trappola && trappola.value;
  }

  function traccia(nome, form) {
    if (!window.umami || typeof window.umami.track !== 'function') { return false; }
    try {
      var invio = window.umami.track(nome, { modulo: form.id });
      if (invio && typeof invio.catch === 'function') { invio.catch(function () {}); }
      return true;
    } catch (errore) {
      return false;
    }
  }

  function generaIdInvio() {
    if (typeof window.crypto.randomUUID === 'function') {
      return window.crypto.randomUUID();
    }
    // Compatibilità con i browser che hanno Web Crypto ma non randomUUID.
    var bytes = window.crypto.getRandomValues(new Uint8Array(16));
    bytes[6] = (bytes[6] & 15) | 64;
    bytes[8] = (bytes[8] & 63) | 128;
    var hex = '';
    for (var i = 0; i < bytes.length; i++) {
      hex += (bytes[i] + 256).toString(16).slice(1);
    }
    return hex.slice(0, 8) + '-' + hex.slice(8, 12) + '-' + hex.slice(12, 16) +
      '-' + hex.slice(16, 20) + '-' + hex.slice(20);
  }

  function prepara(form) {
    var iniziato = false;
    var inInvio = false;
    var ultimoCorpo;
    var idInvio;
    var bottone = form.querySelector('button[type="submit"]');
    var stato = form.querySelector('[data-gp-form-status]');
    var testoBottone = bottone.textContent;

    function allaModifica(evento) {
      if (iniziato || eTrappola(form)) { return; }
      var campo = evento.target;
      if (!campo || CAMPI.indexOf(campo.name) === -1) { return; }
      iniziato = traccia('Inizio modulo proprietari', form);
    }

    form.addEventListener('input', allaModifica);
    form.addEventListener('change', allaModifica);
    form.addEventListener('submit', async function (evento) {
      if (evento.defaultPrevented) { return; }
      evento.preventDefault();
      if (inInvio) { return; }
      if (eTrappola(form)) {
        window.location.assign(PAGINA_GRAZIE);
        return;
      }

      inInvio = true;
      bottone.disabled = true;
      bottone.textContent = 'Invio in corso…';
      form.setAttribute('aria-busy', 'true');
      stato.textContent = '';
      stato.hidden = true;
      var timer;
      try {
        var dati = new FormData(form);
        var payload = { form_id: form.id };
        CAMPI.forEach(function (nome) { payload[nome] = dati.get(nome) || ''; });
        var corpo = JSON.stringify(payload);
        // Lo stesso tentativo mantiene la chiave anche dopo timeout/errori di rete.
        if (corpo !== ultimoCorpo) {
          idInvio = generaIdInvio();
          ultimoCorpo = corpo;
        }
        payload.submission_id = idInvio;
        // Il browser può ripristinare i campi senza emettere input/change.
        if (!iniziato) { iniziato = traccia('Inizio modulo proprietari', form); }
        traccia('Invio modulo proprietari', form);
        var controller = new AbortController();
        timer = setTimeout(function () { controller.abort(); }, 18000);
        var risposta = await window.fetch(form.action, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'same-origin',
          body: JSON.stringify(payload),
          signal: controller.signal,
        });
        // Il limite di Caddy può rispondere in testo semplice, senza JSON.
        if (risposta.status === 429) {
          throw new Error('Hai effettuato più tentativi in poco tempo. Attendi qualche minuto e riprova.');
        }
        var esito = await risposta.json();
        if (!risposta.ok || esito.accepted !== true) {
          if (risposta.status === 422) {
            throw new Error('Controlla nome, telefono e gli altri campi del modulo, poi riprova.');
          }
          throw new Error();
        }
        // Il tracker usa keepalive: la navigazione non interrompe l'invio dell'evento.
        traccia('Richiesta proprietari accettata', form);
        try {
          if (typeof window.fbq === 'function') { window.fbq('track', 'Lead'); }
        } catch (errorePixel) { /* Il Pixel non deve impedire la conferma. */ }
        window.location.assign(PAGINA_GRAZIE);
      } catch (errore) {
        stato.textContent = errore.message && /^(Hai effettuato|Controlla nome)/.test(errore.message)
          ? errore.message
          : 'Non siamo riusciti a confermare l’invio. I dati sono ancora qui: riprova tra poco oppure contattaci via WhatsApp.';
        stato.hidden = false;
      } finally {
        clearTimeout(timer);
        inInvio = false;
        bottone.disabled = false;
        bottone.textContent = testoBottone;
        form.removeAttribute('aria-busy');
      }
    });
  }

  function avvia() {
    var moduli = document.querySelectorAll('form[data-gp-form]');
    for (var i = 0; i < moduli.length; i++) { prepara(moduli[i]); }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', avvia);
  } else {
    avvia();
  }
})();
