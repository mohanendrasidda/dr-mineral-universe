# WHAT WORKS — Dr. Mineral Universe (proven playbook)

A running record of what's **proven to work** so we never restart from zero.
Last major session: 2026-06-29.

---

## 1. Free 3D assets — Poly Pizza is the unlock ✅
- **Best source:** https://poly.pizza — models download as **direct `.glb`, NO login.**
- **Direct-download trick:** the model page `https://poly.pizza/m/<id>` embeds the real file at
  `https://static.poly.pizza/<uuid>.glb`. Extract it with:
  ```bash
  curl -sL "https://poly.pizza/m/<id>" | grep -oE 'static\.poly\.pizza/[a-f0-9-]{36}\.glb' | head -1
  ```
  then `curl -sL "https://<that>" -o name.glb`.
- **License:** Quaternius / Kenney / Kay Lousberg / iPoly3D / CreativeTrio = **CC0** (no credit).
  "Poly by Google" + most others = **CC-BY** (just credit the author).
- **Rigged + animated, CC0:** Quaternius `raccoon`, `rat`, `hedgehog` carry Walk/Idle/Run/etc.
- Downloaded cast lives in `assets/3d/free-models/`; web copies in `assets/3d/web/` and props in `assets/3d/web/props/`.

## 2. The living 3D world — `site/world/index.html` ✅
- **Run it:** `python3 -m http.server 8011` from repo root → `http://127.0.0.1:8011/site/world/index.html`
  (MUST be http — ES modules + textures).
- **`place3D(file,x,z,h,yaw,opts)`** loads a GLB: centers on bbox, drops to floor, scales to height `h`.
  Extended this session to support: **skeletal animation** (`opts.clip:'walk'` → AnimationMixer, ticked via `MIX[]`),
  **`opts.tint`** (recolour untextured models like the rat), vertex-colour sRGB fix, `opts.sat` saturation.
- **Animated workers:** raccoon miner (Mines), beaver (Foundry), hedgehog (Ledger), tortoise (Vault), weasel (Watch).
- **Haulers:** `hauler(file,seg,speed,blockColor,tint)` — critters that **walk the Mine→Foundry→…→Watch loop**
  carrying a glowing block; moved in the loop via `haulers[]`. This is the "world has action" movement.
- **Props:** `prop(file,x,z,h,yaw,opts)` = place3D under `props/` with no warm-clay floor. 24 CC0 props dress the districts.
- **Notice board, cavern, chain-ring, lighting, hero squirrel, particles = LEFT INTACT.** Only added on top.
- Swap plan: when custom models are ready, drop them in by filename — the stand-ins retire.

## 3. The teaser / Enter-the-Lab intro ✅
- Teaser **removed from the landing page** (`site/index.html`) entirely.
- It now plays as the **Enter-the-Lab intro** (`world/index.html?intro=1` → `startVideoIntro` → `../media/teaser-4k.mp4`).
- **No BEGIN gate** (plays straight through). Tries unmuted autoplay; muted-fallback unmutes on first interaction.
- **No overlapping audio:** `startSoundscape()` is blocked while `body.introvid` is set, so the world's music
  starts ONLY after the teaser ends/skips. The separate `intro-score.mp3` layer was removed (teaser carries its own audio).

## 4. The Dr. Mineral hero model — pipeline that runs ⚙️
- **Carve:** Hunyuan3D-2mv multiview → mesh. Runs on **CPU** on the 16GB Mac (`~/code/hunyuan-mac/carve_drmineral.py`),
  slow (preview ~2.5h; max 50-step run ~15h). GPU is the real path (RunPod / HCC Swan — applied, ~1-2 day wait).
- **Texture (CUDA-free, on Mac):** `~/dr-mineral-universe/scripts/bake_mac.py`. The fixes that MADE IT WORK:
  1. **Force a fresh Smart UV unwrap** — imported glb carried a degenerate placeholder UV → baked black until rebuilt.
  2. **`ShaderNodeAttribute`** (not `ShaderNodeVertexColor`) to read the `Col` vertex colours in Blender 5.1.
  3. **Manual PNG writer (numpy+zlib)** — Blender headless `img.save()` silently writes BLACK; bypass it and
     write the baked pixel buffer to PNG ourselves (sRGB-encode colour maps, raw for data maps).
  4. **Floater removal** — separate-by-loose, keep the largest part (the 2mv carve had 124 junk shards).
- **Render check:** `scripts/render_asset.py` (cinematic) and `scripts/render_gallery.py` (one thumb per glb in a folder).
- **Proven DEAD END (do not re-chase):** single/multi-image **photo-projection ghosts** (8 versions). Free image-to-3D
  tops out at "soft/doughy game prop"; clean topology needs **Tripo Pro (~$15)** or hand-sculpt in Blender.

## 5. Tooling that worked ✅
- **Headless WebGL screenshot (no GPU):** Chrome `--headless=new --use-gl=angle --use-angle=swiftshader
  --enable-unsafe-swiftshader --virtual-time-budget=NN --screenshot=out.png URL` — software WebGL, slow but real.
  For a fast/proper look just `open <url>` in the user's GPU browser.
- **JS sanity before testing:** `node -e "new Function(<inline script>)"` to catch parse errors (caught a dup `const`).
- **Blender headless:** `/Applications/Blender.app/Contents/MacOS/Blender -b -P script.py -- args`.
- **Inspect a glb's anims/colours:** import in headless Blender, list `bpy.data.actions` + `color_attributes`.

## 5b. Tools EVALUATED & parked (don't re-litigate) ⛔
Our world is **real-time Three.js meshes**, so the cast must be **riggable mesh** (carve → bake → Mixamo → glb).
Gaussian-splat & video-mocap tools only earn a spot for *offline cinematics* or *one bespoke hero move* — never the working cast.

| Tool | Output | Fits the animated world? | Revisit only when… |
|------|--------|--------------------------|--------------------|
| **TripoSplat** (VAST-AI) | Gaussian splats (.ply/.splat) | ❌ un-riggable, needs 2nd renderer, soft look clashes with toon world | a **static photoreal showpiece** (e.g. rotating hero statue) |
| **ComfyUI-MotionCapture** (GVHMR/SMPL) | human BVH from video | ⚠️ still needs retarget onto our rig + heavy GPU/SMPL-license setup, noisy monocular mocap | one **signature hero gesture** Mixamo lacks (e.g. "eureka") |
| **3DGS Render — KIRI** (Blender addon) | splats *inside Blender* (offline render) | ❌ offline only; doesn't reach Three.js; splats still un-riggable | rendering a splat into the **teaser** cinematic |

**Why splats lose for props too:** they bake their own appearance → won't take cavern torchlight/shadows/fog, and a "mirror" is a Three.js `Reflector` not an asset. **Use Poly Pizza CC0 meshes for furniture/props** (chair/table/mirror-frame/etc.) — same GLTFLoader, lit natively, free, instant.

## 6. Open threads
- MAX-quality Dr. Mineral carve running overnight → auto bake+render+push when done.
- HCC Swan GPU account applied (free, 48GB L40S) — the real path to a clean textured hero.
- Hero in the world is still the old melty `drmineral-color.glb` — swap when a clean carve lands.
- CC-BY assets need an attribution list before any public ship.
