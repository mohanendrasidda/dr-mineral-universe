# CLAUDE.md — The Dr. Mineral Universe

Repo memory for Claude Code. Read `docs/` for full detail; this is the always-on summary.

## What this repo is
The build home for **The Dr. Mineral Universe**, an original transmedia IP by Mohanendra Siddha (Sidd): a **living universe** — an underground research *civilization* — that surfaces as an interactive website, animations, books, and education. Creative and canon-led — NOT a strategy/business repo.

## ⭐ North star (v3 — a living 3D blockchain-mining world)
**Authoritative. Supersedes v2's "many inventions" spread (deliberate canon change).** Full detail: `docs/10_product-direction.md`.
- **Blockchain/mining is the WHOLE point — the only technology.** Not one of many. The lab is a **blockchain-mining civilization**; everything serves the chain. (v2's AI/robotics/SOC/education spread is retired.)
- **The core loop (the only districts):** **Mines** (squirrels mine crystal "blocks") → **Foundry** (forge blocks onto the chain) → **Ledger** (record every contribution; the chain of trust) → **Vault** (treasury of mined value) → **Watch** (secure the chain). That's the world.
- **The product is a TRUE 3D explorable world** (Three.js) — Clash-of-Clans-style: characters are **always mining, hauling, forging, working**; the world perpetually *does something*; you move through it and interact. The scrolling site is just the skin; the **3D world is the product.** Lives in `site/world/`.
- **Dr. Mineral + the lab are the story/brand** — the warm, charming face on the blockchain world. The novel (`book-one/`) is one subtle artifact; the world is overtly blockchain.
- **Pixar emotion + humor** stays; warm characters with flaws.

**Retired from v3:** "blockchain invisible," "blockchain one of many," the broad multi-tech district atlas, the campus-feature mapping. The off-theme districts (AI Center, Sentinel Hall, Codeworks, Academy, Commons, Archives, Version Museum) are **archived**, not active. Firewall + personal-IP rules still hold.

**Canon source of truth:** `docs/01_universe-bible-v1.md` (the soul) **as refocused by** `docs/10_product-direction.md` (v3 — authoritative). `docs/06_universe-bible-v2.md` is superseded where it conflicts (the multi-tech spread).

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
