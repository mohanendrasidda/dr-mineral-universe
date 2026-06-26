# Asset Prompt Pack & Handoff (v2)

Paste-ready prompts per AI tool, and exactly how to hand results back so I can integrate them. Generate in **priority order** (top unblocks the most). Consistency anchor and canon from `05_hero-portrait-brief.md`, `../canon/visual-canon.md`.

---

## 0. HOW TO HAND BACK (do this and I take it from there)
**Save into the repo with these names, then just tell me the filenames (or "dropped them").**

| Kind | Save to | Name like | Background |
|---|---|---|---|
| Character (I will key it) | `assets/raw/` | `char-<who>-v1.png` (e.g. `char-drmineral-hero-v1.png`, `char-tally-v1.png`) | **flat solid grey #777 or flat blue** (NOT green, NOT transparent) |
| Environment / scene | `assets/environments/` | `env-<slug>.png` (e.g. `env-central-cavern.png`) | full painted scene (no keying) |
| Website UI mock (Figma/Claude) | share link, or export to `site/mocks/` | `mock-<page>.png` / `.html` | — |
| Text (ChatGPT style bible etc.) | paste to me, or save `docs/` | `08_<thing>.md` | — |

**Format:** PNG, biggest resolution the tool allows. Generate **4 variants** for hero/characters so we can pick. After you drop characters, I run the keying pass → transparent PNGs in `assets/keyed/` → into the site + character sheet.

---

## 1. NANO BANANA (Gemini) — CHARACTERS ⭐ priority 1
Best at consistency; this is our established pipeline. **Always paste the anchor first**, then the shot. Flat keyable background. Generate 4 variants each.

> **CONSISTENCY ANCHOR (paste at the top of every character prompt):**
> The same squirrel character across all images: warm 3D Pixar-style render, reddish-brown fur, cream/pale belly, large expressive intelligent eyes, a small dark nose, and an oversized bushy tail curving upward behind him. He holds a single acorn. Friendly, humble, curious expression. Consistent character, same proportions every time.

### 1a. Dr. Mineral — hero portrait (THE unblocker)
```
[paste anchor] — SHOT: seated or standing, relaxed three-quarter view, holding the
acorn in both forepaws near his chest, looking slightly off-camera with a thoughtful,
kind expression. Dignified but warm — a scientist's calm curiosity, not a cartoon
mascot. He looks like an ordinary squirrel with an unusual spark of intelligence.
No costume, no lab coat, no glasses, no gadgets. CAMERA: eye-level, portrait framing,
head-and-body, negative space above. LIGHTING: warm cinematic key from upper left,
soft rim light separating the tail. BACKGROUND: flat solid neutral mid-grey (#777)
or flat blue — NOT green, NOT a checkerboard, NOT a scene.
NEGATIVES: no chain, no rope, no leash, no text, no logo, no watermark, no UI, no
clothing, no extra animals, no human objects.
```

### 1b. Tally — the magpie apprentice (co-lead)
```
A young magpie, warm 3D Pixar-style render to match the Dr. Mineral squirrel's style
and lighting. Black-and-white plumage with a hint of blue iridescence, a tail not yet
fully grown, bright curious intelligent eyes, eager and a little brave. Standing
upright, chin up, mid-question. No clothing, no props. LIGHTING: warm cinematic key
from upper left, soft rim light. BACKGROUND: flat solid mid-grey #777 or flat blue.
NEGATIVES: no chain, no text, no logo, no watermark, no UI, no human objects.
```

