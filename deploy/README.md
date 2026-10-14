# Produzione Green Property

Il sito pubblico è una landing italiana su **https://greenproperty.it/**.
Le sezioni precedenti (blog, casi studio, appartamenti, team, ricerca e versione
inglese) sono rimosse. Non aggiungere redirect, alias Hugo, meta refresh o
redirect JavaScript dai vecchi percorsi.

## Percorsi

- `/`: landing proprietari, da `site/content/italian/_index.md` e
  `site/themes/bexer-hugo/layouts/index.html`.
- `/grazie/`: conferma del modulo, esclusa dalla sitemap e con `noindex`.
- `/privacy-policy/`, `/terms/`: pagine legali.
- `/api/leads`: endpoint email Resend sullo stesso dominio; documentato in
  [lead-form/README.md](lead-form/README.md).
- `/advantages/`, `/advantages/grazie/` e le altre sezioni eliminate
  restituiscono 404, senza inoltro automatico.

I sorgenti legali inglesi e le modifiche locali dell'utente possono restare
nel repository; `disableLanguages` impedisce la pubblicazione di `/en/`.

## Build e pubblicazione

Da `site/`:

```sh
node --test scripts/landing-form.test.cjs ../deploy/lead-form/server.test.mjs
hugo --minify --gc --cleanDestinationDir --environment production
python3 scripts/check_single_page_site.py public
```

Il controllo verifica l'insieme delle pagine HTML, i collegamenti interni,
i due form, la conferma in `/grazie/`, il funnel, la sitemap e l'assenza di
vecchi percorsi o redirect. Può includere un'eventuale bozza legale locale
`cancellazione-dati.md`, senza richiederne la pubblicazione.

Su push a `main`, `.github/workflows/deploy.yml` esegue test e build con Hugo
extended 0.163.1, poi il controllo dei percorsi. Soltanto dopo esegue
`rsync --delete`: i vecchi HTML devono sparire anche dal server, non soltanto
dalla navigazione. `public/`, `resources/` e i segreti restano fuori da Git.

## Server esistente

- Host SSH `hetzner`, IP `37.27.202.56`.
- Sito statico in `/opt/stack/www/greenproperty`, montato come
  `/var/www/greenproperty` nel Caddy Docker esistente.
- Configurazione Caddy completa: `/opt/stack/Caddyfile`. Il container usa
  l'immagine custom dello stack `n8n-nocodb`: non sostituire il file completo
  o il container con la configurazione di riferimento `deploy/Caddyfile`.
- Servizio email: progetto Compose `greenproperty-leads`.
- Umami: progetto Compose `greenproperty-umami`, dashboard
  https://stats.greenproperty.it; dettagli in [umami.md](umami.md).

Il passaggio della landing alla root avviene nei contenuti e template Hugo:
non richiede nuove regole Caddy, modifiche DNS o redirect.

## Verifica dopo il deploy

La root deve rispondere 200 direttamente, mostrare la landing e inviare il
modulo a `/api/leads`. Controllare `/grazie/`, privacy e termini, e verificare
che i vecchi percorsi restituiscano 404 senza header `Location`. I controlli
email non devono inviare richieste di prova a persone.

Per tornare alla versione precedente ripristinare il commit del sito e
ripubblicare con lo stesso workflow; non eliminare dati Umami o segreti.
