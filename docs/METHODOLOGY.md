# Portfolio metrics — methodology

Every number on this profile is computed, not claimed. This document + `forensics.py` let anyone
reproduce them against the underlying repositories (private repos verifiable on request).

| Metric | Method |
|---|---|
| Commits (8,010) | `git log --all --format=%at\|%ae\|%an` across 20 original (non-fork) repositories, Dec 2024 – Aug 2026 |
| Active days (254) | Distinct calendar dates among all commit timestamps |
| Hours (~1,850–2,900) | Session clustering (the git-hours algorithm): commits ≤120 min apart form a session; range = Σ intra-session gaps + per-session start adjustment of 30 min (low) / 120 min (high). An estimate of orchestration wall-clock, labeled as such |
| Lines of code (1.27M) | `git ls-files` on 15 locally-present repos, code extensions only, excluding dependencies, lockfiles, build output, vendored code. Includes SQL/config/styles — it is *tracked, authored* code, not just business logic |
| Test files (2,412) | Files matching test/spec naming conventions among counted code files |
| Docs (2,115 files / 554K lines) | Markdown census, same exclusions |
| Night/evening share (49%) | Commits with author-hour ≥17:00 or <02:00 |
| COCOMO ≈364 person-years | COCOMO-81 organic model, PM = 2.4 × KLOC^1.05 on measured LOC. A model of *conventional hand-written* effort — cited precisely because agentic engineering breaks its assumptions |

**Honest boundaries:** hour figures are estimates from commit patterns, not timesheets. LOC measured
on the 15 repos present locally; 5 more counted for commits only. Pre-Dec-2024 work (e.g. an earlier
fintech prototype) predates these histories and is excluded.

**Pre-2023 career record:** the ~5,000+ commits / 20+ projects / 1–37-member teams figure for
2014–2023 is the owner's stated career record (consistent with the LinkedIn history), not part of
the git-measured numbers above — those repositories are corporate/private and contractually
confidential, so they cannot be published or independently audited here.

**Lines delivered per day (3.0M added):** `git log --all --numstat` across the 15 locally audited
repos, additions summed per author-date, dependency/lockfile/build paths excluded. Additions exceed
final LOC (1.27M) because code gets rewritten; both numbers are stated. Commit dates lag the work
they contain: multi-day efforts often land in one commit, so recorded active days (201) are a lower
bound on true working days and single-day spikes are usually batch landings. The daily chart uses a
square-root scale, stated on the chart, so median days stay visible next to the 194K peak.


---

## Revision, 2026-08-17 (v2 methodology)

Numbers were re-derived across **21 repositories** (up from 15) after three of the previously
commits-only repos became locally auditable and two new projects landed. The counting rules were
also tightened, so the change reflects both new work and a stricter method:

| Rule | v1 | v2 |
|---|---|---|
| Generated tool/agent state (`.claude/persistence/`, `snapshot-*.json`, `recovery-*.json`, `*.wal`, work-history dumps) | counted | **excluded** |
| Vendored/archived duplicate trees inside a repo | counted | **excluded** |
| Identical file contents appearing at several paths | counted once per path | **counted once**, deduplicated by git blob hash |
| Daily "lines delivered" | every changed file | **authored extensions only** (code + Markdown) |

The v2 rules were adopted after an audit found a monorepo contributing 150M apparent added lines,
almost all of it committed agent-state JSON. That figure was never published; it was caught by
sanity-checking the per-repo table before publication.

**Current figures:** 8,533 commits · 1.77M lines in production · 5.2M lines delivered ·
2,553 test files · 2,873 docs (716K lines) · 262 active days · ~3,050 hours ·
median 9,964 lines per active day · longest streak 86 days · COCOMO-81 ~515 person-years.

Excluded by choice: the profile repository and portfolio site themselves, and two third-party
checkouts. Recovery duplicates of an existing repo are excluded to avoid double counting.
