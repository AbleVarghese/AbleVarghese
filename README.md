<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="Able Varghese — Application Architect. Ships production platforms end-to-end." src="assets/banner-light.svg" width="100%">
</picture>

### Application architect. I ship complete platforms, solo, at production grade.

*I like building complete production systems, and the engineering machines that build them.*

Software engineer since 2014, with banking-grade delivery for CIBC and payments fintechs behind me.
That discipline now runs a portfolio of **10+ products built in under two years**: architected,
developed, tested, and operated using **agentic AI engineering systems** I designed myself. Every
platform below is real, running software. Full stacks, payment rails, compliance engines, test
suites in the thousands.

## The portfolio, measured

*Computed from git history across 20 original repositories. The audit script and methodology
are published in this repo ([`docs/METHODOLOGY.md`](docs/METHODOLOGY.md)) so every number is verifiable.*

**8,010 commits** · **1.27M lines of tracked code** · **2,412 test files** · **2,115 docs
(554K lines)** · **254 active build days** · **~2,900 hours**, 49% of them between 5pm and 2am,
nights and weekends alongside a full-time payments-fintech role.

Classical software economics (COCOMO-81) prices this codebase at **~364 person-years** of
conventional effort. It was shipped by one person with a self-built agentic engineering system.
**That multiplier is the point.**

*And this is only the public-era ledger. 2014–2023 adds an estimated **5,000+ commits across 20+
enterprise projects**, in teams from solo to 37 people, living in corporate and private
repositories that stay confidential by contract.*

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cadence-dark.svg">
  <img alt="Monthly commits across 20 repositories, December 2024 to August 2026, ramping from single digits to a peak of 2,871 in July 2026" src="assets/cadence-light.svg" width="100%">
</picture>

<sub>*Aug '26 is a partial month. Chart generated from the same audit data as the numbers above, no third-party widgets.*</sub>

**Currently:** Application Systems Analyst at an Interac-member fintech (payments infrastructure) · Founder, building in Toronto 🇨🇦
**Always open to** interesting conversations: architecture, agentic engineering, fintech, or what you're building.

---

## Recently shipped