### 1c. Vellum — the ancient tortoise Keeper
```
An ancient giant tortoise, warm 3D Pixar-style render matching the established
lighting. Vast, grey-green, deeply seamed shell and skin like a dry riverbed, immense
age and patience, kind tired eyes that have watched centuries. Calm, venerable,
gentle. No clothing, no props. LIGHTING: warm cinematic key upper left, soft rim
light. BACKGROUND: flat solid mid-grey #777 or flat blue.
NEGATIVES: no chain, no text, no logo, no watermark, no UI, no human objects.
```
*(Same pattern for June Ringtail/raccoon, Master Castor/beaver, etc. — ask me and I'll write them.)*

---

## 2. NANO BANANA or CHATGPT — CINEMATIC ENVIRONMENTS ⭐ priority 2
Full painted scenes (no keying). These become the website's hero sections and the animation backdrops. **Shared style line — paste into each:**

> **ENV STYLE:** warm 3D Pixar/Disney-quality cinematic render, volumetric golden lamplight, deep atmospheric perspective, rich painterly detail, hopeful and wondrous (never dystopian), 16:9, no text, no watermark, no people-signage.

### env-first-descent
```
[ENV STYLE] POV at a threshold: an ancient counterweighted stone door swinging
inward in a campus wall, revealing a worn spiral stone staircase descending into warm
golden light. Small lamps set into the curving wall glow softly. Warm air and dust
rising from below. The steps are dished and polished by centuries of small feet.
Sense of crossing from an ordinary cool world into an extraordinary warm one.
```

### env-central-cavern  ⭐ the money shot
```
[ENV STYLE] An enormous underground research city seen from a high stone landing — an
inverted cathedral-city falling away into the deep: galleries, bridges, balconies of
dark stone and pale wood, level upon level, thousands of soft golden lamps glowing all
the way down, threads of green growing on columns, distant rivers, faint mist.
Breathtaking scale, the very first sight of a hidden civilization. Wondrous, alive.
```

### env-chain-foundry
```
[ENV STYLE] A vast underground forge-hall, a great central reactor-forge pulsing like
a glowing heart, casting molten gold light up the walls. Order under pressure: forging
links of a glowing chain. Heat-shimmer, sparks, rhythm. The engineered heart of the
laboratory. (Blockchain as craft, never as text or symbols.)
```

### env-crystal-tunnels
```
[ENV STYLE] Mechanical mining squirrels (charming brass-and-wood robots) moving in a
line through glowing crystal tunnels deep underground, veins of luminous crystal in
the rock, small journal-drones drifting overhead carrying papers. Wonder and motion.
```

### env-hall-of-contributors
```
[ENV STYLE] A vast domed hall whose ceiling is a constellation of shimmering golden
stars, each a point of light honoring a contribution, linked by faint glowing threads
into a great chain of light. Reverent, beautiful, moving. New stars kindling.
```

---

## 3. CHATGPT — STYLE BIBLE + COLOR SCRIPT (its best role here)
Nano Banana wins on character consistency, so give ChatGPT the *art-direction* job + alternate environment takes. Paste:
```
You are the art director for "The Dr. Mineral Universe," a warm Pixar-quality animated
world: an underground research civilization of intelligent animals beneath an ordinary
campus, led by a humble squirrel scientist. Tone: hopeful, cinematic, wondrous, never
dystopian; technology glows but never shouts. Produce: (1) a COLOR SCRIPT — 8 sequential
mood frames from "ordinary campus morning" to "first sight of the central cavern,"
each with palette (hex), lighting, and emotion; (2) a one-page STYLE BIBLE — palette,
lighting rules, material language (warm stone, brass, pale wood, glowing crystal,
gold lamplight), and 5 do/don't rules. Text only, tight and usable.
```
Hand back as `docs/08_style-bible.md` (paste it to me and I'll save/clean it).

---

## 4. CLAUDE / FIGMA (Claude Design) — WEBSITE UI ⭐ priority 3
Turn the concept into real UI. Brief:
```
Design the homepage + one district page for "The Dr. Mineral Universe" — an explorable,
living website for an underground research civilization beneath an ordinary campus.
Dark-premium aesthetic, warm gold lamplight accents, Fraunces (display) + Spectral
(body) typography. HOMEPAGE: a campus-surface hero with MULTIPLE entrances (stone wall,
tree roots, storm drain, etc.) that each lead to a different district; below, a "Central
Cavern" reveal; a "TODAY IN THE LAB" live feed; a district atlas grid of cards (each =
a website feature) with public/member/restricted tags; a version slider showing the lab
grow (v1 → v25). DISTRICT PAGE: hero image slot, the lead character, "what they make,"
and the mapped feature. Reference structure: the repo's concept at scratch/universe-
concept.html and canon/district-atlas.md.
```
Hand back: the published link, or export PNGs to `site/mocks/`.

---

## Priority recap
1. **Dr. Mineral hero portrait** (1a) — unblocks the site hero + character sheet. Do this first.
2. **env-central-cavern + env-first-descent** (2) — the two hero backdrops; unblock the landing page + the Remotion teaser's real frames.
3. **Tally + Vellum** (1b/1c) — the cast.
4. **Style bible / color script** (3) and **UI mocks** (4) — parallel, anytime.
