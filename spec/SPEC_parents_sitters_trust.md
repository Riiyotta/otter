Source: https://withotter.com/ (routes specced here: /parents, /sitters, /trust-safety)

# Otter — Build Spec: `/parents`, `/sitters`, `/trust-safety`

Measured live 2026-10-08 with a dedicated Playwright (Chromium 1.63) instance at **1440×900**, **1024×900**, **390×844**, deviceScaleFactor 1.
Companion asset manifest: `/Users/riyaghosh/V3/otter/spec/ASSETS_parents_sitters_trust.md`
Baseline (read first): `/Users/riyaghosh/V3/otter/CLONE_SPEC.md` — the shared design system. **This document only records what is NEW or DIFFERENT.**

Document heights measured:

| Route | @1440 | @1024 | @390 |
|---|---|---|---|
| `/parents` | 3621 | 4049 | 3877 |
| `/sitters` | 3733 | 4155 | 3962 |
| `/trust-safety` | 3558 | 3867 | 4310 |

---

## 0. Baseline confirmation / corrections

Verified against the same compiled stylesheet the homepage spec used (`with-otter-ac17371ef8a503ba0b8fca450052.shared.34930fed5.min.css`). All three routes load the identical CSS and JS bundles.

**Holds exactly as specced — do not re-derive:**

- `:root` tokens. Verbatim from the stylesheet: `:root{--primary:#00373e;--white:white;--celeste:#cafff2;--peach:#fbd3b6;--ivory:#f8f6f5;--olive:#94954c;--coral:#fbad9c;--sandstone:#ac9e88}`
  - **Correction to §2 of the homepage spec:** `--white` is the keyword `white`, not `#ffffff`. Computes identically; only matters if you diff the token block.
  - `--coral`, `--sandstone` were "declared, unused" on the homepage. **Both are now in use** (see §4).
- Fonts: identical set, identical `format("woff")` URLs. Only `RecklessNeue-Heavy.woff` (900) is self-hosted for the display face — relevant to the `/sitters` h1 quirk in §5.
- `.container` (90% / max 90rem; 85% ≤991; 90% ≤479), `.container.cc-narrow` (75rem), the 12-col `.row`/`.col` grid, `.section` padding-block 5rem / 4rem ≤991 / 3rem ≤479 — all identical. Measured container widths again: 1440 → 1296 (72px margins), 1024 → 921.6 (51.2px), 390 → 351 (19.5px). `.cc-narrow`: 1440 → 1200 (120px margins), 1024 → 921.6, 390 → 351.
- Breakpoints 991 / 767 / 479; **1024 still renders desktop/main styles** — reconfirmed (hero h1 is still 80px at 1024).
- Engine is **Webflow IX2, no GSAP**. Nav is **not sticky** (`position:relative`, transparent, `margin-block:3rem`, 60px tall at 1440).
- **No gradients. No `backdrop-filter`.** Re-verified on all three routes.
- Clip-path shapes: all three pages ship **the same 7 `<clipPath>` defs** as the homepage (`stone-hero_top-right`, `stone-hero_bottom-right`, `stone-hero_top-left`, `stone-hero_middle-left`, `stone-hero_bottom-left`, `footer-shape-left`, `footer-shape-right`), plus the two `clip0_254_628` rect clips belonging to the logo SVG. **There are zero new `d` strings** — reuse §5 of the homepage spec verbatim. These pages only recombine the existing shapes with new fills (§4.2).

**Differences from the homepage at the shell level:**

1. **The nav has a real link list.** On the homepage `.nav_links-parent` (non-buttons) and `.footer_links-container` were empty. On all three routes they are populated — see §3.
2. **The footer link lists are populated** — see §3.3. Footer copy, CTA card and shapes are otherwise byte-identical to the homepage.
3. `.section-header.cc-tabas-header` exists on `/parents` and `/sitters` but **carries no `data-w-id` and no inline `opacity:0`** → the homepage's one scroll-reveal (`e-31`) **does not run on these pages**. See §6.
4. There is a **site-wide inline `<style>` embed** (identical on all 3 routes) carrying desktop-only rules, the tab-icon rule and the swiper slide colour loop. The homepage spec captured only its `slideInFromBottom` keyframe. Full text in §6.5 — you need it.

---

## 1. Section map in DOM order

### `/parents`

| # | Element | @1440 y/height | @390 y/height | Padding |
|---|---|---|---|---|
| 1 | `nav.nav_wrapper` | 48 / 60 | 32 / 48 | `margin:48px 0` (`32px 0 48px` @390) |
| 2 | `header.section` — hero | 156 / 732 | 128 / 727 | `80px 0` / `48px 0` |
| 3 | `main#main > section.section` — how-it-works + tabs | 888 / 692 | 855 / 954 | `80px 0` / `48px 0` |
| 4 | `section.section.u-p-0.u-mb-3` — CTA card | 1580 / 480 | 1809 / 422 | `padding:0; margin-bottom:48px` |
| 5 | `section.section` — testimonials slider | 2108 / 640 | 2279 / 447 | `80px 0` / `48px 0` |
| 6 | `section.section` — "Common questions" | 2747 / 300 | 2726 / 209 | `80px 0` / `48px 0` |
| 7 | `footer.section.cc-footer` | 3047 / 574 | 2935 / 942 | `80px 0 48px` / `48px 0` |

### `/sitters`

| # | Element | @1440 y/height | @390 y/height | Padding |
|---|---|---|---|---|
| 1 | `nav.nav_wrapper` | 48 / 60 | 32 / 48 | as above |
| 2 | `header.section` — hero | 156 / 732 | 128 / 741 | `80px 0` / `48px 0` |
| 3 | `section.section` — how-it-works + tabs | 888 / 728 | 869 / 1029 | `80px 0` / `48px 0` |
| 4 | `section.section` — CTA card (**wide variant**) | 1616 / 640 | 1898 / 465 | `80px 0` / `48px 0` |
| 5 | `section.section` — testimonials slider | 2256 / 604 | 2364 / 447 | `80px 0` / `48px 0` |
| 6 | `section.section` — "Common questions" | 2859 / 300 | 2811 / 209 | `80px 0` / `48px 0` |
| 7 | `footer.section.cc-footer` | 3159 / 574 | 3020 / 942 | `80px 0 48px` / `48px 0` |

> Note the CTA differs structurally between the two: `/parents` wraps it in `section.section.u-p-0.u-mb-3` (zero padding, 48px bottom margin) while `/sitters` uses a plain `section.section` and puts `.cc-wide-cta` on the inner container.

### `/trust-safety`

| # | Element | @1440 y/height | @390 y/height | Padding |
|---|---|---|---|---|
| 1 | `nav.nav_wrapper` | 48 / 60 | 32 / 48 | as above |
| 2 | `header.section` — hero (two CTAs) | 156 / 732 | 128 / 792 | `80px 0` / `48px 0` |
| 3 | `main#main > section.section` — **one** section: video block + 4 trust cards | 888 / 2096 | 920 / 2448 | `80px 0` / `48px 0` |
| 4 | `footer.section.cc-footer` | 2984 / 574 | 3368 / 942 | `80px 0 48px` / `48px 0` |

`/trust-safety` has **no tabs, no CTA card, no testimonials slider and no "Common questions" section** (0 `.swiper` elements, 0 `.w-dyn-empty`).

---

## 2. New component: the hero (`header.section`) — all 3 routes

Same skeleton on all three; only the copy, CTA count and shape fills differ. This is a **light** hero on the ivory page background — nothing like the homepage's dark rounded `.container.cc-hero`.

```
header.section
  div.container.cc-narrow
    div.row.row-justify-between.row-align-center      /* /parents, /sitters */
    div.row.row-align-center.row-justify-between      /* /trust-safety — same classes, different source order */
      div.col.<spans>
        div.section-header
          h1
          p.paragraph-1-25.u-mb-0   (/parents, /sitters)
          p.paragraph-1-5           (/trust-safety)
          a.btn.w-button            (/parents, /sitters)
          div.buttons-wrapper       (/trust-safety — 2 buttons)
      div.col.u-mb-0.col-lg-5.col-sm-12
        div.header-shapes-contain
          div.shape-contain.cc-sitters-top
            div.shape-ratio
              div.shape.<stone>[.<fill>]
                div.u-aspect-1x1 > img.u-img-cover     /* only when the shape holds a photo */
          div.shape-contain.cc-sitters-bottom
            div.shape-ratio
              div.shape.<stone>.<fill>[.rotate-90]
```

Column spans per route:
- `/parents` copy col: `col.col-lg-6.col-md-6.col-sm-10.col-xs-12`
- `/sitters` copy col: `col.col-lg-6.col-sm-12`
- `/trust-safety` copy col: `col.col-lg-6.col-sm-10.col-xs-12`
- shapes col (all three): `col.u-mb-0.col-lg-5.col-sm-12`

### 2.1 New utility/layout classes

