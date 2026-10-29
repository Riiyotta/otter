#!/usr/bin/env python3
"""Prove every drift check / pin / gate in extraction/verify_all.py actually FAILS on bad input (BASELINE R5/R14).

    python3 extraction/prove_drift.py --scratch <dir>      # <dir> must be empty or absent; it is created
    python3 extraction/prove_drift.py                      # uses a fresh OS temp dir

Each case copies design-repo/ to <scratch>/<case>/design-repo, injects ONE defect, runs that copy's
verify_all.py and asserts the named check flips to FAIL. Source-dependent cases (citations, provenance,
source identity, router, legal part counts) need the sibling source project: its top-level entries are
symlinked next to each scratch copy; with no source tree those cases are reported SKIP, never PASS.
A control case (no defect) must pass first, so a case can only "catch" what it injected.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SOURCE_ROOT = os.path.dirname(REPO)
SKIP_TOP = {"design-repo", "node_modules", "dist", ".git", "design-repo.zip"}


def edit(root, rel, fn):
    p = os.path.join(root, rel)
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    fn(d)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2)
        f.write("\n")


def sub(root, rel, old, new, count=1):
    p = os.path.join(root, rel)
    t = open(p, encoding="utf-8").read()
    if old not in t:
        raise AssertionError("%s: %r not found" % (rel, old[:60]))
    open(p, "w", encoding="utf-8").write(t.replace(old, new, count))


def append(root, rel, text):
    with open(os.path.join(root, rel), "a", encoding="utf-8") as f:
        f.write(text)


def heights(fn):
    return lambda r: edit(r, "extraction/measured-values.json", lambda d: fn(d["sectionHeights"]))


def hero_to(px):
    def f(h):
        for s in h["routes"]["/"]["sections"]:
            if s["section"] == "hero.dark-rounded":
                s["heightPx"] = px
        h["routes"]["/"]["pageHeight"] += px
    return f


S = True  # needs the sibling source tree
CASES = [
    # (label, check expected to FAIL, mutate(root), needs_source)
    ("phantom allowlist entry", "allowlist-parity",
     lambda r: edit(r, "tokens/llm/component-allowlist.json", lambda j: j["sections"].update({"hero.nonexistent": {"contractFile": "sections/hero.nonexistent.json"}})), False),
    ("orphaned contract (allowlist entry removed)", "allowlist-parity",
     lambda r: edit(r, "tokens/llm/component-allowlist.json", lambda j: j["sections"].pop("trust.press-bar")), False),
    ("allowlist drifted from the schema", "allowlist-schema",
     lambda r: edit(r, "tokens/llm/component-allowlist.json", lambda j: j["sections"]["trust.press-bar"].update(requiredContentFields=["eyebrow"])), False),
    ("out-of-range citation", "citations",
     lambda r: edit(r, "tokens/00-foundation/elevation.json", lambda j: j["tokens"]["elevation.whiteBtnHover"].update(measuredFrom="CLONE_SPEC.md:99000-99001")), S),
    ("in-range but OFF-TOPIC ledger citation", "citations",
     lambda r: edit(r, "extraction/measured-values.json", lambda j: j["citations"][0].update(measuredFrom="CLONE_SPEC.md:1-3")), S),
    ("hand-bumped manifest count", "manifest-counts",
     lambda r: edit(r, "registry.manifest.json", lambda j: j["counts"].update(sections=99)), False),
    ("catalog token count hand-bumped", "manifest-counts",
     lambda r: edit(r, "registry.manifest.json", lambda j: j["counts"].update(catalogTokens=1)), False),
    ("allowlistVersion drift", "version-parity",
     lambda r: edit(r, "registry.manifest.json", lambda j: j.update(allowlistVersion="9.9.9")), False),
    ("tokenCatalogVersion drift", "version-parity",
     lambda r: edit(r, "registry.manifest.json", lambda j: j.update(tokenCatalogVersion="0.0.1")), False),
    ("pinned asset policy switched to a DIFFERENT-BUT-VALID enum member", "pinned-assets",
     lambda r: edit(r, "assets/asset-roles.json", lambda j: j["roles"]["press.logo"].update(generationPolicy="may-generate-new")), False),
    ("entryPoint pointing outside design-repo/", "self-contained",
     lambda r: edit(r, "registry.manifest.json", lambda j: j["entryPoints"].update(external=["../CLONE_SPEC.md"])), False),
    ("absolute local path introduced", "no-abs-paths",
     lambda r: append(r, "README.md", "\nBuilt at " + "/" + "Users" + "/someone/project\n"), False),
    ("stale derived set in the graph", "graph-validator",
     lambda r: edit(r, "compatibility/graph.json", lambda j: j["derivedSets"]["NO_HERO_TEMPLATES"].update(value=["home"])), False),
    ("route double-assigned to two templates", "route-coverage",
     lambda r: edit(r, "templates/templates.json", lambda j: j["templates"]["contact"]["routes"].append("/careers")), False),
    # ---- R11 routes from the real router
    ("served route dropped from the templates", "routes-from-source",
     lambda r: edit(r, "templates/templates.json", lambda j: (j["routeToTemplate"].pop("/faq"), j["templates"]["faq-categories"]["routes"].remove("/faq"))), S),
    # ---- R3 availability pins
    ("registry availability loosened (photo.person -> generation-safe)", "asset-availability",
     lambda r: edit(r, "assets/asset-roles.json", lambda j: j["roles"]["photo.person"].update(availability="generation-safe")), False),
    ("registry + allowlist + registry pin loosened TOGETHER (code pin still catches)", "asset-availability",
     lambda r: (edit(r, "assets/asset-roles.json", lambda j: (j["roles"]["press.logo"].update(availability="generation-safe"), j["pinnedAvailability"].update({"press.logo": "generation-safe"}))),
                edit(r, "tokens/llm/component-allowlist.json", lambda j: j["assetRoles"]["press.logo"].update(availability="generation-safe"))), False),
    ("pin removed from verify_all.py", "asset-availability",
     lambda r: sub(r, "extraction/verify_all.py", '    "photo.person": "clone-only",\n', ""), False),
    ("pin removed from semantic_validate.py", "asset-availability",
     lambda r: sub(r, "schema/semantic_validate.py", '    "photo.person": "clone-only",\n', ""), False),
    ("generation-safe substitute removed from a clone-only role", "asset-availability",
     lambda r: edit(r, "assets/asset-roles.json", lambda j: j["roles"]["icon.values"].update(generationSafeSubstitutes=[])), False),
    ("generatedAssetRoles hand-edited on a contract", "asset-availability",
     lambda r: edit(r, "sections/trust.video-and-cards.json", lambda j: j.update(generatedAssetRoles=["photo.person"])), False),
    # ---- R8 retrieval
    ("empty-state contract AND allowlist flipped to eligible together", "retrieval-pin",
     lambda r: (edit(r, "sections/testimonials.slider-empty.json", lambda j: (j.update(retrievalEligible=True), j.pop("retrievalReason"))),
                edit(r, "tokens/llm/component-allowlist.json", lambda j: j["sections"]["testimonials.slider-empty"].update(retrievalEligible=True))), False),
    ("content contract marked ineligible", "retrieval-pin",
     lambda r: edit(r, "sections/hero.light-split.json", lambda j: j.update(retrievalEligible=False, retrievalReason="x" * 40)), False),
    ("retrieval pin removed from semantic_validate.py", "retrieval-pin",
     lambda r: sub(r, "schema/semantic_validate.py", '    "content.stub-notice",\n', ""), False),
    # ---- R7 provenance / closed contract schema
    ("source line range shifted by hand", "section-contracts",
     lambda r: edit(r, "sections/hero.dark-rounded.json", lambda j: j["source"].update(lines="6-102")), S),
    ("semantic.id differing from the contract id", "section-contracts",
     lambda r: edit(r, "sections/stats.grid.json", lambda j: j["semantic"].update(id="stats.other")), False),
    ("invented top-level key on a contract (closed schema)", "section-contracts",
     lambda r: edit(r, "sections/form.contact.json", lambda j: j.update(inventedField=True)), False),
    ("semantic category outside the closed taxonomy", "section-contracts",
     lambda r: edit(r, "sections/banner.beta-card.json", lambda j: j["semantic"].update(category="BANNER")), False),
    # ---- R10 tokens
    ("token file edited without rebuilding the catalog", "generated-files",
     lambda r: edit(r, "tokens/00-foundation/radius.json", lambda j: j["tokens"]["radius.card"].update({"$value": "30px"})), False),
    ("catalog edited alone", "generated-files",
     lambda r: sub(r, "tokens/llm/token-catalog.json", '"#00373e"', '"#00373f"'), False),
    ("policy slot allowing a token that is not in the catalog", "token-policy",
     lambda r: edit(r, "tokens/llm/token-policy.json", lambda j: j["pageSpecTokenSlots"]["surface"]["allow"].append("semantic.surface.night")), False),
    ("policy category that is not a catalog key", "token-policy",
     lambda r: edit(r, "tokens/llm/token-policy.json", lambda j: j["allowedTokenCategories"].append("shadow")), False),
    ("theme contrast pin loosened in policy only", "token-policy",
     lambda r: edit(r, "tokens/llm/token-policy.json", lambda j: j["themeRules"].update(minTextContrast=1.0)), False),
    ("token slot added to the policy but not the schema", "token-policy",
     lambda r: edit(r, "tokens/llm/token-policy.json", lambda j: j["pageSpecTokenSlots"].update(accent={"location": "tokens.accent", "kind": "color", "required": False, "allow": ["color.peach"], "purpose": "x"})), False),
    ("fill enum widened to a non-token colour", "token-policy",
     lambda r: edit(r, "sections/conversion.cta-card.json", lambda j: j["content"]["properties"]["blob"]["properties"]["fill"]["enum"].append("#ff0000")), False),
    ("token catalog unregistered from the manifest", "token-policy",
     lambda r: edit(r, "registry.manifest.json", lambda j: j["entryPoints"].pop("tokenCatalog")), False),
    # ---- schema / examples
    ("schema content branch edited alone", "generated-files",
     lambda r: edit(r, "schema/pagespec.schema.json", lambda j: j["properties"]["nodes"]["items"]["allOf"][0]["then"]["properties"]["content"]["properties"].pop("title")), False),
    ("generation example edited to carry the source brand", "examples",
     lambda r: edit(r, "schema/examples/generated.home.pagespec.json", lambda j: j["nodes"][1]["content"].update(heading="Otter care near you")), False),
    ("template family left without a generation example", "examples",
     lambda r: os.remove(os.path.join(r, "schema/examples/generated.not-found.pagespec.json")), False),
    ("clone example relabelled as generation", "examples",
     lambda r: edit(r, "schema/example.pagespec.json", lambda j: j.update(mode="generation")), False),
    # ---- R2 leakage registry
    ("leakage registry hand-edited (brand term removed)", "source-identity",
     lambda r: edit(r, "schema/source-identity.json", lambda j: j.update(terms=[t for t in j["terms"] if t["term"] != "Otter"])), S),
    # ---- R9 wrapper gate
    ("HERO measured at 3100px", "wrapper-gate", heights(hero_to(3100)), False),
    ("one section at 70% of its page", "wrapper-gate",
     heights(lambda h: ([s.update(heightPx=9000) for s in h["routes"]["/careers"]["sections"] if s["section"] == "benefits.card-grid"], h["routes"]["/careers"].update(pageHeight=14191))), False),
    ("missing measurement for a template node", "wrapper-gate",
     heights(lambda h: h["routes"]["/contact"]["sections"].pop(2)), False),
    ("measured at the wrong viewport", "wrapper-gate", heights(lambda h: h["viewport"].update(width=1280)), False),
    ("whitelist entry without justification / attestation", "wrapper-gate",
     lambda r: edit(r, "extraction/wrapper-gate-whitelist.json", lambda j: j["entries"].append({"route": "/blog", "section": "blog.post-grid", "rule": "SECTION_SHARE", "maxHeightPx": 9999, "justification": "short", "reviewedBy": "review agent"})), False),
    ("gate threshold loosened in code", "wrapper-gate",
     lambda r: sub(r, "extraction/wrapper_gate.py", "SHARE_WARN = 0.50", "SHARE_WARN = 0.90"), False),
    # ---- legal decomposition
    ("legal part count hand-edited", "legal-parts",
     lambda r: edit(r, "sections/legal.document-part.json", lambda j: j["constraints"]["documentParts"].update({"terms-of-use": 24})), S),
    # ---- requirement 10: policy binding
    ("bound policy switched to the SaaS policy", "design-policy",
     lambda r: edit(r, "registry.manifest.json", lambda j: j["designPolicy"].update(policyId="n0-saas-design-constraints-common")), False),
    ("bound policy version drift", "design-policy",
     lambda r: edit(r, "registry.manifest.json", lambda j: j["designPolicy"].update(policyVersion="0.2.0")), False),
    ("enforcing file changed without re-hashing", "design-policy",
     lambda r: append(r, "schema/semantic_validate.py", "\n# drift\n"), False),
    ("contentHash tampered", "design-policy",
     lambda r: edit(r, "registry.manifest.json", lambda j: j["designPolicy"].update(contentHash="sha256:" + "0" * 64)), False),
    ("local extension file missing", "design-policy",
     lambda r: os.remove(os.path.join(r, "policy/design-policy.json")), False),
    ("SaaS notBoundTo reason dropped", "design-policy",
     lambda r: edit(r, "registry.manifest.json", lambda j: j["designPolicy"].pop("notBoundTo")), False),
    ("stale 'pending architecture review' wording reintroduced", "design-policy",
     lambda r: append(r, "README.md", "\nPolicy status: defined, pending architecture review.\n"), False),
    ("approval reverted to undecided", "design-policy",
     lambda r: edit(r, "policy/design-policy.json", lambda j: j["approval"].update(architectureDecisionRecorded=False)), False),
    ("legal sign-off flag folded into the policy decision", "design-policy",
     lambda r: edit(r, "registry.manifest.json", lambda j: j["approvalFlags"].update(legalContentSignOff=True)), False),
    ("policy classified as SaaS", "design-policy",
     lambda r: edit(r, "policy/design-policy.json", lambda j: j["classification"].update(isSaaS=True)), False),
]


def stage_source(case_dir):
    """Symlink the sibling source project's top-level entries next to the scratch design-repo."""
    for name in os.listdir(SOURCE_ROOT):
        if name in SKIP_TOP or name.startswith("."):
            continue
        os.symlink(os.path.join(SOURCE_ROOT, name), os.path.join(case_dir, name))


