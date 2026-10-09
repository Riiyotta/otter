# https://withotter.com/ — pixel-audited React 18 + Vite + Tailwind v3 clone of the live site

Source: https://withotter.com/ — pixel-audited React 18 + Vite + Tailwind v3 clone of the live site · reference/original.html + reference/assets/with-otter-*.shared.34930fed5.min.css (saved homepage DOM and compiled Webflow stylesheet, byte-identical across every marketing route)
Status: **measured-from-source** · production approved: **false**
21 routes · 13 templates · 36 unique sections

> Generated from `ia.json` by `build.mjs`. Edit the JSON, not this file.

## Shape of the site

The largest 3 templates (Blog article, Homepage, Parents audience page) account for 12 of 21 routes (57%). The remaining 9 routes span 10 templates.

| template | routes | share |
|---|---:|---:|
| Blog article | 10 | 48% |
| Homepage | 1 | 5% |
| Parents audience page | 1 | 5% |
| Sitters audience page | 1 | 5% |
| Trust & Safety | 1 | 5% |
| FAQ | 1 | 5% |
| Contact | 1 | 5% |
| Careers | 1 | 5% |
| Blog index | 1 | 5% |
| Terms of Use | 1 | 5% |
| Privacy Policy | 1 | 5% |
| Log in | 1 | 5% |
| Not found (unmeasured placeholder) | 0 | 0% |

## Page chrome

**1 routes carry chrome = `marketing-home`** — Homepage.

**19 routes carry chrome = `marketing-site`** — Parents audience page, Sitters audience page, Trust & Safety, FAQ, Contact, Careers, Blog index, Blog article, Terms of Use, Privacy Policy, Not found (unmeasured placeholder).

**1 routes carry chrome = `none`** — Log in.

## Sections by reuse

How widely a section is shared determines whether it belongs in a shared
component library or stays local to its page.

