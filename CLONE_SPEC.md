Source: https://withotter.com/

# Otter — Clone Build Spec

Measured live with Playwright on 2026-10-08 at **1440×900**, **1024×900**, **390×844**.
Reference DOM: `/Users/riyaghosh/V3/otter/reference/original.html`
Reference compiled CSS: `/Users/riyaghosh/V3/otter/reference/assets/with-otter-ac17371ef8a503ba0b8fca450052.shared.34930fed5.min.css`
Asset manifest: `/Users/riyaghosh/V3/otter/ASSETS.md`

Platform: **Webflow** (Webflow IX2 for motion, jQuery 3.5.1, Swiper 9 loaded but unused on this route). **No GSAP. No video. No canvas.** Everything on the page is readable from the DOM — nothing was auth-gated or unmeasurable.

Document height at 1440 = 3771px, at 1024 = 3915px, at 390 = 4228px. Page is 1 route (`/`) + hero/banner/how-it-works/trust-bar/footer.

---

## 1. Fonts

All loaded fonts, confirmed from `document.fonts` + network tab.

### Self-hosted (Webflow CDN) — `format("woff")`, `font-display: swap`

| Family | Weight | Style | Loaded on page? | URL |
|---|---|---|---|---|
| Jokker | 400 | normal | **yes** | `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/682e5411afe4660a9707efe4_Jokker-Regular.woff` |
| Jokker | 400 | italic | declared, not used | `.../682e5411afe4660a9707efe3_Jokker-RegularItalic.woff` |
| Jokker | 500 | normal | **yes** | `.../682e5411afe4660a9707efe2_Jokker-Medium.woff` |
| Jokker | 500 | italic | declared, not used | `.../682e5411afe4660a9707efdd_Jokker-MediumItalic.woff` |
| Jokker | 600 | normal | **yes** | `.../682e5411afe4660a9707efe0_Jokker-Semibold.woff` |
| Reckless Neue | 900 | normal | **yes** | `.../682e5411afe4660a9707efde_RecklessNeue-Heavy.woff` |

(Prefix for all: `https://cdn.prod.website-files.com/682e5411afe4660a9707efce/`)

### Google Fonts

`<link href="https://fonts.googleapis.com/css?family=Inconsolata:400,700">`, injected via `WebFont.load({google:{families:["Inconsolata:400,700"]}})`.
Latin woff2 actually downloaded: `https://fonts.gstatic.com/s/inconsolata/v37/QlddNThLqRwH-OJ1UHjlKENVzkWGVkL3GZQmAwLyya15IDhunA.woff2`.
**Inconsolata is only used by the Webflow style-guide class `.styles__selector-callout`, which does not appear on this page. You can skip it entirely.**

### Stacks to use

```css
--font-body:    "Jokker", sans-serif;      /* body, all headings except h1 */
--font-display: "Reckless Neue", sans-serif; /* h1 / .h1 / .u-font-heading only */
```

`body { font-family: Jokker, sans-serif; font-size: 1rem; font-weight: 500; line-height: 1.5; color: var(--primary); -webkit-font-smoothing: antialiased; }`
`html { font-size: 16px }` (browser default — no root-size overrides anywhere, so 1rem === 16px at every breakpoint).

---

## 2. Color tokens

Declared as CSS custom properties on `:root` in the compiled stylesheet — copy verbatim:

```css
:root{
  --primary:   #00373e;  /* rgb(0,55,62)    deep teal — body text, hero bg, dark buttons */
  --white:     #ffffff;
  --celeste:   #cafff2;  /* rgb(202,255,242) mint — light button bg, tag bg, dark-btn text */
  --peach:     #fbd3b6;  /* rgb(251,211,182) trust bar, mobile nav card, button hover, footer-right shape */
  --ivory:     #f8f6f5;  /* rgb(248,246,245) page background */
  --olive:     #94954c;  /* rgb(148,149,76)  hero middle-left stone, footer-left shape */
  --coral:     #fbad9c;  /* rgb(251,173,156) declared; unused on this page */
  --sandstone: #ac9e88;  /* rgb(172,158,136) declared; unused on this page */
}
```

Additional literal colors measured:

| Token | Value | Where |
|---|---|---|
| Page bg | `#f8f6f5` (`--ivory`) | `.page-wrapper` |
| Body bg | `#ffffff` | `body` (covered by `.page-wrapper`) |
| Card surface | `#ffffff` | `.card`, `.home-card-2`, `.footer_card.cc-right` |
| Border, white button | `#d6cfc4` 1px solid | `.btn.cc-white` |
| White-button hover shadow | `0 1px rgba(27,30,31,.08), 0 1px 5px rgba(27,30,31,.04)` (`#1b1e1f14`, `#1b1e1f0a`) | `.btn.cc-white:hover` |
| White-button active shadow | `0 1px rgba(27,30,31,.08)` | `.btn.cc-white:active` |
| White-button focus ring | `outline: 3px solid rgba(13,80,88,.37)` (`#0d50585e`) | `.btn.cc-white:focus` |
| `.button-primary` focus ring | `outline: 3px solid #2e8acc` | |
| Mobile nav overlay | `rgba(253,249,249,0.9)` (`#fdf9f9e6`) | `.nav_menu-overlay` |
| Secondary-btn light hover | `box-shadow: inset 0 0 0 100px rgba(255,255,255,.15)` (`#ffffff26`) | unused on this page |
| Text selection | bg `#00373E`, color `#CAFFF2` | `::selection` |
| Input placeholder | `rgba(0,55,62,.37)` (`#00373e5e`) | no inputs on this page |
| Focus-visible outline (global) | `2px dashed var(--primary)`, offset 2px | `a:focus-visible`, `.btn:focus-visible` |

**There are no gradients anywhere on this page.** The only `background-image` uses are two flat SVGs (`bullet-organic.svg`, `join-bg.svg`) — see ASSETS.md.
**There are no `backdrop-filter` values anywhere** (verified: every element computes `backdrop-filter: none`).

---

## 3. Breakpoints & layout primitives

Webflow's 4 breakpoints. Tailwind config should use **max-width** queries to match exactly:

| Name | Query | Applies at test widths |
|---|---|---|
| main | — (default) | 1440, 1024 |
| medium | `@media (max-width: 991px)` | — |
| small | `@media (max-width: 767px)` | — |
| tiny | `@media (max-width: 479px)` | 390 |

> Note: 1024px still uses **desktop/main** styles (1024 > 991). The only difference vs 1440 is that the container is a percentage, so widths shrink.

### `.container`

```css
.container { width: 90%; max-width: 90rem /*1440px*/; margin-inline: auto; position: relative; }
@media(max-width:991px){ .container{ width:85% } }
@media(max-width:479px){ .container{ width:90% } }
```

Measured: **1440 → 1296px wide, 72px side margins.  1024 → 921.6px wide, 51.2px side margins.  390 → 351px wide, 19.5px side margins.**

