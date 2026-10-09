Source: https://app.withotter.com/log-in (also /sign-up, /sign-up/welcome → /welcome)

# Otter App — Auth Screens Build Spec

> ## ⚠️ THE CLONE OF THESE SCREENS MUST BE INERT
> These are a real service's live authentication screens. The rebuild is **layout and styling only**:
> - **No credential collection.** Render the inputs, but never persist, log or transmit what is typed.
> - **No network submission.** The `<form>` must have **no `action`**, no `method`, and an `onSubmit` that calls `e.preventDefault()` and does nothing else (or use a plain `<div>` instead of `<form>`).
> - **No password manager integration.** Strip the real `autocomplete` values from the clone (use `autocomplete="off"`); the live values are recorded below only as a structural fact of the original, not as something to reproduce.
> - **No auth endpoints.** Do not point anything at `api.withotter.com`. Buttons should be visually interactive but functionally dead (or navigate between local static routes).
> - There are **no password fields and no social-auth buttons** on any of the three screens (see §8), so there is nothing credential-shaped to clone beyond a phone number and two name fields.

Measured live with Playwright on 2026-10-08 at **1440×900**, **1024×900** and **390×844**, in a fresh session with no cookies.
Reference stylesheet downloaded for rule extraction: `https://app.withotter.com/assets/index-kszxQpln.css` (204,769 bytes).
Reference JS bundle inspected for the route table: `https://app.withotter.com/assets/index-3SWImSlZ.js` (1,256,322 bytes).
Asset manifest: `/Users/riyaghosh/V3/otter/spec/ASSETS_auth.md`

The `device-id` query param that the app appends is per-session garbage and has been stripped from everything recorded here.

---

## 0. Reachability and gating

| URL | HTTP | Renders? | Session required? |
|---|---|---|---|
| `https://app.withotter.com/log-in` | **200** | Yes, fully | **No** |
| `https://app.withotter.com/sign-up` | **200** | Yes, fully | **No** |
| `https://app.withotter.com/sign-up/welcome` | **200** (SPA shell) | **No — client-side redirects to `/welcome`** | **No** |

All three are publicly reachable and render without a session. **Nothing on these screens was auth-gated or unmeasurable.** All HTTP 200s are the same 2,907-byte SPA shell (`Content-Length: 2907`, `Server: Vercel`, `X-Vercel-Cache: HIT`); routing happens entirely client-side in React Router.

### `/sign-up/welcome` is not a real route

The route table in the JS bundle has **no `sign-up/welcome` entry**. The real routes under the sign-up tree are `sign-up` and `sign-up/record-interest`. `welcome` is a **top-level sibling route** (`{ landing: { title:"Welcome", path:"welcome" } }`). So `/sign-up/welcome` falls through to the `path:"*"` catch-all, whose element is a guard component (`()=>{const e=kt({requireSignedUp:!1}) …}`) that redirects. Observed behaviour: browser URL rewrites `/sign-up/welcome` → `/welcome`, `document.title` becomes `Otter | Welcome`.

### What `/welcome` actually is

It is **not** a post-signup confirmation and **not** an email-verification prompt. It is the **sitter-facing unauthenticated landing / route-chooser screen**: a hero illustration, `h1` "Welcome to Otter", the sub-line "We want to get you the job and the pay you deserve.", a primary **Log in** button, and a "Don't have an account? **Apply now**" line. It renders standalone with no session and does **not** redirect away when visited cold. Both of its actions are `onClick` navigations (not `href`s) into `/log-in` and `/sign-up` respectively.

---

## 1. The stack — and the one big caveat

**Not Webflow.** This is a **Vite-built React SPA hosted on Vercel**, entirely separate from the marketing site.

| Signal | Value |
|---|---|
| Host / CDN | Vercel (`Server: Vercel`, `X-Vercel-Id`, `X-Vercel-Cache: HIT`) |
| Build tool | Vite (`<script type="module" crossorigin src="/assets/index-3SWImSlZ.js">`, single hashed CSS bundle) |
| Framework | React 18 + React Router (client-side route table with `path:"*"` catch-all) |
| **Design system** | **Mantine v7** — this is the single most important finding. See §1.1. |
| Mount point | `<div id="root"></div>` |
| Toasts | `react-toastify` (`<div class="Toastify">` present but empty on all three screens) |
| Env (from bundle) | `VITE_APP_WEB_DOMAIN: "app.withotter.com"`, `VITE_APP_DOMAIN: "api.withotter.com"` |
| Third-party scripts in `index.html` | HubSpot (`js.hs-scripts.com/21078882.js`), Meta Pixel (`connect.facebook.net/en_US/fbevents.js`), Google Identity Services (`accounts.google.com/gsi/client`), Google Maps Places (`maps.googleapis.com/maps/api/js?...&libraries=places`), LaunchDarkly (`VITE_APP_LD_CLIENTSIDE_ID`) |

### These screens are NOT a third-party hosted auth widget

**Confirmed: there is no Auth0 / Clerk / Firebase / Cognito hosted widget involved.** The forms are first-party React components built from Mantine primitives, rendered into Otter's own `#root`. The rebuild is a normal "clone a page" job, not a "style a vendor widget" job.

Caveat worth flagging: `accounts.google.com/gsi/client` **is** loaded by `index.html` on every route, so Google Sign-In exists somewhere in the app — but **no GSI button is rendered on any of the three screens measured** (`document.querySelectorAll('svg').length === 0`; no `<iframe>`; no provider marks). Don't build one.

### 1.1 Shared vs new design system

| Thing | Marketing site (`withotter.com`) | App (`app.withotter.com`) | Verdict |
|---|---|---|---|
| Platform | Webflow + jQuery + IX2 | Vite + React 18 + **Mantine v7** | **New** |
| Font families | Jokker 400/500/600, Reckless Neue 900 | **Same two families**, self-hosted from the app's own bundle | **Shared** (see §2 for the live-site font bug) |
| Brand hexes | `#00373e`, `#cafff2`, `#fbd3b6`, `#f8f6f5`, `#94954c`, `#fbad9c`, `#ac9e88` | **All seven present**, re-mapped into named Mantine 10-step scales | **Shared values, new token names** |
| Token mechanism | 7 flat `:root` custom props | **~200 `--mantine-color-*` custom props** injected in a runtime `<style data-mantine-styles="true">` | **New** |
| Grid | `.container { width:90%; max-width:90rem }` | Mantine `Container` sizes: xs 540 / sm 720 / md 960 / lg 1140 / xl 1320, `padding-inline:16px`, `margin-inline:auto` | **New** |
| Breakpoints | Webflow max-width 991 / 767 / 479 | Mantine min-width em: xs 36em / sm 48em / md 62em / lg 75em / xl 88em | **New** |
| Spacing scale | ad-hoc | `xs 4 / sm 8 / md 16 / lg 32 / xl 48` px | **New** |
| Radius scale | ad-hoc | `sm 12 / md 16 / lg 24` px, default 16; **buttons override to 999px** | **New** |
| Body line-height | 1.5 | **1.55** (`24.8px` at 16px) | **New** |

**Do not reuse the marketing site's Tailwind config, container or breakpoints for these screens.** Reuse only the font files (already in the repo) and the brand hexes.

---

## 2. Fonts

### Declared `@font-face` (from the app's own CSS bundle)

All six are declared with `format("woff")` and `font-display:swap`, at URLs relative to the stylesheet (`/assets/index-kszxQpln.css`), i.e. resolving to `/assets/art/fonts/…`:

| Family | Weight | Style | Declared URL (resolved) |
|---|---|---|---|
| Jokker | 400 | normal | `https://app.withotter.com/assets/art/fonts/Jokker-Regular.woff` |
| Jokker | 400 | italic | `.../Jokker-RegularItalic.woff` |
| Jokker | 500 | normal | `.../Jokker-Medium.woff` |
| Jokker | 500 | italic | `.../Jokker-MediumItalic.woff` |
| Jokker | 600 | normal | `.../Jokker-Semibold.woff` |
| Reckless Neue | 900 | normal | `.../RecklessNeue-Heavy.woff` |

### ⚠️ On the live site these font files 404 — the original renders in fallback fonts

Every one of those six URLs returns **HTTP 200 with the 2,907-byte `index.html` SPA shell** (`Content-Length: 2907`), not a font. Vercel's SPA rewrite swallows the path. Consequences, measured:

```
document.fonts →  Jokker 600 normal  => "error"
                  Reckless Neue 900  => "error"
                  Jokker 400/500     => "unloaded"
document.fonts.check('600 16px Jokker')            → false
document.fonts.check('700 48px "Reckless Neue"')   → false
```

So the live screens render:
- body / inputs / labels / buttons in `Jokker, sans-serif` → **the system sans-serif fallback**;
- the `h1` in `font-family: "Reckless Neue"` **with no fallback declared** → the browser's **default serif** (Times).

**Build decision: fix it.** Use the real fonts — they are already vendored at `/Users/riyaghosh/V3/otter/public/fonts/` (`Jokker-Regular.woff`, `Jokker-Medium.woff`, `Jokker-Semibold.woff`, `Jokker-RegularItalic.woff`, `Jokker-MediumItalic.woff`, `RecklessNeue-Heavy.woff`). Screenshots of the original will look serif-y in the `h1`; that is the bug, not the design intent. Note that `Reckless Neue` is declared at weight **900** but requested by the `h1` at **700** — the browser synthesises. Keep `RecklessNeue-Heavy.woff` and let `font-weight:700` map onto it, or declare the face at 700 directly.

### Stacks

```css
--mantine-font-family:          "Jokker", sans-serif;
--mantine-font-family-headings: "Jokker", sans-serif;
/* h1 (Title order 0) overrides to: */   font-family: "Reckless Neue";   /* add a serif fallback in the clone */
```

`html { font-size: 16px }` (browser default; no root-size override at any width, so 1rem === 16px everywhere). `--mantine-scale: 1`, so every `calc(Xrem * var(--mantine-scale))` in the markup is just `X * 16px`.

---

## 3. Color tokens

### 3.1 Primitives on `:root` (runtime-injected `<style data-mantine-styles="true">`)

```css
:root{
  --mantine-color-white: #FFFFFF;
  --mantine-color-black: #00373E;          /* NB: "black" is the brand teal */
  --mantine-line-height: 1.55;

  /* spacing */
  --mantine-spacing-xs: 4px;  --mantine-spacing-sm: 8px;  --mantine-spacing-md: 16px;
  --mantine-spacing-lg: 32px; --mantine-spacing-xl: 48px;

  /* font sizes */
  --mantine-font-size-xs: 12px; --mantine-font-size-sm: 14px; --mantine-font-size-md: 16px;

  /* radii */
  --mantine-radius-sm: 12px; --mantine-radius-md: 16px; --mantine-radius-lg: 24px;
  --mantine-radius-default: 16px;

  /* primary = "river" */
  --mantine-primary-color-filled:       var(--mantine-color-river-filled);
  --mantine-primary-color-filled-hover: var(--mantine-color-river-filled-hover);
}
```

### 3.2 Named brand scales (complete, verbatim)

```css
/* river — primary / brand teal */
--mantine-color-river-0:#E1F9FC; --river-1:#E1F9FC; --river-2:#B2E1EB; --river-3:#B2E1EB;
--river-4:#5892A1; --river-5:#1F525E; --river-6:#1F525E; --river-7:#1F525E;
--river-8:#00373E; --river-9:#00373E;

/* moss — olive */
--moss-0:#FBFFEB; --moss-1:#FBFFEB; --moss-2:#E4EAAD; --moss-3:#E4EAAD; --moss-4:#BEC175;
--moss-5:#BEC175; --moss-6:#93954C; --moss-7:#94954C; --moss-8:#94954C; --moss-9:#66672E;

/* aqua — celeste/mint */
--aqua-0:#EDFFF7; --aqua-1:#EDFFF7; --aqua-2:#EDFFF7; --aqua-3:#DCFCF3; --aqua-4:#DCFCF3;
--aqua-5:#DCFCF3; --aqua-6:#CAFFF2; --aqua-7:#CAFFF2; --aqua-8:#CAFFF2; --aqua-9:#CAFFF2;

/* stone — sandstone */
--stone-0:#F7F5F3; --stone-1:#F7F5F3; --stone-2:#F7F5F3; --stone-3:#D6CFC4; --stone-4:#D6CFC4;
--stone-5:#AC9E88; --stone-6:#AC9E88; --stone-7:#564F44; --stone-8:#564F44; --stone-9:#564F44;

/* cloud — ivory surfaces */
--cloud-0:#F8F6F5; --cloud-1:#F8F6F5; --cloud-2:#F8F6F5; --cloud-3..9:#F1ECEB;

/* forest / jungle — identical ramps */
--forest-0:#F5F9F9; --forest-1:#E5EFF1; --forest-2:#C9DADC; --forest-3:#99B3B7; --forest-4:#7E9FA4;
--forest-5:#638C90; --forest-6:#3F6D73; --forest-7:#00373E; --forest-8:#00373E; --forest-9:#00373E;
/* --jungle-0..9 are byte-identical to --forest-0..9 */

/* terra — coral (flat) */    --terra-0..9: #FBAD9C;
/* sand — peach (flat) */     --sand-0..9:  #FBD3B6;
/* warning (flat) */          --warning-0..9: #D89024;

/* accent — new, no marketing equivalent */
--accent-0:#133D44; --accent-1:#D4EAED; --accent-2:#EEFDFF; --accent-3:#0F342F; --accent-4:#1F6F65;
--accent-5:#2EA393; --accent-6:#36BFAD; --accent-7:#E8FCC2; --accent-8:#6FADA2; --accent-9:#A76571;

/* gray */
--gray-0:#FFFFFF; --gray-1:#F7F9FA; --gray-2:#EEF1F1; --gray-3:#CED3D4; --gray-4:#A3A8A9;
--gray-5:#707575; --gray-6:#707575; --gray-7:#505354; --gray-8:#272929; --gray-9:#000000;

/* red */
--red-0:#FFF0F1; --red-1:#F9E7E8; --red-2:#DC9D9F; --red-3:#BA5C5F; --red-4:#97292D;
--red-5:#74060A; --red-6..9:#520003;

/* green */
--green-0:#F0FFF8; --green-1:#E7F9F0; --green-2:#9DDCBD; --green-3:#5CBA8B; --green-4:#299760;
--green-5:#299760; --green-6:#299760; --green-7:#06743D; --green-8:#005229; --green-9:#005229;

/* yellow */
--yellow-0:#FCFAF0; --yellow-1:#F9F5E7; --yellow-2:#F1D785; --yellow-3:#E9C558; --yellow-4:#E3B426;
--yellow-5:#B3890A; --yellow-6..9:#826300;
```

### 3.3 Semantic scales (sparse — blanks are literally empty in the original)