| section | category | templates | routes | implementation | scope |
|---|---|---:|---:|---|---|
| `chrome.nav` | CHROME | 12 | 20 | `src/components/Nav.jsx` | Present on all 20 marketing routes; absent from the log-in screen, which has no marketing chrome. |
| `chrome.footer` | CHROME | 12 | 20 | `src/components/Footer.jsx` | Present on all 20 marketing routes; absent from the log-in screen. |
| `chrome.shape-defs` | CHROME | 12 | 20 | `src/components/ClipPathDefs.jsx` | Mounted once per page on all 20 marketing routes; not used by the log-in screen. |
| `hero.post` | HERO | 1 | 10 | `src/pages/BlogPost.jsx` | All 10 article routes. |
| `content.rich-text` | CONTENT | 1 | 10 | `src/components/blog/RichText.jsx` | All 10 article routes. |
| `content.related-posts` | CONTENT | 1 | 10 | `src/pages/BlogPost.jsx + src/components/blog/PostCard.jsx` | All 10 article routes. |
| `hero.page` | HERO | 3 | 3 | `src/components/pst/PageHero.jsx` | The 3 audience pages: parents, sitters, trust-safety. |
| `hero.centered-title` | HERO | 3 | 3 | `inline in src/pages/Faq.jsx, src/pages/Contact.jsx, src/pages/Careers.jsx` | 3 routes: faq, contact, careers. A reuse candidate — see README. |
| `hero.legal-title` | HERO | 2 | 2 | `src/components/legal/LegalDocument.jsx` | The 2 legal routes: terms-of-use and privacy-policy. |
| `explain.tabs` | EXPLAIN | 2 | 2 | `src/components/pst/Tabs.jsx` | 2 routes: parents and sitters. |
| `proof.testimonials` | PROOF | 2 | 2 | `src/components/pst/TestimonialsSlider.jsx` | 2 routes: parents and sitters. |
| `proof.common-questions` | PROOF | 2 | 2 | `src/components/pst/CommonQuestions.jsx` | 2 routes: parents and sitters. |
| `content.legal-prose` | CONTENT | 2 | 2 | `src/components/legal/LegalDocument.jsx + src/data/legal/` | The 2 legal routes. Holds real operative legal copy — see the README licensing note. |
| `convert.cta-card` | CONVERT | 2 | 2 | `src/components/pst/CtaCard.jsx` | 2 routes: parents and sitters. |
| `hero.home` | HERO | 1 | 1 | `src/components/Hero.jsx` | Homepage only — 1 route. |
| `hero.blog-index` | HERO | 1 | 1 | `src/pages/Blog.jsx` | Blog index only — 1 route. |
| `explain.beta-banner` | EXPLAIN | 1 | 1 | `src/components/BetaBanner.jsx` | Homepage only — 1 route. |
| `explain.how-it-works` | EXPLAIN | 1 | 1 | `src/components/HowItWorks.jsx` | Homepage only — 1 route. |
| `explain.join-card` | EXPLAIN | 1 | 1 | `src/components/HowItWorks.jsx` | Homepage only — 1 route. |
| `proof.press-bar` | PROOF | 1 | 1 | `src/components/TrustBar.jsx` | Homepage only — 1 route. |
| `proof.video-facade` | PROOF | 1 | 1 | `src/components/pst/VideoFacade.jsx` | Trust-safety only — 1 route. |
| `proof.trust-cards` | PROOF | 1 | 1 | `src/pages/TrustSafety.jsx` | Trust-safety only — 1 route. |
| `content.faq-category-rows` | CONTENT | 1 | 1 | `src/pages/Faq.jsx` | Faq only — 1 route. |
| `content.post-grid` | CONTENT | 1 | 1 | `src/pages/Blog.jsx + src/components/blog/PostCard.jsx` | Blog index only — 1 route. |
| `content.load-more` | CONTENT | 1 | 1 | `src/components/blog/LoadMore.jsx` | Blog index only — 1 route. |
| `convert.cta-band` | CONVERT | 1 | 1 | `src/components/blog/CtaBand.jsx` | Blog index only — 1 route. |
| `convert.contact-form` | CONVERT | 1 | 1 | `src/pages/Contact.jsx` | Contact only — 1 route. |
| `convert.contact-info` | CONVERT | 1 | 1 | `src/pages/Contact.jsx` | Contact only — 1 route. |
| `recruit.gap-intro` | RECRUIT | 1 | 1 | `src/pages/Careers.jsx` | Careers only — 1 route. |
| `recruit.gap-stats` | RECRUIT | 1 | 1 | `src/pages/Careers.jsx` | Careers only — 1 route. |
| `recruit.values` | RECRUIT | 1 | 1 | `src/pages/Careers.jsx` | Careers only — 1 route. |
| `recruit.benefits` | RECRUIT | 1 | 1 | `src/pages/Careers.jsx` | Careers only — 1 route. |
| `recruit.compensation` | RECRUIT | 1 | 1 | `src/pages/Careers.jsx` | Careers only — 1 route. |
| `recruit.positions` | RECRUIT | 1 | 1 | `src/pages/Careers.jsx` | Careers only — 1 route. |
| `auth.login-form` | AUTH | 1 | 1 | `src/pages/LogIn.jsx + src/components/auth/` | Log-in only — 1 route, the single route using the app host's design system. |
| `content.not-found-stub` | CONTENT | 1 | 0 | _not yet built_ | Catch-all fallback only — matches no named route, so it carries 0 of the 21 routes. |

**11 shared sections** appear in more than one template and belong in a component library.

**25 single-use sections** appear in exactly one template. Building these
as "reusable" components up front would be speculative — keep them page-local
until a second caller actually appears.

**1 section have no `implementedBy` yet** — not necessarily missing, just not linked to a component in this pass: `content.not-found-stub`.

## Templates

### Homepage — `template.home`

