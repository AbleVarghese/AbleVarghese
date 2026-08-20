#!/usr/bin/env bash
# One command to refresh every published figure on the profile and the portfolio site.
#
#   bash scripts/refresh.sh [path/to/AbleVarghese.github.io]
#
# What it does, in order:
#   1. fetches every audited repo so the audit sees current history
#   2. re-mirrors the repos that have no local checkout
#   3. re-runs the forensic audit
#   4. regenerates all twelve SVGs from the audit output
#   5. rewrites README, METHODOLOGY and the site from the same output
#   6. syncs the GitHub repo description
#
# Nothing here is hand-typed, which is the point: the 2026-08-17 refresh left stale
# numbers in alt text and diagrams because those were written by hand while the
# charts read the audit JSON.
#
# The repo map lives in docs/repos.local.json (gitignored: it holds local paths and
# internal working-directory names). docs/repos.example.json is the public template.
set -euo pipefail

cd "$(dirname "$0")/.."
SITE="${1:-$HOME/AbleVarghese.github.io}"
MAP="docs/repos.local.json"
MIRRORS="mirrors"

[[ -f "$MAP" ]] || { echo "FATAL: $MAP missing. Copy docs/repos.example.json and fill in real paths."; exit 1; }

echo "==> 1/6 fetching local repos"
python3 - "$MAP" <<'PY' | while read -r p; do
import json, sys
print("\n".join(json.load(open(sys.argv[1]))["local"].values()))
PY
  [[ -d "$p/.git" ]] || { echo "  MISSING $p"; continue; }
  # origin only, never --all: several repos carry a second "gitlab" remote on the
  # Mac mini reachable through an SSH alias that does not resolve off-network, and
  # --all reports the whole fetch as failed even when GitHub succeeded. </dev/null
  # keeps git from consuming this loop's stdin.
  timeout 180 git -C "$p" fetch origin --prune -q </dev/null 2>/dev/null || echo "  fetch failed: $p"
done

echo "==> 2/6 refreshing bare mirrors"
mkdir -p "$MIRRORS"
python3 - "$MAP" <<'PY' | while read -r name path; do
import json, sys
for k, v in json.load(open(sys.argv[1]))["mirrors"].items():
    print(k, v)
PY
  if [[ -d "$path" ]]; then
    timeout 300 git -C "$path" fetch origin --prune -q </dev/null 2>/dev/null || echo "  fetch failed: $name"
  else
    echo "  cloning $name"
    timeout 600 gh repo clone "AbleVarghese/$name" "$path" -- --bare -q
  fi
done

echo "==> 3/6 running the audit"
python3 docs/forensics.py "$MAP" docs/forensics.json >/dev/null

echo "==> 4/6 regenerating assets"
python3 scripts/gen_assets.py

echo "==> 5/6 syncing figures"
python3 scripts/sync_figures.py "$SITE"
cp assets/*.svg "$SITE/assets/"
rm -f "$SITE/assets/banner-"*.svg   # the site header is HTML type, not the banner image

echo "==> 6/6 syncing the GitHub description"
bash scripts/sync_profile_meta.sh

cat <<'EOF'

Done. Review, then commit and push BOTH repos:
  cd ~/AbleVarghese-profile     && git add -A && git commit && git pull --rebase && git push
  cd ~/AbleVarghese.github.io   && git add -A && git commit && git push

Pull --rebase on the profile repo matters: a daily Action commits the
"Recently shipped" section, so local is usually behind.
EOF
