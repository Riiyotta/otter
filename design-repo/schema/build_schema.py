#!/usr/bin/env python3
"""Regenerate the GENERATED parts of schema/pagespec.schema.json from the contracts they describe.

    python3 schema/build_schema.py            # --check (default): exit 1 if the schema drifted
    python3 schema/build_schema.py --write

Generated here (everything else in the schema file is hand-written and left untouched):
  * nodes.items.allOf        one if/then content branch per section contract (sections/*.json `content`);
                             media fields (allowedRoles) expand to a oneOf of closed role shapes, grouped by the
                             role's refPattern (assets/asset-roles.json)
  * nodes.items.properties.section.enum, properties.template.enum
  * properties.tokens        the closed token-slot object (tokens/llm/token-policy.json pageSpecTokenSlots)
  * x-counts, x-assetRoleEnum, x-pinnedAssetPolicies, x-pinnedAvailability
verify_all.py runs the --check, so a contract cannot change without the schema following (and vice versa).
"""
import copy, glob, json, os, sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(HERE, "pagespec.schema.json")
LOCAL_DESC = "A LOCAL repository path. An absolute http(s) URL is forbidden (NO_EXTERNAL_ASSET_REQUESTS)."
REF_DESC = {
    "^placeholder/": "A placeholder/ reference (no source asset). Generation-safe.",
    "^generated/": "A generated/ reference: newly generated original art (no source asset). Generation-safe.",
    "^operator/": "An operator/ reference the deployer resolves to an asset they supply and license. Generation-safe.",
}


def jl(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as f:
        return json.load(f)


def role_branches(allowed, roles):
    groups = []  # [(refPattern or None, [roles])]
    for r in allowed:
        pat = roles[r].get("refPattern")
        if r == "decorative.none" or pat is None:
            groups.append((None, [r]))
            continue
        g = next((g for g in groups if g[0] == pat), None)
        if g is None:
            groups.append((pat, [r]))
        else:
            g[1].append(r)
    out = []
    for pat, rs in groups:
        if pat is None:
            out.append({"type": "object", "additionalProperties": False, "properties": {"assetRole": {"const": rs[0]}}, "required": ["assetRole"]})
            continue
        desc = LOCAL_DESC if pat.startswith("^(public/") else next(v for k, v in REF_DESC.items() if pat.startswith(k))
        out.append({"type": "object", "additionalProperties": False,
                    "properties": {"assetRole": {"enum": rs}, "assetRef": {"type": "string", "pattern": pat, "description": desc}},
                    "required": ["assetRole", "assetRef"]})
    return out


def conv(o, roles):
    if isinstance(o, dict):
        if "allowedRoles" in o:
            out = {"oneOf": role_branches(o["allowedRoles"], roles), "x-allowedRoles": list(o["allowedRoles"]),
                   "x-assetRoleEnum": "assets/asset-roles.json#/roles (closed)"}
            for k, v in o.items():
                if k not in ("type", "assetRoleEnumRef", "allowedRoles"):
                    out["description" if k == "note" else k] = v
            return out
        return {k: conv(v, roles) for k, v in o.items()}
    if isinstance(o, list):
        return [conv(x, roles) for x in o]
    return o


def build(current):
    s = copy.deepcopy(current)
    reg = jl("assets/asset-roles.json")
    roles = reg["roles"]
    sections = [jl(os.path.relpath(p, REPO)) for p in sorted(glob.glob(os.path.join(REPO, "sections", "*.json")))]
    templates = jl("templates/templates.json")["templates"]
    policy = jl("tokens/llm/token-policy.json")
    branches = []
    for d in sections:
        then = {"properties": {"content": conv(d["content"], roles)}}
        if d["variants"] != ["default"]:
            then["properties"]["variant"] = {"enum": d["variants"]}
        branches.append({"if": {"properties": {"section": {"const": d["id"]}}, "required": ["section"]}, "then": then})
    items = s["properties"]["nodes"]["items"]
    items["allOf"] = branches
    items["properties"]["section"]["enum"] = [d["id"] for d in sections]
    items["properties"]["section"]["description"] = "Closed enum of the %d real section types." % len(sections)
    s["properties"]["template"]["enum"] = sorted(templates)
    slots = {k: v for k, v in policy["pageSpecTokenSlots"].items() if not k.startswith("$")}
    s["properties"]["tokens"] = {
        "type": "object", "additionalProperties": False,
        "description": "Page-level design tokens, each a catalog path from tokens/llm/token-catalog.json. Closed set of slots = tokens/llm/token-policy.json pageSpecTokenSlots (GENERATED from it by schema/build_schema.py). Whether a path is a real, approved, slot-appropriate, theme-valid token is checked by schema/semantic_validate.py (TOKEN_* rules); a raw colour, length or font name is rejected there.",
        "properties": {k: {"type": "string", "minLength": 1, "maxLength": 80, "description": v["purpose"]} for k, v in slots.items()},
        "required": [k for k, v in slots.items() if v.get("required")],
    }
    s["x-counts"] = {"templates": len(templates), "sections": len(sections), "assetRoles": len(roles),
                     "motionPatterns": len(items["properties"]["motion"]["properties"]["pattern"]["enum"]),
                     "contentBranches": len(branches), "tokenSlots": len(slots)}
    s["x-assetRoleEnum"] = sorted(roles)
    s["x-pinnedAssetPolicies"] = reg["pinnedPolicies"]
    s["x-pinnedAvailability"] = reg["pinnedAvailability"]
    return s


def render(s):
    return json.dumps(s, indent=2) + "\n"


def main(argv):
    with open(OUT, encoding="utf-8") as f:
        current = json.load(f)
    text = render(build(current))
    if "--write" in argv:
        with open(OUT, "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote schema/pagespec.schema.json")
        return 0
    ok = open(OUT, encoding="utf-8").read() == text
    print("schema up to date (generated parts rebuilt from the contracts)" if ok else "DRIFT: schema/pagespec.schema.json differs from a rebuild from sections/, assets/, templates/ and token-policy.json")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
