Source: https://app.withotter.com/log-in, /sign-up, /sign-up/welcome (→ /welcome)

# Auth Screens — Asset Manifest & Missing-Asset Findings

Checked against `/Users/riyaghosh/V3/otter/public/img/` and `/Users/riyaghosh/V3/otter/public/fonts/` on 2026-10-08.
`device-id` query params stripped. All URLs below are live and were fetched successfully at the stated byte sizes.

---

## 1. Summary

| Asset | Needed by | In repo? | Action |
|---|---|---|---|
| Otter wordmark SVG | `/log-in`, `/sign-up` | **NO** | Inline it (markup in §3) or save as `public/img/otter-wordmark.svg` |
| `illo-children-of-different-ages.svg` | `/log-in` | **NO** | **Download** (§2) |
| `illo-care-team.svg` | `/sign-up`, `/welcome` | **NO** | **Download** (§2) |
| Jokker 400/500/600 woff | all three | **YES** | Reuse `public/fonts/` |
| Reckless Neue Heavy woff | `/sign-up`, `/welcome` | **YES** | Reuse `public/fonts/` |
| Favicons / touch icons / manifest | `<head>` only | **NO** | Optional (§4) |
| Social-provider marks | — | n/a | **None exist.** No social sign-in on any of the three screens. |
| Icons (inline `<svg>`) | — | n/a | **None.** `document.querySelectorAll("#root svg").length === 0` on all three screens. |
| Video / canvas / Lottie | — | n/a | **None.** |

**2 files need downloading. 1 asset needs to be reconstructed from an inline data URI.**

---

## 2. Illustrations — MISSING, must be downloaded

Both are flat SVGs served from the app's Vite asset dir with immutable content hashes in the filename.

### 2.1 `illo-children-of-different-ages`

```
https://app.withotter.com/assets/illo-children-of-different-ages-CwALik0h.svg
```

| | |
|---|---|
| Format | `image/svg+xml` |
| Transfer size | **212,959 bytes** (uncompressed SVG — it is large) |
| Intrinsic / `viewBox` | `width="2804" height="1777" viewBox="0 0 2804 1777"` (aspect 1.5779) |
| `naturalWidth × naturalHeight` | 2804 × 1777 |
| Rendered | **400 × 253.5** at **all three widths** — set by inline `style="width: calc(25rem * var(--mantine-scale))"` i.e. a hard 400px, never responsive |
| Used on | `/log-in` only |
| Slot | second `Center` inside the upper `Stack`; rect `[520, 88, 400, 253.5]` @1440, `[312, 88, …]` @1024, **`[-5, 88, 400, 253.5]` @390 (overflows the 326px column by 5px each side; clipped by `overflow-x:hidden` on the AppShell root)** |
| Styling | `display:block; flex:0; object-fit:cover; width:100%; border-radius:0` (Mantine `Image`) |
| In `public/img`? | **NO** |
| Suggested local path | `public/img/illo-children-of-different-ages.svg` |

### 2.2 `illo-care-team`

```
https://app.withotter.com/assets/illo-care-team-AGZuQRFl.svg
```

| | |
|---|---|
| Format | `image/svg+xml` |
| Transfer size | **73,707 bytes** |
| Intrinsic / `viewBox` | `width="170" height="196" viewBox="0 0 170 196"` (aspect 0.8673) |
| `naturalWidth × naturalHeight` | 170 × 196 |
| Rendered | **160 × 184.5** at **all three widths** — inline `style="width: calc(10rem * var(--mantine-scale))"` i.e. a hard 160px. Note it is rendered *slightly smaller* than intrinsic. |
| Used on | `/sign-up` **and** `/welcome` (same file, same size, same slot treatment) |
| Slot | `/sign-up`: `Center` above the h1, rect `[640, 144, 160, 184.5]` @1440 / `[432, 144, …]` @1024 / `[115, 144, …]` @390. `/welcome`: `Center` with `margin-bottom:16px`, rect `[640, 48, 160, 184.5]` @1440 / `[432, 48, …]` @1024 / `[115, 48, …]` @390 |
| In `public/img`? | **NO** |
| Suggested local path | `public/img/illo-care-team.svg` |

