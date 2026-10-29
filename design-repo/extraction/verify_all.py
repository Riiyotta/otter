#!/usr/bin/env python3
"""One-shot verification for the Otter design-repo.

Runs every automated consistency check this repo claims to have. Each check recomputes a fact from the real
files rather than trusting a hand-maintained summary, and each is proven to fail on injected drift by
extraction/prove_drift.py.

  json-parse          every JSON file parses
  no-abs-paths        no absolute local machine paths anywhere in the tree
  self-contained      manifest entryPoints are all INSIDE design-repo/ and exist
  schema              the bundled clone example validates draft-07 with 0 errors
  allowlist-parity    allowlist <-> contract files, both directions
  allowlist-schema    allowlist settable props <-> the real schema
  version-parity      allowlist / token catalog / token policy / pageSpec versions == manifest
  manifest-counts     manifest counts recomputed from disk
  design-policy       bound to n0-design-constraints-common 0.1.0 + local extension; contentHash; no stale wording
  route-coverage      every route assigned exactly once, 1:1 with templates
  graph-validator     every graph rule maps to a real check in the validator
  pinned-assets       the four compliance-critical roles hold their exact generationPolicy
  citations           every measuredFrom resolves, in range AND on-topic
  generated-files     schema branches, token catalog, generation examples == a rebuild (R10, R4)
  token-policy        token policy resolves against the catalog; registered; theme rules pinned (R10)
  asset-availability  PINNED_AVAILABILITY (here + semantic validator) == registry == allowlist (R3)
  retrieval-pin       RETRIEVAL_INELIGIBLE (here + semantic validator) == contracts == allowlist (R8)
  section-contracts   closed contract schema; source/semantic split; source ranges re-read (R7)
  source-identity     generation-mode leakage registry == a rebuild from the source (R2)
  examples            one mode:generation example per template family, all valid (R4)
  wrapper-gate        measured 1440px heights through extraction/wrapper_gate.py (R9)
  routes-from-source  routes in src/App.jsx == mapped routes (R11)
  legal-parts         legal part counts == headings in src/data/legal (R6)
  adversarial         the full control + mutation suite

Source-dependent checks degrade gracefully: with no sibling source tree present (a standalone copy, or an
extracted zip) they WARN and skip rather than fail, since the evidence they point at is build-time context.

Paths derive from __file__, never hardcoded.

Usage:
    python3 verify_all.py                # everything
    python3 verify_all.py --cross-check  # also diff the vendored validator against `jsonschema`, if installed
    python3 verify_all.py --prove-drift  # runs extraction/prove_drift.py
"""
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_ROOT = os.path.dirname(REPO)   # the sibling project, when present
sys.path.insert(0, os.path.join(REPO, "schema"))

PASS, FAIL, WARN, SKIP = "PASS", "FAIL", "WARN", "SKIP"
results = []


def record(name, status, detail=""):
    results.append((name, status, detail))
    print("  %-18s %-4s %s" % (name, status, detail))


def jload(*parts):
    with open(os.path.join(REPO, *parts), encoding="utf-8") as handle:
        return json.load(handle)


def all_json():
    out = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for name in sorted(files):
            if name.endswith(".json"):
                out.append(os.path.relpath(os.path.join(root, name), REPO))
    return sorted(out)


def contract_ids():
    out = {}
    for kind in ("sections", "primitives", "components"):
        folder = os.path.join(REPO, kind)
        out[kind] = sorted(
            n[:-5] for n in os.listdir(folder) if n.endswith(".json")
        )
    return out


# --------------------------------------------------------------------------

def check_json_parse():
    bad = []
    for rel in all_json():
        try:
            with open(os.path.join(REPO, rel), encoding="utf-8") as handle:
                json.load(handle)
        except Exception as exc:
            bad.append("%s: %s" % (rel, exc))
    if bad:
        record("json-parse", FAIL, "; ".join(bad[:3]))
    else:
        record("json-parse", PASS, "%d JSON files parse" % len(all_json()))


def check_no_abs_paths():
    hits = []
    # Assembled from fragments on purpose: spelling these prefixes literally
    # would make this file match its own check (it did, on first run).
    home = "/" + "Users" + "/"
    nix = "/" + "home" + "/"
    pattern = re.compile("%s|%s[a-z]|[A-Z]:%s" % (home, nix, re.escape(chr(92) * 2)))
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for name in files:
            path = os.path.join(root, name)
            try:
                with open(path, encoding="utf-8", errors="replace") as handle:
                    for i, line in enumerate(handle, 1):
                        if pattern.search(line):
                            hits.append("%s:%d" % (os.path.relpath(path, REPO), i))
            except OSError:
                pass
    if hits:
        record("no-abs-paths", FAIL, "%d hit(s): %s" % (len(hits), hits[:4]))
    else:
        record("no-abs-paths", PASS, "no absolute local machine paths")


def check_self_contained():
    manifest = jload("registry.manifest.json")
    entries = manifest.get("entryPoints", {})
    flat = []
    for value in entries.values():
        flat.extend(value if isinstance(value, list) else [value])
    outside = [e for e in flat if e.startswith("../") or e.startswith("/")]
    missing = [e for e in flat if not os.path.exists(os.path.join(REPO, e))]
    if outside:
        record("self-contained", FAIL,
               "%d entryPoint(s) point outside design-repo/: %s"
               % (len(outside), outside[:4]))
    elif missing:
        record("self-contained", FAIL,
               "%d entryPoint(s) do not exist: %s" % (len(missing), missing[:4]))
    else:
        record("self-contained", PASS,
               "%d entryPoints, all inside design-repo/ and all present" % len(flat))


def check_schema():
    import _draft7
    schema = jload("schema", "pagespec.schema.json")
    unsupported = _draft7.check_schema(schema)
    example = jload("schema", "example.pagespec.json")
    errors = _draft7.validate(example, schema)
    if unsupported:
        record("schema", FAIL, "unsupported keywords: %s" % unsupported)
    elif errors:
        record("schema", FAIL, "%d error(s): %s" % (len(errors), errors[:2]))
    else:
        branches = len(schema["properties"]["nodes"]["items"].get("allOf", []))
        record("schema", PASS,
               "example validates with 0 errors; %d content branches live on "
               "node items" % branches)


