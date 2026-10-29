#!/usr/bin/env python3
"""Derive the generation-mode leakage registry (schema/source-identity.json) from the REAL source.

    python3 extraction/build_source_identity.py            # --check (default): rebuild in memory, exit 1 on drift
    python3 extraction/build_source_identity.py --write    # rewrite schema/source-identity.json
    python3 extraction/build_source_identity.py --source <project root>

The source project is the PARENT of design-repo/ (derived from __file__) unless --source is given. When it is
absent the script prints a WARNING and exits 0, leaving the checked-in registry untouched (the semantic
validator only needs the checked-in file, so the design-repo stays usable on its own).

Every term carries file:line evidence harvested here; nothing is typed in by hand except the EXTRACTION RULES
below (which file / which attribute to read). Categories (each maps to one GENERATION_MODE_* rule):
  BRAND      the product name in index.html <title> (text before the bullet), every host / email / social handle
             that contains it, and the legal entity name in src/data/legal/*.js ("With Otter, Inc")
  CUSTOMER   the press marks on the press bar (src/components/TrustBar.jsx alt=), plus the alt with a trailing
             generic descriptor ("magazine") removed
  PERSON     photographer names in public/img/*-<id>-unsplash.* file names (real, identifiable people)
  URL        every http(s) host in src/, index.html, CLONE_SPEC.md, ASSETS.md, spec/*.md, except XML/JSON-LD
             namespace hosts and the RFC 2606 reserved example.com
  EMBED      the video embed id + hash constants in src/components/pst/VideoFacade.jsx and the embed hosts
  CLAIM      the stat claims in src/pages/Careers.jsx STATS (figure + claim sentence)
  ASSET      every file name under public/img and public/fonts (photos, logos, illustrations, fonts)
  SCREENSHOT the subset of ASSET whose name is a screen capture (screen-shot / screenshot)
  COPY       sha256[:16] of every normalised 5-word shingle of the site copy: JSX text and string literals of
             >= 5 words in src/components, src/pages and src/data (blog titles, legal documents)
Normalisation is schema/textnorm.py (shared with the validator). Detection is string-based, see that file.
"""
import argparse, glob, json, os, re, sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "schema"))
import textnorm as tn  # noqa: E402

OUT = os.path.join(REPO, "schema", "source-identity.json")
EXCLUDED_HOSTS = {"www.w3.org", "schema.org", "example.com"}  # namespaces / RFC 2606 reserved: not source identity
DESCRIPTORS = ("magazine", "logo")
HOST_RE = r"https?://([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)"


def rel(src, p):
    return os.path.relpath(p, src).replace(os.sep, "/")


def lines(p):
    return open(p, encoding="utf-8", errors="replace").read().split("\n")


def find_all(src, files, regex, group=1):
    rx = re.compile(regex)
    for f in files:
        for i, ln in enumerate(lines(f), 1):
            for m in rx.finditer(ln):
                yield m.group(group), "%s:%d" % (rel(src, f), i)


def add(store, term, ev):
    k = term.strip()
    if not k:
        return
    e = store.setdefault(k, [])
    if ev not in e and len(e) < 3:
        e.append(ev)


def as_list(store, category):
    return [{"term": t, "category": category, "tokens": tn.tokens(t), "evidence": ev}
            for t, ev in sorted(store.items(), key=lambda kv: kv[0].lower()) if tn.tokens(t)]


def strip_comments(text):
    text = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    return re.sub(r"(^|[^:'\"`])//[^\n]*", r"\1", text)


def copy_strings(src):
    files = sorted(glob.glob(os.path.join(src, "src", "components", "**", "*.js*"), recursive=True)
                   + glob.glob(os.path.join(src, "src", "pages", "*.jsx"))
                   + glob.glob(os.path.join(src, "src", "data", "**", "*.js"), recursive=True))
    out = []
    for f in files:
        t = strip_comments(open(f, encoding="utf-8").read())
        cands = re.findall(r"'((?:[^'\\\n]|\\.)*)'|\"((?:[^\"\\\n]|\\.)*)\"|`([^`]*)`", t)
        cands = [a or b or c for a, b, c in cands]
        cands += re.findall(r">([^<>{}]+)<", t)  # JSX text
        for s in cands:
            s = re.sub(r"\$\{[^}]*\}", " ", s)
            words = s.split()
            if len(words) < 5 or re.search(r"[={};]|=>|\bclassName\b", s):
                continue
            if sum(1 for w in words if re.match(r"^[A-Za-z’'“”\",.!?:;()&$%0-9-]+$", w)) < 0.6 * len(words):
                continue
            out.append(s)
    return out


