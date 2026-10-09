# Hard constraints

These are not style preferences. Each one is either a safety/compliance
requirement or a deliberate decision that a generator must not quietly undo.
Every one is enforced by the schema, the semantic validator, or both.

## 1. `/sign-up` and `/welcome` must NOT be recreated as routes

They were built, then **removed on purpose by explicit decision**. Their CTAs
are now plain external links to the app host. The design-repo must not
reintroduce them as templates.

The path genuinely **differs per component** — do not normalise it:

| Component | Target |
|---|---|
| nav "Sign up", footer "Get started" | `…/sign-up` (on **every** route) |
| homepage hero / banner / join card | `…/sign-up` |
| light-split hero CTAs, CTA card | `…/sign-up/welcome` |
| blog CTA band | `#` — a dead link on the original, preserved deliberately |

`/log-in` **is** a local route.

*Enforced by:* closed `template` enum, per-section `href` enum,
`NO_REMOVED_ROUTES`, `CTA_HREF_NOT_NORMALISED`.

## 2. `/log-in` is a separate design system

The app host is a Vite + React + Mantine SPA, not Webflow. Different grid
(508px content column inside a 540px container), different breakpoints
(Mantine min-width em: 576/768/992/1200/1408 — **none of which fire on that
screen**), different spacing (4/8/16/32/48), different radii (12/16/24),
`line-height: 1.55`, and **no card or panel at all** (content sits flat on
`#f8f6f5`). It shares only the two font families and the brand hexes.

Its tokens live in `tokens/themes/auth-light.json`, in a **separate
namespace**. Never merge them into the marketing set.

*Enforced by:* `AUTH_SYSTEM_ISOLATION`.

## 3. `/log-in` is deliberately INERT and must stay that way

No `action`, no `method`, no endpoint, no `fetch`, `autocomplete="off"`, submit
only `preventDefault()`s. **Any generated instance of that template must never
acquire credential submission.**

*Enforced by:* schema `const` locks on `submit.inert`, `submit.disabled` and
`field.autocomplete`; `AUTH_FORM_MUST_STAY_INERT`; and four adversarial
mutations that each must be rejected.

## 4. No external requests

All 83 images and 6 fonts are local. Re-verified during this build: a grep for
absolute URLs ending in an asset extension across `src/` returns nothing.

The only intentional outbound links are the app-host CTAs, 4 footer socials, and
3 Greenhouse job links. **Correction to the original brief:** that list is not
exhaustive. Additional outbound hosts appear inside the **legal copy**
(a help subdomain, a payment processor, ad-industry opt-out sites, a search
provider) and one in the `/trust-safety` video facade (the Vimeo player, injected
only after a click). These are content, not chrome, and were not in the brief's
list.

*Enforced by:* `NO_EXTERNAL_ASSET_REQUESTS`, `ASSET_REF_MUST_BE_DECLARED_FILE`.

## 5. Empty CMS collections stay empty

The live original renders visible grey `#ddd` "No items found." boxes (10px
padding, 44px tall) where a CMS collection is genuinely empty, and the clone
reproduces them **on purpose**: the testimonials slider and "Common questions"
on `/parents` + `/sitters`, and **both** collections on `/faq`.

So **`/faq` genuinely has no FAQ content, and no accordion is rendered on it.**
(The accordion CSS exists in the design system and is used by the `/careers` job
rows, but it has zero live instances on `/faq`.)

**Do not treat these as missing content to be filled.** The contracts expose no
items array, so a generator has nothing to populate and cannot invent FAQ or
testimonial copy.

*Enforced by:* `const`-locked `emptyState`, `EMPTY_COLLECTIONS_STAY_EMPTY`.

## 6. The video is a click-to-play facade

0 iframes, 0 `<video>`, 0 third-party requests on load. A generated instance must
not autoplay or embed on load.

*Enforced by:* `const`-locked `video.clickToPlay`, `VIDEO_MUST_NOT_AUTOPLAY`.

## 7. The `.u-mb-0` weight quirk is intentional

`.u-mb-0` also declares `font-weight: 400`. Several `h1`s carry it, so they
compute Reckless Neue **400** while only the **900** Heavy file is hosted — the
browser **synthesises** a lighter face. **That is the original's correct
appearance.** Do not "fix" it.

Observed on `/sitters`, `/blog`, `/blog-posts/:slug`, `/careers` and `/contact`;
not on `/trust-safety`, `/faq` or `/parents`. Captured per instance as
`headingWeightQuirk`.

## 8. The blog post template has no fields the original lacks

Its only slots are the title, 1–3 tag pills, a forced 1:1 cover, the rich-text
body, and 3 related cards. There is **not a single `<time>` element** on any blog
page.

Deliberately absent: author, date, read-time, share links, breadcrumb,
back-to-blog, deck, subtitle, excerpt, inline CTA, next/prev.

*Enforced by:* `additionalProperties:false`, `BLOG_POST_FORBIDDEN_FIELDS`.

## 9. The 7 blob shapes are a closed vocabulary

7 clip-path ids, defined once, referenced by `clip-path: url(#id)` with
`clipPathUnits="objectBoundingBox"`. **No route adds new path data** — routes
only recombine the same 7 with different fills, images and rotations.

*Enforced by:* closed `clipId` enum.

## 10. Licensing — the source is a real, live company's site

The clone contains real proprietary content. A generator must **never** reproduce
or fabricate:

- **Real third-party press marks.** The press bar carries four actual
  publications' trademarks. The press-bar contract exposes a logo **count** and
  an eyebrow only — there is deliberately **no field** a generator could populate
  with a mark.
- **The brand wordmark and brand illustrations.** Chrome-owned; not exposed as a
  PageSpec field at all.
- **Photographs of real people.** Referencing an existing local file by path is
  allowed; **synthesising a new photograph of a person is not**, and is prevented
  structurally because the only legal values are paths that already exist.
- **Operative legal text.** The legal section exposes a `documentRef` enum of
  the two real documents and **no body field**, so legal prose cannot be carried
  by a PageSpec. **This is operative legal text and requires sign-off from
  whoever owns legal/content before any real deployment.** A generator must never
  fabricate or paraphrase legal clauses.

Four roles are **pinned** to an exact policy value, not merely constrained to the
enum, because they carry real legal weight: the wordmark, the press marks, real
people's photographs, and the legal text. `verify_all.py` checks the exact
pairing, and an adversarial case proves a mutation to a *different-but-still-valid*
enum member is caught — which a generic membership check cannot do.

**Also:** do not recommend making the repository public, and do not publish
anything from it.

## 11. Content provenance — placeholders vs real content

The blog **article bodies** in the source project are **original placeholder
prose**, written for the clone and deliberately **not** the original articles.
The real **titles, covers and tags are genuine**.

Keep that distinction explicit so nobody mistakes the placeholders for source
content, or tries to "restore" the originals.
