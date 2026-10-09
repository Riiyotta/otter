Source: https://withotter.com/

# Asset inventory — `/blog`, `/blog-posts/*`, `/terms-of-use`, `/privacy-policy`

Companion to `/Users/riyaghosh/V3/otter/spec/SPEC_blog_legal.md`.
Collected 2026-10-08 from the raw HTML of all five pages plus live `naturalWidth/naturalHeight` probes in-browser.

CDN prefixes (two different buckets — note the second one, it is **not** the homepage bucket):
- `A` = `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/` — site-level assets (same bucket as the homepage)
- `B` = `https://cdn.prod.website-files.com/682e5411afe4660a9707effa/` — **CMS collection assets (blog post covers)**

**19 unique `<img src>` across the five pages: 17 real images + 2 tracking pixels.**

## Verification status

**Every image referenced on these five pages resolves HTTP 200 with non-zero bytes. Nothing is missing, nothing is broken.**

Two false alarms worth recording so nobody re-chases them:
1. The `/blog` CTA image (`blog-cta.webp`) reports `currentSrc:""` / `naturalWidth:0` if you query it right after load. That is **`loading="lazy"` plus below-the-fold position**, not a missing asset. It is 2000×1068 and 210,840 bytes.
2. CMS cover filenames are **double URL-encoded** in the markup (`%2520` = an encoded `%20`). Requesting the single-encoded form (`%20`) 404s. Use the `src` string **verbatim from the DOM**; do not "normalise" it.

---

## 1. Site-level images (bucket `A`)

| File | Live URL | Intrinsic | Rendered | Format | Where |
|---|---|---|---|---|---|
| Blog Hero | `A682e5411afe4660a9707f012_Blog%20Hero.webp` | **1983×1752** (1.132:1) | 477×421 @1440 · 358.39×316.82 @1024 · 350.99×310.28 @390 | webp (png fallbacks in srcset) | `/blog` hero, bare `<img>`, `loading=lazy` |
| Blog CTA illustration | `A682e5411afe4660a9707f00c_blog-cta.webp` | **2000×1068** (1.873:1) | 648×402 @1440 · 460.8×285.69 @1024 · 351×217.62 @390 | webp | `/blog` CTA band, `img.u-img-cover` (`object-fit:contain`), `loading=lazy` |
| Playing (featured cover) | `A682e5411afe4660a9707efed_Playing_Colored_01%201.webp` | **1882×1580** (1.191:1) | 648×486 @1440 · 460.8×345.59 @1024 · 351×263.25 @390 | webp (png fallbacks) | `/blog` featured card. **Shared with the homepage hero bottom-left stone** — already in `ASSETS.md`, do not download twice. |
| Otter wordmark | *inline `<svg viewBox="0 0 139 48">`* | — | 128×60 nav, 128×51 footer; 112×48 @390 | inline SVG, `fill #00373E` | nav + footer, every page. Not a network request. |

`Blog Hero` srcset: `-p-500.png 500w, -p-800.png 800w, -p-1080.png 1080w, …` + the `.webp` original at full width.
`sizes="(max-width: 479px) 90vw, (max-width: 767px) 85vw, (max-width: 991px) 33vw, 35vw"`

`blog-cta` srcset: `-p-500.webp 500w, -p-800.webp 800w, …` + original.
`sizes="(max-width: 479px) 90vw, (max-width: 767px) 85vw, (max-width: 991px) 76vw, 45vw"`

`Playing_Colored_01 1` srcset: `-p-500.png 500w, -p-800.png 800w, -p-1080.png 1080w, -p-1600.png 1600w` + `.webp` **1882w**.
`sizes="(max-width: 479px) 90vw, (max-width: 767px) 85vw, (max-width: 991px) 42vw, 45vw"`

---

## 2. Blog post cover images (bucket `B`) — all 10 page-1 posts

All are `img.u-img-cover` → `object-fit:contain` inside a 4:3 box (`padding-top:75%`) on cards, and inside a **1:1** box (`.u-aspect-1x1`) on the post hero. All `loading="lazy"`.
Card `alt="Kid and sitter playing "` (one CMS default reused everywhere, trailing space included); post-hero `alt=""`.

Rendered card width: **405.33px @1440 · 280.52px @1024 · 351px @390** (featured: 648 / 460.8 / 351).

