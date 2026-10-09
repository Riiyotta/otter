# The CSS cascade fact that is load-bearing

This one is not trivia. Misunderstanding it caused real, measured visual
defects that audits had to find and fix. Any change to this design system has to
account for it.

## The fact

Vite emits the page-level stylesheets **before** `src/index.css`, and PostCSS
**flattens Tailwind's `@layer` entirely**. Therefore:

- `index.css` wins **every tie at equal specificity**.
- Page-level CSS must win on **specificity**, never on source order.

## Verified during this build, not taken on trust

Measured against the real built bundle (`dist/assets/index-*.css`, 56,057 bytes):

| Probe | Byte offset | Meaning |
|---|---|---|
| `@layer` occurrences | **0** | PostCSS flattened every layer |
| `.tab-trigger` (page CSS) | 1,771 | page stylesheet emitted early |
| `.w-inline-block{display:flex}` (page CSS attempt) | 10,979 | loses on order |
| `.w-inline-block{max-width:100%;display:inline-block}` (index.css) | 32,139 | wins on order |
| `@font-face` blocks (index.css) | 54,856+ | index.css sits at the END |
| `:root{--primary…}` (index.css) | ~55,800 | same |

So `index.css` content lands at the tail of the bundle, after every page
stylesheet. The ordering claim is confirmed in the direction stated.

## The two defects this caused

**1. Tab pills 60.8px instead of 48px.** A plain `.tab-trigger{display:flex}`
(specificity 0,1,0) silently lost to `index.css`'s
`.w-inline-block{display:inline-block}` (also 0,1,0, but later in the bundle).
The pills rendered `inline-block`, which changed their box and shifted every
element below them.

*Fix, in the repo today:* `a.tab-trigger{display:flex}` — specificity 0,1,1,
which wins regardless of emitted order.
Evidence: `src/styles/parents-sitters-trust.css:115-132`.

**2. Job pills 160px instead of 120px, arrow on the wrong side.**
`.faq-item.cc-listing` rendered `inline-block` for the same reason.

*Fix, in the repo today:* `a.faq-item, .faq-item.w-inline-block` — a 0,2,0
selector.
Evidence: `src/styles/faq-contact-careers.css:171-176`.

**3. The load-more pill's metrics.** Webflow's unstyled `.w-pagination-next`
base sets `font-size:14px`, which beats `.btn{font-size:1rem}`. Because `.btn`
expresses padding and radius in `em`, the whole pill scales down with it:
padding 12.25/17.5, radius 1386px, rendered 110×40.5. That is the original's
appearance and is preserved — won with a 0,2,0 `.w-pagination-next.btn`
selector rather than by relying on order.
Evidence: `src/styles/blog.css:169-179`.

## The rule for anything new

> Never rely on source order to beat `index.css`. Win on specificity.

A 0,1,0 selector that needs to override an `index.css` element-or-class rule
will lose. Add a tag qualifier or a second class.

## Related: Tailwind `preflight` and `container` are disabled on purpose

`tailwind.config.js` disables both core plugins. **Never recommend
re-enabling either.**

- **`preflight`** would apply `img{height:auto}`, collapsing images that rely on
  an intrinsic HTML `height` attribute.
- **`container`** collided with the project's own `.container` primitive.

**Corollary worth remembering:** because preflight is off, there is no
`img{height:auto}` reset, so **any image sized by CSS width alone needs an
explicit height, or its HTML `height` attribute wins.** Two real consequences:

- `Playdate.svg` renders 291.2×180 because of its `height="180"` attribute.
- One `/trust-safety` card icon renders narrower than the 104px CSS cap because
  it carries `width="96"` as an HTML attribute.

Evidence: `tailwind.config.js:3-12`.
