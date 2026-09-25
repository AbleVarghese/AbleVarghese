#!/usr/bin/env python3
"""Regenerate the 'Recently shipped' section of README.md from live repo activity.
Derive-never-hand-maintain: this section is never edited by hand (simonw pattern)."""
import json, re, urllib.request, os, datetime, subprocess

def get_token():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    try:
        token = subprocess.check_output(["gh", "auth", "token"], text=True, stderr=subprocess.DEVNULL).strip()
        if token:
            return token
    except Exception:
        pass
    return None

def api(path):
    headers = {"Accept": "application/vnd.github+json"}
    token = get_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"https://api.github.com{path}", headers=headers)
    return json.load(urllib.request.urlopen(req))

repos = api("/users/AbleVarghese/repos?sort=pushed&per_page=100&type=owner")
lines = []
for r in repos:
    if r["fork"] or r["name"] in ("AbleVarghese", ".github") or r["archived"]: continue
    when = r["pushed_at"][:10]
    desc = (r["description"] or "").split("·")[0].split(" — ")[0].strip()
    if len(desc) > 70: desc = desc[:70].rsplit(" ", 1)[0] + "…"
    lines.append(f'- **[{r["name"]}]({r["html_url"]})**: {desc} <sub>({when})</sub>')
    if len(lines) == 6: break
stamp = datetime.date.today().isoformat()
block = "\n".join(lines) + f"\n\n<sub>*Auto-generated {stamp} by [update_readme.py](scripts/update_readme.py). Derived, never hand-edited.*</sub>"
readme = open("README.md").read()
new = re.sub(r"(<!-- shipped starts -->).*?(<!-- shipped ends -->)",
             rf"\1\n{block}\n\2", readme, flags=re.S)
if new != readme:
    open("README.md","w").write(new); print("updated")
else: print("no change")