1 route · `/` · chrome: **marketing-home**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.shape-defs` | shared ×12 |
| 2 | CHROME | `chrome.nav` | shared ×12 |
| 3 | HERO | `hero.home` | page-local |
| 4 | EXPLAIN | `explain.beta-banner` | page-local |
| 5 | EXPLAIN | `explain.how-it-works` | page-local |
| 6 | EXPLAIN | `explain.join-card` | page-local |
| 7 | PROOF | `proof.press-bar` | page-local |
| 8 | CHROME | `chrome.footer` | shared ×12 |

### Parents audience page — `template.parents`

1 route · `/parents` · chrome: **marketing-site**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.shape-defs` | shared ×12 |
| 2 | CHROME | `chrome.nav` | shared ×12 |
| 3 | HERO | `hero.page` | shared ×3 |
| 4 | EXPLAIN | `explain.tabs` | shared ×2 |
| 5 | CONVERT | `convert.cta-card` | shared ×2 |
| 6 | PROOF | `proof.testimonials` | shared ×2 |
| 7 | PROOF | `proof.common-questions` | shared ×2 |
| 8 | CHROME | `chrome.footer` | shared ×12 |

### Sitters audience page — `template.sitters`

1 route · `/sitters` · chrome: **marketing-site**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.shape-defs` | shared ×12 |
| 2 | CHROME | `chrome.nav` | shared ×12 |
| 3 | HERO | `hero.page` | shared ×3 |
| 4 | EXPLAIN | `explain.tabs` | shared ×2 |
| 5 | CONVERT | `convert.cta-card` | shared ×2 |
| 6 | PROOF | `proof.testimonials` | shared ×2 |
| 7 | PROOF | `proof.common-questions` | shared ×2 |
| 8 | CHROME | `chrome.footer` | shared ×12 |

### Trust & Safety — `template.trust-safety`

1 route · `/trust-safety` · chrome: **marketing-site**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.shape-defs` | shared ×12 |
| 2 | CHROME | `chrome.nav` | shared ×12 |
| 3 | HERO | `hero.page` | shared ×3 |
| 4 | PROOF | `proof.video-facade` | page-local |
| 5 | PROOF | `proof.trust-cards` | page-local |
| 6 | CHROME | `chrome.footer` | shared ×12 |

### FAQ — `template.faq`

1 route · `/faq` · chrome: **marketing-site**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.shape-defs` | shared ×12 |
| 2 | CHROME | `chrome.nav` | shared ×12 |
| 3 | HERO | `hero.centered-title` | shared ×3 |
| 4 | CONTENT | `content.faq-category-rows` | page-local |
| 5 | CHROME | `chrome.footer` | shared ×12 |

### Contact — `template.contact`

1 route · `/contact` · chrome: **marketing-site**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.shape-defs` | shared ×12 |
| 2 | CHROME | `chrome.nav` | shared ×12 |
| 3 | HERO | `hero.centered-title` | shared ×3 |
| 4 | CONVERT | `convert.contact-form` | page-local |
| 5 | CONVERT | `convert.contact-info` | page-local |
| 6 | CHROME | `chrome.footer` | shared ×12 |

### Careers — `template.careers`

1 route · `/careers` · chrome: **marketing-site**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.shape-defs` | shared ×12 |
| 2 | CHROME | `chrome.nav` | shared ×12 |
| 3 | HERO | `hero.centered-title` | shared ×3 |
| 4 | RECRUIT | `recruit.gap-intro` | page-local |
| 5 | RECRUIT | `recruit.gap-stats` | page-local |
| 6 | RECRUIT | `recruit.values` | page-local |
| 7 | RECRUIT | `recruit.benefits` | page-local |
| 8 | RECRUIT | `recruit.compensation` | page-local |
| 9 | RECRUIT | `recruit.positions` | page-local |
| 10 | CHROME | `chrome.footer` | shared ×12 |

### Blog index — `template.blog-index`

1 route · `/blog` · chrome: **marketing-site**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.shape-defs` | shared ×12 |
| 2 | CHROME | `chrome.nav` | shared ×12 |
| 3 | HERO | `hero.blog-index` | page-local |
| 4 | CONTENT | `content.post-grid` | page-local |
| 5 | CONTENT | `content.load-more` | page-local |
| 6 | CONVERT | `convert.cta-band` | page-local |
| 7 | CHROME | `chrome.footer` | shared ×12 |

### Blog article — `template.blog-post`

