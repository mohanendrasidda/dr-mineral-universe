# The Dr. Mineral Universe — Vision & Review Brief

**Purpose of this document:** hand it to a fresh reviewer (another Claude or a person) so they can (1) understand exactly what we are trying to build and the feeling we are chasing, (2) look at the current build, and (3) write back a complete, structured read of *how it actually looks/feels right now* and *how to improve it*. The last two sections tell the reviewer precisely what to evaluate and what to return.

---

## 1. What this project is (one paragraph)

This is the **public face of a University of Nebraska–Lincoln cybersecurity cohort's "Lab Reward Coin"** — a blockchain reward system that pays out for *genuine security work* (bugs found, audits written, protocols hardened), designed to be Sybil-resistant with a real institutional sink, and explicitly **not** a financial security. The engineering is a normal Web3 stack. But the **public skin** is a living storybook world: an **ancient underground laboratory-civilization** kept by a humble campus squirrel, **Dr. Mineral**. The blockchain *is* the world — mining, forging, recording, guarding — told warmly so a newcomer feels wonder first and understands the system second. It is the owner's (Sidd's) IP, brand-skinning a real cohort project.

## 2. The north star (the vision)

- **The product is a true 3D explorable, always-working world** (Three.js, runs in the browser). Think **Clash-of-Clans energy**: the world is perpetually *doing something* — squirrels mine crystal "blocks," haul them, a smith forges them onto a glowing chain, a keeper records them, sentinels guard them. You move a camera through it and click to explore. **The scrolling website is just the skin; the 3D world is the actual product.**
- **Blockchain/mining is the ONLY theme.** Everything serves the chain. There is one set of districts — the **core loop**, and nothing else:
  **The Mines** (do the security work) → **The Foundry** (mint/forge the reward onto the chain) → **The Ledger** (record who earned what, forever) → **The Vault** (the treasury/sink) → **The Watch** (secure & audit the chain).
- **Tone: warm Pixar.** Emotion + gentle humor, characters with real flaws, hopeful and cinematic, **never dystopian, never a lecture.** A child and an adult should both enjoy it. The blockchain meaning should *emerge* from the world, never be explained like a whitepaper.
- **It must feel ancient, alive, and reverent** — a secret subterranean civilization that has stood for ages and is still quietly at work, discovered rather than built.

## 3. The aesthetic target

- **Palette:** warm **sepia / amber / gold over deep near-black**. Candlelit, dim, light *pooled* in shadow. One coherent warm key.
- **Materials & light:** real carved wet stone, aged brass, glass crystal, molten metal; **volumetric god-rays, drifting dust, soft haze**; bloom on the warm sources.
- **Register:** **painterly-photoreal and cinematic** (35mm film feel), grounded and believable — **not cartoon, not anime, not bright, not over-saturated.**
- **Emotional beats:** *arrival* (a shaft of daylight into the dark), *first sight* (a vast hall that makes you stop and stare), then the quiet reverence of the Ledger and the Vault.

## 4. The cast (the brand layer)

- **Dr. Mineral** — a small red squirrel, the humble keeper & secret founder of the lab. Curious, collaborative, flawed, never about treasure/fame/power: *"I don't collect treasure. I collect discoveries."* The warm face on a serious system.
- **The assistant** — a small glowing **teal sprite-wisp** that drifts beside him (a warm/cool accent; currently 3D geometry in the world).
- **Tally** — magpie apprentice (quick, clever). **Vellum** — ancient tortoise, Keeper of the Ledger (solemn, sacred). **Castor** — beaver smith of the Foundry (strong, industrious). **Sasha** — meerkat sentinel of the Watch (still, vigilant). **Worker squirrels** — the mining/hauling crew.

## 5. What is built right now

**A. The landing page** (`site/index.html`)
- Hero = the coin's mission over a cinematic central-cavern render; a tagline introduces Dr. Mineral as the under-the-hood keeper.
- "What we're building" = the **core-loop cards** (Mine→Forge→Record→Sink→Guard), each now carrying its real scene art, plus the system's must-haves (reward genuine work, resist gaming/Sybil/collusion, real sink, audited).
- "The Architects" = the real team (**names are CONSENT-GATED — do not treat any names as public; flag if they appear publicly**).
- A free-roaming Dr. Mineral mascot perches/leaps across the page.

**B. The 3D world** (`site/world/index.html`) — *the product.* Three.js over CDN. Must be served over http for textures.
- A large carved cavern: tiered colonnaded galleries, a central well, a **visibly glowing golden chain**, a deep **forge ember**, fog, bloom, PBR stone, hundreds of warm lamps.
- A **cinematic intro** (campus video → a 3D camera move into the underground) with a continuous music score.
- **Click-to-focus zones** for the five districts (camera flies to each; a panel explains it in plain language).
- The **cast as animated 2.5D billboard sprites** — *just upgraded* from rough cutouts to **painterly keyed characters with per-state frame animation**: Dr. Mineral patrols (idle↔walk), miners swing a real wind-up→strike mine cycle, haulers walk a 2-frame carry between Mines and Foundry, Tally flicks her wings, Vellum keeps the Ledger. Plus set-dressing: rising forge embers, hanging lamps, drifting motes along the chain, mine dust, crates, support timbers, workstations.

**C. Assets**
- **18 cinematic stills** generated in Nano Banana (Gemini): 7 character portraits/poses + 11 scenes (central-cavern, descent, the five districts, campus). Warm, painterly, consistent. In `assets/characters/` and `assets/environments/nb/`.
- **12 keyed character sprites** (transparent, normalized) in `assets/sprites/`.
- **Music:** an interim soft cue ("Hidden Wonders", CC BY) — flagged as not yet "fresh/quality"; a custom track is planned.

**D. Teaser (in progress, not done)**
- A **free pipeline** proven end-to-end: NVIDIA FLUX (free stills) → HuggingFace LTX-Video (free image-to-video) → ffmpeg/edit, to be cut with real UNL campus footage + music. Currently **blocked on a daily free-GPU quota**; a paid path (fal/Seedance) is available but not activated.

## 6. The experience we are chasing (so the reviewer knows the bar)

1. **"Stop and stare."** The first frame — landing hero and the world reveal — should hit with awe and warmth.
2. **A world that is alive.** It should feel perpetually *at work*, not a diorama. Characters move with weight and intention; the chain grows; the place breathes.
3. **Charming but credible.** It's whimsical *and* it's a real security-reward system run by a university lab — it must not feel like a toy or a cartoon gimmick.
4. **Cohesion.** Landing, world, sprites, and scene art should read as **one world** — one palette, one fidelity, one light. (Known tension to judge: **painterly 2D art vs real-time WebGL 3D** living in the same frame.)
5. **The story emerges.** Without reading a whitepaper, a visitor should *feel* "work → mint → record → secure" and warm to Dr. Mineral.

## 7. How to view it

- **Live:** https://mohanendrasidda.github.io/dr-mineral-universe/ (landing) and `…/site/world/index.html?intro=1` (the 3D world with the intro). The whole repo is **public** on GitHub.
- **Local (best for the world; needs http for textures):** from the repo root run `python3 -m http.server 8011`, then open `http://127.0.0.1:8011/site/index.html` and `http://127.0.0.1:8011/site/world/index.html`.
- **Where to look:** the landing hero + core-loop cards; then the 3D world — the cavern reveal, the five districts (click each), and especially **the characters up close** (do the new sprites sit in the world, or look pasted-on? are the walk/mine cycles believable? is the scale/lighting/brightness right?).

## 8. What to evaluate — please report on each

Give an honest, specific read (what works, what doesn't, why) on:
1. **First impression** — does the landing + world reveal achieve "stop and stare"? Where does it fall flat?
2. **Visual cohesion** — do landing, world, sprites, and scene art feel like one world? Call out the painterly-2D-vs-WebGL-3D tension specifically: is it jarring, and how would you reconcile it?
3. **The living world** — does the 3D scene feel perpetually alive and *working*? Is there enough motion/life, or does it feel static/empty? Is the sense of scale/awe there?
4. **Characters & animation** — do the keyed painterly sprites read at world scale and lighting? Believable walk/mine/idle? Right size, brightness, grounding (shadows)? Do they belong in the scene?
5. **Narrative clarity** — without prior context, can you tell this is a blockchain reward for security work? Does Mines→Foundry→Ledger→Vault→Watch communicate? Is Dr. Mineral charming and the tone right (warm, not preachy, not toylike)?
6. **Landing page** — hierarchy, copy, the core-loop section, credibility. Does it make you want to "enter the lab"?
7. **Interaction & navigation** — is exploring the world intuitive (camera, click-to-focus, the intro)? Friction points?
8. **Performance & polish** — load time, smoothness/framerate, mobile, and obvious rough edges.

## 9. Known gaps / in progress (don't re-flag these as new)

- **Teaser** not cut yet (free-GPU quota timer; paid path not activated).
- **Castor & Sasha** are designed but **not yet placed** in the 3D world.
- **Dr. Mineral has only one walk frame** (procedural motion fills the gap); a second pose is pending.
- **Sprite scale/tint** are first-pass and explicitly open to tuning.
- **Music** is an interim track; a custom score is planned.
- **Coin specifics, bounty/reward winners, the "Hall of Contributors"** are future, not built.
- **Team names are consent-gated** and must not be made public without consent.

## 10. What we want back from you (the reviewer)

A structured write-up:
- **"How it looks/feels right now"** — a vivid, honest narrative walk-through of the actual experience (landing → world → characters), section 8's dimensions woven in, with concrete observations (not generic praise).
- **A prioritized improvement list** — the top changes that would most raise quality, each tagged by impact (high/medium/low) and rough effort, and by area (art, 3D scene, animation, copy, interaction, performance). Separate **"cohesion/identity"** fixes (make it feel like one world) from **"polish"** fixes.
- **The single highest-leverage next move**, in your view, and why.

Be candid and specific. The goal is the most believable, alive, cohesive version of this world — we would rather hear the hard truths than be reassured.
