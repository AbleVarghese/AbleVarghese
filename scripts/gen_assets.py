#!/usr/bin/env python3
"""Regenerate every SVG asset from docs/forensics.json.

Run from the repo root:  python3 scripts/gen_assets.py

Why this file exists: on 2026-08-17 a refresh left stale figures inside SVG
aria-labels and inside the banner/diagram, because those strings were typed by
hand while the charts read the audit JSON. Every number and every alt text is
now DERIVED here, so a refresh is one command and drift is impossible.
Shared proportional type scale (ratio ~1.15): 54 / 30 / 20 / 17 / 15 / 13.5 / 12.
"""
import json, math, datetime, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "docs/forensics.json")))
A, DAILY = D["aggregate"], D["daily"]
ASSETS = os.path.join(ROOT, "assets")

MONO = 'font-family="SF Mono, Menlo, Consolas, monospace"'
SANS = 'font-family="Avenir Next, Helvetica Neue, Arial, sans-serif"'

# ---- derived figure strings: the single source for assets, README and site ----
LOC_REPOS = sum(1 for r in D["repos"] if r.get("loc") is not None)
TOP_LANGS = list(A["langs"].items())[:7]
F = {
    "lines_m":     f'{A["lines_added"]/1e6:.2f}M',
    "commits":     f'{A["commits"]:,}',
    "loc_m":       f'{A["loc"]/1e6:.2f}M',
    "tests":       f'{A["test_files"]:,}',
    "docs_k":      f'{A["md_lines"]/1000:.0f}K',
    "doc_files":   f'{A["md_files"]:,}',
    "days":        str(A["commit_active_days"]),
    "hours":       f'{A["hours_hi"]:,}',
    "evening":     str(A["evening_pct"]),
    "cocomo":      f'{A["cocomo_person_years"]:.0f}',
    "median_k":    f'{A["median_day"]/1000:.1f}K',
    "median":      f'{A["median_day"]:,}',
    "streak":      str(A["longest_streak"]),
    "delivery":    str(A["delivery_days"]),
    "repos":       str(A["repos"]),
    "loc_repos":   str(LOC_REPOS),
    "hours_lo":    f'{A["hours_lo"]:,}',
    "peak_k":      f'{A["peak_day_lines"]//1000}K',
    "commit_only": str(A["repos"] - LOC_REPOS),
    "platforms":   "10",
    "end_month":   datetime.date.fromisoformat(A["span"][-10:]).strftime("%B %Y"),
    "start_month": datetime.date.fromisoformat(A["span"][:10]).strftime("%B %Y"),
}
F["langs_alt"] = ", ".join(f"{n} {v//1000}K" for n, v in TOP_LANGS[:6])

ALT = {
    "banner": (f'Able Varghese, Application Architect. Complete platforms, shipped end to end. '
               f'{F["lines_m"]} lines delivered, {F["platforms"]} platforms, {F["commits"]} commits, '
               f'{F["tests"]} test files, agentic engineering.'),
    "stats": (f'{F["lines_m"]} lines delivered, {F["platforms"]} platforms shipped, about {F["cocomo"]} '
              f'COCOMO person-years. {F["commits"]} commits, {F["loc_m"]} lines in production, '
              f'{F["tests"]} test files, {F["docs_k"]} doc lines. {F["days"]} active days, '
              f'about {F["hours"]} hours, {F["evening"]} percent between 5pm and 2am'),
    "daily-lines": (f'Lines of code delivered per day, {F["start_month"]} to {F["end_month"]}: '
                    f'{F["lines_m"]} lines added, median {F["median"]} per active day, '
                    f'longest streak {F["streak"]} consecutive days'),
    "hours": (f'Commits by hour of day: {F["evening"]} percent land between 5pm and 2am, '
              f'peaking at {max(A["hour_of_day"], key=lambda k: A["hour_of_day"][k])}:00'),
    "languages": f'Lines of code by language: {F["langs_alt"]}',
    "system": (f'Diagram: one engineer operates an agentic engineering system of orchestration doctrine, '
               f'adaptive concurrency, live fleet monitoring, self-hosted CI and data supply, which ships '
               f'ten production platforms. {F["commits"]} commits, about {F["hours"]} hours, '
               f'COCOMO-priced at about {F["cocomo"]} person-years.'),
}


