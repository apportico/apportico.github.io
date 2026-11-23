# Apportico app collection

Public one-page app showcase: https://apportico.com/

The showcase is now the root `index.html`, with styles and assets retained in this folder. `/apps/` redirects to the root homepage. App support/privacy pages are unchanged.

## Assets and listings

- `assets/apportico-logo.png`: unmodified official Apportico GitHub organization avatar, retrieved from https://avatars.githubusercontent.com/u/142166324?v=4 on 8 November 2026.
- App icons and screenshots: official Apple App Store listing assets for Whenlet (6831935705), Dimensions Planner (6831661912), and Spin Sprout (6831902087).
- Live listing links checked on 8 November 2026. Availability and pricing vary by storefront.

To preview, serve the repository with a local static web server and visit `/`. Before updating, check each App Store listing, validate asset paths, and test desktop and phone layouts. Do not add unreleased products or private release information.

- Added on 9 November 2026: Daycue (6832012323), Note Porch (6832109392), and Pivotile (6832112459). Icons and screenshots are official Apple listing assets. Listings verified through Apple’s public lookup API in the US and UAE. Descriptions summarize those public listings.

As of 9 November 2026, the homepage is a compact gallery. Dedicated marketing pages now live at `/apps/whenlet/`, `/apps/dimensions-planner/`, `/apps/spin-sprout/`, `/apps/daycue/`, `/apps/note-porch/`, and `/apps/pivotile/`. `/apps/` itself still redirects to the homepage. Marketing content is sourced from the existing verified collection; no new product claims or listings were added.

## Tumblepatch — 10 November 2026

Verified public listing: https://apps.apple.com/us/app/tumblepatch/id6832247736
Official icon and first iPhone screenshot sourced from Apple Lookup API (US storefront, app 6832247736). Screenshot downloaded at 600 × 900 bounding size. Public description confirms offline puzzles, no ads or subscriptions, and a free sample with a one-time unlock.

## Catalog refresh — 16 November 2026

Added Whisper Live (6833964231), WalkLedger (6832005164), Motoring Shelf
(6832641002), Night Signal (6834916645), and Shadow Cast (6835032536).
US App Store listings, icons, and first iPhone screenshots were verified
through Apple's public listings and lookup metadata. Marketing copy describes
public app features; see the App Store for current offers and availability.

## Catalog and design refresh: November 22, 2026

Reviewed the 17 published apps in the US and UAE storefronts for the two
existing catalog publishers: [Eduard Simonyan](https://apps.apple.com/us/developer/eduard-simonyan/id1344536934)
and [Daniele Zanni](https://apps.apple.com/us/developer/daniele-zanni/id6831260606).
Added Drawbright, Snowball Yard, Counterlift, Candle Gremlins, and The Quiet
Wild. Support and privacy routes were not moved. Apple TV-only products use
their native landscape previews.

Current highlights were checked against public Apple listing descriptions
and release notes. In particular, Whisper Live 1.4, Pivotile 1.5, Tumblepatch
1.3 and Drawbright 1.3 are public releases. Nothing from unreleased builds is
included. Artwork and previews are Apple App Store assets, not recreated
UI. To trace a file, take the numerical app ID from its filename and look
it up at `https://itunes.apple.com/lookup?id=APP_ID&country=us&entity=software`.
Use `artworkUrl512` for icons and `screenshotUrls` or
`appletvScreenshotUrls` for the matching device previews. Larger CDN sizes
of the same source images were saved as optimized JPEGs without cropping.
