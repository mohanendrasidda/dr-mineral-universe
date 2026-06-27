# Dr. Mineral teaser

A ~43s cinematic teaser for **The Lab Reward Coin** — real cinematic footage mixed with the Gemini HD lab stills, one warm grade, over the score.

**Output:** `teaser/teaser.mp4` (committed) · also copied to `~/Downloads/dr-mineral-teaser.mp4`.

## The cut
1. **Lincoln at dusk** (real aerial) — "An ordinary city."
2. **UNL campus** (real aerial) — "A quiet campus. Nobody looks twice."
3. **Golden forest god-rays** (real stock) — "The world above."
4. **Descent** (our LTX clip) + dust — "But beneath it,"
5. **The reveal** (Gemini central-cavern still) + real dust motes drifting in the shaft — "a lab has worked for ages."
6. **Crystal macro** (real stock, warm-graded) + sparks — "carved from the rock —"
7. **The five districts** (Gemini stills) — Mines & Forge with real **embers** rising through them, Ledger/Vault/Watch with drifting **dust**; each labeled (MINE / FORGE / RECORD / VAULT / GUARD).
8. **Dr. Mineral** — "I don't collect treasure. I collect discoveries."
9. **CTA** — *The Lab Reward Coin · a coin for real security work.*

The "mix and match" technique: real **embers/dust/sparks on black** are *screen-blended* over the painterly stills, so the static HD renders come alive with moving light and particles — no AI-animation of the stills required.

## Rebuild
```bash
cd teaser
../scripts/teaser-fetch-footage.sh   # (re)download the free stock clips
../scripts/teaser-stage-assets.sh    # copy stills/clips/score into public/
npx remotion render DrMineralTeaser out/teaser.mp4
```
`teaser/public/` (heavy, reproducible) and `teaser/out/` are gitignored.

## Footage sources & licenses  (clear before any public launch)
- **Lincoln-at-dusk + UNL-campus aerials** — `assets/video/footage/{lincoln-dusk,unl-campus-aerial}.mp4` (Sidd-provided; confirm origin/clearance + UNL Comms sign-off for public use of UNL imagery).
- **Stock clips** (all royalty-free, commercial-OK, no attribution required):
  - Cave god-rays, mist, forest god-rays, molten metal, fire embers, sparks — **Mixkit Free License** (mixkit.co).
  - Dust motes in sunbeam, clear-crystal macro, candle flame — **Pexels License** (pexels.com).
- **Lab stills** — Gemini / Nano Banana renders (`assets/environments/nb/`). **Descent clip** — our own LTX-Video generation.
- **Score** — "Hidden Wonders", Kevin MacLeod (CC BY 4.0) — keep the credit, or swap to a custom track.