```css
.row.row-align-center { align-items: center }
.row.row-align-end    { align-items: flex-end }
@media (max-width:991px){ .row.row-md-justify-start { justify-content: flex-start } }
@media (max-width:991px){ .col.col-md-hide { display: none } }

.header-shapes-contain { z-index:1; display:flex; flex-direction:column; align-items:flex-end }
@media (max-width:991px){ .header-shapes-contain{
  justify-content:center; align-items:flex-end; width:50%;
  position:absolute; inset:0 0 0 auto } }
@media (max-width:767px){ .header-shapes-contain{
  gap:10%; flex-direction:row; justify-content:center; align-items:flex-end;
  width:100%; margin-top:-13%; position:relative } }
@media (max-width:479px){ .header-shapes-contain{
  justify-content:flex-start; width:100%; margin-top:-5%; margin-right:0 } }

.shape-contain.cc-sitters-top { width:90% }
@media (max-width:767px){ .shape-contain.cc-sitters-top{ width:80%; margin-right:-20% } }
@media (max-width:479px){ .shape-contain.cc-sitters-top{ width:80% } }

.shape-contain.cc-sitters-bottom { width:50%; margin-top:-20%; margin-left:auto }
@media (max-width:991px){ .shape-contain.cc-sitters-bottom{ margin-top:-40% } }
@media (max-width:767px){ .shape-contain.cc-sitters-bottom{ width:40%; margin-top:-33%; margin-left:-10% } }
@media (max-width:479px){ .shape-contain.cc-sitters-bottom{
  width:50%; margin-top:0; margin-bottom:11%; margin-left:-18% } }

.shape.rotate-90 { transform: rotate(90deg) }

.u-bg-coral     { background-color: var(--coral);     color: var(--primary) }
.u-bg-sandstone { background-color: var(--sandstone); color: var(--primary) }
.u-bg-celeste   { background-color: var(--celeste);   color: var(--primary) }
.u-bg-peach     { background-color: var(--peach);     color: var(--primary) }
.u-bg-olive     { background-color: var(--olive) }           /* note: no colour pairing */
.u-bg-ivory     { background-color: var(--ivory);     color: var(--primary) }

.buttons-wrapper { display:flex; flex-flow:wrap; align-items:center; gap:1em /*16px*/ }
@media (max-width:479px){ .buttons-wrapper{ flex-direction:column; align-items:stretch } }

.u-mb-2 { margin-bottom: 2em }
.u-mt-1 { margin-top: 1em }
.u-p-0  { padding: 0 }
.u-mb-3 { margin-bottom: 3em }
@media (max-width:991px){ .section.u-p-0 { padding-top:0; padding-bottom:0 } }
.container.cc-narrow.cc-cta-2 { width:85% }
@media (max-width:767px){ .container.cc-narrow.cc-cta-2 { width:100% } }
```

### 2.2 Measured hero geometry (identical across all 3 routes)

| Element | @1440 | @1024 | @390 |
|---|---|---|---|
| `header.section` | `0,156 1440×732` | `0,156 1024×750…764` | `0,128 390×727…792` |
| `.container.cc-narrow` | `120,236 1200×572` | `51,236 921.6×590…604` | `20,176 351×631…696` |
| `.row` | `100,236 1240×572` | `31,236 961.6×…` | `0,176 391×…` |
| `.section-header` | `120,… 580×440…454` | `51,236 440.8×550…564` | `20,176 351×328…393` |
| `h1` | `120,… 580×240` (3 lines) | `51,236 440.8×320` (4 lines) | `20,176 351×144` (3 lines) |
| `.header-shapes-contain` | `843,236 476.7×572` | `612,315…322 360.7×432.8` | `20,526…591 351×280.8` |
| `.shape-contain.cc-sitters-top` | `891,236 429×429` | `648,… 324.6×324.6` | `20,… 280.8×280.8` |
| `.shape-contain.cc-sitters-bottom` | `1082,570 238.3×238.3` | `792,… 180.3×180.3` | `202,… 175.5×175.5` |

`.section-header` is `display:flex; flex-direction:column; align-items:flex-start; flex:1; gap:24px; z-index:3; position:relative`. At 390 the gap drops to **16px**.

At ≤991 `.header-shapes-contain` becomes `position:absolute; inset:0 0 0 auto; width:50%` — so the shapes overlay the right half of the hero rather than sitting in a flex column. At ≤767 it returns to `position:relative`, goes `flex-direction:row`, full width, `margin-top:-13%`, so the two stones sit side-by-side **below** the copy (measured at 390: top stone at x=20, bottom stone at x=202).

### 2.3 Per-route hero content

**`/parents`**
- `h1` → "Quality kidcare, when you need it"
- `p.paragraph-1-25.u-mb-0` → "Otter's care options are designed to cater to both planned and unplanned schedule changes, with sitters available with as little as 2 hours notice." (measured `120,562 580×90` @1440)
- `a.btn.w-button[href="https://app.withotter.com/sign-up/welcome"][target=_blank]` → "Book kidcare" — **144.4×46**
- top shape: `div.shape.stone-hero_middle-left.u-bg-coral` holding `Parents.webp` (`alt="Sitter playing with baby"`; note the alt has a trailing newline in source)
- bottom shape: `div.shape.stone-hero_top-left.u-bg-olive.rotate-90` — flat olive, rotated 90°, no image

**`/sitters`**
- `h1.u-mb-0` → "Become a sitter, on your own time" — see the weight quirk in §5
- `p.paragraph-1-25.u-mb-0` → "Otter is the childcare solution created for the people who need it as much as the people who provide it. We connect sitters with families who are in a pinch and need backup care." (measured `120,539 580×120` @1440)
- `a.btn.w-button[...sign-up/welcome]` → "Join us" — **97.1×46**
- top shape: `div.shape.stone-hero_bottom-right` (no fill class) holding `Sitters.webp` (`alt="Kid playing with puzzle toys"`)
- bottom shape: `div.shape.stone-hero_middle-left.u-bg-peach` — flat peach

**`/trust-safety`**
- `h1` → "Complete kidcare peace of mind"
- `p.paragraph-1-5` → "Our top priority is safety – providing your little ones with a safe and trustworthy environment." (en-dash `–`; measured `120,559 580×72` @1440). **This role is `text-align:center` with `margin-bottom:24px`** even though it sits in a left-aligned hero — inherited from the shared `.paragraph-1-5` rules. Reproduce as measured.
- `div.buttons-wrapper` → two buttons, both `→ https://app.withotter.com/sign-up/welcome`, `target=_blank`:
  - `a.btn.w-button` → "Become a caregiver" — **198.0×46** at `120,679`
  - `a.btn.cc-light.w-button` → "Find childcare" — **152.5×46** at `334,679` (bg `--celeste`)
  - wrapper measured `120,679 366.5×46` @1440; at 390 it stacks: `20,461 198×108` with the second button at `20,523 198×46` (`align-items:stretch`, gap 16px)
- top shape: `div.shape.footer-shape-left` (no fill class) holding `FAQ.webp` (`alt="Kid playing with puzzle toy"`)
- bottom shape: `div.shape.stone-hero_top-left.u-bg-sandstone` — flat sandstone `#ac9e88` (first live use of this token)

---

## 3. New component: nav + footer link lists

### 3.1 Desktop nav (≥992px) — `/parents` shown, identical on all 3

`div.nav_menu-card` is `display:flex; justify-content:space-between; align-items:center; min-height:60px`, `1296×60` at `72,48`. It now has **two** children so `space-between` actually separates them:

```
div.nav_links-parent                  /* 72,58  297.5×40 */
  a.nav_link[href="/parents"]         /* + .w--current on the active route */
    div                               /* label */
    div.nav_link-current-icon
      div.current-icon > div.w-embed > svg
  a.nav_link[href="/sitters"]
  a.nav_link[href="/trust-safety"]
  a.nav_link[href="/blog"]
div.nav_links-parent.cc-buttons       /* 1206,55 161.9×46 */
  a.nav_link.cc-log-in → "Log in"   → https://app.withotter.com/log-in           target=_blank
  a.btn.cc-white.w-button → "Sign up" → https://app.withotter.com/sign-up/welcome target=_blank  (100.0×46)
```

Measured link rects @1440 (`.nav_links-parent` gap = 16px, each link `padding:8px 0`, 40px tall, `position:relative; overflow:hidden`):

| Label | href | rect @1440 |
|---|---|---|
| Parents | `/parents` | `72,58 59.4×40` |
| Sitters | `/sitters` | `147,58 49.9×40` |
| Trust & Safety | `/trust-safety` | `213,58 106.2×40` |
| Blog | `/blog` | `335,58 34.1×40` |

```css
.nav_links-parent { display:flex; flex-wrap:nowrap; align-items:center; gap:1em /*16px*/ }
.nav_link { padding-block:.5em; position:relative; overflow:hidden }
```

**The current/hover blob** (`.nav_link-current-icon`) — this is the nav effect the homepage spec listed as "not present in this page's DOM". It is live here.

```css
.nav_link-current-icon{
  position:absolute; inset:0; z-index:-1;
  display:flex; justify-content:center; align-items:center;
  width:100%; height:100%; margin-inline:auto;
  color:var(--celeste);            /* the SVG uses fill="currentColor" */
  mix-blend-mode:multiply;
  opacity:0; transform:translateY(100%);
  transition: opacity .3s cubic-bezier(.165,.84,.44,1),
              transform .3s cubic-bezier(.165,.84,.44,1);
}
.current-icon { width:2.5em /*40px*/; position:relative; top:3px }

/* from the page's inline <style>, desktop only: */
@media screen and (min-width:992px){
  .nav_link.w--current .nav_link-current-icon { opacity:1; transform:translateY(0) }
  .nav_link:hover        .nav_link-current-icon { opacity:1; transform:translateY(0) }
}
```

