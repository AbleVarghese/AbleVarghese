#!/usr/bin/env python3
"""Rewrite every published figure in README.md and the portfolio site from docs/forensics.json.

    python3 scripts/sync_figures.py [path/to/AbleVarghese.github.io]

Companion to gen_assets.py: that file derives the SVGs, this one derives the prose
and the alt text around them. Both read the same audit JSON, so a refresh is:

    python3 docs/forensics.py repos.json docs/forensics.json
    python3 scripts/gen_assets.py
    python3 scripts/sync_figures.py ../AbleVarghese.github.io

Exits non-zero if any rule finds NO target to rewrite, because a rule that
matches nothing is a rule that has silently stopped protecting its figure.
A run that matches everything and changes nothing is correct and exits zero.
"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_assets import F, ALT, ROOT, A  # noqa: E402

site = sys.argv[1] if len(sys.argv) > 1 else None
changed, checked, missing = [], 0, []


def sub(text, pattern, repl, label, flags=0):
    global checked
    new, n = re.subn(pattern, repl, text, flags=flags)
    checked += 1
    if n == 0:
        missing.append(label)
        print(f"  !! no match: {label}  ({pattern})")
    elif new != text:
        changed.append(f"{label} x{n}")
    return new


def sync_alts(text, where, skip=()):
    """Point every alt attribute at the derived string for its asset.

    `skip` names assets a surface legitimately does not display, so a missing
    match stays silent instead of raising a false alarm every run.
    """
    for name, alt in ALT.items():
        if name in skip:
            continue
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

# ---------------- METHODOLOGY.md method table + figure block ----------------
mp = os.path.join(ROOT, "docs/METHODOLOGY.md")
m = open(mp).read()

method = f"""| Metric | Method |
|---|---|
| Commits ({F["commits"]}) | `git log --all --format=%at\\|%ae\\|%an` across {F["repos"]} original (non-fork) repositories, {F["start_month"]} to {F["end_month"]} |
| Active days ({F["days"]}) | Distinct calendar dates among all commit timestamps |
| Hours (~{F["hours_lo"]} to ~{F["hours"]}) | Session clustering (the git-hours algorithm): commits 120 min apart or less form a session; the range is the sum of intra-session gaps plus a per-session start adjustment of 30 min (low) or 120 min (high). An estimate of orchestration wall-clock, labeled as such |
| Lines of code ({F["loc_m"]}) | `git ls-files` on the {F["loc_repos"]} locally-present repos, code extensions only, excluding dependencies, lockfiles, build output and vendored code. Includes SQL, config and styles, because it is *tracked, authored* code rather than business logic alone |
| Test files ({F["tests"]}) | Files matching test and spec naming conventions among counted code files |
| Docs ({F["doc_files"]} files / {F["docs_k"]} lines) | Markdown census, same exclusions |
| Night and evening share ({F["evening"]}%) | Commits with author-hour at or after 17:00, or before 02:00 |
| COCOMO ~{F["cocomo"]} person-years | COCOMO-81 organic model, PM = 2.4 x KLOC^1.05 on measured LOC. A model of *conventional hand-written* effort, cited precisely because agentic engineering breaks its assumptions |

**Honest boundaries:** hour figures are estimates from commit patterns, not timesheets. LOC is
measured on the {F["loc_repos"]} repos present locally; {F["commit_only"]} more are counted for commits only. Work predating
{F["start_month"]}, such as an earlier fintech prototype, sits outside these histories and is excluded.

**Pre-2023 career record:** the 5,000+ commits / 20+ projects / 1 to 37-member teams figure for
2014 to 2023 is the owner's stated career record, consistent with the LinkedIn history, and is not
part of the git-measured numbers above. Those repositories are corporate, private and contractually
confidential, so they cannot be published or independently audited here.

**Lines delivered per day ({F["lines_m"]} added):** `git log --all --numstat` across the locally audited
repos, additions summed per author-date, with dependency, lockfile and build paths excluded.
Additions exceed final LOC ({F["loc_m"]}) because code gets rewritten; both numbers are stated. Commit
dates lag the work they contain: multi-day efforts often land in one commit, so the {F["delivery"]} recorded
active delivery days are a lower bound on true working days, and single-day spikes are usually
batch landings. The daily chart uses a square-root scale, stated on the chart, so median days stay
visible next to the {F["peak_k"]} peak."""

m = sub(m, r'(<!-- method start -->\n).*?(<!-- method end -->)',
        lambda x: x.group(1) + method + "\n" + x.group(2), "METHODOLOGY method table", flags=re.S)
block = (f'**Current figures:** {F["commits"]} commits · {F["loc_m"]} lines in production · '
         f'{F["lines_m"]} lines delivered ·\n{F["tests"]} test files · {F["doc_files"]} docs '
         f'({F["docs_k"]} lines) · {F["days"]} active days · ~{F["hours"]} hours ·\n'
         f'median {F["median"]} lines per active day · longest streak {F["streak"]} days · '
         f'COCOMO-81 ~{F["cocomo"]} person-years.')
m = sub(m, r'(<!-- figures start -->\n).*?(<!-- figures end -->)',
        lambda x: x.group(1) + block + "\n" + x.group(2), "METHODOLOGY figures", flags=re.S)
open(mp, "w").write(m)

# ---------------- portfolio site ----------------
if site:
    sp = os.path.join(os.path.expanduser(site), "index.html")
    h = open(sp).read()
    h = sync_alts(h, "site", skip=("banner",))  # the site header is HTML type, not the banner image
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

if missing:
    print(f"\nFAILED: {len(missing)} rule(s) matched nothing, so their figure is now unguarded:")
    for lbl in missing:
        print(f"  - {lbl}")
    sys.exit(1)
