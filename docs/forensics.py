#!/usr/bin/env python3
"""Forensic quantification of a multi-repo portfolio.
Usage: python3 forensics.py repos.json out.json
Methods: git log timestamps; session-clustered hour estimation (git-hours algorithm,
two parameter sets -> honest range); LOC via git ls-files + line count; daily added
lines via --numstat; COCOMO-81 organic model for industry-standard effort framing.
All estimates are labeled as estimates."""
import subprocess, json, os, sys, collections, datetime, statistics

CFG = json.load(open(sys.argv[1])); OUT = sys.argv[2]

# --- Audit manifest: the tracked source-of-truth for coverage (issue #2) ---
# docs/repos.local.json only maps names to machine paths. WHAT is counted is
# decided by docs/audit-manifest.json (committed). Fail loud on any drift:
# an included repo missing/mismatched, or an excluded repo present, aborts.
MANIFEST_PATH = os.environ.get("AUDIT_MANIFEST") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "audit-manifest.json")
def _gh_id(url):
    import re
    m = re.search(r"github\.com[:/]([^/]+)/([^/\s]+?)(?:\.git)?$", (url or "").strip())
    return f"{m.group(1)}/{m.group(2)}" if m else None
def _remote(path):
    return subprocess.run(["git","-C",path,"remote","get-url","origin"],
                          capture_output=True,text=True).stdout.strip()
COVERAGE = None
if os.path.exists(MANIFEST_PATH):
    MAN = json.load(open(MANIFEST_PATH))
    inc = {e["name"]: e for e in MAN.get("included", [])}
    exc = {e["name"]: e for e in MAN.get("excluded", [])}
    configured = {**CFG.get("local", {}), **CFG.get("mirrors", {})}
    errors = []
    for name in sorted(set(configured) - set(inc)):
        errors.append(f"configured repo '{name}' is not in the audit manifest"
                      + (" (listed EXCLUDED: " + exc[name].get("rationale","") + ")" if name in exc else ""))
    for name in sorted(set(inc) - set(configured)):
        errors.append(f"manifest-included repo '{name}' has no local checkout/mirror in the config")
    for name, entry in inc.items():
        if name not in configured: continue
        path = configured[name]
        if not os.path.isdir(path):
            errors.append(f"included repo '{name}' path missing: {path}"); continue
        got = _gh_id(_remote(path))
        if got != entry["github"]:
            errors.append(f"included repo '{name}' remote identity {got} != manifest {entry['github']}")
    if errors:
        print("AUDIT MANIFEST VIOLATION:", *errors, sep="\n  - ", file=sys.stderr); sys.exit(1)
    COVERAGE = {"included": len(inc), "excluded": len(exc),
                "excluded_names": sorted(exc)}

CODE_EXT = {".ts",".tsx",".js",".jsx",".mjs",".cjs",".py",".swift",".rs",".sh",".zsh",
            ".sql",".go",".java",".kt",".c",".h",".cpp",".css",".scss",".html",".yml",
            ".yaml",".toml",".rb",".php"}
SKIP = ("node_modules","dist/","build/",".next/","vendor/","Pods/","package-lock",
        "pnpm-lock","yarn.lock","Cargo.lock",".min.",
        # generated tool/agent state, never authored source
        "/.claude/persistence/","/.claude/snapshots/",".wal","recovery-","snapshot-",
        "PERSISTENT_WORK_HISTORY","FILE_OPERATION_SUMMARY","UNTRACKED_FILES_LIST",
        # vendored copies / archived duplicate trees
        ".hotel-aggregator-origin/","_archived/",".backup")
AUTHORED = None  # set after CODE_EXT
AUTHORED = CODE_EXT | {".md"}
LANG = {".ts":"TypeScript",".tsx":"TypeScript",".js":"JavaScript",".mjs":"JavaScript",
        ".cjs":"JavaScript",".jsx":"JavaScript",".py":"Python",".swift":"Swift",
        ".rs":"Rust",".sql":"SQL",".css":"CSS",".scss":"CSS",".sh":"Shell",
        ".zsh":"Shell",".html":"HTML",".yml":"Config",".yaml":"Config",".toml":"Config"}

def git(p,*a): return subprocess.run(["git","-C",p]+list(a),capture_output=True,text=True).stdout

def hours(ts, gap=120, a=30, b=120):
    ts=sorted(ts)
    if not ts: return 0.0,0.0
    work=0; sess=1
    for x,y in zip(ts,ts[1:]):
        d=y-x
        if d<=gap*60: work+=d
        else: sess+=1
    base=work/3600
    return round(base+sess*a/60,1), round(base+sess*b/60,1)