Verified by measurement: on `/parents` the `.w--current` link's blob reads `opacity:1`, `transform:matrix(1,0,0,1,0,0)`, `color:rgb(202,255,242)`, `mix-blend-mode:multiply`, `z-index:-1`, rect `72,58 59.4×40`; inner `.current-icon` rect `82,65 40×32.9`. Hovering "Sitters" transitions its blob to `opacity:1` / identity transform over **300ms `cubic-bezier(.165,.84,.44,1)`**.

The blob SVG (inline, `viewBox="0 0 34 22"`, `width/height 100%`, `fill="currentColor"`) — reproduce verbatim:

```
M0.54127 7.43938C-1.37846 10.4619 2.25598 18.3642 4.46461 19.6478C8.02481 21.6745 12.1971 22.4246 16.2626 21.769C20.5028 21.1227 33.3538 20.3852 33.9689 15.0138C34.4908 10.6803 28.3029 4.0891 26.2993 2.86916C24.0627 1.51267 15.6755 -0.553935 13.1127 0.137967C10.55 0.82987 2.29326 4.68998 0.54127 7.43938Z
```

### 3.2 Mobile nav (≤991px)

Adds to the homepage behaviour (§7.2/7.3 there, unchanged — same single `data-w-id="e9e5205a-cbfa-d6b9-11fc-6e90b3191d6d"` on `a.nav_mobile-btn`, same `a-10`/`a-11` action lists):

```css
@media (max-width:991px){
  .nav_links-parent {           /* the LINK group only */
    display:flex; flex-direction:column; align-items:flex-start;
    gap:16px; padding-bottom:2rem;
    border-bottom:1px solid var(--primary);
  }
  .nav_links-parent.cc-buttons {
    flex-direction:row; align-items:center; gap:1.5em /*24px*/;
    padding-bottom:0; border:1px #000;   /* i.e. border-style none → no border */
  }
  .nav_link { color:var(--primary); width:100%; padding-block:0; font-size:1.5em /*24px*/ }
  .nav_link.cc-log-in { width:auto }
  .nav_link.w--current { background-color:#fbad9cbd; border-radius:99px; padding:8px 16px }
  .nav_link-current-icon { color:var(--coral) }   /* but stays opacity:0 — the ≥992 reveal doesn't apply */
  .current-icon { width:1.5em /*24px*/ }
}
@media (max-width:479px){ .nav_links-parent, .nav_links-parent.cc-buttons { gap:1.25em /*20px*/ } }
```

Measured after clicking the burger at **390** (`/parents`):

| Element | rect | notes |
|---|---|---|
| `.nav_menu` | `20,104 351×391` | `display:block`, `position:absolute; inset:72px 0 auto` |
| `.nav_menu-card` | `20,104 351×391` | bg `#fbd3b6`, radius 24px, padding 36px, `flex-direction:column`, gap 20px, `opacity:1`, identity transform |
| `.nav_menu-overlay` | `0,0 390×844` | `rgba(253,249,249,.9)`, `opacity:1` |
| `.nav_links-parent` | `115,140 159.3×253` | column, gap 20px, `padding-bottom:32px`, 1px solid `--primary` bottom border |
| `.nav_links-parent.cc-buttons` | `101,413 188.9×46` | row, gap 20px |

Link rects @390 (all `font-size:24px / line-height:36px`):

| Label | rect | bg | padding | radius |
|---|---|---|---|---|
| Parents (`.w--current`) | `115,140 159.3×52` | `rgba(251,173,156,0.74)` | `8px 16px` | `99px` |
| Sitters | `115,212 159.3×36` | none | 0 | 0 |
| Trust & Safety | `115,268 159.3×36` | none | 0 | 0 |
| Blog | `115,324 159.3×36` | none | 0 | 0 |
| Log in | `101,418 68.8×36` | none | 0 | 0 |

The `.w--current` link's `.nav_link-current-icon` stays hidden at this width (`opacity:0`, `transform:matrix(1,0,0,1,0,52)`).

### 3.3 Footer link lists

`div.footer_links-container` (`display:flex; flex-wrap:wrap; width:80%`) now holds **three** `ul.footer_link-list.w-list-unstyled`. Measured @1440: container `544,3167 627.1×192`; each list `156.8×176` with `margin:0 0 16px`; each `li.footer_link` `156.8×24` with `margin-bottom:20px`.

```css
.footer_link-list { width:25%; padding-left:0 }
@media (max-width:991px){ .footer_link-list{ width:30% } }
@media (max-width:479px){ .footer_link-list{ width:50%; margin-bottom:1em } }
.footer_link { margin-bottom:1.25rem /*20px*/; font-size:1rem }
@media (max-width:767px){ .footer_link{ margin-bottom:.8rem /*12.8px*/; font-size:1rem } }
```

Anchors are bare `<a>` (no class) → inherit `a { color:var(--primary); font-weight:500; text-decoration:none }`; measured `16px/24px`, w500, rendered inline (19px box height). The anchor for the active route carries `.w--current` (no visual rule applies in the footer).

Column 1 — `/parents`, `/sitters`, `/trust-safety` → "Parents", "Sitters", "Trust & Safety"
Column 2 — `/faq`, `/careers`, `/blog`, `/contact` → "FAQ", "Careers", "Blog", "Contact"
Column 3 (all `target=_blank`) — "Instagram", "Facebook", "Twitter", "Linkedin"

Measured container width @1024 = `673.3`, @390 = `303.0×326.4` (wraps to 2 columns of 50%).

Everything else in the footer (the `.footer_card.cc-left` CTA card copy, `.cc-right`, `brand_logo.cc-footer`, `.footer_row.cc-bottom` terms + copyright, both corner shapes) is **identical to the homepage** — including the stray empty `div.container` before `.cc-footer-container`.

---

## 4. New component: tabs / accordion (`/parents`, `/sitters`)

This is the dual-mode disclosure pattern. **≥992px it is a tab strip driving an absolutely-positioned card in the next column. ≤991px it collapses into an accordion** driven purely by a CSS sibling selector. There is **no separate FAQ-style accordion anywhere on these pages** — no `accordion`/`faq`/`disclosure` class exists in the stylesheet at all.

### 4.1 Structure

```
div.row.row-justify-between
  div.col.col-lg-5.col-md-12
    div.section-header.cc-tabas-header     /* NO data-w-id — static, see §6 */
      div.eyebrow            → "how it works"
      h2.h3.u-mb-0
      p.u-mb-0.paragraph-1-5
    div.tabs-wrapper                        /* sibling of section-header */
      div.tab-item  ×3
        a.tab-trigger[.cc-active][href="#"]
          div.tab-trigger_icon
          div                               → label
        div.tab-content-mask                /* only rendered ≤991 */
          div.tab-content
            div.tab-content-image > img.u-img-cover
            p.u-mb-0.u-text-center
  div.col.col-lg-5.col-md-hide              /* hidden ≤991 */
    div.tab-content-wrapper
      div.tab-content.cc-card[.cc-active] ×3
        div.tab-content-image > img.u-img-cover
        p.u-mb-0.u-text-center
div.w-embed                                 /* the duplicate max-height rule, see §6.5 */
```

The copy is duplicated: the accordion bodies (inside `.tab-content-mask`) and the desktop cards (`.tab-content.cc-card`) hold the same three image+paragraph pairs with different `sizes` attributes.

### 4.2 Full box model

```css
.tabs-wrapper { display:flex; flex-direction:column; align-items:flex-start;
                gap:.5em /*8px*/; margin-top:1.5em /*24px*/ }
@media (max-width:991px){ .tabs-wrapper{ align-items:stretch } }

.tab-item { display:flex; flex-direction:column; align-items:flex-start }
@media (max-width:991px){ .tab-item{ background-color:var(--white);
                                     border-radius:32px; overflow:hidden } }

.tab-trigger { display:flex; justify-content:center; align-items:center;
  gap:.5em /*8px*/; padding:12px 20px; border-radius:99px; font-weight:600;
  transition: border-radius .3s cubic-bezier(.165,.84,.44,1) }
.tab-trigger.cc-active { background-color:var(--white) }
@media (max-width:991px){
  .tab-trigger { background-color:var(--white); justify-content:space-between;
                 width:100%; padding:16px 32px }
  .tab-trigger.cc-active { background-color:var(--white) }   /* same — no visual change */
}
@media (max-width:479px){
  .tab-trigger { padding-left:24px; padding-right:24px }
  .tab-trigger.cc-active { border-top-left-radius:20px; border-top-right-radius:20px }
}

.tab-trigger_icon { background-color:var(--coral); border-radius:99px;
                    width:.8em; height:.8em; display:none }
@media (max-width:991px){ .tab-trigger_icon{ order:1; display:flex } }
/* from the inline <style>: */
.tab-trigger.cc-active .tab-trigger_icon { display:block }

.tab-content-mask { max-height:0; overflow:hidden; transform-origin:50% 0; display:none;
                    transition: max-height .3s cubic-bezier(.165,.84,.44,1) }
@media (max-width:991px){ .tab-content-mask{ display:flex } }
/* from the inline <style> + the per-page .w-embed: */
.tab-trigger.cc-active + .tab-content-mask { max-height:800px; transition-delay:100ms }

.tab-content { display:none; flex-direction:column; justify-content:center;
  align-items:stretch; gap:1.5em /*24px*/; margin-top:1.5em; padding:1.5em;
  background-color:var(--ivory); border-radius:48px; overflow:hidden;
  transition: all .3s cubic-bezier(.165,.84,.44,1) }
@media (max-width:991px){ .tab-content{ display:flex; background-color:var(--white);
  border-radius:32px; margin-top:.5em /*8px*/; padding-top:0 } }
@media (max-width:479px){ .tab-content{ gap:1em /*16px*/; padding:1em;
  border-bottom-right-radius:20px; border-bottom-left-radius:20px } }

.tab-content.cc-card { position:absolute; inset:0; z-index:0; opacity:0;
  margin-top:0; transform:translateY(50%);
  transition: opacity .3s cubic-bezier(.165,.84,.44,1) }
.tab-content.cc-card.cc-active { position:relative; display:flex; opacity:1;
  transform:none; background-color:var(--white) }

.tab-content-wrapper { position:relative }

.tab-content-image { width:100%; padding-top:80%; position:relative;
                     border-radius:32px; overflow:hidden; isolation:isolate }
@media (max-width:991px){ .tab-content-image{ border-radius:24px } }
@media (max-width:479px){ .tab-content-image{ border-radius:12px; padding-top:100% } }
```