def check_allowlist_parity():
    allowlist = jload("tokens", "llm", "component-allowlist.json")
    ids = contract_ids()
    problems = []
    for kind in ("sections", "primitives", "components"):
        listed = set(allowlist.get(kind, {}).keys())
        real = set(ids[kind])
        phantom = sorted(listed - real)
        orphan = sorted(real - listed)
        if phantom:
            problems.append("%s: phantom allowlist entries with no contract file %s"
                            % (kind, phantom))
        if orphan:
            problems.append("%s: contract files with no allowlist entry %s"
                            % (kind, orphan))
        for name in sorted(listed & real):
            declared = allowlist[kind][name].get("contractFile")
            expected = "%s/%s.json" % (kind, name)
            if declared != expected:
                problems.append("%s/%s: contractFile says %r, expected %r"
                                % (kind, name, declared, expected))
            elif not os.path.exists(os.path.join(REPO, expected)):
                problems.append("%s/%s: contractFile %r does not exist"
                                % (kind, name, declared))
    roles = set(jload("assets", "asset-roles.json")["roles"].keys())
    listed_roles = set(allowlist.get("assetRoles", {}).keys())
    if roles != listed_roles:
        problems.append("assetRoles mismatch: only-in-registry %s / only-in-allowlist %s"
                        % (sorted(roles - listed_roles), sorted(listed_roles - roles)))
    if problems:
        record("allowlist-parity", FAIL, problems[0])
    else:
        total = sum(len(ids[k]) for k in ids)
        record("allowlist-parity", PASS,
               "%d contracts <-> %d allowlist entries, both directions, + %d asset roles"
               % (total, total, len(roles)))


def check_allowlist_schema():
    """The allowlist must not drift from the schema it claims to describe."""
    allowlist = jload("tokens", "llm", "component-allowlist.json")
    schema = jload("schema", "pagespec.schema.json")
    branches = schema["properties"]["nodes"]["items"].get("allOf", [])
    by_section = {}
    for branch in branches:
        sid = branch["if"]["properties"]["section"]["const"]
        by_section[sid] = branch["then"]["properties"]["content"]
    problems = []
    for sid, entry in sorted(allowlist["sections"].items()):
        content = by_section.get(sid)
        if content is None:
            problems.append("%s has an allowlist entry but no schema branch" % sid)
            continue
        schema_required = content.get("required", [])
        if sorted(entry["requiredContentFields"]) != sorted(schema_required):
            problems.append("%s: required fields differ (allowlist %s vs schema %s)"
                            % (sid, entry["requiredContentFields"], schema_required))
        top = {k for k in entry["settableProperties"] if "." not in k and "[" not in k}
        schema_props = set((content.get("properties") or {}).keys())
        if top != schema_props:
            problems.append("%s: top-level settable props differ (allowlist-only %s / "
                            "schema-only %s)"
                            % (sid, sorted(top - schema_props),
                               sorted(schema_props - top)))
    missing = sorted(set(by_section) - set(allowlist["sections"]))
    if missing:
        problems.append("schema branches with no allowlist entry: %s" % missing)
    if problems:
        record("allowlist-schema", FAIL, problems[0])
    else:
        record("allowlist-schema", PASS,
               "%d section branches agree with the allowlist" % len(by_section))


def check_version_parity():
    manifest = jload("registry.manifest.json")
    allowlist = jload("tokens", "llm", "component-allowlist.json")
    pairs = [("allowlistVersion", allowlist["version"]),
             ("tokenCatalogVersion", jload("tokens", "llm", "token-catalog.json")["version"]),
             ("tokenPolicyVersion", jload("tokens", "llm", "token-policy.json")["version"]),
             ("pageSpecVersion", jload("schema", "pagespec.schema.json")["properties"]["pageSpecVersion"]["const"])]
    bad = ["manifest.%s %r != %r" % (k, manifest.get(k), v) for k, v in pairs if manifest.get(k) != v]
    if bad:
        record("version-parity", FAIL, "; ".join(bad))
    else:
        record("version-parity", PASS, ", ".join("%s %s" % kv for kv in pairs) + " (machine-checked)")


BOUND_POLICY = {"policyId": "n0-design-constraints-common", "policyVersion": "0.1.0", "commonIrVersion": "0.5",
                "enforcementMode": "hard-and-soft"}
LOCAL_EXTENSION = {"ref": "policy/design-policy.json", "policyId": "consumer-service-marketplace-web", "policyVersion": "1.0.0"}
STALE_POLICY_WORDING = re.compile(r"pending[- ]architecture[- ]review|architecture ratification|not recorded|"
                                  r"has not been made|would need an architecture decision|requires a recorded architecture decision",
                                  re.I)