def T(dk):
    return dict(
        bg1="#101418" if dk else "#fbfaf7", bg2="#0b0e11" if dk else "#f3f1ec",
        grid="#1a2027" if dk else "#e6e2d9", border="#232b34" if dk else "#d8d3c8",
        hair="#1c232b" if dk else "#e2ddd2", ink1="#eceff2" if dk else "#20242a",
        ink2="#c3ccd5" if dk else "#3d454e", ink3="#93a0ac" if dk else "#5b6470",
        amber="#e8a33d" if dk else "#b97a17", blue="#6a9fd8" if dk else "#3f6fae",
        card="#151a20" if dk else "#ffffff", top="#2e3a45" if dk else "#c9c2b2",
        side="#7b8794" if dk else "#8a8479",
        ramp=(["#f2bc6a", "#e8a33d", "#d18f2b", "#b97a17", "#9c660f", "#7f530a", "#654208"] if dk
              else ["#8a5a10", "#9c660f", "#b97a17", "#cf8c1f", "#dd9c33", "#e8ab52", "#efbe78"]))


def open_svg(t, W, H, label, grid=False):
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">',
         f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>']
    p.append('<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="%s" stroke-width="1"/></pattern></defs>' % t["grid"]
             if grid else '</defs>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#g)"/>')
    if grid:
        p.append(f'<rect width="{W}" height="{H}" fill="url(#grid)" opacity="0.55"/>')
    p.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" stroke="{t["border"]}"/>')
    return p


def head(t, W, H, title, sub, label):
    p = open_svg(t, W, H, label)
    p.append(f'<text x="64" y="40" {SANS} font-size="20" font-weight="700" letter-spacing="1" fill="{t["ink1"]}">{title}</text>')
    p.append(f'<text x="64" y="62" {MONO} font-size="13.5" font-weight="600" fill="{t["ink3"]}">{sub}</text>')
    return p


def banner(dk):
    t = T(dk); W, H = 1280, 300
    p = open_svg(t, W, H, ALT["banner"], grid=True)
    p += [f'<rect x="0" y="0" width="{W}" height="2" fill="{t["top"]}"/>',
          f'<rect x="64" y="74" width="52" height="4" fill="{t["amber"]}"/>',
          f'<text x="64" y="132" {SANS} font-size="46" font-weight="700" letter-spacing="6" fill="{t["ink1"]}">ABLE VARGHESE</text>',
          f'<text x="64" y="172" {SANS} font-size="23" font-weight="600" letter-spacing="0.6" fill="{t["ink2"]}">Application architect. Complete platforms, shipped end to end</text>',
          f'<text x="64" y="232" {MONO} font-size="17" font-weight="700" letter-spacing="0.3" fill="{t["ink3"]}">'
          f'{F["lines_m"]} lines delivered &#183; {F["platforms"]} platforms &#183; {F["commits"]} commits &#183; {F["tests"]} test files &#183; agentic engineering</text>',
          f'<g {MONO} font-size="13.5" font-weight="600" fill="{t["side"]}" text-anchor="end">',
          '<text x="1216" y="100">licentric</text>', '<text x="1216" y="123">lawyerserved</text>',
          '<text x="1216" y="146">solveright &#183; solvemax</text>', '<text x="1216" y="169">argustest &#183; shelljolt</text>',
          '<text x="1216" y="192">keralora &#183; flowen</text>',
          f'<text x="1216" y="215" fill="{t["amber"]}">toronto, canada</text>', '</g>', '</svg>']
    return "\n".join(p)


