# Otter design-repo

A machine-validated **PageSpec system**: tokens, primitives, components,
sections, templates, a compatibility graph, a JSON Schema and two validators,
built so an LLM can generate new on-brand pages for this site **without
inventing colours, copy, structure or assets**.

Built from a pixel-audited clone of a real, live company's marketing site
(React 18 + Vite 5 + Tailwind CSS v3, react-router-dom 6). Every value cites a
real file and line range.

> **Status:** `design-review-pending` · `productionApproved: false`
> Legal-content sign-off, asset-licensing review and design review are all
> still **open**. See `registry.manifest.json` → `approvalFlags`.
> This repo is **not** to be published and the repository is **not** to be made
> public.

## Design policy binding (decided 2026-10-29)

Bound to the **N0 generic (non-SaaS) common policy `n0-design-constraints-common`
0.1.0** (Common IR 0.5, enforcement `hard-and-soft`), the common policy the N0
capture engine emits. `policy/design-policy.json`
(`consumer-service-marketplace-web` 1.0.0) is a **local extension** layered on
top of it, not the bound common policy. Not bound to
`n0-saas-design-constraints-common` (this is a consumer childcare marketplace,
not a B2B SaaS product). The decision was made by the repository owner and is
recorded in `policy/design-policy.json` → `approval`; `registry.manifest.json` →
`designPolicy.contentHash` hashes the files that enforce the policy and
`verify_all.py` recomputes it. The legal and licensing approval flags are a
separate matter and stay open.

## What is here

| Count | |
|---:|---|
| **30** | section contracts (`sections/`) (counts.sections) |
| **14** | primitives (`primitives/`) (counts.primitives) |
| **18** | components (`components/`) (counts.components) |
| **11** | templates (`templates/templates.json`), one per distinct page shape, in 6 families (counts.templates) |
| **13** | route patterns, each mapped to exactly one template (counts.routePatterns) |
| **48** | compatibility rules (`compatibility/graph.json`) (counts.compatibilityRules) |
| **21** | asset roles (`assets/asset-roles.json`), each with a closed `availability` (counts.assetRoles) |
| **30** | per-section content branches in the schema (counts.schemaContentBranches) |
| **203** | tokens in `tokens/llm/token-catalog.json`, generated from the token files (counts.catalogTokens) |
| **7** | page-level token slots in the PageSpec `tokens` object (counts.tokenSlots) |
| **7** | `mode: "generation"` example PageSpecs in `schema/examples/` (counts.generationExamples) |
| **96** | JSON files in total (counts.jsonFiles) |

These rows are checked against `registry.manifest.json` `counts`, which
`verify_all.py` recomputes from disk; either drifting fails the run.

## Two design systems, deliberately kept apart

- **`marketing`** — the Webflow-derived site, theme `marketing-light`. 12 routes.
- **`auth`** — the app host (`/log-in`): Vite + React + Mantine, theme
  `auth-light`. 1 route. A **separate** design system with its own grid,
  breakpoints, spacing, radii and line-height. Its tokens live in a separate
  namespace and **must never be merged** into the marketing set. The two share
  only the two font families and the brand hexes.

## Routes

| `*` | `not-found` | **stub — not measured** |
| `/` | `home` | measured |
| `/blog` | `blog-index` | measured |
| `/blog-posts/:slug` | `blog-post` | measured |
| `/careers` | `careers` | measured |
| `/contact` | `contact` | measured |
| `/faq` | `faq-categories` | measured |
| `/log-in` | `auth-login` | measured |
| `/parents` | `audience-landing` | measured |
| `/privacy-policy` | `legal-prose` | measured |
| `/sitters` | `audience-landing` | measured |
| `/terms-of-use` | `legal-prose` | measured |
| `/trust-safety` | `trust-safety` | measured |

`/sign-up` and `/welcome` were built and then **removed on purpose**. They must
**not** be reintroduced as templates — see `docs/CONSTRAINTS.md`.