| # | Post slug | Cover file (append to prefix `B`) | Intrinsic | srcset widths |
|---|---|---|---|---|
| 1 ★ | `/blog-posts/series-a` | *(uses bucket `A` `…efed_Playing_Colored_01%201.webp`)* | 1882×1580 | 500/800/1080/1600/1882 |
| 2 | `/blog-posts/how-to-be-an-amazing-babysitter` | `682e5411afe4660a9707f132_635c677622d75f7989f0715e_shutterstock_1770121187.jpeg` | **1331×1232** | *none — bare src* |
| 3 | `/blog-posts/infant-care-101` | `682e5411afe4660a9707f14d_63b60f250027a80c3795f1ab_kelly-sikkema-Z4GKcFAGck4-unsplash.jpeg` | **3375×3182** | *none — bare src* |
| 4 | `/blog-posts/toddler-care-101` | `682e5411afe4660a9707f15e_63c8646503da3e60f10c9c5f_kazuend-ejlRp5ktpfY-unsplash.jpeg` | **3641×3390** | 500/800/1080/1600/2000/2600/3200/3641 |
| 5 | `/blog-posts/how-to-set-your-sitter-up-for-success` | `682e5411afe4660a9707f14f_63ed60950901c607a4352b9f_marisa-howenstine-Cq9slNxV8YU-unsplash.jpeg` | **4109×3723** | 500/800/1080/1600/2000/2600/3200/4109 |
| 6 | `/blog-posts/otter-featured-in-the-new-york-times` | `682e5411afe4660a9707f151_630fd57a2a2143108893c21b_Screen%2520Shot%25202022-08-31%2520at%25208.34.51%2520AM.png` | **866×752** | 500/800/866 |
| 7 | `/blog-posts/how-to-change-a-diaper` | `682e5411afe4660a9707f10b_637510acfaa17b2c0f3e0f77_zelle-duda-uld7AdE36z4-unsplash.jpeg` | **4852×4092** | *none — bare src* |
| 8 | `/blog-posts/tackling-bedtime-routines` | `682e5411afe4660a9707f161_mark-zamora-mFqAeaZgWO8-unsplash.jpg` | **2500×3741** (only portrait one) | 500/800/1080/1600/2000/2500 |
| 9 | `/blog-posts/baby-led-bottle-feeding` | `682e5411afe4660a9707f0d6_6387a0c4a2180b071b6ea74f_lucy-wolski-sljmgxyzmqM-unsplash.jpeg` | **3994×3557** | *none — bare src* |
| 10 | `/blog-posts/how-to-set-parents-at-ease-while-babysitting` | `682e5411afe4660a9707f14c_63dae0b5448c197cc1887fc9_kelly-sikkema-4l2Ml8-MLUg-unsplash.jpeg` | **2094×1831** | *none — bare src* |

★ featured-variant card.

Webflow only generates responsive variants above a size threshold, which is why 5 of the 10 have **no `srcset` and no `sizes`** — just a bare `src`. Variant URLs follow `…<basename>-p-<width>.<ext>`.
`sizes` where present (two forms, both in the wild):
- list page: `(max-width: 479px) 90vw, (max-width: 767px) 85vw, (max-width: 991px) 40vw, 27vw`
- related-posts grid: `(max-width: 479px) 90vw, (max-width: 991px) 40vw, 27vw`

### Post-hero covers (the 1:1 `.u-aspect-1x1` slot)

The post hero cover is a **separate CMS field** from the card cover — they are not always the same image:

| Post | Hero cover | Intrinsic | Note |
|---|---|---|---|
| `/blog-posts/series-a` | `B…f155_6256432b69e584175b132b1a_60e71a5f8b081f448f92552c_Backyard%2520Games.png` | **513×344** | ⚠ Smallest asset on the site. Rendered into a **580×580** box at 1440 → upscaled ~1.7× and letterboxed by `object-fit:contain`. `sizes="(max-width:479px) 90vw, (max-width:767px) 85vw, (max-width:991px) 40vw, 43vw"`, srcset 500w/513w. Low-res on the original; expect it to look soft in the clone too. |
| `/blog-posts/infant-care-101` | `B…f14d_…kelly-sikkema-Z4GKcFAGck4-unsplash.jpeg` | 3375×3182 | same file as its card cover; no `srcset`/`sizes` |

Rendered hero box: **580×580 @1440 · 440.8×440.8 @1024 · 351×351 @390**, `border-radius:32px`.

---

## 3. Additional covers seen only in "Similar articles" grids

These are posts on pages 2–4 of the collection (the list is 4 pages × 9). Captured because their covers load on the two sample post pages.

