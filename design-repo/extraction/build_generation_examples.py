#!/usr/bin/env python3
"""Build the generation-safe example PageSpecs (BASELINE R4): one mode:"generation" example per template family.

    python3 extraction/build_generation_examples.py            # --check (default): exit 1 if an example drifted
    python3 extraction/build_generation_examples.py --write    # rewrite schema/examples/generated.*.pagespec.json

Each example starts from the generic per-template control synthesiser (schema/tests/adversarial_test.py
synth_control, built from the template's own node list and each section's content contract), then:
  * switches mode to "generation" and adds generationContext for a FICTIONAL brand ("Kettlewood", a home-companion
    care marketplace invented for these examples; every URL on the reserved kettlewood.example domain);
  * replaces every clone-only / blocked asset role with its generation-safe substitute (assets/asset-roles.json
    generationSafeSubstitutes) and a generated/ or placeholder/ reference;
  * fills every text field with ORIGINAL copy from the COPY table below (written for these examples; no source copy).
The result must pass Draft-07 + schema/semantic_validate.py with zero errors; verify_all.py re-validates them and
the adversarial suite uses them as the generation-mode controls.
"""
import copy, json, os, re, sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "schema"))
sys.path.insert(0, os.path.join(REPO, "schema", "tests"))
import adversarial_test as at  # noqa: E402

OUT_DIR = os.path.join(REPO, "schema", "examples")
SITE = "https://kettlewood.example"
CONTEXT = {
    "brandName": "Kettlewood",
    "brandMark": {"assetRole": "placeholder.brandMark", "assetRef": "placeholder/kettlewood-mark.svg"},
    "siteUrl": SITE,
    "appUrl": "https://app.kettlewood.example",
    "socialLinks": [{"label": "Newsletter", "href": SITE + "/newsletter"}, {"label": "Community", "href": SITE + "/community"}],
}
# family -> template (one generation example per template family; trust-safety added to exercise the embed rule)
EXAMPLES = {"landing": "home", "company": "careers", "editorial": "blog-post", "legal": "legal-prose",
            "auth": "auth-login", "utility": "not-found", "landing-trust": "trust-safety"}
SAFE = {"photo.person": "person.fictional", "illustration.brand": "illustration.generated",
        "illustration.editorial": "illustration.generated", "icon.feature": "illustration.generated",
        "icon.values": "illustration.generated", "editorial.cover": "illustration.generated",
        "media.videoPoster": "screenshot.placeholder", "auth.illustration": "illustration.generated"}
PREFIX = {"person.fictional": "generated/person-%d.webp", "illustration.generated": "generated/art-%d.svg",
          "screenshot.placeholder": "placeholder/poster-%d.webp"}

