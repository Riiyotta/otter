Source: https://withotter.com/

# Asset inventory — `/faq`, `/contact`, `/careers`

Measured 2026-10-08, Playwright, at 1440 / 1024 / 390. Companion spec: `spec/SPEC_faq_contact_careers.md`.
CDN prefix for every Webflow asset below: `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/`

**Headline: there are no broken assets.** Every URL referenced on these three routes returns `200`. Two assets are simply never fetched on a normal page load (deferred, not missing) and one `srcset` family has a URL-encoding quirk — details in §4 and §5.

---

## 1. Fonts (shared, identical to homepage)

All four self-hosted faces are actually downloaded on **all three** routes, `format("woff")`, `font-display:swap`:

| Family | Weight | URL |
|---|---|---|
| Jokker | 400 | `682e5411afe4660a9707efe4_Jokker-Regular.woff` |
| Jokker | 500 | `682e5411afe4660a9707efe2_Jokker-Medium.woff` |
| Jokker | 600 | `682e5411afe4660a9707efe0_Jokker-Semibold.woff` |
| Reckless Neue | 900 | `682e5411afe4660a9707efde_RecklessNeue-Heavy.woff` |

Declared but never downloaded: `682e5411afe4660a9707efe3_Jokker-RegularItalic.woff`, `682e5411afe4660a9707efdd_Jokker-MediumItalic.woff`.

Also downloaded on all three routes but **unused** (only `.styles__selector-callout` references Inconsolata, which is on no route) — skip it:
`https://fonts.gstatic.com/s/inconsolata/v37/QlddNThLqRwH-OJ1UHjlKENVzkWGVkL3GZQmAwLyya15IDhunA.woff2`

> ⚠ `/contact` and `/careers` request **Reckless Neue 400** (because `h1.u-mb-0` picks up `.u-mb-0{font-weight:400}`) while only the **900** Heavy file is hosted. The browser synthesises a lighter face from Heavy. This is the original's real rendering — reproduce it, don't "fix" it to 900.

## 2. Stylesheet

`css/with-otter-ac17371ef8a503ba0b8fca450052.shared.34930fed5.min.css` — **byte-identical to the homepage's**, serves all 11 routes. Already mirrored at `reference/assets/`.

---

## 3. `/faq`

One image total.

| Slot | URL | Intrinsic (served variant) | Rendered 1440 / 1024 / 390 | `srcset` / `sizes` |
|---|---|---|---|---|
| hero `.cc-sitters-top` → `img.u-img-cover`, `alt="a child with their hands on their head"`, `loading="lazy"` | `682e5411afe4660a9707f006_hero2.webp` | 460 × 460 (`-p-500` variant served at 1440) | 429 × 429 / 324.6 × 324.6 / 280.8 × 280.8 | `srcset`: `…_hero2-p-500.webp 500w, …_hero2.webp 800w`<br>`sizes`: `(max-width: 479px) 72vw, (max-width: 767px) 68vw, (max-width: 991px) 38vw, 32vw` |

Full URLs:
- `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f006_hero2.webp`
- `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f006_hero2-p-500.webp`

Already present in the repo from the homepage pass: `reference/assets/682e5411afe4660a9707f006_hero2.webp`.

The second hero shape (`.cc-sitters-bottom`) is a flat `--peach` div behind `clip-path:url(#stone-hero_bottom-left)` — **no asset**.

---

## 4. `/contact`

| Slot | URL | Intrinsic | Rendered 1440 / 1024 / 390 | Notes |
|---|---|---|---|---|
| hero `div.u-aspect-1x1` → `img.u-img-cover`, `alt=""`, `loading="lazy"` | `682e5411afe4660a9707f04b_Contact Hero.webp` | 504 × 469 (`-p-800` served) | 476.7 × 476.7 / 360.7 × 360.7 / **absent** | `display:none` at ≤767 via `.col-sm-hide`, so not rendered at 390 |
| success block `.trust-card_icon > img`, `alt="Dedicated support"`, `loading="lazy"` | `682e5411afe4660a9707f021_safety.webp` | — | **never loaded** | ⚠ see below |

`sizes` for the hero: `(max-width: 767px) 100vw, (max-width: 991px) 33vw, 35vw`
`srcset`: `…Contact%2520Hero-p-500.png 500w, …Contact%2520Hero-p-800.png 800w, …Contact%20Hero.webp 910w`

Full URLs:
- `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f04b_Contact%20Hero.webp` — 200, `image/webp`, 34,552 B
- `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f04b_Contact%2520Hero-p-500.png`
- `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f04b_Contact%2520Hero-p-800.png` — 200, **`image/webp`**, 32,340 B
- `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f021_safety.webp` — 200, `image/webp`, 7,708 B

### ⚠ Deferred asset: `safety.webp` (success-state icon)