### Download command

```bash
cd /Users/riyaghosh/V3/otter/public/img
curl -O https://app.withotter.com/assets/illo-children-of-different-ages-CwALik0h.svg
curl -O https://app.withotter.com/assets/illo-care-team-AGZuQRFl.svg
# then drop the content hashes:
mv illo-children-of-different-ages-CwALik0h.svg illo-children-of-different-ages.svg
mv illo-care-team-AGZuQRFl.svg               illo-care-team.svg
```

> ⚠️ `illo-children-of-different-ages.svg` is 208 KB of uncompressed SVG path data for an image rendered at 400×253. Consider gzip at the server level (Vite/Vercel do this automatically) rather than converting it — converting to raster would lose the crispness that justifies the 2804px artboard.

---

## 3. Otter wordmark — MISSING, inlined as a data URI in the original

There is **no HTTP request for the logo.** On both `/log-in` and `/sign-up` it is an `<img src="data:image/svg+xml,...">` (URL-encoded, not base64), inlined by Vite's asset-inlining threshold.

| | |
|---|---|
| Intrinsic / `viewBox` | `width="125" height="44" viewBox="0 0 125 44"` |
| Decoded size | 2,557 bytes |
| Fill | `#00373E` on both paths (hard-coded, no `currentColor`) |
| Clip path id | `clip0_10649_115307` — **rename it if you inline the SVG more than once on a page**, duplicate ids will break the clip |
| Rendered on `/log-in` | **96 × 33.8**, via inline `style="width: calc(6rem * var(--mantine-scale)); margin-top: calc(-3rem * var(--mantine-scale))"` → width 96px, **margin-top −48px**. Sits inside a `Center` whose own height collapses to 0, so the logo visually escapes upward: rect `[672, 31.1, 96, 33.8]` @1440 — i.e. its top is 17px *above* the container start. |
| Rendered on `/sign-up` | **79.5 × 28** inside the header anchor, no inline width (sized by the anchor box). rect `[22, 32, 79.5, 28]` at all three widths. |
| Not used on | `/welcome` (no logo on that screen) |
| In `public/img`? | **NO.** `public/img/` has `Otter-Icon.png`, `Otter-Favicon.png` and `Otter-OG-Image.png` — these are the **icon/glyph** marks from the marketing site, **not this wordmark**. Do not substitute them. |
| Suggested local path | `public/img/otter-wordmark.svg` |

### Full decoded markup (verbatim, single-quotes normalised to double)

