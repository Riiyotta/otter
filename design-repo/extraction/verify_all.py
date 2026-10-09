#!/usr/bin/env python3
"""One-shot verification for the Otter design-repo.

Runs every automated consistency check this repo claims to have. Each check is
drift-proofed: it recomputes a fact from the real files rather than trusting a
hand-maintained summary, so a stale number fails the run instead of looking
coherent.

  1  json-parse        every JSON file parses
  2  no-abs-paths      no absolute local machine paths anywhere in the tree
  3  self-contained    manifest entryPoints are all INSIDE design-repo/
  4  schema            the bundled example validates draft-07 with 0 errors
  5  allowlist-parity  allowlist <-> contract files, both directions
  6  allowlist-schema  allowlist settable props <-> the real schema
  7  version-parity    manifest.allowlistVersion == allowlist.version
  8  manifest-counts    manifest counts recomputed from disk
  9  route-coverage     every route assigned exactly once, 1:1 with templates
 10  graph-validator    every graph rule maps to a real check in the validator
 11  pinned-assets      the four compliance-critical roles hold their exact value
 12  citations          every measuredFrom resolves, in range AND on-topic
 13  adversarial        the full control + mutation suite

Citation checks degrade gracefully: with no sibling source tree present (a
standalone copy, or an extracted zip) they WARN and skip rather than fail, since
the evidence they point at is build-time context, not shipped content.

Paths derive from __file__, never hardcoded.

Usage:
    python3 verify_all.py                # everything
    python3 verify_all.py --cross-check  # also diff the vendored validator
                                         # against the reference `jsonschema`
                                         # package, if it happens to be installed
    python3 verify_all.py --prove-drift  # prove the drift checks actually fail
                                         # on bad input, in a scratch copy
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

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
    want = allowlist["version"]
    got = manifest.get("allowlistVersion")
    if got != want:
        record("version-parity", FAIL,
               "manifest.allowlistVersion %r != allowlist.version %r" % (got, want))
    else:
        record("version-parity", PASS, "allowlistVersion %s (machine-checked)" % want)


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
    }
    claimed = manifest.get("counts", {})
    bad = {k: (claimed.get(k), v) for k, v in actual.items() if claimed.get(k) != v}
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
    check_route_coverage,
    check_graph_validator_agreement,
    check_pinned_asset_policies,
    check_citations,
    check_adversarial,
]


def prove_drift():
    """Prove the drift checks actually FAIL on bad input.

    A check that has only ever been run against a correct repo might not be
    checking anything. Each case below copies the repo to a scratch directory,
    injects one specific defect, and asserts the matching check flips to FAIL --
    then confirms the real repo still passes.
    """
    cases = [
        ("phantom allowlist entry", "allowlist-parity",
         lambda d: _edit(d, "tokens/llm/component-allowlist.json",
                         lambda j: j["sections"].update(
                             {"hero.nonexistent": {"contractFile":
                                                   "sections/hero.nonexistent.json"}}))),
        ("orphaned contract (allowlist entry removed)", "allowlist-parity",
         lambda d: _edit(d, "tokens/llm/component-allowlist.json",
                         lambda j: j["sections"].pop("trust.press-bar"))),
        ("out-of-range citation", "citations",
         lambda d: _edit(d, "tokens/00-foundation/color.json",
                         lambda j: j["tokens"]["color.primary"].update(
                             measuredFrom="CLONE_SPEC.md:99000-99001")), True),
        ("in-range but OFF-TOPIC citation", "citations",
         lambda d: _edit(d, "extraction/measured-values.json",
                         lambda j: j["citations"][0].update(
                             measuredFrom="CLONE_SPEC.md:1-3")), True),
        ("hand-bumped manifest count", "manifest-counts",
         lambda d: _edit(d, "registry.manifest.json",
                         lambda j: j["counts"].update(sections=99))),
        ("allowlistVersion drift", "version-parity",
         lambda d: _edit(d, "registry.manifest.json",
                         lambda j: j.update(allowlistVersion="9.9.9"))),
        ("pinned asset policy switched to a DIFFERENT-BUT-VALID enum member",
         "pinned-assets",
         lambda d: _edit(d, "assets/asset-roles.json",
                         lambda j: j["roles"]["press.logo"].update(
                             generationPolicy="may-generate-new"))),
        ("entryPoint pointing outside design-repo/", "self-contained",
         lambda d: _edit(d, "registry.manifest.json",
                         lambda j: j["entryPoints"].update(
                             external=["../CLONE_SPEC.md"]))),
        ("absolute local path introduced", "no-abs-paths",
         lambda d: _append(d, "README.md",
                           "\nBuilt at " + "/" + "Users" + "/someone/project\n")),
        ("stale derived set in the graph", "graph-validator",
         lambda d: _edit(d, "compatibility/graph.json",
                         lambda j: j["derivedSets"]["NO_HERO_TEMPLATES"].update(
                             value=["home"]))),
        ("allowlist drifted from the schema", "allowlist-schema",
         lambda d: _edit(d, "tokens/llm/component-allowlist.json",
                         lambda j: j["sections"]["trust.press-bar"].update(
                             requiredContentFields=["eyebrow"]))),
        ("route double-assigned to two templates", "route-coverage",
         lambda d: _edit(d, "templates/templates.json",
                         lambda j: j["templates"]["contact"]["routes"].append("/careers"))),
    ]
    print()
    print("=" * 74)
    print("DRIFT PROOF -- inject one defect per scratch copy; the matching check")
    print("must flip to FAIL. Proves these checks catch drift, not just that they")
    print("pass on a correct repo.")
    print("=" * 74)
    failures = 0
    cases = [c if len(c) == 4 else (c[0], c[1], c[2], False) for c in cases]
    for label, expect, mutate, needs_source in cases:
        tmp = tempfile.mkdtemp(prefix="drift-")
        dest = os.path.join(tmp, "design-repo")
        shutil.copytree(REPO, dest,
                        ignore=shutil.ignore_patterns("__pycache__"))
        if needs_source:
            # A citation defect can only be CAUGHT where the cited evidence is
            # resolvable. Without this the check correctly warns-and-skips and
            # the injected defect is unobservable -- which is a flaw in the
            # proof, not in the check. Stage just the cited files as siblings.
            staged = _stage_cited_sources(tmp)
            if not staged:
                print("  %-58s SKIP (no source tree to stage from)" % label[:58])
                shutil.rmtree(tmp, ignore_errors=True)
                continue
        mutate(dest)
        proc = subprocess.run(
            [sys.executable, "-I", os.path.join(dest, "extraction", "verify_all.py")],
            capture_output=True, text=True)
        line = next((l for l in proc.stdout.splitlines()
                     if l.strip().startswith(expect)), "")
        caught = " FAIL " in line
        print("  %-58s %s" % (label[:58], "caught" if caught else "NOT CAUGHT"))
        if not caught:
            failures += 1
            print("      expected %r to FAIL; got: %s" % (expect, line.strip() or "(no line)"))
        shutil.rmtree(tmp, ignore_errors=True)
    print()
    print("drift cases: %d | not caught: %d" % (len(cases), failures))
    print("DRIFT PROOF: %s" % ("FAIL" if failures else "PASS"))
    return 1 if failures else 0


def _stage_cited_sources(tmp):
    """Copy every file this repo cites into `tmp`, mirroring its relative path,
    so a scratch copy at tmp/design-repo can resolve its own citations."""
    if not os.path.isdir(os.path.join(SOURCE_ROOT, "src")):
        return 0
    wanted = set()
    for _, _, value in collect_citations():
        match = CITE.match(value)
        if match:
            wanted.add(match.group(1))
    for entry in jload("extraction", "measured-values.json")["citations"]:
        match = CITE.match(entry["measuredFrom"])
        if match:
            wanted.add(match.group(1))
    staged = 0
    for rel in sorted(wanted):
        src = os.path.join(SOURCE_ROOT, rel)
        if not os.path.exists(src):
            continue
        dst = os.path.join(tmp, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        staged += 1
    # the citation check gates on the presence of a src/ directory
    os.makedirs(os.path.join(tmp, "src"), exist_ok=True)
    return staged


def _edit(root, rel, fn):
    path = os.path.join(root, rel)
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    fn(data)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def _append(root, rel, text):
    with open(os.path.join(root, rel), "a", encoding="utf-8") as handle:
        handle.write(text)


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
