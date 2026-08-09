# Profile-excellence research — top AI/software GitHub presences (2026-08-08)

Sources (live API reads, 2026-08-08): karpathy (215,640 followers), torvalds (315,540),
gaearon (91,233), sindresorhus (80,942), simonw (16,337), Shubhamsaboo (9,582).

## Findings

| Profile | Excellence pattern | Verdict for Able |
|---|---|---|
| **karpathy** | One-line HUMAN bio ("I like to train deep neural nets…"); 13 gists that TEACH (each a mini-lesson); repos named nano-/min-/micro- with "simplest, fastest" framing; education as leverage (nn-zero-to-hero, LLM101n); zero marketing tone | ✅ ADOPT: teaching gists, human one-liner, minimalist framing of OSS tools |
| **simonw** | Profile README with AUTO-UPDATING sections (Action-driven markers: recent releases / blog / TILs); "Currently working on X, Y" opener; subscribe links | ✅ ADOPT: self-updating "Recently shipped" section (perfectly matches derive-never-hand-maintain doctrine) |
| **sindresorhus** | Personality + humor (retro gifs); "latest app" CTA; Full-Time Open-Sourcerer identity | ⚠️ PARTIAL: the CTA pattern yes; the humor conflicts with banking-grade positioning — rejected deliberately |
| **gaearon / torvalds** | NO profile README at all — pure artifact reputation | 📌 LESSON: at the top, the work IS the profile. Long-term: reputation > decoration |

## Adoptions implemented (on top of existing profile)
1. Self-updating "Recently shipped" README section — nightly GitHub Action, marker-driven (simonw pattern).
2. Teaching gist: the portfolio-audit methodology + script published as a public gist (karpathy pattern).
3. Human one-liner added to README (karpathy pattern).