```svg
<svg width="125" height="44" viewBox="0 0 125 44" fill="none" xmlns="http://www.w3.org/2000/svg"><g clip-path="url(#clip0_10649_115307)"><path d="M111.904 16.9684L112.782 12.3536H106.603L106.438 13.2249C103.436 28.4639 95.3431 35.6196 85.4708 35.6196C80.0543 35.6196 77.3643 32.8998 76.9403 30.0408C78.7027 31.0678 82.2044 31.8794 85.2224 31.8794C93.902 31.8794 98.9541 26.8936 98.9541 20.2845C98.9541 15.3683 95.1311 11.6181 88.4557 11.6181C81.0714 11.6181 74.9857 17.1936 72.6965 23.2926C69.9734 30.5444 65.8257 35.5236 62.334 35.5236C59.5678 35.5236 59.3325 33.0091 59.6671 31.2169C59.8195 30.4185 60.7703 25.3366 61.7874 19.9333H71.1163L72.6435 12.1846H63.245C63.7419 9.53436 64.1428 7.40751 64.3316 6.43354H58.0571C57.8318 7.60628 57.4376 9.68343 56.9606 12.1846H44.8157C45.8095 6.97353 46.7007 2.16329 47.1347 -0.0198669H40.8635C40.4063 2.35875 39.5119 7.05635 38.5445 12.1846H32.4456L30.915 19.9333H37.0338C36.0102 25.3068 35.0958 30.1104 34.7149 32.1113C33.5322 38.2798 37.0338 43.2524 42.4536 43.2524C46.6576 43.2524 50.5602 40.2179 53.1872 36.8421C54.0453 40.6353 56.9672 43.2524 60.8962 43.2524C65.776 43.2524 69.9038 38.8066 72.0936 34.9206C73.7003 39.6779 77.9143 43.2657 85.3151 43.2657C91.5135 43.2657 97.682 39.8236 102.602 33.3768L100.866 42.4971H107.034L107.925 37.8227C110.32 25.1809 114.276 19.5656 123.337 20.3839L124.993 11.8169C120.418 11.1345 115.26 13.2182 111.904 16.9684ZM44.0438 35.5203C41.1716 35.5203 40.9065 33.0058 41.2444 31.2136C41.3736 30.5278 42.2847 25.6811 43.3647 19.93H55.4896C55.2577 21.1492 55.0292 22.3617 54.8039 23.5344C53.0481 32.4923 47.0519 35.5368 44.0438 35.5368V35.5203ZM88.3099 19.4265C91.159 19.4265 93.2295 20.523 93.2295 22.2623C93.2295 24.6807 90.715 25.8269 85.1859 25.8269C82.8612 25.8054 80.5538 25.4254 78.3449 24.7005C79.4482 23.075 80.934 21.7454 82.6716 20.8287C84.4092 19.9119 86.3454 19.4361 88.3099 19.4431V19.4265Z" fill="#00373E"/><path d="M16.3651 11.638C12.113 11.6181 8.02166 13.2621 4.96549 16.2186C1.90932 19.1751 0.130666 23.2096 0.00961665 27.4601C-0.288539 36.3186 6.38021 43.2789 15.2951 43.2789C19.5469 43.2997 23.6382 41.6564 26.6945 38.7005C29.7507 35.7445 31.5295 31.7103 31.6505 27.4601C31.952 18.6016 25.2799 11.638 16.3651 11.638ZM25.3595 27.4601C25.2071 31.9788 21.5033 35.5302 15.5568 35.5302C9.61024 35.5302 6.1483 31.9788 6.30069 27.4601C6.45308 22.9414 10.2761 19.3867 16.1034 19.3867C21.9306 19.3867 25.5118 22.9381 25.3595 27.4601Z" fill="#00373E"/></g><defs><clipPath id="clip0_10649_115307"><rect width="125" height="43.2855" fill="white"/></clipPath></defs></svg>
```

(Reconstructible at any time: on a live auth screen run
`decodeURIComponent(document.querySelector('img[src^="data:"]').src.split(',').slice(1).join(','))`.)

---

## 4. Fonts — ALREADY IN REPO

The app declares six faces and serves them from `/assets/art/fonts/`. **All six URLs are broken on the live site** — Vercel's SPA rewrite returns the 2,907-byte `index.html` for each, so `document.fonts` reports `error`/`unloaded` and the original renders in fallback fonts. See §2 of `SPEC_auth.md`.

| Family | Weight | Style | Live (broken) URL | Local file — **present** |
|---|---|---|---|---|
| Jokker | 400 | normal | `https://app.withotter.com/assets/art/fonts/Jokker-Regular.woff` | `public/fonts/Jokker-Regular.woff` |
| Jokker | 400 | italic | `.../assets/art/fonts/Jokker-RegularItalic.woff` | `public/fonts/Jokker-RegularItalic.woff` |
| Jokker | 500 | normal | `.../assets/art/fonts/Jokker-Medium.woff` | `public/fonts/Jokker-Medium.woff` |
| Jokker | 500 | italic | `.../assets/art/fonts/Jokker-MediumItalic.woff` | `public/fonts/Jokker-MediumItalic.woff` |
| Jokker | 600 | normal | `.../assets/art/fonts/Jokker-Semibold.woff` | `public/fonts/Jokker-Semibold.woff` |
| Reckless Neue | 900 | normal | `.../assets/art/fonts/RecklessNeue-Heavy.woff` | `public/fonts/RecklessNeue-Heavy.woff` |

