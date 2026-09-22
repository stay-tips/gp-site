/* Recensioni proprietari (landing /advantages/): filtro per città, paginazione e "leggi tutto".
   I dati arrivano dal JSON inline #gp-recensioni-data (data/recensioni_proprietari.json). */
(function () {
  'use strict';

  var PAGINA = 6;
  var SOGLIA_TESTO_LUNGO = 180;
  var TAGLIO_TESTO = 170;
  var DATA_RIFERIMENTO = new Date(2026, 8, 20);
  var COLORI = ['#1A73E8', '#188038', '#D93025', '#E37400', '#9334E6', '#00838F', '#5F6368', '#C5221F', '#7B1FA2', '#0B8043'];
  var MESI = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic'];
  var BADGE_VERIFICATA = '<svg width="14" height="14" viewBox="0 0 24 24" aria-label="Verificata"><path fill="#1A73E8" d="M12 2 9.2 4.4 5.6 4l-.5 3.6L2 9.6l1.9 3.1L2.5 16l3.5 1.1.4 3.6 3.6-.4L12 23l2-2.7 3.6.4.4-3.6 3.5-1.1-1.4-3.3L22 9.6l-3.1-2-.5-3.6-3.6.4z"></path><path fill="#FFFFFF" d="m10.2 16.2-3.4-3.4 1.4-1.4 2 2 5.6-5.6 1.4 1.4z"></path></svg>';

  function escapeHtml(testo) {
    return String(testo)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function etichettaData(n) {
    var settimane = (n * 7) % 52 + 1;
    if (settimane < 5) return settimane + (settimane === 1 ? ' settimana fa' : ' settimane fa');
    var d = new Date(DATA_RIFERIMENTO.getTime());
    d.setDate(d.getDate() - settimane * 7);
    return MESI[d.getMonth()] + ' ' + d.getFullYear();
  }

  function testoVisibile(recensione, aperta) {
    var lungo = recensione.testo.length > SOGLIA_TESTO_LUNGO;
    if (!lungo || aperta) return recensione.testo;
    return recensione.testo.slice(0, TAGLIO_TESTO).replace(/\s+\S*$/, '') + '…';
  }

  function cardHtml(recensione, aperta, logoGoogle) {
    var lungo = recensione.testo.length > SOGLIA_TESTO_LUNGO;
    var toggle = lungo
      ? '<button type="button" class="gp-link-muted" data-toggle-recensione="' + recensione.n + '" style="align-self:flex-start; margin-top:6px; padding:0; border:none; background:none; cursor:pointer; font:inherit; font-size:13.5px; font-weight:500; color:#5F6368;">' + (aperta ? 'Mostra meno' : 'Leggi tutto') + '</button>'
      : '';
    return '<div class="gp-review gp-google">' +
      '<div style="display:flex; align-items:center; gap:12px;">' +
        '<div style="width:40px; height:40px; border-radius:50%; background:' + COLORI[recensione.n % COLORI.length] + '; color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:17px; font-weight:500; flex-shrink:0;">' + escapeHtml(recensione.nome.charAt(0)) + '</div>' +
        '<div style="min-width:0;">' +
          '<div style="font-size:14.5px; font-weight:500; color:#202124; display:flex; align-items:center; gap:5px;">' + escapeHtml(recensione.nome) + BADGE_VERIFICATA + '</div>' +
          '<div style="font-size:12.5px; color:#5F6368; margin-top:2px;">Proprietario · ' + escapeHtml(recensione.citta) + '</div>' +
        '</div>' +
        '<span style="margin-left:auto; display:flex;">' + logoGoogle + '</span>' +
      '</div>' +
      '<div style="display:flex; align-items:center; gap:8px; margin-top:12px;">' +
        '<span style="color:#FBBC04; font-size:15px; letter-spacing:1px; line-height:1;">★★★★★</span>' +
        '<span style="font-size:12.5px; color:#5F6368;">' + etichettaData(recensione.n) + '</span>' +
      '</div>' +
      '<p style="font-size:14px; line-height:1.55; color:#3C4043; margin:10px 0 0; flex:1;">' + escapeHtml(testoVisibile(recensione, aperta)) + '</p>' +
      toggle +
    '</div>';
  }

  function filtra(recensioni, filtro) {
    var ordinate = recensioni.slice().sort(function (a, b) { return a.n - b.n; });
    return filtro === 'Tutte' ? ordinate : ordinate.filter(function (r) { return r.citta === filtro; });
  }

  function leggiDati(el) {
    try {
      var dati = JSON.parse(el.textContent);
      return Array.isArray(dati) ? dati : [];
    } catch (err) {
      console.error('[recensioni] JSON non valido:', err);
      return [];
    }
  }

  function avvia() {
    var datiEl = document.getElementById('gp-recensioni-data');
    var lista = document.getElementById('gp-recensioni-lista');
    var filtroEl = document.getElementById('gp-recensioni-filtro');
    var label = document.getElementById('gp-recensioni-label');
    var altre = document.getElementById('gp-recensioni-altre');
    var logoTpl = document.getElementById('gp-google-logo');
    if (!datiEl || !lista || !filtroEl || !label || !altre) return;

    var recensioni = leggiDati(datiEl);
    var logoGoogle = logoTpl ? logoTpl.innerHTML : '';
    var stato = { filtro: 'Tutte', limite: PAGINA, aperte: {} };

    function render() {
      var filtrate = filtra(recensioni, stato.filtro);
      var visibili = filtrate.slice(0, stato.limite);
      lista.innerHTML = visibili.map(function (r) { return cardHtml(r, !!stato.aperte[r.n], logoGoogle); }).join('');
      label.textContent = visibili.length + ' di ' + filtrate.length + ' recensioni';
      altre.hidden = filtrate.length <= stato.limite;
    }

    filtroEl.addEventListener('change', function (e) {
      stato = Object.assign({}, stato, { filtro: e.target.value, limite: PAGINA });
      render();
    });
    altre.addEventListener('click', function () {
      stato = Object.assign({}, stato, { limite: stato.limite + PAGINA });
      render();
    });
    lista.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-toggle-recensione]');
      if (!btn) return;
      var n = btn.getAttribute('data-toggle-recensione');
      var aperte = Object.assign({}, stato.aperte);
      aperte[n] = !aperte[n];
      stato = Object.assign({}, stato, { aperte: aperte });
      render();
    });

    render();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', avvia);
  else avvia();
})();