def check_design_policy():
    """The 2026-10-29 architecture decision: bound to the N0 generic common policy n0-design-constraints-common
    0.1.0 (Common IR 0.5, hard-and-soft), with policy/design-policy.json as a LOCAL EXTENSION; not bound to the
    SaaS policy; contentHash over the enforcing files matches; no stale 'pending architecture review' wording."""
    sys.path.insert(0, os.path.join(REPO, "extraction"))
    import policy_hash
    manifest = jload("registry.manifest.json")
    dp = manifest.get("designPolicy") or {}
    errs = []
    for k, v in BOUND_POLICY.items():
        if dp.get(k) != v:
            errs.append("designPolicy.%s is %r, expected %r" % (k, dp.get(k), v))
    ext = dp.get("localExtension") or {}
    for k, v in LOCAL_EXTENSION.items():
        if ext.get(k) != v:
            errs.append("designPolicy.localExtension.%s is %r, expected %r" % (k, ext.get(k), v))
    if not os.path.isfile(os.path.join(REPO, ext.get("ref", "missing"))):
        errs.append("local extension file %r does not exist" % ext.get("ref"))
        policy = {}
    else:
        policy = jload(*ext["ref"].split("/"))
    if policy.get("policyId") != LOCAL_EXTENSION["policyId"] or policy.get("policyVersion") != LOCAL_EXTENSION["policyVersion"]:
        errs.append("policy/design-policy.json id/version disagree with localExtension")
    if (policy.get("extends") or {}).get("policyId") != BOUND_POLICY["policyId"] or (policy.get("extends") or {}).get("policyVersion") != BOUND_POLICY["policyVersion"]:
        errs.append("policy/design-policy.json must declare extends n0-design-constraints-common 0.1.0")
    nb = dp.get("notBoundTo") or {}
    if "n0-saas-design-constraints-common" not in nb or len(str(nb.get("n0-saas-design-constraints-common", ""))) < 30:
        errs.append("designPolicy.notBoundTo must keep n0-saas-design-constraints-common with its reason")
    if "saas" in BOUND_POLICY["policyId"] or (policy.get("classification") or {}).get("isSaaS") is not False:
        errs.append("policy is bound to / classified as SaaS")
    if "n0-saas-design-constraints-common" not in (policy.get("notBoundTo") or {}):
        errs.append("policy must record notBoundTo n0-saas-design-constraints-common")
    cls = policy.get("classification") or {}
    if manifest.get("category") != cls.get("productCategory") or dp.get("category") != cls.get("productCategory"):
        errs.append("manifest/designPolicy category != policy productCategory")
    if manifest.get("productDomain") != cls.get("productDomain") or dp.get("domain") != cls.get("productDomain"):
        errs.append("manifest productDomain / designPolicy.domain != policy productDomain")
    ap = policy.get("approval") or {}
    if ap.get("policyDecision") != "ratified" or ap.get("architectureDecisionRecorded") is not True \
            or ap.get("decidedAt") != "2026-10-29" or "repository owner" not in str(ap.get("decidedBy", "")) \
            or BOUND_POLICY["policyId"] not in str(ap.get("decision", "")) or "LOCAL EXTENSION" not in str(ap.get("decision", "")).upper():
        errs.append("policy approval must record the ratified 2026-10-29 decision (bound id/version + local extension)")
    flags = manifest.get("approvalFlags") or {}
    if flags.get("legalContentSignOff") is not False or flags.get("assetLicensingReviewed") is not False:
        errs.append("legal/licensing approvalFlags changed; they are NOT part of the policy decision")
    if dp.get("contentHashFiles") != policy_hash.POLICY_FILES:
        errs.append("designPolicy.contentHashFiles != extraction/policy_hash.py POLICY_FILES")
    want = policy_hash.compute(REPO)
    if dp.get("contentHash") != want:
        errs.append("designPolicy.contentHash %r != recomputed %r" % (dp.get("contentHash"), want))
    stale = []
    for rel in ("README.md", "CHANGELOG.md", "registry.manifest.json", "policy/design-policy.json"):
        if not os.path.isfile(os.path.join(REPO, rel)):
            continue
        with open(os.path.join(REPO, rel), encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                if STALE_POLICY_WORDING.search(line):
                    stale.append("%s:%d" % (rel, i))
    if stale:
        errs.append("stale pending-architecture wording at %s" % stale[:4])
    if errs:
        record("design-policy", FAIL, "; ".join(errs[:3]))
    else:
        record("design-policy", PASS,
               "bound to %s %s (Common IR 0.5, hard-and-soft) + local extension %s %s; not SaaS-bound; contentHash matches"
               % (BOUND_POLICY["policyId"], BOUND_POLICY["policyVersion"], LOCAL_EXTENSION["policyId"], LOCAL_EXTENSION["policyVersion"]))


def check_manifest_counts():
    """Recompute the manifest's own numbers from the files it summarises."""
    manifest = jload("registry.manifest.json")
    ids = contract_ids()
    templates = jload("templates", "templates.json")
    graph = jload("compatibility", "graph.json")
    roles = jload("assets", "asset-roles.json")["roles"]
    schema = jload("schema", "pagespec.schema.json")
    actual = {
        "sections": len(ids["sections"]),
        "primitives": len(ids["primitives"]),
        "components": len(ids["components"]),
        "templates": len(templates["templates"]),
        "routePatterns": len(templates["routeToTemplate"]),
        "compatibilityRules": len(graph["rules"]),
        "assetRoles": len(roles),
        "schemaContentBranches": len(
            schema["properties"]["nodes"]["items"].get("allOf", [])),
        "jsonFiles": len(all_json()),
        "catalogTokens": jload("tokens", "llm", "token-catalog.json")["counts"]["tokens"],
        "tokenSlots": len([k for k in jload("tokens", "llm", "token-policy.json")["pageSpecTokenSlots"] if not k.startswith("$")]),
        "generationExamples": len([n for n in os.listdir(os.path.join(REPO, "schema", "examples")) if n.endswith(".json")]),
    }
    claimed = manifest.get("counts", {})
    bad = {k: (claimed.get(k), v) for k, v in actual.items() if claimed.get(k) != v}
    with open(os.path.join(REPO, "README.md"), encoding="utf-8") as handle:
        readme = re.findall(r"^\| \*\*(\w+)\*\* \|.*\(counts\.(\w+)\) \|$", handle.read(), re.M)
    if not readme:
        bad["README count table"] = ("missing", "rows tagged (counts.<key>)")
    for value, key in readme:
        if str(actual.get(key)) != value:
            bad["README " + key] = (value, actual.get(key))
    if bad:
        record("manifest-counts", FAIL,
               "; ".join("%s claims %r, disk says %r" % (k, c, a)
                         for k, (c, a) in sorted(bad.items())))
    else:
        record("manifest-counts", PASS,
               "%d counts recomputed from disk and matching" % len(actual))


def check_route_coverage():
    templates = jload("templates", "templates.json")
    mapping = templates["routeToTemplate"]
    problems = []
    seen = {}
    for tid, tpl in templates["templates"].items():
        for route in tpl["routes"]:
            if route in seen:
                problems.append("route %r assigned to both %r and %r"
                                % (route, seen[route], tid))
            seen[route] = tid
    if seen != mapping:
        problems.append("routeToTemplate disagrees with the templates' own route lists")
    for route, tid in mapping.items():
        if tid not in templates["templates"]:
            problems.append("route %r maps to unknown template %r" % (route, tid))
    for name in templates["deliberatelyAbsent"]:
        if name in mapping:
            problems.append("deliberately-absent route %r is mapped" % name)
    if templates.get("templateCount") != len(templates["templates"]):
        problems.append("templateCount is stale")
    if templates.get("routePatternCount") != len(mapping):
        problems.append("routePatternCount is stale")
    if problems:
        record("route-coverage", FAIL, problems[0])
    else:
        record("route-coverage", PASS,
               "%d routes -> %d templates, each assigned exactly once"
               % (len(mapping), len(templates["templates"])))


def check_graph_validator_agreement():
    """A rule in the graph and a check in the validator are two authoritative
    sources for one fact. They must agree, and stay agreeing."""
    graph = jload("compatibility", "graph.json")
    with open(os.path.join(REPO, "schema", "semantic_validate.py"),
              encoding="utf-8") as handle:
        source = handle.read()
    import semantic_validate as sv
    implemented = {fn.__name__ for fn in sv.CHECKS}
    problems = []
    for rule in graph["rules"]:
        rid = rule["id"]
        enforced = rule.get("enforcedBy", "")
        for match in re.findall(r"semantic_validate\.py::(\w+)", enforced):
            if match not in implemented:
                problems.append("%s claims %s, which is not in CHECKS" % (rid, match))
        alias = rule.get("ruleIdEmittedAs")
        if "semantic_validate.py" in enforced:
            names = [rid] + ([alias] if alias else [])
            if not any(n in source for n in names):
                problems.append("%s is enforced by the validator but neither its id "
                                "nor its declared ruleIdEmittedAs alias appears there"
                                % rid)
            if alias and alias not in {r["id"] for r in graph["rules"]}:
                problems.append("%s declares ruleIdEmittedAs %r, which is not a real "
                                "rule id" % (rid, alias))
        if "verify_all.py" in enforced:
            for match in re.findall(r"verify_all\.py::(\w+)", enforced):
                if match not in globals():
                    problems.append("%s claims verify_all.py::%s, which does not exist"
                                    % (rid, match))
    # every derived set must still equal what the real data says
    cats = {}
    for sid in contract_ids()["sections"]:
        cats[sid] = jload("sections", "%s.json" % sid)["category"]
    templates = jload("templates", "templates.json")["templates"]
    nohero = sorted(t for t, v in templates.items()
                    if not any(cats[n["section"]] == "hero" for n in v["nodes"]))
    claimed = graph["derivedSets"]["NO_HERO_TEMPLATES"]["value"]
    if sorted(claimed) != nohero:
        problems.append("NO_HERO_TEMPLATES claims %s, real data says %s"
                        % (claimed, nohero))
    home_only = sorted({n["section"] for n in templates["home"]["nodes"]
                        if not n["section"].startswith("chrome.")})
    if sorted(graph["derivedSets"]["HOME_ONLY_SECTIONS"]["value"]) != home_only:
        problems.append("HOME_ONLY_SECTIONS is stale")
    if graph.get("ruleCount") != len(graph["rules"]):
        problems.append("ruleCount is stale")
    if problems:
        record("graph-validator", FAIL, problems[0])
    else:
        record("graph-validator", PASS,
               "%d rules map to real checks; derived sets match the real data"
               % len(graph["rules"]))


def check_pinned_asset_policies():
    """PINNED_ASSET_POLICIES.

    Membership-in-a-closed-set is a weaker claim than 'this role must hold this
    value'. These four roles cover real trademarks, a real person's likeness and
    operative legal text, so each is checked against its EXACT pinned value --
    not merely against the enum.
    """
    registry = jload("assets", "asset-roles.json")
    allowed = set(registry["generationPolicyEnum"])
    pinned = {k: v for k, v in registry["pinnedPolicies"].items() if k != "note"}
    problems = []
    for role, spec in sorted(registry["roles"].items()):
        policy = spec.get("generationPolicy")
        if policy not in allowed:
            problems.append("%s has policy %r, outside the closed enum" % (role, policy))
        if role in pinned and policy != pinned[role]:
            problems.append("PINNED role %s must be %r but is %r"
                            % (role, pinned[role], policy))
    for role in pinned:
        if role not in registry["roles"]:
            problems.append("pinned role %s has no entry in roles" % role)
    allowlist = jload("tokens", "llm", "component-allowlist.json")
    if allowlist.get("pinnedAssetPolicies") != pinned:
        problems.append("the allowlist's pinnedAssetPolicies disagrees with the registry")
    for role, value in sorted(allowlist.get("assetRoles", {}).items()):
        real = registry["roles"].get(role, {}).get("generationPolicy")
        if value.get("generationPolicy") != real:
            problems.append("allowlist role %s says %r, registry says %r"
                            % (role, value.get("generationPolicy"), real))
    if problems:
        record("pinned-assets", FAIL, problems[0])
    else:
        record("pinned-assets", PASS,
               "%d roles within the enum; %d pinned roles hold their exact value"
               % (len(registry["roles"]), len(pinned)))



# --------------------------------------------------------------------------
# BASELINE R1-R10 checks (2.0.0)
# --------------------------------------------------------------------------

# PINNED_AVAILABILITY -- identical to schema/semantic_validate.py's pin, held here independently so that
# editing assets/asset-roles.json (or one of the two pins) alone cannot loosen a role.
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
# RETRIEVAL_INELIGIBLE -- identical to schema/semantic_validate.py's pin.
RETRIEVAL_INELIGIBLE = {"content.stub-notice", "faq.category-empty", "faq.common-questions-empty", "testimonials.slider-empty"}
RUNTIME_UI_HINT = re.compile(r"cookie|consent|modal|dialog|drawer|popup|overlay|preloader|toast|cursor|empty|stub", re.I)
AVAILABILITY = ("clone-only", "generation-safe", "blocked-for-generation")


def _script(rel, *args):
    proc = subprocess.run([sys.executable, "-I", os.path.join(REPO, rel)] + list(args), capture_output=True, text=True)
    return proc.returncode, (proc.stdout.strip().splitlines() or [proc.stderr.strip()[-200:]])[-1]


def _source_present():
    return os.path.isdir(os.path.join(SOURCE_ROOT, "src"))


def check_generated_artifacts():
    """Generated files rebuilt in memory and compared: schema branches, token catalog, generation examples."""
    probs = []
    for rel in ("schema/build_schema.py", "extraction/build_token_catalog.py", "extraction/build_generation_examples.py"):
        code, last = _script(rel)
        if code:
            probs.append("%s: %s" % (rel, last))
    if probs:
        record("generated-files", FAIL, "; ".join(probs))
    else:
        record("generated-files", PASS, "schema branches, token catalog and generation examples equal a rebuild from their sources")


def check_token_policy():
    """R10: catalog + policy registered, every policy category/slot/allow entry resolves against the catalog,
    theme rules equal the semantic validator's pin, every fill enum is covered."""
    import semantic_validate as sv
    cat = jload("tokens", "llm", "token-catalog.json")
    pol = jload("tokens", "llm", "token-policy.json")
    man = jload("registry.manifest.json")
    probs = []
    ep = man.get("entryPoints", {})
    if ep.get("tokenCatalog") != "tokens/llm/token-catalog.json" or ep.get("tokenPolicy") != "tokens/llm/token-policy.json":
        probs.append("token catalog/policy not registered in registry.manifest.json entryPoints")
    cats = set(cat["counts"]["byCategory"])
    for c in pol["allowedTokenCategories"] + pol["notGenerationApproved"]["categories"]:
        if c not in cats:
            probs.append("policy category %r is not a catalog category" % c)
    if sorted(pol["notGenerationApproved"]["categories"]) != sorted(cat["notGenerationApprovedCategories"]):
        probs.append("notGenerationApproved categories != catalog notGenerationApprovedCategories")
    if set(pol["allowedTokenCategories"]) | set(pol["notGenerationApproved"]["categories"]) != cats:
        probs.append("allowedTokenCategories + notGenerationApproved do not cover the catalog categories exactly")
    schema_slots = set(jload("schema", "pagespec.schema.json")["properties"]["tokens"]["properties"])
    slots = {k: v for k, v in pol["pageSpecTokenSlots"].items() if not k.startswith("$")}
    if set(slots) != schema_slots:
        probs.append("token slots in policy %s != schema tokens properties %s" % (sorted(slots), sorted(schema_slots)))
    kind_ok = {"semanticColor": ("semanticColor", "authColor"), "fontFamily": ("fontFamily",), "spacing": ("spacing", "authSpacing"),
               "radius": ("radius", "authRadius")}
    for name, s in slots.items():
        for path in s["allow"]:
            e = cat["tokens"].get(path)
            if e is None:
                probs.append("slot %s allows %r, which is not in the catalog" % (name, path))
            elif e["category"] not in kind_ok.get(s["kind"], (s["kind"],)):
                probs.append("slot %s (%s) allows %r of category %s" % (name, s["kind"], path, e["category"]))
    for path in pol["nodeFillSlots"]["allow"]:
        if cat["tokens"].get(path, {}).get("category") != "color":
            probs.append("fill allow %r is not a catalog colour" % path)
    allowed_fills = set(pol["nodeFillSlots"]["allow"]) | {pol["nodeFillSlots"]["noFillSentinel"]}
    for sid in contract_ids()["sections"]:
        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k == "fill" and isinstance(v, dict) and "enum" in v and not set(v["enum"]) <= allowed_fills:
                        probs.append("%s fill enum %s outside nodeFillSlots" % (sid, sorted(set(v["enum"]) - allowed_fills)))
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(jload("sections", "%s.json" % sid)["content"])
    tr = pol["themeRules"]
    if tr["minTextContrast"] != sv.PINNED_THEME_RULES["minTextContrast"]:
        probs.append("themeRules.minTextContrast != PINNED_THEME_RULES")
    for theme, th in cat["themes"].items():
        pin = sv.PINNED_THEME_RULES.get(theme)
        if not pin or pin["designSystem"] != th["designSystem"] or pin["tokenScopes"] != th["tokenScopes"]:
            probs.append("theme %s scopes/designSystem disagree with PINNED_THEME_RULES" % theme)
    if sorted(cat["themes"]) != sorted(jload("registry.manifest.json")["schemaValidatedThemes"]):
        probs.append("catalog themes != manifest schemaValidatedThemes")
    if probs:
        record("token-policy", FAIL, "; ".join(probs[:3]))
    else:
        record("token-policy", PASS, "%d catalog tokens / %d categories; %d slots + fills resolve; theme rules pinned"
               % (cat["counts"]["tokens"], len(cats), len(slots)))


def check_asset_availability():
    """R3: every role has a closed availability equal to BOTH code pins and the allowlist; substitutes exist and
    are generation-safe; a real mark is never must-reuse-exact; generatedAssetRoles are recomputed."""
    import semantic_validate as sv
    reg = jload("assets", "asset-roles.json")
    roles = reg["roles"]
    allow = jload("tokens", "llm", "component-allowlist.json")
    probs = []
    if PINNED_AVAILABILITY != sv.PINNED_AVAILABILITY:
        probs.append("verify_all PINNED_AVAILABILITY != semantic_validate PINNED_AVAILABILITY")
    if set(roles) != set(PINNED_AVAILABILITY):
        probs.append("roles not pinned / pins without roles: %s" % sorted(set(roles) ^ set(PINNED_AVAILABILITY)))
    for r, spec in sorted(roles.items()):
        av = spec.get("availability")
        if av not in AVAILABILITY:
            probs.append("%s availability %r outside the closed enum" % (r, av))
        if PINNED_AVAILABILITY.get(r) != av:
            probs.append("PINNED role %s must be %r but the registry says %r" % (r, PINNED_AVAILABILITY.get(r), av))
        if reg["pinnedAvailability"].get(r) != av:
            probs.append("registry pinnedAvailability[%s] disagrees with the role" % r)
        if (allow["assetRoles"].get(r) or {}).get("availability") != av:
            probs.append("allowlist role %s availability disagrees" % r)
        subs = spec.get("generationSafeSubstitutes")
        if not isinstance(subs, list) or not spec.get("generatedModeGuidance"):
            probs.append("%s lacks generationSafeSubstitutes / generatedModeGuidance" % r)
        elif av != "generation-safe" and not subs:
            probs.append("%s is %s with no generation-safe substitute" % (r, av))
        for s in subs or []:
            if PINNED_AVAILABILITY.get(s) != "generation-safe":
                probs.append("%s substitute %s is not generation-safe" % (r, s))
    for mark in ("brand.wordmark", "press.logo"):
        if roles[mark]["generationPolicy"] == "must-reuse-exact" or PINNED_AVAILABILITY[mark] == "generation-safe":
            probs.append("real mark %s must never be must-reuse-exact / generation-safe" % mark)
    for sid in contract_ids()["sections"]:
        c = jload("sections", "%s.json" % sid)
        found = []

        def walk(o):
            if isinstance(o, dict):
                if "allowedRoles" in o:
                    found.extend(o["allowedRoles"])
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(c["content"])
        want = [r for r in dict.fromkeys(found) if PINNED_AVAILABILITY.get(r) == "generation-safe"]
        if "blob.fill" in c["assetRoles"] and "blob.fill" not in want:
            want.insert(0, "blob.fill")
        if c.get("generatedAssetRoles") != want:
            probs.append("%s generatedAssetRoles %s != recomputed %s" % (sid, c.get("generatedAssetRoles"), want))
        if allow["sections"][sid].get("generatedAssetRoles") != c.get("generatedAssetRoles"):
            probs.append("%s allowlist generatedAssetRoles disagrees with the contract" % sid)
        for r in found:
            if PINNED_AVAILABILITY.get(r) != "generation-safe" and not set(roles[r]["generationSafeSubstitutes"]) <= set(found):
                probs.append("%s: a field allows %s but not its substitutes" % (sid, r))
    if probs:
        record("asset-availability", FAIL, "; ".join(probs[:3]))
    else:
        n = sum(1 for v in PINNED_AVAILABILITY.values() if v == "generation-safe")
        record("asset-availability", PASS, "%d roles pinned in BOTH validators (%d generation-safe); substitutes + generatedAssetRoles consistent"
               % (len(roles), n))


def check_retrieval_pin():
    """R8: retrievalEligible on every contract equals BOTH pins and the allowlist; ineligible ones have a reason."""
    import semantic_validate as sv
    allow = jload("tokens", "llm", "component-allowlist.json")["sections"]
    probs = []
    if RETRIEVAL_INELIGIBLE != sv.RETRIEVAL_INELIGIBLE:
        probs.append("verify_all RETRIEVAL_INELIGIBLE != semantic_validate RETRIEVAL_INELIGIBLE")
    false_n = 0
    for sid in contract_ids()["sections"]:
        c = jload("sections", "%s.json" % sid)
        want = sid not in RETRIEVAL_INELIGIBLE
        if c.get("retrievalEligible") is not want:
            probs.append("%s retrievalEligible %r, pin says %r" % (sid, c.get("retrievalEligible"), want))
        if allow[sid].get("retrievalEligible") is not c.get("retrievalEligible"):
            probs.append("%s allowlist retrievalEligible disagrees with the contract" % sid)
        if not want:
            false_n += 1
            if len(str(c.get("retrievalReason", ""))) < 30:
                probs.append("%s ineligible without a 30+ char reason" % sid)
        elif RUNTIME_UI_HINT.search(sid + " " + c.get("name", "")):
            probs.append("%s looks like runtime UI but is not in RETRIEVAL_INELIGIBLE" % sid)
    for sid in RETRIEVAL_INELIGIBLE:
        if sid not in contract_ids()["sections"]:
            probs.append("pinned %s has no contract" % sid)
    if probs:
        record("retrieval-pin", FAIL, "; ".join(probs[:3]))
    else:
        record("retrieval-pin", PASS, "%d contracts, %d retrieval-ineligible, pinned in both validators + allowlist"
               % (len(contract_ids()["sections"]), false_n))


def check_section_contracts():
    """R7: every contract validates the CLOSED schema/section-contract.schema.json; semantic.id == id and
    source.id != id; source ranges re-derived (and the tag re-read at the cited line) from the real files."""
    import _draft7
    schema = jload("schema", "section-contract.schema.json")
    probs = []
    if _draft7.check_schema(schema):
        probs.append("section-contract schema uses unsupported keywords")
    checked = 0
    for sid in contract_ids()["sections"]:
        c = jload("sections", "%s.json" % sid)
        for where, msg in _draft7.validate(c, schema)[:1]:
            probs.append("%s %s %s" % (sid, where, msg))
        if (c.get("semantic") or {}).get("id") != c["id"]:
            probs.append("%s semantic.id != id" % sid)
        if (c.get("source") or {}).get("id") == c["id"]:
            probs.append("%s source.id must not equal the contract id" % sid)
        src = c.get("source") or {}
        real = os.path.join(SOURCE_ROOT, src.get("file", ""))
        if _source_present() and os.path.isfile(real):
            lo, hi = map(int, src["lines"].split("-"))
            lines = open(real, encoding="utf-8").read().split("\n")
            if hi > len(lines) or "<" + src["tag"] not in lines[lo - 1] or ("</" + src["tag"] not in lines[hi - 1] and not lines[hi - 1].rstrip().endswith("/>")):
                probs.append("%s source %s:%s does not open/close <%s> there" % (sid, src["file"], src["lines"], src["tag"]))
            checked += 1
        elif _source_present():
            probs.append("%s source file %s missing" % (sid, src.get("file")))
    if _source_present():
        code, last = _script("extraction/build_section_provenance.py")
        if code:
            probs.append(last)
    if probs:
        record("section-contracts", FAIL, "; ".join(probs[:3]))
    else:
        record("section-contracts", PASS if _source_present() else WARN,
               "%d contracts validate the closed contract schema; source/semantic split; %s"
               % (len(contract_ids()["sections"]),
                  "%d source ranges re-read + provenance rebuilt" % checked if _source_present() else "no sibling source tree, ranges NOT re-read"))


def check_source_identity():
    """R2: the generation-mode leakage registry equals a rebuild from the real source."""
    if not _source_present():
        record("source-identity", WARN, "no sibling source tree; checked-in schema/source-identity.json used as-is")
        return
    code, last = _script("extraction/build_source_identity.py")
    record("source-identity", FAIL if code else PASS, last)


def check_examples():
    """R4: every template family has >= 1 mode:generation example; every example passes both validators."""
    import semantic_validate as sv
    tp = jload("templates", "templates.json")
    fams = {t["family"] for t in tp["templates"].values()}
    covered, probs = set(), []
    edir = os.path.join(REPO, "schema", "examples")
    names = sorted(n for n in os.listdir(edir) if n.endswith(".json"))
    reg = sv.load_registry()
    for n in names:
        spec = jload("schema", "examples", n)
        if spec.get("mode") != "generation":
            probs.append("%s is not mode:generation" % n)
        se = sv.validate_schema(spec)
        errs, _ = sv.validate_spec(spec, reg)
        if se or errs:
            probs.append("%s: %s" % (n, (se or errs)[0]))
        covered.add(tp["templates"].get(spec.get("template"), {}).get("family"))
    clone = jload("schema", "example.pagespec.json")
    if clone.get("mode") != "clone":
        probs.append("schema/example.pagespec.json must be the mode:clone example")
    missing = sorted(fams - covered)
    if missing:
        probs.append("template families without a generation example: %s" % missing)
    if probs:
        record("examples", FAIL, "; ".join(probs[:3]))
    else:
        record("examples", PASS, "%d generation examples cover all %d template families; clone example present" % (len(names), len(fams)))


def check_wrapper_gate():
    """R9: extraction/wrapper_gate.py over the measured 1440px section heights."""
    sys.path.insert(0, os.path.join(REPO, "extraction"))
    import wrapper_gate
    pins = (wrapper_gate.HERO_WARN_PX, wrapper_gate.HERO_ERROR_PX, wrapper_gate.SHARE_WARN, wrapper_gate.SHARE_ERROR,
            wrapper_gate.MIN_INFLOW_SECTIONS, wrapper_gate.REQUIRED_VIEWPORT, wrapper_gate.MIN_JUSTIFICATION)
    if pins != (1800, 3000, 0.50, 0.60, 3, 1440, 30):
        record("wrapper-gate", FAIL, "gate thresholds %s differ from the pinned baseline (1800, 3000, 0.5, 0.6, 3, 1440, 30)" % (pins,))
        return
    errors, warnings, _ = wrapper_gate.run(REPO)
    if errors:
        record("wrapper-gate", FAIL, "%d error(s): %s" % (len(errors), errors[0]))
    else:
        record("wrapper-gate", PASS, "0 errors, %d warning(s)%s" % (len(warnings), (": " + "; ".join(w[:70] for w in warnings)) if warnings else ""))


def check_routes_from_source():
    """R11: every route the clone's router serves is mapped exactly once (enumerated from src/App.jsx)."""
    app = os.path.join(SOURCE_ROOT, "src", "App.jsx")
    if not os.path.isfile(app):
        record("routes-from-source", WARN, "no sibling source tree; router not re-read")
        return
    served = re.findall(r'<Route\s+path="([^"]+)"', open(app, encoding="utf-8").read())
    mapping = jload("templates", "templates.json")["routeToTemplate"]
    dup = sorted({r for r in served if served.count(r) > 1})
    if sorted(set(served)) != sorted(mapping) or dup:
        record("routes-from-source", FAIL, "router serves %s, templates map %s, duplicates %s" % (sorted(served), sorted(mapping), dup))
    else:
        record("routes-from-source", PASS, "%d routes in src/App.jsx == %d mapped routes, each exactly once" % (len(served), len(mapping)))


def check_legal_parts():
    """The legal decomposition's per-document part counts equal the real documents' heading counts."""
    want = jload("sections", "legal.document-part.json")["constraints"]["documentParts"]
    if not _source_present():
        record("legal-parts", WARN, "no sibling source tree; part counts not re-counted")
        return
    got = {}
    for ref, fname in (("terms-of-use", "terms.js"), ("privacy-policy", "privacy.js")):
        text = open(os.path.join(SOURCE_ROOT, "src", "data", "legal", fname), encoding="utf-8").read()
        got[ref] = len(re.findall(r"^\s{6}heading:", text, re.M))
    bad = {k: (want.get(k), v) for k, v in got.items() if want.get(k) != v}
    record("legal-parts", FAIL if bad else PASS,
           "declared vs re-counted: %s" % bad if bad else "terms-of-use %d / privacy-policy %d heading-bounded parts re-counted from src/data/legal" % (got["terms-of-use"], got["privacy-policy"]))


CITE = re.compile(r"^([A-Za-z0-9_./\-]+\.(?:md|css|jsx|js|json|html)):(\d+)-(\d+)$")


def collect_citations():
    out = []

    def walk(node, rel):
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, str) and ("measuredFrom" in key or key == "definedIn"):
                    out.append((rel, key, value))
                else:
                    walk(value, rel)
        elif isinstance(node, list):
            for value in node:
                walk(value, rel)

    for rel in all_json():
        walk(jload(rel), rel)
    return out