Variants:
- `.container.cc-nav` → `display:flex`
- `.container.cc-narrow` → `display:flex; flex-direction:column; max-width:75rem (1200px)`. At 1440 → 1200px wide, 120px side margin. At 1024 → 921.6px. At 390 → 351px.
- `.container.cc-footer-container` → `display:flex; flex-wrap:wrap; justify-content:space-between; gap:2.5rem (40px)`
- `.container.cc-hero` → see Hero section.

### 12-column grid (`.row` / `.col`)

```css
.row { display:flex; flex-wrap:wrap; flex:0 auto; align-content:stretch; margin-left:-20px; margin-right:-20px; }
.col { flex:1; margin-bottom:40px; padding-left:20px; padding-right:20px; }
```
→ **Gutter = 40px total (20px padding each side); row overhangs its container by 20px each side.**

Column span classes (`col-lg-N` desktop, `col-md-N` ≤991, `col-sm-N` ≤767, `col-xs-N` ≤479): `flex-basis` + `max-width` = `N/12` as a percentage (e.g. `col-lg-7` → `58.33% / 58.3333%`, `col-lg-12` → `100%`).
At ≤479: **`.col { flex-basis:100%; max-width:100%; order:1; position:static }`** — everything stacks.

Row modifiers used on this page: `.row-justify-center` (`justify-content:center`), `.row-justify-between`, `.row-reverse` (`flex-direction:row-reverse; align-items:flex-end`; ≤991 → `column-reverse wrap, align-items:flex-end`; ≤767 → `column, align-items:flex-start`), `.row.gap-24` (`gap:24px`; ≤479 → `gap:16px`), `.row.how-it-works` (≤991 → `flex-direction:column`).

### Section vertical rhythm

```css
.section { padding-block: 5rem; position: relative; }       /* 80px — 1440 & 1024 */
@media(max-width:991px){ .section { padding-block: 4rem } }  /* 64px */
@media(max-width:479px){ .section { padding-block: 3rem } }  /* 48px */
.section.cc-footer { padding-bottom: 3rem }                  /* 48px */
```

Utility paddings used: `.u-pt-0{padding-top:0}`, `.u-pb-2{padding-bottom:2em}` (=32px at 1440/1024; at ≤479 the media-query `.section{padding-block:3rem}` wins the cascade → **48px**).

---

## 4. Type scale (computed px, per viewport)

Base element styles:

```css
h1 { font-family:"Reckless Neue"; font-weight:900; font-size:5rem; line-height:1; letter-spacing:-.01em; margin:0 0 .2em }
h2 { font-weight:600; font-size:4.5rem; line-height:1;   margin:0 0 .4em }
h3 { font-weight:600; font-size:3.5rem; line-height:1.2; margin:0 0 .3em }
h4 { font-weight:600; font-size:2.5rem; line-height:1.1; margin:0 0 .8em }
p  { margin-bottom: 1em }
a  { color:var(--primary); font-weight:500; text-decoration:none }
strong { font-weight:700 }
/* global link underline tuning */
a { text-underline-position:under; text-decoration-thickness:.1em; text-underline-offset:.05em }
```

Responsive base sizes:

| Element | ≥992 | ≤991 | ≤767 | ≤479 |
|---|---|---|---|---|
| `h1` / `.h1` | 80px (5rem) | 64px (4rem) | 57.6px (3.6rem), `line-height:1` | 48px (3rem) |
| `h2` / `.h2` | 72px (4.5rem) | 56px (3.5rem) | 48px (3rem) | 32px (2rem), `margin-bottom:.5em` |
| `h3` | 56px (3.5rem) | 44.8px (2.8rem) | 40px (2.5rem) | 28.8px (1.8rem) |
| `.h3` | 56px | 40px (2.5rem), `mb:.3em` | 40px (2.5rem) | 28.8px (1.8rem) |
| `h4` / `.h4` | 40px (2.5rem) | 32px (2rem) | 28.8px (1.8rem) lh 1.5 | 20px (1.25rem) lh 1.2 |
| `.h3-small` | 32px (2rem) | 32px | 32px | 24px (1.5rem) |
| `.paragraph-1-5` | 24px (1.5rem) | 24px | 18px (1.125rem) | 18px |
| `.paragraph-1-25` | 20px (1.25rem) | 20px | 16px (1rem) | 16px |
| `.eyebrow` | 14px (`.875em`) | 14px | 14px | 14px |
| `.btn` | 16px | 16px | 16px (`1rem`) | 16px |
| `.heading-long` | 72px (4.5rem) | 40px (2.5rem) | 48px (3rem) | 40px (2.5rem) — *not used on this page* |

**Measured per-role table (what the build must hit exactly):**

| Role | Selector / element | @1440 & @1024 | @390 | Colour |
|---|---|---|---|---|
| **Hero H1** | `h1` (no class) | `80px / 80px`, w900, ls `-0.8px`, Reckless Neue, `mb 16px` | `48px / 48px`, w900, ls `-0.48px`, `mb 9.6px` | `#ffffff` |
| **Hero lede** | `p.paragraph-1-5.u-text-center` | `24px / 36px`, w500, ls normal, `mb 24px`, `text-align:center` | `18px / 27px`, w500, `mb 18px` | `#ffffff` |
| **Banner H2** | `h2.h3-small` | `32px / 32px`, w600, `mb 12.8px`, `text-align:left` | `24px / 24px`, w600, `mb 12px` | `#00373e` |
| **Section H2** | `h2.h3.u-mb-0` | `56px / 56px`, w600, `mb 0` | `28.8px / 28.8px`, w600, `mb 0` | `#00373e` |
| **Card H3** | `h3.h3-small` | `32px / 38.4px`, w600, `mb 9.6px` | `24px / 28.8px`, w600, `mb 7.2px` | `#00373e` |
| **Big-card H3** | `h3.h3` | `56px / 67.2px`, w600, `mb 16.8px` | `28.8px / 34.56px`, w600, `mb 8.64px` | `#00373e` |
| **Footer H2** | `h2.h4.u-mb-0` | `40px / 44px`, w600, `mb 0`, `text-align:left` | `20px / 24px`, w600, `mb 0` | `#ffffff` |
| **Body copy** | `p.paragraph-1-25` | `20px / 30px`, **w400**, `mb 20px`, `text-align:left` | `16px / 24px`, w400, `mb 16px` | `#00373e` (`#ffffff` in footer-left) |
| **Body copy (flex variant)** | `p.paragraph-1-25.u-mb-0` | `20px / 30px`, **w500**, `mb 0`, `flex:1` | `16px / 24px`, w500 | `#00373e` |
| **Eyebrow (plain)** | `div.eyebrow` | `14px / 19.6px`, w600, ls `0.49px`, `text-transform:uppercase`, no bg/padding | same | `#00373e` |
| **Eyebrow (tag pill)** | `div.eyebrow.tag` | `14px / 19.6px`, w600, ls `0.49px`, uppercase, `padding 5.6px 11.2px 4.2px`, `border-radius 20px`, `bg #cafff2` | same | `#00373e` |
| **Trust-bar eyebrow** | `h2.eyebrow.u-mb-0.u-text-center` | `14px / 19.6px`, **w400** (`.u-mb-0` sets `font-weight:400` and wins), ls `0.49px`, uppercase, centered | same | `#00373e` |
| **Button (`.btn`)** | all `.btn` variants | `16px / 16px`, w600, ls normal, `padding 14px 20px` (`.875em 1.25em`) | same | varies |
| **`.button-primary`** | `a.button-primary` | `16px`, **`line-height: 0`**, w600, `padding 32px` (2rem), `max-height 64px` | same | `#cafff2` |
| **Nav link** | `a.nav_link.cc-log-in` | `16px / 24px`, w500, `padding 8px 0` | `24px / 36px` (`1.5em`), w500, `padding 0`, `width:auto` | `#00373e` |
| **Bullet number** | `div.text-block-2` | `24px / 24px` (`1.5rem`), w600, `text-align:center` | same | `#00373e` |
| **Footer terms link** | `a.footer_terms-link` | `16px / 24px`, w500 | same | `#00373e` |
| **Footer copyright** | `div.footer_terms-link` | `16px / 24px`, w500 | same | `#00373e` |

