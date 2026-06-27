# The Lab — World QA & Motion Report (for the implementing agent)

**Scope:** live visual + motion inspection of `site/world/index.html` (the 3-D world), focused on the 3-D Dr. Mineral integration, the cinematic follow-cam, and overall scene behavior. Method: loaded the page over local http, captured ~5 frames across ~35 s to read motion (patrol, camera glide, color consistency), checked the console.

**Headline correction:** an earlier pass mistakenly reported Dr. Mineral as "warm russet." That was a misread — the russet squirrel seen at the Mines in single frames is the **2-D miner *billboard***, not the 3-D model. The actual 3-D Dr. Mineral renders **pale cream (mannequin)**. The items below reflect the corrected reading.

---

## ✅ What is working

- **Camera framing & glide (cinematic):** pulled-back, slightly-high, rule-of-thirds framing reads well; the smoothed/eased heading (`camHeadX/Z` lerp) makes turns glide without snapping. This part is good — keep it.
- **World atmosphere:** the cavern (colonnaded well, arches, fog, hanging lamps, drifting coins, warm sepia palette) is strong and cohesive.
- **3-D pipeline is sound:** FBX loads, skeletal walk/idle blend, the model turns to face its travel tangent, the assistant orb follows. No console **errors** (only benign warnings: FBXLoader ">4 skin weights", UnrealBloom sigma).
- **Color *consistency*:** whatever color the 3-D model has, it is location-independent now (unlit) — so there's no black↔glow flicker. The problem is the *value* of that color, not its stability.

---

## 🔴 Issues, prioritized

### P1 — Dr. Mineral renders PALE CREAM, not russet (the recolor is effectively not applying)
- **Symptom:** the 3-D model is a uniform pale putty/cream — a "missing-texture mannequin." Tellingly, the flat **2-D miner billboard beside him is more vividly colored than the 3-D hero.**
- **Most likely root cause:** the voxel color-transfer (`recolorMesh`) is returning its **fallback color `[0.55,0.45,0.35]` for most/all vertices** — i.e. the source grid isn't being matched. After the warm/dim curve that fallback lands at exactly this pale putty. Candidates to check, in order:
  1. The source `drmineral_raw.glb` `COLOR_0` attribute isn't being read as expected by `GLTFLoader` (verify `src.geometry.attributes.color` exists and has non-grey values; log it).
  2. **Normalization misalignment:** the target (FBX bind pose) and source (GLB) are normalized by their own bboxes; if the **skinning-spike vertex** (see P1b) inflates the *target* bbox, all real vertices squash into a corner of normalized space and miss the grid → fallback everywhere. (The bind-pose clamp may not be removing the spike — see P1b.)
  3. Source colors are genuinely near-grey (InstantMesh is muted) and the warm curve isn't enough.
- **Recommended fix:** *first* make it reliable, *then* make it pretty.
  - **Reliable interim:** drop the per-vertex transfer and give him a **flat russet unlit material** — `new THREE.MeshBasicMaterial({ color: 0x9c4e22, fog:true })` (tune hue). Uniform warm russet, zero dependency on the fragile transfer. He loses fur/coat variation but reads correctly as a warm squirrel — acceptable at the cinematic distance.
  - **Proper fix (parallel):** debug the transfer with logging (does `ca` exist? how many grid voxels filled? does fallback fire?); ensure the spike is removed *before* the target bbox is computed; consider transferring by **nearest-neighbour on normalized, spike-free positions** rather than a coarse 40³ grid.

### P1b — Skinning "spike" artifact still present (reads as a staff across his body)
- **Symptom:** a thin straight pole crosses his torso from a hand outward — a classic stray vertex weighted to the hand/arm bone, stretched during animation. The current **bind-pose outlier clamp does NOT fix it** (it's weight-driven, so the bind pose looks normal).
- **Recommended fix options:**
  1. **Zero the bad skin weights:** scan `skin.geometry.attributes.skinWeight/skinIndex`; for vertices whose deformed position (compute via `SkinnedMesh.applyBoneTransform` / `boneTransform` once at bind+a test pose) lands far from neighbours, re-assign their weight to the nearest body bone (or clamp to the dominant weight). 
  2. **Cheaper:** detect the offending vertex by its **UV/position outlier** and weld it to a neighbour.
  3. **Cleanest long-term:** re-rig on a cleaner mesh (the queued **Hunyuan3D-2** mesh) — image-to-3-D meshes from a single photo often have one stray vert that Mixamo then stretches.

### P2 — Blank / soft face
- InstantMesh generated a featureless face from one photo. Not fixable in code. The cinematic distance hides it, but up close he has no eyes/expression. Mitigations: keep the camera at distance; try the **Hunyuan mesh**; or (later) a cleaner/commissioned model.

### P2 — Cast fidelity split
- A pale 3-D hero stands beside vivid 2-D russet billboard workers/magpie in the same frame — the billboards currently *out-class* the hero. Per the agreed plan, the cast must all move to 3-D (Tally, Vellum, a worker) so it stops reading half-and-half. Do NOT ship mixed.

### P3 — Patrol may not be advancing
- Across ~35 s of capture, Dr. Mineral stayed in/around the **Mines**; I did not observe him reach another district. Verify the orbit actually advances: check that `drMNext()` fires (watch → walk → next angle), that `drMWalking` toggles, and the per-segment speed. If he's effectively parked, the "always working / patrols the districts" promise isn't being met.

### P3 — Camera occasionally too top-down
- One frame was near-overhead (looking down the Mines shaft). The high angle is good in moderation but should be **clamped** (limit pitch) so it never tips into a flat top-down that loses the architecture and the character's silhouette.

### P3 — "Blocks forged" stayed 0 in my session
- The HUD counter read `0 / CHAIN 0` throughout (the forge-timer block→Ledger flyer drives it). Confirm the timer fires and the counter increments (a prior automated pass reported it reaching 2 — so this may be timing/seed; verify).

---

## Recommended order of work
1. **P1 recolor → flat russet now** (unblocks the look immediately), then debug the transfer.
2. **P1b spike** — zero the bad weight, or move to the Hunyuan mesh.
3. **P3 patrol** — confirm he actually circles the districts.
4. **P3 camera pitch clamp** + keep the (good) glide.
5. Then **convert the cast to 3-D** (Tally first) to end the fidelity split.

## Keep (don't regress)
- The cinematic framing + smoothed glide.
- The deterministic, location-independent material approach (just fix its *color value*).
- The world atmosphere and lighting mood.
