# Research synthesis — Seedance, footage mixing, character animation (2026-06-27)

Three parallel research passes. Verdicts + a unified plan at the end.

## 1. Seedance (AI video) — YES, adopt it
- **Seedance 2.0 is currently #1** on the Artificial Analysis arena for **both** text-to-video and image-to-video (ahead of Veo 3.1, Kling 3.0). Its strengths — atmospheric cinematic lighting, golden-hour HDR, **dim cave/underground realism**, and multi-shot consistency — map almost exactly onto our campus→descent→ancient-lab teaser.
- **Image-to-video is its best mode** (the #1 I2V model): feed our drone frames / concept renders as input stills, animate them, and **chain clips via last-frame→next-first-frame handoff** for continuity.
- **Access:** prototype free on **Dreamina** (daily credits) to lock looks; produce via **fal.ai or Replicate API** (fits our Node/Python stack). Cost ≈ **$0.50–0.75 / 5s 1080p**, **$2.50 / 5s 4K**. A ~30–45s teaser of 8–10 clips ≈ **$5–25 total**. BytePlus gives 2M free tokens; fal/Replicate give trial credits.
- **Pick:** Seedance **2.0** for hero 4K shots; **1.0 Pro** (or Lite) for cheaper 1080p coverage.
- **Gotcha:** exact *recurring-character* consistency is Veo 3.1's edge — matters little for a mood-driven teaser. Mix our own audio; don't rely on native audio.

## 2. Footage sourcing + mixing — YES, mix-and-match is right
- **Premium backbone:** **Artgrid / Artlist** (~$30/mo) — cinematic, color-consistent, RAW/LOG so it color-matches our drone footage; Artlist also bundles the **music + LUTs** we need. Best single subscription.
- **Free + scriptable:** **Pexels + Pixabay** — free JSON APIs returning direct MP4 URLs; pull caves/tunnels/ruins fillers from a script. (The only two with real free APIs.)
- **Gap-fillers:** **Envato Elements** (cheap unlimited — temples, abstract blockchain/data) or **Pond5** (per-clip rare shots: mines, caverns).
- **Mixing (the real work is COLOR):**
  1. **Script-prep (ffmpeg + Pexels/Pixabay APIs):** download candidates, transcode everything to one **4K / 24fps / common-codec** normalized set.
  2. **Upscale** soft AI/HD clips with **Topaz Video AI** (temporal-coherent).
  3. **Grade in DaVinci Resolve (free):** color-managed project → normalize every source to one working space → **one shared creative LUT** → per-clip **Shot Match** → unify with shared grain/halation. This is what glues AI + real + stock into one look.
  4. **Cut to a music bed** (Artlist): mark beats; the "descend underground" beat lands on a bass drop / light-to-dark transition; use **motion match-cuts** (downward tilt → into cave mouth → through tunnel) not generic dissolves.
  5. **Master 4K from Resolve** (free, no watermark).
- **Tools:** DaVinci Resolve (free) = the editor/colorist; **ffmpeg** = scripted prep/automation only; CapCut = rough cuts only (can't shot-match).

## 3. Character animation (Dr. Mineral + workers) — the honest path
The wall has *partly moved* since our earlier note: **animal auto-rigging now exists** (Meshy, Anything World, free Mesh2Motion). Options, ranked for our case (custom animal art, web Three.js, low budget, "always-working" world):

- **★ PRIMARY — AI sprite-sheet walk/work cycles → UV-flipbook billboards.** Upload one character PNG → tools (**AutoSprite, Spritesheets.ai, Layer.ai**) emit on-model multi-frame **idle / walk / 2–3 work loops**. Play as a **UV flipbook** on the existing billboard (atlas uploads once; we just change frame index). Best believable-motion **per dollar+effort**: stays exactly on-model, minutes per character, **60fps with many workers** (video textures choke; flipbooks batch). Layer our procedural squash/stretch + foot-plant sync on top for weight. → *This is the immediate upgrade from "gliding" to "walking/working."*
- **▲ UPGRADE — image-to-3D + animal auto-rig → glTF.** **Tripo / Meshy** (PNG→GLB) → **Meshy auto-rig** or **Anything World** (or free **Mesh2Motion**) for quadruped walk/work clips → drive with Three.js `AnimationMixer`. Higher ceiling (walk-anywhere, true 3D, dense world). Cost = **Blender cleanup** to bring the generated mesh back on-model. Start with **Dr. Mineral as the hero**, validate fidelity, then expand.
- **Use sparingly:** AI **video-texture** sprite (Seedance/Kling looping clip) — gorgeous but a **perf killer** (60→30fps), so only a *single foreground hero* shot.
- **Skip:** Mixamo (humanoid only). Spine/Live2D only if hand-rigging a couple of hero characters.

---

## Unified plan
**Teaser:** Seedance 2.0 (image-to-video, via fal.ai, chained on last-frame) for cinematic AI shots **+** Artgrid/Artlist premium stock **+** our real UNL "Campus in Gold" **+** free Pexels/Pixabay fillers → normalize (ffmpeg) → grade to ONE look + cut to an Artlist track in **DaVinci Resolve (free)** → 4K master. Budget ≈ **$30/mo (Artlist) + ~$5–25 (Seedance) + free tools.**

**World characters:** AI **sprite-sheet flipbooks** for the whole cast (on-model, performant) + procedural polish now; **3D auto-rig** Dr. Mineral later for the higher ceiling.

**Suggested order:** (1) character sprite-sheets first — fastest visible win in the live world; (2) then the teaser pipeline (bigger lift, needs DaVinci + subscriptions).
