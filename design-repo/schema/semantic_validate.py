#!/usr/bin/env python3
"""Semantic validation for Otter PageSpecs.

Everything JSON Schema structurally cannot express. A PageSpec is valid only if
it passes BOTH schema/pagespec.schema.json AND this script.

Every check here corresponds to a rule id in compatibility/graph.json, and the
mapping is asserted by extraction/verify_all.py so the graph's prose and this
file's code cannot silently diverge (a real failure mode in prior builds: the
docs get corrected and the enforcing code keeps asserting the old, wrong fact).

Since 2.0.0 it also enforces the BASELINE rules:
  * mode (clone | generation): GENERATION_MODE_BRAND / _CUSTOMER / _PERSON / _URL / _EMBED / _CLAIM / _COPY /
    _ASSET / _SCREENSHOT / _LEGAL against schema/source-identity.json (derived from the real source by
    extraction/build_source_identity.py; string-based, normalised by schema/textnorm.py);
  * PINNED_AVAILABILITY (asset roles), RETRIEVAL_INELIGIBLE (runtime / empty-state UI), PINNED_THEME_RULES --
    pinned here in code and cross-checked against the registries by extraction/verify_all.py;
  * TOKEN_* rules against tokens/llm/token-catalog.json + tokens/llm/token-policy.json;
  * LEGAL_DOCUMENT_BINDING for the decomposed legal page.

Paths are derived from __file__, never hardcoded, so the repo keeps working when
it is extracted somewhere else.

Usage:
    python3 semantic_validate.py [pagespec.json ...]
    python3 semantic_validate.py            # validates the bundled example
"""
import json
import os
import re
import sys

sys.dont_write_bytecode = True

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "schema"))


def _load(*parts):
    with open(os.path.join(REPO, *parts), encoding="utf-8") as handle:
        return json.load(handle)


def load_registry():
    """Everything a check needs, loaded once. Paths derive from __file__."""
    sections = {}
    secdir = os.path.join(REPO, "sections")
    for name in sorted(os.listdir(secdir)):
        if name.endswith(".json"):
            data = _load("sections", name)
            sections[data["id"]] = data
    return {
        "sections": sections,
        "templates": _load("templates", "templates.json"),
        "graph": _load("compatibility", "graph.json"),
        "assets": _load("assets", "asset-roles.json"),
        "catalog": _load("tokens", "llm", "token-catalog.json"),
        "policy": _load("tokens", "llm", "token-policy.json"),
        "identity": _load("schema", "source-identity.json"),
    }


def _words(text):
    return len([w for w in re.split(r"\s+", text.strip()) if w])


# --------------------------------------------------------------------------
# checks -- each returns a list of (severity, rule_id, message)
# --------------------------------------------------------------------------

def check_template_sequence(spec, reg):
    """TEMPLATE_NODE_SEQUENCE_MATCH.

    THE check that matters most. A PageSpec's nodes[] is validated against the
    node list of the template it DECLARES -- not inspected in isolation. Without
    this cross-reference a PageSpec can contradict its own template and pass,
    which is the single most repeated bug class across prior design-repo builds.
    """
    out = []
    tid = spec.get("template")
    templates = reg["templates"]["templates"]
    if tid not in templates:
        return [("error", "TEMPLATE_NODE_SEQUENCE_MATCH",
                 "declared template %r is not a real template" % tid)]
    tpl = templates[tid]
    expected = tpl["nodes"]
    actual = spec.get("nodes", [])

    # Expand the template's repeatable nodes to the occurrence count actually used.
    ai = 0
    for slot in expected:
        sec = slot["section"]
        lo = slot.get("minOccurs", 1 if slot.get("required", True) else 0)
        hi = slot.get("maxOccurs", 1)
        if slot.get("repeatable") and "maxOccurs" not in slot:
            hi = len(actual)
        seen = 0
        while ai < len(actual) and actual[ai].get("section") == sec and seen < hi:
            node = actual[ai]
            pinned = slot.get("variant")
            if pinned is not None and node.get("variant") != pinned:
                out.append(("error", "TEMPLATE_NODE_SEQUENCE_MATCH",
                            "node %d (%s): template %r pins variant %r but the "
                            "PageSpec declares %r"
                            % (ai, sec, tid, pinned, node.get("variant"))))
            seen += 1
            ai += 1
        if seen < lo:
            out.append(("error", "TEMPLATE_NODE_SEQUENCE_MATCH",
                        "template %r requires %s at position %d (%d occurrence(s) "
                        "minimum) but the PageSpec has %d"
                        % (tid, sec, ai, lo, seen)))
    if ai < len(actual):
        extras = [n.get("section") for n in actual[ai:]]
        out.append(("error", "TEMPLATE_NODE_SEQUENCE_MATCH",
                    "PageSpec has %d node(s) template %r does not list, or lists "
                    "in a different order: %s" % (len(extras), tid, extras)))

    declared_route = spec.get("route")
    if declared_route and declared_route not in tpl["routes"]:
        out.append(("error", "TEMPLATE_NODE_SEQUENCE_MATCH",
                    "route %r is not one of template %r's routes %s"
                    % (declared_route, tid, tpl["routes"])))
    if spec.get("designSystem") != tpl["designSystem"]:
        out.append(("error", "AUTH_SYSTEM_ISOLATION",
                    "PageSpec designSystem %r does not match template %r's %r"
                    % (spec.get("designSystem"), tid, tpl["designSystem"])))
    return out


def check_one_hero(spec, reg):
    """ONE_HERO_PER_PAGE, with the DERIVED hero-less exception set."""
    sections = reg["sections"]
    nohero = reg["graph"]["derivedSets"]["NO_HERO_TEMPLATES"]["value"]
    heroes = [n for n in spec.get("nodes", [])
              if sections.get(n.get("section"), {}).get("category") == "hero"]
    if len(heroes) > 1:
        return [("error", "ONE_HERO_PER_PAGE",
                 "%d hero sections on one page" % len(heroes))]
    if not heroes and spec.get("template") not in nohero:
        return [("error", "ONE_HERO_PER_PAGE",
                 "template %r is not in NO_HERO_TEMPLATES %s but has no hero"
                 % (spec.get("template"), nohero))]
    return []


