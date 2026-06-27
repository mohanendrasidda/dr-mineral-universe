# Intro Video Brief — "Descent into the Lab"

The cinematic that plays when a visitor clicks **ENTER THE LAB**. It tells the story (Lincoln → the UNL campus → the library → from the sky, down *through* the earth → reveal the whole hidden lab → zoom into the lab and stop), then hands into our interactive 3D world.

**How it's wired (already built):** the player lives in `site/world/index.html`. Drop the finished file at **`assets/video/intro.mp4`** (H.264 MP4, 1920×1080, ~35–45s, with its own music/audio baked in). On Enter, a one-tap "▶ BEGIN" splash starts it *with sound*; when it ends it dissolves into the 3D world positioned in the Mines. Until the file exists, Enter falls back to the in-engine 3D camera dive — nothing breaks.

---

## Global style anchor — PASTE INTO EVERY CLIP
> Cinematic, photoreal, filmic. Warm **sepia / amber / gold over near-black** palette — candlelit, ancient, mysterious, reverent. Volumetric god-rays, drifting dust, soft haze, shallow depth of field, gentle anamorphic flares, fine 24fps film grain. Slow, weighty, awe-struck camera. **NOT cartoon, NOT bright, NOT cheerful stock-video** — this is a secret discovered. Color grade: teal-free, warm shadows, deep blacks.

## Audio direction (overall)
One continuous score across the cut: **soft warm piano/strings (campus, nostalgic) → a low cello + rising sub-bass hum at the descent → a full, holy, awe-struck swell at the reveal → resolve to a slow, steady low pulse (a forge's heartbeat) as it settles.** Ambient: campus breeze & distant chatter up top; a deep cathedral hum, dripping water, and a faint forge-roar underground. No narration, no chirpy SFX.

---

## Option A — one master prompt (if your tool does a single longer shot)
> A continuous cinematic flight, ~40 seconds, warm sepia/gold over near-black, photoreal and reverent. Open on a slow aerial over **Lincoln, Nebraska at golden dusk**, gliding toward a **University of Nebraska–Lincoln–style red-brick campus** — autumn trees, a grand stone **college library** with glowing windows, students small below. The camera drifts down toward the library courtyard as the light dims and a faint warm glow seems to rise from *beneath* the pavement. Then the camera tilts down and **plunges into the earth** — through soil, rock strata and roots, down a natural shaft, daylight shrinking to a point far above, amber light swelling from below. It bursts out into an **enormous hidden underground hall**: carved sepia-stone tier-upon-tier colonnaded galleries falling into warm dark, hundreds of tiny lanterns receding into haze, a glowing golden chain and a deep forge-ember far below. The camera **pulls back to reveal the whole vast boundary of the lab — a secret subterranean city** — then sweeps down and forward at speed toward one glowing district, a **burning amber crystal seam (the Mines)** with small shadowed figures at slow heavy labor, rushing in and **settling, holding** on the seam. Volumetric god-rays, dust, haze, film grain. Music: warm piano → deep swelling strings at the plunge → holy awe-struck swell at the reveal → settle to a low steady forge-pulse. NOT cartoon, NOT bright.

## Option B — 5 stitched clips (for 5–8s clip tools; render each with the style anchor)

**CLIP 1 — Establish: Lincoln & UNL (≈8s).**
> Aerial drone shot descending over **Lincoln, Nebraska at golden dusk** toward a **University of Nebraska–Lincoln–style red-brick campus** — autumn trees, green quad, a tall campus landmark, students crossing far below. Warm, calm, ordinary, alive. Slow forward glide. Music: soft warm piano & strings. Ambient: gentle breeze, faint distant campus chatter.

**CLIP 2 — The library & the hint (≈7s).**
> Slow push-in on a **grand stone college library** at dusk, tall windows glowing amber; the camera drifts downward past the façade toward the courtyard pavement; the daylight cools and dims; a subtle **warm glow leaks up from below the ground**, as if something vast waits beneath. Mood: quiet curiosity, a secret. Music: a single low note enters under the strings; a hush.

**CLIP 3 — The descent through the earth (≈8s).**
> The camera tilts straight down and **plunges into the ground** — punching through soil, layered rock strata, roots and stone, racing down a narrow natural shaft; daylight shrinks to a tiny point far above; a warm amber glow rises from the deep below. Fast, weighty, vertiginous, awe. Music: swelling deep cello and a rising sub-bass hum — the world changes. Ambient: rush of descent, deepening reverb.

**CLIP 4 — The reveal: the lab & its whole boundary (≈8s).**
> The camera bursts out of the shaft into an **enormous hidden underground hall** — carved sepia-stone, **tier upon tier of colonnaded galleries falling into warm darkness**, hundreds of tiny lanterns receding into haze, a great glowing golden chain and a deep orange forge-ember far below. The camera **pulls back to reveal the whole vast boundary of the lab — a secret subterranean city** that has clearly stood for ages. Mood: wonder, reverence, "it has been here all along." Music: full, holy, awe-struck orchestral swell. Ambient: deep cathedral hum, distant forge.

**CLIP 5 — Zoom into the lab: the Mines (≈7s).**
> The camera sweeps down and forward **at speed** across the galleries toward one glowing district — **the Mines**: a burning amber crystal seam in deep shadow, small shadowed figures at slow, heavy, rhythmic labor. It rushes in and **settles, holding** on the glowing seam. Mood: arrival; the ancient work goes on. Music: resolves to a slow, steady low pulse (a forge's heartbeat). → cut to the interactive world.

**Continuity between clips:** end each clip on the frame the next one opens on (Clip 2 ends looking down at the pavement glow that Clip 3 plunges into; Clip 4 ends on the wide lab that Clip 5 dives into). Keep palette/grain identical across all five (the style anchor does this).

---

## Export & drop-in
- **Format:** H.264 **MP4**, **1920×1080**, ~30fps, audio baked in (AAC). Keep it ≤ ~25 MB if you can (web load).
- **Save as:** `assets/video/intro.mp4` in this repo. That's the only step — the player auto-detects it.
- **Optional:** also export a 9:16 vertical cut as `assets/video/intro-mobile.mp4` later if we want phones (not wired yet).

## Honest notes
- AI video **won't render the real UNL landmarks with documentary accuracy** — it'll give a convincing *UNL-style* red-brick campus and a grand library, not a recognizable photo of Love Library. If you want the *real* campus, the better route is **real licensed drone footage of UNL** for Clips 1–2, then AI/our-world for the underground — we edit them together to the same grade. Say the word and I'll write the edit plan for that hybrid.
- Generate a few takes per clip and pick the ones that best match the warm/dark grade; consistency between clips is the main risk with AI video.