---

## 5. Radii, shadows, filters per component

| Component | border-radius | box-shadow | other |
|---|---|---|---|
| `.container.cc-hero` | `4.5em` → **72px** @1440/1024; ≤767 `2.5em` → **40px** | none | `isolation:isolate; overflow:hidden` |
| `.card` (banner) | **32px** | none | `overflow:hidden` |
| `.home-card-2` (how-it-works + big card) | `2em` → **32px** | none | `overflow:hidden` |
| `.footer_card` | `1.5em` → **24px** | none | `overflow:hidden` |
| `.trust-bar` | `2.5em` → **40px** | none | — |
| `.btn` (all) | `99em` → computed **1584px** (pill) | none normally | `border:1px solid transparent`; `.cc-white` → `border-color:#d6cfc4` |
| `.btn.cc-white:hover` | — | `0 1px #1b1e1f14, 0 1px 5px #1b1e1f0a` | — |
| `.btn.cc-white:active` | — | `0 1px #1b1e1f14` | `transform: scale(.95)` |
| `.button-primary` | **999px** | none | `:active{transform:scale(.95)}` |
| `.bullet-organic.bullet` | `99px` (irrelevant — shape comes from the SVG bg) | none | `64px × 64px`; `width:48px` @≤479 |
| `.nav_mobile-btn` | **50%** (circle) | none | `48px × 48px`, bg `--primary` |
| `.nav_menu-card` (mobile) | `24px` | none | bg `--peach`, padding 36px |
| `.eyebrow.tag` | **20px** | none | — |
| `.featured-logo-wrap` | — | none | `height:1.5em (24px)`; `1.7em` @≤767; `1.5em` @≤479 |

**`backdrop-filter: none` everywhere. No `filter`. No `mix-blend-mode` in use (`.btn.cc-white` declares `mix-blend-mode:normal`).**

### Organic "stone" shapes (SVG clip-paths)

Five hero stones + two footer shapes are plain `<div>`s clipped by inline `<clipPath clipPathUnits="objectBoundingBox">` paths. Ship the SVG defs once (hidden container `width:0;height:0;position:fixed;overflow:hidden`) and apply:

```css
.stone-hero_top-right   { width:100%; height:100%; clip-path:url(#stone-hero_top-right) }
.stone-hero_bottom-right{ width:100%; height:100%; clip-path:url(#stone-hero_bottom-right) }
.stone-hero_top-left    { width:100%; height:100%; clip-path:url(#stone-hero_top-left) }
.stone-hero_middle-left { width:100%; height:100%; clip-path:url(#stone-hero_middle-left) }
.stone-hero_bottom-left { width:100%; height:100%; clip-path:url(#stone-hero_bottom-left) }
.footer-shape-left      { width:100%; height:100%; clip-path:url(#footer-shape-left) }
.footer-shape-right     { width:100%; height:100%; clip-path:url(#footer-shape-right) }
```

Path data (all `clipPathUnits="objectBoundingBox"`), copy verbatim:

```
#stone-hero_top-right
M0.704,0.043 C0.64,0.017,0.448,-0.023,0.349,0.018 C0.245,0.062,0.117,0.317,0.072,0.418 C0.028,0.519,-0.027,0.818,0.016,0.897 C0.045,0.95,0.109,1,0.242,0.979 C0.411,0.898,0.976,0.458,0.999,0.381 C1,0.305,0.768,0.069,0.704,0.043

#stone-hero_bottom-right
M0.996,0.23 C1,0.296,0.946,0.473,0.861,0.648 C0.776,0.823,0.71,0.984,0.613,0.999 C0.519,1,0.337,0.862,0.218,0.735 C0.131,0.643,0.048,0.549,0.025,0.502 C-0.013,0.426,-0.006,0.312,0.038,0.257 C0.085,0.197,0.175,0.204,0.417,0.139 C0.602,0.089,0.668,-0.008,0.76,0 C0.837,0.007,0.975,0.164,0.996,0.23

#stone-hero_top-left
M0.941,0.199 C1,0.306,1,0.775,0.909,0.857 C0.81,0.939,0.354,1,0.239,0.986 C0.125,0.936,0,0.648,0,0.569 C0,0.463,0.082,0.068,0.197,0.017 C0.337,-0.044,0.823,0.069,0.941,0.199

#stone-hero_middle-left
M0.924,0.106 C0.986,0.152,1,0.253,1,0.324 C1,0.395,0.824,0.999,0.622,1 C0.415,1,0.162,0.843,0.042,0.663 C-0.018,0.573,-0.001,0.324,0.018,0.252 C0.037,0.18,0.157,0.03,0.24,0.005 C0.33,-0.022,0.863,0.061,0.924,0.106

#stone-hero_bottom-left
M0.517,0 C0.58,0.003,0.64,0.02,0.694,0.049 C0.747,0.079,0.791,0.12,0.821,0.169 C0.868,0.245,1,0.955,0.955,0.996 C0.842,1,0.7,0.869,0.453,0.806 C0.218,0.747,0.032,0.737,0.003,0.628 C-0.025,0.519,0.134,0.188,0.202,0.126 C0.285,0.05,0.398,0.005,0.517,0

#footer-shape-left
M0.955,0.125 C0.926,0.069,0.871,-0.001,0.794,0 C0.718,0.001,0.182,0.255,0.108,0.331 C0.041,0.4,-0.01,0.589,0.002,0.657 C0.014,0.725,0.101,0.929,0.195,0.964 C0.383,1,0.685,1,0.88,0.879 C1,0.758,0.985,0.18,0.955,0.125

#footer-shape-right
M0,0.676 C0,0.747,0.014,0.848,0.076,0.894 C0.129,0.933,0.533,1,0.701,1 C0.701,1,0.701,1,0.701,1 C0.728,1,0.748,0.998,0.76,0.995 C0.843,0.97,0.963,0.82,0.982,0.748 C0.991,0.714,1,0.639,1,0.561 C1,0.561,1,0.561,1,0.56 C1,0.474,0.99,0.384,0.958,0.337 C0.838,0.157,0.585,0,0.378,0 C0.176,0.001,0,0.605,0,0.676
```

