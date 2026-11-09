# Apportico app collection

Public app showcase: https://apportico.com/

Static HTML and CSS, no build step required. The root `index.html` is the showcase, using `apps/style.css` and `apps/assets/`. The legacy `/apps/` address redirects to the homepage. Existing app support and privacy pages stay at their original paths.

## Local development

Run `python -m http.server 8000` from the repository root, then open http://localhost:8000/. Validate the root page, legacy redirect, asset paths, App Store links, and phone/desktop layouts after edits.

## Assets and listings

See [apps/README.md](apps/README.md) for asset provenance. Add only verified public App Store listings; do not publish private release information.

## Hosting

GitHub Pages serves this repository. The `CNAME` file contains `apportico.com`; configure the matching domain in repository Settings → Pages. Keep DNS ownership verification in place and enable Enforce HTTPS once the certificate is available.