Inner `img.u-img-cover` is the shared `position:absolute; inset:0; width:100%; height:100%; object-fit:contain`.

### 4.3 Measured geometry

**Desktop tab strip** (`/parents` @1440; `/sitters` identical except y-offsets and card height 510.9):

| Element | rect |
|---|---|
| `.section-header.cc-tabas-header` | `120,968 476.7×307.6` (gap 24px) |
| `.tabs-wrapper` | `120,1300 476.7×160` (`margin-top:24px`, gap 8px) |
| `.tab-item` ×3 | `120,1300 118.8×48` / `…,1356` / `…,1412` → **56px pitch** (48 + 8 gap) |
| `.tab-trigger` | `118.8×48`, `padding:12px 20px`, radius 99px |
| `.tab-trigger_icon` | `140,1317 12.8×12.8`, bg `rgb(251,173,156)` |
| label `div` | `161,1312 58×24`, 16px/24px w600 |
| `.tab-content-wrapper` | `843,968 476.7×486.9` |
| `.tab-content.cc-card` | `476.7×486.9`, `padding:24px`, radius **48px**, bg `#fff`, gap 24px |
| `.tab-content-image` (active) | `867,992 428.7×342.9`, radius 32px |
| active card `p` | `867,1359 428.7×72`, 16px/24px **w400**, `text-align:center` |

Trigger widths are content-sized; measured `118.8` for the first item on both routes. Only `.cc-active` has a white pill background — inactive triggers are transparent (`rgba(0,0,0,0)`).

@1024: `.tabs-wrapper` at `51,1466 360.7×160`; `.tab-content-wrapper` `612,986 360.7×394.1`; active image `636,1010 312.7×250.1`.

**Mobile accordion** (`/parents` @390):

| Element | rect / value |
|---|---|
| `.tabs-wrapper` | `20,1090 351×631`, `align-items:stretch`, gap 8px |
| `.tab-item` (open) | `20,1090 351×503`, bg `#fff`, radius 32px, `overflow:hidden` |
| `.tab-trigger` | `351×56`, `padding:16px 24px`, `justify-content:space-between` |
| `.tab-trigger` radius — **active** | `20px 20px 99px 99px` |
| `.tab-trigger` radius — **inactive** | `99px` (full pill) |
| `.tab-trigger_icon` | `334,1112 12.8×12.8` (pushed right by `order:1`), bg `#fbad9c`; **only visible on the active item** |
| `.tab-content-mask` — active | `20,1146 351×447`, `max-height:800px`, `transition: max-height .3s cubic-bezier(.165,.84,.44,1) .1s` |
| `.tab-content-mask` — inactive | height `0`, `max-height:0`, `transition: max-height .3s cubic-bezier(.165,.84,.44,1)` (**no delay**) |
| `.tab-content` | `20,1154 351×439`, `margin-top:8px`, `padding:16px`, gap 16px, radius `32px 32px 20px 20px`, bg `#fff` |
| `.tab-content-image` | `36,1170 319×319` (1:1), radius 12px |

> The open/close asymmetry is real and worth reproducing: opening waits **100ms** then animates max-height over **300ms**; closing starts immediately over **300ms**.

### 4.4 Tab switching behaviour (jQuery, index-based)

```js
$(".tab-trigger").each(function (index) {
  $(this).on("click", function () {
    $(".tab-trigger.cc-active").removeClass("cc-active");
    $(this).addClass("cc-active");
    $(".tab-content.cc-card.cc-active").removeClass("cc-active");
    $(".tab-content.cc-card").eq(index).addClass("cc-active");
  });
});
```

Only the **desktop cards** are switched in JS. The accordion needs no JS — `.cc-active` on the trigger drives `+ .tab-content-mask` in CSS. `href="#"` on the trigger, so suppress default navigation.

Measured before/after clicking tab 2 @1440:
- before: card 1 `opacity:1`, `transform:none`, `position:relative`; cards 2–3 `opacity:0`, `position:absolute`
- after: card 1 `opacity:0`; card 2 `opacity:1`, `transform:matrix(1,0,0,1,0,9.05e-07)` (i.e. settled at 0), `position:relative`
- trigger backgrounds: active `rgb(255,255,255)`, inactive `rgba(0,0,0,0)`; all radii stay `99px` at 1440

There is also a **CSS animation** on every card from the inline embed, which replays on each activation because `display` flips:

```css
@keyframes slideInFromBottom { 0%{transform:translateY(20%)} 100%{transform:translateY(0)} }
.tab-content.cc-card { animation: slideInFromBottom .5s ease }
```

Combined effect when switching: the incoming card fades in over 300ms (`cubic-bezier(.165,.84,.44,1)`) **and** slides up from `translateY(20%)` over 500ms `ease`. The `transform:translateY(50%)` in the base `.cc-card` rule is overridden by the animation while it runs.

Also note from the inline embed: `.tab-content.cc-card { pointer-events:none }` and `.tab-content.cc-card.cc-active { pointer-events:auto }`.

### 4.5 Tab copy

**`/parents`** — eyebrow "how it works"; `h2.h3.u-mb-0` "We help families find reliable, flexible kidcare"; `p.u-mb-0.paragraph-1-5` "We'll match you with sitters based on your family's needs and their availability."

| # | Label | Body | Image |
|---|---|---|---|
| 1 | "Sign up" | "We like to keep it simple. Tell us your contact information and a little bit about your kids. Just like that, you're all set." | `…f022_Sign up 2.webp` — alt "Mom holding baby, checking iPad" |
| 2 | "Book a sitter" | "Let us know when you need care and we'll match you with a sitter based on your family's needs and their availability." | `…f01e_home tabs – book.webp` — alt "Kid in parent's lap" |
| 3 | "Get care & pay" (**non-breaking space** before "pay") | "We've got it from here. Your sitter will show up so you can head out. After your booking wraps up you'll receive a payment request through our app." | `…f01c_home tabs – heda out.webp` — alt "Mom holding and kissing kid" |

**`/sitters`** — eyebrow "how it works"; `h2.h3.u-mb-0` "Be the extra set of hands every family needs"; `p.u-mb-0.paragraph-1-5` "Join us in making parents lives easier. Just follow these steps and you'll be all set to care with Otter."

| # | Label | Body | Image |
|---|---|---|---|
| 1 | "Sign up" | "Tell us about yourself, your availability, and your childcare experience. We'll have you pass a background check to ensure a trustworthy, reliable community of sitters." | `…f023_sitters sign up 2.webp` — alt "Woman checking phone" |
| 2 | "Find & book jobs" | "We'll match you with families and situations that fit your schedule, situation and experience. Care requests will come your way from parents that could use a hand." | `…f013_Sitters - Find & Book Jobs.webp` — alt "Kid toys" |
| 3 | "Give care & get paid" | "When it's time, head over to your family's place to give care. You'll receive payment for your time and care the Friday following your bookings." | `…f01f_Sitters - Care an get paid.webp` — alt "Kid having breakfast" |

Bodies 2 and 3 on `/sitters` use a curly apostrophe `’` (U+2019) in "We'll" / "it's"; bodies on `/parents` use the straight `'`. Preserve as-is.

---

## 5. New component: CTA card (`/parents`, `/sitters`)

```
section.section.u-p-0.u-mb-3          /* /parents */
section.section                        /* /sitters */
  div.container.cc-cta[.cc-wide-cta]
    div.container.cc-narrow.cc-cta-2
      div.row.row-justify-between
        div.col.col-lg-5.col-md-6.col-sm-11.u-mb-0
          div.section-header
            h2.h3.u-mb-0
            a.btn.w-button
        div.col.col-lg-4.u-mb-0        /* empty spacer */
    div.cta-image-wrapper
      div.shape-contain.cc-cta         /* display:none ≥768 */
        div.shape-ratio > div.shape.footer-shape-right.<fill>
      div.cta-image-contain[.cc-extra-wide]
        div.cta-image-aspect[.cc-wide]
          img.u-img-cover
```