Shape scaffolding:
```css
.shape-contain { flex:none; width:100%; overflow:hidden }   /* ≤767: overflow:visible */
.shape-ratio   { padding-top:100%; position:relative }       /* forces 1:1 */
.shape         { position:absolute; inset:0 }
.u-aspect-1x1  { width:100%; padding-top:100%; position:relative; overflow:hidden }
.u-img-cover   { object-fit:contain; width:100%; height:100%; position:absolute; inset:0 }
```
Note `.u-img-cover` is `object-fit: **contain**` despite the name.

---

## 6. Section-by-section structure (DOM order), with real copy

Root: `<div class="page-wrapper">` — `background:#f8f6f5; color:#00373e; overflow:hidden`.
Before it, two `div.styles__global-embed-code.w-embed` (`width:0;height:0;position:fixed;inset:0 auto auto 0`) holding the global `<style>` and the 7 `<svg>` clipPath defs. Keep them, hidden.

### 6.1 `<nav class="nav_wrapper">`

```css
.nav_wrapper { background:transparent; justify-content:space-between; margin-block:3rem; position:relative }
@media(max-width:991px){ .nav_wrapper{ margin-top:2rem } }
```
Measured: @1440/1024 `margin: 48px 0`, height **60px**, `top: 48px`. @390 `margin: 32px 0 48px`, height **48px**.

**Not sticky.** `position: relative`, scrolls away with the page. No background, no blur, no shrink — verified by scrolling to y=1200 and re-reading: `position:relative`, `background:rgba(0,0,0,0)`, `backdrop-filter:none`, height unchanged at 60px, rect y became −1152.

Children in order:
1. `a.nav_skip-link[href="#main"]` → "Skip to Main". `opacity:0; width:0; height:0; position:absolute; left:0; right:0; overflow:hidden`. On `:focus-visible`: `background:var(--primary); color:var(--celeste); opacity:1; width:30%; height:auto; margin-inline:auto; padding:8px; display:flex; transform:translateY(-100%)`.
2. `div.container.cc-nav` (`display:flex`) containing:
   - `div.nav_logo-wrapper` — `position:absolute; inset:0; width:100%; height:100%; display:flex; justify-content:center; align-items:center; pointer-events:none`. Holds `a.brand_logo[href="/"][aria-label="home"]` → inline Otter wordmark SVG (`viewBox="0 0 139 48"`, fill `#00373E`, `width:100%;height:100%`) + `div.u-sr-only` "Go to home page".
     `.brand_logo { z-index:999; width:8rem (128px); height:100%; margin-inline:auto; display:flex; align-items:center; justify-content:center; pointer-events:auto }`. @≤479 `width:7rem (112px)`. Measured @1440: `128 × 60` centred at x=656. @390: `112 × 48` at x=20 (left-aligned, because `.nav_logo-wrapper` becomes `width:auto;height:auto;position:relative` at ≤991).
   - `a.nav_mobile-btn[data-w-id="47e1fa15-…-a6c"]` — `display:none` on desktop. @≤991: `z-index:99; background:var(--primary); border-radius:50%; width:48px; height:48px; display:flex; position:relative`. Contains `div.nav_mobile-line-wrapper` (`position:absolute; inset:0; display:flex; flex-direction:column; justify-content:center; align-items:center`) with three `div.nav_mobile-btn-line` (`.cc-top`, `.cc-middle`, `.cc-bottom`): each `background:var(--white); width:24px; height:2px`; `.cc-middle { margin-block:4px }`. Plus `div.u-sr-only` "Menu". Measured @390: button at x=323,y=32, 48×48; top line at y=49, mid at y=55 (so 6px apart).
   - `div.nav_menu` → `z-index:99; width:100%`. @≤991: `display:none; position:absolute; inset:72px 0 auto` (shown by IX2).
     - `div.nav_menu-card[data-w-id="…-a74"]` → `display:flex; justify-content:space-between; align-items:center; width:100%; min-height:60px`. @≤991: `background:var(--peach); border-radius:24px; flex-direction:column; gap:20px; min-height:auto; padding:36px`.
       - `div.nav_links-parent.cc-buttons` → `display:flex; gap:1em (16px); flex-wrap:nowrap; align-items:center`. @≤991 `.cc-buttons` → `gap:1.5em (24px); flex-direction:row`. @≤479 → `gap:1.25em (20px)`.
         - `a.nav_link.cc-log-in` → **"Log in"**, `href="https://app.withotter.com/log-in?device-id=…"`, `target=_blank`. `padding-block:.5em; position:relative; overflow:hidden`.
         - `a.btn.cc-white.w-button` → **"Sign up"**, `href="https://app.withotter.com/sign-up/welcome?device-id=…"`, `target=_blank`. Measured 100.04 × 46.
3. `div.nav_menu-overlay[data-w-id="…-a93"]` — `z-index:98; background:rgba(253,249,249,.9); width:100%; height:100vh; display:none; position:fixed; inset:0`.

Desktop nav layout @1440: container flex, `Log in` at x=72 (left), `Sign up` at x=133.9 (46px tall), logo absolutely centred at x=656. `justify-content:space-between` on `.nav_menu-card` but with only one child group it sits left.

### 6.2 `<header class="section u-pt-0 u-pb-2">` — Hero

@1440: `padding: 0 0 32px`, rect `0,156,1440,832`. @1024: same, `0,156,1024,832`. @390: `padding: 0 0 48px`, rect `0,128,390,554.4`.

`div.container.cc-hero`:
```css
.container.cc-hero{ background:var(--primary); color:var(--white); border-radius:4.5em;
  display:flex; flex-direction:column; justify-content:center; align-items:stretch;
  height:60vh; min-height:800px; overflow:hidden; isolation:isolate }
@media(max-width:991px){ .container.cc-hero{ height:auto; min-height:60dvh } }
@media(max-width:767px){ .container.cc-hero{ border-radius:2.5em; padding:8em 4em } }
@media(max-width:479px){ .container.cc-hero{ padding:5em 2em } }
```
Measured @1440 `72,156,1296,800` r72. @1024 `51.2,156,921.6,800` r72. @390 `20,128,351,506.4` r40, `padding:80px 32px`.

Children:
1. `div.u-z-index-3` (`z-index:3; position:relative`) → `div.row.row-justify-center` → `div.col.u-mb-0.col-lg-7.col-sm-12`:
   - `div.hero_copy-wrapper` — `z-index:5; text-align:center; display:flex; flex-direction:column; justify-content:center; align-items:center; width:90%; margin-inline:auto; position:relative`. ≤991 `width:100%`; ≤767 `width:80%`; ≤479 `width:100%`. Measured @1440 `387.3,357,665.4,398`; @1024 `277.6,317,468.8,478`; @390 `52,221,287,319.6`.
     - `h1` → **"Build a care career that cares about you"**
     - `div.hero_p-container` (`max-width:80%`; ≤767 `90%`; ≤479 `100%`) → `p.paragraph-1-5.u-text-center` → **"We want to get you the job and the pay you deserve."** Measured @1440 `453.8,613,532.3,72`.
     - `a.btn.cc-light.w-button[href="https://app.withotter.com/sign-up?device-id=…"][target=_blank]` → **"Create a free profile"**. 201.08 × 46, bg `#cafff2`.