def check_hero_kind(spec, reg):
    """HERO_KIND_BY_ROUTE."""
    out = []
    for i, node in enumerate(spec.get("nodes", [])):
        if node.get("section") == "hero.dark-rounded" and spec.get("template") != "home":
            out.append(("error", "HERO_KIND_BY_ROUTE",
                        "node %d: hero.dark-rounded may only appear on the 'home' "
                        "template, not %r" % (i, spec.get("template"))))
    return out


def check_chrome_position(spec, reg):
    """NAV_FIRST and FOOTER_LAST, scoped to marketing templates."""
    out = []
    marketing = reg["graph"]["derivedSets"]["MARKETING_TEMPLATES"]["value"]
    nochrome = reg["graph"]["derivedSets"]["NO_CHROME_TEMPLATES"]["value"]
    tid = spec.get("template")
    nodes = spec.get("nodes", [])
    ids = [n.get("section") for n in nodes]
    if tid in nochrome:
        for i, sec in enumerate(ids):
            if sec.startswith("chrome."):
                out.append(("error", "AUTH_SYSTEM_ISOLATION",
                            "node %d: template %r renders no marketing chrome, but "
                            "%s is present" % (i, tid, sec)))
        return out
    if tid in marketing:
        if not ids or ids[0] != "chrome.navbar":
            out.append(("error", "NAV_FIRST",
                        "first node is %r, expected chrome.navbar"
                        % (ids[0] if ids else None)))
        if not ids or ids[-1] != "chrome.footer":
            out.append(("error", "FOOTER_LAST",
                        "last node is %r, expected chrome.footer"
                        % (ids[-1] if ids else None)))
        if ids.count("chrome.navbar") > 1 or ids.count("chrome.footer") > 1:
            out.append(("error", "NO_DUPLICATE_SINGLETON",
                        "chrome.navbar/chrome.footer may appear at most once each"))
    return out


def check_duplicates(spec, reg):
    """NO_DUPLICATE_SINGLETON and STATS_GRID_VARIANTS_MUST_DIFFER.

    Keyed on (section, variant), never bare section id -- stats.grid legitimately
    appears twice on /careers with different variants.
    """
    out = []
    sections = reg["sections"]
    counts = {}
    keyed = {}
    for node in spec.get("nodes", []):
        sec = node.get("section")
        counts[sec] = counts.get(sec, 0) + 1
        key = (sec, node.get("variant"))
        keyed[key] = keyed.get(key, 0) + 1
    for sec, n in sorted(counts.items()):
        contract = sections.get(sec, {})
        cons = contract.get("constraints", {})
        if cons.get("onePerPage") and n > 1:
            out.append(("error", "NO_DUPLICATE_SINGLETON",
                        "%s sets onePerPage but appears %d times" % (sec, n)))
        cap = cons.get("maxPerPage")
        if isinstance(cap, int) and n > cap:
            out.append(("error", "NO_DUPLICATE_SINGLETON",
                        "%s appears %d times, maxPerPage is %d" % (sec, n, cap)))
    for (sec, variant), n in sorted(keyed.items(), key=lambda kv: (kv[0][0], str(kv[0][1]))):
        contract = sections.get(sec, {})
        if n > 1 and contract.get("constraints", {}).get("variantKeyed"):
            out.append(("error", "STATS_GRID_VARIANTS_MUST_DIFFER",
                        "%s appears %d times with the SAME variant %r; the two real "
                        "instances use different variants"
                        % (sec, n, variant)))
    return out


def check_adjacency(spec, reg):
    """NO_ADJACENT_SAME_CATEGORY -- warn severity, with named exemptions."""
    out = []
    sections = reg["sections"]
    rule = next(r for r in reg["graph"]["rules"]
                if r["id"] == "NO_ADJACENT_SAME_CATEGORY")
    exempt = set(rule.get("exemptSections", []))
    ids = [n.get("section") for n in spec.get("nodes", [])]
    for i, (a, b) in enumerate(zip(ids, ids[1:])):
        if a in exempt or b in exempt:
            continue
        ca = sections.get(a, {}).get("category")
        cb = sections.get(b, {}).get("category")
        if ca and ca == cb:
            out.append(("warn", "NO_ADJACENT_SAME_CATEGORY",
                        "nodes %d and %d are both category %r (%s, %s)"
                        % (i, i + 1, ca, a, b)))
    return out


def check_home_only(spec, reg):
    """HOME_ONLY_SECTIONS."""
    out = []
    home_only = set(reg["graph"]["derivedSets"]["HOME_ONLY_SECTIONS"]["value"])
    if spec.get("template") == "home":
        return out
    for i, node in enumerate(spec.get("nodes", [])):
        if node.get("section") in home_only:
            out.append(("error", "HOME_ONLY_SECTIONS",
                        "node %d: %s may only appear on the 'home' template"
                        % (i, node.get("section"))))
    return out


def check_allowed_templates(spec, reg):
    """SECTION_TEMPLATE_ALLOWLIST."""
    out = []
    sections = reg["sections"]
    tid = spec.get("template")
    for i, node in enumerate(spec.get("nodes", [])):
        allowed = sections.get(node.get("section"), {}) \
                          .get("constraints", {}).get("allowedTemplates")
        if allowed and tid not in allowed:
            out.append(("error", "SECTION_TEMPLATE_ALLOWLIST",
                        "node %d: %s is restricted to templates %s, not %r"
                        % (i, node.get("section"), allowed, tid)))
    return out


def check_motion_pattern(spec, reg):
    """MOTION_PATTERN_CLOSED."""
    out = []
    sections = reg["sections"]
    for i, node in enumerate(spec.get("nodes", [])):
        contract = sections.get(node.get("section"))
        if not contract:
            continue
        allowed = contract["motion"]["allowedPatterns"]
        pattern = (node.get("motion") or {}).get("pattern")
        if pattern not in allowed:
            out.append(("error", "MOTION_PATTERN_CLOSED",
                        "node %d (%s): motion pattern %r is not in the section's "
                        "allowedPatterns %s"
                        % (i, node.get("section"), pattern, allowed)))
    return out


