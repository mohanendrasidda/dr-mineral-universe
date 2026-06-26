# CLAUDE.md — The Dr. Mineral Universe

Repo memory for Claude Code. Read `docs/` for full detail; this is the always-on summary.

## What this repo is
The build home for **The Dr. Mineral Universe**, an original transmedia IP by Mohanendra Siddha (Sidd): a novel-anchored world plus its public web surface and visual-asset pipeline. Creative and canon-led — NOT a strategy/business repo.

**Canon source of truth:** `docs/01_universe-bible-v1.md`. Nothing contradicts it without flagging a deliberate canon change.

## Layout
```
CLAUDE.md                  ← you are here
docs/                      ← canon, registry, story, manifest, briefs (read these)
canon/                     ← registry kept as living files (update as the world grows)
book-one/                  ← outline + chapter drafts
site/                      ← index.html (the public landing page) + future web
assets/raw/                ← source renders (Nano Banana / Gemini PNGs)
assets/keyed/              ← transparent, production-ready cutouts
.claude/skills/            ← ai-asset-generation, ai-render-keying, sprite-animation, immersive-html
```

## Core canon (check before producing)
- **Dr. Mineral:** campus squirrel, humble/curious/collaborative, secretly founder & Chief Researcher of the **Hidden Laboratory** beneath a university. "I don't collect treasure. I collect discoveries." Never revenge/fame/power.
- No magic — everything has a scientific explanation. Research is stewarded, not owned. No one is ever "finished" learning.
- 15 canon districts are fixed (add, don't rename/remove).
- **Tone:** hopeful, cinematic, educational, never dystopian. Multi-level (kids + adults, same text).
- **Blockchain is invisible** in-world — characters experience its benefits, never lecture it. If a draft explains the chain, it's broken.

## Registry discipline (the #1 habit)
Before introducing any character/department/lore, check `canon/`. After establishing anything new, update `canon/`. Continuity via git history is the point.

## Asset-request protocol
This is a visual project; when work needs art that doesn't exist, **stop and ask Sidd** — don't fake it or work around silently. Say what's needed, the kind (still render / GIF-sprite / 3D model / keyed cutout), and give a paste-ready brief with the consistency anchor from `docs/05_hero-portrait-brief.md`. Check `docs/04_asset-manifest.md` first — the pose may already exist (maybe just needs keying). Prefer keying an existing CLEAN render over regenerating. Request CLEAN acorn/discovery framing, never the off-canon chain.

## ⚠️ The chain is off-canon
Many `assets/raw/` renders wrap the squirrel in a literal chain (a blockchain pun built for a separate cohort project). That violates "technology is invisible." **Universe assets use the clean acorn poses only**; chained poses are not used here.

## Hard boundaries
- **Personal IP.** Keep clean of UNL institutional / work-for-hire territory. Don't share a repo/surface/post with cohort/UNL-implementation material.
- **Firewall.** Never use this fiction to explain, hint at, or illustrate any real UNL reward-system roadmap, governance, payouts, or strategic conclusions. Keep layers separate. Don't annotate lore with "this maps to our real X."
- Don't import influence-tactics framing (Cialdini/Greene/etc.) — that's a different project.

## Conventions
Commit by individual contributor; descriptive messages; canon changes flagged in the message. `site/index.html` is currently the cohort token page — re-skin to canon (drop chain/token framing, lead with Dr. Mineral + discovery) before it represents the universe.