```css
--mantine-color-text-0:#B2BABF;  text-1:#667680;  text-2:#1F525E;  text-3:(empty);
--mantine-color-text-4:#00373E;  text-5:#66672E;  text-6..9:(empty);

--mantine-color-button-0:#B2BABF; button-4:#00373E;  /* 1,2,3,5-9 empty */
--mantine-color-surface-0:#FFFFFF; surface-1:#F8F6F5; surface-2:#F1ECEB;  /* 3-9 empty */
--mantine-color-border-0:#F1ECEB;  border-2:#D6CFC4;  border-4:#5892A1;   /* 1,3,5-9 empty */
--mantine-color-icon-3:#879599;    icon-4:#00373E;    /* rest empty */
--mantine-color-statusNegative-2:#F56D58;  statusNegative-7:#CC3F29;
--mantine-color-statusPositive-7:#828C15;
```

### 3.4 Shared vs new, against the marketing baseline

| Marketing token | Value | Present in app? | App name |
|---|---|---|---|
| `--primary` | `#00373e` | **yes** | `river-8/9`, `forest/jungle-7..9`, `--mantine-color-black`, `text-4`, `button-4`, `icon-4` |
| `--celeste` | `#cafff2` | **yes** | `aqua-6..9` |
| `--peach` | `#fbd3b6` | **yes** | `sand-0..9` |
| `--ivory` | `#f8f6f5` | **yes** | `cloud-0..2`, `surface-1` |
| `--olive` | `#94954c` | **yes** | `moss-7/8` (note `moss-6` is the off-by-one `#93954C`) |
| `--coral` | `#fbad9c` | **yes** | `terra-0..9` |
| `--sandstone` | `#ac9e88` | **yes** | `stone-5/6` |

**New in the app, no marketing equivalent** (the ones that actually matter on these three screens): `#F5F9F9` (body), `#F1ECEB` (input border), `#F7F5F3` (input hover border), `#667680` (floated label), `#B2BABF` (placeholder label), `#AEBDBE` (disabled button bg), `#FFFFFA` (disabled button text), `#F56D58` / `#CC3F29` (error), `#93954C` (anchor), `#807D7D` ("weaker" text), `#1F525E` (river-5/6/7), `#5892A1` (river-4), plus the whole `accent-*` ramp.

### 3.5 Colors actually painted on these three screens

| Role | Value | Where |
|---|---|---|
| App shell background | `#F8F6F5` | `._root_1td3m_1` — covers the full viewport, this is the visible page bg |
| `body` background | `#F5F9F9` | `body{...background-color:#f5f9f9...}` — **fully covered by the shell, never visible.** See §5.0 |
| Header surface | `#FFFFFF` | `/sign-up` only |
| Input surface | `#FFFFFF` | all inputs |
| Input border, rest | `#F1ECEB` 2px | |
| Input border, hover | `#F7F5F3` 2px | |
| Input border, focus | `#00373E` 2px + 3px outline `rgba(0,55,62,0.2)` | |
| Input border, error | `#F56D58` 2px | |
| Input text (focused/filled) | `#000000` | note: **pure black**, not the brand teal |
| Label, placeholder position | `#B2BABF` | |
| Label, floated position | `#667680` | |
| Error message text | `#F56D58` | |
| Error label text | `#CC3F29` | |
| Button primary bg / text | `#00373E` / `#CAFFF2` | |
| Button primary hover bg / text | `#93954C` / `#FFFFFF` | |
| Button disabled bg / text | `#AEBDBE` / `#FFFFFA` | |
| Button border (all states) | `1px solid rgba(0,0,0,0.19)` | `#00000030` |
| Button focus-visible outline | `3px solid #CAFFF2`, offset `0px` | |
| Heading / body text | `#00373E` | |
| Anchor | `#93954C` | |
| Header shadow | `0 1px 5px rgba(31,28,27,0.06)` | `#1f1c1b0f` |

---

## 4. Type scale (CSS modules, verbatim)

These are **fixed at every width** — there is no responsive type on any of the three screens. I verified identical computed `font-size` / `font-weight` / `line-height` / `letter-spacing` at 1440, 1024 and 390 for every role below.

### 4.1 Title component (`<h1>`…`<h6>` via Mantine `Title`)

```css
._zero_rz3tu_1  { color:#00373e; font-family:"Reckless Neue"; font-size:48px; font-weight:700; line-height:120%; letter-spacing:-.96px }
._one_rz3tu_10  { font-size:32px; font-weight:900; line-height:38.4px }
._two_rz3tu_16  { font-size:28px; font-weight:600; line-height:33.6px }
._three_rz3tu_22{ font-size:20px; font-weight:600; line-height:24px }
._four_rz3tu_28 { font-size:16px; font-weight:600; line-height:20.8px }
._five_rz3tu_34 { font-size:12px; font-weight:600; letter-spacing:1.2; text-transform:uppercase }  /* sic: unitless 1.2 — invalid, computes to `normal` */
._river_rz3tu_41{ color:#00373e }
._moss_rz3tu_44 { color:#93954c }
```
`order=0` resolves to `48px/700/57.6px/-0.96px` computed. `order=3` resolves to `20px/600/24px/normal`.

### 4.2 Text component (`<p>` via Mantine `Text`)

```css
._extraLarge_1h4u7_1 { font-size:20px; font-weight:500; line-height:28px;   word-wrap:break-word }
._large_1h4u7_9      { font-size:16px; font-weight:500; line-height:22.4px; word-wrap:break-word }
._medium_1h4u7_17    { font-size:14px; font-weight:500; line-height:19.6px; word-wrap:break-word }
._small_1h4u7_25     { font-size:12px; font-weight:500; line-height:16.8px; word-wrap:break-word }
._black_1h4u7_33  { color:#000 }
._river_1h4u7_37  { color:#00373e }
._inherit_1h4u7_41{ color:inherit }
._weaker_1h4u7_45 { color:#807d7d }
```
Default Text size on these screens is `_large_` (16px/500/22.4px).

### 4.3 Anchor

```css
._anchor_1erq5_1 { color:#93954c }
/* Mantine base: text-decoration:none; font-weight:400; line-height:1.55 */
/* data-underline="hover" → text-decoration:underline on :hover and :active only */
```
Inline `style="font-weight:600; text-decoration:underline"` is applied to the "Apply now" anchor, so it is **permanently underlined** at 600 weight. The header anchors (`data-underline="hover"`) compute `text-decoration-line: underline` at rest too — confirmed by computed style on both header links.

### 4.4 Role → computed values table (identical at 1440 / 1024 / 390)

| Role | Element | font-size | weight | line-height | letter-spacing | color | align |
|---|---|---|---|---|---|---|---|
| Screen title (welcome, sign-up) | `h1` `_zero_` | **48px** | **700** | **57.6px** | **-0.96px** | `#00373E` | center |
| Screen title (log-in) | `h3` `_three_` | **20px** | **600** | **24px** | normal | `#00373E` | left |
| Body / sub-line | `p` `_large_` | **16px** | **500** | **22.4px** | normal | `#00373E` | center |
| Input value text | `input` | **16px** | **600** | **24px** | normal | `#000000` | left |
| Label — placeholder position | `label` + `_labelAsPlaceholder_` | **16px** | **600** | **24px** | normal | `#B2BABF` | left |
| Label — floated position | `label` | **11px** | **600** | **15px** | normal | `#667680` | left |
| Helper / error text | `._error_18spb_81` | **12px** | **600** | **16.8px** | normal | `#F56D58` | left |
| Button (large) | `button` `_large_fvrsi_83` | **16px** | **600** | **16px** | normal | `#CAFFF2` | center |
| Nav / header link | `a` `_anchor_` | **16px** | **600** | **24.8px** | normal | `#93954C` | left |
| Inline link ("Apply now") | `a` `_anchor_` | **16px** | **600** | **24.8px** | normal | `#93954C` | center |
| Default body (inherited) | `body` | 16px | 400 | **24.8px** (1.55) | normal | `#00373E` | start |

