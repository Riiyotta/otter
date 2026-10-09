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

## What is here

| Count | |
|---:|---|
| **28** | section contracts (`sections/`) — the first layer with a real content contract |
| **14** | primitives (`primitives/`) |
| **18** | components (`components/`) |
| **11** | templates (`templates/templates.json`) — one per distinct **page shape** |
| **13** | route patterns, each mapped to exactly one template |
| **28** | compatibility rules (`compatibility/graph.json`) |
| **13** | asset roles (`assets/asset-roles.json`), a closed enum |
| **28** | per-section content branches in the schema |
| **189** | settable property paths in the allowlist |
| **66** | keyword-verified citations (`extraction/measured-values.json`) |
| **80** | JSON files in total |

All counts above are **recomputed from disk** by `verify_all.py`, which fails
the run on any mismatch.

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

The repo has **zero runtime dependencies** and needs **no `pip install`** — it
ships its own draft-07 validator (`schema/_draft7.py`), so the self-containment
test depends on the repo's contents rather than on the host environment.

```bash
python3 extraction/verify_all.py                # all 13 checks
python3 extraction/verify_all.py --prove-drift  # prove the drift checks catch drift
python3 extraction/verify_all.py --cross-check  # optional: diff against `jsonschema`
python3 schema/tests/adversarial_test.py        # controls + mutations
python3 schema/semantic_validate.py <spec.json> # validate one PageSpec
```

A PageSpec is valid only if it passes **both** `schema/pagespec.schema.json`
**and** `schema/semantic_validate.py`. The schema closes the enums; the semantic
validator enforces what JSON Schema structurally cannot — most importantly that
a PageSpec's `nodes[]` **matches the node list of the template it declares**,
cross-referencing the `template` field rather than inspecting the array in
isolation.

## Generating a page

1. Pick a `template` from the closed enum and read its node list.
2. Fill each node's `content` using only the paths in
   `tokens/llm/component-allowlist.json` → `sections.<id>.settableProperties`.
3. Respect every `maxWords` budget. Each field records the measured longest real
   instance it was derived from.
4. Every media field needs an `assetRole` from the closed enum. For any role
   that is not `may-generate-new`, `assetRef` must be a file that role **already
   declares** — you may reference an existing asset, never invent one.
5. Declare `motion.pattern` from the section's own `allowedPatterns`, and
   `reducedMotionFallback` matching the section contract.
6. Run both validators.

There is deliberately **no per-instance token-override field**. Styling is owned
entirely by the section and component contracts. This is stated explicitly so
nobody goes looking for a mechanism that was never built.

## Caveat

A design-repo is a **snapshot**, not a living mirror. The source project can be
upgraded afterwards with nothing re-checking these claims. If it has moved on,
re-diff the framework versions and factual claims in
`extraction/measured-values.json` against current source rather than trusting
this snapshot.
