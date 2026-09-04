# website

The public website for **Nairi Quantum** — https://nairiquantum.org

This is a separate repository (not part of `sim`/`sdr`/`tools`/`docs`). It is a single, self-contained
static page — no build tools or frameworks needed to serve it.

## Files
- **`index.html`** — the whole site (logo embedded as a data URI, so the page is self-contained).
- **`build_site.py`** — regenerates `index.html`: it reads the logo PNG, embeds an optimized copy, and
  writes the HTML. Edit the template/colors here, then re-run.
- **`EC_journal.pdf`** — the Engineering City article, linked from the site's Press section.
- **`README.md`** — this file.

## Editing
`index.html` is **generated** — don't hand-edit it for anything the generator controls. Instead:
1. Edit `build_site.py` (the HTML template, palette, or sections).
2. Run it (requires Python + Pillow): `python build_site.py`
3. Commit the updated `index.html`.
Small one-off text tweaks directly in `index.html` are fine, but re-running the generator will overwrite them.

## Deployment (GitHub Pages + Cloudflare)
1. This repo is **public** (Pages is free on public repos). **Do not** grant the sub-teams write access —
   members can view but only the owner edits.
2. **Settings → Pages** → Deploy from a branch → `main` / root.
3. **Settings → Pages → Custom domain** → `nairiquantum.org`.
4. In **Cloudflare DNS**, add (all **DNS only** / grey cloud):
   - `A  @  185.199.108.153` · `185.199.109.153` · `185.199.110.153` · `185.199.111.153`
   - `CNAME  www  nairi-quantum.github.io`
   - Delete any old root `CNAME → www` loop.
5. Enable **Enforce HTTPS** in Pages once the certificate is issued.

## Notes
- Fully self-contained and light: system fonts, one small canvas animation, no external requests.
- The Press link points to `EC_journal.pdf` in this repo (works on the live site).
