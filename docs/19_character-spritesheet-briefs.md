# Character sprite-sheet briefs (walk / work / idle cycles)

Goal: replace the gliding billboards with real **walk + "always-working"** motion, kept exactly on-model, performant for a whole crew. We play these as **UV-flipbook sprites** (player already built in `site/world/index.html`: `sheetSprite()` / `tickSheet()`).

## How to generate (free/low-cost web tools)
Upload the character's existing keyed render + the brief to one of: **AutoSprite** (autosprite.io), **Spritesheets.ai** (spritesheets.ai/walk-cycle-spritesheet), or **Layer.ai**. (Track A is researching a fully-free, terminal-automatable path; if found, I'll generate these myself.)

## Format spec (IMPORTANT — keep identical across all sheets)
- **One transparent PNG per cycle**, a single **horizontal strip**: `cols × 1` (e.g. a 6-frame walk = 6 frames wide, 1 tall).
- **Side profile**, facing **right** (the engine mirrors for left automatically).
- **Each frame square and the same size**; character **centered**, **feet on the bottom edge** (consistent baseline so it doesn't bob-jump).
- Even spacing, no labels/grid lines, clean alpha.
- Loopable: last frame flows back into the first.
- Keep the character **on-model** — same colors/proportions/silhouette as the source render.

Name them: `assets/sprites/<char>-<cycle>.png` (e.g. `drmineral-walk.png`).

## Per character

### Dr. Mineral — keeper squirrel  (source: `assets/keyed/char-drmineral-hero-v1.png`)
- **walk** — 6 frames, calm confident overseer's stroll, tail counter-swaying, slight head turn. `drmineral-walk.png`
- **idle** — 4 frames, standing, breathing, tail flick, occasional glance. `drmineral-idle.png`

### Worker squirrels — miners & haulers  (source: a worker render, or recolor Dr. Mineral)
- **walk** — 6 frames, purposeful hauling walk (carrying weight, slight forward lean). `worker-walk.png`
- **mine** — 6–8 frames, a real swing: wind up → strike a seam with a pick/paws → recoil → reset. `worker-mine.png`
- **idle** — 4 frames. `worker-idle.png`

### Tally — magpie  (source: `assets/keyed/char-tally-v1.png`)
- **idle/hop** — 6 frames, perched, head bobs, wing shuffle, the odd hop. `tally-idle.png`

### Vellum — tortoise  (source: `assets/keyed/char-vellum-v1.png`)
- **walk** — 6 frames, slow heavy plod (legs cycling, shell steady). `vellum-walk.png`

## Wiring (once a sheet exists)
```js
const drM = sheetSprite('../sprites/drmineral-walk.png', 6, 1, 2.0, {fps:8, frames:6});
// in the loop, when moving: tickSheet(drM, dt);  (set drM.userData.facing = ±1 for direction)
```
The flipbook batches to VRAM once and only changes the atlas offset per frame → a full crew stays at 60fps (video-texture sprites would not).
