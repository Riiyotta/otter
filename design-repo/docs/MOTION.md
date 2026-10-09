# Motion inventory

The engine is **Webflow IX2** — not GSAP, not Framer Motion, and there is no
`IntersectionObserver` in the original site code. The complete inventory is
genuinely tiny. The motion schema is **closed** (`additionalProperties: false`)
to exactly these fields, so a generated PageSpec cannot smuggle in an invented
one and still validate.

## Everything that moves on the whole marketing site

| What | Where | Timing |
|---|---|---|
| **One** scroll reveal | `.section-header.cc-tabas-header`, on `/` **only** | `slideInBottom`, 1000ms, `cubic-bezier(.165,.84,.44,1)`, trigger at 20% of viewport height, fires **once** |
| Mobile nav open | `≤991px` | ~600ms, `outQuart`, **independent delays per property** |
| Mobile nav close | `≤991px` | ~500ms, `outQuart`, asymmetric delays |
| Tabs widget (desktop) | `/parents`, `/sitters` | opacity 300ms + a 500ms `slideInFromBottom` that **replays on each switch** |
| Tabs widget (`≤991px`) | becomes an accordion | **asymmetric**: 100ms delay then 300ms on open; **no delay on close** |
| `.nav_link-current-icon` blob reveal | behind the site's single `min-width:992px` query | 300ms |
| CSS hover transitions | `.btn` and friends | colour trio only, 300ms `outQuart` |

The one easing curve is `outQuart` = `cubic-bezier(0.165, 0.84, 0.44, 1)`.
The only measured durations are 200/300/400/500/1000ms; the only delays are
0/100/200ms. The schema's enums are closed to exactly those.

## States that deliberately have NO transition — keep them that way

- `.btn.cc-white`'s **box-shadow** (absent from the transition list, so it snaps)
- `.btn.cc-white`'s `:active` **`transform: scale(.95)`** (instant)
- **`.button-primary`** declares no transition at all — hover and `:active` are
  both instant
- **Blog cards** have no hover state and no transition

Adding a transition to any of these is a regression, not an improvement.

## What does not exist anywhere

- **No stagger.** Anywhere. There is no `stagger` field in the motion schema.
- No marquee, no parallax, no canvas, no Lottie.
- **No video autoplay.** Zero `<video>` elements site-wide. `/trust-safety` is a
  click-to-play facade: 0 iframes and 0 third-party requests on load; the iframe
  is injected only after a user click.
- Swiper is loaded on `/parents` and `/sitters` with 1 live `.swiper` element but
  **0 slides** (the CMS collection is empty). No autoplay, no loop.
- **The homepage reveal does not run on `/parents` or `/sitters`.** They carry
  the same class but have no `data-w-id` and no inline `opacity:0`. Do not add a
  reveal there.

## `prefers-reduced-motion`

**The original ships no `@media (prefers-reduced-motion)` block at all.**

This repo nonetheless requires every node to declare `reducedMotionFallback`,
and the semantic validator enforces that it matches the section contract. That
is a deliberate **additive improvement** over the source, recorded as such
rather than presented as measured behaviour. The fallbacks are closed to
`none`, `instant-visible` and `instant-switch`.
