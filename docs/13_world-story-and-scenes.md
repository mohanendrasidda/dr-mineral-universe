# The Lab — World Story, Scenes & Atmosphere

The narrative and mood bible for the explorable 3D world (`site/world/`). **This is the corrective:** the prototype drifted into a bright, bouncy, comedic mining game — "as if a noob built it." That is wrong. This place is **ancient, hidden, mysterious, and quietly alive.** Everything — lighting, motion, scale, sound, pacing — serves *awe and secrecy*, not fun-and-antics. Read this before touching the world's art or animation.

---

## 1. What this place IS (the one-paragraph truth)
Beneath an ordinary university, in the dark, there is a place that should not exist: a vast underground lab that has been running quietly for longer than anyone above has been alive. It does one thing, with total devotion — it takes the real work people do to keep the world secure (the bugs found, the audits written, the protocols hardened), and it **mines it, forges it onto an unbreakable chain, remembers it forever, keeps its value safe, and guards it.** You have found your way in. You are one of very few who ever have. The lab does not perform for you. It simply continues its ancient, patient work in the warm dark, and lets you witness it.

**The feeling we are building:** *"I have discovered something extraordinary and secret, and it has been here all along."* Wonder. Reverence. A held breath. Not a giggle.

## 1b. Visual target — REALISTIC 3D (not stylized)
**As real as it can be. Not Pixar, not anime, not cartoon.** Real materials (rough wet stone, aged brass, glass crystal, molten metal), real dramatic light, real depth and fog. The realism is what sells "this is a real, hidden place."
- **Environment = genuinely achievable in real 3D** (PBR materials, dramatic dim lighting, fog/depth, real glass/metal, even real-geometry props via image-to-3D for static rocks/crystals/machinery — no rigging needed). This is where realism is built, and it carries the whole mood.
- **Characters = the honest limit.** Realistic *animated* 3D creatures need modeling+rigging (artist/paid) — free tools can't. **In this dark register that's a feature:** keep figures small, distant, and in shadow — silhouettes and forms at work in the gloom. Darkness hides model fidelity and *deepens* the mystery. Detailed realistic character models are a later, paid/artist step if ever needed.

## 2. The mood, in one line each (the tone lock)
- **Ancient, not new.** Worn stone, old brass, centuries of patient work. Nothing feels freshly-built or game-like.
- **Vast and deep, not small and flat.** You sense a city falling away into darkness, not a little arena.
- **Dim, with warmth pooled in the dark.** Light is rare and precious — lamps, crystal-glow, the forge, the shaft from above. Most of the world is shadow you want to lean into.
- **Quietly alive, not busy.** Figures work with weight and purpose, slowly. The motion is *labor and ritual*, never bouncy or comic.
- **Mysterious, not explained.** There is always more in the dark than you can see. Sealed ways, deeper levels, a hum whose source you never quite find.
- **Sacred about the work.** Mining, forging, remembering — these are treated like rites, not chores.

> **Do NOT:** bright flat lighting · cartoon bounce/hops · jokey antics · fast jittery motion · "game HUD" clutter · cute idle wiggles. Those are what made it read as comedy.

## 3. The arrival (Scene 0 — The Descent)
You don't spawn into the lab. You **cross into it.** From the ordinary cool world above, a single shaft of pale daylight falls through a hole in the rock far overhead — the way in, the way it was found. You come down through that shaft into warmth and gold and depth. The air changes. The sound changes (a low hum rises to meet you). The first thing you feel is *scale* — the place is enormous, and it was here before you.

*Build implication:* open on the shaft-lit center, camera low and slow, the world revealed gradually out of darkness — not all-on-screen-at-once.

## 4. The first sight (Scene 1 — The Central Cavern)
The hub. From a high ledge you see it: galleries and bridges of dark stone falling away into a warm gold deep, lamps burning in their hundreds down into the dark, threads of light between them, a quiet that is full of meaning. Far below, the work goes on. **This shot must make the visitor stop and stare.** Dr. Mineral is here — small, still, watchful — the keeper. He does not wave. He simply is.

## 5. The five rites (the zones as scenes, not stations)
Each zone is a *scene with a mood*, a step in the one ancient process. Reframe every one away from "game station" toward "rite witnessed in the dark."

| Zone | What it truly is | What you SEE & FEEL (mysterious register) |
|---|---|---|
| **The Mines** | Where real work is dug from the dark | Figures working a glowing crystal seam in deep shadow — slow, heavy, rhythmic. Not "cute miners hopping"; *labor in a sacred dark*. Glow only from the crystal and a few lamps. |
| **The Foundry** | The heart — where work is forged onto the chain | A great forge breathing like a slow heart, deep orange light pulsing up the walls. Sparks fall slowly. Figures move in time with it. Fire and rhythm; an industry that feels *old and holy*. |
| **The Ledger** | Where everything is remembered, forever | The quietest, most reverent place — a long chain of soft light running back into the dark, each link a contribution kept. Cool, still, almost a shrine. This is where the wonder lands. |
| **The Vault** | The kept value, guarded | Deep blue, cold, silent. A single treasure under light. The sense that what is here matters more than anything, and is watched. |
| **The Watch** | Vigilance in the dark | Eyes in the shadow at the edges. Stillness, not action. The feeling of being *kept safe by something patient and unseen*. |

## 6. The keeper (Dr. Mineral, in this register)
Not a mascot doing bits. He is the **quiet keeper** of an ancient place — humble, watchful, present. He moves rarely and with meaning. When the visitor arrives, he notices, and that's all. His warmth is in stillness and attention, not antics. (His comedy/flaws live in the *story/novel*, not in the atmosphere of the world.)

## 7. The atmosphere bible (how to actually build the feeling)
- **Lighting:** dim base; light as rare warm pools (lamps, crystal, forge, the shaft) in a deep dark. Strong shadow. The eye is led by light, zone to zone. (We have env-map/bloom/shaft already — push *darker and moodier*, not brighter.)
- **Motion:** **slow everything down.** Workers move with weight — slow lifts, long pauses, breathing labor. Cut the bob amplitude; lengthen the cycles. No fast hops. Idle = stillness with the faintest life, not wiggling.
- **Scale & depth:** add the sense of a city *below* — galleries/levels falling away, distant lamps, fog depth. The single floor reads as small; depth reads as mystery.
- **Camera:** slow, heavy, cinematic. Gentle drift. Reveal, don't present. Let darkness hold parts of the frame.
- **Sound (future):** one low ambient hum, the forge's slow beat, distant water, a rare chime. Silence is part of it. (No chirps.)
- **Pacing:** calm. The world is patient. Nothing rushes. The visitor slows down to match it.
- **UI:** minimal and quiet. Less "BLOCKS FORGED" arcade counter, more a single restrained line. Let the place speak.

## 8. What this means for the current build (the re-tone checklist)
1. **Darker, deeper:** lower exposure/ambient further; let zones be islands of light in black.
2. **Slow the cast way down:** longer, weightier cycles; kill the cartoon bob; idle = near-still.
3. **Add depth below the floor:** suggest galleries/levels falling away (even faked) so it reads as a city, not an arena.
4. **Reverent worker behavior:** mining = slow heavy strikes with pauses; hauling = a slow trudge; not a brisk shuttle.
5. **Quiet the UI** toward atmosphere.
6. **Camera:** slower drift; open on the shaft; reveal gradually.
7. Then — and only then — **frame-animate** to this mood (slow, weighty walk/work cycles), per the frame briefs.

This document is the brief. Every render, frame, light, and motion choice answers to Section 2's tone lock.
