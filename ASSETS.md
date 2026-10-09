Source: https://withotter.com/

# Asset Manifest — Otter homepage

Local reference copy: `/Users/riyaghosh/V3/otter/reference/assets/`
CDN prefix (all site assets): `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/`

Status legend: **ON DISK** = present in `reference/assets/` · **MISSING** = must be downloaded from the live URL.

---

## 1. Fonts — ALL MISSING from the saved copy

Self-hosted `.woff`, `font-display: swap`. Download all 6 (or at minimum the 4 marked *used*).

| File | Family / weight / style | Used on homepage | URL | Status |
|---|---|---|---|---|
| `682e5411afe4660a9707efe4_Jokker-Regular.woff` | Jokker 400 normal | **yes** | `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707efe4_Jokker-Regular.woff` | **MISSING** |
| `682e5411afe4660a9707efe2_Jokker-Medium.woff` | Jokker 500 normal | **yes** | `…/682e5411afe4660a9707efe2_Jokker-Medium.woff` | **MISSING** |
| `682e5411afe4660a9707efe0_Jokker-Semibold.woff` | Jokker 600 normal | **yes** | `…/682e5411afe4660a9707efe0_Jokker-Semibold.woff` | **MISSING** |
| `682e5411afe4660a9707efde_RecklessNeue-Heavy.woff` | Reckless Neue 900 normal | **yes** (h1 only) | `…/682e5411afe4660a9707efde_RecklessNeue-Heavy.woff` | **MISSING** |
| `682e5411afe4660a9707efe3_Jokker-RegularItalic.woff` | Jokker 400 italic | declared, unused | `…/682e5411afe4660a9707efe3_Jokker-RegularItalic.woff` | **MISSING** |
| `682e5411afe4660a9707efdd_Jokker-MediumItalic.woff` | Jokker 500 italic | declared, unused | `…/682e5411afe4660a9707efdd_Jokker-MediumItalic.woff` | **MISSING** |

Google Fonts — **not needed**. `Inconsolata:400,700` is injected via the WebFont loader
(`https://fonts.googleapis.com/css?family=Inconsolata:400,700`, latin woff2
`https://fonts.gstatic.com/s/inconsolata/v37/QlddNThLqRwH-OJ1UHjlKENVzkWGVkL3GZQmAwLyya15IDhunA.woff2`)
but its only consumer is the Webflow style-guide class `.styles__selector-callout`, which does not exist on this page. **Skip it.**

Fetch command:
```sh
cd /Users/riyaghosh/V3/otter/public/fonts
B=https://cdn.prod.website-files.com/682e5411afe4660a9707efce
for f in 682e5411afe4660a9707efe4_Jokker-Regular.woff \
         682e5411afe4660a9707efe2_Jokker-Medium.woff \
         682e5411afe4660a9707efe0_Jokker-Semibold.woff \
         682e5411afe4660a9707efde_RecklessNeue-Heavy.woff \
         682e5411afe4660a9707efe3_Jokker-RegularItalic.woff \
         682e5411afe4660a9707efdd_Jokker-MediumItalic.woff ; do
  curl -sSLO "$B/$f"
done
```

---

## 2. Raster images (WebP)

| Slot | File | Intrinsic | Rendered @1440 | alt | Status |
|---|---|---|---|---|---|
| Hero stone — top-left | `682e5411afe4660a9707efeb_hero1.webp` | 800 × 800 | 399 × 399 | `a person holding a baby` | **ON DISK** (378 KB) |
| Hero stone — bottom-left | `682e5411afe4660a9707efed_Playing_Colored_01 1.webp` | 1882 × 1578 (webp) | 363 × 363 | `Kid playing with sitter` | **ON DISK** (230 KB) |
| Hero stone — bottom-right | `682e5411afe4660a9707f006_hero2.webp` | 800 × 800 | 428 × 428 | `a child with their hands on their head` | **ON DISK** (258 KB) |
| How-it-works illustration | `682e5411afe4660a9707f025_Illo Sitter and Kid.webp` | 1062 × 1056 | 406 × 404 | `A child handing a ball to a smiling caregiver` | **ON DISK** (80 KB) |

Full URLs: `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/<file>` (note the space in `Illo Sitter and Kid.webp` is `%20` on the CDN, and `Playing_Colored_01 1.webp` is `Playing_Colored_01%201.webp`).

### Responsive `srcset` (optional — single-source is fine for a clone)

```
hero1:
  …efeb_hero1-p-500.webp 500w
  …efeb_hero1.webp 800w
  sizes="(max-width: 800px) 100vw, 800px"

Playing_Colored_01 1:
  …efed_Playing_Colored_01%25201-p-500.png   500w
  …efed_Playing_Colored_01%25201-p-800.png   800w
  …efed_Playing_Colored_01%25201-p-1080.png 1080w
  …efed_Playing_Colored_01%25201-p-1600.png 1600w
  …efed_Playing_Colored_01%201.webp         1882w
  sizes="(max-width: 1882px) 100vw, 1882px"
  (at 1440 the browser actually picked the 1600w PNG, 1440×1208)

hero2:
  …f006_hero2-p-500.webp 500w
  …f006_hero2.webp       800w
  sizes="(max-width: 800px) 100vw, 800px"

Illo Sitter and Kid:
  …f025_Illo%2520Sitter%2520and%2520Kid-p-500.png  500w
  …f025_Illo%2520Sitter%2520and%2520Kid-p-800.png  800w
  …f025_Illo%20Sitter%20and%20Kid.webp            1062w
  sizes="(max-width: 1062px) 100vw, 1062px"
```

