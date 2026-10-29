#!/usr/bin/env python3
"""Whole-page-wrapper quality gate (BASELINE R9), run by extraction/verify_all.py.

Reads MEASURED section heights (extraction/measured-values.json -> sectionHeights, produced by
extraction/measure_sections.mjs from a local build of the clone at 1440px) and fails when a section behaves
like a whole-page wrapper:

  HERO height  > HERO_WARN_PX  (1800) -> warning
  HERO height  > HERO_ERROR_PX (3000) -> error, unless whitelisted (a whitelisted hit still warns)
  one in-flow section > SHARE_WARN  (50%) of its page -> warning
  one in-flow section > SHARE_ERROR (60%) of its page -> error, unless whitelisted (still warns)
    - pages with fewer than MIN_INFLOW_SECTIONS in-flow sections are skipped; SHELL sections (chrome) count
      toward that total but are never flagged themselves; fixed/sticky elements take no page height.
  missing measurement for any template node, any route not measured, or a wrong viewport -> error
  repeatable nodes (legal.document-part, faq.category-empty) are recorded per instance; each instance is gated.
  whitelist entries: reviewedBy required (an agent reviewer must say "agent attestation, not a human
  sign-off"), justification >= 30 chars, maxHeightPx above the measured height; stale entries -> error.

HERO / SHELL come from each contract's closed semantic.category (R7), never from wrapper/class names.
Thresholds are PINNED here in code (not read from JSON), so editing a data file cannot loosen them.

    python3 extraction/wrapper_gate.py            # gate the real measurements (exit 1 on error)
    python3 extraction/wrapper_gate.py --self-test
"""
import glob, json, os, sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

HERO_WARN_PX = 1800
HERO_ERROR_PX = 3000
SHARE_WARN = 0.50
SHARE_ERROR = 0.60
MIN_INFLOW_SECTIONS = 3
REQUIRED_VIEWPORT = 1440
MIN_JUSTIFICATION = 30
AGENT_ATTESTATION = "agent attestation, not a human sign-off"
WHITELIST_FILE = "extraction/wrapper-gate-whitelist.json"