def check_reduced_motion(spec, reg):
    """REDUCED_MOTION_FALLBACK_REQUIRED."""
    out = []
    sections = reg["sections"]
    for i, node in enumerate(spec.get("nodes", [])):
        motion = node.get("motion") or {}
        if "reducedMotionFallback" not in motion:
            out.append(("error", "REDUCED_MOTION_FALLBACK_REQUIRED",
                        "node %d (%s): motion is missing reducedMotionFallback"
                        % (i, node.get("section"))))
            continue
        contract = sections.get(node.get("section"))
        if contract:
            want = contract["motion"]["reducedMotionFallback"]
            got = motion["reducedMotionFallback"]
            if got != want:
                out.append(("error", "REDUCED_MOTION_FALLBACK_REQUIRED",
                            "node %d (%s): reducedMotionFallback is %r but the "
                            "section contract declares %r"
                            % (i, node.get("section"), got, want)))
    return out


def check_motion_budget(spec, reg):
    """MOTION_BUDGET."""
    out = []
    reveals = [n for n in spec.get("nodes", [])
               if (n.get("motion") or {}).get("pattern", "").startswith("scrollReveal.")]
    if len(reveals) > 1:
        out.append(("error", "MOTION_BUDGET",
                    "%d scroll reveals on one page; the whole site has exactly one"
                    % len(reveals)))
    if reveals and spec.get("template") != "home":
        out.append(("error", "MOTION_BUDGET",
                    "scrollReveal.* may only appear on the 'home' template, not %r "
                    "(/parents and /sitters carry the same class but no trigger)"
                    % spec.get("template")))
    return out


def check_design_system_isolation(spec, reg):
    """AUTH_SYSTEM_ISOLATION."""
    out = []
    sections = reg["sections"]
    want = spec.get("designSystem")
    for i, node in enumerate(spec.get("nodes", [])):
        contract = sections.get(node.get("section"))
        if contract and contract["designSystem"] != want:
            out.append(("error", "AUTH_SYSTEM_ISOLATION",
                        "node %d: %s belongs to design system %r, but the PageSpec "
                        "declares %r. The auth (app host) and marketing systems are "
                        "separate and must not be mixed."
                        % (i, node.get("section"), contract["designSystem"], want)))
    theme = spec.get("theme")
    if want == "auth" and theme != "auth-light":
        out.append(("error", "AUTH_SYSTEM_ISOLATION",
                    "designSystem 'auth' requires theme 'auth-light', got %r" % theme))
    if want == "marketing" and theme != "marketing-light":
        out.append(("error", "AUTH_SYSTEM_ISOLATION",
                    "designSystem 'marketing' requires theme 'marketing-light', got %r"
                    % theme))
    return out


def check_auth_inert(spec, reg):
    """AUTH_FORM_MUST_STAY_INERT -- a hard safety constraint."""
    out = []
    for i, node in enumerate(spec.get("nodes", [])):
        if node.get("section") != "auth.login-form":
            continue
        content = node.get("content") or {}
        submit = content.get("submit") or {}
        field = content.get("field") or {}
        if submit.get("inert") is not True:
            out.append(("error", "AUTH_FORM_MUST_STAY_INERT",
                        "node %d: submit.inert must be true. A generated log-in "
                        "screen must never acquire credential submission." % i))
        if submit.get("disabled") is not True:
            out.append(("error", "AUTH_FORM_MUST_STAY_INERT",
                        "node %d: submit.disabled must be true" % i))
        if field.get("autocomplete") != "off":
            out.append(("error", "AUTH_FORM_MUST_STAY_INERT",
                        "node %d: field.autocomplete must be 'off'" % i))
        for banned in ("action", "method", "endpoint", "onSubmit", "fetch"):
            if banned in content:
                out.append(("error", "AUTH_FORM_MUST_STAY_INERT",
                            "node %d: %r is forbidden on an inert auth form"
                            % (i, banned)))
    return out


def check_empty_collections(spec, reg):
    """EMPTY_COLLECTIONS_STAY_EMPTY."""
    out = []
    locked = ("testimonials.slider-empty", "faq.common-questions-empty",
              "faq.category-empty")
    for i, node in enumerate(spec.get("nodes", [])):
        if node.get("section") not in locked:
            continue
        content = node.get("content") or {}
        if content.get("emptyState") is not True:
            out.append(("error", "EMPTY_COLLECTIONS_STAY_EMPTY",
                        "node %d (%s): emptyState must stay true. The CMS collection "
                        "is genuinely empty on the original and the grey 'No items "
                        "found.' box is intentional, not missing content."
                        % (i, node.get("section"))))
        for banned in ("items", "questions", "testimonials", "quotes", "faqs"):
            if banned in content:
                out.append(("error", "EMPTY_COLLECTIONS_STAY_EMPTY",
                            "node %d (%s): %r is forbidden -- a generator must not "
                            "invent FAQ or testimonial copy"
                            % (i, node.get("section"), banned)))
    return out


def check_video_facade(spec, reg):
    """VIDEO_MUST_NOT_AUTOPLAY."""
    out = []
    for i, node in enumerate(spec.get("nodes", [])):
        if node.get("section") != "trust.video-and-cards":
            continue
        video = (node.get("content") or {}).get("video") or {}
        if video.get("clickToPlay") is not True:
            out.append(("error", "VIDEO_MUST_NOT_AUTOPLAY",
                        "node %d: video.clickToPlay must stay true. The original "
                        "ships 0 iframes and 0 third-party requests on load." % i))
        for banned in ("autoplay", "iframeSrc", "embedOnLoad"):
            if banned in video:
                out.append(("error", "VIDEO_MUST_NOT_AUTOPLAY",
                            "node %d: %r is forbidden on a click-to-play facade"
                            % (i, banned)))
    return out


def check_removed_routes(spec, reg):
    """NO_REMOVED_ROUTES."""
    out = []
    removed = set(reg["templates"]["deliberatelyAbsent"].keys())
    if spec.get("route") in removed:
        out.append(("error", "NO_REMOVED_ROUTES",
                    "route %r was removed on purpose and must not be reintroduced "
                    "as a local route" % spec.get("route")))
    if spec.get("template") in ("sign-up", "welcome"):
        out.append(("error", "NO_REMOVED_ROUTES",
                    "template %r was removed on purpose" % spec.get("template")))
    return out