def check_citations():
    citations = collect_citations()
    ledger = jload("extraction", "measured-values.json")
    if not os.path.isdir(os.path.join(SOURCE_ROOT, "src")):
        record("citations", WARN,
               "%d citations recorded; no sibling source tree present, so range and "
               "keyword resolution is SKIPPED (this is a standalone copy)"
               % len(citations))
        return
    problems = []
    unparsed = []
    for rel, key, value in citations:
        match = CITE.match(value)
        if not match:
            unparsed.append("%s/%s -> %r" % (rel, key, value))
            continue
        path, lo, hi = match.group(1), int(match.group(2)), int(match.group(3))
        real = os.path.join(SOURCE_ROOT, path)
        if not os.path.exists(real):
            problems.append("%s cites missing file %s" % (rel, path))
            continue
        with open(real, encoding="utf-8", errors="replace") as handle:
            lines = handle.read().splitlines()
        if lo < 1 or hi < lo or hi > len(lines):
            problems.append("%s cites %s:%d-%d but the file has %d lines"
                            % (rel, path, lo, hi, len(lines)))
    # the on-topic half: a citation can be in range and still describe the wrong code
    offtopic = []
    for entry in ledger["citations"]:
        value = entry["measuredFrom"]
        match = CITE.match(value)
        if not match:
            offtopic.append("unparseable ledger citation %r" % value)
            continue
        path, lo, hi = match.group(1), int(match.group(2)), int(match.group(3))
        real = os.path.join(SOURCE_ROOT, path)
        if not os.path.exists(real):
            offtopic.append("ledger cites missing file %s" % path)
            continue
        with open(real, encoding="utf-8", errors="replace") as handle:
            lines = handle.read().splitlines()
        if hi > len(lines):
            offtopic.append("ledger citation %s out of range" % value)
            continue
        window = "\n".join(lines[lo - 1:hi])
        for needle in entry["keywords"]:
            if needle not in window:
                offtopic.append("%s: keyword %r is NOT inside the cited range (the "
                                "citation resolves but describes the wrong lines)"
                                % (value, needle))
    if unparsed:
        record("citations", FAIL, "unparseable: %s" % unparsed[:2])
    elif problems:
        record("citations", FAIL, "%d out of range: %s" % (len(problems), problems[:2]))
    elif offtopic:
        record("citations", FAIL, "%d off-topic: %s" % (len(offtopic), offtopic[:2]))
    else:
        record("citations", PASS,
               "%d citations in range; %d ledger entries keyword-verified on-topic"
               % (len(citations), len(ledger["citations"])))


