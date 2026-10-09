# Changelog

## 1.0.0 — initial build

Built from scratch (Situation A: no design-repo existed). Bottom-up per the
build methodology: tokens → primitives → components → sections → templates →
compatibility graph → schema → example → semantic validator → adversarial
tests → manifest/allowlist/docs.

### Added

- **Tokens.** Marketing foundation (colour, typography, radius, spacing,
  breakpoint, elevation, motion, clip-path), semantic roles, component
  overrides, layout, and `marketing-light`. The **9** `:root` custom properties
  are the whole palette; nothing was added that is not in the real stylesheet.
  Measured literals that are *not* brand tokens are kept in a separate
  `literals` block so nobody promotes them.
- **A separate `auth-light` token namespace** for the app host, deliberately not
  merged into the marketing set.
- **14 primitives, 18 components,
  28 section contracts**, each with `additionalProperties: false`,
  a `maxWords` budget on every text field (derived from the measured longest
  real instance), structured per-breakpoint responsive fields, and a closed
  motion block.
- **11 templates** over **13** route patterns,
  with structured node objects so `required`/`repeatable`/`variant` are
  machine-enforceable. Two shared templates were grouped only after diffing the
  real page components directly.
- **28 compatibility rules**, every one derived from
  `templates.json`'s actual node sequences at the time it was written. The
  hero-less, chrome-less and home-only sets are **computed**, not hand-listed,
  so they cannot silently diverge from the validator.
- **Draft-07 schema** with closed `template`, `section`, `assetRole`, `clipId`,
  motion-pattern, duration, delay and easing enums. Polymorphic media fields use
  `oneOf` of **fully independent** schemas rather than a shared base plus
  patches, because draft-07's `additionalProperties:false` on a shared base
  cannot see properties a sibling `allOf` branch adds.
- **A vendored, dependency-free draft-07 validator** (`schema/_draft7.py`), so
  the repo needs no `pip install` and the self-containment test depends on the
  repo's own contents. Cross-checked against the reference `jsonschema` package
  on every control and mutation; both agree on all cases.
- **Semantic validator** with 20 checks, including the template↔nodes
  cross-reference.
- **Adversarial suite**: 12 controls (the bundled example plus one generically
  **synthesised** control per template, so a future template split needs no new
  control code) and **45** mutations.
- **`verify_all.py`** with 13 drift-proofed checks and a `--prove-drift` mode
  that injects 12 specific defects into scratch copies and asserts the matching
  check flips to FAIL.
- **Closed `assetRole` enum** wired through schema + allowlist + example, with
  explicit AI-generation and licensing guidance. Four compliance-critical roles
  are **pinned** to an exact policy value rather than merely constrained to the
  enum.
- **Docs**: `CASCADE.md`, `MOTION.md`, `CONSTRAINTS.md`, `EVIDENCE.md`.

### Fixed during this build

Found by this repo's own checks, and recorded because a check that has never
caught anything may not be checking anything:

- **All 28 content contracts were dead code in the schema.** The
  per-section `if/then` branches were attached to the root object, where each
  `if` required a `section` property the root does not have. Five mutations that
  should have been rejected were not. Branches moved onto the node items.
- **An asset rule that was wrong, not an example that was wrong.** A first draft
  banned the real-person photo role from PageSpecs outright, failing the bundled
  example, which correctly references existing files. The role is explicitly
  exposed; what is banned is *synthesising* a new photograph. Corrected, and the
  correction propagated into the graph's prose as well as the code.
- **An invented value.** The blog CTA band's href had been pinned to the
  app-host sign-up URL by analogy. The real href is the literal `#`, a dead link
  preserved on purpose.
- **A route-level rule that the data disproved.** `/sign-up` vs
  `/sign-up/welcome` is a per-**component** split, not per-route. Rewritten to a
  per-section pinned enum.
- **16 in-range but off-topic citations** in this repo's own ledger, caught by
  the keyword half of the citation check.
- **A constant +1/+2 offset** across the colour-token citations.
- **Two control failures caused by the test synthesiser**, not the contracts: it
  ignored `pattern`, so it produced invalid emails and job URLs. Made
  pattern-aware.

### Known limitations, stated rather than papered over

- `not-found` is a **stub, not measured**. The original 404 was never visited.
- The `/trust-safety` video iframe's **interior** was not measurable; only the
  outer box is spec-exact.
- Legal-text character counts are an **upper bound** (the measurement method
  includes structural strings). See `docs/EVIDENCE.md`.
- `prefers-reduced-motion` does not exist in the original. Requiring
  `reducedMotionFallback` is a deliberate **additive** improvement, labelled as
  such.
- There is **no per-instance token-override field** in the PageSpec schema, so
  adversarial coverage for token misuse lives at the catalog layer rather than
  the PageSpec layer.