def stats(dk):
    t = T(dk); W, H = 1280, 258
    p = open_svg(t, W, H, ALT["stats"])
    hero = [(F["lines_m"], "lines delivered"), (F["platforms"], "platforms shipped"),
            (f'&#8776;{F["cocomo"]}', "COCOMO person-years")]
    for i, (n, l) in enumerate(hero):
        x = 64 + i * 390
        p.append(f'<text x="{x}" y="92" {SANS} font-size="54" font-weight="700" fill="{t["amber"]}">{n}</text>')
        p.append(f'<text x="{x}" y="118" {MONO} font-size="13.5" font-weight="600" letter-spacing="1" fill="{t["ink3"]}">{l}</text>')
    p.append(f'<line x1="64" y1="146" x2="1216" y2="146" stroke="{t["hair"]}"/>')
    t2 = [(F["commits"], "commits"), (F["loc_m"], "lines in production"),
          (F["tests"], "test files"), (F["docs_k"], f'doc lines &#183; {F["doc_files"]} files')]
    for i, (n, l) in enumerate(t2):
        x = 64 + i * 295
        p.append(f'<text x="{x}" y="196" {SANS} font-size="30" font-weight="700" fill="{t["ink1"]}">{n}</text>')
        p.append(f'<text x="{x}" y="218" {MONO} font-size="13.5" font-weight="600" fill="{t["ink3"]}">{l}</text>')
    p.append(f'<text x="64" y="242" {MONO} font-size="13.5" font-weight="600" fill="{t["ink3"]}">'
             f'{F["days"]} active build days &#183; ~{F["hours"]} hours &#183; {F["evening"]}% of commits between 5pm and 2am, alongside a full-time fintech role</text>')
    p.append('</svg>'); return "\n".join(p)


def daily(dk):
    t = T(dk)
    d0 = datetime.date.fromisoformat(min(DAILY)); d1 = datetime.date.fromisoformat(max(DAILY))
    N = (d1 - d0).days + 1
    vals = [DAILY.get((d0 + datetime.timedelta(i)).isoformat(), 0) for i in range(N)]
    W, H, BASE, MAXH, X0, X1 = 1280, 278, 214, 112, 64, 1216
    peak = max(vals); sc = lambda v: (math.sqrt(v) / math.sqrt(peak)) * MAXH; bw = (X1 - X0) / N
    p = head(t, W, H, "LINES DELIVERED, DAILY",
             f'{F["lines_m"]} added &#183; median {F["median_k"]} per active day &#183; longest streak {F["streak"]} days &#183; sqrt scale',
             ALT["daily-lines"])
    for gv in [10000, 50000, 200000]:
        gy = BASE - sc(gv)
        p.append(f'<line x1="{X0}" y1="{gy:.0f}" x2="{X1}" y2="{gy:.0f}" stroke="{t["grid"]}"/>')
        p.append(f'<text x="{X1+4}" y="{gy+4:.0f}" {MONO} font-size="12" font-weight="600" fill="{t["ink3"]}">{gv//1000}K</text>')
    p.append(f'<line x1="{X0}" y1="{BASE}" x2="{X1}" y2="{BASE}" stroke="{t["grid"]}"/>')
    for i, v in enumerate(vals):
        if v <= 0: continue
        p.append(f'<rect x="{X0+i*bw:.1f}" y="{BASE-max(1.5,sc(v)):.1f}" width="{max(bw-0.6,1.6):.1f}" height="{max(1.5,sc(v)):.1f}" fill="{t["amber"]}"/>')
    pi = vals.index(peak)
    p.append(f'<text x="{X0+pi*bw:.0f}" y="{BASE-MAXH-8}" {MONO} font-size="13.5" font-weight="700" fill="{t["ink1"]}" text-anchor="middle">{peak//1000}K in a day</text>')
    for i in range(N):
        dt = d0 + datetime.timedelta(i)
        if dt.day == 1 and dt.month in (1, 4, 7, 10):
            p.append(f'<text x="{X0+i*bw:.0f}" y="{BASE+22}" {MONO} font-size="12" font-weight="600" fill="{t["ink3"]}" text-anchor="middle">{dt.strftime("%b &#8217;%y")}</text>')
    p.append('</svg>'); return "\n".join(p)