**No download needed.** These are the same files the marketing clone already vendored. Working upstream copies, if you ever need them, are on the Webflow CDN under `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/`.

Weights actually exercised by the three screens: **Jokker 600** (inputs, labels, buttons, anchors, h3), **Jokker 500** (body `<p>`), **Jokker 400** (inherited default, little visible text), **Reckless Neue** requested at **700** for the h1 (only a 900 file exists → synthesised, or re-declare the face at 700).

---

## 5. `<head>` assets (document chrome, not screen content)

Served from Google Cloud Storage, all with `?v=20230411`. Optional for a visual clone; none appear in the rendered page.

| Purpose | URL | In repo? |
|---|---|---|
| Apple touch icon 180×180 | `https://storage.googleapis.com/otter-public/apple-touch-icon.png?v=20230411` | NO |
| Favicon 32×32 | `https://storage.googleapis.com/otter-public/favicon-32x32.png?v=20230411` | NO |
| Favicon 16×16 | `https://storage.googleapis.com/otter-public/favicon-16x16.png?v=20230411` | NO |
| Safari pinned tab (mask, color `#00373e`) | `https://storage.googleapis.com/otter-public/safari-pinned-tab.svg?v=20230411` | NO |
| Shortcut icon | `https://storage.googleapis.com/otter-public/favicon.ico?v=20230411` | NO |
| MS tile config | `https://storage.googleapis.com/otter-public/browserconfig.xml?v=20230411` | NO |
| Android chrome 192×192 (from `/manifest.json`, actually requested at runtime) | `https://storage.googleapis.com/otter-public/android-chrome-192x192.png` | NO |
| Web app manifest | `https://app.withotter.com/manifest.json` | NO |

Relevant `<head>` meta: `theme-color: #00373E`, `msapplication-TileColor: #2b5797`, `apple-mobile-web-app-title: Otter`, `application-name: Otter`.

---

## 6. Reference files (for rule extraction, not shipping)

| What | URL | Size |
|---|---|---|
| Compiled CSS bundle | `https://app.withotter.com/assets/index-kszxQpln.css` | 204,769 bytes |
| Main JS bundle | `https://app.withotter.com/assets/index-3SWImSlZ.js` | 1,256,322 bytes |
| Lazy chunks seen on these routes | `https://app.withotter.com/assets/web--iGZl08Q.js`, `https://app.withotter.com/assets/web-DqedlYgu.js` | — |
| SPA shell | `https://app.withotter.com/log-in` (any route) | 2,907 bytes |

> These hashed filenames will change on the next deploy. If a URL 404s later, re-read the hash from the `<script type="module">` / `<link rel="stylesheet">` tags in the SPA shell.

---

## 7. Assets explicitly NOT present (so nobody goes looking)

- **No social / OAuth provider marks.** No Google, Apple, Facebook or Microsoft logo on any of the three screens. `accounts.google.com/gsi/client` is loaded by `index.html` on every route, but **no GSI button renders** on `/log-in`, `/sign-up` or `/welcome` — no `<iframe>`, no provider SVG, no `.g_id_signin` element.
- **No inline `<svg>` icons at all.** Zero `<svg>` elements under `#root` on all three screens at all three widths. No chevrons, eye-toggles, country-flag/dial-code marks, checkmarks or spinners.
- **No spinner/loader graphic.** Mantine's `Loader` CSS is absent from the bundle entirely; the button's loading affordance is a pure-CSS blurred white sweep (`::before`, `filter:blur(12px)`) plus a label opacity fade.
- **No card/panel background image, no decorative blobs, no pattern, no gradient, no backdrop-filter.** Content sits flat on `#F8F6F5`.
- **No video, no `<canvas>`, no Lottie/JSON animation, no webfont icon set.**
- **No images on `/welcome` other than** `illo-care-team.svg`. No logo on that screen.
