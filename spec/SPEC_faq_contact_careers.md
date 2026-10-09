Source: https://withotter.com/

# Otter — Build Spec: `/faq`, `/contact`, `/careers`

Measured live with Playwright on 2026-10-08 at **1440×900**, **1024×900**, **390×844**.
Companion asset notes: `spec/ASSETS_faq_contact_careers.md`.
Shared design-system baseline: `CLONE_SPEC.md` (homepage). **Read that first** — this document only records what is new or different.

Raw HTML captured for all three routes; compiled CSS is byte-identical to the homepage's
(`https://cdn.prod.website-files.com/682e5411afe4660a9707efce/css/with-otter-ac17371ef8a503ba0b8fca450052.shared.34930fed5.min.css`),
so every class below already exists in the one stylesheet the homepage ships.

Document heights:

| Route | 1440 | 1024 | 390 |
|---|---|---|---|
| `/faq` | 2019 | 2198 | 2090 |
| `/contact` | 2043 | 2189 | 2386 |
| `/careers` | 6631 | 7477 | 8532 |

---

## 0. Baseline spot-check — what holds, and the three things that don't

**Confirmed identical to `CLONE_SPEC.md`** (re-measured on these routes, not assumed):

- Same single stylesheet; `:root` tokens unchanged.
- Fonts: same 4 self-hosted files actually downloaded on all three routes — `Jokker-Regular.woff`, `Jokker-Medium.woff`, `Jokker-Semibold.woff`, `RecklessNeue-Heavy.woff`, plus the unused Inconsolata woff2. `format("woff")`, `font-display:swap`.
- `.container` 90%/max 90rem; `.cc-narrow` max 75rem → **1200px @1440, 921.594px @1024, 351px @390**.
- `.row` margin-inline −20px, `.col` padding 20px + margin-bottom 40px, `.col` → `flex-basis:100%;order:1` at ≤479.
- `.section` padding-block **80px @1440 & @1024, 48px @390**. 1024 renders desktop styles (confirmed: `.col-lg-*` still active, `.col-md-hide` not applied).
- Nav is **not** sticky: `position:relative`, `margin:48px 0`, height 60px @1440/1024; `margin:32px 0 48px`, height 48px @390.
- `.btn` transition `color/background-color/border-color .3s cubic-bezier(.165,.84,.44,1)`; `:hover` → bg `--peach`, color `--primary`. Verified live on the contact submit button (`#00373e`→`#fbd3b6`, `#cafff2`→`#00373e`).
- The 7 clip-path `<clipPath>` defs and the three global `<style>` embeds are shipped on every route, identical. **No new clip paths and no new path `d` strings on these three routes** — `/careers` reuses `#stone-hero_top-left` and `/faq` reuses `#footer-shape-right` + `#stone-hero_bottom-left`. Use the `d` strings already in `CLONE_SPEC.md` §5 verbatim.
- No gradients, no `backdrop-filter`, no `<video>`, no `<canvas>`, no `.swiper` elements on any of the three routes. Nothing auth-gated; everything below was read from the live DOM.

**Differences from the homepage spec — correct these three things:**