def check_cta_hrefs(spec, reg):
    """CTA_HREF_NOT_NORMALISED.

    Defence in depth behind the schema's per-section href enum. The app-host
    target is a property of the COMPONENT, not of the route: the nav and footer
    CTAs point at /sign-up on every route, the light-split hero and the CTA card
    point at /sign-up/welcome, and the blog CTA band's href is the literal '#'
    (a dead link on the original, preserved on purpose). An earlier draft of
    this check used a route-level heuristic and was wrong -- see the
    correctedDuringBuild note on the matching graph rule.
    """
    out = []
    sections = reg["sections"]

    def pinned_hrefs(contract, path_keys):
        node = contract["content"]
        for key in path_keys:
            node = (node.get("properties") or {}).get(key, {})
            if "items" in node:
                node = node["items"]
        return (node.get("properties") or {}).get("href", {}).get("enum")

    def walk(value, schema, path):
        if not isinstance(schema, dict):
            return
        if isinstance(value, dict):
            href = value.get("href")
            hs = (schema.get("properties") or {}).get("href", {})
            allowed = hs.get("x-cloneEnum") or hs.get("enum")
            clone_pattern = hs.get("x-clonePattern")
            if isinstance(href, str) and spec.get("mode") == "generation" and (allowed or clone_pattern):
                anchor_ok = bool(allowed) and href in allowed and not URL_LIKE.search(href)
                if not anchor_ok and not PLACEHOLDER_URL.match(href):
                    out.append(("error", "GENERATION_MODE_URL",
                                "%s: href %r in a mode:generation PageSpec must be a reserved "
                                ".example/.invalid URL (or a same-page anchor); the source's "
                                "app host / job board must not be reused" % (path, href)))
            elif isinstance(href, str) and allowed and href not in allowed:
                out.append(("error", "CTA_HREF_NOT_NORMALISED",
                            "%s: href %r is not one of the values this section pins "
                            "(%s). The app-host target is per component, not per "
                            "route -- do not normalise it."
                            % (path, href, allowed)))
            elif isinstance(href, str) and clone_pattern and not re.match(clone_pattern, href):
                out.append(("error", "CTA_HREF_NOT_NORMALISED",
                            "%s: href %r does not match the source pattern %s required in "
                            "mode:clone" % (path, href, clone_pattern)))
            for key, sub in (schema.get("properties") or {}).items():
                if key in value:
                    walk(value[key], sub, "%s.%s" % (path, key))
        elif isinstance(value, list) and isinstance(schema.get("items"), dict):
            for i, sub in enumerate(value):
                walk(sub, schema["items"], "%s[%d]" % (path, i))

    for i, node in enumerate(spec.get("nodes", [])):
        contract = sections.get(node.get("section"))
        if contract:
            walk(node.get("content"), contract["content"], "node[%d]" % i)
    return out


def check_asset_roles(spec, reg):
    """ASSET_ROLE_CLOSED, ASSET_REF_MUST_BE_DECLARED_FILE, NO_EXTERNAL_ASSET_REQUESTS.

    Note on what "pinned" does and does not mean here. The four pinned roles in
    assets/asset-roles.json carry real legal weight, but they are not all banned
    from a PageSpec in the same way:

      * brand.wordmark, press.logo and legal.operativeText are
        exposedAsPageSpecField: false -- there is no field for them at all, so
        any appearance in a PageSpec is an error.
      * photo.person IS exposedAsPageSpecField: true. A PageSpec may REFERENCE
        one of the existing local photographs by path; what is forbidden is
        SYNTHESISING a new photograph of a person. Because the only legal value
        is a path already present in the role's declared file list, that ban is
        enforced structurally: a generator cannot name an asset that does not
        already exist.

    Pinned POLICY VALUES (the registry not having drifted) are checked by
    extraction/verify_all.py::check_pinned_asset_policies, not here -- that is a
    claim about the registry, not about any one PageSpec.
    """
    out = []
    roles = reg["assets"]["roles"]

    def walk(value, path):
        if isinstance(value, dict):
            role = value.get("assetRole")
            if role is not None:
                spec_role = roles.get(role)
                if spec_role is None:
                    out.append(("error", "ASSET_ROLE_CLOSED",
                                "%s: assetRole %r is not in the closed enum"
                                % (path, role)))
                else:
                    if spec_role.get("exposedAsPageSpecField") is False:
                        out.append(("error", "ASSET_ROLE_CLOSED",
                                    "%s: assetRole %r is deliberately NOT exposed as "
                                    "a PageSpec field -- %s"
                                    % (path, role, spec_role.get("reason", ""))))
                    ref = value.get("assetRef")
                    if isinstance(ref, str):
                        if re.match(r"^https?://", ref):
                            out.append(("error", "NO_EXTERNAL_ASSET_REQUESTS",
                                        "%s: assetRef %r is an external URL; every "
                                        "asset on this site is local"
                                        % (path, ref)))
                        declared = spec_role.get("files") or []
                        policy = spec_role.get("generationPolicy")
                        if declared and policy != "may-generate-new" \
                                and ref not in declared:
                            out.append(("error", "ASSET_REF_MUST_BE_DECLARED_FILE",
                                        "%s: assetRef %r is not one of the %d files "
                                        "declared for role %r (policy %r). A "
                                        "generator may reference an existing asset "
                                        "but must not invent a new one."
                                        % (path, ref, len(declared), role, policy)))
            for key, sub in value.items():
                walk(sub, "%s.%s" % (path, key))
        elif isinstance(value, list):
            for i, sub in enumerate(value):
                walk(sub, "%s[%d]" % (path, i))

    for i, node in enumerate(spec.get("nodes", [])):
        walk(node.get("content"), "node[%d]" % i)
    return out


def check_blog_forbidden_fields(spec, reg):
    """BLOG_POST_FORBIDDEN_FIELDS."""
    out = []
    banned = ("author", "date", "publishedAt", "readTime", "excerpt", "deck",
              "subtitle", "shareLinks", "breadcrumb", "backToBlog", "inlineCta",
              "nextPrev")
    targets = ("blog.post-header", "blog.post-grid", "blog.related-posts")

    def walk(value, path):
        if isinstance(value, dict):
            for key in banned:
                if key in value:
                    out.append(("error", "BLOG_POST_FORBIDDEN_FIELDS",
                                "%s: %r does not exist on the original (there is not "
                                "a single <time> element on any blog page)"
                                % (path, key)))
            for key, sub in value.items():
                walk(sub, "%s.%s" % (path, key))
        elif isinstance(value, list):
            for i, sub in enumerate(value):
                walk(sub, "%s[%d]" % (path, i))

    for i, node in enumerate(spec.get("nodes", [])):
        if node.get("section") in targets:
            walk(node.get("content"), "node[%d]" % i)
    return out


