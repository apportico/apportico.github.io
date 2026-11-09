# Apportico app collection

Public app showcase: https://apportico.com/

Static HTML and CSS, no build step required. The root `index.html` is the showcase, using `apps/style.css` and `apps/assets/`. The legacy `/apps/` address redirects to the homepage. Existing app support and privacy pages stay at their original paths.

## Local development

Run `python -m http.server 8000` from the repository root, then open http://localhost:8000/. Validate the root page, legacy redirect, asset paths, App Store links, and phone/desktop layouts after edits.

## Assets and listings

See [apps/README.md](apps/README.md) for asset provenance. Add only verified public App Store listings; do not publish private release information.

## Hosting

GitHub Pages serves this repository. The `CNAME` file contains `apportico.com`; configure the matching domain in repository Settings → Pages. Keep DNS ownership verification in place and enable Enforce HTTPS once the certificate is available.

## App gallery and detail pages

The homepage has compact cards with separate detail and App Store links. Each verified app has a page at `/apps/<slug>/`. Existing root-level support and privacy routes are deliberately preserved.

To add or update an app, edit `apps/catalog.json` using verified public listing information and add its official assets in `apps/assets/`. The shared home layout is `apps/home-template.html` and the detail layout is in `scripts/build_catalog.py`.

Run `python scripts/build_catalog.py` then `python scripts/check_catalog.py`. Commit the catalog, generated `index.html`, and generated app detail pages together. Serving is still buildless: no runtime JavaScript or framework needed. Test desktop and narrow phone widths before publication.
