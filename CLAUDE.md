# CLAUDE.md — The Dr. Mineral Universe

Repo memory for Claude Code. Read `docs/` for full detail; this is the always-on summary.

## What this repo is
The build home for **The Dr. Mineral Universe**, an original transmedia IP by Mohanendra Siddha (Sidd): a **living universe** — an underground research *civilization* — that surfaces as an interactive website, animations, books, and education. Creative and canon-led — NOT a strategy/business repo.

## ⭐ North star (v2 — the product is the world, not the book)
Build **a world that keeps happening,** not a story that happens. Decisions serve the *universe*, not a single plot.
- **The laboratory is a co-protagonist** — a bustling civilization (districts, daily life, society, festivals, engineering), not a backdrop. Aim: as unforgettable as Hogwarts / Pandora / Coruscant.
- **Every district maps to a website feature** — explore a real place, not a menu. See `canon/district-atlas.md`.
- **The lab evolves with versions** — every software release is a *physical expansion* (new wings, cranes, scaffolding). "TODAY IN THE LAB" is the content model; visitors return because the world grew. See `canon/growth-and-versions.md`.
- **The campus squirrels are the hidden civilization** (Sidd's original inspiration) — every campus squirrel is secretly a lab member with a role; **many** entrances, each to a different district. See `canon/the-squirrel-network.md`.
- **A research civilization that invents technology** — prototypes, failures, debugging, the joy of making. **Blockchain is ONE invention among many** (AI, robotics, distributed systems, cybersecurity, energy), emerging naturally. Audience includes students, developers, researchers, security/blockchain people. See `canon/technology-and-engineering.md`.
- **Pixar rule: emotion + humor.** Dr. Mineral has real flaws and the lab has comedy; the funny beats make the emotional ones land. See his flaw sheet in `canon/characters.md`.
- **The novel is one artifact, not the universe.** Book I (`book-one/`) is "a first thread," kept for its voice but subordinate to the world.

**Canon source of truth:** `docs/01_universe-bible-v1.md` **as evolved by** `docs/06_universe-bible-v2.md` (the living-universe expansion — a *deliberate* canon change, esp. the broadened mission). v2 wins on conflict.

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
- **Mission (v2, broadened — deliberate canon change):** *"Our laboratory exists to discover, build, protect, preserve, and pass on knowledge that helps future generations contribute more than we could."* The Contribution Registry is **one department** of a larger research civilization, not the whole mission.
- **Dr. Mineral:** campus squirrel, humble/curious/collaborative, secretly founder & Chief Researcher of the **Hidden Laboratory** beneath a university. "I don't collect treasure. I collect discoveries." Never revenge/fame/power. **Has real flaws + humor** (see characters.md) — he is not a saint.
- No magic — everything has a scientific/engineered explanation. Research is stewarded, not owned. No one is ever "finished" learning.
- The original 15 canon districts are fixed (add, don't rename/remove); the world now has **many more** — see `canon/district-atlas.md`.
- **Tone:** hopeful, cinematic, educational, never dystopian; **emotion + humor** (Pixar). Multi-level (kids + adults, same text).
- **Blockchain emerges, never lectures.** It is one of many inventions; characters experience benefits and *build* it as research, but a draft that explains the chain like a whitepaper is broken. Lead with curiosity, characters, the world.

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