10 routes · `/blog-posts/{slug}` · chrome: **marketing-site**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.shape-defs` | shared ×12 |
| 2 | CHROME | `chrome.nav` | shared ×12 |
| 3 | HERO | `hero.post` | page-local |
| 4 | CONTENT | `content.rich-text` | page-local |
| 5 | CONTENT | `content.related-posts` | page-local |
| 6 | CHROME | `chrome.footer` | shared ×12 |

### Terms of Use — `template.terms`

1 route · `/terms-of-use` · chrome: **marketing-site**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.shape-defs` | shared ×12 |
| 2 | CHROME | `chrome.nav` | shared ×12 |
| 3 | HERO | `hero.legal-title` | shared ×2 |
| 4 | CONTENT | `content.legal-prose` | shared ×2 |
| 5 | CHROME | `chrome.footer` | shared ×12 |

### Privacy Policy — `template.privacy`

1 route · `/privacy-policy` · chrome: **marketing-site**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.shape-defs` | shared ×12 |
| 2 | CHROME | `chrome.nav` | shared ×12 |
| 3 | HERO | `hero.legal-title` | shared ×2 |
| 4 | CONTENT | `content.legal-prose` | shared ×2 |
| 5 | CHROME | `chrome.footer` | shared ×12 |

### Log in — `template.login`

1 route · `/log-in` · chrome: **none**

| # | category | section | |
|---:|---|---|---|
| 1 | AUTH | `auth.login-form` | page-local |

### Not found (unmeasured placeholder) — `template.not-found`

0 routes · `*` · chrome: **marketing-site**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.shape-defs` | shared ×12 |
| 2 | CHROME | `chrome.nav` | shared ×12 |
| 3 | CONTENT | `content.not-found-stub` | page-local |
| 4 | CHROME | `chrome.footer` | shared ×12 |

## Section reference

### CHROME

_Shared wrapper present on every marketing route: navigation, footer, and the SVG clip-path definitions the organic shapes reference._

**`chrome.nav`** — Non-sticky top navigation: wordmark, four primary links with an organic blob current-indicator, and log-in / sign-up actions. Ships two variants — the homepage renders an empty primary-link container, every other marketing route populates it.

· Present on all 20 marketing routes; absent from the log-in screen, which has no marketing chrome. · appears on 20 routes · implemented by `src/components/Nav.jsx`

**`chrome.footer`** — Two-card footer: a dark primary sign-up card and a white card, above a link region and a legal/copyright row. Like the nav, the homepage ships an empty link container while other routes populate three columns.

· Present on all 20 marketing routes; absent from the log-in screen. · appears on 20 routes · implemented by `src/components/Footer.jsx`

**`chrome.shape-defs`** — Invisible SVG defs block holding the seven objectBoundingBox clip paths that every organic stone and blob references by id. Renders nothing itself; no route adds new path data.

· Mounted once per page on all 20 marketing routes; not used by the log-in screen. · appears on 20 routes · implemented by `src/components/ClipPathDefs.jsx`

### HERO

_Page-opening header block, above or at the start of the main content._

**`hero.home`** — Homepage hero: large display headline, supporting copy, a single CTA, and a 72px-radius image container flanked by five clipped stone shapes.

· Homepage only — 1 route. · appears on 1 routes · implemented by `src/components/Hero.jsx`

**`hero.page`** — Shared audience-page hero: copy column plus a shape container carrying two clipped stones, with per-route fills and a per-route photo. Parametrised by props rather than duplicated.

· The 3 audience pages: parents, sitters, trust-safety. · appears on 3 routes · implemented by `src/components/pst/PageHero.jsx`

**`hero.centered-title`** — Simple centred page header — eyebrow plus display heading in a narrow container, with no image. Structurally the same block on each route but currently written inline in all three pages rather than extracted.

· 3 routes: faq, contact, careers. A reuse candidate — see README. · appears on 3 routes · implemented by `inline in src/pages/Faq.jsx, src/pages/Contact.jsx, src/pages/Careers.jsx`

**`hero.blog-index`** — Blog index header: display heading beside a full-bleed hero illustration, in a zero-padding section.

· Blog index only — 1 route. · appears on 1 routes · implemented by `src/pages/Blog.jsx`

**`hero.post`** — Article header: title, one to three tag pills, and a 1:1 cover image at 32px radius. Deliberately carries no author, date, read-time, share or breadcrumb slot — the original has none.