<!-- shipped starts -->
- **[ops-dashboard](https://github.com/AbleVarghese/ops-dashboard)**: Ops dashboard <sub>(2026-08-09)</sub>
- **[AbleVarghese.github.io](https://github.com/AbleVarghese/AbleVarghese.github.io)**: Portfolio <sub>(2026-08-09)</sub>
- **[ios-claude-toolkit](https://github.com/AbleVarghese/ios-claude-toolkit)**: 22 battle-tested Claude Code skills for iOS/Swift development <sub>(2026-08-09)</sub>
- **[keralora.com](https://github.com/AbleVarghese/keralora.com)**: Invite-only B2B spice trade, Kerala → Canada, with three-wall… <sub>(2026-08-08)</sub>
- **[shelljolt.com](https://github.com/AbleVarghese/shelljolt.com)**: The cockpit for AI coding CLIs <sub>(2026-08-08)</sub>
- **[argustest.dev](https://github.com/AbleVarghese/argustest.dev)**: iOS device monitoring + AI-assisted debugging via MCP for Claude Code… <sub>(2026-08-08)</sub>

<sub>*Auto-generated 2026-08-08 by [update_readme.py](scripts/update_readme.py). Derived, never hand-edited.*</sub>
<!-- shipped ends -->

## Platforms I've built and operate

| Platform | What it is | Under the hood |
|---|---|---|
| **[Licentric](https://licentric.com)** | Software licensing and monetization, from license keys to AI-agent tokens. 3 minutes to first validation vs. hours on incumbents | Ed25519 offline-first signed licenses · declarative Stripe→license mapping (zero webhook code) · Python SDK on PyPI · TypeScript |
| **[LawyerServed](https://lawyerserved.com)** | North America's transparent legal directory: **1.47M+ verified lawyer profiles** in a double-blind two-sided marketplace | Next.js 16 · tRPC · Drizzle · Supabase RLS · Meilisearch at 1M+ scale · Stripe · per-jurisdiction compliance rule-packs |
| **[SolveRight](https://solveright.ai)** | Decision intelligence. **155 decision frameworks** run simultaneously with deterministic 0–100 scoring and contradiction detection | Three-phase AI+deterministic hybrid scoring engine · <100ms sensitivity analysis · 7 export formats |
| **[solvemax](https://solvemax.solveright.ai)** | A verdict with receipts: decisions interrogated, scored, red-teamed through **5,000 seeded Monte-Carlo futures**, then given a blind second-pass audit | Next.js · multi-model LLM failover chain · Stripe · seeded deterministic simulation |
| **[ArgusTest](https://argustest.dev)** | iOS device monitoring and AI-assisted debugging for Claude Code / Cursor users. 100% app-agnostic | MCP integration · HMAC-verified webhooks · SHA-256 error dedup (78% noise reduction) · self-healing daemons |
| **[ShellJolt](https://shelljolt.com)** | macOS cockpit for AI coding CLIs. Cost, context, usage-limits, and model in one live line; stops OOM freezes before they happen | Rust · Ed25519 licensing · adaptive per-session memory engine · cross-CLI (Claude/Codex/Gemini/Grok) |
| **[Keralora](https://keralora.com)** | Invite-only B2B spice-trade platform, Kerala to Canada, with complete buyer↔seller anonymity | Three-wall anonymity architecture (DAL + Postgres RLS + document redaction) · anonymity test suite in CI |

## Engineering infrastructure I built to build them

The portfolio above is shipped by a self-built **agentic engineering system**. This is the part most profiles can't show:

- **Multi-agent orchestration doctrine**: model-tiered routing (reason/build/research), adaptive concurrency with circuit breakers, orchestrator-gated acceptance where no agent's work merges until independently re-verified
- **Scrapos**: standalone data-supply engine. 64 scrapers, queue-based pipeline, self-healing, drift-gated auto-redeploy
- **SwitchboardOS**: control plane for LLM cost, observability, and agent governance
- **[ops-dashboard](https://github.com/AbleVarghese/ops-dashboard)**: zero-dependency live SDLC monitor that watches every project's agents, tests, and git state simultaneously over SSE. **Open source (MIT)**
- **local-gitlab**: fully self-hosted GitLab CE + runner. $0/month CI/CD any project plugs into
- **Relay**: portable partner-marketing engine (attribution, commissions, payouts) that integrates with any product from zero code upward
- **[ios-claude-toolkit](https://github.com/AbleVarghese/ios-claude-toolkit)**: 22 battle-tested Claude Code skills for iOS, distilled from 75+ production sessions. **Open source (MIT)**
- **Flowen**: iOS money-transfer app. Swift 6, MVVM, **2,838 test methods**, 9-stage CI pipeline
- **Devrule.ai**: enterprise AI-rules middleware that validates code changes against configurable rules before AI tools (Claude Code, Cursor, Copilot) can execute them. Multi-tenant RLS, Stripe billing, 40+ test suites
- **Dwellium**: trust-first hotel booking platform. NestJS monorepo, **294-table** global schema, Amadeus + Stripe integration, web + React Native mobile

## Before this

**Interac-member fintech**, Application Systems Analyst: BASE24 / HP NonStop transaction processing, AI-agent orchestration for internal tooling
**CIBC** (4 yrs), Senior Application Engineer: architected and shipped five banking applications to production; Java/Python; CI/CD with IBM UrbanCode; Scrum Master; led the Drive Smart iOS/Android app team as PM; built an internal application platform and CMS used across Solutions, Development, QA, Build and Production teams
**StrongBase Capital**, securities and options trader: quantitative strategies, Greeks-based risk management
**Spine Hedge** (2021–), AI-powered fintech project: the bridge between my trading years and the platform portfolio above
**Earlier**: Mechanical Engineering @ Carleton · Software Engineering @ Centennial · NASA CanSat & Lunabotics team lead · conference speaker on engineering entrepreneurship

*A decade of enterprise work before 2024, for CIBC and other institutions and clients, stays
confidential, per contract and by principle. The portfolio above is what I can show publicly;
the discipline underneath it is what those years built.*

## How I work

TDD-first · spec-before-code · structural prevention over instance fixes · single-source-of-truth
documentation · evidence before conclusions. The whole doctrine is codified as machine-enforced
rules my agent fleets follow. Quality is a system property, not a habit.

---

📫 **able.varghese@hotmail.com** · [LinkedIn](https://www.linkedin.com/in/ablevt/) · [X @AbleVeez](https://x.com/AbleVeez) · Toronto, Canada

<!-- profile v1.2 -->