COPY = {
    "home": {
        "nodes[1].content.heading": "Companions for the people you love",
        "nodes[1].content.lede": "Kettlewood pairs families with vetted companions for everyday visits and errands.",
        "nodes[1].content.cta.label": "Find a companion",
        "nodes[2].content.eyebrow": "Now in early access",
        "nodes[2].content.heading": "Kettlewood is opening in three new towns",
        "nodes[2].content.body": "Join the waitlist and we will tell you when visits open near you.",
        "nodes[2].content.cta.label": "Join the waitlist",
        "nodes[3].content.eyebrow": "the visit flow",
        "nodes[3].content.heading": "Three steps to a calmer week",
        "nodes[3].content.cards[0].heading": "Share your routine",
        "nodes[3].content.cards[0].body": "Tell us about the visits, errands and hobbies that matter.",
        "nodes[3].content.cards[1].heading": "Meet your companion",
        "nodes[3].content.cards[1].body": "We introduce a vetted companion who fits your schedule.",
        "nodes[3].content.cards[2].heading": "Settle in together",
        "nodes[3].content.cards[2].body": "Visits run on your calendar and billing stays simple.",
        "nodes[4].content.heading": "Become a Kettlewood companion",
        "nodes[4].content.body": "Flexible hours, friendly neighbours and fair pay every week.",
        "nodes[4].content.cta.label": "Apply today",
        "nodes[5].content.eyebrow": "Mentioned by",
    },
    "careers": {
        "nodes[1].content.heading": "Build calmer days with us",
        "nodes[1].content.ctas[0].label": "See open roles",
        "nodes[2].content.heading": "Why we started Kettlewood",
        "nodes[2].content.body": "Caring for an older relative should never mean doing it alone, so we built a team around it.",
        "nodes[3].content.heading": "The companionship gap",
        "nodes[3].content.stats[0].label": "Fictional sample figure for layout only",
        "nodes[3].content.stats[1].label": "A second illustrative sample figure",
        "nodes[3].content.stats[2].label": "A third illustrative sample figure",
        "nodes[5].content.eyebrow": "Perks",
        "nodes[5].content.heading": "Benefits that travel with you",
        "nodes[5].content.lede": "Every Kettlewood teammate gets the same core package from day one.",
        "nodes[6].content.heading": "How we think about pay",
        "nodes[6].content.stats[0].label": "Transparent salary bands",
        "nodes[6].content.stats[1].label": "Annual review cycle",
        "nodes[6].content.stats[2].label": "Equal starting ranges",
        "nodes[7].content.eyebrow": "Open roles",
        "nodes[7].content.heading": "Join the team",
        "nodes[7].content.lede": "Roles below are examples for a fictional company.",
        "nodes[7].content.rows[0].title": "Companion Success Lead",
        "nodes[7].content.rows[0].location": "Remote",
    },
    "trust-safety": {
        "nodes[1].content.heading": "Safety at every visit",
        "nodes[1].content.ctas[0].label": "Find a companion",
        "nodes[2].content.heading": "How Kettlewood keeps visits safe",
        "nodes[2].content.lede": "Every companion completes identity checks, reference calls and a practical orientation before a first visit.",
        "nodes[2].content.video.title": "A short tour of our checks",
    },
    "blog-post": {
        "nodes[1].content.title": "Planning a gentle weekly routine",
        "nodes[1].content.tags[0].name": "Routines",
        "nodes[2].content.blocks[0].text": "Small rituals help a week feel steady.",
    },
    "legal-prose": {
        "nodes[1].content.title": "Terms of service",
    },
    "auth-login": {
        "nodes[0].content.title": "Sign in to Kettlewood",
    },
    "not-found": {
        "nodes[1].content.text": "This page is still being written.",
    },
}
ROW_COPY = {
    "values": ["Lead with kindness", "Keep promises small", "Listen first", "Leave things better"],
    "benefit_heading": ["Health cover", "Paid leave", "Learning budget", "Home office kit", "Retirement match", "Wellbeing days"],
    "benefit_body": "A fictional benefit described for this example page only.",
    "card_heading": ["Identity checks", "Reference calls", "Orientation", "Visit check-ins"],
    "card_body": "A fictional safety step written for this example page.",
    "related": ["Gentle stretches for mornings", "Making a shared calendar", "Questions for a first visit"],
}


def setp(obj, path, value):
    parts = re.findall(r"[^.\[\]]+|\[\d+\]", path)
    cur = obj
    for p in parts[:-1]:
        cur = cur[int(p[1:-1])] if p.startswith("[") else cur[p]
    last = parts[-1]
    if last.startswith("["):
        cur[int(last[1:-1])] = value
    else:
        if last not in cur:
            raise KeyError(path)
        cur[last] = value