def build(src):
    code = sorted(glob.glob(os.path.join(src, "src", "**", "*.jsx"), recursive=True)
                  + glob.glob(os.path.join(src, "src", "**", "*.js"), recursive=True))
    docs = [os.path.join(src, "index.html")] + [p for p in [os.path.join(src, "CLONE_SPEC.md"), os.path.join(src, "ASSETS.md")] if os.path.isfile(p)] \
        + sorted(glob.glob(os.path.join(src, "spec", "*.md")))

    title = next(find_all(src, [os.path.join(src, "index.html")], r"<title>([^<]+)</title>"))
    root = re.split(r"\s*[•|—-]\s*", title[0])[0].strip()
    brand = {}
    add(brand, root, title[1])
    for v, ev in find_all(src, code + docs, HOST_RE):
        if root.lower() in v.lower():
            add(brand, v.lower(), ev)
    for v, ev in find_all(src, code + docs, r"([A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[a-z]+)"):
        if root.lower() in v.lower():
            add(brand, v.lower(), ev)
    footer = [os.path.join(src, "src", "components", "Footer.jsx")]
    for v, ev in find_all(src, footer, r"href: 'https?://[^/']+/(?:company/)?([A-Za-z0-9_.-]+)/?'"):
        if root.lower() in v.lower():
            add(brand, v, ev)
    legal = sorted(glob.glob(os.path.join(src, "src", "data", "legal", "*.js")))
    for v, ev in find_all(src, legal, r"(With %s, Inc)" % re.escape(root)):
        add(brand, v, ev)

    customers = {}
    for v, ev in find_all(src, [os.path.join(src, "src", "components", "TrustBar.jsx")], r"alt: '([^']+)'"):
        add(customers, v, ev)
        words = v.split()
        if len(words) > 1 and words[-1].lower() in DESCRIPTORS:
            add(customers, " ".join(words[:-1]), ev)

    people = {}
    for f in sorted(glob.glob(os.path.join(src, "public", "img", "*"))):
        m = re.match(r"^([a-z]+(?:-[a-z]+)*)-[A-Za-z0-9_-]{11}-unsplash\.[a-z]+$", os.path.basename(f))
        if m:
            add(people, m.group(1).replace("-", " "), rel(src, f))

    hosts = {}
    for v, ev in find_all(src, code + docs, HOST_RE):
        h = v.lower()
        if h not in EXCLUDED_HOSTS:
            add(hosts, h, ev)

    embeds = {}
    vf = [os.path.join(src, "src", "components", "pst", "VideoFacade.jsx")]
    for v, ev in find_all(src, vf, r"const VIMEO_(?:ID|HASH) = '([^']+)'"):
        add(embeds, v, ev)
    for v, ev in find_all(src, vf, HOST_RE):
        add(embeds, v.lower(), ev)

    claims = {}
    careers = os.path.join(src, "src", "pages", "Careers.jsx")
    L = lines(careers)
    in_stats = False
    for i, ln in enumerate(L, 1):
        if ln.startswith("const STATS = ["):
            in_stats = True
            continue
        if in_stats and ln.startswith("]"):
            break
        if in_stats:
            for m in re.finditer(r"'(\d[\d.,]*%|\d[\d.,]* million)',\s*(['\"])((?:(?!\2).)+)\2", ln):
                add(claims, m.group(3), "%s:%d" % (rel(src, careers), i))
            m = re.match(r"\s*(['\"])((?:(?!\1).){20,})\1,?\s*$", ln)
            if m and re.match(r"\s*'(\d[\d.,]*%|\d[\d.,]* million)',", L[i - 2]):
                add(claims, m.group(2), "%s:%d" % (rel(src, careers), i))

    assets, shots = {}, {}
    for f in sorted(glob.glob(os.path.join(src, "public", "img", "*")) + glob.glob(os.path.join(src, "public", "fonts", "*"))):
        if os.path.isfile(f):
            b = os.path.basename(f)
            add(assets, b, rel(src, f))
            if re.search(r"screen-?shot", b, re.I):
                add(shots, b, rel(src, f))

    shingles = set()
    texts = copy_strings(src)
    for s in texts:
        shingles |= tn.shingle_hashes(s)

    return {
        "_note": "GENERATED by extraction/build_source_identity.py from the real source (do not hand-edit; verify_all.py re-derives it and fails on drift when the source tree is present). Used by schema/semantic_validate.py to reject source identity/content in mode:generation PageSpecs. Detection is string-based on schema/textnorm.py-normalised text; nobody has hand-reviewed these patterns.",
        "normalization": "NFKC; zero-width, soft hyphen and bidi controls removed; curly quotes -> straight; dash variants -> '-'; lower-case; apostrophes dropped; tokens [a-z0-9]+; terms match as contiguous token sequences",
        "brandRoot": root,
        "terms": as_list(brand, "BRAND") + as_list(customers, "CUSTOMER") + as_list(people, "PERSON") + as_list(hosts, "URL")
                 + as_list(embeds, "EMBED") + as_list(claims, "CLAIM"),
        "assetFiles": as_list(assets, "ASSET"),
        "screenshotFiles": as_list(shots, "SCREENSHOT"),
        "copy": {"shingleSize": tn.SHINGLE, "hash": "sha256 hex[:16] of the space-joined normalised tokens", "sourceStrings": len(texts), "hashes": sorted(shingles)},
    }


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=os.path.dirname(REPO))
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    if not (os.path.isdir(os.path.join(a.source, "src")) and os.path.isfile(os.path.join(a.source, "index.html"))):
        print("WARNING: source tree absent; schema/source-identity.json not re-derived (checked-in copy used)")
        return 0
    new = build(a.source)
    if a.write:
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(new, f, indent=1, ensure_ascii=False)
            f.write("\n")
        print("wrote schema/source-identity.json: %d terms, %d asset files, %d screenshots, %d copy shingles"
              % (len(new["terms"]), len(new["assetFiles"]), len(new["screenshotFiles"]), len(new["copy"]["hashes"])))
        return 0
    old = json.load(open(OUT, encoding="utf-8")) if os.path.isfile(OUT) else None
    if old != new:
        diff = [k for k in new if (old or {}).get(k) != new[k]]
        print("DRIFT: schema/source-identity.json differs from a rebuild from the source (keys: %s)" % diff)
        return 1
    print("source identity up to date: %d terms, %d asset files, %d copy shingles re-derived from the source"
          % (len(new["terms"]), len(new["assetFiles"]), len(new["copy"]["hashes"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
