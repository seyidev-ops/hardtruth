# The House — Austine Ojo · landing page

A single-book landing page for **The House — 2nd Corinthians 5:17** by **Austine Ojo**.
Static HTML, built from structured content, deployed to GitHub Pages.

**Live:** https://seyidev-ops.github.io/hardtruth/

## How it is put together

| Path | What it holds |
|---|---|
| `site.config.json` | **One place** for the site origin, Facebook link, purchase URL, offer, indexing and verification IDs |
| `content/chapters.json` | The 15 chapter titles, briefs and manuscript page references (references are not published) |
| `src/index.template.html` | Page markup with `{{TOKENS}}` filled at build time |
| `src/styles.css`, `src/main.js` | Styles (Day/Night tokens) and progressive enhancements (theme switch, mobile menu, gentle reveal) |
| `assets/` | The four supplied images, unchanged |
| `seo/*.template` | Sitemap and robots templates (`{{SITE_ORIGIN}}`) |
| `scripts/build.py` | Builds everything into `dist/` and fails if tokens, placeholders or private files would ship |
| `.github/workflows/deploy.yml` | Builds and publishes `dist/` to the `gh-pages` branch on every push to `main` |
| `BUILD_BRIEF.md` | The original build specification |

## Build locally

```bash
pip install Pillow
python3 scripts/build.py
cd dist && python3 -m http.server 8000   # open http://localhost:8000
```

## Common updates

- **Purchase link becomes available:** set `purchaseUrl` in `site.config.json`. Every primary button switches to **Get Your Copy** automatically. Add price/format to the page copy only once confirmed.
- **Stable Facebook page URL:** replace `facebookUrl`.
- **Custom domain:** set `siteOrigin` to the new https origin, add the domain under repo Settings → Pages → Custom domain, and point DNS at GitHub Pages. Canonical, Open Graph, JSON-LD, sitemap and robots all update from `siteOrigin`.
- **Hide from search (preview mode):** set `indexable` to `false` (adds `noindex`).
- **Search Console / Bing:** paste the verification codes into `googleSiteVerification` / `bingSiteVerification`, push, then submit `sitemap.xml`.

## Hosting

The workflow publishes the built site to **both** the root of `main` and the `gh-pages` branch, so Pages works with either source (Settings → Pages → *Deploy from a branch* → `main` / root, or `gh-pages` / root).

These files at the repo root are **generated — do not edit them by hand**: `index.html`, `styles.css`, `main.js`, `favicon.ico`, `icons/`, `site.webmanifest`, `sitemap.xml`, `robots.txt`, `.nojekyll`, `assets/img/`. Edit `src/`, `content/` or `site.config.json` instead and push; the workflow rebuilds.

### Custom domain (hardtruthgospelmission.org)

Switching is a one-line change: in `site.config.json` set `"customDomain": "hardtruthgospelmission.org"` and push. The build then writes the `CNAME` file and moves canonical, Open Graph, JSON-LD, sitemap and robots to `https://hardtruthgospelmission.org`.

**Do this only after DNS answers**, or the github.io address will redirect to a domain that does not load. As of 10 Oct 2026:
- Nameservers `ns1/ns2.hostley.io` are not responding (registrar: PDR Ltd / PublicDomainRegistry, via Hostley).
- **The domain expires on 25 Oct 2026. Renew it first.**

DNS records to set at whichever DNS host is used:

| Type | Host | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | seyidev-ops.github.io |

After pushing the config change: Settings → Pages → confirm the custom domain shows a green DNS check, then tick **Enforce HTTPS**.

## Notes and known limits

- On a GitHub Pages *project* site (`/hardtruth/`), search engines only read `robots.txt` from the domain root, so the generated `robots.txt` becomes effective once a custom domain is used. The sitemap can still be submitted directly in Search Console.
- The supplied Facebook share link could not be verified automatically. Open it manually before promoting the site.
- The manuscript PDF, the laptop video and the video contact sheet are intentionally **not** in this repository and are blocked by the build.
- Fonts: Cormorant Garamond + Source Sans 3 from Google Fonts (`display=swap`), with Georgia/system fallbacks.

## Acceptance checklist (initial build)

- [x] Only The House promoted; "Austine Ojo" spelled consistently
- [x] All 15 chapters in order with briefs, in the initial HTML
- [x] Hero, gallery and portrait use `object-fit: contain`, intrinsic dimensions, no clipping
- [x] No manuscript, contact sheet or recording deployed
- [x] Primary/secondary actions work; no placeholder checkout, no `href="#"`
- [x] Day / Night / System persist across reloads and follow OS changes
- [x] Skip link, focus styles, 44px targets, keyboard mobile menu (Escape closes), reduced-motion respected
- [x] No horizontal overflow at 320, 375, 768, 1440 px
- [x] Canonical, Open Graph, X card metadata and JSON-LD (WebSite, WebPage, Book, Person) present and parse
- [x] Sitemap lists only the canonical homepage
- [ ] Facebook link manually tested
- [ ] Social preview checked in Facebook Sharing Debugger
- [ ] Rich Results Test / Schema validator run on the live URL
- [ ] Core Web Vitals measured from real-user data (not yet available)
