# AGENTS.md — Green Property site

## Repo layout

```
gp-site/
  .github/workflows/hugo.yml   # GitHub Pages deploy (main branch)
  site/                        # ← all Hugo work happens here
    config/_default/           # hugo.toml, languages.toml, params.toml, menus.it.toml
    content/italian/           # Italian-only content (no english dir exists)
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

- **Apartments (booking):** `site/content/italian/booking/*.md`
  - Frontmatter fields: `title`, `layout: "booking/single"`, `address`, `price_per_night`, `cleaning_fee`, `max_guests`, `bedrooms`, `bathrooms`, `square_meters`, `latitude`, `longitude`, `main_image`, `image_webp`, `image`, `gallery` (array of paths), `amenities` (array of `{name, icon}`)
- **Other sections:** `blog/`, `project/`, `team/`, `advantages/`, `apartment/`, `contact.md`, `search.md`, `values.md`, `privacy-policy.md`, `terms.md`

## Images

- Format: **WebP preferred** (JPG fallback). Stored in `site/static/images/apartments/`
- Referenced in frontmatter as `images/apartments/<name>-N.webp` (relative to `static/`)
- `scripts/convert_to_webp.fish` — batch convert JPGs to WebP
- `scripts/create_apartments.py` — auto-generate apartments with AI images via Replicate API (needs `REPLICATE_API_TOKEN`)
- `scripts/generate_apartment_images.py` — generate images for a single apartment

## Config highlights

- Single language: Italian (`defaultContentLanguage = 'it'`, `defaultContentLanguageInSubdir = true`)
- Theme: `bexer-hugo` (gethugothemes commercial theme)
- Timezone: `Europe/Rome`
- Contact form: uses Airform (`airform.io/info@greenproperty.it`)
- Prettier configured with `go-template` parser for `.html` files

## Deploy

- **GitHub Pages:** `.github/workflows/hugo.yml` — builds on push to `main`, deploys to GitHub Pages
- **Netlify:** `netlify.toml` — `yarn project-setup && yarn build`
- **Vercel:** `vercel.json` + `vercel-build.sh` — installs Go + Hugo extended, runs project-setup + build
- **GitLab CI:** `site/.gitlab-ci.yml` — similar to Vercel flow

## Gotchas

- `public/`, `resources/`, `.hugo_build.lock` are gitignored — do not commit build artifacts
- The `project-setup` script is destructive: it moves files from root-level `layouts/`, `assets/`, `static/` into `themes/bexer-hugo/` and deletes `exampleSite/`. Only run once on a fresh theme checkout.
- This repo is Italian-only — no `content/english/` directory exists despite languages.toml having an `[en]` block
- Hugo **extended** version required (for SCSS/SASS processing)