```css
.container.cc-cta { background-color:var(--white); border-radius:4.5rem /*72px*/;
  display:flex; flex-direction:column; justify-content:center; align-items:stretch;
  min-height:30rem /*480px*/; padding-block:4rem /*64px*/; overflow:hidden;
  isolation:isolate /* from inline embed */ }
@media (max-width:991px){ .container.cc-cta.cc-wide-cta{ justify-content:flex-start; padding-bottom:39% } }
@media (max-width:767px){ .container.cc-cta{ border-radius:2rem /*32px*/; min-height:auto;
    padding:2rem 2rem 11rem }
  .container.cc-cta.cc-wide-cta{ padding-bottom:41% }
  .container.cc-cta.u-pb-2{ padding-bottom:2rem } }
@media (max-width:479px){ .container.cc-cta{ padding-bottom:13.3rem /*212.8px*/ } }

.cta-image-wrapper { position:absolute; inset:0; z-index:1; display:flex;
  justify-content:flex-end; align-items:center; width:100%; height:100% }
@media (max-width:991px){ .cta-image-wrapper.cc-extra-wide{ justify-content:center; align-items:flex-end } }
@media (max-width:767px){ .cta-image-wrapper{ justify-content:space-between;
  align-items:flex-end; inset:auto 0 0 } }

.cta-image-contain { width:33% }
.cta-image-contain.cc-extra-wide { width:50% }
@media (max-width:991px){ .cta-image-contain{ width:50%; margin-right:-10% }
  .cta-image-contain.cc-extra-wide{ width:90%; margin-right:0 } }
@media (max-width:767px){ .cta-image-contain{ position:absolute; inset:auto 0 0 auto;
    margin-bottom:-18%; margin-right:-14% }
  .cta-image-contain.cc-extra-wide{ width:100%; margin-bottom:0; margin-left:auto } }
@media (max-width:479px){ .cta-image-contain{ width:80%; margin-bottom:-40%; margin-right:-35% }
  .cta-image-contain.cc-extra-wide{ margin-right:-11% } }

.cta-image-aspect { width:100%; padding-top:141%; position:relative; overflow:hidden }
.cta-image-aspect.cc-wide       { padding-top:75% }
.cta-image-aspect.cc-extra-wide { padding-top:62% }   /* declared, unused on these routes */

.shape-contain.cc-cta { width:55%; display:none }
@media (max-width:767px){ .shape-contain.cc-cta{ display:block;
  margin-bottom:-24%; margin-left:-10% } }
@media (max-width:479px){ .shape-contain.cc-cta{ width:60%;
  margin-bottom:-8%; margin-left:-16% } }
```

### Measured

**`/parents`** — `.cta-image-contain` (33%) + `.cta-image-aspect` (141%), image `mom on phone.webp`, `alt=""`, decorative blob `footer-shape-right.u-bg-peach`:

| Element | @1440 | @1024 | @390 |
|---|---|---|---|
| `section` | `0,1580 1440×480` (`padding:0; margin-bottom:48px`) | `0,1746 1024×480` | `0,1809 390×422` |
| `.container.cc-cta` | `72,1580 1296×480`, r72, bg `#fff`, `padding:64px 0` | `51,1746 921.6×480` | `20,1809 351×422` |
| `.container.cc-narrow.cc-cta-2` | `169,1673 1101.6×294` (85% of 1296) | `120,1811 783.3×350` | `52,1841 287×177.2` |
| `h2.h3.u-mb-0` | `169,1673 435.7×224` | `120,1811 343.6×280` | `52,1841 259.8×115.2` |
| `.btn` ("Book kidcare") | `169,1921 144.4×46` | `120,2115 144.4×46` | `52,1972 144.4×46` |
| `.cta-image-contain` | `940,1518 427.7×603` | `669,1771 304.1×428.8` | `213,1975 280.8×395.9` |
| `.shape-contain.cc-cta` | hidden | hidden | `-37,2049 210.6×210.6` |

Copy: `h2.h3.u-mb-0` → "Experienced kidcare is right around the corner." (the period is in the source). CTA → "Book kidcare", `https://app.withotter.com/sign-up/welcome`, `target=_blank`.

**`/sitters`** — `.cta-image-contain.cc-extra-wide` (50%) + `.cta-image-aspect.cc-wide` (75%), image `holding hands.webp`, blob `footer-shape-right.u-bg-celeste`, container gets `.cc-wide-cta`:

| Element | @1440 | @1024 | @390 |
|---|---|---|---|
| `section` | `0,1616 1440×640` (`padding:80px 0`) | `0,1820 …` | `0,1898 390×465` |
| `.container.cc-cta.cc-wide-cta` | `72,1696 1296×480` | `51,1820 921.6×480` | `20,1946 351×369.1` |
| `.cc-cta-2` | `169,1789 1101.6×294` | `120,1913 783.3×294` | `52,1978 287×177.2` |
| `h2.h3.u-mb-0` | `169,1789 435.7×224` | `120,1913 417.2×224` | `52,1978 259.8×115.2` |
| `.btn` ("Sign up") | `169,2037 100×46` | `120,2161 100×46` | `52,2110 100×46` |
| `.cta-image-contain` | `720,1693 648×486` | `512,1887 460.8×345.6` | `58,2052 351×263.3` |
| `.shape-contain.cc-cta` | hidden | hidden | `-37,2133 210.6×210.6` |

Copy: `h2.h3.u-mb-0` → "Make people's day with kind, compassionate kidcare." (curly apostrophe `’`). CTA → "Sign up", `https://app.withotter.com/sign-up/welcome`, `target=_blank`.

### The `/sitters` h1 weight quirk

`.u-mb-0` is a heavily overloaded Webflow combo class. The variant that wins for `h1.u-mb-0` is `.u-mb-0{margin-bottom:0;font-weight:400}`. Measured: `/sitters` `h1` computes **`font-weight:400`** and `margin-bottom:0`, whereas `/parents` and `/trust-safety` (plain `h1`) compute `font-weight:900`, `margin-bottom:16px` (9.6px @390).

Because **only `RecklessNeue-Heavy.woff` (900) is self-hosted**, the browser has no 400 face and renders the 900 file for both. So the two headings look the same, but if you ship a real 400-weight display face the `/sitters` h1 will diverge. Safest build: declare `font-weight:400; margin-bottom:0` on that h1 and map every Reckless Neue weight to the single Heavy file, exactly as the original does.

---

## 6. New component: testimonials slider (`/parents`, `/sitters`)

**Critical: the slider has a real `.swiper` element but the CMS collection is EMPTY.** Measured: `document.querySelectorAll('.swiper').length === 1`, `.swiper-slide` → **0**, and the list renders Webflow's placeholder `div.w-dyn-empty` → "No items found." with `background:#ddd; padding:10px`. This grey box is **visible on the live production site**.

Unlike the homepage (where Swiper was loaded but had no `.swiper` target at all), here `new Swiper(".swiper", …)` **does** initialise against a real element with zero slides.

### Structure

```
section.section
  div.container                               /* NOT cc-narrow */
    div.col.col-lg-6.col-md-6.u-mb-0          /* stray empty col, 648×0 — drop it */
    div.row.row-justify-between
      div.col.col-lg-5.col-md-12
        div.u-bg-ivory
          div.testimonials-contain
            div.section-header
              div.eyebrow → "testimonials"
              h2.h3.u-mb-0
              p.paragraph-1-5.u-mb-0
            div.slider-arrows-wrapper
              a.swiper-arrow.swiper-button-prev[href="#"][aria-label="previous slide"]
                div.swiper-icon > div.w-embed > svg
              a.swiper-arrow.swiper-button-next[href="#"][aria-label="next slide"]
      div.col.col-lg-6.col-md-12
        div.swiper-contain
          div.swiper.w-dyn-list
            div.w-dyn-empty → "No items found."
```

```css
.testimonials-contain { position:relative; z-index:99; display:flex; flex-direction:column;
  justify-content:space-between; align-items:flex-start; width:80%; height:100% }
@media (max-width:991px){ .testimonials-contain{ flex-flow:wrap;
  justify-content:space-between; align-items:flex-end; width:100% } }

.slider-arrows-wrapper { display:flex; gap:1em /*16px*/; margin-top:3rem /*48px*/ }
@media (max-width:767px){ .slider-arrows-wrapper{ width:100%; margin-top:1rem /*16px*/ } }

.swiper-arrow { display:flex; justify-content:center; align-items:center;
  width:3em /*48px*/; height:3em; border-radius:50%; cursor:pointer;
  background-color:var(--white);
  transition: color .3s cubic-bezier(.165,.84,.44,1),
              background-color .3s cubic-bezier(.165,.84,.44,1) }
.swiper-arrow:hover { background-color:var(--primary); color:var(--celeste) }
.swiper-arrow.swiper-button-next { transform: rotate(180deg) }
.swiper-arrow.swiper-button-next:hover { background-color:var(--primary) }

.swiper-icon { width:1.375em /*22px*/; height:1.75em /*28px*/; overflow:hidden }

.swiper-contain { flex-direction:row; height:100% }
@media screen and (min-width:992px){                 /* from the inline <style> */
  .swiper-contain { clip-path: inset(-100vw -100vw -100vw 0) }
}
.swiper { z-index:2; cursor:grab; height:100% }

/* declared for slides that never render on these routes: */
.swiper-slide { background-color:var(--primary); color:var(--white);
                border-radius:2em /*32px*/; flex:none }
.swiper-slide:nth-child(5n+2){ background-color:#94954C; color:#F8F6F5 }
.swiper-slide:nth-child(5n+3){ background-color:#FBAD9C; color:#00373E }
.swiper-slide:nth-child(5n+4){ background-color:#AC9E88; color:#00373E }
.swiper-slide:nth-child(5n+5){ background-color:#FBD3B6; color:#00373E }
```

