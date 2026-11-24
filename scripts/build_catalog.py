"""Generate the public app catalog and canonical discovery files."""

from html import escape
import json
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parent.parent
SITE = "https://apportico.com"
APPS = json.loads((ROOT / "apps/catalog.json").read_text())
ARROW = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 19 19 5M5 5h14v14"/></svg>'
HEADER = '''<header class="wrap"><a class="brand" href="/" aria-label="Apportico home"><img class="official-logo" src="/apps/assets/apportico-logo.png" alt="" width="56" height="56">apportico</a><nav aria-label="Main navigation"><a href="/#about">The studio</a><a href="/#apps" class="nav-pill">All apps <span aria-hidden="true">→</span></a></nav></header>'''
FOOTER = '''<footer class="wrap"><a href="/" class="brand"><img class="official-logo" src="/apps/assets/apportico-logo.png" alt="" width="44" height="44">apportico</a><span>Small apps. More possibility.</span><a href="/#apps">Back to the collection ↑</a></footer>'''


def route(app):
    return f'/apps/{app["slug"]}/'


def support_links(app):
    links = []
    for key, label in (("support", "Support"), ("privacy", "Privacy")):
        default = f'/{app["slug"]}/{key}.html'
        href = app.get(key) or (default if (ROOT / default.lstrip("/")).is_file() else None)
        if href:
            links.append(f'<a href="{escape(href)}">{label}</a>')
    return f'<nav class="support-links" aria-label="App information">{"".join(links)}</nav>' if links else ""


def store_link(app, css_class, label):
    return (
        f'<a class="{css_class}" href="{escape(app["store"])}" target="_blank" rel="noopener" '
        f'aria-label="View {escape(app["name"])} on the App Store (opens in new tab)">{label} {ARROW}</a>'
    )


def card(app, index):
    name = escape(app["name"])
    path = route(app)
    platforms = escape(", ".join(app["devices"]))
    return f"""
      <article class="app-card product-{index}" id="{app["slug"]}">
        <a class="card-art" href="{path}" aria-label="Explore {name}">
          <img src="{app["icon"]}" alt="" width="112" height="112" loading="lazy">
          <span class="card-art-label">{escape(app["label"])}</span><span class="card-arrow" aria-hidden="true">{ARROW}</span>
        </a>
        <div class="card-copy"><span class="category">{escape(app["category"])}</span>
          <h3><a href="{path}">{name}</a></h3>
          <p class="card-platforms">{platforms}</p>
          <p>{escape(app["description"])}</p>
          <div class="card-actions"><a class="details-link" href="{path}" aria-label="View {name} details">View details <span aria-hidden="true">→</span></a>
            {store_link(app, "card-store", "App Store")}</div>
        </div>
      </article>"""


def related_links(app):
    return "".join(
        f'<a class="related-app" href="{route(other)}"><img src="{other["icon"]}" alt="" width="44" height="44" loading="lazy"><span>{escape(other["name"])}</span><span aria-hidden="true">{ARROW}</span></a>'
        for other in APPS if other != app
    )


def app_schema(app, canonical):
    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": app["name"],
        "url": canonical,
        "description": app["description"],
        "image": SITE + app["icon"],
        "screenshot": SITE + app["screenshot"],
        "operatingSystem": ", ".join(dict.fromkeys({
            "iPhone": "iOS", "iPad": "iPadOS", "Apple Watch": "watchOS", "Apple TV": "tvOS", "Mac": "macOS",
        }[device] for device in app["devices"])),
        "installUrl": app["store"],
        "publisher": {"@type": "Person", "name": app["publisher"]},
    }
    return json.dumps(schema, ensure_ascii=False).replace("<", "\\u003c")


def detail(app, index):
    name = escape(app["name"])
    description = escape(app["description"])
    query = escape(app["seo_title"])
    title = f"{name} | {query} | Apportico"
    canonical = SITE + route(app)
    platforms = escape(", ".join(app["devices"]))
    headline = "<br>".join(map(escape, app["headline"].split("<br>")))
    use_cases = "".join(f"<li>{escape(use)}</li>" for use in app["use_cases"])
    device = escape(app["screenshot_device"])
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#101114"><title>{title}</title>
<meta name="description" content="{description}"><link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{description}">
<meta property="og:type" content="website"><meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}{app["icon"]}"><meta name="twitter:card" content="summary">
<link rel="icon" href="/apps/assets/apportico-logo.png"><link rel="stylesheet" href="/apps/style.css">
<script type="application/ld+json">{app_schema(app, canonical)}</script>
</head><body><a class="skip" href="#app">Skip to app details</a>{HEADER}
<main id="app" class="app-detail wrap"><a class="back-link" href="/#apps">← All apps</a>
  <section class="detail-hero product-{index}" aria-labelledby="app-name">
    <div class="detail-copy">
      <div class="detail-identity">
        <img src="{app["icon"]}" alt="" width="76" height="76">
        <div><span class="category">{platforms}</span><h1 id="app-name">{name}<span>{query}</span></h1></div>
      </div>
      <p class="detail-headline">{headline}</p><p class="detail-description">{description}</p>
      <ul class="detail-use-cases">{use_cases}</ul>
      {store_link(app, "store", "View on the App Store")}
      <span class="publisher">Published by {escape(app["publisher"])}</span>
      <p class="detail-availability">Check the App Store for pricing, device requirements and availability in your country.</p>{support_links(app)}
    </div>
    <div class="detail-visual">
      <span class="visual-label">{device} screenshot</span>
      <a class="screenshot-link" href="{app["screenshot"]}" aria-label="View full-size {name} screenshot">
        <img class="detail-screen" src="{app["screenshot"]}" alt="{name} on {device}" width="600">
      </a><span class="screenshot-caption">Tap to view full size</span>
    </div>
  </section>
  <section class="more-apps" aria-labelledby="more-heading"><div class="section-top">
    <h2 id="more-heading">Explore more apps</h2><a href="/#apps" class="details-link">All apps →</a>
  </div><div class="related-grid">{related_links(app)}</div></section>
</main>{FOOTER}</body></html>
"""


def write_discovery_files():
    sitemap = ElementTree.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for path in ["/", *(route(app) for app in APPS)]:
        url = ElementTree.SubElement(sitemap, "url")
        ElementTree.SubElement(url, "loc").text = SITE + path
    ElementTree.indent(sitemap)
    ElementTree.ElementTree(sitemap).write(ROOT / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    (ROOT / "robots.txt").write_text(f"User-agent: *\nDisallow:\n\nSitemap: {SITE}/sitemap.xml\n")


def main():
    cards = []
    for index, app in enumerate(APPS):
        cards.append(card(app, index))
        destination = ROOT / route(app).strip("/")
        destination.mkdir(exist_ok=True)
        (destination / "index.html").write_text(detail(app, index))
    home = (ROOT / "apps/home-template.html").read_text()
    home = home.replace("{{CATALOG}}", '<div class="app-grid">' + "".join(cards) + "</div>")
    home = home.replace("THE COLLECTION / 01—06", f"THE COLLECTION / {len(APPS):02} APPS")
    (ROOT / "index.html").write_text(home + "\n")
    write_discovery_files()
    print(f"Generated homepage, sitemap and {len(APPS)} app pages")


if __name__ == "__main__":
    main()
