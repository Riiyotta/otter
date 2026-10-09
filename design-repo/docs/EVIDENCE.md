# Evidence levels, and where things did not hold up

Every value in this repo cites a real file and line range
(`extraction/measured-values.json`, 66 entries). Each citation carries
**keywords that must literally appear inside the cited range**, which is what
catches the dangerous half of citation drift: a range that resolves fine but
describes the wrong lines. `verify_all.py` checks both halves.

## Evidence level per template

| Template | Level |
|---|---|
| home, audience-landing, trust-safety, faq-categories, contact, careers, blog-index, blog-post, legal-prose, auth-login | **measured** |
| **not-found** | **stub — NOT measured** |

`not-found` is recorded honestly. The original is a Webflow site-level 404 that
recon never visited, so there is no measured structure for it; the clone ships a
deliberate one-paragraph placeholder. It is kept at its real evidence level
rather than dressed up as a designed page, and a generator must not invent a 404
layout from the marketing vocabulary. One deeply-measured family member does not
launder the evidence level for the rest.

## Shared templates — grouped only after a real diff

Two templates cover two routes each. Neither was grouped by assumption:

- **audience-landing** (`/parents`, `/sitters`) — both page components were
  diffed directly. Both render the same five sections in the same order, with no
  extra or missing section on either side. The **only** structural difference is
  the CTA card's variant (narrow vs wide), which is exactly why structural rules
  key on `(section, variant)` rather than bare section id.
- **legal-prose** (`/terms-of-use`, `/privacy-policy`) — both render the identical
  single component with the same three-node shape, differing only in which
  document module they pass and in their declared per-route link repairs.

## Where the pre-existing specs did not hold up

Spot-checked per the methodology's independent-second-pass principle. Four real
corrections:

1. **The blog CTA band's href.** My first draft of the contract pinned it to the
   app-host sign-up URL by analogy with the other conversion sections. Direct
   inspection showed the real href is the literal **`#`** — a dead link on the
   original, kept as-is rather than repaired. The invented value was removed.
   This is exactly the plausible-but-unmeasured guess the methodology forbids.

2. **The `/sign-up` vs `/sign-up/welcome` split is per component, not per
   route.** The brief framed it as homepage-vs-subpages. Enumerating every real
   occurrence disproved that: the nav "Sign up" pill and the footer "Get started"
   CTA both target `…/sign-up` on **every** route, subpages included. Two source
   comments even contradict each other about what the original did; the code is
   unambiguous and was treated as authoritative. The graph rule was rewritten
   from a route-level heuristic to a per-section pinned enum.

3. **The "only outbound links" list was incomplete.** The brief listed the
   app-host CTAs, 4 footer socials and 3 Greenhouse links. Additional outbound
   hosts exist inside the **legal copy** (a help subdomain, a payment processor,
   ad-industry opt-out sites, a search provider), plus the Vimeo player in the
   click-to-play facade. These are content rather than chrome, which is probably
   why they were missed. The "no external **asset** requests" claim, separately,
   holds exactly: that grep returns nothing.

4. **The legal-text character counts differ from the brief.** The brief cited
   55,618 and 23,747 characters. Importing the modules and concatenating every
   string value gives roughly **56,170** and **23,964**. The difference is
   structural strings (hrefs, block type tags) that this method includes, so
   these figures are an **upper bound** on the body text. The brief's figures are
   plausible for body text alone. Recorded with the method stated rather than
   silently adopting either number.

Two further notes where the brief **did** hold up, but needed care:

- **The 7 clip paths.** A naive grep for `clipPath id=` returns **1**, not 7,
  which looks like a contradiction. It is not: the source defines a 7-entry array
  and renders one JSX `<clipPath>` element over it, so the source contains one
  literal and the DOM contains seven. The claim is correct; the grep was naive.
- **The CSS cascade ordering claim.** Verified directly against the built bundle
  rather than taken on trust — see `docs/CASCADE.md` for the byte offsets. It
  holds in the direction stated.

## Defects found in this repo's own work, by its own checks

Recorded because a check that has never caught anything may not be checking
anything:

1. **All 28 content contracts were dead code in the schema.** The per-section
   `if/then` branches were attached to the **root** object, where each `if`
   required a `section` property the root does not have — so every branch
   silently never fired. The adversarial suite caught it: five mutations that
   should have been rejected were not. Branches now live on the node items.
2. **A rule that was wrong, not an example that was wrong.** A first draft of the
   asset check banned the real-person photo role from PageSpecs outright, and the
   bundled example — which correctly references existing files — failed against
   it. The role is explicitly exposed, and what is banned is *synthesising* a new
   photograph. The rule was corrected and the correction was propagated into the
   graph's prose, not just the code.
3. **16 imprecise citations in this repo's own ledger**, all in-range but
   off-topic, caught by the keyword half of the citation check and fixed.
4. **A constant +1/+2 offset** across the colour-token citations, caught by
   eyeballing the first line of each cited range during the build.