def make(tid):
    spec = at.synth_control(tid)
    spec["mode"] = "generation"
    spec["generationContext"] = copy.deepcopy(CONTEXT)
    counter = [0]

    def fix(o):
        if isinstance(o, dict):
            role = o.get("assetRole")
            if role in SAFE:
                counter[0] += 1
                o["assetRole"] = SAFE[role]
                o["assetRef"] = PREFIX[SAFE[role]] % counter[0]
            if isinstance(o.get("href"), str) and o["href"].startswith("http"):
                o["href"] = SITE + "/start" if "greenhouse" not in o["href"] else "https://jobs.kettlewood.example/roles/%d" % (counter[0] + 1)
            for v in o.values():
                fix(v)
        elif isinstance(o, list):
            for v in o:
                fix(v)
    fix(spec["nodes"])
    for path, value in COPY.get(tid, {}).items():
        setp(spec, path, value)
    for n in spec["nodes"]:
        c = n["content"]
        if n["section"] == "values.principle-cards":
            for i, card in enumerate(c["cards"]):
                card["heading"] = ["What we value", "How we work"][i % 2]
                for j, item in enumerate(card["items"]):
                    item["label"] = ROW_COPY["values"][j % 4]
        if n["section"] == "benefits.card-grid":
            for i, card in enumerate(c["cards"]):
                card["heading"] = ROW_COPY["benefit_heading"][i % 6]
                card["body"] = ROW_COPY["benefit_body"]
        if n["section"] == "trust.video-and-cards":
            for i, card in enumerate(c["cards"]):
                card["heading"] = ROW_COPY["card_heading"][i % 4]
                card["body"] = ROW_COPY["card_body"]
        if n["section"] == "blog.related-posts":
            for i, post in enumerate(c["posts"]):
                post["slug"] = "sample-article-%d" % (i + 1)
                post["title"] = ROW_COPY["related"][i % 3]
                post["tags"][0]["name"] = "Routines"
        if n["section"].startswith("legal."):
            c["documentRef"] = "operator-supplied"
        if n["section"] == "hero.dark-rounded":
            fills = ["color.peach", "color.olive", "none", "color.celeste", "none"]
            for i, (stone, slot) in enumerate(zip(c["stones"], ["top-left", "middle-left", "bottom-left", "top-right", "bottom-right"])):
                stone["slot"], stone["fill"] = slot, fills[i]
                if fills[i] == "none":
                    stone["media"] = {"assetRole": "person.fictional", "assetRef": "generated/person-hero-%d.webp" % i}
    if tid == "legal-prose":
        part = next(n for n in spec["nodes"] if n["section"] == "legal.document-part")
        i = spec["nodes"].index(part)
        spec["nodes"][i:] = [dict(copy.deepcopy(part), content={"documentRef": "operator-supplied", "partIndex": k}) for k in (1, 2, 3)] + spec["nodes"][-1:]
        spec["nodes"] = [n for n in spec["nodes"] if not (n["section"] == "legal.document-part" and n["content"]["partIndex"] > 3)]
    if tid == "home":
        n = next(n for n in spec["nodes"] if n["section"] == "trust.press-bar")
        n["content"]["logoCount"] = 2
        spec["generationContext"]["pressLogos"] = [
            {"name": "Harbor Weekly", "assetRole": "logo.placeholder", "assetRef": "placeholder/press-harbor-weekly.svg"},
            {"name": "Morning Ledger", "assetRole": "logo.placeholder", "assetRef": "placeholder/press-morning-ledger.svg"}]
    if tid == "trust-safety":
        spec["generationContext"]["videoEmbedUrl"] = "https://video.kettlewood.example/embed/safety-tour"
    leftovers = [p for p, k, s in _strings(spec) if s == "placeholder" and k not in ("slug",)]
    if leftovers:
        raise SystemExit("example %s still has synthesised placeholder text at %s" % (tid, leftovers[:5]))
    return spec


def _strings(o, path="$", key=None):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _strings(v, "%s.%s" % (path, k), k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _strings(v, "%s[%d]" % (path, i), key)
    elif isinstance(o, str):
        yield path, key, o


def render(spec):
    return json.dumps(spec, indent=2, ensure_ascii=False) + "\n"


def main(argv):
    write = "--write" in argv
    os.makedirs(OUT_DIR, exist_ok=True)
    bad = 0
    for family, tid in EXAMPLES.items():
        rel = "schema/examples/generated.%s.pagespec.json" % tid
        text = render(make(tid))
        path = os.path.join(REPO, rel)
        if write:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            print("wrote %s (family %s)" % (rel, family))
        elif not os.path.isfile(path) or open(path, encoding="utf-8").read() != text:
            print("DRIFT: %s differs from a rebuild" % rel)
            bad += 1
    if not write:
        print("generation examples up to date (%d)" % len(EXAMPLES) if not bad else "generation examples: %d drifted" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