def check_max_words(spec, reg):
    """MAX_WORDS_BUDGETS -- per-instance word counts, not just the example."""
    out = []
    sections = reg["sections"]

    def walk(value, schema, path):
        if not isinstance(schema, dict):
            return
        if "anyOf" in schema:
            for branch in schema["anyOf"]:
                walk(value, branch, path)
            return
        budget = schema.get("maxWords")
        if budget is not None and isinstance(value, str):
            n = _words(value)
            if n > budget:
                out.append(("error", "MAX_WORDS_BUDGETS",
                            "%s: %d words exceeds maxWords %d" % (path, n, budget)))
        props = schema.get("properties")
        if props and isinstance(value, dict):
            for key, sub in props.items():
                if key in value:
                    walk(value[key], sub, "%s.%s" % (path, key))
        items = schema.get("items")
        if items and isinstance(value, list):
            if isinstance(items, dict) and "oneOf" in items:
                for i, sub in enumerate(value):
                    for branch in items["oneOf"]:
                        walk(sub, branch, "%s[%d]" % (path, i))
            elif isinstance(items, dict):
                for i, sub in enumerate(value):
                    walk(sub, items, "%s[%d]" % (path, i))

    for i, node in enumerate(spec.get("nodes", [])):
        contract = sections.get(node.get("section"))
        if contract:
            walk(node.get("content"), contract["content"], "node[%d]" % i)
    return out



# --------------------------------------------------------------------------
# BASELINE R1-R3 / R8 / R10 additions: mode, generation leakage, asset
# availability pins, retrieval eligibility pins, legal binding, tokens.
# --------------------------------------------------------------------------

import textnorm as tn  # noqa: E402

PLACEHOLDER_URL = re.compile(
    r"^(https?://([a-z0-9-]+\.)*[a-z0-9-]+\.(example|invalid)(/[^\s]*)?"
    r"|mailto:[^@\s]+@([a-z0-9-]+\.)*[a-z0-9-]+\.(example|invalid))$")
URL_LIKE = re.compile(r"(https?://|mailto:|\bwww\.|\b[a-z0-9-]+\.(com|org|net|io|co|app)\b)", re.I)
URL_IN_TEXT = re.compile(r"(https?://[^\s\"'<>]+|mailto:[^\s\"'<>]+|\bwww\.[^\s\"'<>]+)", re.I)

# PINNED_AVAILABILITY -- pinned in code, independent of assets/asset-roles.json, so editing the registry alone
# cannot loosen a role. extraction/verify_all.py holds an identical pin and cross-checks registry == both pins.
PINNED_AVAILABILITY = {
    "asset.operatorSupplied": "generation-safe",
    "auth.illustration": "clone-only",
    "blob.fill": "generation-safe",
    "brand.wordmark": "blocked-for-generation",
    "copy.original": "generation-safe",
    "decorative.none": "generation-safe",
    "editorial.cover": "clone-only",
    "icon.feature": "clone-only",
    "icon.values": "clone-only",
    "illustration.brand": "clone-only",
    "illustration.editorial": "clone-only",
    "illustration.generated": "generation-safe",
    "legal.operativeText": "blocked-for-generation",
    "logo.placeholder": "generation-safe",
    "media.videoPoster": "clone-only",
    "person.fictional": "generation-safe",
    "photo.person": "clone-only",
    "placeholder.brandMark": "generation-safe",
    "press.logo": "blocked-for-generation",
    "screenshot.placeholder": "generation-safe",
    "url.placeholder": "generation-safe",
}

# RETRIEVAL_INELIGIBLE -- runtime / empty-state / scaffold UI that must never be retrieved as a design
# exemplar. Pinned here AND in extraction/verify_all.py; a contract whose id or name looks like runtime UI
# (RUNTIME_UI_HINT) must be in the pin.
RETRIEVAL_INELIGIBLE = {
    "content.stub-notice",
    "faq.category-empty",
    "faq.common-questions-empty",
    "testimonials.slider-empty",
}
RUNTIME_UI_HINT = re.compile(r"cookie|consent|modal|dialog|drawer|popup|overlay|preloader|toast|cursor|empty|stub", re.I)

# PINNED_THEME_RULES -- the theme/token restrictions of tokens/llm/token-policy.json themeRules, pinned in code.
PINNED_THEME_RULES = {
    "marketing-light": {"designSystem": "marketing", "tokenScopes": ["marketing", "shared"]},
    "auth-light": {"designSystem": "auth", "tokenScopes": ["auth", "shared"]},
    "minTextContrast": 4.5,
}

LEGAL_SECTIONS = ("legal.document-header", "legal.document-intro", "legal.document-part")
LEGAL_TITLES = {"terms-of-use": "Terms of use", "privacy-policy": "Privacy Policy"}

# string paths that are closed identifiers, not copy: excluded from the COPY/BRAND scans (they are schema enums)
IDENT_KEYS = {"section", "template", "variant", "theme", "designSystem", "mode", "pageSpecVersion", "pattern",
              "reducedMotionFallback", "easing", "assetRole", "clipId", "fill", "kind", "ledeClass", "color",
              "documentRef", "slot", "anchorId", "srHeading", "requiredNote"}


def iter_strings(obj, path="$", key=None):
    if isinstance(obj, dict):
        for k, v in obj.items():
            for x in iter_strings(v, "%s.%s" % (path, k), k):
                yield x
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            for x in iter_strings(v, "%s[%d]" % (path, i), key):
                yield x
    elif isinstance(obj, str):
        yield path, key, obj


