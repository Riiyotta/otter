# Otter clone — information architecture

A pixel-audited rebuild of `https://withotter.com/` in React 18 + Vite +
Tailwind v3. This README documents the **information architecture**; the IA is
kept as data so the numbers in it can be machine-checked rather than trusted.

## Which files to edit

| File | Status |
|---|---|
| `ia.json` | **Hand-edited.** The single source of truth. |
| `IA.md` | Generated — do not hand-edit, it will be overwritten. |
| `matrix.csv` | Generated — section × template matrix, for a spreadsheet. |
| `validate.mjs`, `build.mjs` | Copied in from the `ia-builder` skill. Generic; driven entirely by `ia.json`. |

After changing `ia.json`:

```bash
node validate.mjs   # must print "All hard invariants reconcile."
node build.mjs      # regenerates IA.md + matrix.csv
```

`validate.mjs` checks that template route counts sum to `meta.totalRoutes`,
that every referenced section is defined and every defined section is used,
and that each category exists. It also re-reads every number written into a
section's `scope` prose and compares it against the route count actually
computed from the data — so a stale claim in prose can't drift unnoticed.

## What the data shows

**21 routes across 13 templates, built from 36 distinct sections — 11 shared,
25 page-local.** The reuse is concentrated almost entirely in the chrome:
`chrome.nav`, `chrome.footer` and `chrome.shape-defs` each appear on 11
templates covering 20 of the 21 routes. Below that the site is unusually flat
— after the chrome, the most-reused section (`hero.page`) covers just 3 routes,
and 25 sections are single-use.

**Ten of the 21 routes (48%) render from one template**, the blog article. So
the actual build and review effort lives in the other 11 routes, which carry 11
templates between them — one template per route. (A 13th template, the
not-found placeholder, carries no routes; see below.) `/careers` alone
contributes 6 single-use sections, more than any other route.

**The chrome partition has three values, not two**, and that is deliberate
rather than an inconsistency: `marketing-home` (1 route), `marketing-site` (19
routes) and `none` (1 route). The homepage ships *empty* primary-nav and
footer-link containers while every other marketing route populates them — a
real quirk of the original that the clone reproduces rather than normalising.
`/log-in` is the single `none` route because it belongs to the app host's own
design system (a Mantine-derived SPA), sharing only the two font families and
the brand palette with the marketing site.

**One concrete reuse opportunity surfaced.** `hero.centered-title` is used by 3
routes (`/faq`, `/contact`, `/careers`) but is currently written **inline in all
three page files** rather than extracted into a component. It is the only
section in the project used by more than one template without a single shared
implementation. Every other multi-template section already points at one real
component via `implementedBy`.

## Things the IA records on purpose, which look like gaps

- **Three sections render deliberate empty states.** `proof.testimonials`,
  `proof.common-questions` and `content.faq-category-rows` sit on CMS
  collections that are genuinely empty on the live original, so they render a
  grey "No items found." box. `/faq` therefore carries no actual
  question-and-answer content, and there is no accordion behind it. This is
  reproduced, not missing — do not fill these with invented copy.
- **`hero.post` has no author, date, read-time, share or breadcrumb slot.** The
  original has none; there are zero `<time>` elements in its markup.
- **`content.load-more` is inert**, because the original's collection holds more
  posts than the ten rebuilt here and there is no further page to load.
- **`proof.video-facade` injects its player iframe only after a user click**, so
  page load makes no cross-origin request. Keep it that way.
- **`template.not-found` is an unmeasured placeholder with `routeCount: 0`.** The
  catch-all route renders the scaffold stub (`content.not-found-stub`), and the
  original site's 404 page was never visited, so no real layout is documented
  for it. It is listed so the IA doesn't silently omit a route the app responds
  to, but it carries none of the 21 counted routes. Replace it once the real
  404 has been measured.
- **`auth.login-form` is inert by construction** — no `action`, no endpoint,
  `autocomplete` disabled, submit cancelled.

## Content and licensing notes

This documents a **real, live company's site**, and some of what the clone
contains is not ours to reuse freely:

- **`proof.press-bar` carries four real third-party publication trademarks.**
  Neither these nor imitations of them should be reproduced in any derived or
  generated work.
- **`content.legal-prose` holds the site's real operative legal copy**, ported
  verbatim and character-verified against the live DOM. It needs sign-off from
  whoever owns legal/content before any real deployment, and must never be
  paraphrased or regenerated.
- **`content.rich-text` article bodies are original placeholder prose**, not the
  original articles. Post titles, covers and tags are genuine; the body text is
  not. Keep that distinction clear so placeholders aren't mistaken for source
  content.
- Brand assets (the wordmark, illustrations) and photographs of real people
  appear throughout and should not be regenerated or imitated.

## Relationship to `design-repo/`

The design-repo groups pages into **11 templates** because it merges pages whose
section sequences are identical (`/parents` + `/sitters`, and the two legal
pages). This IA keeps them as separate templates so each route stays
traceable, which is why the template counts differ. Both are correct for their
purpose; neither is a stale copy of the other.

## Provenance

Section order within each template is **real DOM order as rendered**, read from
the components in `src/`, cross-checked against the Playwright-measured specs on
disk (`CLONE_SPEC.md` and `spec/SPEC_*.md`) after three independent pixel-audit
passes. `meta.productionApproved` is `false`: the IA is accurate to the current
build, but the licensing items above are unresolved.
