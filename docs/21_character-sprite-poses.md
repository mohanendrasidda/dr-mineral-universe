# Character sprite poses — clean solo PNGs for the 3D world

Generate each as a **separate PNG** in Nano Banana. I'll rembg them to transparent and wire them as per-state animation frames (idle / walk / mine).

## Rules for EVERY pose (this is what makes them usable as sprites)
- **Side profile, facing RIGHT.** Full body, centered, **feet exactly on the bottom edge**. (Engine mirrors for left.)
- **Plain flat pale-grey studio background** — no scene, no cast shadow, no vignette. (Clean silhouette = clean cutout.)
- **Evenly + clearly lit** (soft warm key + gentle rim) so every part reads — NOT the dark moody scene lighting.
- **Same scale & framing across all poses of a character** so the frames line up when animated.
- **On-model:** warm painterly-realistic, grounded. **Use a reference image** so the character stays identical across poses.
- Square, no text, no watermark.

**Reference for consistency:** use `assets/characters/drmineral-keeper-walk.png` as the Dr. Mineral reference; for workers, generate `worker-idle` first then reference it for the rest.

**Anchors (baked into each prompt below):**
- **DR. MINERAL:** the same red squirrel — warm russet-orange fur, large bushy tail, bright dark eyes, worn earthy keeper's coat + apron.
- **WORKER:** a red squirrel worker — russet-orange fur, bushy tail, simple worn leather work apron, sturdy.

---

## Dr. Mineral (the keeper — idle + 2 walk frames)

**`drmineral-idle.png`**
> The same red squirrel Dr. Mineral (warm russet-orange fur, large bushy tail, bright dark eyes, worn earthy keeper's coat and apron), standing relaxed in side profile facing right, holding a small brass lantern at his side, calm and watchful, weight balanced. Clean full-body character sprite, side profile facing right, centered with feet exactly on the bottom edge, plain flat pale-grey studio background, no scene, no cast shadow, evenly and clearly lit with soft warm key and gentle rim light, warm painterly-realistic, crisp silhouette, no text, no watermark, square.

**`drmineral-walk-a.png`**
> The same red squirrel Dr. Mineral, side profile facing right, mid-stride walking — near leg forward and planted (contact pose), far leg back, brass lantern swinging in one paw, slight forward lean. Clean full-body character sprite, side profile facing right, centered, feet on the bottom edge, plain flat pale-grey studio background, evenly lit, warm painterly-realistic, crisp silhouette, no text, no watermark, square.

**`drmineral-walk-b.png`**
> The same red squirrel Dr. Mineral, side profile facing right, mid-stride passing pose — legs crossing under the body, the opposite paw forward, body lifted slightly at the top of the step, tail counter-swaying. Clean full-body character sprite, side profile facing right, centered, feet on the bottom edge, plain flat pale-grey studio background, evenly lit, warm painterly-realistic, crisp silhouette, no text, no watermark, square.

---

## Worker squirrel (miners + haulers — idle + 2 walk + 2 mine frames)

**`worker-idle.png`**
> A red squirrel worker (russet-orange fur, bushy tail, simple worn leather work apron, sturdy), side profile facing right, standing, a small pick resting on the shoulder, earnest. Clean full-body character sprite, side profile facing right, centered, feet on the bottom edge, plain flat pale-grey studio background, evenly lit, warm painterly-realistic, crisp silhouette, no text, no watermark, square.

**`worker-walk-a.png`**
> A red squirrel worker (worn apron), side profile facing right, mid-stride walking and carrying weight — near leg forward and planted, leaning forward, paws low as if hauling. Clean full-body character sprite, side profile facing right, centered, feet on the bottom edge, plain flat pale-grey studio background, evenly lit, warm painterly-realistic, crisp silhouette, no text, no watermark, square.

**`worker-walk-b.png`**
> A red squirrel worker (worn apron), side profile facing right, mid-stride passing pose — legs crossing under the body, the other leg forward, body lifted slightly. Clean full-body character sprite, side profile facing right, centered, feet on the bottom edge, plain flat pale-grey studio background, evenly lit, warm painterly-realistic, crisp silhouette, no text, no watermark, square.

**`worker-mine-a.png`**  *(wind-up)*
> A red squirrel worker (worn apron), side profile facing right, winding up to swing a pickaxe — pick raised high above and behind the head, body leaning back, both paws gripping the handle, ready to strike. Clean full-body character sprite, side profile facing right, centered, feet on the bottom edge, plain flat pale-grey studio background, evenly lit, warm painterly-realistic, crisp silhouette, no text, no watermark, square.

**`worker-mine-b.png`**  *(strike)*
> A red squirrel worker (worn apron), side profile facing right, mid-strike with the pickaxe swung down and forward hitting the ground in front, body bent forward at the moment of impact, both paws low on the handle. Clean full-body character sprite, side profile facing right, centered, feet on the bottom edge, plain flat pale-grey studio background, evenly lit, warm painterly-realistic, crisp silhouette, no text, no watermark, square.

---

## Tally — the magpie apprentice (idle + hop)

**`tally-idle.png`**
> The same small magpie Tally (glossy black-and-white feathers, blue iridescent wing-sheen, bright clever eyes), side profile facing right, perched, wings folded, head up and alert. Clean full-body character sprite, side profile facing right, centered, feet on the bottom edge, plain flat pale-grey studio background, evenly lit, warm painterly-realistic, crisp silhouette, no text, no watermark, square.

**`tally-hop.png`**
> The same small magpie Tally, side profile facing right, mid-hop — wings half-open, one foot lifted, leaning forward, lively. Clean full-body character sprite, side profile facing right, centered, feet on the bottom edge, plain flat pale-grey studio background, evenly lit, warm painterly-realistic, crisp silhouette, no text, no watermark, square.

---

## Vellum — the tortoise, Keeper of the Ledger (idle + 2 walk)

**`vellum-idle.png`**
> The same ancient anthropomorphic tortoise Vellum (worn mossy shell with faint carved glyphs, scholar's mantle, wise hooded eyes), side profile facing right, standing upright and still, holding a small stone tablet, patient and solemn. Clean full-body character sprite, side profile facing right, centered, feet on the bottom edge, plain flat pale-grey studio background, evenly lit, warm painterly-realistic, crisp silhouette, no text, no watermark, square.

**`vellum-walk-a.png`**
> The same tortoise Vellum, side profile facing right, slow heavy plod — near foot forward and planted, body low and deliberate. Clean full-body character sprite, side profile facing right, centered, feet on the bottom edge, plain flat pale-grey studio background, evenly lit, warm painterly-realistic, crisp silhouette, no text, no watermark, square.

**`vellum-walk-b.png`**
> The same tortoise Vellum, side profile facing right, slow plod passing pose — the other foot forward, weight shifting, shell steady. Clean full-body character sprite, side profile facing right, centered, feet on the bottom edge, plain flat pale-grey studio background, evenly lit, warm painterly-realistic, crisp silhouette, no text, no watermark, square.

---

## Deliver
Save all as `assets/sprites/<name>.png` (names above). Tell me when they're in — I'll rembg them to transparent and wire **per-state frame animation** (idle / walk two-frame / mine two-frame) into the world's sprite system, replacing the current single-image billboards. *(Optional later: Castor the beaver at the Foundry, Sasha the meerkat at the Watch — same format — if you want them placed in the world too.)*
