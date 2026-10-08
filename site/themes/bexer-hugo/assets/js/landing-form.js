/* Moduli lead della landing /advantages/ (partials/landing/form.html).
   Invio in pagina verso Airform (che accetta richieste dal browser) e poi pagina di ringraziamento;
   se l'invio fallisce il modulo resta compilato e compare l'avviso con il telefono.
   Senza JavaScript il modulo funziona comunque con il POST normale. */
(function () {
  'use strict';

  var TESTO_INVIO = 'Invio in corso…';

  function vaiAlGrazie(form) {
    window.location.assign(form.getAttribute('data-thanks') || '/');
  }

  function inviaModulo(form, evento) {
    var bottone = form.querySelector('button[type="submit"]');
    var errore = form.querySelector('[data-gp-error]');
    var trappola = form.querySelector('input[name="sito_web"]');

    evento.preventDefault();
    if (errore) { errore.hidden = true; }

    // Campo trappola compilato: è un bot. Si finge successo, senza inviare niente.
    if (trappola && trappola.value) {
      vaiAlGrazie(form);
      return;
    }

    var testoOriginale = bottone ? bottone.textContent : '';
    if (bottone) { bottone.disabled = true; bottone.textContent = TESTO_INVIO; }

    // Stesso formato del POST normale (application/x-www-form-urlencoded): niente preflight.
    fetch(form.getAttribute('action'), {
      method: 'POST',
      body: new URLSearchParams(new FormData(form))
    }).then(function (risposta) {
      if (!risposta.ok) { throw new Error('HTTP ' + risposta.status); }
      vaiAlGrazie(form);
    }).catch(function () {
      if (errore) { errore.hidden = false; }
      if (bottone) { bottone.disabled = false; bottone.textContent = testoOriginale; }
    });
  }

  function avvia() {
    var moduli = document.querySelectorAll('form[data-gp-form]');
    for (var i = 0; i < moduli.length; i++) {
      (function (form) {
        form.addEventListener('submit', function (evento) { inviaModulo(form, evento); });
      })(moduli[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', avvia);
  } else {
    avvia();
  }
})();
