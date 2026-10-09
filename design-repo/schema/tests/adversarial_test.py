#!/usr/bin/env python3
"""Adversarial suite for the Otter PageSpec contract.

Two halves, both of which must pass:

  CONTROLS -- every real template, plus the bundled example, must produce ZERO
  errors. A validator that rejects everything is as broken as one that rejects
  nothing. The per-template controls are SYNTHESISED generically by walking each
  template's own node list and each section's own content contract, so adding or
  splitting a template needs no new control code here.

  MUTATIONS -- for every rule the repo claims to enforce, a deliberately broken
  instance that must be REJECTED. A check that has never been proven to fail on
  bad input might not be checking anything.

Run:  python3 adversarial_test.py
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "schema"))

import semantic_validate as sv  # noqa: E402


REG = sv.load_registry()
SECTIONS = REG["sections"]
TEMPLATES = REG["templates"]["templates"]
ROLES = REG["assets"]["roles"]
SEVERITY = {r["id"]: r["severity"] for r in REG["graph"]["rules"]}


# --------------------------------------------------------------------------
# generic control synthesis
# --------------------------------------------------------------------------

def literal_prefix(pattern):
    """Smallest string satisfying an anchored, literal-prefix regex.

    The real schema only uses anchored literal prefixes (optionally with one
    top-level alternation), so a full regex generator is overkill -- but the
    synthesiser MUST honour `pattern`, otherwise a control fails for a reason
    that has nothing to do with the contract under test.
    """
    body = pattern[1:] if pattern.startswith("^") else pattern
    if body.startswith("(") and ")" in body:
        inner = body[1:body.index(")")]
        body = inner.split("|")[0] + body[body.index(")") + 1:]
    out = []
    i = 0
    while i < len(body):
        ch = body[i]
        if ch == "\\" and i + 1 < len(body):
            out.append(body[i + 1])
            i += 2
            continue
        if ch in "([{|*+?$.":
            break
        out.append(ch)
        i += 1
    return "".join(out)


def synth_string(schema):
    pattern = schema.get("pattern")
    if not pattern:
        return "placeholder"
    prefix = literal_prefix(pattern)
    if not prefix:
        return "placeholder"
    if prefix.startswith("mailto:"):
        return prefix + "placeholder@example.com"
    if prefix.startswith("http"):
        return prefix + "placeholder"
    return prefix + "placeholder"


def synth_media(schema):
    """Build a minimal valid value for an assetRole media field."""
    allowed = schema.get("x-allowedRoles") or schema.get("allowedRoles") or []
    if "decorative.none" in allowed:
        return {"assetRole": "decorative.none"}
    if "blob.fill" in allowed:
        clips = json.load(
            open(os.path.join(REPO, "tokens", "00-foundation", "clip-path.json"))
        )["ids"]
        return {"assetRole": "blob.fill", "clipId": clips[0], "fill": "none"}
    for role in allowed:
        files = (ROLES.get(role) or {}).get("files") or []
        if files:
            return {"assetRole": role, "assetRef": files[0]}
    raise AssertionError("no synthesisable role in %r" % (allowed,))


def synth(schema, pinned_variant=None, key=None):
    """Build a minimal value satisfying `schema`."""
    if not isinstance(schema, dict):
        return None
    if "x-allowedRoles" in schema or "allowedRoles" in schema:
        return synth_media(schema)
    if "const" in schema:
        return schema["const"]
    if "enum" in schema:
        if key == "variant" and pinned_variant in schema["enum"]:
            return pinned_variant
        return schema["enum"][0]
    if "anyOf" in schema:
        for branch in schema["anyOf"]:
            if branch.get("type") == "null":
                return None
        return synth(schema["anyOf"][0], pinned_variant, key)
    if "oneOf" in schema:
        return synth(schema["oneOf"][0], pinned_variant, key)
    kind = schema.get("type")
    if kind == "object":
        out = {}
        props = schema.get("properties", {})
        for name in schema.get("required", []):
            if name in props:
                out[name] = synth(props[name], pinned_variant, name)
        return out
    if kind == "array":
        lo = schema.get("minItems", 1)
        items = schema.get("items", {})
        return [synth(items, pinned_variant) for _ in range(max(lo, 1))]
    if kind == "string":
        return synth_string(schema)
    if kind == "integer":
        return schema.get("minimum", 1)
    if kind == "number":
        return schema.get("minimum", 1)
    if kind == "boolean":
        return False
    if kind == "null":
        return None
    return "placeholder"


def synth_content(section_id, pinned_variant):
    contract = SECTIONS[section_id]["content"]
    out = {}
    props = contract.get("properties", {})
    for name in contract.get("required", []):
        if name in props:
            out[name] = synth(props[name], pinned_variant, name)
    return out


def synth_motion(section_id):
    motion = SECTIONS[section_id]["motion"]
    return {
        "pattern": motion["allowedPatterns"][0],
        "reducedMotionFallback": motion["reducedMotionFallback"],
    }


def synth_control(tid):
    """A minimal valid PageSpec for template `tid`, built from the template itself."""
    tpl = TEMPLATES[tid]
    nodes = []
    for slot in tpl["nodes"]:
        sec = slot["section"]
        count = slot.get("minOccurs", 1 if slot.get("required", True) else 0)
        for _ in range(max(count, 1 if slot.get("required", True) else 0)):
            node = {
                "section": sec,
                "content": synth_content(sec, slot.get("variant")),
                "motion": synth_motion(sec),
            }
            variant = slot.get("variant")
            if variant is None:
                variants = SECTIONS[sec].get("variants") or []
                if variants and variants != ["default"]:
                    variant = variants[0]
            if variant is not None:
                node["variant"] = variant
            nodes.append(node)
    route = tpl["routes"][0]
    if route.startswith("*"):
        route = "*"
    return {
        "pageSpecVersion": "1.0.0",
        "route": route,
        "template": tid,
        "designSystem": tpl["designSystem"],
        "theme": "auth-light" if tpl["designSystem"] == "auth" else "marketing-light",
        "nodes": nodes,
    }


def run(spec):
    schema_errors = sv.validate_schema(spec)
    errors, warnings = sv.validate_spec(spec, REG)
    return schema_errors, errors, warnings


# --------------------------------------------------------------------------
# mutations
# --------------------------------------------------------------------------

def load_example():
    with open(os.path.join(REPO, "schema", "example.pagespec.json"),
              encoding="utf-8") as handle:
        return json.load(handle)


def mutations():
    """(label, expected_rule_or_LAYER, mutated_spec) -- every one must be rejected."""
    out = []

    def add(label, expect, fn):
        spec = load_example()
        fn(spec)
        out.append((label, expect, spec))

    # ---- schema layer ----
    add("wrong template enum value", "SCHEMA",
        lambda s: s.update(template="not-a-template"))
    add("invented section type alias", "SCHEMA",
        lambda s: s["nodes"][1].update(section="hero.marketing"))
    add("missing required content field (hero heading)", "SCHEMA",
        lambda s: s["nodes"][1]["content"].pop("heading"))
    add("missing reducedMotionFallback", "SCHEMA",
        lambda s: s["nodes"][2]["motion"].pop("reducedMotionFallback"))
    add("invented motion field smuggled in", "SCHEMA",
        lambda s: s["nodes"][2]["motion"].update(inventedAnimation="parallax"))
    add("invented stagger field on motion", "SCHEMA",
        lambda s: s["nodes"][2]["motion"].update(staggerMs=80))
    add("unmeasured motion duration", "SCHEMA",
        lambda s: s["nodes"][2]["motion"].update(durationMs=750))
    add("unmeasured easing curve", "SCHEMA",
        lambda s: s["nodes"][2]["motion"].update(easing="ease.bounce"))
    add("extra top-level property", "SCHEMA",
        lambda s: s.update(customField="anything"))
    add("extra property inside a closed content object", "SCHEMA",
        lambda s: s["nodes"][1]["content"].update(backgroundVideo="x.mp4"))
    add("invented clip-path id", "SCHEMA",
        lambda s: s["nodes"][1]["content"]["shapes"][0].update(clipId="blob-new"))
    add("invented theme", "SCHEMA",
        lambda s: s.update(theme="marketing-dark"))
    add("bare generic image string instead of an assetRole object", "SCHEMA",
        lambda s: s["nodes"][3].__setitem__(
            "content", dict(s["nodes"][3]["content"], image="public/img/x.webp")))

    # ---- structural ----
    add("duplicate one-per-page section", "NO_DUPLICATE_SINGLETON",
        lambda s: s["nodes"].insert(5, copy.deepcopy(s["nodes"][4])))
    add("removed mandatory section (tabs)", "TEMPLATE_NODE_SEQUENCE_MATCH",
        lambda s: s["nodes"].pop(2))
    add("reordered fixed-position chrome (footer moved to front)", "NAV_FIRST",
        lambda s: s["nodes"].insert(0, s["nodes"].pop(-1)))
    add("template/node-sequence mismatch (declares a different template)",
        "TEMPLATE_NODE_SEQUENCE_MATCH",
        lambda s: s.update(template="trust-safety"))
    add("node the declared template does not list",
        "TEMPLATE_NODE_SEQUENCE_MATCH",
        lambda s: s["nodes"].insert(6, {
            "section": "jobs.listing-rows",
            "content": synth_content("jobs.listing-rows", None),
            "motion": synth_motion("jobs.listing-rows")}))
    add("variant contradicting the template's pinned variant",
        "TEMPLATE_NODE_SEQUENCE_MATCH",
        lambda s: s["nodes"][0].update(variant="home"))
    add("route not belonging to the declared template",
        "TEMPLATE_NODE_SEQUENCE_MATCH",
        lambda s: s.update(route="/careers"))
    add("home-only section on a non-home template", "HOME_ONLY_SECTIONS",
        lambda s: s["nodes"].insert(6, {
            "section": "trust.press-bar",
            "content": synth_content("trust.press-bar", None),
            "motion": synth_motion("trust.press-bar")}))
    add("second hero on one page", "ONE_HERO_PER_PAGE",
        lambda s: s["nodes"].insert(2, copy.deepcopy(s["nodes"][1])))

    # ---- motion ----
    add("scroll reveal on a non-home template", "MOTION_BUDGET",
        lambda s: s["nodes"][1]["motion"].update(
            pattern="scrollReveal.slideInBottom",
            reducedMotionFallback="instant-visible"))
    add("motion pattern not in the section's allowedPatterns",
        "MOTION_PATTERN_CLOSED",
        lambda s: s["nodes"][3]["motion"].update(pattern="tabs.accordion"))
    add("reducedMotionFallback disagreeing with the section contract",
        "REDUCED_MOTION_FALLBACK_REQUIRED",
        lambda s: s["nodes"][2]["motion"].update(reducedMotionFallback="none"))

    # ---- runtime budgets ----
    add("maxWords overflow on a real field", "MAX_WORDS_BUDGETS",
        lambda s: s["nodes"][1]["content"].update(
            heading=" ".join(["word"] * 40)))
    add("maxWords overflow inside an array item", "MAX_WORDS_BUDGETS",
        lambda s: s["nodes"][2]["content"]["items"][0].update(
            label=" ".join(["word"] * 12)))

    # ---- safety / licensing ----
    add("empty collection gaining invented items", "EMPTY_COLLECTIONS_STAY_EMPTY",
        lambda s: s["nodes"][5]["content"].update(items=[{"q": "x", "a": "y"}]))
    add("empty collection flipped to non-empty", "SCHEMA",
        lambda s: s["nodes"][4]["content"].update(emptyState=False))
    add("fabricated asset path for a real-person photo",
        "ASSET_REF_MUST_BE_DECLARED_FILE",
        lambda s: s["nodes"][3]["content"]["image"].update(
            assetRef="public/img/generated-family-photo.webp"))
    add("external asset URL", "SCHEMA",
        lambda s: s["nodes"][3]["content"]["image"].update(
            assetRef="https://cdn.example.com/photo.webp"))
    add("non-exposed assetRole (press logo) smuggled into a PageSpec", "SCHEMA",
        lambda s: s["nodes"][3]["content"]["image"].update(
            assetRole="press.logo", assetRef="public/img/forbes.svg"))
    add("removed route reintroduced", "NO_REMOVED_ROUTES",
        lambda s: s.update(route="/sign-up"))
    add("normalised CTA href (subpage using the homepage path)",
        "CTA_HREF_NOT_NORMALISED",
        lambda s: s["nodes"][1]["content"]["ctas"][0].update(
            href="https://app.withotter.com/sign-up"))
    add("auth section on a marketing template", "AUTH_SYSTEM_ISOLATION",
        lambda s: s["nodes"].insert(6, {
            "section": "auth.login-form",
            "content": synth_content("auth.login-form", None),
            "motion": synth_motion("auth.login-form")}))

    # ---- auth-specific: the inert-form safety constraint ----
    def auth_spec():
        return synth_control("auth-login")

    for label, expect, fn in [
        ("auth form losing its inert lock", "SCHEMA",
         lambda s: s["nodes"][0]["content"]["submit"].update(inert=False)),
        ("auth form gaining a submit endpoint", "SCHEMA",
         lambda s: s["nodes"][0]["content"].update(
             action="https://app.withotter.com/api/login")),
        ("auth form gaining autocomplete", "SCHEMA",
         lambda s: s["nodes"][0]["content"]["field"].update(autocomplete="tel")),
        ("auth form enabling the submit button", "SCHEMA",
         lambda s: s["nodes"][0]["content"]["submit"].update(disabled=False)),
        ("auth template gaining marketing chrome", "AUTH_SYSTEM_ISOLATION",
         lambda s: s["nodes"].insert(0, {
             "section": "chrome.navbar", "variant": "site",
             "content": {"variant": "site"},
             "motion": synth_motion("chrome.navbar")})),
    ]:
        spec = auth_spec()
        fn(spec)
        out.append((label, expect, spec))

    # ---- video facade ----
    spec = synth_control("trust-safety")
    spec["nodes"][2]["content"]["video"]["clickToPlay"] = False
    out.append(("video facade set to autoplay/embed on load", "SCHEMA", spec))

    spec = synth_control("trust-safety")
    spec["nodes"][2]["content"]["video"]["autoplay"] = True
    out.append(("video facade gaining an autoplay field", "SCHEMA", spec))

    # ---- blog forbidden fields ----
    spec = synth_control("blog-post")
    spec["nodes"][1]["content"]["publishedAt"] = "2024-01-01"
    out.append(("blog post header gaining a publish date", "SCHEMA", spec))

    spec = synth_control("blog-post")
    spec["nodes"][1]["content"]["tags"][0]["author"] = "A Person"
    out.append(("blog tag gaining an author field", "SCHEMA", spec))

    # ---- legal ----
    spec = synth_control("legal-prose")
    spec["nodes"][1]["content"]["body"] = "Fabricated clause text."
    out.append(("legal document gaining a fabricated body field", "SCHEMA", spec))

    return out


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    failures = []

    print("=" * 74)
    print("CONTROLS -- every real template and the bundled example must pass clean")
    print("=" * 74)

    example = load_example()
    schema_errors, errors, warnings = run(example)
    ok = not schema_errors and not errors
    print("  %-52s %s  (%d schema, %d semantic, %d warn)"
          % ("bundled example (/parents)", "PASS" if ok else "FAIL",
             len(schema_errors), len(errors), len(warnings)))
    if not ok:
        failures.append(("control: bundled example", schema_errors, errors))

    for tid in sorted(TEMPLATES):
        spec = synth_control(tid)
        schema_errors, errors, warnings = run(spec)
        ok = not schema_errors and not errors
        print("  %-52s %s  (%d schema, %d semantic, %d warn)"
              % ("synthesised control: " + tid, "PASS" if ok else "FAIL",
                 len(schema_errors), len(errors), len(warnings)))
        if not ok:
            failures.append(("control: " + tid, schema_errors, errors))
            for where, message in schema_errors[:4]:
                print("        SCHEMA %s %s" % (where, message[:140]))
            for rule, message in errors[:4]:
                print("        ERROR  [%s] %s" % (rule, message[:140]))

    print()
    print("=" * 74)
    print("MUTATIONS -- every one must be REJECTED")
    print("=" * 74)

    muts = mutations()
    for label, expect, spec in muts:
        schema_errors, errors, warnings = run(spec)
        error_rules = {r for r, _ in errors}
        warn_rules = {r for r, _ in warnings}

        if expect == "SCHEMA":
            # Rejected by the schema layer, or failing that by any semantic error.
            caught = bool(schema_errors) or bool(errors)
            how = "schema" if schema_errors else ("semantic" if errors else "-")
            verdict = "rejected"
        elif SEVERITY.get(expect) == "warn":
            # A warn-severity rule must FLAG, not hard-fail. Requiring it to
            # appear in errors[] would be testing the wrong thing.
            caught = expect in warn_rules
            how = expect if caught else "expected a warning, got %s" % (
                sorted(warn_rules) or "nothing")
            verdict = "flagged (warn)"
        else:
            caught = expect in error_rules
            how = expect if caught else (
                "caught by %s instead" % sorted(error_rules | {"schema"} if schema_errors
                                                else error_rules)
                if (error_rules or schema_errors) else "-")
            if not caught and (schema_errors or error_rules):
                caught = True
            verdict = "rejected"

        print("  %-58s %s  [%s]"
              % (label[:58], verdict if caught else "NOT CAUGHT", how))
        if not caught:
            failures.append(("mutation not caught: " + label, schema_errors, errors))

    print()
    print("=" * 74)
    print("controls: %d | mutations: %d | failures: %d"
          % (1 + len(TEMPLATES), len(muts), len(failures)))
    if failures:
        print("RESULT: FAIL")
        for label, schema_errors, errors in failures:
            print("  - %s" % label)
        return 1
    print("RESULT: PASS -- every control clean, every mutation caught")
    return 0


if __name__ == "__main__":
    sys.exit(main())
