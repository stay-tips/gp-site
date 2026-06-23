# Deploy in produzione — Green Property (Hetzner + Caddy)

## Contesto
Sito **statico generato con Hugo** (extended), multilingua IT/EN.
- Repo: `github.com/stay-tips/gp-site` — il progetto Hugo è nella sottocartella `site/`.
- Lingua default **italiano** servito alla root; inglese sotto `/en/`.
- Dominio di produzione: **greenproperty.it** (il `www` deve redirezionare all'apex).
- Server: VPS **Hetzner già esistente** (Debian/Ubuntu), accesso SSH disponibile. **Caddy NON è installato.**
- Strategia deploy: **GitHub Actions automatico** ad ogni push su `main` (build in CI + `rsync` su server via SSH). Caddy serve i file statici con HTTPS automatico (Let's Encrypt).

## Cosa è GIÀ pronto nel repo (non rifare)
- `.github/workflows/deploy.yml` → build `hugo --minify --gc --environment production` + `rsync --delete site/public/ → $HETZNER_DEPLOY_PATH`.
- `deploy/Caddyfile` → config Caddy di riferimento (apex + redirect www, gzip/zstd, cache asset, 404 Hugo).
- `site/config/production/hugo.toml` → `baseURL = "https://greenproperty.it/"`.

## Cosa fare

### 1. Server: installare Caddy
Repo ufficiale Caddy (apt) + `rsync`. Caddy gira come servizio systemd, utente `caddy`.

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update && sudo apt install -y caddy rsync
```

### 2. Server: utente e cartella di deploy
- Creare utente `deploy` (o equivalente) per il deploy via SSH.
- `mkdir -p /var/www/greenproperty`, owner `deploy`, permessi tali che l'utente `caddy` possa leggere (`755` su `/var/www` e sulla dir).

```bash
sudo useradd -m -s /bin/bash deploy
sudo mkdir -p /var/www/greenproperty
sudo chown -R deploy:deploy /var/www/greenproperty
sudo chmod 755 /var/www /var/www/greenproperty
```

### 3. Server: configurare Caddy
- Copiare il contenuto di `deploy/Caddyfile` in `/etc/caddy/Caddyfile`.
- `sudo systemctl reload caddy`.
- Aprire le porte **80** e **443** (firewall/ufw); SSH già aperta.

```bash
sudo ufw allow 80,443/tcp   # se usi ufw
```

### 4. Chiave SSH di deploy
- Generare keypair ed25519 dedicato.
- Pubblica → `authorized_keys` dell'utente `deploy`.
- Privata → secret GitHub (sotto).

```bash
ssh-keygen -t ed25519 -f gp_deploy_key -C "gh-actions-deploy" -N ""
ssh-copy-id -i gp_deploy_key.pub deploy@IP_DEL_SERVER
```

### 5. GitHub → Settings → Secrets and variables → Actions
Creare i secret usati dal workflow:

| Secret | Valore |
|--------|--------|
| `HETZNER_HOST` | IP/hostname del server |
| `HETZNER_USER` | `deploy` |
| `HETZNER_SSH_KEY` | chiave **privata** ed25519 (intero contenuto di `gp_deploy_key`) |
| `HETZNER_DEPLOY_PATH` | `/var/www/greenproperty` |
| `HETZNER_SSH_PORT` | porta SSH (opzionale, default 22) |

### 6. DNS (registrar del dominio)
- `A greenproperty.it → IP_SERVER`
- `A www.greenproperty.it → IP_SERVER`
- Attendere la propagazione prima del primo deploy (Caddy emette il certificato solo con DNS già puntato e porte 80/443 aperte).

### 7. Primo deploy e verifica
- Lanciare il workflow (push su `main` o "Run workflow" dalla tab Actions).

**Acceptance criteria:**
- `https://greenproperty.it` risponde in HTTPS valido e mostra il sito in **italiano**.
- `https://greenproperty.it/en/` mostra la versione **inglese**.
- `http://...` e `https://www.greenproperty.it` redirezionano a `https://greenproperty.it`.
- Il workflow GitHub Actions termina verde; un secondo push aggiorna i file (verificare che `rsync --delete` non lasci file orfani).

## Vincoli / note
- Hugo **extended** richiesto (lo SCSS usa `toCSS`); versione in CI: `0.163.1` (allineata al locale). Mantenere allineate CI e ambiente di sviluppo.
- Non committare segreti nel repo. La build NON richiede Dart Sass (libsass integrato in Hugo extended).
- Sito 100% statico: nessun runtime/app server, nessun database. Deploy = sincronizzazione di file.