2. `div.hero-brackgorund-wrapper` (sic — keep the typo'd class name or rename, your call) — `position:absolute; inset:0; display:flex; flex-direction:row; justify-content:space-between`.
   - `div.hero_stones-col.cc-left` — `z-index:1; display:flex; flex-direction:column; justify-content:space-between; align-items:stretch; width:28%; height:100%; margin-right:0`. (`.hero_stones-col` base: `width:33%; margin-right:-10%; justify-content:center`.) ≤991: `.cc-left{width:35%}` base `{width:37%; justify-content:space-between}`; ≤479: base `{width:40%}`.
     Measured @1440: `72,156,362.875,800`. @390: `20,128,122.8,506.4`.
     1. `.shape-contain.cc-hero_top-left` → `z-index:3; width:110%; margin-top:-30%; margin-left:-30%`. @1440 = `399.16 × 399.16` at `-36.9,47.1`, margins `-108.86px`. Inside: `.shape.stone-hero_top-left.u-bg-peach` → `.u-aspect-1x1` → `img.u-img-cover` **hero1.webp**, alt `"a person holding a baby"`.
     2. `.shape-contain.cc-hero_middle-left` → `z-index:1; margin-top:-3%; margin-left:-30%`. @1440 `362.875²` at `-36.9,435.4`. ≤991 `margin-top:-23%`; ≤767 `margin:20% 0 45% -41%`; **≤479 `display:none`**. Inside: `.shape.stone-hero_middle-left.u-bg-olive` (flat `#94954c`, no image).
     3. `.shape-contain.cc-hero_bottom-left` → `z-index:2; margin-top:-40%; margin-left:39%`. @1440 `362.875²` at `213.5,653.1`. ≤991 `width:100%; margin-bottom:-22%; margin-left:-10%`; ≤767 adds `margin-right:-49%`. Inside: `.shape.stone-hero_bottom-left` → `.u-aspect-1x1` → `img.u-img-cover` **Playing_Colored_01 1.webp**, alt `"Kid playing with sitter"`.
   - `div.hero_stones-col` (right) — `width:33%; margin-right:-10%; justify-content:center`. @1440 `1069.9,156,427.68,800`.
     1. `.shape-contain.cc-hero_top-right` → `position:relative`. @1440 `427.68²` at `1069.9,172.2`. ≤767 `margin-left:27%`; ≤479 `margin-top:-8%`. Inside: `.shape.stone-hero_top-right.u-bg-celeste` (flat `#cafff2`).
     2. `.shape-contain.cc-hero_bottom-right` → `margin-top:-20.5%; position:relative`. @1440 `427.68²` at `1069.9,512.2`, margin-top `-87.67px`. ≤767 `margin-bottom:-10%; margin-right:-49%`. Inside: `.shape.stone-hero_bottom-right` → `.u-aspect-1x1` → `img.u-img-cover` **hero2.webp**, alt `"a child with their hands on their head"`.

### 6.3 `<header class="section hp-banner">` — "Now in Beta" banner

@1440 `padding:80px 0`, rect `0,988,1440,454.2`. @390 `padding:48px 0`, rect `0,682,390,635.4`.

`div.container.hp-banner` → `div.row.row-justify-center` → `div.col` → `div.card`:
- `.card { background:#fff; border-radius:32px; display:flex; flex-direction:column; flex:1; justify-content:flex-start; margin-bottom:0; padding:32px; position:relative; overflow:hidden }`; `@≤479 { padding-left:24px }` → measured @390 `padding:32px 32px 32px 24px`.
- Measured @1440 `72,1068,1296,254.2`; @1024 `51.2,1068,921.6,284.2`; @390 `20,730,351,499.4`.
- `div.row.gap-24` (`gap:24px`; `margin-inline:-20px`; @≤479 `gap:16px`):
  - `div.col.col-narrow.u-mb-0` (`flex:0 auto; align-self:center`) → `img.image-2` = **Playdate.svg**, `height="180"`, `alt=""`. Rendered 291.2 × 180 (intrinsic 254×157, scaled to the 180px height attr).
  - `div.col.u-mb-0.v-align-center.spacing-md` (`align-self:center; display:flex; flex-direction:column; flex:1; gap:16px`):
    - `div.stack` → `div.section-header` (`z-index:3; display:flex; flex-direction:column; flex:1; gap:1.5em (24px); align-items:flex-start; position:relative`; @≤991 `gap:1em (16px)`)
      - `div.eyebrow.tag` → **"Now in Beta"** (rendered uppercase: NOW IN BETA)
      - `h2.h3-small` → **"Become a founding caregiver"**
    - `p.paragraph-1-25.u-mb-0` → **"Join Otter now and Otter will be free for you forever, even if we introduce paid plans."**
    - `div.stack.stack-x` (`display:flex; gap:16px`) → `a.btn.cc-white.w-button[href="https://app.withotter.com/sign-up?device-id=…"][target=_blank]` → **"Create a free profile"** (+ a `<link rel="prefetch" href="https://app.withotter.com/sign-up">`, ignorable).
  - @390 the two cols stack: image col at y=762 (331.2×180), copy col at y=958 (335×239.4) with `order:1`.

### 6.4 `<main id="main">` → `<section class="section how-it-works">`

@1440 `padding:80px 0`, rect `0,1442.2,1440,1458.9`. @390 `padding:48px 0`, rect `0,1318,390,1875.2`.

`div.container.cc-narrow` (max-width 1200px, `display:flex; flex-direction:column`) contains two rows:

**Row A — `div.row.row-reverse`** (`flex-direction:row-reverse; align-items:flex-end`; @≤991 `column-reverse wrap, align-items:flex-end`; @≤767 `column, align-items:flex-start`). Measured @1440 `100,1522.2,1240,387.7`.
- `div.col` → `div.how-it-works-image-wrapper` (`display:block; position:static`; @≤479 `min-width:100%; min-height:64px`) → `img.image` = **Illo Sitter and Kid.webp**, alt `"A child handing a ball to a smiling caregiver"`.
  `.image { max-width:70%; margin-bottom:-56px }`; @≤991 `max-width:100%`; @≤767 `max-width:70%; margin-bottom:-40px; margin-left:-40px`; @≤479 `margin-left:-24px`.
  Measured @1440 `740,1522.2,406×403.7`; @1024 `532,1552.2,308.5×306.8`; @390 `-5,1366,245.7×244.3`.
- `div.col` → `div.section-header.cc-tabas-header[data-w-id="b1db74f4-c45f-40e9-fd53-68334a687f34"]` — **this is the only scroll-reveal element on the page**; it ships with inline `style="opacity:0"`.
  `.section-header.cc-tabas-header` @≤991 `{ align-items:flex-start; width:auto; display:flex }`; @≤767 `{ width:100% }`.
  - `div.eyebrow` → **"how it works"** (uppercase: HOW IT WORKS)
  - `h2.h3.u-mb-0` → **"A&nbsp;profile that feels like you, because it is"** (note the non-breaking space after "A")
  Measured @1440 `120,1714.3,580×155.6`, gap 24px.

**Row B — `div.row.how-it-works`** (@≤991 `flex-direction:column`). Measured @1440 `100,1909.9,1240,911.2`.
- 3 × `div.col` → `div.home-card-2.how-it-works-card`:
  ```css
  .home-card-2 { background:#fff; border-radius:2em(32px); display:flex; flex-wrap:wrap;
    place-content:flex-start; align-items:center; height:auto; min-height:25rem(400px);
    padding:2.5em(40px); position:relative; overflow:hidden; gap:0 }
  .home-card-2.how-it-works-card { gap:16px; height:100% }
  @media(max-width:991px){ .home-card-2{ flex-direction:column; justify-content:flex-start;
    align-items:flex-start; height:100%; min-height:auto; gap:0 } }
  ```
  Measured @1440 `120,1909.9,373.3×408`; @1024 `51.2,1843,280.5×498`; @390 `20,1743,351×332` (stacked, `min-height:auto`).
  - `div.bullet-organic.bullet` — `64×64`, `background-image:url(bullet-organic.svg)`, `background-position:0 0; background-size:auto; background-color:transparent; border-radius:99px; display:flex; align-items:center; justify-content:center`. @≤479 `width:48px`.
    - `div.text-block-2` → **"1"** / **"2"** / **"3"** — `24px/24px`, w600, centred.
  - `div.how-it-works-copy` (`display:flex; flex-direction:column; flex:0 auto; gap:0`):
    - `h3.h3-small` → **"Get started"** / **"Give us a call"** / **"Share your profile"**
    - `p.paragraph-1-25` →
      1. "We like to keep it simple. Tell us your name, contact information, and a little bit about your childcare experience and what you're looking for in your next role."
      2. "Meet Autumn, our AI assistant, who asks you all the right questions to understand your strengths and help you present your best self in just minutes!"
      3. "Showcase your best self everywhere you apply with your portable, customized profile, designed to help you shine."
- 1 × `div.col.col-lg-12` → `div.home-card-2.home-card-lg`:
  ```css
  .home-card-2.home-card-lg{
    background-image:url(join-bg.svg); background-position:100% 0; background-repeat:no-repeat;
    background-size:auto 100%; flex-direction:row; padding:4em(64px) }
  @media(max-width:991px){ background-position:160% }
  @media(max-width:767px){ background-position:190%; padding:2em(32px) }
  @media(max-width:479px){ background-position:200px }
  ```
  Measured @1440 `120,2357.9,1200×423.2`; @390 `20,2835,351×269.7` padding 32px.
  - `div.join-copy` (`order:1; max-width:50%`; @≤767 `max-width:75%`; @≤479 `max-width:none`):
    - `h3.h3` → **"We want to help you grow"**
    - `p.paragraph-1-25` → **"We want to help you build a sustainable, rewarding career."**
    - `a.button-primary.w-inline-block[href="https://app.withotter.com/sign-up?device-id=…"]` → **"Join Otter"**. Measured `143.33 × 64` at `184,2653.1`.

### 6.5 `<section class="section">` — "As featured in" trust bar

@1440 `padding:80px 0`, rect `0,2901.1,1440,296`.
`div.container` → `div.row.row-justify-between` → `div.col.col-lg-12.u-mb-0` → `div.trust-bar`:
```css
.trust-bar { background:var(--peach); border-radius:2.5em(40px); display:flex; flex-wrap:wrap;
  justify-content:space-around; align-items:center; gap:2em(32px); padding:3.5em 3vw }
@media(max-width:991px){ .trust-bar{ flex-direction:column; padding:2em(32px); gap:2em } }
@media(max-width:479px){ .trust-bar{ gap:3em(48px) } }
```
Measured padding @1440 `56px 43.2px`, @1024 `56px 30.72px`, @390 `32px` with `gap:48px` and `flex-direction:column`.
- `h2.eyebrow.u-mb-0.u-text-center` → **"As featured in"** (uppercase, w400). Measured width 109.82px @1440.
- `div.featured-logos` — `display:flex; flex-wrap:wrap; place-content:center space-between; align-items:center; width:70%; max-width:750px; gap:2.5em (40px)`. @≤991 `{ justify-content:center; width:100%; max-width:100%; gap:2em (32px) }`; @≤479 `{ flex-flow:column }`.
  Measured @1440 `495.4,3037.1,750×24`; @1024 `310.9,3060.2,602.1×24`; @390 column, 287×192.
  - 4 × `div.featured-logo-wrap` (`height:1.5em = 24px`) → `img.featured-logo` (`height:100%`). Intrinsic SVG sizes & rendered widths @24px tall:

    | alt | intrinsic | rendered @1440 |
    |---|---|---|
    | `Forbes magazine` | 120×32 | 90 × 24 |
    | `parents.com` | 188×32 | 141 × 24 |
    | `The New York Times` | 238×32 | 178.5 × 24 |
    | `mom.com` | 96×32 | 72 × 24 |

    DOM order: **Forbes, Parents, The New York Times, mom.com**.

### 6.6 `<footer class="section cc-footer">`

@1440 `padding:80px 0 48px`, rect `0,3197.1,1440,574`. @390 `padding:48px 0`, rect `0,3613,390,615.2`.

There is a stray empty `div.container` before the real one — harmless, drop it.

`div.container.cc-footer-container` (`display:flex; flex-wrap:wrap; justify-content:space-between; gap:40px`). Measured @1440 `72,3277.1,1296×446`; @1024 wraps to two full-width rows; @390 same.

- `div.footer_card.cc-left.u-bg-primary` — `border-radius:1.5em(24px); display:flex; flex-direction:column; flex:1; justify-content:space-between; padding:2.5em(40px); overflow:hidden; min-width:20rem(320px)`; bg `--primary`, color `#fff`. @≤991 `min-width:100%`; @≤479 `padding:1.5em(24px)`.
  Measured @1440 `72,3277.1,392.1×446`; @390 `20,3661,351×262`, padding 24px.
  - `div.section-header.cc-footer` (`max-width:50ch`; gap 24px):
    - `h2.h4.u-mb-0` → **"Build a care career that loves you back"** (`text-align:left`)
    - `p.paragraph-1-25` → **"Level up your care career: gain access to the best care jobs, maximize your earnings, and unlock your potential."**
    - `a.btn.w-button[href="https://app.withotter.com/sign-up?device-id=…"][target=_blank]` → **"Get started"**. 130.98 × 46, bg `--primary`, text `--celeste`.
  - `div.shape-contain.cc-footer-left` → `width:76%; max-width:400px; margin-bottom:-20%; margin-left:-15%; position:absolute; inset:auto auto 0 0`. @≤991 `width:40%; margin-bottom:-7%; margin-left:-5%`. Measured @1440 `13.2,3503.5,298×298`. Inside: `.shape.footer-shape-left.u-bg-olive` (`#94954c`).
- `div.footer_card.cc-right.u-bg-white` — same base, `flex:1 0 auto; min-width:66.66%`, bg `#fff`. @≤991 `min-width:auto`; @≤479 `max-width:100%`.
  Measured @1440 `504.1,3277.1,863.9×446`; @390 `20,3963,351×217.2`.
  - `div.footer_row` (`z-index:3; display:flex; justify-content:space-between; align-items:flex-start; position:relative`; @≤767 `flex-direction:column; gap:2rem(32px)`):
    - `div.footer_links-container` — **empty** on this page (`flex-wrap:wrap; width:80%`). Renders as a 0-height spacer.
    - `div.brand_logo.cc-footer[aria-label="home"]` — not a link here, just a div. `height:auto; margin-inline:0`. @≤767 `order:-1`. Contains the same Otter wordmark SVG + `div.u-sr-only` "Go to home page". Measured @1440 `1200,3317.1,128×50.7`; @390 `44,3987,112×45.2` (order −1 → logo above the terms row).
  - `div.footer_row.cc-bottom` (@≤991 `flex-wrap:wrap`; @≤767 `gap:.75rem(12px); margin-top:2rem(32px)`):
    - `div.footer_terms-links-wrapper` (`display:flex; gap:1rem(16px); align-items:center`):
      - `a.footer_terms-link[href="/terms-of-use"]` → **"Terms of Use"**
      - `div.bullet` → `&nbsp;●` — `background:var(--primary); border-radius:99px; font-size:.4rem (6.4px); line-height:1`
      - `a.footer_terms-link[href="/privacy-policy"]` → **"Privacy Policy"**
    - `div.footer_terms-link` → **"© 2025 With Otter Inc."** (year rendered into `span.copyright-year`)
  - `div.shape-contain.cc-footer-right` → `width:36.47%; margin-top:-20%; margin-right:-7.6%; position:absolute; inset:0 0 auto auto`. @≤991 `margin-top:-17%`; @≤767 `width:40%; margin-top:-19%; margin-left:-8%; margin-right:0; inset:0 auto auto 0`; @≤479 `width:73%; margin-top:-27%; margin-left:-14%`. Measured @1440 `1118.6,3104.3,315.1×315.1`. Inside: `.shape.footer-shape-right.u-bg-peach` (`#fbd3b6`).

---

## 7. Motion

**Engine: Webflow IX2.** No GSAP, no IntersectionObserver in site code, no scroll listeners other than IX2's own. Only **three** IX2 events have live targets on this page (verified by matching every event target against the DOM).

### 7.1 Scroll reveal — the only entrance animation

| | |
|---|---|
| Event | `e-31`, `SCROLL_INTO_VIEW`, preset `SLIDE_EFFECT` |
| Target | `div.section-header.cc-tabas-header` (the "HOW IT WORKS / A profile that feels like you, because it is" block) |
| Media queries | all (`main`, `medium`, `small`, `tiny`) |
| Trigger offset | **`scrollOffsetValue: 20, scrollOffsetUnit: "%"`** — i.e. fires when the element is 20% of the viewport height inside the viewport |
| Direction | `BOTTOM`, `effectIn: true` |
| Event delay | `0` |
| Loop | `false`, `playInReverse: false` |
| Auto-stop | `e-32` (the reverse-out pair; not present as a separate live event) |

Action list `slideInBottom` (3 groups, `useFirstGroupAsInitialState: true`):
1. Initial: `opacity: 0`, duration 0, delay 0
2. Initial: `transform: translate(0px, 100px)`, duration 0, delay 0
3. Animate (both simultaneous): `transform: translate(0,0)` and `opacity: 1`, **`duration: 1000ms`, `delay: 0`, easing `outQuart`**

**`outQuart` = `cubic-bezier(0.165, 0.84, 0.44, 1)`.**

So in CSS/React terms:
```css
.reveal        { opacity:0; transform:translateY(100px) }
.reveal.is-in  { opacity:1; transform:none;
                 transition: opacity 1000ms cubic-bezier(.165,.84,.44,1),
                             transform 1000ms cubic-bezier(.165,.84,.44,1) }
```
Fire `is-in` via an IntersectionObserver with `rootMargin: "0px 0px -20% 0px"` (20% viewport offset), `threshold: 0`, once.

**There is no stagger anywhere, and no other element on this page animates on scroll or on load.** The hero, banner, cards, trust bar and footer are all statically rendered.

### 7.2 Mobile nav open — `e-41` → action list `a-10` ("mobile-nav-open 2")

Trigger: `MOUSE_CLICK` on `a.nav_mobile-btn`. Media queries: `medium`, `small`, `tiny` only (≤991px). Easing for every item: **`outQuart` = `cubic-bezier(0.165,0.84,0.44,1)`**.

**Group 1 — initial state** (`useFirstGroupAsInitialState: true`, applied instantly):
| target | property | value | dur |
|---|---|---|---|
| `.nav_mobile-btn-line.cc-top` | translateY | `0px` | 300 |
| `.nav_mobile-btn-line.cc-top` | rotateZ | `0deg` | 300 |
| `.nav_mobile-btn-line.cc-bottom` | rotateZ | `0deg` | 300 |
| `.nav_mobile-btn-line.cc-bottom` | translateY | `0px` | 300 |
| `.nav_mobile-btn-line.cc-middle` | opacity | `1` | 300 |
| `.nav_menu-card` | opacity | `0` | 400 |
| `.nav_menu-card` | translateY | `60px` | 400 |
| `.nav_menu-overlay` | opacity | `0` | 300 |

**Group 2 — instant display flips** (duration 0): `.nav_menu → display:block`, `.nav_menu-overlay → display:block`

**Group 3 — the animation:**
| target | property | to | delay | duration |
|---|---|---|---|---|
| `.nav_mobile-btn-line.cc-top` | translateY | `6px` | 0 | 300 |
| `.nav_mobile-btn-line.cc-bottom` | translateY | `-6px` | 0 | 300 |
| `.nav_mobile-btn-line.cc-middle` | opacity | `0` | 0 | 300 |
| `.nav_menu-overlay` | opacity | `1` | 0 | 300 |
| `.nav_menu-card` | translateY | `0px` | **200** | 400 |
| `.nav_menu-card` | opacity | `1` | **200** | 400 |
| `.nav_mobile-btn-line.cc-top` | rotateZ | `45deg` | **200** | 300 |
| `.nav_mobile-btn-line.cc-bottom` | rotateZ | `-45deg` | **200** | 300 |

Total open duration ≈ 600ms. Verified post-click @390: top line `matrix(0.707107, 0.707107, -0.707107, 0.707107, 0, 6)` (translateY 6 + rotate 45°), bottom `matrix(0.707107, -0.707107, 0.707107, 0.707107, 0, -6)`, middle `opacity:0`, overlay `opacity:1` covering `0,0,390,844`, `.nav_menu` at `20,104,351×118` (`position:absolute; inset:72px 0 auto`), `.nav_menu-card` peach, 36px padding, radius 24px, `opacity:1`, `transform:none`.

### 7.3 Mobile nav close — `e-42` → action list `a-11` ("mobile-nav-close 2")

Trigger: `MOUSE_SECOND_CLICK` on the same button. Easing `outQuart` throughout. `useFirstGroupAsInitialState: false`.

**Group 1:**
| target | property | to | delay | duration |
|---|---|---|---|---|
| `.nav_mobile-btn-line.cc-bottom` | rotateZ | `0deg` | 0 | 300 |
| `.nav_mobile-btn-line.cc-top` | rotateZ | `0deg` | 0 | 300 |
| `.nav_mobile-btn-line.cc-bottom` | translateY | `0px` | **200** | 300 |
| `.nav_mobile-btn-line.cc-top` | translateY | `0px` | **200** | 300 |
| `.nav_mobile-btn-line.cc-middle` | opacity | `1` | **200** | 300 |
| `.nav_menu-card` | translateY | `60px` | **200** | 300 |
| `.nav_menu-card` | opacity | `0` | **200** | 300 |
| `.nav_menu-overlay` | opacity | `0` | **200** | 300 |

**Group 2** (duration 0): `.nav_menu → display:none`, `.nav_menu-overlay → display:none`

Total close duration ≈ 500ms.

Plus inline jQuery: clicking `.nav_menu-overlay` programmatically clicks `.nav_mobile-btn` (closes the menu).
```js
$(function () { $(".nav_menu-overlay").click(function () { $(".nav_mobile-btn").click(); }); });
```

### 7.4 Hover / interaction transitions (CSS)

Only **one** transition shorthand exists on any rendered element on this page:

```css
.btn {
  transition: color .3s cubic-bezier(.165,.84,.44,1),
              background-color .3s cubic-bezier(.165,.84,.44,1),
              border-color .3s cubic-bezier(.165,.84,.44,1);
}
```

Hover/active/focus states:

| Selector | State | Change |
|---|---|---|
| `.btn` | `:hover` | `background-color: var(--peach)`, `color: var(--primary)` |
| `.btn.cc-light` | `:hover` | `background-color: var(--peach)` |
| `.btn.cc-white` | `:hover` | `background:#fff` (unchanged), `border-color:#d6cfc4`, `box-shadow: 0 1px #1b1e1f14, 0 1px 5px #1b1e1f0a` — **note box-shadow is NOT in the transition list, so it snaps** |
| `.btn.cc-white` | `:active` | `transform: scale(.95)`, `box-shadow: 0 1px #1b1e1f14` — **no transition, instant** |
| `.btn.cc-white` | `:focus` | `outline: 3px solid #0d50585e; outline-offset: 0` |
| `.btn` | `:focus-visible` | `outline: 2px dashed var(--primary); outline-offset:2px` |
| `.button-primary` | `:hover` | `color:#00373e; background-color:#fbd3b6` — **no transition declared → instant** |
| `.button-primary` | `:active` | `transform: scale(.95)` — instant |
| `.button-primary` | `:focus` | `outline: 3px solid #2e8acc; outline-offset:0` |
| `a` | `:hover` | `text-decoration: none` (no visual change) |
| `a` | `:focus-visible` | `outline: 2px dashed var(--primary); outline-offset:2px` |

`.nav_link:hover .nav_link-current-icon { opacity:1; transform:translateY(0) }` exists at ≥992px but `.nav_link-current-icon` is **not present in this page's DOM** — no nav hover effect to build.

### 7.5 Carousels / marquees / video — none

- `swiper-bundle.min.js` (jsDelivr, Swiper 9) **is loaded** and `window.Swiper` is a function, but **`document.querySelectorAll('.swiper').length === 0`** on this route. The inline init runs against nothing. Config, for reference if a future route needs it:
  ```js
  const swiper = new Swiper(".swiper", {
    navigation: { nextEl: ".swiper-button-next", prevEl: ".swiper-button-prev" },
    speed: 400,
    spaceBetween: "4%",
    slidesPerView: 1.25,
    breakpoints: { 480: { slidesPerView: 2 }, 768: { slidesPerView: 2.1 }, /* …truncated in page source dump… */ }
  });
  ```
  **Do not ship Swiper for the homepage.**
- No marquees.
- `document.querySelectorAll('video').length === 0`. No autoplaying media of any kind.
- One unused keyframe exists in the global embed (for tab cards, not on this page):
  `@keyframes slideInFromBottom { 0%{transform:translateY(20%)} 100%{transform:translateY(0)} }` applied as `.tab-content.cc-card { animation: slideInFromBottom .5s ease }`.

---

## 8. Nav behaviour summary

- **Desktop (≥992px):** static, non-sticky, `position:relative`, transparent, `margin: 48px 0`, 60px tall. Logo absolutely centred (128px wide); "Log in" + "Sign up" pill at left. `.nav_mobile-btn` is `display:none`. Scrolls out of view with the page — **no sticky, no shrink, no blur, no background change** (verified by remeasuring at scrollY=1200).
- **≤991px:** `.nav_wrapper { margin-top: 2rem }`. Logo becomes `position:relative` left-aligned (112px @≤479). `.nav_mobile-btn` appears: 48×48 circle, `background:#00373e`, `border-radius:50%`, `z-index:99`, three 24×2 white bars with 4px gaps. `.nav_menu` becomes `display:none; position:absolute; inset:72px 0 auto` and is revealed by IX2 (§7.2). The open panel `.nav_menu-card` is a peach (`#fbd3b6`) card, `border-radius:24px`, `padding:36px`, `flex-direction:column`, `gap:20px`, holding "Log in" (24px/36px) and the white "Sign up" pill side by side (`.nav_links-parent.cc-buttons` stays `flex-direction:row`, `gap:24px`; `gap:20px` @≤479). Full-screen overlay `rgba(253,249,249,.9)`, `z-index:98`, `position:fixed`, click-to-close.

---

## 9. Other routes linked from the homepage (not specced)

| Href | Notes |
|---|---|
| `/` | this page (logo link) |
| `/terms-of-use` | same-origin page |
| `/privacy-policy` | same-origin page |
| `https://app.withotter.com/log-in?device-id=…` | external app, `target="_blank"` |
| `https://app.withotter.com/sign-up?device-id=…` | external app; used by hero CTA, banner CTA, "Join Otter", footer "Get started" |
| `https://app.withotter.com/sign-up/welcome?device-id=…` | external app, nav "Sign up", `target="_blank"` |
| `#main` | skip link |
| `#` | mobile menu toggle href |

The `device-id` query value is generated per-session by the app's JS; it differs between loads (saved HTML has `l-fIkPsttEwdnFxOn5qhmi`, live load had `0HDGi4CKnruMrpk6gzd-Pj`). **Hardcode the bare URL without `device-id` in the clone.**

---

## 10. Third-party scripts on the original (do NOT port)

jQuery 3.5.1, Webflow IX2 chunks, Swiper 9, WebFont loader, Google Tag Manager/gtag (`G-MQF6KJPCXL`, `G-2NVK8NS1G0`, `AW-10801161001`), Facebook Pixel (`2667541703549888`), Nextdoor Pixel, FullStory (`o-1DCR26-na1`), Amplitude 8.17.0.