**There is no legal / footnote / terms text on any of the three screens.** No "by continuing you agree to…" line, no privacy link, no ToS link. (Recorded as a fact, not an omission.)

---

## 5. Layout geometry

### 5.0 The shell (all three screens)

```css
._root_1td3m_1 {                       /* Mantine AppShell root */
  min-height: 100%;
  min-height: stretch;
  overflow-x: hidden;                  /* ← this is what clips the oversized log-in illustration at 390 */
  display: flex;
  flex-direction: column;
  min-width: 300px;
  background-color: #F8F6F5;
}
._content_1td3m_16 {                   /* also carries Mantine Container, size md */
  height: 100vh;
  padding-top: 48px;
}
```
AppShell runtime vars: `--app-shell-padding: 0px`, `--app-shell-transition-duration: 200ms`, `--app-shell-transition-timing-function: ease`.

There is a stray global `body { padding:16px; background-color:#f5f9f9; color:#00373e; box-shadow:0 4px 8px #00000040; border-radius:8px; margin:0 16px }` rule in the bundle (it sits right after the Toast keyframes — almost certainly a toast style that leaked its selector). Measured `body` margin is `0px` (something later resets it) and the `#F5F9F9` bg and shadow are entirely hidden behind the full-bleed shell. **Do not reproduce it.**

### 5.1 The two-container pattern

Both containers are Mantine `Container`:

```css
.mantine-Container-root {
  --container-size-xs: 540px;  --container-size-sm: 720px;  --container-size-md: 960px;
  --container-size-lg: 1140px; --container-size-xl: 1320px;
  --container-size: var(--container-size-md);   /* default */
  max-width: var(--container-size);
  padding-inline: 16px;
  margin-inline: auto;
}
```

- **Outer** (`._content_1td3m_16`): default size → `max-width:960px`, `padding:48px 16px 0`.
- **Inner** (`data-size="xs"`): `max-width:540px`, `padding:0 16px` → **content column is exactly 508px** at every width ≥ 540.

Resulting `margin-inline` (measured, auto-computed):

| Viewport | Outer container x / width | Outer margin-inline | Inner container x / width | Content column |
|---|---|---|---|---|
| 1440 | x=240, w=960 | 240px | x=450, w=540 | **508px** (x=466) |
| 1024 | x=32, w=960 | 32px | x=242, w=540 | **508px** (x=258) |
| 390 | x=0, w=390 | 0px | x=16, w=358 | **326px** (x=32) |

So at 390 the content column is `390 − 16 − 16 − 16 − 16 = 326px`.

Centring is **horizontal only** (`margin-inline:auto`). There is **no vertical centring** — content is top-aligned, pinned 48px below the shell top (or 48px below the 96px header on `/sign-up`). The card/panel metaphor doesn't apply: **there is no card.** No panel background, no border, no shadow, no backdrop-filter anywhere in the content column on any of the three screens. Content sits directly on the `#F8F6F5` shell.

### 5.2 Breakpoints

Mantine min-width, em-based (16px root), from the injected `@media` helpers:

| Name | em | px |
|---|---|---|
| xs | 36em | **576** |
| sm | 48em | **768** |
| md | 62em | **992** |
| lg | 75em | **1200** |
| xl | 88em | **1408** |

**None of these breakpoints fire any rule on these three screens.** Every responsive change measured is pure flexbox/`max-width` reflow. The only media queries present are the `mantine-visible-from-*` / `mantine-hidden-from-*` display helpers (unused here) and `@media (prefers-reduced-motion: reduce) { [data-respect-reduced-motion] [data-reduce-motion] { transition:none; animation:none } }` (the data attributes are not set on these screens, so reduced-motion does nothing).

### 5.3 Header (only on `/sign-up`)

`/log-in` and `/welcome` have **no `<header>` element at all** (`document.querySelector('header') === null`, verified at all three widths). On those screens `--app-shell-header-height: 0rem`, `--app-shell-header-offset: 0rem`, so `main` has `padding-top:0`.

On `/sign-up`:

```
header                        position:fixed; top:0; left:0; width:100vw; height:96px; z-index:100
                              background:#FFFFFF; border:none; box-shadow:0 1px 5px rgba(31,28,27,0.06)
  > div (Mantine Group)       width:100%; height:92px; padding:32px 22px; display:flex; flex-direction:row
                              flex-wrap:wrap; justify-content:space-between; align-items:center; gap:16px
      > div (Group)           gap:12px; justify-content:flex-start    → logo link
      > div (Group)           gap:16px; justify-content:flex-start    → "Log in" link
main                          padding-top:96px   (= --app-shell-header-offset)
```
Identical at 1440 / 1024 / 390 — the header does **not** collapse to a burger, and the two groups stay on one row (`flex-wrap:wrap` is set but never triggers at 390; the logo is 79.5px and "Log in" is 48px).

| Viewport | Logo rect | "Log in" rect |
|---|---|---|
| 1440 | `[22, 32, 79.5, 28]` | `[1370, 33.6, 48, 24.8]` |
| 1024 | `[22, 32, 79.5, 28]` | `[954, 33.6, 48, 24.8]` |
| 390 | `[22, 32, 79.5, 28]` | `[320, 33.6, 48, 24.8]` |

### 5.4 Document heights

| Screen | 1440×900 | 1024×900 | 390×844 |
|---|---|---|---|
| `/log-in` | 900 (no scroll) | 900 (no scroll) | 844 (no scroll) |
| `/sign-up` | **996** (scrolls 96px) | **996** (scrolls 96px) | **940** (scrolls 96px) |
| `/welcome` | 900 (no scroll) | 900 (no scroll) | 844 (no scroll) |

