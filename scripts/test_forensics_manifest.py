#!/usr/bin/env python3
"""Negative controls for docs/forensics.py manifest enforcement."""
import json, os, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORENSICS = os.path.join(ROOT, "docs", "forensics.py")
def git(path, *args):
    subprocess.run(["git", "-C", path, *args], check=True, capture_output=True)
def make_repo(path, remote_repo):
    os.makedirs(path)
    git(path, "init", "-q"); git(path, "config", "user.email", "t@t.t"); git(path, "config", "user.name", "Able Varghese")
    open(os.path.join(path, "a.py"), "w").write("x = 1\n")
    git(path, "add", "."); git(path, "commit", "-qm", "init")
    git(path, "remote", "add", "origin", f"https://github.com/AbleVarghese/{remote_repo}.git")
def run(manifest, cfg):
    with tempfile.TemporaryDirectory() as d:
        mp, cp, out = (os.path.join(d, n) for n in ("m.json", "c.json", "o.json"))
        json.dump(manifest, open(mp, "w")); json.dump(cfg, open(cp, "w"))
        env = {**os.environ, "AUDIT_MANIFEST": mp}
        return subprocess.run([sys.executable, FORENSICS, cp, out], capture_output=True, text=True, env=env)
def main():
    with tempfile.TemporaryDirectory() as d:
        owned, upstream = os.path.join(d, "owned"), os.path.join(d, "up")
        make_repo(owned, "owned"); make_repo(upstream, "upstream")
        manifest = {"included": [{"name": "owned", "github": "AbleVarghese/owned", "classification": "owned-primary", "via": "local"}],
                    "excluded": [{"name": "upstream", "github": "AbleVarghese/upstream", "classification": "upstream-import", "rationale": "upstream history, not owner delivery"}]}
        clean = {"local": {"owned": owned}, "mirrors": {}}
        cases = [("clean passes", manifest, clean, 0),
                 ("excluded repo in config fails", manifest, {"local": {"owned": owned, "upstream": upstream}, "mirrors": {}}, 1),
                 ("included repo missing fails", manifest, {"local": {}, "mirrors": {}}, 1),
                 ("remote mismatch fails", {"included": [{"name": "owned", "github": "AbleVarghese/other", "classification": "owned-primary", "via": "local"}], "excluded": manifest["excluded"]}, clean, 1)]
        failed = 0
        for label, m, c, want in cases:
            got = run(m, c).returncode
            ok = (got == 0) == (want == 0)
            print(f"{'PASS' if ok else 'FAIL'}: {label} (exit={got}, want {'0' if want==0 else 'nonzero'})")
            failed += not ok
        sys.exit(1 if failed else 0)
if __name__ == "__main__":
    main()