Measured (`/parents` @1440 — `/sitters` identical geometry, y-offsets +148):

| Element | @1440 | @1024 | @390 |
|---|---|---|---|
| `.u-bg-ivory` | `72,2188 516.7×439.6` | `51,2354 360.7×439.6` | `20,2327 351×227.2` |
| `.testimonials-contain` | `72,2188 413.3×439.6` | `51,2354 288.5×439.6` | `20,2327 351×227.2` |
| `h2.h3.u-mb-0` | `72,2231 413.3×168` | `51,2397 288.5×168` | `20,2363 351×57.6` |
| `p.paragraph-1-5.u-mb-0` | `72,2423 413.3×108` | `51,2589 288.5×108` | `20,2436 351×54` |
| `.slider-arrows-wrapper` | `72,2579 112×48` | `51,2745 112×48` | `20,2506 **351**×48` |
| `.swiper-arrow` | `72,2579 48×48` | `51,2745 48×48` | `20,2506 48×48` |
| `.swiper-icon` | `85,2589 22×28` | `64,2755 22×28` | `33,2516 22×28` |
| `.swiper-contain` / `.swiper` | `740,2188 628×439.6`, clip-path `inset(-1440px -1440px -1440px 0px)` | `532,2354 440.8×439.6` | `20,2594 351×44` (no clip-path) |
| `.w-dyn-empty` | `740,2188 628×44` | `532,2354 440.8×44` | `20,2594 351×44` |

The `.u-bg-ivory` wrapper paints ivory on ivory — invisible, but keep it for layout (it is the thing that is 516.7 wide while `.testimonials-contain` is 80% of it).

Arrow SVG — `viewBox="0 0 22 28"`, `fill="currentColor"`, uses a `<mask id="path-1-inside-1_199_686">`. The visible path `d`:

```
M11.5314 26.823L10.3135 28C3.72297 21.6755 0.000137671 17.9124 0.000138013 14C0.000138355 10.0876 3.72297 6.28301 10.3135 -1.02167e-06L11.5314 1.16874C5.45837 6.9966 2.31558 10.315 1.8029 13.1715L22 13.1715L22 14.8293L1.80307 14.8293C2.31628 17.6843 5.45904 20.9958 11.5314 26.823Z
```

It is a left-pointing arrow; `.swiper-button-next` is the same SVG rotated 180°. Verified hover: background → `rgb(0,55,62)`, colour → `rgb(202,255,242)` over 300ms.

### Swiper config (runs on these routes)

```js
const swiper = new Swiper(".swiper", {
  navigation: { nextEl: ".swiper-button-next", prevEl: ".swiper-button-prev" },
  speed: 400,
  spaceBetween: "4%",
  slidesPerView: 1.25,
  breakpoints: {
    480: { slidesPerView: 2 },     // mobile landscape
    768: { slidesPerView: 2.1 },   // tablet
    992: { slidesPerView: 1.5 }    // desktop
  }
});
```

