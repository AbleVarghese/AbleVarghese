#!/usr/bin/env python3
"""Forensic quantification of 3 years of portfolio work across all original repos.
Methods: git log timestamps; session-clustered hour estimation (git-hours algorithm,
two parameter sets → honest range); LOC via git ls-files+wc for local repos;
COCOMO-81 organic model for industry-standard effort framing. All estimates labeled."""
import subprocess, json, os, collections, datetime, math

HOME = os.path.expanduser("~")
SCRATCH = os.path.dirname(os.path.abspath(__file__))
LOCAL = json.load(open("repos.json"))["local"]  # {name: path} — supply your own
MIRROR = json.load(open("repos.json"))["mirrors"]  # {name: bare-clone path}

CODE_EXT = {".ts",".tsx",".js",".jsx",".mjs",".cjs",".py",".swift",".rs",".sh",".zsh",
            ".sql",".go",".java",".kt",".c",".h",".cpp",".css",".scss",".html",".yml",
            ".yaml",".toml",".rb",".php"}
EXCLUDE_PARTS = ("node_modules","dist/","build/",".next/","vendor/","Pods/",
                 "package-lock","pnpm-lock","yarn.lock","Cargo.lock",".min.")

def git(path, *args):
    r = subprocess.run(["git","-C",path]+list(args), capture_output=True, text=True)
    return r.stdout

def hours_from_sessions(ts, gap_min=120, first_add_min_a=30, first_add_min_b=120):
    """git-hours session clustering. Returns (conservative, standard) hour estimates."""
    ts = sorted(ts)
    if not ts: return 0.0, 0.0
    work_sec, sessions = 0, 1
    for a, b in zip(ts, ts[1:]):
        d = b - a
        if d <= gap_min*60: work_sec += d
        else: sessions += 1
    base = work_sec/3600
    return round(base + sessions*first_add_min_a/60,1), round(base + sessions*first_add_min_b/60,1)

def analyze(name, path, bare=False):
    out = {"name": name}
    log = git(path,"log","--all","--format=%at|%ae|%an")
    lines = [l for l in log.strip().splitlines() if l]
    if not lines: return None
    ts = [int(l.split("|")[0]) for l in lines]
    out["commits"] = len(lines)
    authors = collections.Counter(l.split("|")[2] for l in lines)
    out["top_author"], out["top_author_commits"] = (authors.most_common(1)[0])
    days = {datetime.date.fromtimestamp(t) for t in ts}
    out["active_days"] = len(days)
    out["first"] = min(days).isoformat(); out["last"] = max(days).isoformat()
    out["hours_lo"], out["hours_hi"] = hours_from_sessions(ts)
    out["ts"] = ts  # for aggregate histograms
    # co-authored-by (agentic workflow share)
    co = git(path,"log","--all","--format=%b").count("Co-Authored-By")
    out["coauthored"] = co
    if not bare:
        files = [f for f in git(path,"ls-files").splitlines()
                 if not any(x in f for x in EXCLUDE_PARTS)]
        loc_by_ext = collections.Counter(); loc = 0; test_files=0; md_lines=0; md_files=0
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            fp = os.path.join(path,f)
            if not os.path.isfile(fp): continue
            try: n = sum(1 for _ in open(fp,"rb"))
            except OSError: continue
            base = os.path.basename(f).lower()
            if ext in CODE_EXT:
                loc += n; loc_by_ext[ext]+=n
                if "test" in base or "spec" in base or "/__tests__/" in f or "/tests/" in f or f.startswith("tests/"): test_files+=1
            elif ext==".md": md_lines+=n; md_files+=1
        out["loc"]=loc; out["loc_by_ext"]=dict(loc_by_ext.most_common(6))
        out["test_files"]=test_files; out["md_files"]=md_files; out["md_lines"]=md_lines
    return out

results=[]
for n,p in LOCAL.items():
    r=analyze(n,p);  results.append(r) if r else None
for n,p in MIRROR.items():
    r=analyze(n,p,bare=True); results.append(r) if r else None

# aggregates
all_ts=[t for r in results for t in r.pop("ts")]
agg={
 "repos": len(results),
 "total_commits": sum(r["commits"] for r in results),
 "total_active_days": len({datetime.date.fromtimestamp(t) for t in all_ts}),
 "span": f'{datetime.date.fromtimestamp(min(all_ts))} → {datetime.date.fromtimestamp(max(all_ts))}',
 "hours_lo": round(sum(r["hours_lo"] for r in results)),
 "hours_hi": round(sum(r["hours_hi"] for r in results)),
 "total_loc_measured": sum(r.get("loc",0) for r in results),
 "total_test_files": sum(r.get("test_files",0) for r in results),
 "total_md_files": sum(r.get("md_files",0) for r in results),
 "total_md_lines": sum(r.get("md_lines",0) for r in results),
 "total_coauthored": sum(r["coauthored"] for r in results),
}
# hour-of-day + monthly cadence
hod=collections.Counter(datetime.datetime.fromtimestamp(t).hour for t in all_ts)
agg["hour_of_day"]={h:hod.get(h,0) for h in range(24)}
mon=collections.Counter(datetime.date.fromtimestamp(t).strftime("%Y-%m") for t in all_ts)
agg["monthly"]=dict(sorted(mon.items()))
# COCOMO-81 organic: PM = 2.4 * KLOC^1.05  (person-months of 152h)
kloc=agg["total_loc_measured"]/1000
pm=2.4*(kloc**1.05)
agg["cocomo_person_months"]=round(pm)
agg["cocomo_person_years"]=round(pm/12,1)
agg["cocomo_hours_equiv"]=round(pm*152)

json.dump({"aggregate":agg,"repos":results}, open(f"{SCRATCH}/forensics.json","w"), indent=1, default=str)
print(json.dumps(agg, indent=1))
print("\nPER-REPO (commits | days | hours lo-hi | LOC | tests | md):")
for r in sorted(results,key=lambda x:-x["commits"]):
    print(f'{r["name"]:18} {r["commits"]:6} | {r["active_days"]:4} | {r["hours_lo"]:7}-{r["hours_hi"]:<7} | {r.get("loc","-"):>8} | {r.get("test_files","-"):>5} | {r.get("md_files","-"):>4}')