`measured: naturalWidth 0, currentSrc ""` on a normal load. **Not a broken asset** — the URL is valid (verified 200 / `image/webp` / 7,708 B). It has `loading="lazy"` and sits inside `.form-success.w-form-done`, which is `display:none` until Webflow reveals it, so the browser never schedules the fetch. Because of this the live `.trust-card_icon` measures `0 × 24` instead of its CSS `max-width:6.5rem` (104px) + `margin-bottom:3rem`.

**Action for Build:** download it explicitly — it will not be captured by crawling a default page load, and the success state will render with a collapsed icon slot if it is missed.

### Inline SVGs on `/contact` (not network assets — copy into markup)

- Envelope, `viewBox="0 0 28 28"`, 2 paths: body `fill="currentColor"` (resolves to `--celeste`), flap `fill="#00373E"`.
- Map pin, `viewBox="0 0 24 24"`, 2 paths: outer `fill="currentColor"`, inner circle `fill="#00373E"`.

Both `width="100%" height="100%"` inside a 24 × 24 `.icon-wrap-24`.

---

## 5. `/careers`

17 `<img>` elements. All URLs 200.

### Hero + section illustration

| Slot | URL | Intrinsic (served) | Rendered 1440 / 1024 / 390 | `sizes` |
|---|---|---|---|---|
| hero `.cc-sitters-top`, `alt="Kid playing with sitter"` | `682e5411afe4660a9707efed_Playing_Colored_01 1.webp` | 460 × 387 (`-p-500` served) | 429 × 429 / 324.6 × 324.6 / 280.8 × 280.8 | `(max-width: 479px) 72vw, (max-width: 767px) 68vw, (max-width: 991px) 38vw, 32vw` |
| `.u-aspect-9x16`, `alt=""` | `682e5411afe4660a9707f04c_Illo Sitter + Parents.webp` | 619 × 408 (`-p-800` served) | 580 × 324.8 / 440.8 × 246.8 / 351 × 196.5 | `(max-width: 479px) 90vw, (max-width: 767px) 85vw, (max-width: 991px) 40vw, 43vw` |

Full URLs:
- `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707efed_Playing_Colored_01%201.webp` (1882w master; already in `reference/assets/`)
- `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f04c_Illo%20Sitter%20%2B%20Parents.webp` — 200, `image/webp`, 141,138 B (1252w master)

`srcset` for `Illo Sitter + Parents`:
```
…682e5411afe4660a9707f04c_Illo%2520Sitter%2520%252B%2520Parents-p-500.png   500w
…682e5411afe4660a9707f04c_Illo%2520Sitter%2520%252B%2520Parents-p-800.png   800w
…682e5411afe4660a9707f04c_Illo%2520Sitter%2520%252B%2520Parents-p-1080.png 1080w
…682e5411afe4660a9707f04c_Illo%2520Sitter%2520%252B%2520Parents-p-1600.png 1600w
…682e5411afe4660a9707f04c_Illo%20Sitter%20%2B%20Parents.webp               1252w
```

`srcset` for `Playing_Colored_01 1`:
```
…682e5411afe4660a9707efed_Playing_Colored_01%25201-p-500.png   500w
…682e5411afe4660a9707efed_Playing_Colored_01%25201-p-800.png   800w
…682e5411afe4660a9707efed_Playing_Colored_01%25201-p-1080.png 1080w
…682e5411afe4660a9707efed_Playing_Colored_01%25201-p-1600.png 1600w
…682e5411afe4660a9707efed_Playing_Colored_01%201.webp         1882w
```

### ⚠ Webflow encoding quirk in these two `srcset`s

The resized variants are **double-encoded**: the master is `…Illo%20Sitter%20%2B%20Parents.webp` (single-encoded) but the variants are `…Illo%2520Sitter%2520%252B%2520Parents-p-800.png` (`%25` = a literal `%`). Likewise `Playing_Colored_01%201.webp` → `Playing_Colored_01%25201-p-500.png`.

Two consequences:
1. The variant filenames end in **`.png` but the CDN serves `image/webp`** (verified: `-p-800.png` → 200, `image/webp`, 59,762 B). Don't infer format from the extension.
2. If you re-host, copy these URLs **character-for-character**. Naively decoding or re-encoding them produces 404s. At 1440 the browser picks `-p-500.png` / `-p-800.png`, not the `.webp` master, so the variants are the ones actually needed.

### Values icons — 6 × 72 px (56 px @390), `alt=""`, `loading="lazy"`, no `srcset`/`sizes`

