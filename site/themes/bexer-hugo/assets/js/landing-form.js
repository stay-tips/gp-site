/* Moduli lead della landing /advantages/ (partials/landing/form.html).
   L'invio resta quello normale del browser verso Airform: Airform chiede a ogni invio di confermare
   con un reCAPTCHA su una sua pagina, e un fetch in pagina salterebbe quella conferma (il lead
   non verrebbe mai consegnato). Qui si fanno solo due cose:
   - campo trappola compilato (bot): non si invia nulla e si finge successo;
   - invio di una persona: evento Lead del Meta Pixel. */
(function () {
  'use strict';

  // Pagina di ringraziamento (content/italian/advantages/grazie.md), costante e non letta dal markup.
  var PAGINA_GRAZIE = '/advantages/grazie/';

  function allInvio(form, evento) {
    var trappola = form.querySelector('input[name="sito_web"]');

    if (trappola && trappola.value) {
      evento.preventDefault();
      window.location.assign(PAGINA_GRAZIE);
      return;
    }

    // Se il Pixel è bloccato dal browser, l'invio funziona lo stesso.
    if (typeof window.fbq === 'function') { window.fbq('track', 'Lead'); }
  }

  function avvia() {
    var moduli = document.querySelectorAll('form[data-gp-form]');
    for (var i = 0; i < moduli.length; i++) {
      (function (form) {
        form.addEventListener('submit', function (evento) { allInvio(form, evento); });
      })(moduli[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', avvia);
  } else {
    avvia();
  }
})();
