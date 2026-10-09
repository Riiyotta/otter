Source: https://withotter.com/ (routes: /parents, /sitters, /trust-safety)

# Asset manifest — `/parents`, `/sitters`, `/trust-safety`

Measured 2026-10-08 with Playwright at 1440×900 / 1024×900 / 390×844, `deviceScaleFactor: 1`.
Companion spec: `/Users/riyaghosh/V3/otter/spec/SPEC_parents_sitters_trust.md`
Homepage manifest (separate, do not edit): `/Users/riyaghosh/V3/otter/ASSETS.md`

**CDN prefix for every raster asset below:**
`https://cdn.prod.website-files.com/682e5411afe4660a9707efce/`

All `<img>` are `loading="lazy"`. All are WebP. Webflow's responsive variants use the `-p-NNN.webp` suffix and have the filename **double-URL-encoded** in `srcset` (`%2520` for a space) while the base `src` is single-encoded (`%20`) — copy the URLs verbatim, they are not interchangeable.

---

## 1. Images NOT already in the homepage manifest — download these

| # | File | Route(s) | Slot | Intrinsic | Rendered @1440 |
|---|---|---|---|---|---|
| 1 | `682e5411afe4660a9707efea_Parents.webp` | /parents | hero top stone | 441×441 | 429×429 |
| 2 | `682e5411afe4660a9707f007_Sitters.webp` | /sitters | hero top stone | 441×441 | 429×429 |
| 3 | `682e5411afe4660a9707f008_FAQ.webp` | /trust-safety | hero top stone | 441×441 | 429×429 |
| 4 | `682e5411afe4660a9707f022_Sign up 2.webp` | /parents | tab 1 | 528×441 (528w) | 428.7×342.9 |
| 5 | `682e5411afe4660a9707f01e_home tabs – book.webp` | /parents | tab 2 | 528w | — (hidden until active) |
| 6 | `682e5411afe4660a9707f01c_home tabs – heda out.webp` | /parents | tab 3 | 528w | — (hidden until active) |
| 7 | `682e5411afe4660a9707f023_sitters sign up 2.webp` | /sitters | tab 1 | 528w | 428.7×342.9 |
| 8 | `682e5411afe4660a9707f013_Sitters - Find & Book Jobs.webp` | /sitters | tab 2 | 528w | — (hidden until active) |
| 9 | `682e5411afe4660a9707f01f_Sitters - Care an get paid.webp` | /sitters | tab 3 | 528w | — (hidden until active) |
| 10 | `682e5411afe4660a9707f00a_mom on phone.webp` | /parents | CTA card image | 907w | 427.7×603.0 |
| 11 | `682e5411afe4660a9707f00b_holding hands.webp` | /sitters | CTA card image | 1445w | 648.0×486.0 |
| 12 | `682e5411afe4660a9707f020_universal screening.webp` | /trust-safety | trust card 1 icon | 615w | 104×81.5 |
| 13 | `682e5411afe4660a9707f021_safety.webp` | /trust-safety | trust card 2 icon | 523×364 | 104×72.4 |
| 14 | `682e5411afe4660a9707efec_payment.webp` | /trust-safety | trust card 3 icon | 435×628 | 96×138.6 |
| 15 | `682e5411afe4660a9707efef_health.webp` | /trust-safety | trust card 4 icon | 477×428 | 104×93.3 |

