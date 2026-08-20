#!/usr/bin/env bash
# Set the profile repo's GitHub description from the audit data.
#
# The description is a published surface: it shows on the repo page and in search
# results, and it carried figures that went stale twice because nothing generated
# them. This makes it derived like every other figure on the profile.
#
#   bash scripts/sync_profile_meta.sh          # apply
#   bash scripts/sync_profile_meta.sh --dry    # print what it would set
#
# Deliberately NOT touching the user bio: that field is kept figure-free precisely
# so it has nothing that can go stale.
set -euo pipefail

cd "$(dirname "$0")/.."

read -r LINES COMMITS < <(python3 -c "
import json
a = json.load(open('docs/forensics.json'))['aggregate']
print(f\"{a['lines_added']/1e6:.2f}M\", f\"{a['commits']:,}\")
")

DESC="Profile: verified portfolio metrics. ${LINES} lines delivered · ${COMMITS} commits · 10 platforms + published research, built with agentic engineering"

if [[ "${1:-}" == "--dry" ]]; then
  echo "would set: $DESC"
  echo "currently: $(gh api repos/AbleVarghese/AbleVarghese --jq .description)"
  exit 0
fi

gh api -X PATCH repos/AbleVarghese/AbleVarghese -f description="$DESC" --jq .description
echo "description synced to audit figures"