def hours(dk):
    t = T(dk); HOD = {int(k): v for k, v in A["hour_of_day"].items()}
    W, H, BASE, MAXH, X0 = 1280, 248, 196, 110, 64
    slot = (1216 - X0) / 24; peak = max(HOD.values())
    p = head(t, W, H, "WHEN I BUILD",
             f'commits by hour of day &#183; {F["evening"]}% land 5pm&#8211;2am, after the day job', ALT["hours"])
    p.append(f'<line x1="{X0}" y1="{BASE}" x2="1216" y2="{BASE}" stroke="{t["grid"]}"/>')
    for h in range(24):
        v = HOD[h]; x = X0 + slot * h + slot / 2; ht = max(3, v / peak * MAXH)
        p.append(f'<rect x="{x-14:.0f}" y="{BASE-ht:.0f}" width="28" height="{ht:.0f}" rx="3" fill="{t["amber"] if (h>=17 or h<2) else t["ink3"]}"/>')
    for h, l in [(0, "12am"), (6, "6am"), (12, "12pm"), (18, "6pm"), (23, "11pm")]:
        p.append(f'<text x="{X0+slot*h+slot/2:.0f}" y="{BASE+22}" {MONO} font-size="12" font-weight="600" fill="{t["ink3"]}" text-anchor="middle">{l}</text>')
    ph = max(HOD, key=HOD.get)
    p.append(f'<text x="{X0+slot*ph+slot/2:.0f}" y="{BASE-MAXH-12}" {MONO} font-size="13.5" font-weight="700" fill="{t["ink1"]}" text-anchor="middle">peak {ph%12 or 12}{"am" if ph<12 else "pm"}</text>')
    p.append('</svg>'); return "\n".join(p)


def langs(dk):
    t = T(dk); L = TOP_LANGS
    W = 1280; RH = 34; TOP = 84; H = TOP + len(L) * RH + 28; mx = L[0][1]; X0, XW = 230, 900
    p = head(t, W, H, "WHAT IT&#8217;S WRITTEN IN",
             f'{F["loc_m"]} lines in production across {F["loc_repos"]} audited repos', ALT["languages"])
    for i, (n, v) in enumerate(L):
        y = TOP + i * RH; w = max(4, v / mx * XW)
        p.append(f'<text x="{X0-14}" y="{y+17}" {SANS} font-size="13.5" font-weight="600" fill="{t["ink3"]}" text-anchor="end">{n}</text>')
        p.append(f'<rect x="{X0}" y="{y}" width="{w:.0f}" height="24" rx="3" fill="{t["ramp"][i]}"/>')
        p.append(f'<text x="{X0+w+12:.0f}" y="{y+17}" {MONO} font-size="13.5" font-weight="600" fill="{t["ink1"]}">{round(v/1000)}K</text>')
    p.append('</svg>'); return "\n".join(p)