> Note: the three hero stone photos (#1–3) are all 441×441 originals with **no `srcset`** — a single fetch each.
> Icons #13–15 have **no `srcset`** either; only #12 has one. #14 carries `width="96"` as an HTML attribute, which is why it renders narrower than the other three (the `.trust-card_icon` cap is `max-width:104px`).

---

## 2. Full download URLs

### 2.1 `/parents`

Hero stone — `alt="Sitter playing with baby"` (trailing newline in source), no srcset:
```
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707efea_Parents.webp
```

Tab 1 — `alt="Mom holding baby, checking iPad"` (trailing newline):
```
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f022_Sign%20up%202.webp
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f022_Sign%2520up%25202-p-500.webp
```
- accordion copy `sizes="(max-width: 479px) 80vw, (max-width: 767px) 79vw, (max-width: 991px) 80vw, 100vw"`
- desktop card copy `sizes="(max-width: 991px) 100vw, 30vw"`
- `srcset="…-p-500.webp 500w, …Sign%20up%202.webp 528w"`
- selected variant: `-p-500` @1440 (nat 432×361) and @390 (nat 390×326)

Tab 2 — `alt="Kid in parent's lap"`:
```
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f01e_home%20tabs%20%E2%80%93%20book.webp
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f01e_home%2520tabs%2520%25E2%2580%2593%2520book-p-500.webp
```
`srcset="…-p-500.webp 500w, …book.webp 528w"`. Filename contains an **en dash** (U+2013 → `%E2%80%93` / `%25E2%2580%2593`).

Tab 3 — `alt="Mom holding and kissing kid"`:
```
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f01c_home%20tabs%20%E2%80%93%20heda%20out.webp
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f01c_home%2520tabs%2520%25E2%2580%2593%2520heda%2520out-p-500.webp
```
`srcset="…-p-500.webp 500w, …heda%20out.webp 528w"`. Note "heda" is a typo in the original filename — keep it or rename consistently.

CTA image — `alt=""` (decorative):
```
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f00a_mom%20on%20phone.webp
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f00a_mom%2520on%2520phone-p-500.webp
```
- `srcset="…-p-500.webp 500w, …mom%20on%20phone.webp 907w"`
- `sizes="(max-width: 479px) 72vw, (max-width: 767px) 43vw, (max-width: 991px) 42vw, 30vw"`
- selected @1440: `-p-500` (nat 432×601), rendered 427.7×603.0

### 2.2 `/sitters`

Hero stone — `alt="Kid playing with puzzle toys"`, no srcset:
```
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f007_Sitters.webp
```

Tab 1 — `alt="Woman checking phone"`:
```
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f023_sitters%20sign%20up%202.webp
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f023_sitters%2520sign%2520up%25202-p-500.webp
```
`srcset="…-p-500.webp 500w, …sitters%20sign%20up%202.webp 528w"`; selected `-p-500` @1440 (nat 432×361).

Tab 2 — `alt="Kid toys"`:
```
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f013_Sitters%20-%20Find%20%26%20Book%20Jobs.webp
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f013_Sitters%2520-%2520Find%2520%2526%2520Book%2520Jobs-p-500.webp
```
`srcset="…-p-500.webp 500w, …Jobs.webp 528w"`. Contains an `&` → `%26` / `%2526`.

Tab 3 — `alt="Kid having breakfast"`:
```
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f01f_Sitters%20-%20Care%20an%20get%20paid.webp
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f01f_Sitters%2520-%2520Care%2520an%2520get%2520paid-p-500.webp
```
`srcset="…-p-500.webp 500w, …paid.webp 528w"`. "Care an get paid" is the original wording.

CTA image — `alt="Illustration of a kid and sitter holding hands"` (3-step srcset, the only one on these routes):
```
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f00b_holding%20hands.webp
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f00b_holding%2520hands-p-500.webp
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f00b_holding%2520hands-p-800.webp
```
- `srcset="…-p-500.webp 500w, …-p-800.webp 800w, …holding%20hands.webp 1445w"`
- `sizes="(max-width: 479px) 90vw, (max-width: 767px) 85vw, (max-width: 991px) 76vw, 45vw"`
- selected @1440: `-p-800` (nat 648×480), rendered 648.0×486.0

### 2.3 `/trust-safety`

Hero stone — `alt="Kid playing with puzzle toy"`, no srcset:
```
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f008_FAQ.webp
```

Trust card icons (DOM order):
```
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f020_universal%20screening.webp
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f020_universal%2520screening-p-500.webp
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707f021_safety.webp
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707efec_payment.webp
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707efef_health.webp
```

| Icon | alt | srcset / sizes | intrinsic | rendered @1440 |
|---|---|---|---|---|
| `universal screening` | `Background Check` | `srcset="…-p-500.webp 500w, …screening.webp 615w"`, `sizes="(max-width: 479px) 32vw, 104px"` | 615w (selected `-p-500`: 103×81) | 104×81.5 |
| `safety` | `Dedicated support` | none | 523×364 | 104×72.4 |
| `payment` | `Payment Protection` | none; `width="96"` attr | 435×628 | 96×138.6 |
| `health` | `Healthy Care Standars` *(typo in source)* | none | 477×428 | 104×93.3 |

---

## 3. Video / embed (`/trust-safety`)

**No `<video>` element exists** (0 on all three routes) and nothing autoplays. The video is a cross-origin embedly click-to-play facade wrapping Vimeo.

- Vimeo video id **705608326**, `h=131a48dcba`, `app_id=122963`
- iframe `title="Trust and Safety at Otter"`, `class="embedly-embed"`, no `allow` / `allowfullscreen`
- rendered 993.3×559.0 @1440, 761.3×428.4 @1024, 351×197.5 @390

Canonical player URL:
```
https://player.vimeo.com/video/705608326?h=131a48dcba&app_id=122963
```

Poster / preview frame (download this if you build a click-to-play facade):
```
https://i.vimeocdn.com/video/1424614019-1e9830b25303d82a02dfd4e33829977859d0df3d56aac3d91891ef53ee666073-d_1280
```

Full embedly iframe `src` as it appears in the DOM:
```
https://cdn.embedly.com/widgets/media.html?src=https%3A%2F%2Fplayer.vimeo.com%2Fvideo%2F705608326%3Fh%3D131a48dcba%26app_id%3D122963&dntp=1&display_name=Vimeo&url=https%3A%2F%2Fplayer.vimeo.com%2Fvideo%2F705608326&image=https%3A%2F%2Fi.vimeocdn.com%2Fvideo%2F1424614019-1e9830b25303d82a02dfd4e33829977859d0df3d56aac3d91891ef53ee666073-d_1280&key=96f1f04c5f4143bcb0f2e68c87d65feb&type=text%2Fhtml&schema=vimeo
```

**Not measurable:** the iframe is cross-origin, so its internal DOM, poster crop, play-button styling and player chrome could not be read. The `key=` value is an embedly account key belonging to the original site — do not reuse it; embed Vimeo directly instead.

---

## 4. Inline SVG (no download needed — paste the markup)

Counts: 15 inline `<svg>` on `/parents` and `/sitters`, 13 on `/trust-safety`. Breakdown: 7 clipPath defs + 2 logo instances (each with 1 nested `clip0_254_628` rect clip) + the nav current-icon blobs + the 2 swiper arrows (slider routes only).

| SVG | viewBox | Where | Source |
|---|---|---|---|
| Otter wordmark | `0 0 139 48` | `a.brand_logo` (nav), `div.brand_logo.cc-footer` | identical to homepage — reuse |
| 7 × `<clipPath>` organic stones | `objectBoundingBox` | global embed | identical to homepage — reuse §5 `d` strings verbatim |
| Nav current-icon blob | `0 0 34 22` | `.current-icon` ×4 (one per nav link) | **new** — `d` in spec §3.1 |
| Swiper arrow | `0 0 22 28` | `.swiper-icon` ×2 | **new** — `d` in spec §6; `.swiper-button-next` is the same SVG `rotate(180deg)` |

Both new SVGs use `fill="currentColor"` and `width="100%" height="100%"`, so they inherit colour from their parent (`--celeste` for the nav blob at ≥992, `--coral` at ≤991; `currentColor` on `.swiper-arrow`, which goes `--celeste` on hover).

**There are no new `clip-path` `d` strings on these routes.** The pages only recombine the existing 7 shapes with new fills:

| Route | Shape class stack | Fill |
|---|---|---|
| /parents | `.shape.stone-hero_middle-left.u-bg-coral` | `#fbad9c` + photo |
| /parents | `.shape.stone-hero_top-left.u-bg-olive.rotate-90` | `#94954c`, rotated 90° |
| /parents | `.shape.footer-shape-right.u-bg-peach` | `#fbd3b6` (CTA blob, ≤767 only) |
| /sitters | `.shape.stone-hero_bottom-right` | no fill class + photo |
| /sitters | `.shape.stone-hero_middle-left.u-bg-peach` | `#fbd3b6` |
| /sitters | `.shape.footer-shape-right.u-bg-celeste` | `#cafff2` (CTA blob, ≤767 only) |
| /trust-safety | `.shape.footer-shape-left` | no fill class + photo |
| /trust-safety | `.shape.stone-hero_top-left.u-bg-sandstone` | `#ac9e88` — **first live use of `--sandstone`** |
| all | `.shape.footer-shape-left.u-bg-olive` | `#94954c` (footer, as homepage) |
| all | `.shape.footer-shape-right.u-bg-peach` | `#fbd3b6` (footer, as homepage) |

---

## 5. Fonts — unchanged, already in the homepage manifest

Same six self-hosted faces, `format("woff")`, `font-display: swap`, same URLs under
`https://cdn.prod.website-files.com/682e5411afe4660a9707efce/`:
`Jokker-Regular`, `Jokker-RegularItalic`, `Jokker-Medium`, `Jokker-MediumItalic`, `Jokker-Semibold`, `RecklessNeue-Heavy`.

Actually used on these routes: Jokker 400 / 500 / 600 and Reckless Neue 900.
Inconsolata (Google Fonts, via `WebFont.load`) is still requested but still **unused** — skip it.

**Gotcha:** `/sitters` declares `font-weight:400` on its `h1` (via `.u-mb-0`) but no 400-weight Reckless Neue face exists, so the browser renders `RecklessNeue-Heavy.woff`. Map all Reckless Neue weights to the single Heavy file, as the original does. See spec §5.

---

## 6. Third-party CSS/JS loaded (do not port)

```
https://cdn.jsdelivr.net/npm/swiper@9/swiper-bundle.min.css
https://cdn.jsdelivr.net/npm/swiper@9/swiper-bundle.min.js
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/css/with-otter-ac17371ef8a503ba0b8fca450052.shared.34930fed5.min.css
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/js/with-otter-ac17371ef8a503ba0b8fca450052.cd9b2d68.73970c04f9b055b6.js
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/js/with-otter-ac17371ef8a503ba0b8fca450052.schunk.36b8fb49256177c8.js
https://cdn.prod.website-files.com/682e5411afe4660a9707efce/js/with-otter-ac17371ef8a503ba0b8fca450052.schunk.f6944230270a2d07.js
https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7f18c8.js?site=682e5411afe4660a9707efce
https://ajax.googleapis.com/ajax/libs/webfont/1.6.26/webfont.js
https://cdn.amplitude.com/libs/amplitude-8.17.0-min.gz.js
```
Plus GTM/gtag, Facebook Pixel, Nextdoor Pixel, FullStory, embedly.

---

## 7. Missing-asset findings

- **No missing or broken images.** Every `<img>` on all three routes resolved (HTTP 200) and reported a non-zero `naturalWidth` once its container became visible. The zero-size readings in my raw capture are the inactive tab panels (`display:none`), not load failures.
- **Two empty CMS collections** render Webflow's `div.w-dyn-empty` → "No items found." on the live site:
  - `/parents` and `/sitters`: the testimonials slider (`.swiper.w-dyn-list`) — **0 `.swiper-slide`**, so there are **no testimonial images, names or quotes to download**. Any testimonial avatars the design implies do not exist as assets.
  - `/parents` and `/sitters`: the "Common questions" list — **no FAQ item content exists**.
  These are content gaps on the original, not download failures. Do not fabricate replacements; confirm the intended treatment with the caller.
- **Cross-origin, not downloadable as a flat asset:** the `/trust-safety` Vimeo/embedly player (§3). Only the poster JPEG is directly fetchable.