`/sign-up` overflows by exactly the 96px header offset because `._content_1td3m_16` is `height:100vh` *and* `main` adds `padding-top:96px`. (A real bug in the original; reproduce it or not, but know that's where the 96px comes from.)

---

## 6. Form controls — complete inventory

### 6.1 `/log-in` — 1 field

| # | Attribute | Value |
|---|---|---|
| 1 | `type` | `tel` |
| | `name` | `phoneNumber` |
| | `id` | `mantine-br3902h4m` — **randomly generated per render, do not hardcode**; use a stable id in the clone |
| | `autocomplete` | `tel-national` ← **original value; use `off` in the clone** |
| | label text | `Phone Number` (capital N) |
| | `placeholder` | **none** — the label doubles as the placeholder (see §7) |
| | `required` | **absent** |
| | `pattern` / `minlength` / `maxlength` / `inputmode` | **all absent** |
| | `aria-invalid` | `false` |
| | `data-variant` | `default` |
| | `data-empty` | `true` when empty, attribute removed on focus/fill |
| | `data-label` | `true` (always — drives the `padding:21px 14px 6px` offset) |
| | `aria-describedby` | absent |
| | wired via | `<label for="{input.id}" id="{input.id}-label">` |

### 6.2 `/sign-up` — 3 fields, in DOM order

| # | `type` | `name` | `autocomplete` (original) | Label | Width @1440/1024 | Width @390 |
|---|---|---|---|---|---|---|
| 1 | `tel` | `phoneNumber` | `tel` | `Phone number` (lowercase n) | 508px (full) | 326px (full) |
| 2 | `text` | `firstName` | `given-name` | `First name` | 246px | 155px |
| 3 | `text` | `lastName` | `family-name` | `Last name` | 246px | 155px |

All three: no `placeholder`, no `required`, no `pattern`, no `min/maxlength`, no `inputmode`, `aria-invalid="false"`, `data-variant="default"`, `data-empty="true"`, `data-label="true"`, random `mantine-*` id.

**Note the inconsistency between screens:** `/log-in` labels its field "Phone **N**umber" with `autocomplete="tel-national"`; `/sign-up` labels it "Phone **n**umber" with `autocomplete="tel"`. Reproduce both as-is (minus the autocomplete).

Fields 2+3 sit in a Mantine `Group`:
```css
display:flex; flex-direction:row; flex-wrap:wrap; align-items:center; gap:16px; justify-content:flex-start;
/* each child InputWrapper: */ max-width: calc(50% - 8px);
```
At 390 this still yields two side-by-side columns of 155px (`(326 − 16)/2`); it does **not** stack.

### 6.3 `/welcome` — 0 fields

No `<input>`, no `<form>`. One `<button type="button">` and one `<a>`.

### 6.4 Input box model (identical for all 4 inputs across all 3 screens)

```css
._input_18spb_10 {
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  height: auto;                              /* computed height: 55px */
  background-color: #fff;
  color: #000;
  padding: 14px;                             /* overridden below when data-label */
  border: 2px solid #f1eceb !important;
  border-radius: 12px !important;
  outline: 3px solid transparent !important;
  transition: border-color .2s ease, outline-color .2s ease, background-color .2s ease, color .2s ease;
  box-sizing: border-box;
  display: block;
  width: 100%;
  min-height: 36px;
  overflow: clip;
}
._input_18spb_10[data-label] { padding: 21px 14px 6px }   /* ← the state that actually applies */
```
Computed height = `21 + 24 + 6 + 2 + 2 = 55px`. **No box-shadow.** The wrapper:
```css
._root_18spb_1    { position: relative }
._wrapper_18spb_5 { display: flex; width: 100% }
```

### 6.5 Input visual states — all measured or read from the stylesheet

| State | How reached | Border | Outline | Background | Text color |
|---|---|---|---|---|---|
| **default / empty** | as-rendered ✅measured | `2px solid #F1ECEB` | `3px solid transparent` | `#FFFFFF` | `transparent` (via `[data-empty]{color:transparent}`) |
| **hover** | stylesheet rule ✅read | `2px solid #F7F5F3` | unchanged | unchanged | unchanged |
| **focus** | real click, no typing ✅measured | `2px solid #00373E` | `3px solid rgba(0,55,62,0.2)` (`#00373e33`) | `#FFFFFF` | `#000000` |
| **focus-visible** | — | **no distinct rule.** `:focus` and `:focus-visible` are identical for inputs. `.mantine-focus-auto:focus-visible` exists but is not on the input. |
| **filled** | DOM class toggle ✅measured | `2px solid #F1ECEB` | transparent | `#FFFFFF` | `#000000` (`data-empty` removed → base `color:#000` applies) |
| **disabled** | `input.disabled = true` ✅measured; rule ✅read | `2px solid #F1ECEB` | transparent | `rgba(175,184,193,0.2)` (`#afb8c133`) over white | `#000000`; Mantine base also adds `cursor:not-allowed; opacity:.6` |
| **error** | `data-error` DOM toggle ✅**measured** → `border-color: rgb(245,109,88)` | `2px solid #F56D58` | transparent | `#FFFFFF` | `#000000` |
| **error + focus** | stylesheet rule ✅read | `2px solid #F56D58` | `3px solid rgba(245,109,88,0.2)` (`#f56d5833`) | `#FFFFFF` | `#000000` |

Stylesheet source for the above (verbatim):
```css
._input_18spb_10:hover              { border-color:#f7f5f3 !important }
._input_18spb_10:focus              { border-color:#00373e !important; outline-color:#00373e33 !important }
._input_18spb_10::placeholder       { color:#b2babf !important }
._input_18spb_10:disabled           { background-color:#afb8c133 !important }
._input_18spb_10[data-error]        { border-color:#f56d58 !important }
._input_18spb_10[data-error]:focus  { outline-color:#f56d5833 !important }
._input_18spb_10[data-error] ._label_18spb_46 { color:#cc3f29 }
._input_18spb_10[data-empty]        { color:transparent }
```

**Error-message styling (unverified in the DOM, read from the stylesheet only):**
```css
._error_18spb_81 { font-size:12px; font-weight:600; color:#f56d58; line-height:16.8px; margin-top:8px }
```
> ⚠️ **UNMEASURED:** no error message is ever rendered on these screens without submitting the form, which the constraints forbid. The rule above is the definition the app would use, and the `[data-error]` border/outline/label colors are confirmed by DOM toggling, but the **rendered position and wrapping of an actual error message string were not observed.** Also note the selector `._input_18spb_10[data-error] ._label_18spb_46` is a *descendant* selector on an `<input>`, which can never match — so **the `#CC3F29` error-label color is dead CSS in the original.** Don't chase it.
>
> ⚠️ **UNMEASURED:** the placeholder color `#B2BABF` is declared via `::placeholder`, but **no input on these screens has a `placeholder` attribute**, so it is never painted. It happens to be the same hex as `_labelAsPlaceholder_`, which is where it's actually visible.

---

## 7. The floating-label pattern (the signature interaction)

There is no `placeholder` attribute anywhere. Instead, the Mantine `InputWrapper` label is absolutely positioned over the input and moves between two positions.

```css
._label_18spb_46 {               /* FLOATED (small, up) position — the base state */
  z-index: 101;
  position: absolute;
  transition: all .2s ease;
  color: #667680;
  font-size: 11px;
  line-height: 15px;
  font-weight: 600;
  pointer-events: none;
  top: 10px;
  left: 16px;
  cursor: text;
}
._labelAsPlaceholder_18spb_74 {  /* PLACEHOLDER (large, centred) position — added while empty+unfocused */
  color: #b2babf !important;
  font-size: 16px;
  line-height: 24px;
  top: 16px;
}
/* Mantine base .m_8fdc1311: display:inline-block; font-weight:500; word-break:break-word; cursor:default */
```

Measured, on the `/log-in` phone field at 1440 (input rect `[466, 421.5, 508, 55]`):

| Label state | rect | font | color |
|---|---|---|---|
| placeholder position (empty, unfocused) | `[482, 437.5, 113.8, 24]` → top = input.top + **16px**, left = input.left + **16px** | 16px / 600 / 24px | `#B2BABF` |
| floated position (focused or filled) | `[482, 431.5, 113.8, 15]` → top = input.top + **10px**, left = input.left + **16px** | 11px / 600 / 15px | `#667680` |

So the label travels **6px up** and shrinks 16px → 11px over `all .2s ease`. The `21px` input `padding-top` is what reserves room for the floated label.

The `_labelAsPlaceholder_*` class is **added/removed by React**, not by CSS `:placeholder-shown` — confirmed: on focus the class list changes from
`_label_18spb_46 _labelAsPlaceholder_18spb_74 m_8fdc1311 mantine-InputWrapper-label mantine-TextInput-label`
to
`_label_18spb_46 m_8fdc1311 mantine-InputWrapper-label mantine-TextInput-label`,
and simultaneously `data-empty` is removed from the input (which un-hides the text color). In the clone, drive it from React state on `focus`/`blur`/`value.length`.

---

## 8. Buttons

### 8.1 Variant system (CSS modules, verbatim)

```css
._root_fvrsi_1 { font-weight:600; transition:all .3s; border-radius:999px }
._root_fvrsi_1:active:not(:disabled) { transform:scale(.92) }

._primary_fvrsi_12          { background-color:#00373e; color:#cafff2; border:1px solid #00000030; outline-color:#cafff2 }
._primary_fvrsi_12:hover    { background-color:#93954c; color:#fff }
._primary_fvrsi_12:disabled { background-color:#aebdbe; color:#fffffa }

._secondary_fvrsi_29            { background-color:#fff; color:#00373e }
._secondary_fvrsi_29:disabled   { background-color:#d3d3d3; color:gray }
._secondary_fvrsi_29[data-icon] { border-color:#f1eceb }
._secondary_fvrsi_29:disabled   { background-color:auto; color:#fffffa; min-width:105px }   /* sic: duplicate, later wins */

._invisible_fvrsi_48 { padding:14px 8px !important }

._section_fvrsi_52[data-position=left]  { margin-inline-end:12px }
._section_fvrsi_52[data-position=right] { margin-inline-start:12px }

._small_fvrsi_61             { height:32px; padding:8px 12px;  font-size:12px }
._small_fvrsi_61[data-icon]  { width:32px;  padding:8px }
._medium_fvrsi_72            { height:40px; padding:12px 16px; font-size:14px }
._medium_fvrsi_72[data-icon] { width:40px;  padding:12px }
._large_fvrsi_83             { height:56px; padding:16px 24px; font-size:16px }
._large_fvrsi_83[data-icon]  { width:56px;  padding:16px }
```

**Only `primary` + `large` is used on these three screens.** `secondary`, `invisible`, `small`, `medium` and the icon/section variants exist in the bundle but appear on none of them. There are **no social-auth buttons and no provider icons** on any of the three screens — no Google, Apple, Facebook mark, no `<svg>` at all (`document.querySelectorAll('#root svg').length === 0` on all three).

### 8.2 Measured box model (primary / large)

| Screen | rect @1440 | rect @1024 | rect @390 | margin-top | type |
|---|---|---|---|---|---|
| `/log-in` "Continue" | `[466, 500.5, 508, 56]` | `[258, 500.5, 508, 56]` | `[32, 500.5, 326, 56]` | **8px** (`--mantine-spacing-sm`) | `submit`, `disabled` |
| `/sign-up` "Continue" | `[466, 592.1, 508, 56]` | `[258, 592.1, 508, 56]` | `[32, 649.7, 326, 56]` | 0 | `submit`, `disabled` |
| `/welcome` "Log in" | `[474, 376.5, 492, 56]` | `[266, 376.5, 492, 56]` | `[40, 456.5, 310, 56]` | 0 | `button`, **enabled** |

```
height:          56px
padding:         16px 24px
border:          1px solid rgba(0,0,0,0.19)
border-radius:   999px
box-shadow:      none
font:            16px / 600 / line-height 16px / letter-spacing normal / text-align center
display:         block       (width is 100% of the stack, set by the parent flex stretch)
position:        relative
overflow:        hidden      ← needed for the loading overlay, see §9
transition:      all .3s
user-select:     none
vertical-align:  middle
```
Inline style on every one of them:
```
--button-bg: var(--mantine-color-river-filled);
--button-hover: var(--mantine-color-river-filled-hover);
--button-color: var(--mantine-color-white);
--button-bd: 1px solid transparent;
```
These Mantine vars are all **overridden by the higher-specificity `._primary_fvrsi_12` rule**, so the painted values are the hard-coded hexes in §8.1. Measured confirmation: enabled → `background-color: rgb(0,55,62)`, `color: rgb(202,255,242)`; disabled → `rgb(174,189,190)` / `rgb(255,255,250)`.

Internal structure:
```html
<button class="mantine-focus-auto _root_fvrsi_1 _primary_fvrsi_12 _large_fvrsi_83 mantine-Button-root mantine-UnstyledButton-root" data-variant="filled" type="submit" disabled>
  <span class="mantine-Button-inner">   <!-- display:flex; align-items:center; justify-content:center; height:100%; overflow:visible; transition:transform .15s ease, opacity .1s ease -->
    <span class="mantine-Button-label">Continue</span>  <!-- white-space:nowrap; height:100%; overflow:hidden; display:flex; align-items:center; opacity:1 -->
  </span>
</button>
```
Inner span rect @1440 on `/log-in`: `[491, 517.5, 458, 22]`; label span: `[685.3, 517.5, 69.3, 22]`.

### 8.3 Button states

| State | How reached | Background | Text | Transform | Border | Outline |
|---|---|---|---|---|---|---|
| **default (enabled)** | `/welcome` as-rendered ✅measured | `#00373E` | `#CAFFF2` | none | `1px solid rgba(0,0,0,.19)` | — |
| **hover** | stylesheet ✅read | `#93954C` | `#FFFFFF` | none | unchanged | — |
| **active** | stylesheet ✅read | `#93954C` | `#FFFFFF` | **`scale(.92)`** | unchanged | — |
| **focus-visible** | `btn.focus()` ✅measured | unchanged | unchanged | none | unchanged | **`3px solid #CAFFF2`, `outline-offset: 0px`** |
| **disabled** | `/log-in` + `/sign-up` as-rendered ✅measured | `#AEBDBE` | `#FFFFFA` | `none` forced | `1px solid transparent` forced by Mantine, but `._primary_` border wins → `1px solid rgba(0,0,0,.19)` measured | `cursor:not-allowed` |
| **loading** | Mantine `[data-loading]` ✅rules read, ⚠️**not observed live** | unchanged + `::before` overlay | label `opacity:.2` | inner `translateY(100%)` | — | `cursor:not-allowed` |

Note on focus: `.mantine-focus-auto:focus-visible { outline:2px solid var(--mantine-primary-color-filled); outline-offset:2px }` is Mantine's default and **is** on the button's class list, but `._primary_fvrsi_12{outline-color:#cafff2}` plus the `outline:3px` width wins — measured `outline: rgb(202,255,242) solid 3px`, `outline-offset: 0px`. `.mantine-active:active{transform:translateY(1px)}` is also present on the `/welcome` button but is overridden by `._root_fvrsi_1:active:not(:disabled){transform:scale(.92)}`.

### 8.4 Anchors as controls

```css
.m_849cf0da { color:var(--mantine-color-anchor); text-decoration:none; appearance:none; border:none;
              display:inline; padding:0; margin:0; background-color:transparent; cursor:pointer }
.m_849cf0da[data-underline=hover]:hover,
.m_849cf0da[data-underline=hover]:active { text-decoration:underline }
._anchor_1erq5_1 { color:#93954c }
```
`transition: all` (unitless duration → `0s`, i.e. no actual transition despite the declaration).

---

## 9. Radii, shadows, borders, backdrop-filters

| Component | Radius | Border | Shadow | Backdrop-filter |
|---|---|---|---|---|
| App shell | 0 | none | none | **none** |
| Header (`/sign-up`) | 0 | `none` (explicitly `border:none`, overriding Mantine's `--app-shell-border-color: var(--mantine-color-gray-3)`) | `0 1px 5px rgba(31,28,27,0.06)` | **none** |
| Content containers / stacks | 0 | none | none | **none** |
| Input | **12px** (`!important`) | **2px solid** `#F1ECEB` (`!important`) | **none** | **none** |
| Input outline ring | follows radius | `3px` outline, transparent at rest | — | — |
| Button | **999px** (pill) | **1px solid** `rgba(0,0,0,0.19)` | **none** | **none** |
| Images | `var(--image-radius, 0)` → **0** | none | none | **none** |

**`backdrop-filter` is `none` on every element on all three screens.** There is no glass/blur anywhere. (The only blur in the system is `filter:blur(12px)` inside the button's loading `::before` overlay — see §10.)

Token reference: `--mantine-radius-sm:12px` / `md:16px` / `lg:24px`, default `16px`. Note the input uses `12px` and the button `999px`, so **neither matches the default radius token**.

---

## 10. Motion

**There are no entrance animations, no scroll-triggered animations, and no scroll listeners on any of the three screens.** Verified:
- `[...document.querySelectorAll('#root *')].filter(e => getComputedStyle(e).animationName !== 'none')` → **`[]`** on all three screens, at all three widths. Nothing is animating on load.
- `animation` computes to `none 0s ease 0s` on every element.
- Only 9 `@keyframes` exist in the entire bundle: `Notification-in`, `Notification-out`, `Toastify__trackProgress` (all toast-only, and the `.Toastify` container is empty), plus 6 Mantine internals (`m_299c329c`, `m_5d2b3b9d`, `m_81a374bd`, `m_885901b1`, `m_aac34a1`, `m_f8e89c4b`) for Popover/Modal/Transition components that aren't mounted here.
- `IntersectionObserver` is available in the page but **no element is observed** — there is no reveal-on-scroll anywhere; two of the three screens don't even scroll.
- No `<canvas>`, no `<video>`, no Lottie, no GSAP.

### Transitions that do exist (all measured from computed style)

| What | Property | Duration | Easing | Delay |
|---|---|---|---|---|
| **Input border + ring + bg + text** | `border-color, outline-color, background-color, color` | **0.2s** | `ease` | 0 |
| **Floating label** (size, color, position) | `all` | **0.2s** | `ease` | 0 |
| **Button** (bg, color, transform) | `all` | **0.3s** | default `ease` (no function declared) | 0 |
| **Button loading overlay** (`::before`) | `transform` / `opacity` | **0.15s / 0.1s** | `ease` | 0 |
| **Button inner span** (loading) | `transform` / `opacity` | **0.15s / 0.1s** | `ease` | 0 |
| **Anchor** | `all` | **0s** (unitless value in source → invalid → no transition) | — | — |
| AppShell padding | `padding` | `200ms` | `ease` | 0 — never fires here (no navbar/aside) |
| Radio (elsewhere in app) | `border-color, background-color` | `0.1s` | `ease` | — |

**No stagger anywhere** — there is no sequenced/delayed group animation on any screen.

### Button loading state (Mantine built-in; rules read, not observed)

```css
.m_77c9d27d::before {
  content:""; pointer-events:none; position:absolute; inset:-1px;
  border-radius: var(--button-radius, var(--mantine-radius-default));
  transform: translateY(-100%); opacity:0; filter: blur(12px);
  transition: transform .15s ease, opacity .1s ease;
  background-color: rgba(255,255,255,0.15);     /* #ffffff26, light scheme */
}
.m_77c9d27d[data-loading]                   { cursor:not-allowed; transform:none }
.m_77c9d27d[data-loading]::before           { transform: translateY(0); opacity:1 }
.m_77c9d27d[data-loading] .mantine-Button-inner { opacity:0; transform: translateY(100%) }
.mantine-Button-label[data-loading]         { opacity:.2 }
```
> ⚠️ **UNMEASURED:** reaching `[data-loading]` requires submitting the form, which is forbidden. The rules above are the definitions; the live appearance was not observed. **There is no spinner component** — Mantine's `Loader` CSS is **not present in the bundle at all** (grep for `Loader`/`spinner` selectors → no matches), so the loading affordance is purely the blurred white sweep + label fade described above. Do not add a spinner.

---

## 11. Structural outlines in DOM order, with real copy

### 11.1 `/log-in` — `<title>Otter | Log in</title>`

No header. No links. One field. 24 elements under `#root` (3 of them `<style>`).

```
div#root
├─ style × 3                                   (Mantine tokens, media helpers, app-shell vars)
├─ div ._root_1td3m_1 .mantine-AppShell-root   bg #F8F6F5, 1440×900
│  └─ main .mantine-AppShell-main              padding 0
│     └─ div ._content_1td3m_16 Container       max-w 960, padding 48px 16px 0
│        └─ div Container data-size="xs"        max-w 540, padding 0 16px   → column 508px
│           └─ div Stack                        gap 16px
│              ├─ div Stack                     gap 16px, margin-block 24px
│              │  ├─ div Center                 (height 0 — collapsed, logo escapes upward)
│              │  │  └─ img  style="width:96px; margin-top:-48px"
│              │  │           ASSET: inline data-URI Otter wordmark SVG, 125×44 → rendered 96×33.8
│              │  │           rect @1440 [672, 31.1, 96, 33.8]  ← note negative y offset
│              │  └─ div Center
│              │     └─ img  style="width:400px"
│              │              ASSET: /assets/illo-children-of-different-ages-CwALik0h.svg
│              │              intrinsic 2804×1777 → rendered 400×253.5
│              └─ form  data-hs-cf-bound="true"      ← HubSpot touched it; NO action, NO method
│                 └─ div Stack                  gap 16px
│                    ├─ h3 ._three_ ._river_    "Welcome back!"            20px/600/24px
│                    ├─ div ._root_18spb_1 InputWrapper
│                    │  ├─ label ._label_ ._labelAsPlaceholder_   "Phone Number"
│                    │  └─ div ._wrapper_18spb_5
│                    │     └─ input type=tel name=phoneNumber
│                    └─ button[type=submit][disabled] primary/large   "Continue"   margin-top 8px
└─ div.Toastify                                 (empty)
```

Vertical rhythm @1440 (`y`, `height`):
```
logo        31.1   33.8      (pulled up out of flow by margin-top:-48px)
illo        88.0  253.5
h3         381.5   24.0      ← 40px below illo bottom (16px stack gap + 24px margin-block)
input      421.5   55.0      ← 16px stack gap
button     500.5   56.0      ← 16px stack gap + 8px button margin-top = 24px
```
Identical `y` values at 1024 and 390. At **390** the illustration is a fixed **400px** wide inside a 326px column → rect `[-5, 88, 400, 253.5]`, **overflowing both edges by 5px and clipped by `overflow-x:hidden` on the AppShell root.** Reproduce the clip, or clamp the width — flag this to the user as an original-site quirk.

**Copy on this screen, complete:** `Welcome back!`, `Phone Number`, `Continue`. Nothing else — no "forgot password", no "don't have an account?", no legal text, no link to `/sign-up`.

### 11.2 `/sign-up` — `<title>Otter | Sign Up</title>`

```
div#root
├─ style × 3
├─ div ._root_1td3m_1 AppShell-root            bg #F8F6F5
│  ├─ header .mantine-AppShell-header .right-scroll-bar-position ._header_1td3m_11
│  │        fixed, 96px tall, bg #FFFFFF, shadow 0 1px 5px rgba(31,28,27,.06), z-index 100
│  │  └─ div Group    padding 32px 22px, justify-content space-between, gap 16px, wrap
│  │     ├─ div Group  gap 12px
│  │     │  └─ a[href="/"] Anchor data-underline="hover"      → app host root, NOT withotter.com
│  │     │     └─ img  ASSET: inline data-URI Otter wordmark SVG, 125×44 → rendered 79.5×28
│  │     └─ div Group  gap 16px
│  │        └─ a[href="/log-in"] Anchor data-underline="hover"   "Log in"   16px/600, #93954C
│  └─ main   padding-top 96px
│     └─ div ._content_1td3m_16 Container       max-w 960, padding 48px 16px 0
│        └─ form                                ← NO action, NO method
│           └─ div Container data-size="xs"     max-w 540 → column 508px
│              └─ div Stack                     gap 32px
│                 ├─ div Stack                  gap 16px
│                 │  ├─ div Center
│                 │  │  └─ img style="width:160px"
│                 │  │          ASSET: /assets/illo-care-team-AGZuQRFl.svg
│                 │  │          intrinsic 170×196 → rendered 160×184.5
│                 │  └─ h1 ._zero_ ._river_ ta=center  "Welcome to Otter"   48px/700/57.6px/-0.96px
│                 │          inline style: font-family:"Reckless Neue"; text-align:center
│                 ├─ div Stack                  gap 16px
│                 │  ├─ div InputWrapper        label "Phone number" / input tel name=phoneNumber   (full width)
│                 │  └─ div Group               gap 16px, wrap, children max-width calc(50% - 8px)
│                 │     ├─ div InputWrapper     label "First name" / input text name=firstName
│                 │     └─ div InputWrapper     label "Last name"  / input text name=lastName
│                 └─ button[type=submit][disabled] primary/large   "Continue"
└─ div.Toastify
```

Vertical rhythm @1440 / @1024 (identical):
```
header         0.0    96.0
illo         144.0   184.5    ← 48px below header
h1           344.5    57.6    ← 16px stack gap
phone        434.1    55.0    ← 32px outer stack gap
first/last   505.1    55.0    ← 16px stack gap
button       592.1    56.0    ← 32px outer stack gap
```
@390 the h1 wraps to 2 lines (height 115.2px) and everything below shifts: illo 144, h1 344.5 (h 115.2), phone 491.7, names 562.7, button 649.7.

**Copy on this screen, complete:** `Log in` (header), `Welcome to Otter`, `Phone number`, `First name`, `Last name`, `Continue`. No legal text, no "already have an account" line in the body (it's the header link instead).

### 11.3 `/welcome` — `<title>Otter | Welcome</title>` (reached from `/sign-up/welcome`)

No header. No form. No inputs.

```
div#root
├─ style × 3
├─ div ._root_1td3m_1 AppShell-root            bg #F8F6F5
│  └─ main
│     └─ div ._content_1td3m_16 Container       max-w 960, padding 48px 16px 0
│        └─ div Container data-size="xs"        max-w 540 → column 508px
│           └─ div Stack   gap 32px, align stretch, justify center, padding 0 8px, min-height 100%
│              ├─ div Stack   gap 16px, justify center       → column 492px
│              │  └─ div Stack   gap 16px, justify flex-start
│              │     └─ div Stack   gap 8px, align center, justify center
│              │        ├─ div Center   margin-bottom 16px
│              │        │  └─ img  style="width:160px"
│              │        │          ASSET: /assets/illo-care-team-AGZuQRFl.svg  (same as /sign-up)
│              │        │          intrinsic 170×196 → rendered 160×184.5
│              │        ├─ h1 ._zero_ ._river_ ta=center  "Welcome to Otter"  48px/700/57.6px/-0.96px
│              │        └─ p  ._large_ ._river_ ta=center
│              │              "We want to get you the job and the pay you deserve."   16px/500/22.4px
│              └─ div Stack   gap 32px
│                 ├─ button[type=button] primary/large  ENABLED   "Log in"
│                 │        onClick → navigate to /log-in   (no href)
│                 └─ p ._large_ ._river_ ta=center
│                       "Don't have an account? " + <a>"Apply now"</a>
│                       anchor: href="" , inline style font-weight:600; text-decoration:underline
│                       onClick → navigate to /sign-up    ⚠️ empty href — in the clone use a real
│                                                            local route or a <button>, not href=""
└─ div.Toastify
```

Vertical rhythm @1440 / @1024 (identical):
```
illo       48.0   184.5
h1        256.5    57.6    ← 24px below illo (8px stack gap + 16px Center margin-bottom)
p         322.1    22.4    ← 8px stack gap
button    376.5    56.0    ← 32px outer stack gap
p (link)  464.5    24.8    ← 32px stack gap
```
@390: illo 48, h1 256.5 (wraps, h 115.2), p 379.7 (wraps, h 44.8), button 456.5, link-p 544.5. Column 310px (326 − 2×8px stack padding).

Note the three nested single-child `Stack`s with gaps 16/16/8 — redundant in the original but they contribute the 8px gap that sets h1→p spacing. Flatten in the clone, but keep the measured 24px / 8px / 32px / 32px gaps.

**Copy on this screen, complete:** `Welcome to Otter`, `We want to get you the job and the pay you deserve.`, `Log in`, `Don't have an account?`, `Apply now`. (Apostrophe is a straight `'` in the source.)

---

## 12. Links and other routes

### 12.1 Links back to `withotter.com`

**There are none.** No element on any of the three screens links to the marketing site. The header logo on `/sign-up` points to `href="/"` on the **app** host. Searching the whole JS bundle for `withotter.com` finds only: `https://api.withotter.com` (API base), `mailto:community@withotter.com` (used on a *different* screen, not these three), and the `VITE_APP_DOMAIN` / `VITE_APP_WEB_DOMAIN` env strings.

### 12.2 Links present on these three screens

| Screen | Element | Target |
|---|---|---|
| `/sign-up` | header logo `<a>` | `/` (app host) |
| `/sign-up` | header `<a>` "Log in" | `/log-in` |
| `/welcome` | `<button>` "Log in" | `/log-in` via `onClick` (no href) |
| `/welcome` | `<a>` "Apply now" | `/sign-up` via `onClick`; `href=""` |
| `/log-in` | — | no links at all |

### 12.3 Other routes on the app host (list only, not specced)

From the client route table in `index-3SWImSlZ.js`:

```
/                      /log-in                /log-in/verify         /log-in/password
/log-out               /sign-up               /sign-up/record-interest
/welcome               /confirm-phone         /join-waitlist         /waitlisted
/inactive              /call-us               /profile               /photo
/about-me              /about-you             /availability          /check-availability
/experience            /work-history          /add-position          /hours
/job-preferences       /pay-preferences       /languages             /other-skills
/transportation        /credits               *  (catch-all → redirect guard)
```

The presence of `log-in/verify` and `log-in/password` confirms the shape of the flow: phone number first, then a one-time-code (or password) step. **Only the three screens above are in scope; do not build the verify step.**

---

## 13. Things that could not be measured

| Item | Why | What I did instead |
|---|---|---|
| Rendered error message text + position | Requires form submission (forbidden) | Extracted `._error_18spb_81` rule verbatim; marked **unmeasured**; confirmed `[data-error]` border/outline via DOM attribute toggle |
| Button `[data-loading]` live appearance | Requires form submission (forbidden) | Extracted the full Mantine loading rule set; marked **unmeasured**; confirmed no `Loader`/spinner CSS exists |
| Actual validation rules (phone format, min length) | Enforced in JS on submit; no HTML `pattern`/`required`/`minlength` attributes exist | Recorded the complete (empty) set of validation attributes |
| `::placeholder` appearance | No input has a `placeholder` attribute | Recorded the declared color `#B2BABF`; never painted |
| Post-submit screens (`/log-in/verify`, `/confirm-phone`) | Out of scope + would require submitting | Listed in §12.3 only |
| Any authenticated screen | Would require a session (forbidden) | Not attempted |

No value in this document is estimated. Every px/hex is either a `getComputedStyle`/`getBoundingClientRect` reading or a verbatim declaration from the shipped stylesheet, and the two are distinguished wherever they differ.