def check_adversarial():
    script = os.path.join(REPO, "schema", "tests", "adversarial_test.py")
    proc = subprocess.run([sys.executable, "-I", script],
                          capture_output=True, text=True)
    tail = [l for l in proc.stdout.strip().splitlines() if l.startswith(("controls:", "RESULT"))]
    if proc.returncode != 0:
        record("adversarial", FAIL, " | ".join(tail) or proc.stdout[-200:])
    else:
        record("adversarial", PASS, " | ".join(tail))


def cross_check():
    """Diff the vendored validator against the reference jsonschema package."""
    try:
        from jsonschema import Draft7Validator
    except ImportError:
        print("  cross-check         SKIP jsonschema not installed (the repo does "
              "not need it; this is an optional second opinion)")
        return
    import _draft7
    sys.path.insert(0, os.path.join(REPO, "schema", "tests"))
    import adversarial_test as at
    schema = jload("schema", "pagespec.schema.json")
    Draft7Validator.check_schema(schema)
    cases = [("example", jload("schema", "example.pagespec.json"))]
    cases += [("control:" + t, at.synth_control(t))
              for t in sorted(at.TEMPLATES)]
    cases += [("mutation:" + l, s) for l, _, s in at.mutations()]
    disagree = []
    for label, spec in cases:
        mine = bool(_draft7.validate(spec, schema))
        theirs = bool(list(Draft7Validator(schema).iter_errors(spec)))
        if mine != theirs:
            disagree.append("%s (vendored=%s reference=%s)" % (label, mine, theirs))
    if disagree:
        print("  cross-check         FAIL %d disagreement(s): %s"
              % (len(disagree), disagree[:3]))
        return 1
    print("  cross-check         PASS vendored validator agrees with jsonschema on "
          "all %d cases" % len(cases))
    return 0