def check_asset_availability(spec, reg):
    """ASSET_AVAILABILITY_PINNED + GENERATION_MODE_ASSET / _SCREENSHOT."""
    out = []
    roles = reg["assets"]["roles"]
    for role, want in sorted(PINNED_AVAILABILITY.items()):
        got = (roles.get(role) or {}).get("availability")
        if got != want:
            out.append(("error", "ASSET_AVAILABILITY_PINNED",
                        "assets/asset-roles.json role %s has availability %r but PINNED_AVAILABILITY "
                        "says %r (the registry cannot loosen a pinned role)" % (role, got, want)))
    extra = sorted(set(roles) - set(PINNED_AVAILABILITY))
    if extra:
        out.append(("error", "ASSET_AVAILABILITY_PINNED",
                    "roles %s are not pinned in PINNED_AVAILABILITY" % extra))
    if spec.get("mode") != "generation":
        return out
    files = {a["term"] for a in reg["identity"]["assetFiles"]}
    shots = {a["term"] for a in reg["identity"]["screenshotFiles"]}

    def walk(value, path):
        if isinstance(value, dict):
            role = value.get("assetRole")
            if isinstance(role, str):
                avail = PINNED_AVAILABILITY.get(role)
                if avail != "generation-safe":
                    subs = (roles.get(role) or {}).get("generationSafeSubstitutes") or []
                    out.append(("error", "GENERATION_MODE_ASSET",
                                "%s: assetRole %r is %s; a mode:generation PageSpec may only use "
                                "generation-safe roles (substitutes: %s)" % (path, role, avail, subs)))
                ref = value.get("assetRef")
                if isinstance(ref, str):
                    base = os.path.basename(ref)
                    if base in shots:
                        out.append(("error", "GENERATION_MODE_SCREENSHOT",
                                    "%s: assetRef %r is a source screenshot" % (path, ref)))
                    elif base in files or ref.startswith(("public/", "src/")):
                        out.append(("error", "GENERATION_MODE_ASSET",
                                    "%s: assetRef %r is a source asset file" % (path, ref)))
            for k, v in value.items():
                walk(v, "%s.%s" % (path, k))
        elif isinstance(value, list):
            for i, v in enumerate(value):
                walk(v, "%s[%d]" % (path, i))

    walk(spec.get("nodes"), "nodes")
    walk(spec.get("generationContext"), "generationContext")
    return out


def check_generation_mode(spec, reg):
    """GENERATION_MODE_BRAND / _CUSTOMER / _PERSON / _URL / _EMBED / _CLAIM / _COPY (and the clone-mode
    counterpart: generationContext belongs to generation mode only)."""
    out = []
    mode = spec.get("mode")
    ctx = spec.get("generationContext")
    if mode == "clone":
        if ctx is not None:
            out.append(("error", "GENERATION_MODE_BRAND",
                        "mode:clone must not declare generationContext (the source's own identity renders)"))
        return out
    if mode != "generation":
        return out
    if not isinstance(ctx, dict):
        out.append(("error", "GENERATION_MODE_BRAND",
                    "mode:generation requires generationContext: without it the chrome renders the source "
                    "wordmark, app host and social links"))
        ctx = {}
    ident = reg["identity"]
    by_cat = {}
    for t in ident["terms"]:
        by_cat.setdefault(t["category"], []).append(t)
    shingles = set(ident["copy"]["hashes"])
    rule_of = {"BRAND": "GENERATION_MODE_BRAND", "CUSTOMER": "GENERATION_MODE_CUSTOMER",
               "PERSON": "GENERATION_MODE_PERSON", "URL": "GENERATION_MODE_URL",
               "EMBED": "GENERATION_MODE_EMBED", "CLAIM": "GENERATION_MODE_CLAIM"}
    seen = set()
    for path, key, s in iter_strings({"nodes": spec.get("nodes"), "generationContext": ctx, "route": spec.get("route")}):
        if key in IDENT_KEYS:
            continue
        toks = tn.tokens(s)
        for cat, rule in rule_of.items():
            for t in by_cat.get(cat, []):
                if tn.contains_terms(toks, t["tokens"]) and (path, rule) not in seen:
                    seen.add((path, rule))
                    out.append(("error", rule, "%s: %r carries source %s %r (%s)"
                                % (path, s[:60], cat.lower(), t["term"], t["evidence"][0])))
        for m in URL_IN_TEXT.finditer(s):
            u = m.group(0).rstrip(".,;)")
            if not PLACEHOLDER_URL.match(u) and (path, "GENERATION_MODE_URL") not in seen:
                seen.add((path, "GENERATION_MODE_URL"))
                out.append(("error", "GENERATION_MODE_URL",
                            "%s: URL %r is not on a reserved .example/.invalid domain" % (path, u)))
        hit = tn.shingle_hashes(s) & shingles
        if hit:
            out.append(("error", "GENERATION_MODE_COPY",
                        "%s: %r reuses source copy (%d matching 5-word shingle(s))" % (path, s[:60], len(hit))))
    ids = [n.get("section") for n in spec.get("nodes", [])]
    if "trust.press-bar" in ids:
        node = spec["nodes"][ids.index("trust.press-bar")]
        want = (node.get("content") or {}).get("logoCount")
        logos = ctx.get("pressLogos") or []
        if len(logos) != want:
            out.append(("error", "GENERATION_MODE_CUSTOMER",
                        "trust.press-bar shows %r logo slot(s) but generationContext.pressLogos has %d: "
                        "without placeholder logos the bar renders the source's real press marks"
                        % (want, len(logos))))
    if "trust.video-and-cards" in ids:
        url = ctx.get("videoEmbedUrl")
        if not isinstance(url, str) or not PLACEHOLDER_URL.match(url):
            out.append(("error", "GENERATION_MODE_EMBED",
                        "trust.video-and-cards needs generationContext.videoEmbedUrl on a reserved "
                        ".example/.invalid domain; otherwise the facade plays the source's video"))
    return out


