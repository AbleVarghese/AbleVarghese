#!/usr/bin/env python3
"""Rewrite every published figure in README.md and the portfolio site from docs/forensics.json.

    python3 scripts/sync_figures.py [path/to/AbleVarghese.github.io]

Companion to gen_assets.py: that file derives the SVGs, this one derives the prose
and the alt text around them. Both read the same audit JSON, so a refresh is:

    python3 docs/forensics.py repos.json docs/forensics.json
    python3 scripts/gen_assets.py
    python3 scripts/sync_figures.py ../AbleVarghese.github.io

Exits non-zero if any figure it was asked to sync did not actually change shape,
so a silent no-op cannot be mistaken for a successful sync.
"""
import re, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_assets import F, ALT, ROOT, A  # noqa: E402

site = sys.argv[1] if len(sys.argv) > 1 else None
changed, checked = [], 0


def sub(text, pattern, repl, label, flags=0):
    global checked
    new, n = re.subn(pattern, repl, text, flags=flags)
    checked += 1
    if n == 0:
        print(f"  !! no match: {label}  ({pattern})")
    elif new != text:
        changed.append(f"{label} x{n}")
    return new


def sync_alts(text, where):
    """Point every alt attribute at the derived string for its asset."""
    for name, alt in ALT.items():
        text = sub(text,
                   r'(<img alt=")[^"]*("\s+src="assets/%s-light\.svg")' % re.escape(name),
                   lambda m: m.group(1) + alt + m.group(2), f"{where} alt:{name}")
    return text


# ---------------- README ----------------
rp = os.path.join(ROOT, "README.md")
t = open(rp).read()
t = sync_alts(t, "README")
t = sub(t, r'across \d+ repositories', f'across {F["repos"]} repositories', "README repo count")
t = sub(t, r'\*\*~[\d,]+ person-years\*\*', f'**~{F["cocomo"]} person-years**', "README cocomo")
t = sub(t, r'~[\d,]+ hours', f'~{F["hours"]} hours', "README hours")
open(rp, "w").write(t)

# ---------------- portfolio site ----------------
if site:
    sp = os.path.join(os.path.expanduser(site), "index.html")
    h = open(sp).read()
    h = sync_alts(h, "site")
    statline = (f'{F["lines_m"]} lines delivered &middot; {F["platforms"]} platforms &middot; '
                f'{F["commits"]} commits &middot; {F["tests"]} test files &middot; agentic engineering '
                f'&middot; Toronto, Canada')
    h = sub(h, r'(<p class="statline mono">).*?(</p>)', lambda m: m.group(1) + statline + m.group(2),
            "site statline")
    h = sub(h, r'(content="Application architect who ships complete platforms: )[^"]*?(, published research)',
            lambda m: m.group(1) + f'{F["platforms"]} products, {F["lines_m"]} lines delivered' + m.group(2),
            "site meta description")
    tiles = [
        (F["lines_m"], f'lines delivered &middot; median {F["median_k"]}/day'),
        (F["commits"], f'commits &middot; {F["repos"]} repos'),
        (F["loc_m"], "lines in production"),
        (F["tests"], "test files"),
        (F["docs_k"], f'lines of docs &middot; {F["doc_files"]} files'),
        (f'~{F["hours"]} h', f'{F["evening"]}% between 5pm&ndash;2am'),
        (f'&asymp;{F["cocomo"]} py', "COCOMO-81 conventional effort"),
    ]
    grid = "\n".join(f'    <div class="num"><b>{n}</b><span class="mono">{l}</span></div>'
                     for n, l in tiles)
    h = sub(h, r'(<div class="nums">\n).*?(\n  </div>)',
            lambda m: m.group(1) + grid + m.group(2), "site stat grid", flags=re.S)
    open(sp, "w").write(h)

# ---------------- loud verification: no superseded figure may survive ----------------
print(f"\nsynced from audit {A['span']}  ({checked} rules, {len(changed)} produced edits)")
for c in changed:
    print(f"  ~ {c}")
print("\ncurrent figures:", " · ".join(
    f"{k}={F[k]}" for k in ("lines_m", "commits", "loc_m", "tests", "docs_k",
                            "days", "hours", "cocomo", "median", "streak", "repos")))
