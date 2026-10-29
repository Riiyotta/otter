#!/usr/bin/env python3
"""Derive every section contract's closed `source` and `semantic` objects (BASELINE R7) from the real source.

    python3 extraction/build_section_provenance.py            # --check (default): exit 1 if any contract drifted
    python3 extraction/build_section_provenance.py --write    # rewrite sections/*.json source + semantic

`source` = what the DOM/component is, traceable: {id, tag, file, lines}. The line range is COMPUTED here by
locating the opening tag (the EXTRACTION RULES table below names the file, the opening-line regex, the
occurrence and the tag) and walking forward to its closing tag at the same indentation. Nothing about a line
number is typed by hand.

`semantic` = what the AI sees: {id, category}. semantic.id always equals the contract id; source.id never does.
The category comes from the closed SEMANTIC_CATEGORY table below (a taxonomy decision, recorded here once);
wrapper/class naming never decides it.

The source project is the PARENT of design-repo/ (derived from __file__) unless --source is given. When it is
absent the script prints a WARNING and exits 0 (verify_all then only checks shape, not ranges).
"""
import argparse, glob, json, os, re, sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

SEMANTIC_CATEGORIES = ["HERO", "SHELL", "CTA", "FEATURES", "CONTENT", "EDITORIAL", "SOCIAL_PROOF", "TRUST", "FAQ",
                       "FORM", "LEGAL", "STATS", "AUTH", "UTILITY"]

# section id -> (file under the source root, opening-line regex, occurrence (1-based), tag)
EXTRACTION_RULES = {
    "chrome.navbar": ("src/components/Nav.jsx", r"^\s*<nav className=", 1, "nav"),
    "chrome.footer": ("src/components/Footer.jsx", r'^\s*<footer className="section cc-footer">', 1, "footer"),
    "hero.dark-rounded": ("src/components/Hero.jsx", r'^\s*<header className="section u-pt-0 u-pb-2">', 1, "header"),
    "banner.beta-card": ("src/components/BetaBanner.jsx", r'^\s*<header className="section hp-banner">', 1, "header"),
    "process.numbered-cards": ("src/components/HowItWorks.jsx", r'^\s*<section className="section how-it-works">', 1, "section"),
    "conversion.join-card": ("src/components/HowItWorks.jsx", r'^\s*<div className="col col-lg-12">', 1, "div"),
    "trust.press-bar": ("src/components/TrustBar.jsx", r'^\s*<section className="section">', 1, "section"),
    "hero.light-split": ("src/components/pst/PageHero.jsx", r'^\s*<header className="section">', 1, "header"),
    "disclosure.tabs-accordion": ("src/pages/Parents.jsx", r'^\s*<section className="section">', 1, "section"),
    "conversion.cta-card": ("src/pages/Parents.jsx", r'^\s*<section className="section u-p-0 u-mb-3">', 1, "section"),
    "testimonials.slider-empty": ("src/components/pst/TestimonialsSlider.jsx", r'^\s*<section className="section">', 1, "section"),
    "faq.common-questions-empty": ("src/components/pst/CommonQuestions.jsx", r'^\s*<section className="section">', 1, "section"),
    "trust.video-and-cards": ("src/pages/TrustSafety.jsx", r'^\s*<section className="section">', 1, "section"),
    "faq.category-empty": ("src/pages/Faq.jsx", r'^\s*<section className="section">', 1, "section"),
    "form.contact": ("src/pages/Contact.jsx", r'^\s*<section className="section">', 1, "section"),
    "content.image-copy-split": ("src/pages/Careers.jsx", r'^\s*<section className="section">', 1, "section"),
    "stats.grid": ("src/pages/Careers.jsx", r'^\s*<section className="section">', 2, "section"),
    "values.principle-cards": ("src/pages/Careers.jsx", r'^\s*<section className="section">', 3, "section"),
    "benefits.card-grid": ("src/pages/Careers.jsx", r'^\s*<section className="section">', 4, "section"),
    "jobs.listing-rows": ("src/pages/Careers.jsx", r'^\s*<section id="jobs" className="section">', 1, "section"),
    "blog.post-grid": ("src/pages/Blog.jsx", r'^\s*<section className="section">', 1, "section"),
    "conversion.cta-band": ("src/components/blog/CtaBand.jsx", r'^\s*<div className="section">', 1, "div"),
    "blog.post-header": ("src/pages/BlogPost.jsx", r'^\s*<div className="section u-pb-0">', 1, "div"),
    "content.rich-text-body": ("src/pages/BlogPost.jsx", r'^\s*<div className="section">', 1, "div"),
    "blog.related-posts": ("src/pages/BlogPost.jsx", r'^\s*<div className="section">', 2, "div"),
    "legal.document-header": ("src/components/legal/LegalDocument.jsx", r'^\s*<div className="section u-pb-0">', 1, "div"),
    "legal.document-intro": ("src/components/legal/LegalDocument.jsx", r"^\s*<div>\s*$", 1, "div"),
    "legal.document-part": ("src/components/legal/LegalDocument.jsx", r"^\s*<div key=\{i\}>", 1, "div"),
    "auth.login-form": ("src/pages/LogIn.jsx", r"^\s*<AuthShell>", 1, "AuthShell"),
    "content.stub-notice": ("src/pages/NotFound.jsx", r'^\s*<main id="main" className="section">', 1, "main"),
}