def analyze(name,path,bare=False):
    log=git(path,"log","--all","--format=%at|%an <%ae>")
    lines=[l for l in log.strip().splitlines() if l]
    if not lines: return None
    ts=[int(l.split("|")[0]) for l in lines]
    authors=collections.Counter(l.split("|",1)[1] for l in lines if "|" in l)
    r={"name":name,"commits":len(lines),"ts":ts,"authors":dict(authors)}
    bare_repo = git(path,"rev-parse","--is-bare-repository").strip() == "true"
    r["uncommitted_entries"] = 0 if bare_repo else len(
        [l for l in git(path,"status","--porcelain").splitlines() if l])
    days={datetime.date.fromtimestamp(t) for t in ts}
    r["active_days"]=len(days); r["first"]=min(days).isoformat(); r["last"]=max(days).isoformat()
    r["hours_lo"],r["hours_hi"]=hours(ts)
    # daily added lines
    daily=collections.Counter(); day=None
    for L in git(path,"log","--all","--format=@%at","--numstat").splitlines():
        if L.startswith("@"): day=datetime.date.fromtimestamp(int(L[1:])).isoformat()
        elif L.strip() and day:
            p=L.split("\t")
            if (len(p)==3 and p[0].isdigit() and not any(x in p[2] for x in SKIP)
                    and os.path.splitext(p[2])[1].lower() in AUTHORED):
                daily[day]+=int(p[0])
    r["daily"]=dict(daily); r["added"]=sum(daily.values())
    if not bare:
        loc=0; by=collections.Counter(); tests=0; mdf=0; mdl=0
        seen=set()
        for row in git(path,"ls-files","-s").splitlines():
            try: meta,f = row.split("\t",1)
            except ValueError: continue
            sha = meta.split()[1]
            if any(x in f for x in SKIP): continue
            if sha in seen: continue          # identical content already counted
            seen.add(sha)
            fp=os.path.join(path,f)
            if not os.path.isfile(fp): continue
            ext=os.path.splitext(f)[1].lower()
            try: n=sum(1 for _ in open(fp,"rb"))
            except OSError: continue
            if ext in CODE_EXT:
                loc+=n; by[LANG.get(ext,"Other")]+=n
                b=os.path.basename(f).lower()
                if "test" in b or "spec" in b or "/tests/" in f or "/__tests__/" in f: tests+=1
            elif ext==".md": mdf+=1; mdl+=n
        r.update(loc=loc,langs=dict(by),test_files=tests,md_files=mdf,md_lines=mdl)
    return r

res=[]
for n,p in CFG["local"].items():
    x=analyze(n,p)
    if x: res.append(x)
for n,p in CFG.get("mirrors",{}).items():
    x=analyze(n,p,bare=True)
    if x: res.append(x)

all_ts=[t for r in res for t in r.pop("ts")]
daily=collections.Counter()
for r in res:
    for d,v in r.pop("daily").items(): daily[d]+=v
days=sorted(daily); vals=[daily[d] for d in days]
ds=[datetime.date.fromisoformat(d) for d in days]
streak=best=1
for x,y in zip(ds,ds[1:]):
    streak = streak+1 if (y-x).days==1 else 1
    best=max(best,streak)
langs=collections.Counter()
for r in res:
    for k,v in (r.get("langs") or {}).items(): langs[k]+=v
loc=sum(r.get("loc",0) for r in res)
kloc=loc/1000; pm=2.4*(kloc**1.05)
hod=collections.Counter(datetime.datetime.fromtimestamp(t).hour for t in all_ts)
tot_c=sum(hod.values()); ev=sum(v for h,v in hod.items() if h>=17 or h<2)
all_authors=collections.Counter()
for r in res: all_authors.update(r.pop("authors", {}))
agg=dict(repos=len(res), commits=sum(r["commits"] for r in res),
 coverage=COVERAGE,
 commit_authors=dict(all_authors.most_common(15)),
 uncommitted_repos=sum(1 for r in res if r.get("uncommitted_entries")),
 uncommitted_entries=sum(r.get("uncommitted_entries",0) for r in res),
 commit_active_days=len({datetime.date.fromtimestamp(t) for t in all_ts}),
 span=f"{datetime.date.fromtimestamp(min(all_ts))} to {datetime.date.fromtimestamp(max(all_ts))}",
 hours_lo=round(sum(r["hours_lo"] for r in res)), hours_hi=round(sum(r["hours_hi"] for r in res)),
 loc=loc, langs=dict(langs.most_common()), test_files=sum(r.get("test_files",0) for r in res),
 md_files=sum(r.get("md_files",0) for r in res), md_lines=sum(r.get("md_lines",0) for r in res),
 lines_added=sum(vals), delivery_days=len(days),
 median_day=int(statistics.median([v for v in vals if v>0])), peak_day_lines=max(vals),
 peak_day=days[vals.index(max(vals))], longest_streak=best,
 evening_pct=round(100*ev/tot_c), hour_of_day={h:hod.get(h,0) for h in range(24)},
 monthly=dict(sorted(collections.Counter(datetime.date.fromtimestamp(t).strftime("%Y-%m") for t in all_ts).items())),
 cocomo_person_months=round(pm), cocomo_person_years=round(pm/12,1))
json.dump({"aggregate":agg,"daily":dict(daily),"repos":res},open(OUT,"w"),indent=1,default=str)
print(json.dumps({k:v for k,v in agg.items() if k not in("hour_of_day","monthly","langs")},indent=1))
print("\nLANGS:",dict(langs.most_common(8)))
print("\nPER-REPO commits|days|LOC|tests|added")
for r in sorted(res,key=lambda x:-x["commits"]):
    print(f'{r["name"]:24}{r["commits"]:6} {r["active_days"]:5} {r.get("loc","-"):>9} {r.get("test_files","-"):>5} {r["added"]:>9}')