def check_retrieval(spec, reg):
    """RETRIEVAL_ELIGIBILITY_PINNED."""
    out = []
    sections = reg["sections"]
    for sid, c in sorted(sections.items()):
        want = sid not in RETRIEVAL_INELIGIBLE
        got = c.get("retrievalEligible")
        if got is not want:
            out.append(("error", "RETRIEVAL_ELIGIBILITY_PINNED",
                        "contract %s retrievalEligible is %r but the RETRIEVAL_INELIGIBLE pin says %r"
                        % (sid, got, want)))
        if not want and len(str(c.get("retrievalReason", ""))) < 30:
            out.append(("error", "RETRIEVAL_ELIGIBILITY_PINNED",
                        "contract %s is retrieval-ineligible without a 30+ char retrievalReason" % sid))
        if want and RUNTIME_UI_HINT.search(sid + " " + str(c.get("name", ""))):
            out.append(("error", "RETRIEVAL_ELIGIBILITY_PINNED",
                        "contract %s looks like runtime/utility UI but is not in RETRIEVAL_INELIGIBLE" % sid))
    for i, node in enumerate(spec.get("nodes", [])):
        if "retrievalEligible" in node:
            want = node.get("section") not in RETRIEVAL_INELIGIBLE
            if node["retrievalEligible"] is not want:
                out.append(("error", "RETRIEVAL_ELIGIBILITY_PINNED",
                            "node %d (%s): retrievalEligible %r contradicts the pinned contract value %r"
                            % (i, node.get("section"), node["retrievalEligible"], want)))
    return out


def check_legal_binding(spec, reg):
    """LEGAL_DOCUMENT_BINDING and GENERATION_MODE_LEGAL."""
    out = []
    nodes = [n for n in spec.get("nodes", []) if n.get("section") in LEGAL_SECTIONS]
    if not nodes:
        return out
    refs = {(n.get("content") or {}).get("documentRef") for n in nodes}
    if len(refs) != 1:
        out.append(("error", "LEGAL_DOCUMENT_BINDING",
                    "legal sections on one page point at different documents: %s" % sorted(map(str, refs))))
        return out
    ref = refs.pop()
    parts = [(n.get("content") or {}).get("partIndex") for n in nodes if n["section"] == "legal.document-part"]
    if parts != list(range(1, len(parts) + 1)):
        out.append(("error", "LEGAL_DOCUMENT_BINDING",
                    "legal.document-part partIndex must run 1..N in order, got %s" % parts))
    if spec.get("mode") == "generation":
        if ref != "operator-supplied":
            out.append(("error", "GENERATION_MODE_LEGAL",
                        "mode:generation legal pages must use documentRef 'operator-supplied' (the "
                        "deployer's legal owner supplies the text); %r is the source's operative legal text" % ref))
        return out
    if ref not in LEGAL_TITLES:
        out.append(("error", "LEGAL_DOCUMENT_BINDING",
                    "mode:clone documentRef must be one of the real documents %s, got %r" % (sorted(LEGAL_TITLES), ref)))
        return out
    want_parts = reg["sections"]["legal.document-part"]["constraints"]["documentParts"][ref]
    if len(parts) != want_parts:
        out.append(("error", "LEGAL_DOCUMENT_BINDING",
                    "%s has %d heading-bounded parts; the PageSpec declares %d" % (ref, want_parts, len(parts))))
    for n in nodes:
        if n["section"] == "legal.document-header" and (n.get("content") or {}).get("title") != LEGAL_TITLES[ref]:
            out.append(("error", "LEGAL_DOCUMENT_BINDING",
                        "mode:clone %s title must be %r" % (ref, LEGAL_TITLES[ref])))
    return out


HEX = re.compile(r"#[0-9A-Fa-f]{3,8}\b")
FUNC_COLOR = re.compile(r"\b(rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\s*\(", re.I)
NAMED_COLOR = re.compile(r"^(white|black|red|green|blue|yellow|orange|purple|pink|gray|grey|teal|navy|transparent|currentcolor)$", re.I)
RAW_LENGTH = re.compile(r"^-?\d*\.?\d+\s*(px|rem|em|vh|vw|vmin|vmax|%|pt|ch|ex)?$|calc\(", re.I)
TOKEN_PATH = re.compile(r"^[A-Za-z][A-Za-z0-9-]*(\.[A-Za-z0-9-]+)+$")