1. **The nav has four content links on these routes** (`/parents`, `/sitters`, `/trust-safety`, `/blog`) in a second `.nav_links-parent` group. The homepage had only the Log in / Sign up group. This means `.nav_link-current-icon` **is** present in the DOM here and the hover effect is real (§2.1). `CLONE_SPEC.md` §7.4 says "not present in this page's DOM — no nav hover effect to build"; that is true of `/` only.
2. **The footer link container is populated** — three `ul.footer_link-list` columns with 11 links. On the homepage `.footer_links-container` was an empty 0-height spacer (§2.2).
3. **The mobile-nav IX2 interaction uses different action lists.** The homepage fires `e-41`/`e-42` → `a-10`/`a-11`. These three routes fire **`e-13`/`e-14` → `a-5`/`a-6`**, and their button carries `data-w-id="e9e5205a-cbfa-d6b9-11fc-6e90b3191d6d"` (the homepage's is `47e1fa15-…-a6c`). The timings differ slightly on close — see §5.1.

---

## 1. New type roles / utility classes (not in `CLONE_SPEC.md` §4)

All computed values measured; `@1440` and `@1024` are identical for every row below unless a third value is given.

| Role | Selector | @1440 / @1024 | @390 | Colour |
|---|---|---|---|---|
| **Page H1 (weight-400 variant)** | `h1.u-mb-0` (`/contact`, `/careers`) | `80px / 80px`, **w400**, ls `-0.8px`, Reckless Neue, `mb 0` | `48px / 48px`, w400, ls `-0.48px` | `#00373e` |
| **Page H1 (weight-900)** | `h1` bare (`/faq`) | `80px / 80px`, **w900**, ls `-0.8px`, `mb 16px` | `48px / 48px`, w900, `mb 9.6px` | `#00373e` |
| **Section H2** | `h2.h3` / `h2.h3.u-mb-0` | `56px / 56px`, w600, `mb 22.4px` (`.u-mb-0` → 0) | `28.8px / 28.8px`, w600, `mb 8.64px` | `#00373e` |
| **Centred H2 w/ 2em gap** | `h2.h3.u-text-center.u-mb-2` | `56px / 56px`, w600, `mb 112px`, centered | `28.8px`, `mb 57.6px` | `#00373e` |
| **Lede (left-aligned)** | `p.paragraph-1-5.u-mb-0` | `24px / 36px`, **w400**, `text-align:left`, `mb 0` | `18px / 27px`, w400 | `#00373e` |
| **Body (centred-header variant)** | `.cc-centered p.paragraph-1-25.u-mb-0` | `20px / 30px`, w400, **`text-align:left`**, `flex:1 1 0%` | `16px / 24px` | `#00373e` |
| **Stat eyebrow** | `.stat-contain h3.eyebrow` | `14px / 19.6px`, w600, ls `0.49px`, uppercase, `mb 4.2px` | same | `#00373e` |
| **Stat figure** | `.stat-contain div.h4.u-mb-0` | `40px / 44px`, w600, `text-align:left`, `mb 0` | `20px / 24px`, w600 | `#00373e` |
| **Stat body** | `.stat-contain p` | `16px / 24px`, w500, `mb 16px` | same | `#00373e` |
| **Values row label** | `.values_item .paragraph-1-5` | `24px / 36px`, w500, `text-align:center`, `mb 24px` | `18px / 27px`, `mb 18px` | `#00373e` |
| **Values card title** | `.values-wrap h3.h4.u-mb-2.u-text-center` | `40px / 44px`, w600, centered, `mb 80px` | `20px / 24px`, `mb 40px` | `#00373e` |
| **Benefit card title** | `h3.trust-bar_header` | `32px / 38.4px`, w600, `mb 0` | `20px / 24px`, w600 | `#ffffff` |
| **Benefit card body** | `.trust-card_header p.u-mb-0` | `16px / 24px`, **w400**, `mb 0` | same | `#ffffff` |
| **Job row title** | `.faq-spacer h3.paragraph-1-5.u-mb-0` | `24px / 28.8px`, **w400**, `text-align:left`, `mb 0` | `18px / 21.6px`, w400 | inherits row |
| **Job row location** | `.faq-content p.u-mb-0` | `16px / 24px`, w400, `mb 0` | same | inherits row |
| **Input label** | `label.input-label` | `16px / 16px`, w500, `margin:0 0 8px 20px`, `border-radius:0 3px 0 0`, `z-index:1`, `display:block`, `cursor:default` | same | `#00373e` |
| **Required note** | `.form_required-note` | `12.8px / 19.2px` (`.8rem`), w400, `position:absolute; inset:auto 0 0 auto` | same | `#00373e` |
| **Success heading** | `.form-success h4.u-mb-0` | `40px / 44px`, **w400**, centered, `mb 0` | `20px / 24px` | `#00373e` |
| **Error text** | `.form-error`, `.form-error > div` | `16px / 24px`, w400 | same | **`#e31700`** |
| **Nav content link** | `a.nav_link` (not `.cc-log-in`) | `16px / 24px`, w500, `padding:8px 0`, `position:relative; overflow:hidden` | `24px / 36px` (`1.5em`), `padding 0`, `width:100%` | `#00373e` |
| **Footer nav link** | `.footer_link a` | `16px / 24px`, w500, `display:inline` | same | `#00373e` |

New utility classes used here and not on the homepage:

```css
.u-mb-1 { margin-bottom: 1em }
.u-mb-2 { margin-bottom: 2em }
.u-mt-1 { margin-top: 1em }
.u-bg-coral { background-color: var(--coral); color: var(--primary) }
.shape.rotate-90 { transform: rotate(90deg) }          /* computed matrix(0,1,-1,0,0,0) */
.col.col-md-hide { display: none }                      /* @≤991 only */
.col.col-sm-hide { display: none }                      /* @≤767 only */
.col.col-sm-first { order: -1 }                         /* @≤767 only */
.u-sr-only { width:1px; height:1px; margin-top:-1px; padding:0; border:0; white-space:nowrap; position:absolute; overflow:hidden }
.section-header.cc-centered { text-align:center; align-items:center }
.u-aspect-9x16 { background:var(--ivory); border-radius:2em; width:100%; padding-top:56%;
                 display:flex; justify-content:center; align-items:center; position:relative;
                 overflow:hidden; isolation:isolate }
@media(max-width:767px){ .u-aspect-9x16 { border-radius:1em } }
```

> `.u-aspect-9x16` is a **56%** padding-top box (≈16:9), not 9:16. Measured `580 × 324.797` @1440, `440.797 × 246.844` @1024, `351 × 196.547` @390 (radius 32px / 32px / **16px**).
> Note `.u-mb-0` also sets `font-weight:400`, which is why several headings above compute w400. This is load-bearing for `h1.u-mb-0`: `/contact` and `/careers` request Reckless Neue **400**, but only the **900** `RecklessNeue-Heavy.woff` is hosted, so the browser synthesises a lighter face from the Heavy file. Reproduce by keeping `font-weight:400` on that h1 with only the Heavy font declared — do **not** "fix" it to 900.

---

## 2. Shared chrome deltas (apply to all three routes)

### 2.1 Nav with content links + the hover "stone" icon

`div.container.cc-nav` → `div.nav_menu` → `div.nav_menu-card` now holds **two** `.nav_links-parent` groups:

```css
.nav_links-parent { display:flex; gap:1em; flex-wrap:nowrap; align-items:center }
@media(max-width:991px){
  .nav_links-parent { gap:16px; flex-direction:column; align-items:flex-start;
                      padding-bottom:2rem; border-bottom:1px solid var(--primary) }
  .nav_links-parent.cc-buttons { gap:1.5em; flex-direction:row; align-items:center;
                                 padding-bottom:0; border:1px #000 }
}
@media(max-width:479px){ .nav_links-parent, .nav_links-parent.cc-buttons { gap:1.25em } }
```

Group 1 (content links), DOM order and measured @1440:

| Text | href | rect @1440 | rect @1024 | width |
|---|---|---|---|---|
| Parents | `/parents` | `72, 58` | `51.2, 58` | 59.359 × 40 |
| Sitters | `/sitters` | `147.4, 58` | `126.6, 58` | 49.859 × 40 |
| Trust & Safety | `/trust-safety` | `213.2, 58` | `192.4, 58` | 106.219 × 40 |
| Blog | `/blog` | `335.4, 58` | `314.6, 58` | 34.109 × 40 |

Group 2 `.nav_links-parent.cc-buttons` — unchanged from homepage ("Log in" + white "Sign up" pill), 161.922 × 46, right-aligned at `x=1206.1` @1440 / `x=810.9` @1024.

Each content link contains a hover reveal:

```html
<a href="/parents" class="nav_link w-inline-block">
  <div>Parents</div>
  <div class="nav_link-current-icon">
    <div class="current-icon"><div class="w-embed"><svg …/></div></div>
  </div>
</a>
```

```css
.nav_link-current-icon {
  z-index:-1; opacity:0; color:var(--celeste); mix-blend-mode:multiply;
  display:flex; justify-content:center; align-items:center;
  width:100%; height:100%; margin-inline:auto;
  position:absolute; inset:0; transform:translateY(100%);
  transition: opacity .3s cubic-bezier(.165,.84,.44,1),
              transform .3s cubic-bezier(.165,.84,.44,1);
}
.current-icon { width:2.5em; position:relative; top:3px }
@media(max-width:991px){ .nav_link-current-icon { color:var(--coral) } .current-icon { width:1.5em } }
```

Reveal rule (lives in the page's global `<style>`, **min-width** query — the only min-width query on the site):

```css
@media screen and (min-width: 992px) {
  .nav_link.w--current .nav_link-current-icon,
  .nav_link:hover     .nav_link-current-icon { opacity:1; transform:translateY(0) }
}
```

Measured default state @1440: `opacity:0`, `transform:matrix(1,0,0,1,0,40)` (= translateY(100%) of the 40px-tall link), `z-index:-1`, `mix-blend-mode:multiply`, colour `#cafff2`; `.current-icon` 40 × 32.875 at `inset:3px 0 -3px`. @390 colour becomes `#fbad9c` and `.current-icon` width 36px.

The icon is an inline organic blob, `viewBox="0 0 34 22"`, `fill="currentColor"`, `width/height 100%`:

```
M0.54127 7.43938C-1.37846 10.4619 2.25598 18.3642 4.46461 19.6478C8.02481 21.6745 12.1971 22.4246 16.2626 21.769C20.5028 21.1227 33.3538 20.3852 33.9689 15.0138C34.4908 10.6803 28.3029 4.0891 26.2993 2.86916C24.0627 1.51267 15.6755 -0.553935 13.1127 0.137967C10.55 0.82987 2.29326 4.68998 0.54127 7.43938Z
```

`.nav_link.w--current` also has a ≤991px style — `background:#fbad9cbd; border-radius:99px; padding:8px 16px` — but **none of these three routes has a nav link matching its own URL**, so `w--current` never applies in the nav here. (It does apply to the *footer* `/faq`, `/contact`, `/careers` link, which has no distinct styling.) Build the rule, expect it unused on these routes.

### 2.2 Footer link columns

`div.footer_row` → `div.footer_links-container` is populated:

```css
.footer_links-container { display:flex; flex-flow:wrap; width:80% }
.footer_link-list { width:25%; padding-left:0 }        /* ul.w-list-unstyled */
.footer_link { margin-bottom:1.25rem; font-size:1rem } /* li */
@media(max-width:991px){ .footer_link-list { width:30% } }
@media(max-width:767px){ .footer_links-container { justify-content:space-between; width:100% }
                         .footer_link { margin-bottom:.8rem } }
@media(max-width:479px){ .footer_link-list { width:50%; margin-bottom:1em } }
```

Measured: container `627.125 × 192` @1440 (x 544.1), `673.266 × 192` @1024, `303 × 326.375` @390 (`justify-content:space-between`, 2-up). Each `.footer_link-list` 156.781px @1440 / 168.312px @1024 / 151.5px @390 wide, `margin-bottom:16px`. `li` height 24px, `margin-bottom:20px` (**12.8px @390**). Links `display:inline`, 16px/24px, w500, `#00373e`.

Three columns, DOM order:

| Col 1 | Col 2 | Col 3 (`target="_blank"`) |
|---|---|---|
| Parents → `/parents` | FAQ → `/faq` | Instagram → `https://www.instagram.com/otterchildcare/` |
| Sitters → `/sitters` | Careers → `/careers` | Facebook → `https://www.facebook.com/withotter/` |
| Trust & Safety → `/trust-safety` | Blog → `/blog` | Twitter → `https://twitter.com/WithOtter` |
| | Contact → `/contact` | Linkedin → `https://www.linkedin.com/company/withotter` |

Everything else in the footer (`.footer_card.cc-left` / `.cc-right`, the two clipped shapes, terms row, copyright `© 2025 With Otter Inc.`) is **identical to the homepage**, including copy and the `.btn` "Get started". The stray empty `div.container` before `.cc-footer-container` is present here too.

---

## 3. `/faq` — "Common Questions • Otter Kidcare"

### 3.1 ⚠ The accordion does not exist on the live page

**This is the single most important finding for this route.** There is no accordion, no disclosure panel, no toggle icon, no category tabs and no filters in the live DOM. Both FAQ categories render Webflow's **empty-collection placeholder**:

```html
<div class="w-dyn-list">
  <div class="w-dyn-empty"><div>No items found.</div></div>
</div>
```

Verified three ways:
- Raw server HTML contains no collection-item template at all (Webflow emits only `.w-dyn-empty` when a list has zero published items) — so this is a genuinely empty CMS collection, not a client-render failure.
- `document.querySelectorAll('.faq-item').length === 0`; the string `accordion` appears in no class name on any of the three routes.
- Zero IX2 events resolve to any accordion target (§5).

Measured placeholder box (Webflow default, unstyled by the site): `background:#dddddd; padding:10px`, height **44px**, inner `div` 24px tall holding "No items found.". Widths: `683.328` @1440, `520.922` @1024, `351` @390.

**Build decision for Build:** reproduce the live page as-is — two category rows with the grey "No items found." placeholder — or stub the collection with content. If you stub it, the design system already contains the full accordion and the matching IX2 timings; both are specced in §3.4 and §5.2 so you do not have to derive them. Do not invent FAQ copy; none is published.

### 3.2 Section-by-section, DOM order

Root `div.page-wrapper` (bg `#f8f6f5`, colour `#00373e`, `overflow:hidden`), preceded by the three hidden global embeds.

| # | Element | pad | y / h @1440 | y / h @1024 | y / h @390 |
|---|---|---|---|---|---|
| 1 | `nav.nav_wrapper` | — | 48 / 60 | 48 / 60 | 32 / 48 |
| 2 | `header.section` | `80px 0` / `48px 0` | 156 / 732 | 156 / 592.8 | 128 / 504.8 |
| 3 | `main#main > section.section` ("For parents") | same | 888 / 278.4 | 749 / 334.4 | 633 / 257.4 |
| 4 | `main#main > section.section` ("For sitters") | same | 1166 / 278.4 | 1083 / 278.4 | 890 / 257.4 |
| 5 | `footer.section.cc-footer` | `80px 0 48px` / `48px 0` | 1445 / 574 | 1362 / 836 | 1148 / 942 |

**2 — `header.section`**

`div.container.cc-narrow` → `div.row.row-align-center.row-justify-between`
(`align-items:center; justify-content:space-between`; measured `1240 × 571.984` @1440 at x=100, `961.594 × 432.781` @1024, `391 × 408.844` @390).

- `div.col.col-lg-6.col-sm-10.col-xs-12` → `div.section-header` (gap **24px**, 16px @390)
  - `h1` → **"Common questions"** — 80px/80px w900 (this route's h1 has no `.u-mb-0`), `mb 16px`. Measured `580 × 160` at `120,414`; `440.797 × 160` at `51.2,344.4` @1024; `351 × 96` at `19.5,176` @390.
- `div.col.u-mb-0.col-lg-5.col-sm-12` → `div.header-shapes-contain` (see §3.3)

**3 / 4 — the two category sections** (structurally identical, only the h2 differs)

```html
<section class="section"><div class="container cc-narrow">
  <div class="row row-justify-around">
    <div class="col col-lg-4 col-sm-12"><div><h2 class="h3">For parents</h2></div></div>
    <div class="col col-lg-7 col-sm-12"><div class="w-dyn-list">…empty…</div></div>
  </div>
</div></section>
```

`.row.row-justify-around { justify-content: space-around }` — new row modifier.
Measured @1440: row `1240 × 118.391` at x=100; `.col-lg-4` `413.328 × 78.391` at x=125.8 (`flex:1 1 33.33%; max-width:33.3333%`); `.col-lg-7` `723.328 × 78.391` at x=590.8 (`58.3333%`). h2 `373.328 × 56`, 56px/56px w600 `mb 22.4px` at `145.8,968`.
@1024: cols 320.516 / 560.922 wide; the "For parents" h2 wraps to 2 lines (112px tall) so the first section grows to 334.4px.
@390: both cols `flex-basis:100%`, h2 28.8px at `19.5,680.8`, list at `19.5,758.3`.

Second section h2 → **"For sitters"**.

### 3.3 `/faq` hero shape stack — `.header-shapes-contain`

```css
.header-shapes-contain { z-index:1; display:flex; flex-direction:column; align-items:flex-end }
@media(max-width:991px){ .header-shapes-contain { justify-content:center; align-items:flex-end;
  width:50%; position:absolute; inset:0 0 0 auto } }
@media(max-width:767px){ .header-shapes-contain { gap:10%; flex-direction:row;
  justify-content:center; align-items:flex-end; width:100%; margin-top:-13%; position:relative } }
@media(max-width:479px){ .header-shapes-contain { justify-content:flex-start; width:100%;
  margin-top:-5%; margin-right:0 } }

.shape-contain.cc-sitters-top    { width:90% }
.shape-contain.cc-sitters-bottom { width:50%; margin-top:-20%; margin-left:auto }
@media(max-width:991px){ .shape-contain.cc-sitters-bottom { margin-top:-40% } }
@media(max-width:767px){ .shape-contain.cc-sitters-top { width:80%; margin-right:-20% }
                         .shape-contain.cc-sitters-bottom { width:40%; margin-top:-33%; margin-left:-10% } }
@media(max-width:479px){ .shape-contain.cc-sitters-top { width:80% }
                         .shape-contain.cc-sitters-bottom { width:50%; margin-top:0;
                           margin-bottom:11%; margin-left:-18% } }
```

Measured `.header-shapes-contain`: `476.656 × 571.984` at `843.3,236` @1440; `360.656 × 432.781` at `612.1,236` @1024; `351 × 280.797` at `19.5,304` @390 with `margin-top:-17.5469px`, `gap:10%`, row direction.

Children:

1. `div.shape-contain.cc-sitters-top` → `div.shape-ratio` → `div.shape.footer-shape-right` → `div.u-aspect-1x1` → `img.u-img-cover`
   Clip path **`url(#footer-shape-right)`** (reused from the footer). Image `hero2.webp`, `alt="a child with their hands on their head"`, `loading="lazy"`.
   Measured `428.984²` at `891,236` @1440; `324.578²` at `648.2,236` @1024; `280.797²` at `19.5,304` @390 (`margin-right:-70.1875px`).
2. `div.shape-contain.cc-sitters-bottom` → `div.shape-ratio` → `div.shape.stone-hero_bottom-left.u-bg-peach`
   Flat `#fbd3b6`, clip path `url(#stone-hero_bottom-left)`, no image.
   Measured `238.328²` at `1081.7,569.7` @1440 (`margin:-95.3281px 0 0 238.328px`); `180.328²` at `792.5,488.5` @1024; `175.5²` at `202,370.7` @390 (`margin:0 0 38.6094px -63.1719px`).

### 3.4 The accordion as the design system defines it (CSS present, zero live instances)

Only needed if Build stubs CMS content. All values read from the shipped stylesheet; **no live box model could be measured because no instance exists** — flagged rather than guessed.

```css
.faq-item {                                 /* the clickable row — closed AND open */
  background-color: var(--white);
  cursor: pointer;
  border-radius: 2.5em;                     /* 40px */
  display: flex; flex-direction: row;
  justify-content: space-between; align-items: flex-start;
  width: 100%; margin-bottom: 1.5em;        /* 24px */
  padding: 1.5em 1.5em 1.5em 2.5em;         /* 24px 24px 24px 40px */
  position: relative;
}
.faq-item:focus-visible,
.faq-item[data-wf-focus-visible] { outline: 3px dashed #00373e; outline-offset: 0 }
@media(max-width:767px){ .faq-item { padding-left: 2em } }   /* 32px */
@media(max-width:479px){ .faq-item { padding-left: 1.5em } } /* 24px */

.faq-content { z-index:3; width:75% }
@media(max-width:767px){ .faq-content { width:86% } }

.faq-spacer { padding-block: .6em }         /* 9.6px */
.faq-answer { overflow: hidden }            /* height animated by IX2 — see §5.2 */

.faq-icon-wrapper {                         /* the toggle button */
  z-index:3; background-color: var(--ivory); border-radius: 99px;
  display:flex; justify-content:center; align-items:center;
  width:2.5em; height:2.5em;                /* 40 × 40 */
  margin-top:1.5em; margin-right:1.5em;     /* 24px */
  position:absolute; inset: 0 0 auto auto;
}
.faq-icon { display:flex; justify-content:center; align-items:center;
  width:1em; min-width:1em; height:1em; min-height:1em;   /* 16 × 16 */
  position:relative; overflow:hidden }

/* the plus/minus glyph */
.icon-line         { background-color: var(--primary); width:4px; height:100% }
.icon-line.cc-hr   { width:100%; height:4px; position:absolute }
/* .icon-line.cc-vr is the vertical bar; it has no extra rule — it is the base .icon-line.
   IX2 rotates it 0deg → 90deg to turn "+" into "−". */
```

- **Toggle icon:** a 16×16 `.faq-icon` containing a horizontal 4px bar (`.icon-line.cc-hr`, absolute) and a vertical 4px bar (`.icon-line.cc-vr`). Open rotates `.cc-vr` by **+90°** about Z so it lies over the horizontal bar → a minus sign. Colour `--primary` on `--ivory` pill.
- **Open/close is IX2-driven, not CSS-transitioned.** `.faq-answer` carries no `transition`; its `height` is animated by IX2 `STYLE_SIZE`. Timings in §5.2.
- **Multiple panels can be open at once.** Each item gets its own independent `MOUSE_CLICK` / `MOUSE_SECOND_CLICK` event pair with no "close siblings" action anywhere in the IX2 data, so toggling one never collapses another.
- **No category tabs or filters.** `.w-tabs`/`.w-tab-link`/`.w-tab-pane` rules exist only as unstyled Webflow defaults and appear in no route's DOM. The two categories are two separate static `<section>`s, not tabs.

---

## 4. `/contact` — "Contact us"

### 4.1 Section-by-section, DOM order

| # | Element | pad | y / h @1440 | y / h @1024 | y / h @390 |
|---|---|---|---|---|---|
| 1 | `nav.nav_wrapper` | — | 48 / 60 | 48 / 60 | 32 / 48 |
| 2 | `header.section` | `80px 0` / `48px 0` | 156 / 636.7 | 156 / 520.7 | 128 / 232 |
| 3 | `main#main > section.section` | same | 792.7 / 676 | 676.7 / 676 | 360 / 996 |
| 4 | `footer.section.cc-footer` | `80px 0 48px` / `48px 0` | 1468.7 / 574 | 1352.7 / 836 | 1356 / 1030 |

**2 — `header.section`** → `div.container.cc-narrow` → `div.row.row-justify-between.row-align-center` (`1240 × 476.656` @1440; `961.594 × 360.656` @1024; `391 × 136` @390)

- `div.col.col-lg-5.col-md-7.col-sm-11.u-mb-0` → `div.section-header` (gap 24px / 16px @390)
  - `h1.u-mb-0` → **"Contact us"** — 80px/80px **w400**, ls −0.8px, `mb 0`. Measured `416.562 × 80` at `120,392.3`; `360.656 × 160` (wraps) at `51.2,279.3` @1024; `249.938 × 48` at `19.5,176` @390.
  - `p.paragraph-1-25.u-mb-0` → **"Otter matches parents who need care with trusted sitters in their community, on demand."** — 20px/30px w500, `text-align:left`, `flex:1 1 0%`. `476.656 × 60` at `120,496.3`; `16px/24px`, `318.406 × 72` at `19.5,240` @390.
- `div.col.u-mb-0.col-lg-5.col-sm-hide` → bare `div` → `div.u-aspect-1x1` → `img.u-img-cover`
  `Contact Hero.webp`, `alt=""`, `loading="lazy"`, `sizes="(max-width: 767px) 100vw, (max-width: 991px) 33vw, 35vw"`.
  Measured `476.656²` at `843.3,236` @1440 (rendered 476.7 × 476.7, intrinsic of served variant 504 × 469); `360.656²` at `612.1,236` @1024. **`display:none` at ≤767** via `.col-sm-hide`, so the hero image is absent at 390.

**3 — the form section** → `div.container.cc-narrow`
- `h2.u-sr-only` → **"Form"** (visually hidden; keep for a11y)
- `div.row.row-justify-between`
  - `div.col.col-lg-7.col-md-12` → `div.u-mb-0.w-form` → the form (§4.2)
    Measured col `723.328 × 476` at x=100 @1440; `560.922 × 476` @1024; `391 × 716` at `-0.5,408` @390.
  - `div.col.col-lg-4.col-md-12` → two `.contact-info` blocks (§4.4)
    Measured col `413.328 × 476` at x=926.7 @1440; `320.516 × 476` @1024; `391 × 192` at `-0.5,1164` @390.

### 4.2 The form — attributes

```html
<form id="wf-form-Contact-Form" name="wf-form-Contact-Form" data-name="Contact Form"
      method="get" class="form"
      data-wf-page-id="682e5411afe4660a9707f05b"
      data-wf-element-id="deb1166d-d0d5-d9af-2db6-2913476f0d5b">
```

- **`action` is absent** and `method="get"`. There is no `data-redirect` and no `novalidate`. Webflow's `webflow.js` intercepts `submit` and AJAX-POSTs to Webflow's own form endpoint, then toggles `.w-form-done` / `.w-form-fail`. A clone must supply its own handler; the markup carries no endpoint.
- Native HTML validation **is** active (no `novalidate`), so the browser blocks submit on the three `required` fields.
- `.form { width:100%; position:relative }` — measured `683.328 × 476` @1440, `520.922 × 476` @1024, `351 × 716` @390.

Fields in DOM order, inside `div.row` → one `div.col` each:

| # | Col classes | `<label for>` / text | element | `name` | `data-name` | `id` | type | placeholder | required | maxlength |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `col col-lg-6 col-xs-12` | `First-Name` → **First Name\*** | `input.input.w-input` | `First-Name` | `First Name` | `First-Name` | `text` | `e.g. Jane` | ✅ | 256 |
| 2 | `col col-lg-6 col-xs-12` | `Last-Name-2` → **Last name\*** | `input.input.w-input` | `Last-Name` | `Last Name` | `Last-Name-2` | `text` | `e.g. Doe` | ✅ | 256 |
| 3 | `col col-lg-6 col-xs-12` | `Email` → **Email\*** | `input.input.w-input` | `Email` | `Email` | `Email` | `email` | `hello@withotter.com` | ✅ | 256 |
| 4 | `col col-lg-6 col-xs-12` | `Phone` → **Phone** | `input.input.w-input` | `Phone` | `Phone` | `Phone` | `tel` | `(123) 456-7890` | ❌ | 256 |
| 5 | `col u-mb-0` | `Comments` → **Comments** | `textarea.input.cc-text-area.w-input` | `Comments` | `Comments` | `Comments` | textarea | `Leave us a message...` | ❌ | 5000 |

> Note the `id`/`name` mismatch on field 2: `id="Last-Name-2"` but `name="Last-Name"`. Keep both verbatim — the label's `for` points at the id.

Then, as direct children of `<form>`:
- `input[type=submit].btn.u-mt-1.w-button` — `value="Submit"`, **`data-wait="Please wait..."`**
- `div.form_required-note` → **"\*Required"**

Siblings of `<form>` inside `.w-form`: `div.form-success.w-form-done`, then `div.form-error.w-form-fail`.

### 4.3 Form box model and every state

```css
.input-group { display:block; flex-direction:column; text-align:left; position:relative }
.input-group.cc-textarea { min-height:140px }

.input-label { z-index:1; color:var(--primary); display:block;
  margin:0 0 8px 20px; border-top-right-radius:3px;
  font-size:1rem; font-weight:500; line-height:1; position:relative }

.input {
  border:1px solid var(--primary);
  background-color:var(--ivory);
  color:var(--primary);
  border-radius:99px;
  height:100%; min-height:3.5rem;        /* 56px */
  margin-bottom:0; padding:1em 1.25em;   /* 16px 20px */
  font-size:1rem;
  transition: border-color .3s cubic-bezier(.165,.84,.44,1);
}
.input:hover, .input:focus          { border-color: var(--primary) }   /* = default, no visual change */
.input:focus-visible,
.input[data-wf-focus-visible]       { border-width: 2px }
.input::placeholder                 { color: #00373e5e }               /* rgba(0,55,62,.37) */
.input.cc-text-area                 { border-radius:24px; min-height:150px }
```

Measured, all three widths (geometry identical except width):

| Element | @1440 | @1024 | @390 |
|---|---|---|---|
| `.input-group` (fields 1–4) | `321.656 × 80` | `240.453 × 80` | `351 × 80` |
| `.input-group.cc-textarea` | `683.328 × 174` | `520.922 × 174` | `351 × 174` |
| `label.input-label` | `301.656 × 16` | `220.453 × 16` | `331 × 16` |
| `input.input` | `321.656 × 56` | `240.453 × 56` | `351 × 56` |
| `textarea.input.cc-text-area` | `683.328 × 150` | `520.922 × 150` | `351 × 150` |
| `input[type=submit].btn` | `97.578 × 46` | `97.578 × 46` | `97.578 × 46` |

`form .row`: `723.328 × 414` @1440 / `560.922 × 414` @1024 / `391 × 654` @390, `margin-inline:-20px`.
`form .col.col-lg-6`: `flex:1 1 50%; max-width:50%`, 4 of them → 2×2 grid @1440/1024 at y 872.7 and 992.7 (120px row pitch); `flex-basis:100%` and `order:1` @390 → 4 stacked rows at y 408 / 528 / 648 / 768.
Submit button: `margin-top:16px` (`.u-mt-1`), `padding:14px 20px`, `border-radius:1584px` (99em pill), `white-space:pre`.
`.form_required-note`: `position:absolute; inset:auto 0 0 auto`, measured `63.016 × 19.188` — computed inset `456.812px 0 0 620.312px` @1440, `456.812px 0 0 457.906px` @1024, `696.812px 0 0 287.984px` @390.

**All states, measured live** (focused / hovered / filled in a real browser; the form was **not** submitted):

| State | How reached | Result |
|---|---|---|
| **default** | — | bg `#f8f6f5`, text `#00373e`, border `1px solid #00373e`, radius 99px, 56px tall, no shadow |
| **placeholder** | — | `rgba(0, 55, 62, 0.37)` |
| **hover** | pointer over input | **no visual change** — `:hover` re-declares the same `border-color`. Border stays 1px. |
| **focus (keyboard or `.focus()`)** | Tab / programmatic | **`border-width: 2px`** (`:focus-visible`), colour unchanged `#00373e`. `outline` resolves to `none`. Transition only covers `border-color`, so the 1px→2px width change **snaps** while colour is unchanged — visually an instant thickening. |
| **focus (mouse click)** | click | same 2px — text inputs always match `:focus-visible` |
| **filled** | typed "Jane" | identical to focus state; value colour `#00373e`. No separate filled styling. |
| **error** | — | **There is no author-written error styling at all.** Verified by scanning every CSSOM rule for `:invalid`, `:user-invalid`, `.w-input-error`, `aria-invalid` → **0 matches**. Invalid fields get only the browser's native validation bubble. Do not invent an error ring. |
| **disabled** | simulated by setting `disabled` | Webflow base only: `background-color:#eee`, `cursor:not-allowed`, border unchanged `1px solid #00373e`, `opacity:1`. **No field is disabled on the live page.** |
| **textarea** | — | same colours, `border-radius:24px`, `min-height:150px`, `resize:both` (not reset) |
| **submit default** | — | bg `#00373e`, colour `#cafff2`, border `1px solid transparent`, radius pill |
| **submit hover** | pointer over | bg **`#fbd3b6`**, colour **`#00373e`**, transitioned `.3s cubic-bezier(.165,.84,.44,1)` |
| **submit focus-visible** | Tab | `outline: 2px dashed var(--primary); outline-offset:2px` (inherited `.btn` rule) |
| **submit submitting** | — | Webflow swaps `value` to `data-wait` → **"Please wait..."** |

### 4.4 Success and error message blocks (hidden by default)

Both are `display:none` until Webflow toggles them. Measured by unhiding in the DOM at 1440.

**Success — `div.form-success.w-form-done`**

```css
.form-success { background-color: var(--white); border-radius: 1.5em; /*24px*/
                min-height: 320px; position: relative }
.form-success_flex { display:flex; flex-direction:column; justify-content:center;
  align-items:center; width:100%; max-width:500px; height:100%;
  margin-inline:auto; position:absolute; inset:0 }
@media(max-width:767px){ .form-success_flex { max-width:340px } }
@media(max-width:479px){ .form-success_flex { padding-inline:30px } }
.trust-card_icon { max-width:6.5rem; margin-bottom:3rem }   /* 104px / 48px */
@media(max-width:479px){ .trust-card_icon { width:50% } }
```

Webflow's own `.w-form-done { text-align:center; background-color:#ddd; padding:20px; display:none }` still contributes `text-align:center` and `padding:20px`; the site's `.form-success` overrides only the background and radius. **Measured: `padding:20px` is live** (`683.328 × 320` at `120,473`, bg `#ffffff`, radius 24px, min-height 320px, `text-align:center`). `.form-success_flex` measured `500 × 320` at `212,473`.

```html
<div class="form-success w-form-done">
  <div class="form-success_flex">
    <div class="trust-card_icon">
      <img src="…682e5411afe4660a9707f021_safety.webp" loading="lazy" alt="Dedicated support"/>
    </div>
    <h4 class="u-mb-0">Thanks for reaching out! We’ll be in touch soon.</h4>
  </div>
</div>
```

- Copy: **"Thanks for reaching out! We’ll be in touch soon."** (curly apostrophe U+2019).
- `h4.u-mb-0` measured `500 × 88` at `212,625` — **40px / 44px, weight 400, centered** (`.u-mb-0` forces w400).
- The icon `img` has `loading="lazy"` inside a `display:none` ancestor, so it is **never fetched on a normal page load** (`naturalWidth === 0`, empty `currentSrc`). The URL is valid (200, `image/webp`, 7708 bytes) — see the asset file. `.trust-card_icon` measured `0 × 24` only because the image never loaded; with the image present expect max-width 104px and `margin-bottom:48px`.

**Error — `div.form-error.w-form-fail`**

```css
.form-error { color:#e31700; background-color:transparent;
              border-top:1px solid #e31700; margin-top:16px; padding:8px 0 0 }
```

(Overrides Webflow's default `.w-form-fail { background-color:#ffdede; margin-top:10px; padding:10px }` — the site's version is a transparent block with a red top rule, **not** a pink box.)

```html
<div class="form-error w-form-fail">
  <div>Oops! Something went wrong while submitting the form.</div>
</div>
```

- Copy: **"Oops! Something went wrong while submitting the form."**
- Measured `683.328 × 33` at `120,809` (when shown directly after the form): colour `#e31700`, bg transparent, `border-top:1px solid #e31700`, `margin-top:16px`, `padding:8px 0 0`, `text-align:start`, 16px/24px w400. Inner `div` `683.328 × 24`.

### 4.5 Contact info blocks

```css
.contact-info { display:flex; align-items:center; gap:1.5em; margin-bottom:2.5rem }  /* 24px / 40px */
.contact-info_icon { background-color:var(--primary); color:var(--celeste);
  border-radius:99px; display:flex; justify-content:center; align-items:center;
  width:3.5rem; height:3.5rem; padding:14px }                                        /* 56 × 56 */
.icon-wrap-24 { width:24px; height:24px; overflow:hidden }
.conta-info_emails { display:flex; flex-direction:column; gap:8px }                  /* sic: "conta" */
```

Measured @1440: `.contact-info` `373.328 × 56` at `946.7,872.7` and `946.7,968.7` (96px pitch = 56 + 40 margin). Icon pill 56 × 56, `padding:14px`, bg `#00373e`, colour `#cafff2`. `.icon-wrap-24` 24 × 24 at `962.7,888.7`. `.conta-info_emails` `186.656 × 56` (block 1, two links) / `180 × 24` (block 2).
@390 the whole column drops below the form: blocks at `19.5,1164` and `19.5,1260`.

**Block 1** — inline `<svg viewBox="0 0 28 28">`, envelope, two paths: the outer body `fill="currentColor"` (→ `--celeste`) and the flap `fill="#00373E"` hard-coded. Then `div.conta-info_emails` with two `<a>`:
- `mailto:support@withotter.com` → **support@withotter.com**
- `mailto:media@withotter.com` → **media@withotter.com**

**Block 2** — inline `<svg viewBox="0 0 24 24">`, map pin, outer `fill="currentColor"`, inner circle `fill="#00373E"`. Then `div.conta-info_emails` with a plain `<div>` → **"San Francisco, CA 94114"** (not a link).

Both SVGs are `width="100%" height="100%"` inside the 24px wrapper. Copy them inline; they are not network assets.

---

## 5. `/careers` — "Careers • Join our team"

### 5.1 Section-by-section, DOM order

| # | Element | id | y / h @1440 | y / h @1024 | y / h @390 |
|---|---|---|---|---|---|
| 1 | `nav.nav_wrapper` | — | 48 / 60 | 48 / 60 | 32 / 48 |
| 2 | `header.section` — hero | — | 156 / 766 | 156 / 882 | 128 / 798.3 |
| 3 | `section.section` — "Kidcare that fills the gap" | — | 922 / 524.8 | 1038 / 540 | 926 / 570.3 |
| 4 | `section.section` — "The kidcare gap" stats | — | 1447 / 759.6 | 1578 / 807.6 | 1497 / 845.7 |
| 5 | `section.section` — values / operating principles | — | 2206 / 824 | 2386 / 940 | 2342 / 1024 |
| 6 | `section.section` — Benefits | — | 3030 / 1439.6 | 3326 / 1674.3 | 3366 / 2536.4 |
| 7 | `section.section` — compensation philosophy | — | 4470 / 709.6 | 5000 / 733.6 | 5903 / 889.2 |
| 8 | `section.section` — Current Positions | **`jobs`** | 5180 / 877.5 | 5733 / 907.5 | 6792 / 797.9 |
| 9 | `footer.section.cc-footer` | — | 6057 / 574 | 6641 / 836 | 7590 / 942 |

All `section` paddings are the standard `80px 0` (`48px 0` @390); footer `80px 0 48px` / `48px 0`.

**2 — hero** → `div.container.cc-narrow` → `div.row.row-justify-between.row-align-center`

- `div.col.col-lg-6.col-md-6.col-sm-10.col-xs-12` → `div.section-header` (gap 24px / 16px @390; measured `580 × 566` at `120,236`, `440.797 × 682` @1024, `351 × 399` @390)
  - `h1.u-mb-0` → **"Making the impossible things about kidcare possible"** — 80px/80px **w400**, ls −0.8px. `580 × 400` at `120,236`; `440.797 × 480` @1024; `351 × 240` at `19.5,176` @390.
  - `p.paragraph-1-5.u-mb-0` → **"We connect parents who need childcare with parents who can care for their kids."** — 24px/36px **w400**, `text-align:left`. `580 × 72` at `120,660`; `351 × 81` (18px/27px) at `19.5,432` @390.
  - `a.btn.w-button[href="#jobs"]` → **"Join our team"** — dark pill, `149.297 × 46` at `120,756` (identical width at all three widths). **Same-page anchor to `#jobs`** — no smooth-scroll JS is attached; it is a plain native jump.
- `div.col.u-mb-0.col-lg-5.col-sm-12` → `div.header-shapes-contain` — same CSS as `/faq` §3.3, different fills:
  1. `.shape-contain.cc-sitters-top` → `.shape.stone-hero_middle-left.u-bg-coral` → `.u-aspect-1x1` → `img.u-img-cover`
     Clip `url(#stone-hero_middle-left)`, backing colour **`--coral` `#fbad9c`** (first live use of `--coral`). Image `Playing_Colored_01 1.webp`, `alt="Kid playing with sitter"`.
     Measured `428.984²` at `891,253` @1440; `324.578²` at `648.2,380.6` @1024; `280.797²` at `19.5,597.5` @390.
  2. `.shape-contain.cc-sitters-bottom` → `.shape.stone-hero_top-left.u-bg-olive.rotate-90`
     Flat `#94954c`, clip `url(#stone-hero_top-left)`, **`transform: rotate(90deg)`** → computed `matrix(0, 1, -1, 0, 0, 0)`. No image.
     Measured `238.328²` at `1081.7,586.7` @1440; `180.328²` at `792.5,633.1` @1024; `175.5²` at `202,664.1` @390.

**3 — "Kidcare that fills the gap"** → `div.container.cc-narrow` → `div.row`

- `div.col.col-lg-6.col-sm-12` → `div.u-aspect-9x16` → `img.u-img-cover` = `Illo Sitter + Parents.webp`, `alt=""`.
  Measured box `580 × 324.797` at `120,1002` (bg `#f8f6f5`, radius 32px); `440.797 × 246.844` @1024; `351 × 196.547` at `19.5,1212` @390 (radius 16px).
- `div.col.col-lg-6.col-sm-first.col-sm-12` → `div.section-header`
  - `h2.h3.u-mb-0` → **"Kidcare that fills the gap"** — 56px/56px w600. `580 × 112` at `740,1002`.
  - `p.paragraph-1-5` → **"If we succeed in closing the childcare gap, every child will have access to trustworthy kidcare and every parent will be economically empowered like never before."**

  `.col-sm-first { order:-1 }` at ≤767 → **the copy moves above the image on mobile** (measured @390: h2 at y 974.3, image at y 1212).

**4 — "The kidcare gap"** → `div.container.cc-narrow.u-mb-1` (`margin-bottom:16px`)

- `h2.h3.u-text-center.u-mb-2` → **"The kidcare gap"** — 56px/56px w600, centered, `margin-bottom:112px` (2em). `1200 × 56` at `120,1526.8`; `351 × 28.8`, `mb 57.6px` @390.
- `div.row.row-justify-center` with 8 cols: a `col.col-lg-1.u-mb-0.col-md-hide` spacer, 3 stat cols, another spacer, then 3 more stat cols.
  Spacers: `flex:1 1 8.33%; max-width:8.3333%`, measured `103.328 × 219.781` at x=151.7 and x=1185 @1440; `80.125` wide @1024; **`display:none` at ≤991** via `.col-md-hide` (measured rect `0,0,0,0` @390).
  Stat cols `col.col-lg-3.col-md-4.col-sm-6` → `flex:1 1 25%` → measured `.stat-contain` **270 × 155.781** at x 275 / 585 / 895 (row 1, y 1694.8) and the same x at y 1914.6 (row 2). @1024 `200.391` wide at x 171.4 / 411.8 / 652.2. @390 **two per row**, `155.5` wide at x 19.5 / 215.

```css
.stat-contain { display:flex; flex-direction:column; gap:.75em }  /* 12px */
```

Each `.stat-contain`: `h3.eyebrow` (14px/19.6px w600 uppercase ls .49px, `mb 4.2px`) + `div.h4.u-mb-0` (40px/44px w600; 20px/24px @390) + `p` (16px/24px w500, `mb 16px`).

Six stats, DOM order — eyebrow / figure / body:

1. `Affordability` / **50%** / "Of American families can't afford childcare"
2. `access` / **50%** / "Of families live in a childcare desert, where there are 3 kids for every seat"
3. `Impact` / **2 million** / "Women left the workforce during the pandemic"
4. `stay-at-home parents` / **12 million** / "Parents don't work outside the home"
5. `Poverty` / **25%** / "Of stay-at-home parents and their families live in poverty"
6. `Daycare` / **4 million** / "Childcare seats have been lost since March 2020"

(Eyebrows are authored in mixed case and rendered uppercase by `text-transform`.)

**5 — values** → `h2.u-sr-only` → **"Values"**, then `div.container` (**full `.container`, not `cc-narrow`**) → `div.row.row-justify-center` → 2 × `div.col.col-lg-5.col-md-12` → `div.values-wrap`

```css
.values-wrap { background-color:var(--white); border-radius:4.5em; /*72px*/
  display:flex; flex-direction:column; justify-content:center; align-items:center;
  height:100%; padding:4.5em 3.5em }                                /* 72px 56px */
@media(max-width:479px){ .values-wrap { border-radius:2.5em; padding:3em 1.5em } }  /* 40px; 48px 24px */
.values_item { display:flex; flex-direction:row; justify-content:space-between;
  align-items:center; width:100%; padding-block:1em }               /* 16px */
.icon-wrap-72 { width:72px; height:72px; overflow:hidden }
@media(max-width:479px){ .icon-wrap-72 { width:56px; height:56px } }
```

Measured `.values-wrap`: `516.656 × 624` at `183.3,2286.4` and `740,2286.4` @1440 (padding 72/56, radius 72px); `360.656 × 740` @1024; `351 × 424` at `19.5,2390.3` and `19.5,2854.3` @390 (padding 48/24, radius 40px).
`.values_item`: `404.656 × 104` @1440 (104px pitch), `248.656 × 104` @1024, `303 × 88` @390.
`.icon-wrap-72` → `div.u-aspect-1x1` → `img.u-img-cover`; rendered 72 × 72 (56 × 56 @390).

Card 1 — `h3.h4.u-mb-2.u-text-center` → **"Our values"**, then three `.values_item` (label + icon):
`Care first` · `Always build trust` · `Be rigorous`
Card 2 — **"Our operating principles"**:
`Always do the right thing` · `Win some, learn some` · `Build for diversity`

**6 — Benefits** → `div.container.cc-narrow`

- `div.row.row-justify-center.u-mb-1` → `div.col.col-lg-5.col-md-8.col-sm-12` → `div.section-header.cc-centered`
  - `div.eyebrow` → **"Taking Care of Our Team"**
  - `h2.h3.u-mb-0` → **"Benefits"**
  - `p.u-mb-0.paragraph-1-25` → **"In addition to competitive salaries and equity ownership in the company, we offer:"**
  Measured header `476.656 × 183.594` at `481.7,3110.4`, gap 24px, `align-items:center`, `text-align:center`. Note the `p` inside still computes `text-align:left` (the `.paragraph-1-25.u-mb-0` rule wins) while the eyebrow and h2 are centered — reproduce that asymmetry.
- `div.row` → 6 × `div.col.col-lg-4.col-md-6.col-sm-12` → `div.trust-card`

```css
.trust-card { background-color:var(--primary); color:var(--white); border-radius:2em; /*32px*/
  display:flex; flex-direction:column; justify-content:space-between;
  height:100%; min-height:30em; padding:3em }                    /* 480px; 48px */
@media(max-width:991px){ .trust-card { gap:2em; min-height:auto; padding:2em } }
.benefits-icons { max-width:5.5rem; margin-bottom:3rem }         /* 88px; 48px */
@media(max-width:767px){ .benefits-icons { max-width:4rem } }     /* 64px */
@media(max-width:479px){ .benefits-icons { width:50% } }
.trust-card_header { z-index:3; display:flex; flex-direction:column;
  align-items:flex-start; gap:1.5em; max-width:80%; position:relative }
@media(max-width:991px){ .trust-card_header { gap:1em } }
@media(max-width:767px){ .trust-card_header { max-width:86% } }
@media(max-width:479px){ .trust-card_header { max-width:100% } }
.trust-bar_header { margin-bottom:0; font-size:2em }              /* 32px */
@media(max-width:767px){ .trust-bar_header { font-size:1.5em } }
@media(max-width:479px){ .trust-bar_header { font-size:1.25em } } /* 20px */
```

Measured @1440: cards `373.328 × 480` in a 3×2 grid at x 120 / 533.3 / 946.7, y 3350 and 3870. `padding:48px`, radius 32px, bg `#00373e`, colour `#ffffff`. `.benefits-icons` 88 × 88 with `margin-bottom:48px`. `.trust-card_header` `221.859` wide (80%), gap 24px.
@1024: `280.516` wide, height **591.953** (content-driven, `min-height:480px` still applies), still 3-up (1024 > 991 → `col-lg-4`).
@390: `351` wide, 1-up, `padding:32px`, `gap:32px`, heights 320 / 296 / 344 / 344 / 344 / 368. `.benefits-icons` 64 × 64 (`max-width:4rem` at ≤767 wins over the ≤479 `width:50%`). `.trust-card_header` `287` wide (100%), gap 16px.

Each card: `div.benefits-icons > div.u-aspect-1x1 > img.u-img-cover`, then `div.trust-card_header` with `h3.trust-bar_header` + `p.u-mb-0`.

Six benefits, DOM order — title / body:

1. **Healthcare** / "We offer free medical, vision, and dental benefits for you and your dependents."
2. **401(k) plan** / "We offer a 401(k) plan so you can plan for your future, starting now."
3. **7 years to exercise your options** / "We offer a 7-year exercise window to exercise options for people who stay with Otter for two years or more."
4. **Flexible time off** / "We want you to recharge as you need and take time for the things you love — and we'll insist you take the time."
5. **Parental leave** / "We offer 16 weeks of paid parental leave and flexible schedules as you come back to work so you can spend time with your growing family."
6. **Dependent care FSA** / "You can set aside up to $5,000/yr pre-tax to put towards care for any of your dependents — and we will contribute up to $2,500 of that amount."

**7 — compensation philosophy** → `div.container.cc-narrow.u-mb-1`

- `div.row.row-justify-center.u-mb-1` → `div.col.col-lg-7.col-md-12` → `div.section-header.cc-centered`
  - `div.eyebrow` → **"internal equity"**
  - `h2.h3.u-mb-0` → **"Our compensation philosophy"**
  - `p.u-mb-0.paragraph-1-25` → **"We articulated our compensation philosophy when we were still a team of two; our way of taking care of the team before they walked in the door."**
  Measured `683.328 × 213.594` at `378.3,5259.5`… (header 2 of 3; see `.cc-centered` rect list: y 3110.4 / 4550 / 5259.5 @1440).
- `div.row.row-justify-center` → 3 × `div.col` (`col-lg-4 col-sm-10 col-xs-12`, `col-lg-4 col-sm-12 col-xs-12`, `col-lg-4 col-md-12 col-xs-12`) → `div.stat-contain.u-text-center`
  - `h3.h4.u-mb-0` + `p`. Measured `373.328 × 144/168/120` at x 120 / 533.3 / 946.7, y 4875.5 @1440. Note `.stat-contain.u-text-center` sets `text-align:center` on the wrapper but the `h3.h4.u-mb-0` inside still computes **`text-align:left`** (`.h4.u-mb-0 { text-align:left }` wins) while the `p` is centered. Reproduce verbatim.

1. **Cohesive** / "Otter's compensation strategy fits together as a whole, with each individual piece making sense in light of the overall strategy."
2. **Consistent** / "Like individuals should be treated alike. There should be no differentiation based on irrelevant factors, like a better understanding of equity compensation."
3. **Coherent** / "Otter's compensation strategy should be clear and easily understood by team members."

(Apostrophes in 1 and 3 are curly U+2019.)

**8 — `section#jobs`** → `div.container.cc-narrow.u-mb-1`

- `div.row.row-justify-center.u-mb-1` → `div.col.col-lg-7.col-md-12` → `div.section-header.cc-centered`
  - `div.eyebrow` → **"join the team"**
  - `h2.h3.u-mb-0` → **"Current Positions"**
  - `p.u-mb-0.paragraph-1-25` → **"To build childcare that feels like family for families everywhere, we need a team with all kinds of different perspectives, experiences and backgrounds."**
- `div.row` → **two empty `div.col.u-mb-0.col-lg-12`** — harmless leftovers; each contributes 0 height. Safe to drop.
- `div.w-dyn-list` → `div[role=list].row.w-dyn-items` → 3 × `div[role=listitem].col.u-mb-0.col-lg-12.w-dyn-item` → the job row (§5.2).

### 5.2 Job listing rows — `.faq-item.cc-listing`

**There is no department grouping, no ATS iframe, and no empty state** on the live page: three roles are published, rendered as a flat Webflow collection list, each linking out to Greenhouse in a new tab. (The design system's empty-state would be Webflow's `.w-dyn-empty` grey box, as seen on `/faq`.)

The row reuses the FAQ accordion's `.faq-item` markup as an `<a>`, with `.cc-listing` overriding it into a pill:

```css
.faq-item.cc-listing {
  border-radius: 8em;                       /* 128px */
  align-items: center;
  padding-left: 4em; padding-right: 4em;    /* 64px */
  font-weight: 500;
  transition: color .3s cubic-bezier(.165,.84,.44,1),
              background-color .3s cubic-bezier(.165,.84,.44,1);
}
.faq-item.cc-listing:hover { background-color: var(--primary); color: var(--white) }
@media(max-width:479px){ .faq-item.cc-listing { border-radius:1.5em; /*24px*/
                                                padding-left:2em; padding-right:2em } }
.faq-icon-wrapper.cc-listing { margin-top:0; margin-right:0; position:relative }
```

Inherited from base `.faq-item`: `background:var(--white)`, `cursor:pointer`, `display:flex`, `flex-direction:row`, `justify-content:space-between`, `width:100%`, `margin-bottom:1.5em` (24px), `padding-block:1.5em` (24px), `position:relative`, and the focus ring.

Measured box model:

| | @1440 | @1024 | @390 |
|---|---|---|---|
| `.faq-item.cc-listing` | `1200 × 119.984`, pad `24px 64px`, radius **128px**, `mb 24px` | `921.594 × 119.984`, pad `24px 64px`, radius 128px | `351 × 112.781`, pad `24px 32px`, radius **24px** |
| row x / y | x 120; y 5529.1 / 5673.1 / 5817.1 (144px pitch) | x 51.2; y 6113.1 / 6257.1 / 6401 | x 19.5; y 7072.3 / 7209.1 / 7367.5 |
| `.faq-content` (`width:75%`) | `804 × 71.984` at x 184 | `595.188 × 71.984` at x 115.2 | `246.812 × 64.781` at x 51.5 (**86%** at ≤767) |
| `.faq-spacer` (`padding-block:.6em`) | `804 × 47.984`, pad `9.6px 0` | `595.188 × 47.984` | `246.812 × 40.781` |
| `h3.paragraph-1-5.u-mb-0` | `24px / 28.8px`, w400 | same | `18px / 21.6px` |
| `p.u-mb-0` | `16px / 24px`, w400, at y +48 from row top | same | same |
| `.faq-icon-wrapper.cc-listing` | **40 × 40**, bg `#f8f6f5`, radius 99px, `position:relative`, at x 1216 | x 868.8 | x 298.5 |
| `.faq-icon` | **16 × 16** (`min-width/min-height:1em`), `overflow:hidden`, at x 1228 | x 880.8 | x 310.5 |

Row markup:

```html
<div role="listitem" class="col u-mb-0 col-lg-12 w-dyn-item">
  <a href="https://boards.greenhouse.io/withotter/jobs/4243384004" target="_blank"
     class="faq-item cc-listing w-inline-block">
    <div class="faq-content">
      <div class="faq-spacer"><h3 class="paragraph-1-5 u-mb-0">General Interest</h3></div>
      <p class="u-mb-0">San Francisco</p>
    </div>
    <div aria-label="accordeon open" role="button" class="faq-icon-wrapper cc-listing">
      <div class="faq-icon">
        <img src="…682e5411afe4660a9707f026_up-right.svg" loading="lazy" alt="" class="u-img-cover"/>
      </div>
    </div>
  </a>
</div>
```

The three published roles, DOM order:

| Title | Location | href (`target="_blank"`) |
|---|---|---|
| **General Interest** | San Francisco | `https://boards.greenhouse.io/withotter/jobs/4243384004` |
| **Market Operations - Chicago** | Chicago, IL | `https://boards.greenhouse.io/withotter/jobs/4894785004` |
| **Market Operations - SF Bay Area** | San Francisco Bay Area | `https://boards.greenhouse.io/withotter/jobs/4807382004` |

The icon is a 16×16 up-right arrow SVG (`viewBox="0 0 16 16"`, single path, `fill="#00373E"`):

```
M3.4878 14.396L10.1598 7.724C11.0238 6.836 11.6238 6.02 11.8878 5.468L11.7438 12.62H14.4078V1.604H3.3678V4.268L10.5198 4.124C9.9918 4.364 9.1518 4.94 8.2638 5.828L1.5918 12.5L3.4878 14.396Z
```

**Accessibility bugs to decide on, carried over from the accordion it was copied from:** the icon wrapper still says `aria-label="accordeon open"` and `role="button"` (misspelled, and wrong — it is a decorative icon inside a link, and a nested `role="button"` inside an `<a>` is invalid). Recommend dropping both attributes and leaving `alt=""`; record here that they exist on the original.

**Row states, measured live:**

| State | Measured |
|---|---|
| default | bg `#ffffff`, colour `#00373e`, radius 128px, no border, no shadow, `cursor:pointer` |
| **hover** | bg **`#00373e`**, colour **`#ffffff`** — transitioned `.3s cubic-bezier(.165,.84,.44,1)` on `color` and `background-color` only. Confirmed `h3` and `p` both go `#ffffff` by inheritance. **`.faq-icon-wrapper` background stays `#f8f6f5`** (ivory pill on the dark row) — it is not in the transition and has no hover rule. |
| focus-visible | `outline: 3px dashed #00373e; outline-offset: 0` (from `.faq-item:focus-visible`) — note this is **3px dashed**, different from the global `.btn` 2px dashed + 2px offset |
| active | no rule — no transform |

---

## 6. Motion

### 6.1 What actually animates — exhaustively verified

On each of the three routes, **exactly one element carries a `data-w-id`**:

```
e9e5205a-cbfa-d6b9-11fc-6e90b3191d6d  ::  a.nav_mobile-btn.w-inline-block
```

Of the 37 IX2 events in the site-wide data, I resolved every event's target against the live DOM on each route. **Exactly two resolve: `e-13` and `e-14`.** Everything else (including the homepage's `e-31` `slideInBottom` scroll reveal on `.section-header.cc-tabas-header`, and the 15 accordion click-pairs) targets elements that do not exist on these routes.

**Consequences — do not build these:**
- **No scroll reveals, no entrance animations, no stagger on any of the three routes.** Every section renders statically; no element ships with an inline `style="opacity:0"`.
- No `.swiper` elements → Swiper is loaded but inert. Do not ship it.
- No marquees, no `<video>`, no `<canvas>`, no `IntersectionObserver` in site code.
- `@keyframes slideInFromBottom` + `.tab-content.cc-card { animation: slideInFromBottom .5s ease }` exist in the global embed but `.tab-content` appears on none of these routes.

### 6.2 Mobile nav — `e-13` → `a-5` ("mobile-nav-open") / `e-14` → `a-6` ("mobile-nav-close")

Trigger: `MOUSE_CLICK` / `MOUSE_SECOND_CLICK` on `a.nav_mobile-btn`. Media queries **`medium`, `small`, `tiny` only** (≤991px). Easing for every item: **`outQuart` = `cubic-bezier(0.165, 0.84, 0.44, 1)`**.

**`a-5` open** — `useFirstGroupAsInitialState: true`

Group 1 (initial state, applied instantly): `.cc-top` translateY 0 / rotateZ 0 (300); `.cc-bottom` translateY 0 / rotateZ 0 (300); `.cc-middle` opacity 1 (300); `.nav_menu-card` opacity 0 + translateY 60px (400); `.nav_menu-overlay` opacity 0 (300).

Group 2 (duration 0): `.nav_menu` → `display:block`; `.nav_menu-overlay` → `display:block`.

Group 3:

| Target | Property | To | Delay | Duration |
|---|---|---|---|---|
| `.nav_mobile-btn-line.cc-top` | translateY | `6px` | 0 | 300 |
| `.nav_mobile-btn-line.cc-bottom` | translateY | `-6px` | 0 | 300 |
| `.nav_mobile-btn-line.cc-middle` | opacity | `0` | 0 | 300 |
| `.nav_menu-overlay` | opacity | `1` | 0 | 300 |
| `.nav_menu-card` | translateY | `0px` | **200** | 400 |
| `.nav_menu-card` | opacity | `1` | **200** | 400 |
| `.nav_mobile-btn-line.cc-top` | rotateZ | `45deg` | **200** | 300 |
| `.nav_mobile-btn-line.cc-bottom` | rotateZ | `-45deg` | **200** | 300 |

Total ≈ **600ms**. (Identical to the homepage's `a-10`.)

**`a-6` close** — `useFirstGroupAsInitialState: false`, single animated group:

| Target | Property | To | Delay | Duration |
|---|---|---|---|---|
| `.nav_mobile-btn-line.cc-bottom` | rotateZ | `0deg` | 0 | 300 |
| `.nav_mobile-btn-line.cc-top` | rotateZ | `0deg` | 0 | 300 |
| `.nav_mobile-btn-line.cc-bottom` | translateY | `0px` | **200** | 300 |
| `.nav_mobile-btn-line.cc-top` | translateY | `0px` | **200** | 300 |
| `.nav_mobile-btn-line.cc-middle` | opacity | `1` | **200** | 300 |
| `.nav_menu-card` | translateY | `60px` | **200** | **300** |
| `.nav_menu-card` | opacity | `0` | **200** | **300** |
| `.nav_menu-overlay` | opacity | `0` | **200** | 300 |

Then group 2 (duration 0): `.nav_menu` → `display:none`; `.nav_menu-overlay` → `display:none`. Total ≈ **500ms**.

> Difference from the homepage's `a-11`: the `.nav_menu-card` opacity/translateY on close run for **300ms** here vs 400ms on `/`. Everything else matches.

Measured open panel @390: `.nav_menu` `position:absolute; inset:72px 0 auto`, `z-index:99`; `.nav_menu-card` `background:#fbd3b6`, `border-radius:24px`, `padding:36px`, `flex-direction:column`, `gap:20px`, `justify-content:space-between`, `align-items:center`, `width:100%`. Inside it the content-links group becomes `flex-direction:column; align-items:flex-start; gap:16px; padding-bottom:2rem; border-bottom:1px solid var(--primary)`, with each `.nav_link` at `font-size:1.5em` (24px/36px) and `width:100%`; the buttons group stays `flex-direction:row; gap:20px` with no border.

Plus the same inline jQuery as the homepage — clicking the overlay re-clicks the button to close:

```js
$(function () { $(".nav_menu-overlay").click(function () { $(".nav_mobile-btn").click(); }); });
```

### 6.3 Accordion timings — `a-3` / `a-4` (defined, zero live targets)

Only needed if Build stubs FAQ content. Both lists animate `.faq-answer` height and rotate `.icon-line.cc-vr`.

**`a-3` "faq-open"** — `useFirstGroupAsInitialState: true`
- Group 1 (initial): `.faq-answer` `STYLE_SIZE` height, duration **500**, easing **linear/none** (`easing: ""`); `.icon-line.cc-vr` rotateZ `0deg`, duration 500, easing `""`.
- Group 2 (animate): `.faq-answer` `STYLE_SIZE` height, duration **600ms**, easing **`outQuart`**; `.icon-line.cc-vr` rotateZ **`90deg`**, duration **600ms**, easing `outQuart`. Both delay 0, simultaneous.

**`a-4` "faq-close"** — `useFirstGroupAsInitialState: false`, one group:
- `.faq-answer` `STYLE_SIZE` height, duration **200ms**, easing `outQuart`.
- `.icon-line.cc-vr` rotateZ `0deg`, duration **200ms**, easing `outQuart`.

So: **open 600ms, close 200ms, both `cubic-bezier(.165,.84,.44,1)`, no delay, no stagger.** Webflow's `STYLE_SIZE` animates `height` from 0 to the measured auto height on `.faq-answer` (`overflow:hidden`). The icon rotation and the height run together. Each item is independent — multiple panels open simultaneously.

CSS equivalent, if Build implements it without IX2:

```css
.faq-answer { overflow:hidden; height:0;
  transition: height 200ms cubic-bezier(.165,.84,.44,1) }
.faq-item.is-open .faq-answer { height:auto;             /* needs JS-measured px or grid-template-rows */
  transition: height 600ms cubic-bezier(.165,.84,.44,1) }
.icon-line.cc-vr { transition: transform 200ms cubic-bezier(.165,.84,.44,1) }
.faq-item.is-open .icon-line.cc-vr { transform: rotate(90deg);
  transition: transform 600ms cubic-bezier(.165,.84,.44,1) }
```

### 6.4 CSS transitions actually present on these routes

| Selector | Transition | Trigger / result |
|---|---|---|
| `.btn` (incl. `input[type=submit].btn`) | `color, background-color, border-color .3s cubic-bezier(.165,.84,.44,1)` | `:hover` → bg `--peach`, colour `--primary` |
| `.btn.cc-white` | same | `:hover` → `box-shadow: 0 1px #1b1e1f14, 0 1px 5px #1b1e1f0a` (**not** in the transition list → snaps); `:active` → `scale(.95)` instant |
| `.input`, `.input.cc-text-area` | `border-color .3s cubic-bezier(.165,.84,.44,1)` | `:focus-visible` → `border-width:2px` (**width is not transitioned → snaps**) |
| `.faq-item.cc-listing` | `color, background-color .3s cubic-bezier(.165,.84,.44,1)` | `:hover` → bg `--primary`, colour `--white` |
| `.nav_link-current-icon` | `opacity, transform .3s cubic-bezier(.165,.84,.44,1)` | `.nav_link:hover` (≥992px) → `opacity:1; translateY(0)` |

That is the complete set. No other rendered element on any of the three routes declares a transition.

---

## 7. Links to routes outside the 10 known ones

Scanned every `a[href]` on all three routes. **No same-origin route outside the known 10 is linked.** Off-site and non-route targets:

| Target | Where | Notes |
|---|---|---|
| `#` | `a.nav_skip-link`, `a.nav_mobile-btn` | On these routes the skip link's `href` is **`#`**, not `#main` as on the homepage — even though `<main id="main">` exists. Likely a Webflow authoring slip; it makes the skip link a no-op. Recommend `#main`; recorded as-is. |
| `#jobs` | `/careers` hero `a.btn` "Join our team" | same-page anchor to `section#jobs`, native jump |
| `https://app.withotter.com/log-in` | nav "Log in", `target="_blank"` | strip `?device-id=` |
| `https://app.withotter.com/sign-up/welcome` | nav "Sign up", `target="_blank"` | strip `?device-id=` |
| `https://app.withotter.com/sign-up` | footer "Get started", `target="_blank"` | strip `?device-id=` |
| `https://boards.greenhouse.io/withotter/jobs/4243384004` | `/careers` job row 1, `target="_blank"` | external ATS |
| `https://boards.greenhouse.io/withotter/jobs/4894785004` | `/careers` job row 2, `target="_blank"` | external ATS |
| `https://boards.greenhouse.io/withotter/jobs/4807382004` | `/careers` job row 3, `target="_blank"` | external ATS |
| `mailto:support@withotter.com` | `/contact` info block 1 | |
| `mailto:media@withotter.com` | `/contact` info block 1 | |
| `https://www.instagram.com/otterchildcare/` | footer col 3, `target="_blank"` | |
| `https://www.facebook.com/withotter/` | footer col 3, `target="_blank"` | |
| `https://twitter.com/WithOtter` | footer col 3, `target="_blank"` | |
| `https://www.linkedin.com/company/withotter` | footer col 3, `target="_blank"` | |

`device-id` is regenerated per session (three different values across my three loads). **Hardcode the bare `app.withotter.com` URLs with no query string.**

Third-party scripts present and **not to be ported** (same set as the homepage): jQuery 3.5.1, Webflow IX2, Swiper 9, WebFont loader, GTM/gtag, Facebook Pixel, Nextdoor Pixel, FullStory, Amplitude 8.17.0.

---

## 8. Open items / anything not measurable

- **`/faq` has no published FAQ content.** The accordion component, its box model and its IX2 timings are all specced from the shipped CSS and IX2 data (§3.4, §6.3), but **no live instance exists to measure**, so the rendered open/closed heights and the real answer copy are unknown. This is a content gap on the original, not a measurement failure.
- **`.nav_link.w--current`'s ≤991px peach-pill style** never applies on these three routes (no nav link matches these URLs). Specced from CSS; unmeasured in the live DOM.
- **`.form-success` / `.form-error`** were measured by unhiding them in the DOM. The form was **not** submitted, so Webflow's real success/failure sequencing (which block shows, whether the `<form>` is hidden) is inferred from Webflow's standard behaviour: on success `.w-form-done` replaces the form, on failure `.w-form-fail` appears below it.
- **The success block's icon never loads** on a normal visit (`loading="lazy"` inside `display:none`). Its URL is valid; see the asset file.
- Everything else on all three routes was read directly from the live DOM. Nothing was auth-gated, canvas-rendered, or otherwise unreachable.
