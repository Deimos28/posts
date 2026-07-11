#!/usr/bin/env python3
"""Gating checks for essays that are ready to publish.

Only files named published.md are checked (and published). notes.md and draft.md
are working documents and never gate.

Checks (all gating):
  spell   - en_US plus shared/dictionary.txt whitelist
  urls    - GET with retry; fails only on connection error or 404/410
  style   - CLAUDE.md banned constructions (Kleppmann register)
Exit non-zero if any check fails. Emits GitHub Actions ::error:: annotations.
"""
import re, sys, pathlib, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGETS = sorted(ROOT.glob("essays/**/published.md"))

def annotate(file, line, msg):
    print(f"::error file={file},line={line}::{msg}")

def rel(p):
    return p.relative_to(ROOT)

# ---- spell -------------------------------------------------------------
def check_spell():
    import enchant
    d = enchant.Dict("en_US")
    wl = set()
    dic = ROOT / "shared/dictionary.txt"
    if dic.exists():
        wl = {w.strip().lower() for w in dic.read_text().split() if w.strip()}
    bad = []
    token = re.compile(r"[A-Za-z][A-Za-z'-]*")
    for f in TARGETS:
        for i, line in enumerate(f.read_text().splitlines(), 1):
            # skip fenced code and link URLs
            if line.strip().startswith("```"):
                continue
            line = re.sub(r"\]\([^)]*\)", "]()", line)   # drop link targets
            line = re.sub(r"`[^`]*`", "", line)          # drop inline code
            line = re.sub(r"https?://\S+", "", line)      # drop bare URLs
            for m in token.finditer(line):
                w = m.group(0)
                # check hyphenated compounds piece by piece
                parts = w.split("-")
                for part in parts:
                    if not part or part.lower() in wl or part.isupper():
                        continue
                    if not d.check(part) and not d.check(part.capitalize()):
                        bad.append((f, i, part))
    for f, i, w in bad:
        annotate(rel(f), i, f"Spell: unknown word '{w}' (add to shared/dictionary.txt if intended)")
    return not bad

# ---- urls --------------------------------------------------------------
def check_urls():
    import requests
    url_re = re.compile(r"https?://[^\s)\]>\"']+")
    seen, dead = {}, []
    hdr = {"User-Agent": "Mozilla/5.0 (essay-CI link check)"}
    for f in TARGETS:
        for i, line in enumerate(f.read_text().splitlines(), 1):
            for u in url_re.findall(line):
                u = u.rstrip(".,);:")
                key = u
                if key not in seen:
                    ok = True
                    for attempt in range(2):
                        try:
                            r = requests.get(u, headers=hdr, timeout=10,
                                             allow_redirects=True, stream=True)
                            r.close()
                            # only hard-fail on definitively-gone codes
                            ok = r.status_code not in (404, 410)
                            break
                        except requests.RequestException:
                            if attempt == 1:
                                ok = False
                            time.sleep(1)
                    seen[key] = ok
                if not seen[key]:
                    dead.append((f, i, u))
    for f, i, u in dead:
        annotate(rel(f), i, f"URL: unreachable or gone (404/410): {u}")
    return not dead

# ---- style (CLAUDE.md banned constructions) ----------------------------
BANNED = [
    (re.compile(r"\bnot\s+(?!only\b|just\b|merely\b)\w+[^.,;]{0,40}?,?\s+but\s+(?!also\b)\w+", re.I), "‘not X but Y’ construction"),
    (re.compile(r"^(you're right|exactly|absolutely|great question|good question)\b", re.I), "validating opener"),
    (re.compile(r"\b(that's the essay|the strongest|the best possible|nobody\b.{0,30}\btwice)\b", re.I), "superlative pronouncement"),
    (re.compile(r"^(and here's the thing|but notice|here's what)\b", re.I), "dramatic transition"),
]
def check_style():
    hits = []
    for f in TARGETS:
        for i, line in enumerate(f.read_text().splitlines(), 1):
            s = line.strip()
            for rx, label in BANNED:
                if rx.search(s):
                    hits.append((f, i, label, s[:60]))
    for f, i, label, snip in hits:
        annotate(rel(f), i, f"Style: {label} — “{snip}…”")
    return not hits

def main():
    if not TARGETS:
        print("No published.md files to check; nothing to gate.")
        return 0
    print(f"Checking {len(TARGETS)} published essay(s):")
    for f in TARGETS:
        print(f"  - {rel(f)}")
    results = {
        "spell": check_spell(),
        "urls":  check_urls(),
        "style": check_style(),
    }
    print("\nResults:")
    for k, v in results.items():
        print(f"  {k:6} {'PASS' if v else 'FAIL'}")
    return 0 if all(results.values()) else 1

if __name__ == "__main__":
    sys.exit(main())