· All 10 article routes. · appears on 10 routes · implemented by `src/pages/BlogPost.jsx`

**`hero.legal-title`** — Legal document title band — eyebrow plus document title, rendered outside the main content element as on the original.

· The 2 legal routes: terms-of-use and privacy-policy. · appears on 2 routes · implemented by `src/components/legal/LegalDocument.jsx`

### EXPLAIN

_Product explanation: how the service works, capability tabs, programme status._

**`explain.beta-banner`** — Programme-status banner announcing beta availability and free access, with a sign-up CTA.

· Homepage only — 1 route. · appears on 1 routes · implemented by `src/components/BetaBanner.jsx`

**`explain.how-it-works`** — Section header plus three numbered steps on organic bullet backgrounds. Carries the site's only scroll-reveal animation, on its section header.

· Homepage only — 1 route. · appears on 1 routes · implemented by `src/components/HowItWorks.jsx`

**`explain.join-card`** — Large full-width card with a background illustration, growth-oriented copy and a primary join action. Rendered at the tail of the how-it-works section.

· Homepage only — 1 route. · appears on 1 routes · implemented by `src/components/HowItWorks.jsx`

**`explain.tabs`** — Dual-mode capability explainer: a pill tab strip with an absolutely-positioned card above 991px, which becomes a CSS-sibling-driven accordion at or below it. Open and close timings are deliberately asymmetric.

· 2 routes: parents and sitters. · appears on 2 routes · implemented by `src/components/pst/Tabs.jsx`

### PROOF

_Social proof and reassurance: press logos, testimonials, trust cards, video._

**`proof.press-bar`** — Press bar on a peach 40px-radius panel carrying four third-party publication logos. These are real external trademarks — see the licensing note in the README.

· Homepage only — 1 route. · appears on 1 routes · implemented by `src/components/TrustBar.jsx`

**`proof.testimonials`** — Testimonial slider with heading, lede and two circular arrow controls. The underlying CMS collection is empty on the original, so it renders a grey 'No items found.' empty state — intentional, not missing content.

· 2 routes: parents and sitters. · appears on 2 routes · implemented by `src/components/pst/TestimonialsSlider.jsx`

**`proof.common-questions`** — 'Common questions' heading above an empty CMS collection list. Renders the same deliberate grey empty state; there is no accordion behind it on the original.

· 2 routes: parents and sitters. · appears on 2 routes · implemented by `src/components/pst/CommonQuestions.jsx`

**`proof.video-facade`** — Click-to-play video facade: poster image and play button in a ~16:9 ivory box. The third-party player iframe is injected only after a user click, so page load makes no cross-origin request.

· Trust-safety only — 1 route. · appears on 1 routes · implemented by `src/components/pst/VideoFacade.jsx`

**`proof.trust-cards`** — Two rows of two white trust cards, each with an icon, heading and body, covering vetting and care standards.

· Trust-safety only — 1 route. · appears on 1 routes · implemented by `src/pages/TrustSafety.jsx`

### CONTENT

_The substantive body content of a route — prose, collections, article text._

**`content.faq-category-rows`** — Two static audience category rows ('For parents', 'For sitters'), each pairing a heading with an empty CMS collection list. Because both collections are empty on the original, this route carries no actual question-and-answer content.

· Faq only — 1 route. · appears on 1 routes · implemented by `src/pages/Faq.jsx`

**`content.post-grid`** — Collection grid: one featured post in a 50/50 row, then a three-up grid of standard cards. Both card variants are 4:3, and neither has any hover state or transition on the original.

· Blog index only — 1 route. · appears on 1 routes · implemented by `src/pages/Blog.jsx + src/components/blog/PostCard.jsx`

**`content.load-more`** — Pagination pill reproducing the original's Finsweet load-more control. Deliberately inert in the clone — the original's collection holds more posts than the ten rebuilt here, so there is no further page to load.

· Blog index only — 1 route. · appears on 1 routes · implemented by `src/components/blog/LoadMore.jsx`

**`content.rich-text`** — Article body prose block. Base 16/24 weight-500 body type at every breakpoint, with a flat 4rem heading top-margin that does not shrink on mobile. Article bodies in this clone are placeholder prose, not the original articles.