def _hex_rgb(value):
    v = value.strip().lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    if not re.match(r"^[0-9a-fA-F]{6}$", v):
        return None
    return tuple(int(v[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def contrast_ratio(a, b):
    ca, cb = _hex_rgb(a), _hex_rgb(b)
    if ca is None or cb is None:
        return None

    def lum(c):
        lin = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    la, lb = sorted((lum(ca), lum(cb)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _resolve(cat, theme, path):
    th = cat["themes"].get(theme) or {}
    r = (th.get("resolves") or {}).get(path)
    if r:
        return r.get("value")
    v = cat["tokens"].get(path, {}).get("value")
    m = re.match(r"^\{(.+)\}$", str(v))
    return cat["tokens"].get(m.group(1), {}).get("value") if m else v


def classify_token(slot_name, slot, value, reg):
    cat, pol = reg["catalog"], reg["policy"]
    kind = slot["kind"]
    if HEX.search(value) or FUNC_COLOR.search(value) or NAMED_COLOR.match(value):
        return "TOKEN_RAW_COLOR", "%s: raw colour %r; name a token (%s)" % (slot_name, value, ", ".join(slot["allow"][:3]))
    if kind in ("spacing", "radius") and RAW_LENGTH.search(value):
        return "TOKEN_ARBITRARY_SPACING", "%s: arbitrary length %r; name a %s token (%s)" % (slot_name, value, kind, ", ".join(slot["allow"][:3]))
    if not TOKEN_PATH.match(value):
        if kind == "fontFamily":
            return "TOKEN_UNSUPPORTED_FONT", "%s: unsupported font %r; fonts are tokens (%s)" % (slot_name, value, ", ".join(slot["allow"]))
        return "TOKEN_UNKNOWN", "%s: %r is not a token path" % (slot_name, value)
    if value not in cat["tokens"]:
        if kind == "fontFamily":
            return "TOKEN_UNSUPPORTED_FONT", "%s: %r is not one of the catalog font families (%s)" % (slot_name, value, ", ".join(slot["allow"]))
        return "TOKEN_UNKNOWN", "%s: unknown token %r (not in tokens/llm/token-catalog.json)" % (slot_name, value)
    entry = cat["tokens"][value]
    if entry["category"] in pol["notGenerationApproved"]["categories"] or not entry.get("generationApproved", True):
        return "TOKEN_NOT_APPROVED", "%s: token %r (%s) is not generation-approved" % (slot_name, value, entry["category"])
    if value not in slot["allow"]:
        return "TOKEN_SLOT_MISMATCH", "%s: token %r (%s) is not accepted by this slot (allowed: %s)" % (slot_name, value, entry["category"], ", ".join(slot["allow"]))
    return None


def check_tokens(spec, reg):
    """TOKEN_UNKNOWN / _RAW_COLOR / _ARBITRARY_SPACING / _UNSUPPORTED_FONT / _SLOT_MISMATCH / _NOT_APPROVED /
    _THEME_COMBINATION. The policy is tokens/llm/token-policy.json; the catalog is generated from the token files."""
    out = []
    cat, pol = reg["catalog"], reg["policy"]
    slots = {k: v for k, v in pol["pageSpecTokenSlots"].items() if not k.startswith("$")}
    given = spec.get("tokens") if isinstance(spec.get("tokens"), dict) else {}
    ok = {}
    for name, value in given.items():
        if name not in slots or not isinstance(value, str):
            continue
        res = classify_token(name, slots[name], value, reg)
        if res:
            out.append(("error",) + res)
        else:
            ok[name] = value
    fills = pol["nodeFillSlots"]
    for i, node in enumerate(spec.get("nodes", [])):
        for path, key, s in iter_strings(node.get("content"), "node[%d].content" % i):
            if key == "fill" and s != fills["noFillSentinel"]:
                if s not in cat["tokens"]:
                    out.append(("error", "TOKEN_UNKNOWN", "%s: fill %r is not a catalog token" % (path, s)))
                elif s not in fills["allow"]:
                    out.append(("error", "TOKEN_SLOT_MISMATCH", "%s: fill %r is not a colour fill token" % (path, s)))
                else:
                    ok.setdefault("__fill__%s" % path, s)
    for path, key, s in iter_strings({k: v for k, v in spec.items() if k != "tokens"}):
        if HEX.search(s) or FUNC_COLOR.search(s):
            out.append(("error", "TOKEN_RAW_COLOR", "%s: raw colour value in %r; colours are tokens, never values" % (path, s[:60])))
    theme = spec.get("theme")
    pinned = PINNED_THEME_RULES.get(theme)
    th = cat["themes"].get(theme)
    if th is None or pinned is None:
        out.append(("error", "TOKEN_THEME_COMBINATION", "theme %r is not a theme of the token catalog %s" % (theme, sorted(cat["themes"]))))
        return out
    if th["designSystem"] != spec.get("designSystem") or pinned["designSystem"] != spec.get("designSystem"):
        out.append(("error", "TOKEN_THEME_COMBINATION", "theme %r belongs to design system %r, not %r" % (theme, th["designSystem"], spec.get("designSystem"))))
    scopes = set(pinned["tokenScopes"])
    for name, value in ok.items():
        scope = cat["tokens"][value]["themeScope"]
        if scope not in scopes:
            out.append(("error", "TOKEN_THEME_COMBINATION", "%s: token %r is %s-scoped and cannot be used with theme %r (allowed scopes %s)"
                        % (name.replace("__fill__", ""), value, scope, theme, sorted(scopes))))
        elif slots.get(name, {}).get("themeResolved") and value not in th["semanticTokens"]:
            out.append(("error", "TOKEN_THEME_COMBINATION", "%s: token %r is not resolved by theme %r" % (name, value, theme)))
    against = slots.get("text", {}).get("contrastAgainst")
    if "text" in ok and against in ok:
        a, b = _resolve(cat, theme, ok["text"]), _resolve(cat, theme, ok[against])
        r = contrast_ratio(a, b) if isinstance(a, str) and isinstance(b, str) else None
        if r is not None and r < PINNED_THEME_RULES["minTextContrast"]:
            out.append(("error", "TOKEN_THEME_COMBINATION", "text %r (%s) on %s %r (%s) has contrast %.2f, below %s in theme %r"
                        % (ok["text"], a, against, ok[against], b, r, PINNED_THEME_RULES["minTextContrast"], theme)))
    return out


CHECKS = [
    check_template_sequence,
    check_one_hero,
    check_hero_kind,
    check_chrome_position,
    check_duplicates,
    check_adjacency,
    check_home_only,
    check_allowed_templates,
    check_motion_pattern,
    check_reduced_motion,
    check_motion_budget,
    check_design_system_isolation,
    check_auth_inert,
    check_empty_collections,
    check_video_facade,
    check_removed_routes,
    check_cta_hrefs,
    check_asset_roles,
    check_blog_forbidden_fields,
    check_max_words,
    check_asset_availability,
    check_generation_mode,
    check_retrieval,
    check_legal_binding,
    check_tokens,
]


def validate_spec(spec, reg=None):
    """Return (errors, warnings) as lists of (rule_id, message)."""
    reg = reg or load_registry()
    errors, warnings = [], []
    for check in CHECKS:
        for severity, rule, message in check(spec, reg):
            (errors if severity == "error" else warnings).append((rule, message))
    return errors, warnings


def validate_schema(spec):
    """Draft-07 validation using the repo's vendored, dependency-free validator."""
    import _draft7
    schema = _load("schema", "pagespec.schema.json")
    return _draft7.validate(spec, schema)


def main(argv):
    paths = argv[1:] or [os.path.join(REPO, "schema", "example.pagespec.json")]
    reg = load_registry()
    bad = 0
    for path in paths:
        with open(path, encoding="utf-8") as handle:
            spec = json.load(handle)
        label = os.path.relpath(path, REPO)
        schema_errors = validate_schema(spec)
        errors, warnings = validate_spec(spec, reg)
        print("== %s" % label)
        for where, message in schema_errors:
            print("   SCHEMA  %s %s" % (where, message))
        for rule, message in errors:
            print("   ERROR   [%s] %s" % (rule, message))
        for rule, message in warnings:
            print("   WARN    [%s] %s" % (rule, message))
        total = len(schema_errors) + len(errors)
        print("   -> %d schema error(s), %d semantic error(s), %d warning(s)"
              % (len(schema_errors), len(errors), len(warnings)))
        bad += total
    print()
    print("FAIL: %d error(s)" % bad if bad else "PASS: 0 errors")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
