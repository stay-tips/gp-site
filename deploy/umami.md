# Umami — Green Property

Attivato il 14 ottobre 2026 su `37.27.202.56`.

- Dashboard: https://stats.greenproperty.it (account amministratore `admin`).
- Website ID: `bb00791e-37cf-49f9-93a5-03d506b8d827`.
- Configurazione Hugo: `site/config/production/hugo.toml`.
- Tracker: `site/themes/bexer-hugo/layouts/partials/analytics.html`, incluso da `head.html`.
- Solo produzione e domini `greenproperty.it` / `www.greenproperty.it`; rispetta Do Not Track ed esclude query string e frammenti. Le campagne UTM non vengono raccolte con questa configurazione.

## Heatmap

La raccolta richiede sia `script.js` sia `recorder.js`, nello stesso ordine e
con lo stesso website ID. Il tracker fornisce la sessione al recorder: quando
il tracker è disattivato (sviluppo, dominio diverso o Do Not Track), il recorder
non dispone della sessione necessaria per inviare clic e scorrimenti.

In Umami → Websites → Green Property → Replays & Heatmaps, le heatmap sono
abilitate con campionamento 100%; le registrazioni delle sessioni restano spente.
L'API `/api/websites/{websiteId}/recorder` deve restituire `enabled: true`,
`heatmapEnabled: true` e `heatmapSampleRate: 1`. Le visite raccolte prima
dell'attivazione non contengono i dati necessari per ricostruire una heatmap.

Verifica delle pagine pubblicate (dalla directory `site/`):

```bash
ssh hetzner 'python3 - https://greenproperty.it/ https://greenproperty.it/en/ https://greenproperty.it/advantages/' < scripts/check_umami.py
```

## Servizio

Umami 3.4.0 in Docker, immagine fissata anche tramite digest, stack
`greenproperty-umami` in `/opt/stack/umami`. Limite RAM 768 MiB, CPU 1.
Database e ruolo dedicati `umami` nel PostgreSQL 16 esistente; nessuna porta
database pubblica. Caddy inoltra `stats.greenproperty.it` a `gp-umami:3000`
sulla rete Docker `n8n-nocodb_backend`.

I file infrastrutturali sono nel repository `stay-tips/devops`, directory
`tools/n8n-nocodb/prod/umami/`, e il virtual host nel relativo `prod/Caddyfile`.

```bash
ssh hetzner 'cd /opt/stack/umami && docker compose ps'
ssh hetzner 'cd /opt/stack/umami && docker compose logs --tail 50 umami'
curl --fail https://stats.greenproperty.it/api/heartbeat
```

La password iniziale è stata sostituita prima di esporre il servizio.
Credenziali in `/opt/stack/umami/credentials.json` e segreti in `.env`, entrambi
con permessi 600. Sul Mac, le credenziali della dashboard sono in
`deploycredentials.md` alla radice di questo repository (escluso da Git);
la copia dei segreti del server resta in `~/.config/greenproperty/umami-server.env`.
La chiave 2FA è predisposta; l'abilitazione del secondo fattore si fa dal profilo.

## Backup e ripristino

`/etc/cron.d/greenproperty-umami` esegue ogni giorno alle 03:20 (ora del server)
`/opt/stack/umami/backup.sh`. Conserva circa 14 giorni di dump PostgreSQL custom
in `/opt/stack/umami/backups`. I dump sono locali al server.

Per recuperare un dump, fermare prima Umami e ripristinarlo in un database vuoto
di proprietà del ruolo `umami`, usando `pg_restore --no-owner --no-acl --role=umami`.
Conservare anche `.env`: contiene le chiavi di autenticazione e cifratura 2FA.

## Disattivazione

Impostare `params.umami.enabled = false` e pubblicare il sito per interrompere
la raccolta. `docker compose stop umami` dalla directory dello stack ferma il
servizio mantenendo database e configurazione. Non eliminare database o segreti.