· All 10 article routes. · appears on 10 routes · implemented by `src/components/blog/RichText.jsx`

**`content.related-posts`** — 'Similar articles' row of three post cards in the wide container, reusing the standard card. Selection is next-in-collection-order here, because the original draws from posts outside the rebuilt set.

· All 10 article routes. · appears on 10 routes · implemented by `src/pages/BlogPost.jsx + src/components/blog/PostCard.jsx`

**`content.legal-prose`** — Hand-authored legal document body: a repeating rule-plus-heading-plus-paragraph pattern in the wide container, giving a wider measure than the article prose block. Lists are faked with line breaks exactly as the original does.

· The 2 legal routes. Holds real operative legal copy — see the README licensing note. · appears on 2 routes · implemented by `src/components/legal/LegalDocument.jsx + src/data/legal/`

**`content.not-found-stub`** — Placeholder body for the catch-all route: a single line of scaffold text in a plain section. The original site's 404 page was never visited or measured, so no real layout is documented. Not a copy of anything on withotter.com.

· Catch-all fallback only — matches no named route, so it carries 0 of the 21 routes. · appears on 0 routes

### CONVERT

_Blocks whose job is to get the visitor to act: CTA cards and bands, the contact form._

**`convert.cta-card`** — Large conversion card pairing an illustration with a heading and a sign-up action, in a wide or extra-wide variant depending on route.

· 2 routes: parents and sitters. · appears on 2 routes · implemented by `src/components/pst/CtaCard.jsx`

**`convert.cta-band`** — Horizontal conversion band with heading, supporting copy, an action and a supporting image.

· Blog index only — 1 route. · appears on 1 routes · implemented by `src/components/blog/CtaBand.jsx`

**`convert.contact-form`** — Five-field contact form with a screen-reader heading, plus custom success and failure blocks. Submits locally only — no endpoint and no network request — and carries no error styling, because the original defines none.

· Contact only — 1 route. · appears on 1 routes · implemented by `src/pages/Contact.jsx`

**`convert.contact-info`** — Supporting contact column: icon-led email and postal-address blocks beside the form.

· Contact only — 1 route. · appears on 1 routes · implemented by `src/pages/Contact.jsx`

### RECRUIT

_Careers-only blocks: the market-gap argument, values, benefits, compensation, open roles._

**`recruit.gap-intro`** — Narrative block introducing the childcare-market gap the company positions against, with supporting imagery.

· Careers only — 1 route. · appears on 1 routes · implemented by `src/pages/Careers.jsx`

**`recruit.gap-stats`** — Centred heading above a six-up responsive grid of statistic blocks, each an eyebrow, a large figure and a caption.

· Careers only — 1 route. · appears on 1 routes · implemented by `src/pages/Careers.jsx`

**`recruit.values`** — Operating-principles grid: six value cards with 72px icons, behind a screen-reader-only heading. Uses the full-width container rather than the narrow one.

· Careers only — 1 route. · appears on 1 routes · implemented by `src/pages/Careers.jsx`

**`recruit.benefits`** — Centred header plus a grid of six benefit items with 88px icons.

· Careers only — 1 route. · appears on 1 routes · implemented by `src/pages/Careers.jsx`

**`recruit.compensation`** — Centred header plus prose setting out the company's compensation philosophy.

· Careers only — 1 route. · appears on 1 routes · implemented by `src/pages/Careers.jsx`

**`recruit.positions`** — Open-roles list at an anchor target. Each row reuses the accordion item markup as a link pill out to the external applicant-tracking system, with a hover inversion that deliberately excludes its icon pill.

· Careers only — 1 route. · appears on 1 routes · implemented by `src/pages/Careers.jsx`

### AUTH

_Blocks belonging to the app host's own design system, not the marketing one._

**`auth.login-form`** — Log-in screen: wordmark, illustration, heading and a single phone-number field with a floating label, on a flat background with no card. Built from the app host's own design system, and deliberately inert — no action, no endpoint, autocomplete disabled, submit cancelled.

· Log-in only — 1 route, the single route using the app host's design system. · appears on 1 routes · implemented by `src/pages/LogIn.jsx + src/components/auth/`