| Value | URL (prefix + …) | Intrinsic | Rendered |
|---|---|---|---|
| Care first | `682e5411afe4660a9707f028_care%20first.webp` | 300 × 300 | 72 × 72 |
| Always build trust | `682e5411afe4660a9707f03b_always%20build%20trust.webp` | 284 × 284 | 72 × 72 |
| Be rigorous | `682e5411afe4660a9707f03c_be%20rigorous.webp` | 300 × 300 | 72 × 72 |
| Always do the right thing | `682e5411afe4660a9707f03a_do%20the%20right%20thing.webp` | 276 × 276 | 72 × 72 |
| Win some, learn some | `682e5411afe4660a9707f03d_win%20some%2C%20learn%20some.webp` | 276 × 276 | 72 × 72 |
| Build for diversity | `682e5411afe4660a9707f027_build%20for%20diversity.webp` | 244 × 244 | 72 × 72 |

> Note the comma in `win%20some%2C%20learn%20some.webp` is `%2C`-encoded. Keep it; a raw `,` in a `srcset` would be a separator, and even here it is safest left encoded.

### Benefits icons — 6 × 88 px (64 px @≤767), `alt=""`, `loading="lazy"`, no `srcset`/`sizes`

| Benefit | URL (prefix + …) | Intrinsic | Rendered |
|---|---|---|---|
| Healthcare | `682e5411afe4660a9707f02c_healthcare.webp` | 264 × 264 | 88 × 88 |
| 401(k) plan | `682e5411afe4660a9707f029_401k.webp` | 300 × 300 | 88 × 88 |
| 7 years to exercise your options | `682e5411afe4660a9707f035_exercising%20options%201x1.webp` | 271 × 271 | 88 × 88 |
| Flexible time off | `682e5411afe4660a9707f02a_flexible%20time%20off.webp` | 300 × 300 | 88 × 88 |
| Parental leave | `682e5411afe4660a9707f038_parental%20leave.webp` | 300 × 300 | 88 × 88 |
| Dependent care FSA | `682e5411afe4660a9707f037_dependent%20fsa.webp` | 300 × 300 | 88 × 88 |

All 12 icon images above were confirmed fetched with status 200 on a 1440 load.

### Job-row arrow icon — 3 identical instances

`https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f026_up-right.svg`

- 200, `image/svg+xml`, 320 B. Intrinsic `width="16" height="16"`, `viewBox="0 0 16 16"`, single path, `fill="#00373E"`.
- Rendered 16 × 16 at all three widths.
- **Deferred, like `safety.webp`:** `loading="lazy"` and far below the fold, so it is not requested during the initial load window (`naturalWidth 0`, empty `currentSrc` when measured at the top of the page). Not broken.
- Because it's a tiny single-path SVG, **recommend inlining it** rather than shipping a network request. Path `d`:

```
M3.4878 14.396L10.1598 7.724C11.0238 6.836 11.6238 6.02 11.8878 5.468L11.7438 12.62H14.4078V1.604H3.3678V4.268L10.5198 4.124C9.9918 4.364 9.1518 4.94 8.2638 5.828L1.5918 12.5L3.4878 14.396Z
```

### Shapes with no asset

`/careers` hero `.cc-sitters-bottom` is a flat `--olive` div, `clip-path:url(#stone-hero_top-left)`, `transform:rotate(90deg)`. The `.cc-sitters-top` backing colour is `--coral` `#fbad9c` (first live use of that token). Footer shapes are the homepage's two flat clipped divs. No images.

---

## 6. Nav / footer inline SVGs (shared, already specced for the homepage)

- Otter wordmark, `viewBox="0 0 139 48"`, fill `#00373E` — used twice per page (`a.brand_logo` in the nav, `div.brand_logo.cc-footer` in the footer). Rendered 128 × 50.7 (112 px wide @≤479).
- **New on these routes:** the nav hover blob inside `.current-icon`, `viewBox="0 0 34 22"`, `fill="currentColor"`, rendered 40 × 32.875 @1440/1024 (36 px wide @390). Four instances (one per content nav link). Path `d` is in `spec/SPEC_faq_contact_careers.md` §2.1.

---

## 7. Summary of findings to action

| # | Finding | Action |
|---|---|---|
| 1 | No 404s, no broken references on any of the three routes | none |
| 2 | `682e5411afe4660a9707f021_safety.webp` never fetched (lazy inside `display:none` success block) | **download explicitly**; a page-load crawl will miss it |
| 3 | `682e5411afe4660a9707f026_up-right.svg` never fetched during initial load (lazy, below fold) | download explicitly, or inline the 320 B path |
| 4 | `Illo Sitter + Parents` and `Playing_Colored_01 1` resized variants are double-encoded (`%2520`, `%25201`) and serve WebP under a `.png` extension | copy URLs verbatim; the `-p-500`/`-p-800` variants are the ones the browser actually loads |
| 5 | `Contact Hero` hero image is `display:none` at ≤767 | still download; needed at ≥768 |
| 6 | Reckless Neue **400** is requested but only **900** is hosted | keep as-is; synthesised face is the original's look |
| 7 | 12 values/benefits icons are 244–300 px intrinsic but rendered at 72/88 px | safe to downscale when self-hosting |
