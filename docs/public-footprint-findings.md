# Public-footprint sweep — Able Varghese (2026-08-08)

Method: WebSearch (3 queries) + Playwright visits (LinkedIn, licentric.com, lawyerserved.com,
argustest.dev, shelljolt.com, solveright.ai, keralora.com) + PyPI/npm registry APIs.

## Findings

| Source | Result | Detail |
|---|---|---|
| Google/web search (name + handle) | ❌ nothing relevant | "Able Varghese Tharayil"/"ablevt" return unrelated people; no link between name and products |
| Search (name + product names) | ❌ nothing | No indexed page connects "Able Varghese" to Licentric/LawyerServed/ShellJolt/SolveRight |
| LinkedIn /in/ablevt | 🔒 authwall (anonymous) | Full content already held via owner's PDF export (2026-08-08) |
| licentric.com | live, no founder mention | Title: "the control plane for AI agents, licensing built in" |
| lawyerserved.com | live, no founder mention | "Find Trusted Lawyers" |
| argustest.dev | live, no founder mention | "Give Your AI Eyes on iOS" |
| shelljolt.com | live, no founder mention | "cockpit for your AI coding CLIs" |
| solveright.ai | live, no founder mention | "155 Frameworks" positioning |
| keralora.com | live, minimal page | Title only: "Keralora" |
| **PyPI licentric** | ✅ **only public artifact naming him** | v0.3.0, author "Able Varghese", full SDK summary |
| npm licentric | ❌ not published | (repo README says "TS SDK npm pending" — consistent) |
| Carleton CanSat/OSPE/Ottawa Skeptics | ❌ not indexed by name | 2015 CanSat team pages exist but don't name him |

## Implications for the GitHub-profile project

1. **The GitHub profile will BE the public identity anchor** — nothing else on the open web
   connects the person to the portfolio. Highest-leverage single move.
2. Product sites name no founder — deliberate or not, owner should decide per-product
   (Keralora anonymity model may WANT this; Licentric/ArgusTest probably benefit from a founder page).
3. Cross-linking loop once profile ships: LinkedIn ↔ GitHub ↔ product sites ↔ PyPI = search
   engines finally connect name → work.
4. PyPI authorship already public and consistent with the plan.
