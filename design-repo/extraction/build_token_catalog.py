#!/usr/bin/env python3
"""Generate tokens/llm/token-catalog.json from the REAL token files (BASELINE R10).

    python3 extraction/build_token_catalog.py            # --check (default): exit 1 if the catalog drifted
    python3 extraction/build_token_catalog.py --write    # rewrite tokens/llm/token-catalog.json

Every catalog entry is read out of tokens/{00-foundation,10-semantic,20-component,30-layout,themes}/*.json by
the EXTRACTION RULES in this file (which key of which file becomes which catalog path and category). No value
is typed in here: a value that is not in a token file cannot reach the catalog, and verify_all.py rebuilds the
catalog in memory and fails on any difference, so neither side can be edited alone.

Each entry: {category, value, source (file#key path), themeScope (marketing | auth | shared), generationApproved,
measuredFrom (when the token file records one)}. Themes: which semantic tokens each theme resolves, and to what.
"""
import argparse, json, os, re, sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TOK = os.path.join(REPO, "tokens")
OUT = os.path.join(TOK, "llm", "token-catalog.json")
VERSION = "1.0.0"

CATEGORIES = ["color", "colorLiteral", "semanticColor", "fontFamily", "fontWeight", "typography", "spacing", "radius",
              "layout", "breakpoint", "elevation", "motion", "component", "clipPath",
              "authColor", "authSpacing", "authRadius", "authTypography"]
# Measured literals are kept apart by the token file itself ("so nobody promotes them to brand tokens").
NOT_APPROVED_CATEGORIES = {"colorLiteral": "tokens/00-foundation/color.json keeps these measured literals OUT of the brand palette on purpose (\"so nobody promotes them to brand tokens\")."}


def jl(rel):
    with open(os.path.join(TOK, rel), encoding="utf-8") as f:
        return json.load(f)


def seg(key):
    """A token-file key as a catalog path segment: keep [A-Za-z0-9.-], collapse anything else to '-'."""
    return re.sub(r"[^A-Za-z0-9.]+", "-", key).strip("-")


