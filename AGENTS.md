# AGENTS.md — Green Property site

## Repo layout

```
gp-site/
  .github/workflows/hugo.yml   # GitHub Pages deploy (main branch)
  site/                        # ← all Hugo work happens here
    config/_default/           # hugo.toml, languages.toml, params.toml, menus.it.toml
    content/italian/           # Homepage proprietari, grazie e pagine legali
    content/english/           # Bozze legali conservate; lingua non pubblicata
    themes/bexer-hugo/         # theme (layouts + assets)
    scripts/                   # Python apartment/image generators, projectSetup.js
    netlify.toml               # Netlify deploy config
    vercel.json + vercel-build.sh  # Vercel deploy config
    .gitlab-ci.yml             # GitLab CI deploy config
    public/                    # build output (gitignored)
```

## Commands (always run from `site/`)

```bash
cd site
npm run dev       # Hugo dev server
npm run build     # Production build (minified, gc, drafts+future included)
npm run test      # Dev server in production mode (minified, no fast render)
npm run format    # Prettier (uses go-template parser for .html)
npm run project-setup  # One-time: moves layouts/assets/static into themes/bexer-hugo/
npm run theme-setup    # Inverse of project-setup: extracts theme files back to root
```

## Content structure

- **Homepage proprietari (`/`, solo IT):** `site/content/italian/_index.md` → `themes/bexer-hugo/layouts/index.html`, sezioni in `layouts/partials/landing/`, recensioni in `data/recensioni_proprietari.json`, logica in `assets/js/landing-recensioni.js`, immagini in `static/images/landing/`.
- **Modulo:** `assets/js/landing-form.js` invia a `/api/leads`; backend Resend in `deploy/lead-form/`. Successo e honeypot portano a `/grazie/`, ma soltanto il successo Resend genera una conversione.
- **Pagine di supporto:** `/grazie/`, `/privacy-policy/`, `/terms/`; eventuali bozze legali restano preservate.
- Blog, casi studio, appartamenti, team, ricerca e vecchia landing `/advantages/` sono rimossi. **Nessun redirect** dai vecchi percorsi: devono rispondere 404. Niente menu di sezioni o newsletter.
- Verifica build: `python3 scripts/check_single_page_site.py public` dalla directory `site/`. Controlla pagine, link, form, sitemap e assenza di vecchi percorsi e redirect.

## Images

- Format: **WebP preferred** (JPG fallback). Stored in `site/static/images/apartments/`
- Referenced in frontmatter as `images/apartments/<name>-N.webp` (relative to `static/`)
- `scripts/convert_to_webp.fish` — batch convert JPGs to WebP
- `scripts/create_apartments.py` — auto-generate apartments with AI images via Replicate API (needs `REPLICATE_API_TOKEN`)
- `scripts/generate_apartment_images.py` — generate images for a single apartment

## Config highlights

- Solo italiano pubblicato alla root; inglese disabilitato tramite `disableLanguages` (sorgenti legali conservati).
- Theme: `bexer-hugo` (gethugothemes commercial theme)
- Timezone: `Europe/Rome`
- Contact form: endpoint `/api/leads` sullo stesso dominio, Resend; documentazione in `deploy/lead-form/README.md`.
- Prettier configured with `go-template` parser for `.html` files

## Deploy

- **Produzione Hetzner:** `.github/workflows/deploy.yml` — test, build Hugo e verifica dei percorsi su push `main`, poi rsync con `--delete` per rimuovere anche i vecchi file pubblicati. Caddy esistente serve i file e `/api/leads`.
- **Netlify:** `netlify.toml` — `yarn project-setup && yarn build`
- **Vercel:** `vercel.json` + `vercel-build.sh` — installs Go + Hugo extended, runs project-setup + build
- **GitLab CI:** `site/.gitlab-ci.yml` — similar to Vercel flow

## Gotchas

- `public/`, `resources/`, `.hugo_build.lock` are gitignored — do not commit build artifacts
- The `project-setup` script is destructive: it moves files from root-level `layouts/`, `assets/`, `static/` into `themes/bexer-hugo/` and deletes `exampleSite/`. Only run once on a fresh theme checkout.
- Hugo **extended** version required (for SCSS/SASS processing)
