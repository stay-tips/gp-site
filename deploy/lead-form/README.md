# Modulo proprietari senza CAPTCHA

Backend separato per sostituire Airform: il browser invia al proprio dominio,
Caddy inoltra al container `gp-leads`, Resend accetta l'email destinata a
`info@greenproperty.it`. Nessun database aggiuntivo, nessun dato del modulo in
Umami o nei log. Questi file non attivano da soli il servizio o il frontend.

Attivo dal 14 ottobre 2026 su `37.27.202.56`, progetto Compose
`greenproperty-leads` in `/opt/stack/greenproperty-leads/`. Il mittente iniziale
è `Green Property <no-reply@updates.stay.tips>`, già funzionante con la chiave
Resend sending-only esistente. Il destinatario è `info@greenproperty.it`.
I due moduli sono sulla homepage `/`, con conferma in `/grazie/`.
Il servizio email viene aggiornato separatamente dal deploy del sito statico.
Prima di aggiornare il frontend verificare che il backend sia pronto.

La configurazione Caddy precedente all'attivazione è conservata sul server in
`/opt/stack/Caddyfile.pre-gp-leads-20261014T105045Z`.

## Contratto frontend

`POST /api/leads`, `Content-Type: application/json`, stessa origine
`https://greenproperty.it`. Campi stringa del form attuale: `nome`, `telefono`,
`email` (facoltativo), `citta`, `tipo`, `note` (facoltativo), `privacy=accettata`,
`sito_web` (honeypot). `_subject` viene ignorato; mittente, oggetto e destinatario
sono fissati dal backend. Aggiungere `form_id` (`gp-form-1` o `gp-form-2`) e
`submission_id` (UUID v4).

Conservare lo stesso UUID quando si ritenta **lo stesso contenuto**; generarne
uno nuovo se cambia il payload. Non aggiungere timestamp variabili alle richieste
di retry. Resend deduplica per 24 ore con `Idempotency-Key`.

| HTTP | Risposta | Comportamento frontend |
| --- | --- | --- |
| 201 | `{ "accepted": true }` | Conferma, evento Umami senza dati personali, pagina grazie |
| 200 | `{ "accepted": false }` | Honeypot: nessun evento di conversione |
| 422 | `{ "accepted": false, "error": "invalid_fields", "fields": [...] }` | Invitare a correggere i campi, conservare i valori |
| 429 | `{ "accepted": false, "error": "rate_limited" }` + `Retry-After` | Attendere; conservare valori e UUID |
| 409 | `{ "accepted": false, "error": "submission_conflict" }` | Retry stesso payload/UUID se simultaneo; nuovo UUID solo dopo modifica |
| 502/503 | `{ "accepted": false, "error": "..." }` | Messaggio di errore e retry con stesso UUID |

Il frontend deve controllare `accepted === true`, non soltanto `response.ok`.
L'accettazione da parte di Resend non certifica la consegna alla casella. Un
eventuale evento di consegna richiede in seguito un webhook firmato del provider.
Il backend accetta soltanto JSON: con JavaScript disabilitato il sito deve offrire
un contatto telefonico con `<noscript>`, senza provare il POST HTML.

## Controlli

- Validazione lato server, consenso obbligatorio, limiti per campo, body massimo
  12 KiB anche senza `Content-Length`; email soltanto testuale.
- Honeypot lato server; origine esatta e content type JSON. Non sono una prova di
  umanità: un bot può simulare questi valori.
- Caddy limita 5 richieste per IP (IPv6 /64) ogni 15 minuti; applicazione con un
  secondo limite 5/15 min e budget totale 100 richieste/ora. I retry consumano il
  budget. Tre invii Resend contemporanei, timeout provider 12 secondi.
- Il container non pubblica porte. Caddy sovrascrive `X-Real-IP` con l'IP della
  connessione, indipendentemente dagli header del chiamante. Il backend ignora
  `X-Forwarded-For` e rifiuta richieste prive di un IP valido.
- Rate limit in memoria: un riavvio dell'app azzera il budget globale. Fare
  `caddy reload` conserva i contatori dell'edge; non ricreare Caddy per questo cambio.
- Nessuna conferma di successo quando Resend fallisce. Il browser conserva i dati
  per il retry; non esiste una coda locale di richieste non accettate.

## Verifiche locali

```sh
node --test deploy/lead-form/server.test.mjs
```

I test usano HTTP locale e un adapter Resend simulato: nessuna email viene inviata.

Il 14 ottobre 2026 è stato verificato anche Resend reale con un destinatario
simulatore `delivered+gp-form-smoke@resend.dev`: accettazione e stesso receipt
sul retry con chiave idempotente. Nessuna email di prova inviata a persone.

Controllo servizio, senza leggere i segreti:

```sh
ssh hetzner 'cd /opt/stack/greenproperty-leads && docker compose ps'
ssh hetzner 'cd /opt/stack/greenproperty-leads && docker compose logs --tail 20 leads'
```

## Attivazione sullo stack esistente

1. Copiare `server.mjs` e `compose.yaml` in `/opt/stack/greenproperty-leads/`.
   L'immagine Node è fissata al digest multiarch verificato il 14 ottobre 2026.
2. Creare `.env` con permessi `600` da `.env.example`, solo sul server. La chiave
   Resend sending-only attualmente usata da NocoDB vive in `NC_SMTP_PASSWORD`;
   copiarla in `RESEND_API_KEY` senza stamparla. `LEAD_FROM` deve essere consentito
   dalla chiave e dal dominio verificato. Non copiare l'intero `.env` dello stack.
3. Avviare soltanto il nuovo progetto Compose; controllare `/health` internamente.
4. Unire `Caddy.fragment` al blocco `greenproperty.it` esistente in
   `/opt/stack/Caddyfile`, prima di `file_server`. Il file completo contiene altri
   servizi: **non sostituirlo** con questo frammento. Validare la configurazione
   col container Caddy custom già in servizio, poi eseguire `caddy reload`.
5. Collegare entrambi i form al backend; mantenere il normale sito statico.
   Verificare successo, errore e retry senza inviare richieste a persone.

Per un test d'integrazione provider usare esclusivamente i
[destinatari simulatori ufficiali Resend](https://resend.com/docs/dashboard/emails/send-test-emails),
ad esempio `delivered+gp-form-smoke@resend.dev`, con testo sintetico. Il destinatario
dell'endpoint pubblico resta sempre `info@greenproperty.it`: il test del provider
si esegue separatamente, non rendendo configurabile il destinatario dal browser.
Questi test consumano quota del provider.

Rollback: ripristinare il frontend Airform, togliere soltanto l'handler `/api/leads`
da Caddy e ricaricare; fermare il progetto `greenproperty-leads`. Non toccare i
container esistenti, i loro volumi o lo stack Umami.

Riferimenti: [Resend send email](https://resend.com/docs/api-reference/emails/send-email),
[idempotency keys](https://resend.com/docs/dashboard/emails/idempotency-keys).