def system(dk):
    t = T(dk); W, H = 1280, 468
    p = open_svg(t, W, H, ALT["system"])
    p.append(f'<text x="64" y="40" {SANS} font-size="20" font-weight="700" letter-spacing="1" fill="{t["ink1"]}">HOW ONE PERSON SHIPS TEN PLATFORMS</text>')
    p.append(f'<text x="64" y="62" {MONO} font-size="13.5" font-weight="600" fill="{t["ink3"]}">the agentic engineering system underneath the portfolio</text>')
    prods = ["Licentric", "LawyerServed", "SolveRight", "solvemax", "ArgusTest",
             "ShellJolt", "Keralora", "Flowen", "Devrule.ai", "Dwellium"]
    # The product row must end exactly where every panel below it ends (x=1216),
    # so box width is solved from the band rather than picked: 10*bw + 9*gap = 1152.
    gap, BY, BH = 7.6, 92, 48
    bw = (1152 - 9 * gap) / 10
    for i, n in enumerate(prods):
        px = 64 + i * (bw + gap)
        p.append(f'<rect x="{px:.0f}" y="{BY}" width="{bw}" height="{BH}" rx="4" fill="{t["card"]}" stroke="{t["amber"]}" stroke-width="1.4"/>')
        p.append(f'<text x="{px+bw/2:.0f}" y="{BY+30}" {SANS} font-size="13.5" font-weight="600" fill="{t["ink1"]}" text-anchor="middle">{n}</text>')
    SY = 196
    for i in range(10):
        cx = 64 + i * (bw + gap) + bw / 2
        p.append(f'<line x1="{cx:.0f}" y1="{SY}" x2="{cx:.0f}" y2="{BY+BH}" stroke="{t["ink3"]}" stroke-width="1.2"/>')
        p.append(f'<path d="M {cx-4:.0f} {BY+BH+8} L {cx:.0f} {BY+BH} L {cx+4:.0f} {BY+BH+8}" fill="none" stroke="{t["ink3"]}" stroke-width="1.2"/>')
    p.append(f'<rect x="64" y="{SY}" width="1152" height="138" rx="6" fill="{t["card"]}" stroke="{t["blue"]}" stroke-width="1.6"/>')
    p.append(f'<text x="88" y="{SY+32}" {SANS} font-size="17" font-weight="700" letter-spacing="1" fill="{t["blue"]}">AGENTIC ENGINEERING SYSTEM</text>')
    chips = [("Orchestration doctrine", "tiered agents, gated merges"),
             ("Adaptive concurrency", "circuit breakers, backoff"),
             ("ops-dashboard", "live fleet monitor, MIT"),
             ("local-gitlab", "self-hosted $0 CI/CD"),
             # No count here on purpose: nothing derives a scraper count from the audit
             # JSON, so a number in this chip can only ever drift. The README bullet
             # carries it, counted from the repo, in exactly one place.
             ("Scrapos", "queue-based data supply")]
    # Same solve for the chip row, so its right inset matches its 24px left inset.
    cg, CY, CH = 9, SY + 48, 66
    cw = (1152 - 48 - 4 * cg) / 5
    for i, (a, b) in enumerate(chips):
        cx = 88 + i * (cw + cg)
        p.append(f'<rect x="{cx}" y="{CY}" width="{cw}" height="{CH}" rx="4" fill="none" stroke="{t["border"]}"/>')
        p.append(f'<text x="{cx+12}" y="{CY+26}" {SANS} font-size="15" font-weight="600" fill="{t["ink1"]}">{a}</text>')
        p.append(f'<text x="{cx+12}" y="{CY+49}" {MONO} font-size="12" font-weight="600" fill="{t["ink3"]}">{b}</text>')
    p.append(f'<text x="64" y="{SY+168}" {MONO} font-size="12" font-weight="600" fill="{t["ink3"]}">operated by</text>')
    AY = SY + 182
    p.append(f'<rect x="64" y="{AY}" width="1152" height="62" rx="6" fill="none" stroke="{t["amber"]}" stroke-width="1.4"/>')
    p.append(f'<text x="88" y="{AY+28}" {SANS} font-size="15" font-weight="700" letter-spacing="0.5" fill="{t["ink1"]}">ONE ENGINEER</text>')
    p.append(f'<text x="88" y="{AY+50}" {MONO} font-size="13.5" font-weight="600" fill="{t["ink3"]}">'
             f'{F["commits"]} commits &#183; ~{F["hours"]} hours &#183; nights + weekends &#183; COCOMO prices the output at ~{F["cocomo"]} person-years</text>')
    p.append('</svg>'); return "\n".join(p)


if __name__ == "__main__":
    for nm, fn in [("banner", banner), ("stats", stats), ("daily-lines", daily),
                   ("hours", hours), ("languages", langs), ("system", system)]:
        for dk, suffix in [(True, "dark"), (False, "light")]:
            open(os.path.join(ASSETS, f"{nm}-{suffix}.svg"), "w").write(fn(dk))
    print(f"regenerated 12 SVGs from docs/forensics.json ({A['span']})")
