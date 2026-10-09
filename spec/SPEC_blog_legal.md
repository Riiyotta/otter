Source: https://withotter.com/

# Otter — Blog + Legal Build Spec

Routes covered: `/blog`, `/blog-posts/*` (shared CMS template), `/terms-of-use`, `/privacy-policy`.

Measured live with Playwright on 2026-10-08 at **1440×900**, **1024×900**, **390×844**.
Companion asset manifest: `/Users/riyaghosh/V3/otter/spec/ASSETS_blog_legal.md`
Homepage/design-system spec (read first, not duplicated here): `/Users/riyaghosh/V3/otter/CLONE_SPEC.md`

Same Webflow project and **the same compiled stylesheet** as the homepage:
`https://cdn.prod.website-files.com/682e5411afe4660a9707efce/css/with-otter-ac17371ef8a503ba0b8fca450052.shared.34930fed5.min.css`
(byte-identical filename to the local reference copy at `reference/assets/…shared.34930fed5.min.css`, so all rules below were read out of that file and then confirmed against computed style in the live DOM).

Document heights: `/blog` 4174px @1440, 4070px @1024. `/blog-posts/series-a` 4262px @1440. `/terms-of-use` 20679px @1440, 37399px @390. `/privacy-policy` shorter but same structure.

---

## 0. What carries over unchanged from the homepage spec

Spot-checked and **confirmed identical** on all five pages — do not re-derive:

- **Fonts**: Jokker 400/500/600 (+ italics), Reckless Neue 900, `format("woff")`. Same URLs. Inconsolata still unused.
- **`:root` tokens**: `--primary #00373e`, `--white #fff`, `--celeste #cafff2`, `--peach #fbd3b6`, `--ivory #f8f6f5`, `--olive #94954c`, `--coral #fbad9c`, `--sandstone #ac9e88`.
- **`.container{width:90%;max-width:90rem}`** → 1296px @1440, 921.59px @1024, 351px @390 (`width:85%` ≤991, `90%` ≤479). **`.cc-narrow` max-width 75rem** → 1200px @1440, 921.59px @1024, 351px @390.
- **12-col flex grid**: `.row{margin-inline:-20px}`, `.col{flex:1;padding-inline:20px;margin-bottom:40px}`, `col-*-N` = N/12. At ≤479 every `.col` → `flex-basis:100%;max-width:100%;order:1`.
- **`.section{padding-block:5rem}`** → 80px; 64px ≤991; 48px ≤479. Confirmed: legal + post + blog-list sections all measured **80px @1440 and @1024, 48px @390**.
- **Breakpoints** 991 / 767 / 479 max-width. **1024 renders desktop styles** (verified again: legal `h1` is still 80px at 1024).
- Base type scale (`h1` 5rem Reckless 900 ls −.01em; `h2` 4.5rem/1 w600; `h3` 3.5rem/1.2 w600; `h4` 2.5rem/1.1 w600; `.h2` 4.5rem/**1.1** mb .3em; `.h3` 3.5rem w600; `.h4` 2.5rem/1.1 mb .6em; `.paragraph-1-25` 1.25rem **w400**) — unchanged, full responsive table in homepage spec §4.
- **No gradients, no `backdrop-filter`, no `filter`** anywhere on any of these five pages (verified by walking every element).
- **No `<video>`, no `<iframe>`, no `.swiper`** on any of these pages. Swiper 9 is still loaded and still unused — do not ship it.
- Footer markup is the homepage footer **plus a populated link block** (see §1.2) — otherwise identical, including the two `clip-path` footer shapes (`#footer-shape-left` olive, `#footer-shape-right` peach). The only `clip-path` users on these pages are those two divs; **no new blob shapes anywhere in blog or legal.** Reuse the path `d` strings verbatim from homepage spec §5.
- `::selection`, `a` underline tuning, `a:focus-visible{2px dashed}` — unchanged.

### Corrections / additions to the shared system

| Thing | Homepage spec said | Blog/legal reality |
|---|---|---|
| `.footer_links-container` | "**empty** on this page, renders as a 0-height spacer" | **Populated on every one of these pages** with 3 `ul.footer_link-list`. See §1.2. |
| Nav | only "Log in" + "Sign up" | **Full primary nav is present**: Parents / Sitters / Trust & Safety / Blog, in a second `.nav_links-parent`. See §1.1. |
| `.nav_link-current-icon` | "not present in this page's DOM — no nav hover effect to build" | **Present and live.** Real hover + current-page affordance. See §1.1. |
| `.u-mb-0` | used as a margin reset | It also declares **`font-weight:400`** (`.u-mb-0{margin-bottom:0;font-weight:400}`). This is why `/blog` and `/terms-of-use` `h1`s compute **w400 Reckless Neue, not w900**. Easy to get wrong — see §4. |

---

## 1. Shared chrome on these routes

### 1.1 Nav — now has primary links

`nav.nav_wrapper > div.container.cc-nav > div.nav_menu > div.nav_menu-card` contains **two** sibling groups:

```
div.nav_links-parent            ← NEW (primary links)
  a.nav_link[href="/parents"]        > div "Parents"      + div.nav_link-current-icon
  a.nav_link[href="/sitters"]        > div "Sitters"      + div.nav_link-current-icon
  a.nav_link[href="/trust-safety"]   > div "Trust & Safety" + div.nav_link-current-icon
  a.nav_link[href="/blog"]           > div "Blog"         + div.nav_link-current-icon
div.nav_links-parent.cc-buttons ← as on homepage
  a.nav_link.cc-log-in[href="https://app.withotter.com/log-in"][target=_blank]  "Log in"
  a.btn.cc-white.w-button[href="https://app.withotter.com/sign-up/welcome"][target=_blank] "Sign up"
```

The active link gets Webflow's `w--current` class (on `/blog` that is the Blog link; on legal/post pages **no** link is current).

```css
.nav_links-parent{ display:flex; align-items:center; gap:1em /*16px*/; flex-wrap:nowrap }
.nav_link{ padding-block:.5em; position:relative; overflow:hidden }
.nav_link-current-icon{
  z-index:-1; opacity:0; color:var(--celeste); mix-blend-mode:multiply;
  display:flex; justify-content:center; align-items:center;
  width:100%; height:100%; margin-inline:auto;
  position:absolute; inset:0; transform:translateY(100%);
  transition: opacity .3s cubic-bezier(.165,.84,.44,1),
              transform .3s cubic-bezier(.165,.84,.44,1);
}
/* from the global <style> embed, desktop only */
@media screen and (min-width:992px){
  .nav_link.w--current .nav_link-current-icon{ opacity:1; transform:translateY(0) }
  .nav_link:hover      .nav_link-current-icon{ opacity:1; transform:translateY(0) }
}
@media (max-width:991px){
  .nav_links-parent{ flex-direction:column; align-items:flex-start; gap:16px;
                     border-bottom:1px solid var(--primary); padding-bottom:2rem }
  .nav_links-parent.cc-buttons{ flex-direction:row; align-items:center; gap:1.5em; border:1px #000; padding-bottom:0 }
  .nav_link{ color:var(--primary); width:100%; padding-block:0; font-size:1.5em /*24px*/ }
  .nav_link.w--current{ background-color:#fbad9cbd /*rgba(251,173,156,.741) coral @74%*/;
                        border-radius:99px; padding:8px 16px }
  .nav_link.cc-log-in{ width:auto }
  .nav_link-current-icon{ color:var(--coral) }
}
@media (max-width:479px){ .nav_links-parent, .nav_links-parent.cc-buttons{ gap:1.25em /*20px*/ } }
```

**Desktop nav-link measurements @1024** (`/blog`, each 40px tall, y=58):
`Parents` x=51.2 w=59.35 · `Sitters` x=126.55 w=49.86 · `Trust & Safety` x=192.41 w=106.2 · `Blog` x=314.61 w=34.09. Font 16px/24px w500 `#00373e`. 16px gaps.
Verified computed on the current icon @1024: `opacity:1`, `transform:matrix(1,0,0,1,0,0)` (i.e. translateY(0)), `color:rgb(202,255,242)`, `mix-blend-mode:multiply`.

So the desktop nav affordance is: **a celeste pill-less block slides up from below and multiply-blends behind the link label**, 300ms `outQuart`, on hover and permanently on the current page. On mobile the current page instead gets a solid coral-74% rounded pill.

Nav is still **not sticky** (`position:relative`, `margin-block:3rem`, `margin-top:2rem` ≤991).

### 1.2 Footer link block (new)

```
div.footer_row > div.footer_links-container
  ul.footer_link-list.w-list-unstyled   li.footer_link > a  → /parents, /sitters, /trust-safety
  ul.footer_link-list.w-list-unstyled   li.footer_link > a  → /faq, /careers, /blog, /contact
  ul.footer_link-list.w-list-unstyled   li.footer_link > a  → Instagram, Facebook, Twitter, Linkedin
```

External social hrefs, verbatim:
`https://www.instagram.com/otterchildcare/` · `https://www.facebook.com/withotter/` · `https://twitter.com/WithOtter` · `https://www.linkedin.com/company/withotter`
(The `/blog` link carries `w--current` on the blog route.)

```css
.footer_links-container{ display:flex; flex-wrap:wrap; width:80% }
.footer_link-list{ width:25%; padding-left:0 }
.footer_link{ margin-bottom:1.25rem /*20px*/; font-size:1rem }
@media (max-width:991px){ .footer_link-list{ width:30% } }
@media (max-width:767px){ .footer_links-container{ width:100%; justify-content:space-between }
                          .footer_link{ margin-bottom:.8rem /*12.8px*/ } }
@media (max-width:479px){ .footer_link-list{ width:50%; margin-bottom:1em } }
```

Measured @1440: container `544.09,3317.06 627.13×192`; each `ul` 157×176; each `li` 157×24; `a` display:inline, 16px/24px w500, `#00373e`, no underline.
Measured @390: container `43.5,… 303×326.38`, `justify-content:space-between`, each `ul` 151.5 wide with `margin-bottom:16px`, `li` margin-bottom 12.8px.
`li.footer_link` computes `display:list-item` but the `w-list-unstyled` parent removes the marker (`list-style:none;padding-left:0`).

---

## 2. `/blog` — CMS collection list

`<title>Adventures with Otter • The Otter Blog</title>`

### 2.1 Section structure, DOM order

```
div.page-wrapper
  nav.nav_wrapper                                   ← §1.1
  header.section.u-p-0                              ← page hero (padding:0)
    div.container.cc-narrow
      div.row.row-justify-between.row-align-center
        div.col.col-lg-5.col-md-7.col-sm-11.col-xs-12
          div.section-header
            h1.u-mb-0            "Adventures with Otter"
            p.paragraph-1-25.u-mb-0
        div.col.u-mb-0.col-lg-5.col-sm-12
          img                    (Blog Hero.webp — bare <img>, no aspect wrapper)
  main#main
    section.section
      h2.u-sr-only               "Blog posts"
      div.container
        div.w-dyn-list                               ← FEATURED list (limit 1)
          div[role=list].row.u-mb-2.w-dyn-items
            div[role=listitem].col.col-lg-12.w-dyn-item
              div.blog_item.cc-featured              ← featured card variant
        div.w-dyn-list                               ← MAIN list (9 per page)
          div[role=list].row.w-dyn-items[fs-cmsload-element="list"]
            9 × div[role=listitem].col.col-lg-4.col-md-6.col-sm-12.w-dyn-item
                  div.blog_item                      ← standard card
          div[role=navigation].w-pagination-wrapper.u-mt-3
            a.w-pagination-previous.u-d-none         (hidden, display:none)
            a.w-pagination-next.btn[fs-cmsload-mode="load-under"][href="?77d76c3c_page=2"]
              div.w-inline-block "Load more"
            link[rel=prerender][href="?77d76c3c_page=2"]
            div.w-page-count.u-d-none "1 / 4"
    div.section                                      ← CTA band
      div.container.cc-cta.cc-wide-cta
        div.container.cc-narrow.cc-cta-2
          div.row.row-justify-between
            div.col.col-lg-5.col-md-10.col-xs-11.u-mb-0
              div.section-header
                h2.h3.u-mb-0  "Find kidcare that works for your family."
                a.btn.w-button[href="#"]  "Book kidcare"
            div.col.col-lg-4                         ← EMPTY spacer col
        div.cta-image-wrapper.cc-extra-wide
          div.cta-image-contain.cc-extra-wide
            div.cta-image-aspect.cc-extra-wide
              img.u-img-cover  (blog-cta.webp)
    footer.section.cc-footer                         ← §1.2 + homepage footer
```

Real copy, verbatim:
- `h1.u-mb-0` → **"Adventures with Otter"**
- `p.paragraph-1-25.u-mb-0` → **"From parenting hacks to homemade slime recipes – we've thought of everything childcare so you don't have to."**
- `h2.u-sr-only` → **"Blog posts"**
- CTA `h2.h3.u-mb-0` → **"Find kidcare that works for your family."**
- CTA `a.btn` → **"Book kidcare"**, `href="#"` (dead link on the original — keep as `#`)
- Pagination button label → **"Load more"**

**There is no category filter, no tab bar, and no search on this page.** The only control is the single "Load more" button.
**No Webflow `.w-dyn-empty` empty-state block is present in the markup** for either list (Webflow only emits it when the designer adds one — it was not added). If you render an empty state, it is your own addition.

### 2.2 Hero header geometry

`header.section.u-p-0` → `.u-p-0{padding:0}` plus `@media(max-width:991px){.section.u-p-0{padding-top:0;padding-bottom:0}}`. Computed padding **0px at all three widths**.

| | @1440 | @1024 | @390 |
|---|---|---|---|
| `header.section.u-p-0` rect | `0,156 1440×421` | `0,156 1024×~400` | `0,128 390×534.28` |
| `.container.cc-narrow` | `120,156 1200×421` | `51.2,… 921.59×…` | `19.5,128 351×534.28` |
| `.row…row-align-center` | `100,156 1240×421`, `align-items:center` | `31.2,… 961.59×…` | `-0.5,128 391×534.28` (cols stack) |
| copy `.col.col-lg-5` | `100,210 517×274` | `31.2,… 400.66×304` | `-0.5,128 391×184` |
| `.section-header` | `120,210 477×274`, gap **24px** | gap 24px | `19.5,128 351×184`, gap **16px** |
| `h1.u-mb-0` | **80px/80px w400** ls −0.8px, Reckless Neue, mb 0 | same (80/80 w400) | **48px/48px w400** ls −0.48px |
| `p.paragraph-1-25.u-mb-0` | **20px/30px w500** mb 0 | 20px/30px w500 | **16px/24px w500** |
| image `.col.u-mb-0.col-lg-5` | `823,156 517×421` | `592.13,… 400.66×316.82` | `-0.5,352 391×310.28` (order:1 → below copy) |
| `img` (bare) | `843,156 **477×421**` | `612.13,… **358.39×316.82**` | `19.5,352 **350.99×310.28**` |

The hero image is a **plain `<img>` with no wrapper and no `object-fit`** — it renders at its natural 1983×1752 (1.1318:1) aspect, width-limited by the column (`max-width:100%`). `loading="lazy"`.
`sizes="(max-width:479px) 90vw, (max-width:767px) 85vw, (max-width:991px) 33vw, 35vw"`.

`.section-header` (shared primitive, used on every page here):
```css
.section-header{ z-index:3; position:relative; display:flex; flex-direction:column;
                 flex:1; gap:1.5em /*24px*/; align-items:flex-start }
@media (max-width:991px){ .section-header{ gap:1em /*16px*/ } }
```

### 2.3 The post card component

Two variants, both built from the same parts. **Important: the regular card's aspect div also carries `cc-featured`**, so *both* variants are 4:3 — there is no 1:1 card on this page even though `.blog_item-image-aspect` defaults to 1:1.

```css
.blog_item{ display:flex; flex-direction:column; gap:1em /*16px*/; position:relative }
.blog_item.cc-featured{ flex-direction:row; justify-content:flex-start;
                        align-items:center; gap:4em /*64px*/ }
@media (max-width:991px){ .blog_item.cc-featured{ flex-direction:column; gap:1em } }

.blog_item-image{ width:100%; border-radius:2em /*32px*/; overflow:hidden; isolation:isolate }
.blog_item-image.cc-featured{ width:50% }
@media (max-width:991px){ .blog_item-image{ width:100%; border-radius:1.5em /*24px*/ } }
@media (max-width:767px){ .blog_item-image{ border-radius:1em /*16px*/ }
                          .blog_item-image.cc-featured{ width:100% } }
@media (max-width:479px){ .blog_item-image{ border-radius:1em /*16px*/ } }

.blog_item-image-aspect{ width:100%; padding-top:100%; position:relative; overflow:hidden }
.blog_item-image-aspect.cc-featured{ padding-top:75% }   /* ← 4:3, used by BOTH variants */

.blog_heading-wrapper{ display:flex; flex-direction:column; gap:1em /*16px*/ }
.blog_heading-wrapper.cc-featured{ max-width:40% }
@media (max-width:991px){ .blog_heading-wrapper.cc-featured{ max-width:none; gap:.8em /*12.8px*/ } }

.blog_item-tags-wrapper{ display:flex; flex-wrap:wrap; align-items:center; gap:.5em /*8px*/ }

.tag{ background-color:var(--celeste); color:var(--primary);
      border-radius:8px; padding:.4em .8em; font-size:.875rem /*14px*/ }

.u-link-cover{ position:absolute; inset:0; width:100%; height:100%;
               display:flex; justify-content:center; align-items:center }
.u-link-cover:focus-visible, .u-link-cover[data-wf-focus-visible]{
  outline-offset:4px; outline-width:3px }
```

`.u-img-cover` is the homepage primitive — `object-fit:**contain**` (yes, contain), `position:absolute; inset:0; width:100%; height:100%`.
`.blog_item-image` carries `isolation:isolate` (set in the global `<style>` embed alongside `.container.cc-hero`) so the rounded corners clip correctly on iOS.

#### Featured card (`.blog_item.cc-featured`)

Markup — note the tag here is a **static, hand-authored `div.tag`** reading "Featured", not a CMS tag list:

```
div.blog_item.cc-featured
  div.blog_item-image.cc-featured > div.blog_item-image-aspect.cc-featured > img.u-img-cover
  div.blog_heading-wrapper.cc-featured
    div.blog_item-tags-wrapper > div.tag > div   "Featured"
    h3.h3                                        post title
  a.u-link-cover.w-inline-block[href="/blog-posts/…"] > div.u-sr-only (title repeated)
```

| | @1440 | @1024 | @390 |
|---|---|---|---|
| `.col.col-lg-12.w-dyn-item` | `52,657 1336×486` | `31.2,… 961.59×345.59` | `-0.5,710 391×401.98` |
| `.blog_item.cc-featured` | `72,657 1296×486`, row, gap 64px, align center | `51.2,… 921.59×345.59` | `19.5,710 351×401.98`, **column**, gap 16px, `align-items:center` |
| `.blog_item-image.cc-featured` | `648×486` (50%) r32 | `460.8×345.59` r32 | `351×263.25` (100%) r**16** |
| aspect `padding-top` | 75% → 486px | 345.594px | 263.25px |
| `.blog_heading-wrapper.cc-featured` | `518.4×199`, max-width 40%, gap 16px | `266.57` tall, max-w 40%, gap 16px | `351×122.73`, max-w none, gap **12.8px** |
| `div.tag` "Featured" | `83.84×32.19`, pad 5.6/11.2, r8, **bg `#cafff2` / fg `#00373e`** | same | same |
| `h3.h3` | **56px/67.2px w600**, mb 16.8px | 56/67.2 mb16.8 | **28.8px/34.56px w600**, mb 8.64px |

#### Standard card (`.blog_item`)

```
div.blog_item
  div.blog_item-image > div.blog_item-image-aspect.cc-featured > img.u-img-cover
  div.blog_heading-wrapper
    div.blog_item-tags-wrapper
      div.w-dyn-list > div[role=list].blog_item-tags-wrapper.w-dyn-items   ← nested CMS list
        n × div.tag.w-dyn-item[color="<token>"] > div   tag name
    h3.h4.u-mb-0                                        post title
  a.u-link-cover.w-inline-block[href="/blog-posts/…"] > div.u-sr-only (title repeated)
```

Note the doubly-nested `.blog_item-tags-wrapper` (outer static wrapper, inner `w-dyn-items`) — both get `display:flex;gap:8px`, so it behaves as one row.

| | @1440 | @1024 | @390 |
|---|---|---|---|
| `.col` box | `445.33` wide | `320.52` wide | `391` wide |
| `.blog_item` | `405.33` wide, gap 16px | `280.52` wide, gap 16px | `351` wide, gap 16px |
| `.blog_item-image` radius | **32px** | **32px** | **16px** |
| aspect padding-top (=image height) | `303.99px` | `210.39px` | `263.25px` |
| `.blog_heading-wrapper` gap | 16px | 16px | 16px |
| `.tag.w-dyn-item` | `32.19` tall, pad `5.6px 11.2px`, r8, 14px/21px w500 | same | same |
| `h3.h4.u-mb-0` | **40px/44px w600**, mb 0 | 40/44 | **20px/24px w600** |

#### Tag colour tokens

`div.tag.w-dyn-item` carries a `color="…"` attribute driven by a CMS field; the global `<style>` embed maps it:

```css
.tag{ background-color:var(--celeste); color:var(--primary) }   /* default / no attr */
.tag[color='coral']    { background:#FBAD9C }
.tag[color='sandstone']{ background:#AC9E88 }
.tag[color='peach']    { background:#FBD3B6 }
.tag[color='midnight'] { background:#00373E; color:#F8F6F5 }    /* only one that flips fg */
```

Verified computed: `midnight` → `bg rgb(0,55,62) / fg rgb(248,246,245)`; `peach` → `bg rgb(251,211,182) / fg rgb(0,55,62)`.
Tokens observed in the wild: `midnight`, `peach`, `coral`, `sandstone`. Tag names observed: `Childcare`, `Tips`, `Parenting`, `Otter news`, `SAHM`, `Daycare`.

#### Card hover — there is none

**Definitive: the cards have no hover state and no transition.** Verified two ways:
1. Grepped the whole compiled stylesheet for `:hover`/`:focus`/`:active` rules matching `blog_item`, `u-link-cover`, `.tag`, `cc-cta`, `w-pagination`, `footer_link`, `splitter`, `b-radius` → the **only** match is `.u-link-cover:focus-visible{outline-offset:4px;outline-width:3px}`.
2. Computed `transition` on `.blog_item`, `.u-link-cover` and the card `<img>` is `all 0s ease 0s` (no transition), and `transform` is `none`.

So: no image zoom, no lift, no colour change. Only the focus ring (global `a:focus-visible{outline:2px dashed var(--primary);outline-offset:2px}`, widened to 3px/4px by `.u-link-cover`). **Do not invent a hover effect.**

### 2.4 The grid

Both lists are plain `.row` / `.col` flex grids — **no CSS grid, no `gap`**. Spacing comes entirely from `.col{padding-inline:20px;margin-bottom:40px}` on a `.row{margin-inline:-20px}`.

→ **Effective column gutter 40px, effective row gap 40px**, at every breakpoint.

| Width | Column classes in play | Columns | `.col` width | `.blog_item` width | `.col` x positions |
|---|---|---|---|---|---|
| 1440 | `col-lg-4` | **3** | 445.33px | 405.33px | 52 / 497 / 943 |
| 1024 | `col-lg-4` | **3** | 320.52px | 280.52px | 31.2 / 351.73 / 672.25 |
| 390 | `col-xs` fallback (`flex-basis:100%`) | **1** | 391px | 351px | −0.5 |

(`col-md-6` → 2-up at ≤991; `col-sm-12` → 1-up at ≤767. 1024 is >991 so it stays 3-up.)

Featured row: `div.row.u-mb-2` → `.u-mb-2{margin-bottom:2em}` = **32px** (measured mb 32px at 1440, 1024 and 390), on top of the `.col`'s own 40px bottom margin.
The 9-item row is a plain `.row.w-dyn-items` (also measured mb 32px at 1024/390 — it inherits nothing extra; the 32px there is the `.u-mb-2` on the *featured* row above it. The main row itself has margin-bottom 0 at 1440).

### 2.5 Pagination / load-more

Not Webflow-native paging — it is **Finsweet CMS Load v1**:
`<script src="https://cdn.jsdelivr.net/npm/@finsweet/attributes-cmsload@1/cmsload.js">` (deferred, no `fs-cmsload` settings attribute on `<html>`).

- `div.row.w-dyn-items[fs-cmsload-element="list"]`
- `a.w-pagination-next.btn[fs-cmsload-mode="load-under"][href="?77d76c3c_page=2"]` → appends the next page in place.
- `div.w-page-count.u-d-none` → **"1 / 4"** ⇒ **4 pages × 9 posts = up to 36 posts total**; the first render shows 9 + 1 featured.
- `a.w-pagination-previous.u-d-none` is present but `display:none` (`.u-d-none{display:none}`).
- `<link rel="prerender" href="?77d76c3c_page=2">` — drop it in the clone.

**Button metrics (measured, @1024).** This is a trap: `.w-pagination-next` sets `font-size:14px` and **wins over `.btn{font-size:1rem}`**, and because `.btn`'s padding and radius are in `em`, everything scales down:

| | `.btn` elsewhere | `.w-pagination-next.btn` |
|---|---|---|
| font-size | 16px | **14px** |
| line-height | 16px | **14px** |
| padding (`.875em 1.25em`) | 14px 20px | **12.25px 17.5px** |
| border-radius (`99em`) | 1584px | **1386px** |
| rendered | — | **110 × 40.5** |

bg `rgb(0,55,62)`, color `rgb(202,255,242)`, `border:1px solid rgba(0,0,0,0)`,
`transition: color .3s cubic-bezier(.165,.84,.44,1), background-color .3s …, border-color .3s …`.
`.w-pagination-wrapper{display:flex;flex-wrap:wrap;justify-content:center}` + `.u-mt-3{margin-top:3em}` → measured `margin-top:48px`.
Hover inherits `.btn:hover{background-color:var(--peach);color:var(--primary)}`.

Webflow's unstyled base (`.w-pagination-next{color:#333;background:#fafafa;border:1px solid #ccc;border-radius:2px;margin-inline:10px;padding:9px 20px;font-size:14px}`) is mostly overridden by `.btn`, but **`margin-inline:10px` and `font-size:14px` survive** — measured `margin:0px 10px`.

### 2.6 CTA band

```css
.container.cc-cta{ background-color:var(--white); border-radius:4.5rem /*72px*/;
  display:flex; flex-direction:column; justify-content:center; align-items:stretch;
  min-height:30rem /*480px*/; padding-block:4rem /*64px*/; overflow:hidden;
  isolation:isolate /* from global embed */ }
.container.cc-narrow.cc-cta-2{ width:85% }
@media (max-width:991px){ .container.cc-cta.cc-wide-cta{ justify-content:flex-start; padding-bottom:39% } }
@media (max-width:767px){ .container.cc-cta{ border-radius:2rem /*32px*/; min-height:auto; padding:2rem 2rem 11rem }
                          .container.cc-cta.cc-wide-cta{ padding-bottom:41% }
                          .container.cc-narrow.cc-cta-2{ width:100% } }
@media (max-width:479px){ .container.cc-cta{ padding-bottom:13.3rem } }

.cta-image-wrapper{ z-index:1; position:absolute; inset:0; width:100%; height:100%;
                    display:flex; justify-content:flex-end; align-items:center }
.cta-image-contain{ width:33% }
.cta-image-contain.cc-extra-wide{ width:50% }
.cta-image-aspect{ width:100%; padding-top:141%; position:relative; overflow:hidden }
.cta-image-aspect.cc-wide{ padding-top:75% }
.cta-image-aspect.cc-extra-wide{ padding-top:62% }
@media (max-width:991px){ .cta-image-wrapper.cc-extra-wide{ justify-content:center; align-items:flex-end }
                          .cta-image-contain{ width:50%; margin-right:-10% }
                          .cta-image-contain.cc-extra-wide{ width:90%; margin-right:0 } }
@media (max-width:767px){ .cta-image-wrapper{ justify-content:space-between; align-items:flex-end; inset:auto 0 0 }
                          .cta-image-contain{ position:absolute; inset:auto 0 0 auto;
                                              margin-bottom:-18%; margin-right:-14% }
                          .cta-image-contain.cc-extra-wide{ width:100%; margin-bottom:0; margin-left:auto } }
@media (max-width:479px){ .cta-image-contain{ width:80%; margin-bottom:-40%; margin-right:-35% }
                          .cta-image-contain.cc-extra-wide{ margin-right:-11% } }
.shape-contain.cc-cta{ width:55%; display:none }   /* ≤767 → display:block, see note */
```

Measured:

| | @1440 | @1024 | @390 |
|---|---|---|---|
| wrapping `div.section` | `padding:80px 0`, rect `0,2960 1440×640` | `80px 0` | `48px 0` |
| `.container.cc-cta.cc-wide-cta` | `72,3040 1296×480`, pad `64px 0`, r **72px**, min-h 480px | `51.2,… 921.59×480`, pad `64px 0`, r 72px | `19.5,… 351×380.29`, pad **`32px 32px 159.898px`**, r **32px**, min-h auto |
| `.container.cc-narrow.cc-cta-2` | `169,3161 1102×238` (85%) | — | `51.5,… 287×188.39` |
| `h2.h3.u-mb-0` | **56px/56px w600** mb 0 | 56/56, w=303.06 | **28.8px/28.8px w600** |
| `a.btn` "Book kidcare" | `144.41×46`, pad 14/20, r1584, bg primary, fg celeste | same | same |
| `.cta-image-contain.cc-extra-wide` | `720,3079 648×402` (50%) | `460.8` wide, 285.69 tall | `351` wide (100%), `217.62` tall, `margin-right:-38.61px` (−11% of 351) |
| `.cta-image-aspect` padding-top | 62% → 402px | 285.688px | 217.617px |

Note the `padding-bottom:41%` at ≤479 resolves against the **parent** `.section` width: 41% × 390 = **159.898px** ✓.
The empty `div.col.col-lg-4` after the copy column is a layout spacer (`flex:1 1 33.33%; max-width:33.33%; height:0; margin-bottom:40px`) — keep it or replace with `justify-content` math.
`.shape-contain.cc-cta` exists in CSS (a ≤767 decorative blob) but **is not in this page's DOM** — nothing to build.

### 2.7 The 10 rendered posts (page 1)

Recorded exactly as rendered. **Important: the card template has no excerpt, no date, no author and no read-time slot** — a card is image + tag pills + title only. There is no such data anywhere in the markup (confirmed: no `<time>`, no date/author field, and no deck text on either the cards or the post pages). So "excerpt / date / author" for these posts **does not exist on the original** and must not be invented.

| # | Slug | Title | Tags (`color` token) | Cover image (filename) |
|---|---|---|---|---|
| 1 ★ | `/blog-posts/series-a` | Announcing Otter's Series A | `Featured` (static `div.tag`, celeste) | `…efed_Playing_Colored_01 1.webp` |
| 2 | `/blog-posts/how-to-be-an-amazing-babysitter` | How to be an Amazing Babysitter | Childcare (midnight), Tips (peach) | `…f132_…shutterstock_1770121187.jpeg` |
| 3 | `/blog-posts/infant-care-101` | Infant Care 101 | Childcare (midnight), Tips (peach) | `…f14d_…kelly-sikkema-Z4GKcFAGck4-unsplash.jpeg` |
| 4 | `/blog-posts/toddler-care-101` | Toddler Care 101 | Childcare (midnight), Tips (peach) | `…f15e_…kazuend-ejlRp5ktpfY-unsplash.jpeg` |
| 5 | `/blog-posts/how-to-set-your-sitter-up-for-success` | How to Set Your Sitter Up for Success | Childcare (midnight), Parenting (coral), Tips (peach) | `…f14f_…marisa-howenstine-Cq9slNxV8YU-unsplash.jpeg` |
| 6 | `/blog-posts/otter-featured-in-the-new-york-times` | Otter Featured in the New York Times | Otter news (midnight) | `…f151_…Screen Shot 2022-08-31 at 8.34.51 AM.png` |
| 7 | `/blog-posts/how-to-change-a-diaper` | How to Change a Diaper | Childcare (midnight), Tips (peach) | `…f10b_…zelle-duda-uld7AdE36z4-unsplash.jpeg` |
| 8 | `/blog-posts/tackling-bedtime-routines` | Tackling Bedtime Routines | Childcare (midnight), Tips (peach) | `…f161_mark-zamora-mFqAeaZgWO8-unsplash.jpg` |
| 9 | `/blog-posts/baby-led-bottle-feeding` | Baby-led Bottle Feeding | Childcare (midnight), Tips (peach) | `…f0d6_…lucy-wolski-sljmgxyzmqM-unsplash.jpeg` |
| 10 | `/blog-posts/how-to-set-parents-at-ease-while-babysitting` | How to Set Parents at Ease While Babysitting | Childcare (midnight), Tips (peach) | `…f14c_…kelly-sikkema-4l2Ml8-MLUg-unsplash.jpeg` |

★ = featured variant. Note the featured post (#1) is *also* the first list, so it is not duplicated in the 9-item grid.
Every card `<img>` carries `alt="Kid and sitter playing "` (yes, trailing space) — a single CMS default reused for all of them. Full URLs, intrinsic sizes and srcsets in `ASSETS_blog_legal.md`.

---

## 3. The blog-post template (`/blog-posts/<slug>`)

**This is the key deliverable — 10+ pages render from it.** Measured on `/blog-posts/series-a` and `/blog-posts/infant-care-101`; the two differ only in the CMS-bound slots marked **[slot]**.

### 3.1 Template skeleton

```
div.page-wrapper
  nav.nav_wrapper                                      ← §1.1, no link is w--current
  div.section.u-pb-0                                   ← POST HEADER (note: plain div, not <header>)
    div.container.cc-narrow
      div.row.row-justify-between.row-align-center
        div.col.col-lg-6.col-sm-12
          div.section-header
            h1.h2.u-mb-0                               [slot] post title
            div.w-dyn-list
              div[role=list].blog_item-tags-wrapper.w-dyn-items
                n × div.tag.w-dyn-item[color=…] > div   [slot] tag names
        div.col.col-lg-6.col-sm-12.u-mb-0
          div.b-radius-32
            div.u-aspect-1x1
              img.u-img-cover                          [slot] cover image, alt=""
  main#main
    div.section
      div.container.cc-narrow
        div.row.row-justify-center
          div.col.col-lg-8.col-md-12
            div.blog-rich-text.w-richtext              [slot] post body
    div.section                                        ← RELATED POSTS
      div.container
        h2.h3.u-mb-1  "Similar articles"
        div.w-dyn-list
          div[role=list].row.w-dyn-items[fs-cmsload-element="list"]
            3 × div[role=listitem].col.col-lg-4.col-md-6.col-xs-12.w-dyn-item
                  div.blog_item                        ← identical standard card, §2.3
  footer.section.cc-footer
```

### 3.2 Slots that exist vs. slots that do NOT

Present: **title**, **tag pills** (1–3), **cover image**, **rich-text body**, **3 related posts**.

**Absent — do not build these, there is nothing to bind them to:**
- ❌ subtitle / deck / excerpt line
- ❌ author block (no name, no avatar, no role)
- ❌ publish date (no `<time>` element on the page at all)
- ❌ read-time
- ❌ share links / social buttons
- ❌ breadcrumb or "← Back to blog" link
- ❌ inline CTA block inside the body
- ❌ next/prev post navigation (only the 3-up "Similar articles" grid)

I checked for each of these in the raw HTML of both posts and in the live DOM; none exist. The only navigation away from a post is the nav bar, the related cards, and the footer.

### 3.3 Post header geometry

`div.section.u-pb-0` → `.section{padding-block:5rem}` + `.u-pb-0{padding-bottom:0}`.
Measured padding: **`80px 0 0` @1440 & @1024, `48px 0 0` @390.**

| | @1440 | @1024 | @390 |
|---|---|---|---|
| `.section.u-pb-0` | `0,156 1440×660` | pad `80px 0 0` | pad `48px 0 0` |
| `.container.cc-narrow` | `120,236 1200×580` | `51.2,… 921.59×…` | `19.5,… 351×…` |
| `.row…row-align-center` | `100,236 1240×580`, `align-items:center` | — | `-0.5,… 391×474.38`, still `flex-direction:row` but cols are 100% so they stack |
| copy `.col.col-lg-6` | `100,398.71 620×214.58` (50%) | `31.2,… 480.8×214.58` | `-0.5,… 391×83.38` |
| `.section-header` gap | **24px** | **24px** | **16px** |
| `h1.h2.u-mb-0` | **72px/79.2px w400**, Reckless Neue, ls **−0.72px**, mb 0 | **72px/79.2px w400** | **32px/35.2px w400**, ls −0.32px (derived from `h1{letter-spacing:-.01em}`) |
| tags wrapper | `120,581.1 280.41×32.19`, gap 8px | — | `19.5,… 146.91×32.19` |
| `.tag` | `32.19` tall, pad 5.6/11.2, r8, 14px/21px w500 | same | same |
| image `.col…u-mb-0` | `720,236 620×580` | `532,… 440.8×440.8` | — |
| `.b-radius-32` | `740,236 **580×580**`, r **32px** | `440.8×440.8`, r 32px | `19.5,… **351×351**`, r 32px |

**Cover image treatment**: `div.b-radius-32 > div.u-aspect-1x1 > img.u-img-cover`
```css
.b-radius-32{ border-radius:32px; overflow:hidden }
.u-aspect-1x1{ width:100%; padding-top:100%; position:relative; overflow:hidden }
.u-img-cover { object-fit:contain; width:100%; height:100%; position:absolute; inset:0 }
```
→ **forced 1:1 square, 32px radius at every breakpoint**, image letterboxed inside it (`contain`, not `cover` — matches the homepage primitive). `alt=""`, `loading="lazy"`.
`sizes="(max-width:479px) 90vw, (max-width:767px) 85vw, (max-width:991px) 40vw, 43vw"` (present on series-a; infant-care-101's cover has no `sizes`/`srcset` — Webflow only generates them above a size threshold).

The header **title is `h1.h2`** (so it uses `.h2`'s 4.5rem/1.1 scale, overriding `h1`'s 5rem/1) but keeps `h1`'s `font-family:Reckless Neue` and `letter-spacing:-.01em`, and `.u-mb-0` drops it to **font-weight 400**. Net: Reckless Neue 400, not 900.

### 3.4 The rich-text body — `div.blog-rich-text.w-richtext`

```css
.blog-rich-text{ margin-left:auto; margin-right:auto }   /* no max-width of its own */
.blog-rich-text p  { margin-bottom:1em }
.blog-rich-text h3 { margin-top:4rem }
.blog-rich-text h4 { margin-top:4rem; margin-bottom:.5em }
.blog-rich-text img{ border-radius:16px }
/* from the global <style> embed */
.w-richtext > :first-child { margin-top:0 }
.w-richtext > :last-child, .w-richtext ol li:last-child, .w-richtext ul li:last-child { margin-bottom:0 }
```

**Prose measure** — `.blog-rich-text` has **no `max-width`**; the measure comes entirely from `.col.col-lg-8` inside `.container.cc-narrow` (1200px):

| Width | `.container.cc-narrow` | `.col.col-lg-8` | **`.blog-rich-text` (the measure)** | x |
|---|---|---|---|---|
| 1440 | 1200px | 826.66px | **786.66px** | 326.66 |
| 1024 | 921.59px | 641.06px | **601.06px** | 211.47 |
| 390 | 351px | 391px (100%) | **351px** | 19.5 |

Body section padding: `80px 0` @1440/@1024, `48px 0` @390. The `.col` adds its usual `margin-bottom:40px`.

#### Computed type for every element role

Roles **observed live** in the two sample posts:

| Role | @1440 | @1024 | @390 | Notes |
|---|---|---|---|---|
| `p` (body) | **16px / 24px, w500**, mt 0, **mb 16px** | 16/24 w500 mb16 | 16/24 w500 mb16 | **No class — this is plain `body` type (1rem/1.5 w500), NOT `.paragraph-1-25`.** Identical at all 3 widths. |
| `h3` | **56px / 67.2px, w600**, **mt 64px**, mb **16.8px** | 56/67.2, mt64, mb16.8 | **28.8px / 34.56px w600**, mt **64px**, mb 8.64px | `mt` is the flat `4rem` from `.blog-rich-text h3` (not em-scaled, so it does **not** shrink on mobile). `mb` is `h3{margin-bottom:.3em}`. Family Jokker. |
| `strong` | w**700**, inherits parent size | same | same | Inside an `h3` it computes 56px/67.2px **w700** — the authors wrap every `h3` label in `<strong>`, which bumps 600→700. Reproduce that. |
| `em` | italic, 16px/24px w500 | same | same | |
| inline `a` | 16px/24px **w500**, `color:var(--primary)`, `text-decoration:none`, `display:inline` | same | same | **Links in the prose are visually identical to body text — no underline, no colour change.** See hover note below. |
| `br` | — | — | — | Used heavily (see "fake lists" below). |

Roles **declared in CSS but absent from both sample posts** — I could not measure these live, so these are the rules that *would* apply, read straight out of the compiled stylesheet. **Flagged as underived: confirm against a post that actually uses them before trusting the numbers.**

| Role | Applicable CSS | Computed would-be |
|---|---|---|
| `h2` | `h2{font-size:4.5rem;line-height:1;font-weight:600;margin:0 0 .4em}`; ≤991 3.5rem; ≤767 3rem; ≤479 2rem + `mb .5em` | 72px/72px @1440; 32px/32px @390. **No `.blog-rich-text h2` margin-top rule exists**, so an `h2` would get **mt 0** — unlike `h3`/`h4` which get 4rem. |
| `h4` | `h4{font-size:2.5rem;line-height:1.1;font-weight:600}` + `.blog-rich-text h4{margin-top:4rem;margin-bottom:.5em}` | 40px/44px, mt 64px, mb 20px @1440; 20px/24px, mt 64px, mb 10px @390 |
| `ul` / `ol` | `ul,ol{margin-top:0;margin-bottom:1em;padding-left:2.2em}` + `.w-richtext ol,.w-richtext ul{overflow:hidden}` | **indent 35.2px** (2.2em × 16px), mb 16px |
| `li` | `li{margin-bottom:.3em}` | mb 4.8px; last-child mb 0 (global embed) |
| markers | no `list-style-type` override anywhere | `ul` → **disc**, `ol` → **decimal**, `list-style-position:outside` (browser default) |
| `blockquote` | `blockquote{border-left:5px solid #e2e2e2;margin:0 0 10px;padding:10px 20px;font-size:18px;line-height:22px}` | **This is unstyled Webflow boilerplate** — grey 5px left rule, 18px/22px. Almost certainly not intended by the designer; flag it rather than shipping it blindly. |
| `img` | `img{max-width:100%;display:inline-block}` + `.blog-rich-text img{border-radius:16px}` + `.w-richtext figure img{width:100%}` | **16px radius**, fluid to the 786.66/601.06/351px measure |
| `figure` | `.w-richtext figure{max-width:60%;position:relative}`; `.w-richtext-align-fullwidth{width:100%;max-width:100%;margin-inline:auto;text-align:center}`; `…-align-center{margin-inline:auto}`; `…-align-floatleft{float:left;margin-right:15px}`; `…-align-floatright{float:right;margin-left:15px}` | default inline figure capped at **60% of the measure** (471.99px @1440) |
| `figcaption` | `figcaption{text-align:center;margin-top:5px}`; `.w-richtext figure[data-rt-type=image]>figcaption{caption-side:bottom;display:table-caption}` | centred, mt 5px, inherits 16px/24px w500 |
| embedded video | `.w-richtext figure[data-rt-type=video]{width:60%;height:0}` + `>div{width:100%}` + `iframe{position:absolute;inset:0 auto auto 0;width:100%;height:100%}` | responsive iframe, 60% of measure. **Zero `<iframe>`s on either sample post.** |
| `hr` | `hr{box-sizing:content-box;height:0}` only | **no custom styling at all** — would render as the browser default rule |

#### Vertical rhythm between consecutive block types (measured)

Margins do **not** collapse into anything surprising — `p` has `mb 16px / mt 0`, `h3` has `mt 64px / mb 16.8px`:

| Sequence | Gap @1440 | Gap @390 |
|---|---|---|
| `p` → `p` | **16px** | 16px |
| `p` → `h3` | 16 + 64 = **80px** | 80px |
| `h3` → `p` | **16.8px** | 8.64px |
| `h3` → `h3` | 16.8 + 64 = **80.8px** | 72.64px |
| first child | `margin-top:0` forced by the global embed | same |
| last child | `margin-bottom:0` forced by the global embed | same |

Observed child sequence on `/blog-posts/infant-care-101` (26 children): 22 × `p`, 3 × `h3`, 1 × trailing `p`.
On `/blog-posts/series-a` (14 children): 14 × `p` only.

#### ⚠️ Lists in the body are faked with `<br>`, not `<ul>`

Neither sample post contains a single `<ul>`, `<ol>` or `<li>`. "Bulleted" passages are authored as one `<p>` with literal `" - "` prefixes separated by `<br/>`. Same pattern on the legal pages (§5). Build the real list CSS anyway (cheap, and later posts may use it), but **do not "fix" the source by converting these to semantic lists** if you are porting body HTML verbatim — it will change the vertical rhythm.

Empty spacer paragraphs containing only a zero-width non-joiner (`&zwnj;`) are used as manual vertical gaps, and `* * *` on its own line as a section divider. Both are content, not styling.

### 3.5 Related posts — "Similar articles"

```
div.section > div.container
  h2.h3.u-mb-1  "Similar articles"
  div.w-dyn-list > div[role=list].row.w-dyn-items[fs-cmsload-element="list"]
    3 × div.col.col-lg-4.col-md-6.col-xs-12.w-dyn-item > div.blog_item
```

- Cards are the **standard `.blog_item`** from §2.3, byte-for-byte the same markup (image → tags → `h3.h4.u-mb-0` → `.u-link-cover`). Same 32px/16px radii, same 4:3 aspect, same tag tokens, same no-hover.
- Container is the **wide `.container`** (1296px @1440), *not* `.cc-narrow` — so the related grid is wider than the prose above it. Deliberate; keep it.
- Column classes differ slightly from `/blog`: `col-xs-12` instead of `col-sm-12` (same practical result).
- `fs-cmsload-element="list"` is present but there is **no pagination button**, so Finsweet does nothing here.
- Exactly 3 items, no "view all" link.

| | @1440 | @1024 | @390 |
|---|---|---|---|
| `div.section` | `0,2832 1440×856.18`, pad `80px 0` | pad `80px 0` | pad `48px 0` |
| `.container` | `72,2912 1296×696.18` | 921.59px | 351px |
| `h2.h3.u-mb-1` | **56px/56px w600, mb 56px** | 56/56, mb **56px** | **28.8px/28.8px w600, mb 8.64px** |
| `.col` x / w | 72 / 445.33 (3-up) | 31.2 / 351.73 / 672.25, w 320.52 | −0.5, w 391 (1-up) |
| `.blog_item` | 405.33 wide | 280.52 | 351 |
| `h3.h4` | 40px/44px w600 | 40/44 | 20px/24px w600 |

**`.u-mb-1` cascade gotcha**: `.u-mb-1{margin-bottom:1em}` wins at >991 (→ 56px), but at ≤991 the later media rule `@media(max-width:991px){.h3{margin-bottom:.3em;font-size:2.5rem}}` **overrides it** → mb becomes `.3em` (8.64px at 390). Measured and confirmed at both widths. Don't hardcode `1em`.

---

## 4. `/terms-of-use` and `/privacy-policy`

Both pages are structurally identical. **They are *not* rich-text** — the body is hand-authored Webflow divs, so there is no `.w-richtext` prose block and none of §3.4 applies.

### 4.1 Skeleton

```
div.page-wrapper
  nav.nav_wrapper                           ← §1.1, no w--current
  div.section.u-pb-0                        ← page title band
    div.container                           ← NOTE: plain .container, NOT .cc-narrow
      div.row.row-justify-center
        div.col.col-lg-8.col-md-12
          div.section-header
            h1.u-mb-0                       "Terms of use" / "Privacy Policy"
  main#main
    div.section
      div.container
        div.row.row-justify-center
          div.col.col-lg-8.col-md-12
            div                             ← intro block ("last updated")
              div.eyebrow.u-mb-1            (terms)   ← a DIV
              h2.eyebrow.u-mb-1             (privacy) ← an H2  ⚠ differs
              p                             (privacy only: intro paragraph)
            n × div                         ← one wrapper div per section
              div.splitter                  ← 1px rule
              h3.h4                         section heading
              p                             section body (with <br> runs)
  footer.section.cc-footer
```

**The two pages differ in exactly one markup detail**: the "Effective date" line is a `div.eyebrow.u-mb-1` on `/terms-of-use` but an `h2.eyebrow.u-mb-1` on `/privacy-policy`. Same computed styling either way.

### 4.2 Measured geometry & type scale

Container is the **wide `.container`** (90% / max 90rem), and the prose column is `col-lg-8` of *that* — so the legal measure is **wider than the blog post measure**:

| | @1440 | @1024 | @390 |
|---|---|---|---|
| title `div.section.u-pb-0` padding | `80px 0 0` | `80px 0 0` | `48px 0 0` |
| `main .section` padding | `80px 0` | `80px 0` | `48px 0` |
| `.container` | `72,… 1296px` | `51.2,… 921.59px` | `19.5,… 351px` |
| `.col.col-lg-8.col-md-12` | `274.66,… **890.66px**` (66.67%) | `191.47,… **641.06px**` | `−0.5,… **391px**` (100%) |
| **prose measure** (`.splitter`/`h3`/`p` width) | **850.66px** | **601.06px** | **351px** |
| `.section-header` gap | 24px | 24px | 16px |
| `h1.u-mb-0` | **80px/80px w400** ls −0.8px Reckless Neue, mb 0 | **80px/80px w400** | **48px/48px w400** ls −0.48px |
| `.eyebrow.u-mb-1` | **14px/19.6px w600**, ls **0.49px**, **uppercase**, mb **14px** | same | same |
| `h3.h4` (section heading) | **40px/44px w600**, mt 0, mb **24px** | 40px/44px, mb 24px | **20px/24px w600**, mb **12px** |
| `p` (body) | **16px/24px w500**, mt 0, mb **16px** | same | same |
| `a` inline | 16px/24px w500, `#00373e`, no underline | same | same |
| `em` | italic 16px/24px w500 | same | same |
| `strong` | **w700**, inherits context (inside `.eyebrow` → 14px/19.6px uppercase ls .49px w700) | same | same |

So the legal **type scale is the ordinary marketing scale** — `h1` at the base 5rem, section headings via the `.h4` class (2.5rem), body at base `1rem/1.5`. The *only* legal-specific primitive is `.splitter`.

```css
.splitter{ background-color:var(--primary); width:100%; height:1px;
           margin-top:3em; margin-bottom:3em }   /* 48px/48px at 16px base */
.eyebrow{ letter-spacing:.035em; text-transform:uppercase;
          font-size:.875em; font-weight:600; line-height:1.4 }
.u-mb-1{ margin-bottom:1em }
.u-pb-0{ padding-bottom:0 }
```

**Section rhythm (measured, one block):**
```
div.splitter   mt 48px  mb 48px   h=1px   bg #00373e
h3.h4          mt 0     mb 24px   40px/44px w600
p              mt 0     mb 16px   16px/24px w500
```
→ gap from the end of one section's text to the next heading = 16 (p mb) + 48 (splitter mt) + 1 + 48 (splitter mb) = **113px** @1440.
The intro block has **no** `.splitter`; the first splitter appears above section 1.
`.u-mb-1` on the eyebrow resolves to **14px** (1em of its own 14px font-size), not 16px.

### 4.3 Table of contents / jump links / anchors — effectively none

- **No table of contents and no jump-link list** on either page.
- `/terms-of-use`: **no `id` attributes at all** inside `<main>`. 3 × `href="#"` links exist but they are **placeholders pointing nowhere** (verified: `document.querySelector('#')` → nothing; one of them is labelled "www.jamsadr.com" and should probably be a real external URL, but on the original it is `#`).
- `/privacy-policy`: exactly **one** anchor target, `<strong id="information-we-collect-automatically">`, and a link in a later section whose label references that section — but **its `href` is `"#"`, not `"#information-we-collect-automatically"`. The anchor is orphaned; the link is broken on the live site.** Reproduce as-is, or fix it and note the deviation.
- `scroll-behavior: auto` on `<html>` — **no smooth scrolling**.

### 4.4 "Last updated" treatment

Both pages open with an uppercase eyebrow reading **"Effective date: October 10, 2021"** (same date on both), styled as `.eyebrow.u-mb-1` → 14px/19.6px, w600, `letter-spacing:0.49px`, `text-transform:uppercase`, `margin-bottom:14px`, colour `--primary`. No icon, no border, no background.
On `/terms-of-use` the same block continues into an all-caps `<strong>` legal notice (arbitration/jury-waiver warning) which inherits the eyebrow's uppercase + 14px, bumped to **w700** by `strong`. That is why a 14px uppercase run appears to dominate the top of the terms page — it is the eyebrow div, not a separate style.

### 4.5 Nested list styling — not applicable

**There are zero `<ul>`, `<ol>`, `<li>` and zero `<table>` elements on either page** (counted in the live DOM: `ul:0 ol:0 table:0`). Every list is faked inside a `<p>` with `" - "` prefixes and `<br/>` separators (`/terms-of-use` has **189 `<br>` elements**). There is consequently **no nested-list styling to port** — nesting is expressed only by the authors' leading spaces in the text.
If you port the DOM verbatim this is free. If you convert to semantic lists you must re-derive the rhythm yourself (the base rules would be `padding-left:2.2em`, `li{margin-bottom:.3em}`, disc/decimal markers).

### 4.6 Section heading lists

Body copy should be **ported from the live DOM at build time** — not transcribed here. These are the `h3.h4` headings in document order, which is all you need to scaffold the pages.

`/terms-of-use` — `h1` "Terms of use", then 25 sections (25 `.splitter`s):
1. Acceptance of Terms · 2. The Otter Platform · 3. Eligibility · 4. Account Creation · 5. Rules and Prohibitions · 6. User Content · 7. Notice and Procedure for Making Claims of Copyright Infringement · 8. Feedback · 9. Bookings, Fees, and Taxes · 10. Cancellations, Care Access Issues, Refunds, and Booking Modifications · 11. Additional Obligations of Sitters · 12. Additional Obligations of Parents · 13. Reviews · 14. Term and Termination · 15. Indemnity and Release · 16. Disclaimers · 17. Limitation of Liability · 18. Arbitration and Class Action Waiver · 19. Venue and Governing Law · 20. Links · 21. Application License · 22. General · 23. Contact Us · 24. iOS Terms · 25. California Civil Code § 1812.5095

`/privacy-policy` — `h1` "Privacy Policy", then 12 sections (12 `.splitter`s):
1. The information we collect · 2. How We Use the Information We Collect · 3. When Otter Shares Your Information · 4. Online Analytics and Tailored Advertising · 5. Children's privacy · 6. Security of Your Information · 7. Links to External Sites and Services · 8. Your Choices · 9. California Do-Not-Track Disclosure · 10. Consent to Transfer · 11. Changes to This Privacy Policy · 12. Contact Us

Outbound links inside the legal copy (port verbatim): `https://withotter.com/privacy` (note: **not** `/privacy-policy` — a dead link on the original), `http://help.withotter.com/`, `https://help.withotter.com/hc/en-us/articles/4410166870413-Cancellations`, `https://help.withotter.com/hc/en-us/categories/4410166453645-Parent-Handbook`, `https://stripe.com/connect-account/legal`, `https://stripe.com/legal`, `https://tools.google.com/dlpage/gaoptout`, `http://www.networkadvertising.org/choices`, `http://www.aboutads.info/choices`, `https://www.google.com/settings/ads`, `https://www.aap.org/en/patient-care/safe-sleep/`.

---

## 5. New type roles & utility/variant classes (not in homepage spec §4)

All measured. Sizes given as @1440 / @1024 / @390.

| Role | Selector | @1440 | @1024 | @390 |
|---|---|---|---|---|
| Blog list H1 | `h1.u-mb-0` | 80px/80px **w400** ls −0.8px Reckless | 80/80 w400 | 48/48 w400 ls −0.48px |
| Legal H1 | `h1.u-mb-0` | identical to above | identical | identical |
| Post H1 | `h1.h2.u-mb-0` | **72px/79.2px w400** ls −0.72px Reckless | 72/79.2 w400 | **32px/35.2px w400** |
| Featured card title | `h3.h3` | 56px/67.2px w600 mb16.8 | same | 28.8/34.56 w600 mb8.64 |
| Card title | `h3.h4.u-mb-0` | 40px/44px w600 mb0 | same | 20px/24px w600 |
| Section H2 (CTA) | `h2.h3.u-mb-0` | 56px/56px w600 mb0 | same | 28.8/28.8 w600 |
| "Similar articles" | `h2.h3.u-mb-1` | 56px/56px w600 **mb56** | same | 28.8/28.8 **mb8.64** |
| Legal section head | `h3.h4` | 40px/44px w600 mb24 | same | 20px/24px w600 mb12 |
| Rich-text H3 | `.blog-rich-text h3` | 56px/67.2px w600 **mt64** mb16.8 | same | 28.8/34.56 **mt64** mb8.64 |
| Rich-text body | `.blog-rich-text p` | 16px/24px **w500** mb16 | same | same |
| Legal body | `main p` | 16px/24px w500 mb16 | same | same |
| Blog hero lede | `p.paragraph-1-25.u-mb-0` | 20px/30px w500 mb0 | same | 16px/24px w500 |
| Eyebrow / last-updated | `.eyebrow.u-mb-1` | 14px/19.6px w600 ls0.49 upper mb14 | same | same |
| Tag pill | `.tag` | 14px/21px w500, pad 5.6/11.2, r8 | same | same |
| Nav link | `.nav_link` | 16px/24px w500 pad 8px 0 | same | 24px/36px (`1.5em`) pad 0, w100% |
| Footer link | `.footer_link a` | 16px/24px w500, inline | same | same |
| Load-more pill | `.w-pagination-next.btn` | 14px/14px w600, pad 12.25/17.5, r1386 | same (110×40.5) | same |

New utility / variant classes:

```css
.u-p-0   { padding:0 }                /* + @media(max-width:991px){.section.u-p-0{padding-block:0}} */
.u-pb-0  { padding-bottom:0 }
.u-mb-1  { margin-bottom:1em }
.u-mb-2  { margin-bottom:2em }        /* 32px */
.u-mt-3  { margin-top:3em }           /* 48px */
.u-d-none{ display:none }
.u-mb-0  { margin-bottom:0; font-weight:400 }   /* ⚠ also sets weight */
.b-radius-32{ border-radius:32px; overflow:hidden }
.splitter{ background-color:var(--primary); width:100%; height:1px; margin-block:3em }
.row.row-align-center{ align-items:center }
.container.cc-narrow.cc-cta-2{ width:85% }   /* ≤767 → 100% */
.w-page-count{ text-align:center; width:100%; margin-top:20px }
```

Variant classes on existing components: `.blog_item.cc-featured`, `.blog_item-image.cc-featured`, `.blog_item-image-aspect.cc-featured`, `.blog_heading-wrapper.cc-featured`, `.container.cc-cta`, `.container.cc-cta.cc-wide-cta`, `.cta-image-contain.cc-extra-wide`, `.cta-image-aspect.cc-extra-wide` (+ `.cc-wide`), `.tag[color=…]`, `.nav_link.w--current`.

Declared but **not present in any of these pages' DOM** — skip: `.shape-contain.cc-cta`, `.cta-image-aspect.cc-wide`, `.cta-image-contain` (non-extra-wide), `.eyebrow.tag`, `.subhead.u-mb-1`, `.subhead.u-mb-0`, `.styles__nav-link.cc-cta`, `.swiper-contain`, `.swiper-slide:nth-child(5n+…)` colour loop, `.tab-*` classes, `.card.u-pb-0`.

---

## 6. Motion

**Engine is still Webflow IX2. No GSAP, no IntersectionObserver in site code, no scroll listeners beyond IX2's own.**

IX2 ships **37 defined events** on each of these pages. I matched every event's target (`selector` or `data-w-id`) against the live DOM on `/blog`, `/blog-posts/series-a` and `/privacy-policy`. On all three, exactly **two** events have a live target:

| Event | Type | Target | Media queries | Config |
|---|---|---|---|---|
| `e-13` | `MOUSE_CLICK` | `a.nav_mobile-btn.w-inline-block` (`data-w-id="e9e5205a-cbfa-d6b9-11fc-6e90b3191d6d"`) | `medium`, `small`, `tiny` (≤991 only) | `loop:false, playInReverse:false, delay:null, scrollOffset:null` |
| `e-14` | `MOUSE_SECOND_CLICK` | same element | `medium`, `small`, `tiny` | same |

These are the **mobile nav open / close** pair — functionally and parametrically the same interaction the homepage exposes as `e-41`/`e-42`. **Reuse homepage spec §7.2 and §7.3 verbatim** (full action-list tables: 300/400ms items, `outQuart` = `cubic-bezier(0.165,0.84,0.44,1)`, 200ms stagger delays, ≈600ms open / ≈500ms close, plus the inline jQuery that forwards an overlay click to the button).

### What does NOT animate

- **No scroll-reveal anywhere on blog or legal.** The homepage's `e-31` / `slideInBottom` targets `.section-header.cc-tabas-header`, which is **not in any of these pages' DOM**. Confirmed independently: **zero elements carry an inline `opacity:0`** on `/blog-posts/series-a` (Webflow's tell-tale for an IX2 initial state).
- **No card hover transitions** — see §2.3. Computed `transition` on `.blog_item`, `.u-link-cover` and card images is `all 0s ease 0s`.
- **No carousels.** `document.querySelectorAll('.swiper').length === 0` on every one of these routes, though `swiper-bundle.min.js` is still loaded. Do not ship Swiper.
- **No marquees, no `<video>`, no `<iframe>`, no canvas.**
- No `scroll-behavior:smooth`.

### Real CSS transitions on these pages (complete list — only two)

```css
/* 1. buttons, incl. the Load-more pill */
.btn{ transition: color .3s cubic-bezier(.165,.84,.44,1),
                  background-color .3s cubic-bezier(.165,.84,.44,1),
                  border-color .3s cubic-bezier(.165,.84,.44,1) }
.btn:hover{ background-color:var(--peach); color:var(--primary) }

/* 2. NEW on these pages — the nav current/hover icon */
.nav_link-current-icon{ transition: opacity .3s cubic-bezier(.165,.84,.44,1),
                                    transform .3s cubic-bezier(.165,.84,.44,1);
                        opacity:0; transform:translateY(100%) }
@media screen and (min-width:992px){
  .nav_link.w--current .nav_link-current-icon,
  .nav_link:hover      .nav_link-current-icon{ opacity:1; transform:translateY(0) }
}
```
Trigger: hover (and permanent on the current route), **300ms, `outQuart`, no delay, no stagger**, desktop-only (≥992px).
Everything else — `.btn.cc-white` box-shadow, `:active` scale(.95), focus rings — is unchanged from homepage spec §7.4.

---

## 7. Clip-path / organic shapes

**No new shapes.** The only `clip-path` consumers in the blog/legal DOM are the two footer blobs, identical to the homepage:

```css
.footer-shape-left { width:100%; height:100%; clip-path:url(#footer-shape-left) }
.footer-shape-right{ width:100%; height:100%; clip-path:url(#footer-shape-right) }
```
Verified computed on `/blog-posts/series-a`: `.shape.footer-shape-left.u-bg-olive → url("#footer-shape-left")`, `.shape.footer-shape-right.u-bg-peach → url("#footer-shape-right")`.

The hidden `div.styles__global-embed-code.w-embed` block still ships **all seven** `<clipPath>` defs (5 hero stones + 2 footer) on every page, even though the five hero stones are unused here. Keep the shared hidden SVG def block; take the path `d` strings verbatim from **homepage spec §5** — they are byte-identical and are not duplicated in this document.

(There is also an unrelated `url("#clip0_254_628")` on two `<svg>` internals — that is the Otter wordmark's own internal clip, part of the inline logo SVG, not a layout shape.)

---

## 8. Third-party scripts (do NOT port)

Same stack as the homepage — jQuery 3.5.1, three Webflow chunks, Swiper 9, WebFont loader, GTM/gtag (`G-MQF6KJPCXL`, `G-2NVK8NS1G0`, `AW-10801161001`), FB Pixel, Nextdoor, FullStory, Amplitude — **plus one new entry**:

```
https://cdn.jsdelivr.net/npm/@finsweet/attributes-cmsload@1/cmsload.js
```

This is the only third-party script that does real work on these routes (the `/blog` Load-more). Implement load-more natively instead of porting it.

## 9. URL hygiene

`app.withotter.com` links carry a per-session `device-id` query param that differs on every load. **Hardcode the bare URLs:**

| Link | Use |
|---|---|
| `https://app.withotter.com/log-in` | nav "Log in" (`target=_blank`) — on these pages the raw href already has **no** `device-id` |
| `https://app.withotter.com/sign-up/welcome` | nav "Sign up" (`target=_blank`) — live href had `?device-id=NJ1fbftABJ6d8pzJ9Oix9n`, strip it |

Internal links to keep: `/`, `/parents`, `/sitters`, `/trust-safety`, `/blog`, `/faq`, `/careers`, `/contact`, `/terms-of-use`, `/privacy-policy`, `/blog-posts/<slug>`, `#main`.
Known-broken on the original (reproduce or fix deliberately): `/blog` CTA `href="#"`; legal `href="#"` × 3; `https://withotter.com/privacy` (should be `/privacy-policy`); some in-body post links use the old `/post/<slug>` prefix instead of `/blog-posts/<slug>`.