def _jl(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as f:
        return json.load(f)


def _is(sid, contract, cat):
    sem = (contract or {}).get("semantic")
    return isinstance(sem, dict) and sem.get("category") == cat


def evaluate(heights, whitelist, sections, templates, routes):
    """Pure gate. routes = {path: template}. Returns (errors, warnings, infos)."""
    errors, warnings, infos = [], [], []
    if not isinstance(heights, dict) or not heights.get("routes"):
        return ["MISSING_MEASUREMENT: no sectionHeights recorded"], warnings, infos
    vw = (heights.get("viewport") or {}).get("width")
    if vw != REQUIRED_VIEWPORT:
        errors.append("WRONG_VIEWPORT: measured at width %r, required %d" % (vw, REQUIRED_VIEWPORT))
    entries = (whitelist or {}).get("entries", [])
    used = [False] * len(entries)

    def wl_for(route, sid, rule):
        for i, e in enumerate(entries):
            if e.get("rule") == rule and e.get("section") == sid and e.get("route") == route:
                return i, e
        return None, None

    for i, e in enumerate(entries):
        tag = "WHITELIST[%d] %s %s" % (i, e.get("section"), e.get("rule"))
        if e.get("rule") not in ("HERO_HEIGHT", "SECTION_SHARE"):
            errors.append("%s: rule must be HERO_HEIGHT or SECTION_SHARE" % tag)
        if not e.get("route"):
            errors.append("%s: needs route" % tag)
        if len(str(e.get("justification", "")).strip()) < MIN_JUSTIFICATION:
            errors.append("%s: justification missing or shorter than %d chars" % (tag, MIN_JUSTIFICATION))
        rb = str(e.get("reviewedBy", "")).strip()
        if not rb:
            errors.append("%s: reviewedBy missing" % tag)
        elif "agent" in rb.lower() and AGENT_ATTESTATION not in rb:
            errors.append("%s: an agent reviewer must state '%s'" % (tag, AGENT_ATTESTATION))
        if not isinstance(e.get("maxHeightPx"), (int, float)):
            errors.append("%s: maxHeightPx missing" % tag)

    for path, tmpl in routes.items():
        if path not in heights["routes"]:
            errors.append("MISSING_MEASUREMENT: route %s (template %s) not measured" % (path, tmpl))

    for path, rec in heights["routes"].items():
        tmpl = rec.get("template") or routes.get(path)
        page_h = rec.get("pageHeight")
        meas = {}
        for s in rec.get("sections", []):
            meas.setdefault((s.get("section"), s.get("variant") or None), []).append(s)
        for n in templates.get(tmpl, {}).get("nodes", []):
            key = (n["section"], n.get("variant") or None)
            if not any(isinstance(x.get("heightPx"), (int, float)) for x in meas.get(key, [])):
                errors.append("MISSING_MEASUREMENT: %s %s%s has no measured height" % (path, key[0], "/" + key[1] if key[1] else ""))
        if not isinstance(page_h, (int, float)) or page_h <= 0:
            errors.append("MISSING_MEASUREMENT: %s has no pageHeight" % path)
            continue
        inflow = [s for s in rec.get("sections", []) if s.get("inFlow") and isinstance(s.get("heightPx"), (int, float))]
        for s in rec.get("sections", []):
            sid, var, h = s.get("section"), s.get("variant") or None, s.get("heightPx")
            if not isinstance(h, (int, float)):
                errors.append("MISSING_MEASUREMENT: %s %s has a null height" % (path, sid))
                continue
            label = "%s %s%s%s" % (path, sid, "/" + var if var else "", "[%d]" % s["instance"] if isinstance(s.get("instance"), int) else "")
            if _is(sid, sections.get(sid), "HERO") and h > HERO_WARN_PX:
                i, e = wl_for(path, sid, "HERO_HEIGHT")
                if h > HERO_ERROR_PX:
                    if e is not None and e.get("maxHeightPx", 0) > h:
                        used[i] = True
                        warnings.append("HERO_HEIGHT %s: %dpx > %d (whitelisted: %s)" % (label, h, HERO_ERROR_PX, e.get("reviewedBy")))
                    else:
                        if e is not None:
                            used[i] = True
                            errors.append("WHITELIST HERO_HEIGHT %s: maxHeightPx %s is not above measured %dpx" % (label, e.get("maxHeightPx"), h))
                        errors.append("HERO_HEIGHT %s: %dpx > %dpx" % (label, h, HERO_ERROR_PX))
                else:
                    if e is not None:
                        used[i] = True
                    warnings.append("HERO_HEIGHT %s: %dpx > %dpx" % (label, h, HERO_WARN_PX))
            if not s.get("inFlow") or _is(sid, sections.get(sid), "SHELL") or len(inflow) < MIN_INFLOW_SECTIONS:
                continue
            share = h / float(page_h)
            if share > SHARE_WARN:
                i, e = wl_for(path, sid, "SECTION_SHARE")
                msg = "SECTION_SHARE %s: %dpx = %.1f%% of %dpx page" % (label, h, share * 100, page_h)
                if share > SHARE_ERROR:
                    if e is not None and e.get("maxHeightPx", 0) > h:
                        used[i] = True
                        warnings.append(msg + " > %d%% (whitelisted: %s)" % (SHARE_ERROR * 100, e.get("reviewedBy")))
                    else:
                        if e is not None:
                            used[i] = True
                            errors.append("WHITELIST SECTION_SHARE %s: maxHeightPx not above the measured value" % label)
                        errors.append(msg + " > %d%%" % (SHARE_ERROR * 100))
                else:
                    if e is not None:
                        used[i] = True
                    warnings.append(msg + " > %d%%" % (SHARE_WARN * 100))
        if len(inflow) < MIN_INFLOW_SECTIONS:
            infos.append("%s: %d in-flow sections < %d, share check skipped" % (path, len(inflow), MIN_INFLOW_SECTIONS))

    for i, e in enumerate(entries):
        if not used[i]:
            errors.append("WHITELIST[%d] %s %s is STALE: no matching over-threshold measurement on %s" % (i, e.get("section"), e.get("rule"), e.get("route")))
    return errors, warnings, infos


def run(repo_root=REPO, whitelist=None, heights=None):
    sections = {}
    for p in sorted(glob.glob(os.path.join(repo_root, "sections", "*.json"))):
        with open(p, encoding="utf-8") as f:
            s = json.load(f)
        sections[s["id"]] = s
    tp = _jl(repo_root, "templates/templates.json")
    if heights is None:
        heights = _jl(repo_root, "extraction/measured-values.json").get("sectionHeights")
    if whitelist is None:
        wp = os.path.join(repo_root, WHITELIST_FILE)
        whitelist = _jl(repo_root, WHITELIST_FILE) if os.path.isfile(wp) else {"entries": []}
    return evaluate(heights, whitelist, sections, tp["templates"], tp["routeToTemplate"])


def self_test():
    H_ = {"id": "hero.a", "semantic": {"id": "hero.a", "category": "HERO"}}
    sections = {"hero.a": H_, "body.a": {"semantic": {"category": "CONTENT"}}, "body.b": {"semantic": {"category": "CONTENT"}},
                "shell.f": {"semantic": {"category": "SHELL"}}}
    templates = {"t": {"nodes": [{"section": "hero.a"}, {"section": "body.a"}, {"section": "body.b"}, {"section": "shell.f"}]}}
    routes = {"/p": "t"}

    def H(hero=500, a=500, b=500, f=300, vw=1440):
        secs = [dict(section="hero.a", heightPx=hero, inFlow=True), dict(section="body.a", heightPx=a, inFlow=True),
                dict(section="body.b", heightPx=b, inFlow=True), dict(section="shell.f", heightPx=f, inFlow=True)]
        return {"viewport": {"width": vw, "height": 900}, "routes": {"/p": {"template": "t", "pageHeight": hero + a + b + f, "sections": secs}}}

    def WL(**kw):
        return {"entries": [dict(dict(route="/p", section="body.a", rule="SECTION_SHARE", maxHeightPx=99999,
                                      justification="genuinely one continuous prose body, reviewed",
                                      reviewedBy="build agent (" + AGENT_ATTESTATION + ")"), **kw)]}
    results = []

    def case(name, heights, wl, want_err=None, want_warn=None, tpl=templates):
        e, w, _ = evaluate(heights, wl, sections, tpl, routes if tpl is templates else {k: v for k, v in [("/p", list(tpl)[0])]})
        ok = (any(want_err in x for x in e) if want_err else not e) and (any(want_warn in x for x in w) if want_warn else True)
        results.append(ok)
        print("%s %-62s errors=%d warnings=%d %s" % ("OK  " if ok else "FAIL", name, len(e), len(w), (e or w or [""])[0][:80]))

    case("control: balanced page passes", H(), None)
    case("HERO 1900px warns (no error)", H(hero=1900, a=1900, b=1900, f=300), None, want_warn="HERO_HEIGHT")
    case("HERO 3100px errors", H(hero=3100, a=3000, b=3000), None, want_err="HERO_HEIGHT")
    case("section at 65% of page errors", H(a=1300, hero=300, b=200, f=200), None, want_err="SECTION_SHARE")
    case("section at 55% of page warns only", H(a=1100, hero=400, b=300, f=200), None, want_warn="SECTION_SHARE")
    case("SHELL section at 70% is never flagged", H(f=2800, hero=400, a=400, b=400), None)
    two = {"viewport": {"width": 1440}, "routes": {"/p": {"template": "t3", "pageHeight": 1000, "sections": [
        dict(section="body.a", heightPx=900, inFlow=True), dict(section="body.b", heightPx=100, inFlow=True)]}}}
    case("page with < 3 in-flow sections skipped", two, None, tpl={"t3": {"nodes": [{"section": "body.a"}, {"section": "body.b"}]}})
    fixed = H(a=1300, hero=300, b=200, f=200)
    fixed["routes"]["/p"]["sections"][1]["inFlow"] = False
    case("fixed/sticky element takes no page height", fixed, None)
    case("whitelisted 65% section passes but still warns", H(a=1300, hero=300, b=200, f=200), WL(), want_warn="whitelisted")
    case("whitelist: justification < 30 chars rejected", H(a=1300, hero=300, b=200, f=200), WL(justification="short"), want_err="justification")
    case("whitelist: reviewedBy missing rejected", H(a=1300, hero=300, b=200, f=200), WL(reviewedBy=""), want_err="reviewedBy")
    case("whitelist: agent reviewer without attestation wording rejected", H(a=1300, hero=300, b=200, f=200), WL(reviewedBy="review agent"), want_err="agent attestation")
    case("whitelist: maxHeightPx <= measured rejected", H(a=1300, hero=300, b=200, f=200), WL(maxHeightPx=1300), want_err="SECTION_SHARE")
    case("whitelist: stale entry fails", H(), WL(), want_err="STALE")
    miss = H()
    miss["routes"]["/p"]["sections"].pop(1)
    case("missing measurement for a template node errors", miss, None, want_err="MISSING_MEASUREMENT")
    nul = H()
    nul["routes"]["/p"]["sections"][2]["heightPx"] = None
    case("null height errors", nul, None, want_err="MISSING_MEASUREMENT")
    case("route not measured errors", {"viewport": {"width": 1440}, "routes": {"/other": {"template": "t", "pageHeight": 1, "sections": []}}}, None, want_err="route /p")
    case("no sectionHeights at all errors", None, None, want_err="MISSING_MEASUREMENT")
    case("wrong viewport (1280) errors", H(vw=1280), None, want_err="WRONG_VIEWPORT")
    rt = {"r": {"nodes": [{"section": "body.a", "repeatable": True}, {"section": "shell.f"}]}}

    def R(*hs, f=300):
        secs = [dict(section="body.a", instance=i, heightPx=h, inFlow=True) for i, h in enumerate(hs)] + [dict(section="shell.f", heightPx=f, inFlow=True)]
        return {"viewport": {"width": 1440}, "routes": {"/p": {"template": "r", "pageHeight": sum(hs) + f, "sections": secs}}}
    case("repeatable: balanced instances pass", R(400, 400, 400, 400), None, tpl=rt)
    case("repeatable: one instance at 70% errors on its own", R(2800, 400, 400, 100), None, want_err="body.a[0]", tpl=rt)
    pins = (HERO_WARN_PX, HERO_ERROR_PX, SHARE_WARN, SHARE_ERROR, MIN_INFLOW_SECTIONS, REQUIRED_VIEWPORT) == (1800, 3000, 0.50, 0.60, 3, 1440)
    results.append(pins)
    print("%s thresholds pinned in code (1800/3000px, 50%%/60%%, min 3 in-flow, 1440px)" % ("OK  " if pins else "FAIL"))
    print("\nwrapper_gate self-test: %d/%d cases OK" % (sum(results), len(results)))
    return 0 if all(results) else 1


def main(argv):
    if "--self-test" in argv:
        return self_test()
    errors, warnings, infos = run(REPO)
    for x in infos:
        print("INFO ", x)
    for x in warnings:
        print("WARN ", x)
    for x in errors:
        print("ERROR", x)
    print("wrapper gate: %d error(s), %d warning(s)" % (len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