(Swiper 9 from jsDelivr, plus `swiper-bundle.min.css`. `speed: 400` is the slide transition; Swiper's default easing is `ease-out` via its own transition handling.)

**Build recommendation:** since there are zero slides, either omit the slider column entirely or render a real carousel with placeholder slides using the colour loop above. Reproducing the grey "No items found." box pixel-for-pixel is almost certainly not wanted — flag to the caller, don't silently invent testimonial copy.

### "Common questions" section (`/parents`, `/sitters`)

```
section.section
  div.container.cc-narrow
    div.row.row-justify-around            /* justify-content: space-around */
      div.col
        div.section-header
          h2.h3.u-mb-0 → "Common questions"
    div.w-dyn-list
      div.w-dyn-empty → "No items found."
```

Also an **empty CMS collection**. `h2` measured `120,2827 534.3×56` @1440, `20,2774 274.8×28.8` @390; the `.w-dyn-list` placeholder `120,2923 1200×44` @1440. Section is `80px 0` / `48px 0`, total height 300 @1440 / 209 @390.

**There is no accordion markup or CSS behind this heading** — the FAQ items would have come from the CMS. Nothing to build beyond the heading. Same recommendation as above.

---

## 7. New component: trust cards + video (`/trust-safety`)

One `section.section` holds both blocks.

```
section.section
  div.container.cc-narrow
    div.u-mb-2                                        /* margin-bottom:2em = 32px */
      div.row.row-justify-center.row-md-justify-start.row-align-end
        div.col.col-lg-10.col-md-12
          div.trust-content
            div.section-header
              h2.h3.u-mb-0 → "High-quality childcare, without question"
            p.paragraph-1-25.u-mb-0 → "Our community of caregivers …"
            div.u-aspect-9x16
              div.u-img-cover.w-video.w-embed [style="padding-top:56.27659574468085%"]
                iframe.embedly-embed [title="Trust and Safety at Otter"]
    div.u-mt-1                                        /* margin-top:1em = 16px */
      div.row.row-justify-center
        div.col.col-lg-5.col-md-6.col-sm-12 > div.trust-card   /* card 1 */
        div.col.col-lg-5.col-md-6.col-sm-12 > div.trust-card   /* card 2 */
      div.row.row-justify-center
        div.col.col-lg-5.col-md-6.col-sm-12 > div.trust-card   /* card 3 */
        div.col.col-lg-5.col-md-6.col-sm-12 > div.trust-card   /* card 4 */
```

Note `.section-header` here wraps **only** the `h2`; the lede paragraph and the video are its *siblings* inside `.trust-content`, which is the flex-wrap container.

```css
.trust-content { display:flex; flex-flow:wrap; align-items:flex-end;
                 gap:3em 2em /* row 48px, column 32px */ }
@media (max-width:991px){ .trust-content{ gap:1em /*16px*/ } }
@media (max-width:767px){ .trust-content{ flex-direction:column } }

.u-aspect-9x16 { width:100%; padding-top:56%; position:relative; overflow:hidden;
  display:flex; justify-content:center; align-items:center;
  background-color:var(--ivory); border-radius:2em /*32px*/;
  isolation:isolate /* from inline embed */ }
@media (max-width:767px){ .u-aspect-9x16{ border-radius:1em /*16px*/ } }

.trust-card { display:flex; flex-direction:column; justify-content:space-between;
  height:100%; min-height:30em /*480px*/; padding:3em /*48px*/;
  background-color:var(--primary); color:var(--white); border-radius:2em /*32px*/ }
@media (max-width:991px){ .trust-card{ gap:2em /*32px*/; min-height:auto; padding:2em /*32px*/ } }

.trust-card_icon { max-width:6.5rem /*104px*/; margin-bottom:3rem /*48px*/ }
@media (max-width:479px){ .trust-card_icon{ width:50% } }

.trust-card_header { position:relative; z-index:3; display:flex; flex-direction:column;
  align-items:flex-start; gap:1.5em /*24px*/; max-width:80% }
@media (max-width:991px){ .trust-card_header{ gap:1em /*16px*/ } }
@media (max-width:767px){ .trust-card_header{ max-width:86% } }
@media (max-width:479px){ .trust-card_header{ max-width:100% } }

.trust-bar_header { margin-bottom:0; font-size:2em /*32px*/ }
@media (max-width:767px){ .trust-bar_header{ font-size:1.5em /*24px*/ } }
@media (max-width:479px){ .trust-bar_header{ font-size:1.25em /*20px*/ } }
```

`.trust-bar_header` is an `h3`, so it inherits `h3`'s `font-weight:600; line-height:1.2`. Measured **32px/38.4px w600 `#ffffff`** @1440 and @1024; **20px/24px** @390.

### Measured geometry

| Element | @1440 | @1024 | @390 |
|---|---|---|---|
| `section.section` | `0,888 1440×2096` | `0,…1024×…` | `0,920 390×2448` |
| `.u-mb-2` | `120,968 1200×824.3` | `51,998 921.6×738.3` | `20,968 351×470.1` |
| `.trust-content` | `223,968 993.3×784.3` | `131,998 761.3×698.3` | `20,968 351×430.1` |
| `h2` (inside `.section-header`) | starts `223,968`, ~480.7 wide | — | full width |
| `p.paragraph-1-25.u-mb-0` | `736,968 480.7×180` | `528,1012 364.7×210` | `20,1041 351×144` |
| `.u-aspect-9x16` | `223,1196 993.3×556.3` | `131,1270 761.3×426.3` | `20,1201 351×196.5` |
| iframe | `223,1196 993.3×559` | `131,1270 761.3×428.4` | `20,1201 351×197.5` |
| `.u-mt-1` | `120,1840 1200×1063.4` | `51,1784 921.6×1166.8` | `20,1486 351×1833.8` |
| `.trust-card` (1st) | `223,1840 476.7×480` | `131,1784 360.7×508.7` | `20,1486 351×385.5` |
| `.trust-card_icon` | `271,1888 104×81.5` | `179,1832 104×81.5` | `52,1518 104×81.5` |
| `.trust-card_header` | `271,2075 304.5×196.8` | `179,1962 211.7×283.2` | `52,1680 287×160` |
| `.trust-bar_header` | `271,2075 304.5×76.8` | `179,1962 211.7×115.2` | `52,1680 280.1×24` |
| `.trust-card_header p` | `271,2176 304.5×96` | `179,2101 211.7×144` | `52,1720 287×120` |

At 1440 the h2 and lede sit **side by side** (two ~480.7px columns, 32px column gap) with the video full-width beneath them (48px row gap). `align-items:flex-end` bottom-aligns the h2 and lede. At ≤767 `.trust-content` becomes a single column.

The 4 cards are `col-lg-5` (41.67%) inside `.row.row-justify-center`, laid out **2 rows of 2** — not a single 4-up wrap. At 390 all four stack full width.

### Card content (DOM order)

| # | `h3.trust-bar_header` | `p.u-mb-0` (16px/24px w400 `#ffffff`) | Icon (`alt`) |
|---|---|---|---|
| 1 | Universal background check | "Every member of the Otter community, including parents and sitters, is background checked so we can foster a safe and trustworthy community." | `universal screening.webp` ("Background Check") |
| 2 | Dedicated Support | "Our support team is on standby during active care sessions. We're prepared to respond to any questions or concerns that come up before, during, or after a care session." | `safety.webp` ("Dedicated support") |
| 3 | Payment Protection | "Booking care? Our secure platform protects your payments. Providing care? Our cancellation and late arrivals policies ensure you get paid even if unexpected changes occur." | `payment.webp` ("Payment Protection", `width="96"`) |
| 4 | Healthy Care Standards | "Otter's healthy care guidelines are designed to promote the health of children, sitters, and parents. We stay up to date on the latest guidance from public health authorities, helping you make the best decisions for your family." | `health.webp` ("Healthy Care Standars" — typo in source) |

Lede copy: "Our community of caregivers is made up of highly vetted sitters who have been selected based on their ability to create a safe environment for your children. We can confidently say, we'd leave our own kids with Otter in a heartbeat."

### The video — partially unmeasurable

`div.u-img-cover.w-video.w-embed` carries inline `style="padding-top:56.27659574468085%"` and contains a single cross-origin iframe:

- `title="Trust and Safety at Otter"`
- `class="embedly-embed"`
- `src` = `https://cdn.embedly.com/widgets/media.html?src=https%3A%2F%2Fplayer.vimeo.com%2Fvideo%2F705608326%3Fh%3D131a48dcba%26app_id%3D122963&dntp=1&display_name=Vimeo&url=https%3A%2F%2Fplayer.vimeo.com%2Fvideo%2F705608326&image=https%3A%2F%2Fi.vimeocdn.com%2Fvideo%2F1424614019-1e9830b25303d82a02dfd4e33829977859d0df3d56aac3d91891ef53ee666073-d_1280&key=96f1f04c5f4143bcb0f2e68c87d65feb&type=text%2Fhtml&schema=vimeo`
- no `allow` attribute, no `allowfullscreen`
- Vimeo video id **705608326**, `h=131a48dcba`, `app_id=122963`
- poster frame: `https://i.vimeocdn.com/video/1424614019-1e9830b25303d82a02dfd4e33829977859d0df3d56aac3d91891ef53ee666073-d_1280`

**Explicitly not measured:** the iframe is cross-origin, so I could not read its internal DOM, poster crop, play-button styling or player chrome. `document.querySelectorAll('video').length === 0` in the top document — there is **no autoplaying media**; it is an embedly click-to-play facade. The outer `.u-aspect-9x16` is a 56%-ratio ivory box with 32px radius (16px ≤767); the iframe fills it absolutely via `.u-img-cover`. Build it as a click-to-play poster + iframe, or embed the Vimeo player directly with the poster above.

> Side effect worth knowing: this iframe keeps the network permanently busy, so Playwright's `waitUntil:'networkidle'` never settles on `/trust-safety`. Use `'load'` plus a fixed wait when auditing this route.

---

## 8. Motion — complete audit

I matched every IX2 event against the real DOM of all three routes.

### 8.1 IX2: exactly one live interaction per page

`grep data-w-id` across all three pages returns **one** value, on all three: `e9e5205a-cbfa-d6b9-11fc-6e90b3191d6d`, attached to `a.nav_mobile-btn`.

That means:

- **The only IX2 interactions with live targets are the mobile-nav open (`e-41` → `a-10`) and close (`e-42` → `a-11`).** These are **unchanged from the homepage spec §7.2 / §7.3** — same action lists, same `outQuart` = `cubic-bezier(0.165,0.84,0.44,1)` throughout, same ~600ms open / ~500ms close, same `.nav_menu-overlay` click-to-close jQuery shim. Re-verified by clicking at 390: `.nav_menu-card` ends `opacity:1`, `transform:matrix(1,0,0,1,0,0)`, peach, 36px padding, 24px radius; overlay `opacity:1` at `0,0 390×844`.
- **The homepage's scroll reveal does NOT run here.** `.section-header.cc-tabas-header` exists on `/parents` and `/sitters` but the element is `<div class="section-header cc-tabas-header">` — **no `data-w-id`, no inline `style="opacity:0"`**. Do not add a reveal. Verified: it renders at full opacity with no transform on load.
- **There is no scroll-triggered animation of any kind on these three routes, and no stagger.**

### 8.2 CSS transitions (the real motion)

| Target | Property / duration / easing | Trigger |
|---|---|---|
| `.btn` (all variants) | `color, background-color, border-color` — `.3s cubic-bezier(.165,.84,.44,1)` | hover; same as homepage |
| `.nav_link-current-icon` | `opacity, transform` — `.3s cubic-bezier(.165,.84,.44,1)` | `:hover` on `.nav_link`, and permanently on `.w--current`, **≥992px only** |
| `.swiper-arrow` | `color, background-color` — `.3s cubic-bezier(.165,.84,.44,1)` | hover → bg `#00373e`, colour `#cafff2` |
| `.tab-trigger` | `border-radius` — `.3s cubic-bezier(.165,.84,.44,1)` | gaining/losing `.cc-active` (visible only ≤479, where the active trigger's top corners go 99px → 20px) |
| `.tab-content.cc-card` | `opacity` — `.3s cubic-bezier(.165,.84,.44,1)` | `.cc-active` toggle |
| `.tab-content.cc-card` | `animation: slideInFromBottom .5s ease` (`translateY(20%)` → `0`) | replays whenever the card becomes active (display flips) |
| `.tab-content` | `all .3s cubic-bezier(.165,.84,.44,1)` | — |
| `.tab-content-mask` | `max-height .3s cubic-bezier(.165,.84,.44,1)` — **plus `transition-delay:100ms` when opening** | `.cc-active` on the preceding `.tab-trigger`, ≤991px |

Button hover/active/focus states, the `::selection` colours and the global `focus-visible` outline are all unchanged from the homepage spec §7.4.

### 8.3 Carousels / marquees / video / canvas

- **Swiper: 1 live `.swiper` element on `/parents` and `/sitters`** (0 on `/trust-safety`), but **0 `.swiper-slide`** — the CMS collection is empty. Config in §6. Autoplay is **not** configured; there is no loop and no marquee anywhere.
- **No marquees. No `<video>` elements** (0 on all three routes). No `<canvas>`.
- One cross-origin Vimeo/embedly iframe on `/trust-safety` (§7) — click-to-play, not autoplaying.
- Accordion open/close timings: 300ms, `cubic-bezier(.165,.84,.44,1)`, +100ms delay on open only.

### 8.4 Reduced motion

No `@media (prefers-reduced-motion)` block exists in the stylesheet or the inline embed. Consider adding one in the clone, but it is **not** in the original.

### 8.5 Site-wide inline `<style>` embed — ship this

Lives in `div.styles__global-embed-code.w-embed` and is **byte-identical on all three routes** (diffed). The homepage spec captured only the keyframe; here is everything in it that matters for these pages:

```css
a { text-underline-position: under; text-decoration-thickness: .1em; text-underline-offset: .05em }
.w-richtext>:first-child { margin-top: 0 }
.w-richtext>:last-child, .w-richtext ol li:last-child, .w-richtext ul li:last-child { margin-bottom: 0 }

/* Disable click action */
.hero_overlay, .u-click-none, .tab-content.cc-card, .nav_logo-wrapper { pointer-events: none }
/* Re-enable inside a pointer-events:none parent */
.tab-content.cc-card.cc-active, .brand_logo { pointer-events: auto }

/* Display icon on active tab */
.tab-trigger.cc-active .tab-trigger_icon { display: block }

@keyframes slideInFromBottom {
  0%   { transform: translateY(20%) }
  100% { transform: translateY(0) }
}
.tab-content.cc-card { animation: slideInFromBottom .5s ease }

/* Enable rounded corners iOS */
.container.cc-hero, .container.cc-cta, .u-aspect-9x16, .blog_item-image, .tab-content-image {
  isolation: isolate;
}

.tab-trigger.cc-active + .tab-content-mask { max-height: 800px }

/* Testimonials slider colour loop */
.swiper-slide:nth-child(5n+2) { background-color:#94954C; color:#F8F6F5 }
.swiper-slide:nth-child(5n+3) { background-color:#FBAD9C; color:#00373E }
.swiper-slide:nth-child(5n+4) { background-color:#AC9E88; color:#00373E }
.swiper-slide:nth-child(5n+5) { background-color:#FBD3B6; color:#00373E }

@media screen and (min-width: 992px) {
  .swiper-contain { clip-path: inset(-100vw -100vw -100vw 0) }
  .nav_link.w--current .nav_link-current-icon { opacity: 1; transform: translateY(0) }
  .nav_link:hover        .nav_link-current-icon { opacity: 1; transform: translateY(0) }
}
```

Plus a second, per-page `div.w-embed` sitting after the tabs row on `/parents` and `/sitters`, which re-declares the mask rule **with the delay**:

```css
.tab-trigger.cc-active + .tab-content-mask { max-height: 800px; transition-delay: 100ms }
```

---

## 9. New / changed type roles

Measured at 1440 / 1024 / 390. Roles already in §4 of the homepage spec are omitted unless a value differs.

| Role | Selector | @1440 & @1024 | @390 | Colour |
|---|---|---|---|---|
| **Hero H1 (light)** | `header h1` | `80px / 80px`, w**900**, ls `-0.8px`, Reckless Neue, `mb 16px`, `text-align:start` | `48px / 48px`, w900, ls `-0.48px`, `mb 9.6px` | `#00373e` (**not** white — new) |
| **Hero H1, sitters** | `header h1.u-mb-0` | `80px / 80px`, w**400**, ls `-0.8px`, `mb 0` | `48px / 48px`, w400, `mb 0` | `#00373e` |
| **Hero lede (1-25)** | `header p.paragraph-1-25.u-mb-0` | `20px / 30px`, w500, `mb 0`, `text-align:left`, `flex:1` | `16px / 24px`, w500 | `#00373e` |
| **Hero lede (1-5), trust** | `header p.paragraph-1-5` | `24px / 36px`, w500, `mb 24px`, **`text-align:center`** | `18px / 27px`, w500, `mb 18px` | `#00373e` |
| **Section H2** | `h2.h3.u-mb-0` | `56px / 56px`, w600, `mb 0` | `28.8px / 28.8px`, w600, `mb 0` | `#00373e` |
| **Eyebrow (plain)** | `div.eyebrow` | `14px / 19.6px`, w600, ls `0.49px`, uppercase, no bg | same | `#00373e` |
| **Tabs lede** | `.cc-tabas-header p.paragraph-1-5` | `24px / 36px`, **w400**, `mb 0`, `text-align:left` | `18px / 27px`, w400 | `#00373e` |
| **Tab label** | `.tab-trigger > div` | `16px / 24px`, w600 | same | `#00373e` |
| **Tab body** | `.tab-content p.u-mb-0.u-text-center` | `16px / 24px`, **w400**, `mb 0`, `text-align:center` | same | `#00373e` |
| **CTA H2** | `.cc-cta-2 h2.h3.u-mb-0` | `56px / 56px`, w600, `mb 0` | `28.8px / 28.8px` | `#00373e` |
| **Testimonial H2** | `.testimonials-contain h2.h3.u-mb-0` | `56px / 56px`, w600 | `28.8px / 28.8px` | `#00373e` |
| **Testimonial lede** | `.testimonials-contain p.paragraph-1-5.u-mb-0` | `24px / 36px`, **w400**, `mb 0`, `text-align:left` | `18px / 27px`, w400 | `#00373e` |
| **Trust card H3** | `h3.trust-bar_header` | `32px / 38.4px`, w600, `mb 0` | `20px / 24px`, w600 | `#ffffff` |
| **Trust card body** | `.trust-card_header p.u-mb-0` | `16px / 24px`, **w400**, `mb 0`, `text-align:start` | same | `#ffffff` |
| **Trust lede** | `.trust-content p.paragraph-1-25.u-mb-0` | `20px / 30px`, w500, `mb 0`, `text-align:left` | `16px / 24px`, w500 | `#00373e` |
| **Nav link** | `.nav_links-parent a.nav_link` | `16px / 24px`, w500, `padding:8px 0` | `24px / 36px`, w500, `padding 0`, `width:100%` | `#00373e` |
| **Footer list link** | `.footer_link a` | `16px / 24px`, w500 | same | `#00373e` |

At ≤767 `.trust-bar_header` is `1.5em` (24px) and at ≤479 `1.25em` (20px) — measured 20px at 390, confirming the ≤479 rule wins.

New radii not in homepage §5:

| Component | border-radius |
|---|---|
| `.container.cc-cta` | `4.5rem` → **72px**; `2rem` → **32px** ≤767 |
| `.tab-content` / `.tab-content.cc-card` | **48px**; ≤991 **32px**; ≤479 `32px 32px 20px 20px` |
| `.tab-item` (≤991) | **32px** |
| `.tab-trigger` | **99px** pill; ≤479 active → `20px 20px 99px 99px` |
| `.tab-content-image` | **32px**; ≤991 **24px**; ≤479 **12px** |
| `.trust-card` | `2em` → **32px** |
| `.u-aspect-9x16` | `2em` → **32px**; ≤767 `1em` → **16px** |
| `.swiper-arrow` | **50%** (48×48 circle) |
| `.swiper-slide` | `2em` → **32px** (never rendered) |
| `.nav_link.w--current` (≤991) | **99px**, bg `#fbad9cbd` = `rgba(251,173,156,.74)` |
| `.w-dyn-empty` | 0, bg `#dddddd`, padding 10px |

No new shadows. No new filters. `backdrop-filter: none` everywhere.

---

## 10. Links to routes outside the 10 known ones

Collected from every `a[href]` on all three routes.

**Within the known set:** `/`, `/parents`, `/sitters`, `/trust-safety`, `/blog`, `/faq`, `/careers`, `/contact`, `/terms-of-use`, `/privacy-policy`, plus `#` (burger + tab triggers + swiper arrows).

**New / outside the known routes — all four are footer social links, `target="_blank"`:**

| Href | Label |
|---|---|
| `https://www.instagram.com/otterchildcare/` | Instagram |
| `https://www.facebook.com/withotter/` | Facebook |
| `https://twitter.com/WithOtter` | Twitter |
| `https://www.linkedin.com/company/withotter` | Linkedin |

**External app URLs** (strip `device-id`, which is regenerated per session — I observed `0HDGi4CKnruMrpk6gzd-Pj`, `iLDwIULvVcFnHUEjR7Dx6l` and `NJ1fbftABJ6d8pzJ9Oix9n` across loads):

| Bare URL | Used by |
|---|---|
| `https://app.withotter.com/log-in` | nav "Log in" |
| `https://app.withotter.com/sign-up/welcome` | nav "Sign up"; all hero CTAs; both CTA-card buttons |
| `https://app.withotter.com/sign-up` | footer card "Get started" |

Note: on these three routes the hero and CTA-card buttons point at **`/sign-up/welcome`**, not the bare `/sign-up` the homepage used for its hero. Only the footer card uses `/sign-up`.

No `<form>`, no `<input>`, no `<select>`, no `<textarea>` on any of the three routes — **there are no forms or input states to spec here.** (`::placeholder` is declared globally but unused.)

---

## 11. Build notes / gotchas

1. **Two empty CMS collections render visible grey placeholders** on `/parents` and `/sitters` (testimonials slider, "Common questions"). Decide with the caller whether to omit those sections, stub them, or reproduce the placeholder. Do not invent testimonial or FAQ copy.
2. **`/trust-safety` is much simpler than the other two** — hero + one section + footer. No tabs, CTA card, slider or FAQ.
3. The `.tab-content` markup is **duplicated** (accordion bodies + desktop cards). Simplest clone: render once and drive both layouts from the same data, with `.col-md-hide` / `.tab-content-mask` controlling which is visible.
4. `.tabs-wrapper` is a **sibling** of `.section-header.cc-tabas-header`, not a child.
5. Stray elements to drop: the empty `div.col.col-lg-6.col-md-6.u-mb-0` before the testimonials row, the empty `div.col.col-lg-4.u-mb-0` in the CTA row, and the empty `div.container` before `.cc-footer-container`.
6. `.u-img-cover` is `object-fit: **contain**` despite the name — unchanged from the homepage, and it matters for the CTA and tab images, several of which are not square.
7. `.u-mb-0` is a landmine: it carries conflicting `font-weight` declarations (400/500/600) depending on cascade position. Don't model it as a pure margin utility — bake the measured weight into each role per §9.
8. Third-party scripts on the original (do **not** port): jQuery 3.5.1, Webflow IX2 chunks, Swiper 9 (jsDelivr) + its CSS, WebFont loader (Inconsolata — still unused), GTM/gtag, Facebook Pixel, Nextdoor Pixel, FullStory, Amplitude 8.17.0, embedly.