| Slug | Cover (prefix `B`) | Intrinsic | srcset widths |
|---|---|---|---|
| `/blog-posts/working-through-working-mom-guilt` | `682e5411afe4660a9707f15d_63a318ae3aa639e25f14c342_alexander-dummer-UH-xs-FizTk-unsplash.jpeg` | **720×636** | 500/720 |
| `/blog-posts/transferable-skills-for-sahm-resumes-problem-solving-skills` | `682e5411afe4660a9707f15c_636c3a60d91a93144f4dd58e_jose-escobar-tHLCjhDCw3M-unsplash.jpeg` | **3634×3144** | 500/800/1080/1600/2000/2600/3200/3634 |
| `/blog-posts/transferable-skills-for-sahm-resumes-communication-skills` | `682e5411afe4660a9707f15b_63597841cf05da1a9748b313_sai-de-silva-httxBNGKapo-unsplash.jpeg` | **3205×2965** | 500/800/1080/1600/2000/2600/3200/3205 |
| `/blog-posts/what-to-include-in-a-babysitting-bag` | `682e5411afe4660a9707f160_639a2f443b8fed7f9a477ecb_stephen-andrews-u0zTce7KNlY-unsplash.jpeg` | **4292×3793** | 500/800/1080/1600/2000/2600/3200/4292 |

---

## 4. Fonts

**No new fonts.** Identical set and identical URLs to the homepage — see `ASSETS.md`. All `format("woff")`, `font-display:swap`, bucket `A`:

| Family | Weight/Style | File |
|---|---|---|
| Jokker | 400 normal | `A682e5411afe4660a9707efe4_Jokker-Regular.woff` |
| Jokker | 400 italic | `A682e5411afe4660a9707efe3_Jokker-RegularItalic.woff` |
| Jokker | 500 normal | `A682e5411afe4660a9707efe2_Jokker-Medium.woff` |
| Jokker | 500 italic | `A682e5411afe4660a9707efdd_Jokker-MediumItalic.woff` |
| Jokker | 600 normal | `A682e5411afe4660a9707efe0_Jokker-Semibold.woff` |
| Reckless Neue | 900 normal | `A682e5411afe4660a9707efde_RecklessNeue-Heavy.woff` |

**Reckless Neue is used at `font-weight:400` on these pages** (the `h1`s carry `.u-mb-0`, which declares `font-weight:400`). Only the 900 Heavy file is loaded, so the browser **synthesises nothing and simply renders Heavy** — the visual result is still the heavy cut. Ship only `RecklessNeue-Heavy.woff` and declare it as the single `@font-face` for the family, exactly as the homepage does, so `font-weight:400` still resolves to it.

Inconsolata (Google) is still requested by the WebFont loader and still unused. Skip it.

---

## 5. Non-image assets / no-ops

- **No SVG files fetched over the network.** `bullet-organic.svg` and `join-bg.svg` (homepage) are **not** used on blog or legal. The only SVG on these pages is the inline Otter wordmark.
- **No `<video>`, no `<iframe>`, no canvas, no `.swiper`** on any of the five pages.
- **No background-image CSS assets** on any blog/legal element (zero gradients, zero `url()` backgrounds).
- Tracking pixels present in `<noscript>` on all five pages — **do not port**:
  - `https://www.facebook.com/tr?id=2667541703549888&ev=PageView&noscript=1`
  - `https://flask.nextdoor.com/pixel?pid=5385b479-ad20-4ab3-b8df-644cbd737389&ev=PAGE_VIEW&noscript=1`
- Third-party script that **does** do work on `/blog` (reimplement natively, don't port): `https://cdn.jsdelivr.net/npm/@finsweet/attributes-cmsload@1/cmsload.js`
- `<link rel="prerender" href="?77d76c3c_page=2">` on `/blog` — drop.

---

## 6. Missing-asset findings

**None.** All 17 content images across `/blog`, `/blog-posts/series-a`, `/blog-posts/infant-care-101`, `/terms-of-use` and `/privacy-policy` were fetched and confirmed:

```
blog-cta.webp                                    HTTP 200  image/webp  210,840 B
blog-cta-p-500.webp                              HTTP 200  image/webp   25,786 B
Blog Hero.webp                                   HTTP 200  image/webp  131,856 B
Playing_Colored_01 1.webp                        HTTP 200  image/webp  230,002 B
kelly-sikkema-Z4GKcFAGck4-unsplash.jpeg          HTTP 200  image/jpeg 1,321,541 B
```
…and every remaining cover resolved to a valid decoded bitmap in-browser (intrinsic dimensions listed in §2/§3, which is only obtainable from a successful decode).

Quality caveats rather than missing files:
- `Backyard Games.png` (513×344) is **materially under-sized** for its 580×580 render slot on `/blog-posts/series-a`. Upstream problem; reproduce as-is.
- `/terms-of-use` and `/privacy-policy` reference **zero images** of their own — they inherit only the nav/footer wordmark. Nothing to fetch for the legal routes.