def run_case(scratch, idx, label, expect, mutate, needs_source, have_source):
    case_dir = os.path.join(scratch, "case-%02d" % idx)
    os.makedirs(case_dir)
    dest = os.path.join(case_dir, "design-repo")
    shutil.copytree(REPO, dest, ignore=shutil.ignore_patterns("__pycache__"))
    if have_source:
        stage_source(case_dir)
    if mutate:
        mutate(dest)
    proc = subprocess.run([sys.executable, "-I", os.path.join(dest, "extraction", "verify_all.py")], capture_output=True, text=True)
    lines = proc.stdout.splitlines()
    line = next((l for l in lines if expect and l.strip().startswith(expect + " ")), "")
    shutil.rmtree(case_dir, ignore_errors=True)
    return proc.returncode, line, lines


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", help="empty (or absent) directory for the scratch copies")
    a = ap.parse_args(argv)
    scratch = a.scratch or tempfile.mkdtemp(prefix="otter-drift-")
    if os.path.exists(scratch) and os.listdir(scratch):
        print("--scratch %s is not empty; refusing to write into it" % scratch)
        return 2
    os.makedirs(scratch, exist_ok=True)
    have_source = os.path.isdir(os.path.join(SOURCE_ROOT, "src"))
    print("=" * 78)
    print("DRIFT PROOF -- one injected defect per scratch copy; the named verify_all check must FAIL")
    print("sibling source tree: %s" % ("present (symlinked into each scratch case)" if have_source else "ABSENT (source-dependent cases SKIP)"))
    print("=" * 78)
    code, _, lines = run_case(scratch, 0, "control", None, None, False, have_source)
    print("  %-70s %s" % ("control: unmodified copy passes verify_all", "PASS" if code == 0 else "FAIL"))
    if code != 0:
        print("\n".join("      " + l for l in lines if " FAIL " in l))
        return 1
    caught = missed = skipped = 0
    for i, (label, expect, mutate, needs_source) in enumerate(CASES, 1):
        if needs_source and not have_source:
            print("  %-70s SKIP (needs source)" % label[:70])
            skipped += 1
            continue
        _, line, _ = run_case(scratch, i, label, expect, mutate, needs_source, have_source)
        ok = " FAIL " in line
        caught += ok
        missed += not ok
        print("  %-70s %s" % (label[:70], "caught [%s]" % expect if ok else "NOT CAUGHT"))
        if not ok:
            print("      expected %r to FAIL; got: %s" % (expect, line.strip() or "(no line)"))
    shutil.rmtree(scratch, ignore_errors=True) if not a.scratch else None
    print()
    print("drift cases: %d | caught: %d | not caught: %d | skipped: %d" % (len(CASES), caught, missed, skipped))
    print("DRIFT PROOF: %s" % ("FAIL" if missed else "PASS"))
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