CHECKS = [
    check_json_parse,
    check_no_abs_paths,
    check_self_contained,
    check_schema,
    check_allowlist_parity,
    check_allowlist_schema,
    check_version_parity,
    check_manifest_counts,
    check_design_policy,
    check_route_coverage,
    check_graph_validator_agreement,
    check_pinned_asset_policies,
    check_citations,
    check_generated_artifacts,
    check_token_policy,
    check_asset_availability,
    check_retrieval_pin,
    check_section_contracts,
    check_source_identity,
    check_examples,
    check_wrapper_gate,
    check_routes_from_source,
    check_legal_parts,
    check_adversarial,
]


def prove_drift():
    """Delegates to extraction/prove_drift.py (the drift proof lives in its own script since 2.0.0)."""
    return subprocess.run([sys.executable, "-I", os.path.join(REPO, "extraction", "prove_drift.py")]).returncode


def main(argv):
    print("=" * 74)
    print("design-repo verification")
    print("repo: %s" % os.path.basename(REPO))
    print("sibling source tree: %s"
          % ("present" if os.path.isdir(os.path.join(SOURCE_ROOT, "src"))
             else "ABSENT (citation resolution will warn and skip)"))
    print("=" * 74)
    for check in CHECKS:
        try:
            check()
        except Exception as exc:
            record(check.__name__, FAIL, "raised %s: %s" % (type(exc).__name__, exc))
    extra = 0
    if "--cross-check" in argv:
        extra = cross_check() or 0
    failed = [r for r in results if r[1] == FAIL]
    warned = [r for r in results if r[1] == WARN]
    print("=" * 74)
    print("%d checks | %d pass | %d warn | %d FAIL"
          % (len(results), len(results) - len(failed) - len(warned),
             len(warned), len(failed)))
    print("RESULT: %s" % ("FAIL" if failed or extra else "PASS"))
    if "--prove-drift" in argv:
        extra = prove_drift() or extra
    return 1 if (failed or extra) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