SEMANTIC_CATEGORY = {
    "chrome.navbar": "SHELL", "chrome.footer": "SHELL",
    "hero.dark-rounded": "HERO", "hero.light-split": "HERO",
    "banner.beta-card": "CTA", "conversion.join-card": "CTA", "conversion.cta-card": "CTA", "conversion.cta-band": "CTA",
    "process.numbered-cards": "FEATURES", "disclosure.tabs-accordion": "FEATURES", "benefits.card-grid": "FEATURES",
    "trust.video-and-cards": "TRUST",
    "trust.press-bar": "SOCIAL_PROOF", "testimonials.slider-empty": "SOCIAL_PROOF",
    "faq.common-questions-empty": "FAQ", "faq.category-empty": "FAQ",
    "form.contact": "FORM",
    "content.image-copy-split": "CONTENT", "values.principle-cards": "CONTENT", "jobs.listing-rows": "CONTENT",
    "stats.grid": "STATS",
    "blog.post-grid": "EDITORIAL", "blog.post-header": "EDITORIAL", "content.rich-text-body": "EDITORIAL", "blog.related-posts": "EDITORIAL",
    "legal.document-header": "LEGAL", "legal.document-intro": "LEGAL", "legal.document-part": "LEGAL",
    "auth.login-form": "AUTH",
    "content.stub-notice": "UTILITY",
}


def locate(src, rule):
    """Return (lo, hi, source_id) for one rule, or raise ValueError with the reason."""
    rel, rx, occ, tag = rule
    path = os.path.join(src, rel)
    lines = open(path, encoding="utf-8").read().split("\n")
    hits = [i for i, ln in enumerate(lines) if re.search(rx, ln)]
    if len(hits) < occ:
        raise ValueError("%s: opening pattern %r occurs %d time(s), occurrence %d wanted" % (rel, rx, len(hits), occ))
    lo = hits[occ - 1]
    opening = lines[lo]
    if "<" + tag not in opening:
        raise ValueError("%s:%d does not open <%s>" % (rel, lo + 1, tag))
    indent = len(opening) - len(opening.lstrip())
    hi = None
    if opening.rstrip().endswith("/>"):
        hi = lo
    else:
        for j in range(lo + 1, len(lines)):
            ln = lines[j]
            if len(ln) - len(ln.lstrip()) == indent and ln.strip().startswith("</" + tag + ">"):
                hi = j
                break
    if hi is None:
        raise ValueError("%s:%d <%s> has no closing tag at the same indentation" % (rel, lo + 1, tag))
    cls = re.search(r'className="([^"]+)"', opening)
    ident = re.search(r'id="([^"]+)"', opening)
    sid = "%s:%s%s%s" % (os.path.basename(rel), tag, ("#" + ident.group(1)) if ident else "",
                          ("." + ".".join(cls.group(1).split())) if cls else "")
    if occ > 1:
        sid += "[%d]" % occ
    return lo + 1, hi + 1, sid


def build(src):
    out = {}
    located = {sid: locate(src, rule) for sid, rule in sorted(EXTRACTION_RULES.items())}
    ids = [v[2] for v in located.values()]
    for sid, rule in sorted(EXTRACTION_RULES.items()):
        lo, hi, source_id = located[sid]
        if ids.count(source_id) > 1:  # same tag+classes twice in one file: disambiguate by opening line
            source_id += "@L%d" % lo
        out[sid] = {
            "source": {"id": source_id, "tag": rule[3], "file": rule[0], "lines": "%d-%d" % (lo, hi)},
            "semantic": {"id": sid, "category": SEMANTIC_CATEGORY[sid]},
        }
    return out


def contracts():
    out = {}
    for p in sorted(glob.glob(os.path.join(REPO, "sections", "*.json"))):
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        out[d["id"]] = (p, d)
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=os.path.dirname(REPO))
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    secs = contracts()
    missing = sorted(set(secs) ^ set(EXTRACTION_RULES))
    if missing or set(SEMANTIC_CATEGORY) != set(EXTRACTION_RULES):
        print("FAIL: extraction rules and section contracts disagree: %s" % missing)
        return 1
    bad_cat = sorted(k for k, v in SEMANTIC_CATEGORY.items() if v not in SEMANTIC_CATEGORIES)
    if bad_cat:
        print("FAIL: categories outside the closed taxonomy: %s" % bad_cat)
        return 1
    if not os.path.isdir(os.path.join(a.source, "src")):
        print("WARNING: source tree absent; provenance not re-derived (checked-in source/semantic used)")
        return 0
    try:
        new = build(a.source)
    except ValueError as exc:
        print("FAIL: %s" % exc)
        return 1
    drift = []
    for sid, (path, d) in secs.items():
        if d.get("source") != new[sid]["source"] or d.get("semantic") != new[sid]["semantic"]:
            drift.append(sid)
            if a.write:
                d["source"] = new[sid]["source"]
                d["semantic"] = new[sid]["semantic"]
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(d, f, indent=2)
                    f.write("\n")
    if a.write:
        print("wrote source + semantic for %d contract(s) (%d changed)" % (len(secs), len(drift)))
        return 0
    if drift:
        print("DRIFT: %d contract(s) differ from a rebuild from the source: %s" % (len(drift), drift[:5]))
        return 1
    print("provenance up to date: %d contracts, source ranges re-derived from the real files" % len(secs))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