def build():
    toks = {}

    def put(path, category, value, source, scope, measured=None):
        if path in toks:
            raise ValueError("duplicate catalog path %s" % path)
        if category not in CATEGORIES:
            raise ValueError("category %s not in CATEGORIES" % category)
        e = {"category": category, "value": value, "source": source, "themeScope": scope,
             "generationApproved": category not in NOT_APPROVED_CATEGORIES}
        if measured:
            e["measuredFrom"] = measured
        toks[path] = e

    c = jl("00-foundation/color.json")
    for k, v in c["tokens"].items():
        put(k, "color", v["$value"], "tokens/00-foundation/color.json#tokens/" + k, "marketing", v.get("measuredFrom"))
    for k, v in c["literals"].items():
        if isinstance(v, dict):
            put("color.literal." + k, "colorLiteral", v["$value"], "tokens/00-foundation/color.json#literals/" + k, "marketing", v.get("measuredFrom"))

    sem = jl("10-semantic/semantic.json")
    for k, v in sem["roles"].items():
        ref = v["ref"]
        put("semantic." + k, "semanticColor", "{%s}" % (ref if not ref.startswith("literals.") else "color.literal." + ref[len("literals."):]),
            "tokens/10-semantic/semantic.json#roles/" + k, "marketing")

    ty = jl("00-foundation/typography.json")
    for k, v in ty["families"].items():
        # The two families are shared with the auth app host (tokens/themes/auth-light.json sharedWithMarketing).
        put("typography." + k, "fontFamily", v["$value"], "tokens/00-foundation/typography.json#families/" + k, "shared", v.get("measuredFrom"))
    for k, v in ty["weightScale"].items():
        put("typography.weight." + k, "fontWeight", int(k), "tokens/00-foundation/typography.json#weightScale/" + k, "marketing")
    for k, v in ty["scale"].items():
        size = v.get("desktop") or v.get("all")
        put("typography.scale." + k, "typography", size, "tokens/00-foundation/typography.json#scale/" + k, "marketing", v.get("measuredFrom"))

    sp = jl("00-foundation/spacing.json")
    for k, v in sp["sectionRhythm"].items():
        put("spacing.section." + k, "spacing", v["paddingBlock"], "tokens/00-foundation/spacing.json#sectionRhythm/" + k, "marketing", v.get("measuredFrom"))
    put("spacing.gridGutter", "spacing", sp["gridGutter"]["$value"], "tokens/00-foundation/spacing.json#gridGutter", "marketing", sp["gridGutter"].get("measuredFrom"))
    for k, v in sp["utilities"].items():
        put("spacing.utility." + seg(k), "spacing", v["$value"], "tokens/00-foundation/spacing.json#utilities/" + k, "marketing")
    for k, v in sp["componentGaps"].items():
        put("spacing.gap." + k, "spacing", v["$value"], "tokens/00-foundation/spacing.json#componentGaps/" + k, "marketing", v.get("measuredFrom"))

    for k, v in jl("00-foundation/radius.json")["tokens"].items():
        put(k, "radius", v["$value"], "tokens/00-foundation/radius.json#tokens/" + k, "marketing", v.get("measuredFrom"))

    bp = jl("00-foundation/breakpoint.json")
    for k, v in bp["tokens"].items():
        put("breakpoint." + k[len("bp."):], "breakpoint", v["$value"], "tokens/00-foundation/breakpoint.json#tokens/" + k, "marketing")
    put("breakpoint.navIconMinWidth", "breakpoint", bp["theOneMinWidthQuery"]["$value"], "tokens/00-foundation/breakpoint.json#theOneMinWidthQuery", "marketing", bp["theOneMinWidthQuery"].get("measuredFrom"))

    for k, v in jl("00-foundation/elevation.json")["tokens"].items():
        put(k, "elevation", v["$value"], "tokens/00-foundation/elevation.json#tokens/" + k, "marketing", v.get("measuredFrom"))

    mo = jl("00-foundation/motion.json")
    for k, v in mo["easing"].items():
        put("motion." + k, "motion", v["$value"], "tokens/00-foundation/motion.json#easing/" + k, "marketing", v.get("measuredFrom"))
    for k, v in mo["duration"].items():
        put("motion." + k, "motion", v, "tokens/00-foundation/motion.json#duration/" + k, "marketing")
    for k, v in mo["delay"].items():
        put("motion." + k, "motion", v.split(" ")[0], "tokens/00-foundation/motion.json#delay/" + k, "marketing")
    for k, v in mo["patterns"].items():
        put("motion.pattern." + k, "motion", k, "tokens/00-foundation/motion.json#patterns/" + k, "marketing", v.get("measuredFrom"))

    lay = jl("30-layout/layout.json")
    base = lay["container"]["base"]
    put("layout.container.width", "layout", base["width"], "tokens/30-layout/layout.json#container/base/width", "marketing", base.get("measuredFrom"))
    put("layout.container.maxWidth", "layout", base["maxWidth"], "tokens/30-layout/layout.json#container/base/maxWidth", "marketing", base.get("measuredFrom"))
    for k, v in lay["container"]["variants"].items():
        put("layout.container." + seg(k), "layout", v, "tokens/30-layout/layout.json#container/variants/" + k, "marketing")
    put("layout.grid.columns", "layout", lay["grid"]["columns"], "tokens/30-layout/layout.json#grid/columns", "marketing", lay["grid"].get("measuredFrom"))

    comp = jl("20-component/component.json")
    for name, props in comp["overrides"].items():
        for p, v in props.items():
            put("component.%s.%s" % (seg(name), seg(p)), "component", v, "tokens/20-component/component.json#overrides/%s/%s" % (name, p), "marketing")

    clip = jl("00-foundation/clip-path.json")
    for cid in clip["ids"]:
        put("clipPath." + cid, "clipPath", "url(#%s)" % cid, "tokens/00-foundation/clip-path.json#ids", "marketing", clip.get("definedIn"))

    auth = jl("themes/auth-light.json")
    for k, v in auth["color"].items():
        put("auth.color." + k[len("auth."):], "authColor", v["$value"], "tokens/themes/auth-light.json#color/" + k, "auth", auth.get("measuredFrom"))
    for k, v in auth["spacing"].items():
        put("auth.spacing." + k[len("auth.space."):], "authSpacing", v, "tokens/themes/auth-light.json#spacing/" + k, "auth")
    for k, v in auth["radius"].items():
        put("auth.radius." + k[len("auth.radius."):], "authRadius", v, "tokens/themes/auth-light.json#radius/" + k, "auth")
    for k, v in auth["typography"]["roles"].items():
        put("auth.typography." + k[len("auth."):], "authTypography", v["size"], "tokens/themes/auth-light.json#typography/roles/" + k, "auth", auth["typography"].get("measuredFrom"))

    # themes: which semantic tokens each theme resolves, and to which foundation value
    mk = jl("themes/marketing-light.json")
    resolves = {}
    for k, ref in mk["resolves"].items():
        path = "semantic." + k
        target = ref if not ref.startswith("literals.") else "color.literal." + ref[len("literals."):]
        resolves[path] = {"ref": target, "value": toks[target]["value"] if target in toks else None}
    themes = {
        "marketing-light": {"file": "tokens/themes/marketing-light.json", "designSystem": mk["designSystem"], "tokenScopes": ["marketing", "shared"],
                            "semanticTokens": sorted(p for p in resolves if p in toks), "resolves": dict(sorted(resolves.items()))},
        # The auth theme file IS the auth token set: its colours resolve to themselves.
        "auth-light": {"file": "tokens/themes/auth-light.json", "designSystem": auth["designSystem"], "tokenScopes": ["auth", "shared"],
                       "semanticTokens": sorted(p for p in toks if p.startswith("auth.color.")),
                       "resolves": {p: {"ref": p, "value": toks[p]["value"]} for p in sorted(toks) if p.startswith("auth.color.")}},
    }
    counts = {}
    for t in toks.values():
        counts[t["category"]] = counts.get(t["category"], 0) + 1
    return {
        "version": VERSION,
        "$comment": "GENERATED by extraction/build_token_catalog.py from the real token files. Do not hand-edit: extraction/verify_all.py rebuilds it and fails on any difference. A PageSpec names tokens by these catalog paths (tokens/llm/token-policy.json pageSpecTokenSlots), never by raw values.",
        "counts": {"tokens": len(toks), "byCategory": dict(sorted(counts.items())), "themes": len(themes)},
        "categories": CATEGORIES,
        "notGenerationApprovedCategories": NOT_APPROVED_CATEGORIES,
        "themes": themes,
        "tokens": dict(sorted(toks.items())),
    }


def render(cat):
    return json.dumps(cat, indent=1, ensure_ascii=False) + "\n"


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    text = render(build())
    if a.write:
        with open(OUT, "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote tokens/llm/token-catalog.json")
        return 0
    ok = os.path.exists(OUT) and open(OUT, encoding="utf-8").read() == text
    print("token catalog up to date (rebuilt from the token files)" if ok else "DRIFT: tokens/llm/token-catalog.json differs from a rebuild from the token files")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