## Read these before changing anything

| Doc | Why |
|---|---|
| **`docs/CONSTRAINTS.md`** | The hard constraints: the inert log-in form, the deliberately empty CMS collections, the click-to-play video, the licensing bans. |
| **`docs/CASCADE.md`** | The load-bearing CSS cascade fact, and the two real measured defects it caused. |
| **`docs/MOTION.md`** | The complete motion inventory, and the states that deliberately have **no** transition. |
| **`docs/EVIDENCE.md`** | Evidence level per template, and every place the pre-existing specs did not hold up. |

## Verifying

The repo has **zero runtime dependencies** and needs **no `pip install`**: it
ships its own draft-07 validator (`schema/_draft7.py`). Python 3 standard
library only.

```bash
python3 extraction/verify_all.py                     # every check (see its docstring)
python3 extraction/prove_drift.py --scratch <dir>    # inject one defect per scratch copy; each must be caught
python3 schema/tests/adversarial_test.py             # controls + mutations
python3 extraction/wrapper_gate.py --self-test       # the height gate's own cases
python3 schema/semantic_validate.py <spec.json>      # validate one PageSpec
python3 extraction/verify_all.py --cross-check       # optional: diff against `jsonschema`
```

Generated files are rebuilt and compared on every run; regenerate with `--write`:
`schema/build_schema.py`, `extraction/build_token_catalog.py`,
`extraction/build_source_identity.py`, `extraction/build_section_provenance.py`,
`extraction/build_generation_examples.py`, `extraction/policy_hash.py`.
Section heights are re-measured with `extraction/measure_sections.mjs` against a
local `vite preview` of the built clone (Playwright resolved at runtime).

A PageSpec is valid only if it passes **both** `schema/pagespec.schema.json`
**and** `schema/semantic_validate.py`. The schema closes the enums; the semantic
validator enforces what JSON Schema structurally cannot, most importantly that
a PageSpec's `nodes[]` **matches the node list of the template it declares**.

## Generating a page

1. Choose `mode`: `clone` (a faithful reconstruction of the source) or
   `generation` (a new page for a different brand).
2. Pick a `template` from the closed enum and read its node list.
3. Fill each node's `content` using only the paths in
   `tokens/llm/component-allowlist.json` → `sections.<id>.settableProperties`,
   within every `maxWords` budget.
4. Declare the seven page-level `tokens` (catalog paths allowed by
   `tokens/llm/token-policy.json` for the declared theme). No raw colours,
   lengths or font names anywhere.
5. Every media field needs an `assetRole` from the closed enum. In `clone` mode a
   `must-reuse-exact` role's `assetRef` must be a file the role already declares.
   In `generation` mode only `generation-safe` roles are allowed
   (`placeholder/`, `generated/`, `operator/` references), every URL must be on a
   reserved `.example` / `.invalid` domain, and `generationContext` replaces the
   chrome-owned identity (wordmark, app host, social links, press marks, video).
6. Declare `motion.pattern` from the section's own `allowedPatterns`, and
   `reducedMotionFallback` matching the section contract.
7. Run both validators. `schema/examples/` holds one passing generation example
   per template family.

## Honest limits

- Generation-mode leakage detection is **string-based** (normalised tokens and
  5-word shingles of the real source). It does not catch paraphrase,
  translation or text inside images. **No human has reviewed the derived
  patterns** in `schema/source-identity.json`.
- Section heights were measured on a local build of the clone at 1440px, not on
  the live site. Visual parity against the live site was **not** measured.
- The wrapper-gate whitelist is empty; nothing in this repo is an
  agent attestation presented as a human sign-off.

## Caveat

A design-repo is a **snapshot**, not a living mirror. The source project can be
upgraded afterwards with nothing re-checking these claims. If it has moved on,
re-diff the framework versions and factual claims in
`extraction/measured-values.json` against current source rather than trusting
this snapshot.
