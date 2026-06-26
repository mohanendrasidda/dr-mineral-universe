# Product Direction v3 — The Living 3D Blockchain-Mining World

**Authoritative.** Locked 2026-06-26 after an explicit re-verification of the vision. Supersedes v2's "many inventions / many districts" spread. The soul (Dr. Mineral, curiosity, warmth, no magic, hopeful tone) is unchanged.

## The one-line vision
**A true 3D explorable world — Clash-of-Clans-style — where Dr. Mineral's lab is a blockchain-mining civilization that is *always working*: squirrels mine blocks, forge them onto the chain, record them in the ledger, store the value, and guard it. You move through it and watch it run.**

## The big corrections from v2 (what changed)
1. **Blockchain/mining is the ONLY technology.** v2 spread the world across AI, robotics, security, education, etc. — that diluted it. Gone. Everything is the chain.
2. **The product is a living 3D world**, not a scrolling lore site. The site we built is the *skin*; `site/world/` (Three.js) is the *product*.
3. **"Always happening" is literal** — autonomous characters on work loops (mine → haul → forge → record), not lore text. Like Clash of Clans' base that's alive when you open it.

## The core loop (the only districts)
A blockchain, told as a mining town. Each zone is a step in the loop:

| Zone | Blockchain meaning | What you SEE happening | Lead |
|---|---|---|---|
| **The Mines** | Mining / proof-of-work | Squirrels & mechanical miners dig glowing crystal "blocks" from the seams, on endless loops | Pip (mining bots) |
| **The Foundry** | Forging a block onto the chain | Miners haul crystals here; they're forged into links and welded onto the great glowing chain | Master Castor (beaver) |
| **The Ledger** | The distributed ledger / chain of trust | Every forged block is recorded as an honored link; a new star kindles | Vellum + Tally |
| **The Vault** | Treasury / stored value | Mined value & the Seed kept safe under blue light | (keeper TBD) |
| **The Watch** | Security / consensus | Sentinels guard the chain, sound the alarm, verify | Commander Sasha (meerkat) |

The world is the loop: **Mine → Forge → Ledger → Vault**, with **the Watch** protecting all of it.

## What stays / what's archived
- **Active:** Dr. Mineral, Tally, Vellum, Castor, Sasha, Pip; the Mines/Foundry/Ledger/Vault/Watch; all blockchain-mining themed assets.
- **Archived (not deleted, not active):** AI Center, Codeworks, Educational Academy, Commons & Bakery, Historical Archives, Version History Museum, the multi-tech atlas, the campus-feature mapping. They were good craft; they're off-theme now. Kept in git history / `canon/` for possible later flavor, but not part of v3.
- **The scrolling site** (`site/index.html`, `site/districts/`) becomes a **landing/skin** in front of the 3D world, or is retired. Decide as the world matures.

## Build phases (toward the 3D world)
- **Phase 0 — Prototype (now):** a Three.js explorable scene you can orbit/move: a cavern with the 5 zones marked, Dr. Mineral + a miner as **billboard sprites** (our keyed renders), a visible **mining loop** (miner digs a crystal, hauls it to the forge), and a **glowing chain** that grows as blocks are forged. Proves the living-world direction with the assets we already have. → `site/world/index.html`.
- **Phase 1 — The living base:** all 5 zones modeled, multiple autonomous workers on loops, day-feel lighting, click a zone to focus, the chain visibly lengthening over time ("blocks" accumulating).
- **Phase 2 — Real 3D assets:** replace billboard sprites with actual 3D character models. **Asset reality:** image generators (Nano Banana) make 2D only; true 3D needs models — via image-to-3D tools (Meshy / Luma / Tripo / Rodin) from our character renders, or hand-modeled low-poly. Until then, billboard sprites of our 2D renders are the bridge (a legit, good-looking technique).
- **Phase 3 — Functional layer:** wire the world to real data so it's a *functional product* (the end goal you chose) — the Ledger reflects real contributions/commits, mining ticks are real events, the chain is real state. Stack decision (static+data vs backend/DB) happens here.

## Stack
- **Phase 0–1:** Three.js via CDN, single self-contained page, no build step; served over `http://localhost` (Three texture loading needs http, not file://).
- **Phase 2+:** likely a real bundler (Vite) + GLTF models; revisit then.

## Guardrails (unchanged)
Personal IP; firewalled from any real UNL reward-system roadmap; warm/hopeful tone; no magic (mining/forging are "engineered," fantastical but not magical).