All four carry `loading="lazy"` on the original.

---

## 3. SVG images (`<img src>`)

| Slot | File | Intrinsic | Rendered @1440 | alt | Status |
|---|---|---|---|---|---|
| Banner illustration | `682e5411afe4660a9707f050_Playdate.svg` | 254 × 157 | 291.2 × 180 (`height="180"` attr) | `""` (decorative) | **ON DISK** (152 KB) |
| Trust logo 1 | `682e5411afe4660a9707efdf_forbes.svg` | 120 × 32 | 90 × 24 | `Forbes magazine` | **ON DISK** (8 KB) |
| Trust logo 2 | `682e5411afe4660a9707efe6_parents.svg` | 188 × 32 | 141 × 24 | `parents.com` | **ON DISK** (7 KB) |
| Trust logo 3 | `682e5411afe4660a9707efe5_NYT.svg` | 238 × 32 | 178.5 × 24 | `The New York Times` | **ON DISK** (10 KB) |
| Trust logo 4 | `682e5411afe4660a9707efe1_mom.svg` | 96 × 32 | 72 × 24 | `mom.com` | **ON DISK** (8 KB) |

Trust logos render at `height: 24px` (`.featured-logo-wrap { height: 1.5em }`, `.featured-logo { height: 100% }`), width auto from intrinsic aspect ratio.

---

## 4. CSS `background-image` SVGs — MISSING from the saved copy

| Used by | File | CSS | Status |
|---|---|---|---|
| `.bullet-organic.bullet` (the 1/2/3 blobs) | `682e5411afe4660a9707f04d_bullet-organic.svg` | `background-position:0 0; background-size:auto; background-color:transparent` on a `64×64` box (`48px` wide @≤479) | **MISSING** → `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f04d_bullet-organic.svg` |
| `.home-card-2.home-card-lg` ("We want to help you grow" card) | `682e5411afe4660a9707f04e_join-bg.svg` | `background-position:100% 0; background-repeat:no-repeat; background-size:auto 100%`<br>@≤991 `background-position:160%` · @≤767 `190%` · @≤479 `200px` | **MISSING** → `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f04e_join-bg.svg` |

Two further background SVGs are referenced by the stylesheet but **not used on this page** (style-guide / form classes): `…f03f_arrow-black.svg` (`.input.cc-select`), `…f040_bg-margin.svg`, `…f03e_bg-padding.svg`.

---

## 5. Inline SVG (no file — copy the markup)

| Slot | Source | Notes |
|---|---|---|
| Otter wordmark (nav + footer) | inline `<svg viewBox="0 0 139 48" width="100%" height="100%">`, two `<path fill="#00373E">`, wrapped in `clip-path:url(#clip0_254_628)` | Appears **twice** with the *same* `<clipPath id="clip0_254_628">` — dedupe the id or make it unique per instance in React. Full path data is in `/Users/riyaghosh/V3/otter/reference/original.html` (search `clip0_254_628`). |
| 7 organic clip-path defs | 7 × `<svg class="svg"><clipPath id="…" clipPathUnits="objectBoundingBox"><path d="…"/></clipPath></svg>` | Full path data reproduced verbatim in `CLONE_SPEC.md` §5. Render once in a hidden container (`width:0;height:0;position:fixed;inset:0 auto auto 0`, `overflow:hidden`). IDs: `stone-hero_top-right`, `stone-hero_bottom-right`, `stone-hero_top-left`, `stone-hero_middle-left`, `stone-hero_bottom-left`, `footer-shape-left`, `footer-shape-right`. |

---

## 6. Favicons / meta images — MISSING

| Purpose | URL | Status |
|---|---|---|
| `rel="shortcut icon"` | `https://cdn.prod.website-files.com/6424ac4b25764708c6aa49f7/642e390d59ef945e692bfb65_Otter%20Favicon.png` | **MISSING** |
| `rel="apple-touch-icon"` | `https://cdn.prod.website-files.com/6424ac4b25764708c6aa49f7/642e39266f382a63e8e7e853_Otter%20Icon.png` | **MISSING** |
| `og:image` / `twitter:image` | `https://cdn.prod.website-files.com/6424ac4b25764708c6aa49f7/642e393ac0355a46d5c3f130_Otter%20OG%20Image.png` | **MISSING** |

Note these live under a **different** Webflow site id (`6424ac4b25764708c6aa49f7`), not `682e5411afe4660a9707efce`.

---

## 7. Media

**No video, no audio, no canvas, no Lottie on this page.** `document.querySelectorAll('video').length === 0`.

---

## 8. Scripts present in `reference/assets/` that should NOT be ported

`jquery-3.5.1.min.dc5e7f18c8.js`, `swiper-bundle.min.js` (loaded but zero `.swiper` elements on this route), `webfont.js`, `with-otter-*.schunk.*.js` + `with-otter-*.cd9b2d68.*.js` (Webflow runtime + IX2 — reimplement the 3 live interactions natively per `CLONE_SPEC.md` §7), `amplitude-8.17.0-min.gz.js`, `fbevents.js`, `fs.js` (FullStory), `ndp.js` + `advmtch.js` (Nextdoor), `js`/`js(1)`…`js(4)` (gtag bundles), `2667541703549888` (FB pixel config), `f.txt`, `css` (Google Fonts CSS for Inconsolata).

The one stylesheet worth keeping as a reference is
`with-otter-ac17371ef8a503ba0b8fca450052.shared.34930fed5.min.css` (77 KB) — the compiled Webflow stylesheet every measurement in `CLONE_SPEC.md` was cross-checked against.
