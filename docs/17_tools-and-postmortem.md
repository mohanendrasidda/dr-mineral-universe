# Tools & Postmortem — what we used, what worked, what didn't

A running log of the toolchain behind The Lab / Dr. Mineral Universe, so we don't re-learn the same lessons. Updated 2026-06-27.

## The stack (what's in the build)
| Tool | Used for | Verdict |
|---|---|---|
| **Three.js** (r0.160, CDN importmap) | the interactive 3D world (`site/world/`) | ✅ The right medium for a real-time browser world. Carries the whole experience. |
| **ffmpeg** | all video: stitch, color grade, watermark removal (`delogo`), crossfades, fades, push-ins (`zoompan`), audio trim/fade, **frame extraction for QC** | ✅ The workhorse. Did everything we needed. |
| **Frame-extraction QC** (ffmpeg → Read image) | letting Claude actually *see* footage/renders to diagnose | ✅ Game-changer. This is how we caught mirrored text, blown skies, wrong shots, off grades. |
| **Poly Haven** (CC0 PBR textures) | `castle_brick_01` stone (diffuse/normal/rough) | ✅ Free, high quality. Download needs a `User-Agent` header on the API. |
| **Incompetech / Kevin MacLeod** (CC-BY music) | "The Descent" intro score | ✅ Direct MP3 download works. Requires attribution (in footer + `assets/audio/README`). |
| **UNL MediaHub** (real UNL footage) | "Campus in Gold" — the campus opening | ✅ Best footage by far. Needs UNL-affiliate login; downloads as `media.mp4` (Kaltura). |
| **rembg** (`uvx rembg`) | keying character renders to transparent PNG | ✅ Worked for the sprite cast. |
| **WebSearch / WebFetch** | finding UNL footage sources + licensing | ✅ Found MediaHub, the media kit, the Flying Club. |

## What didn't work (and the lesson)
| Tried | Why it failed | What we did instead |
|---|---|---|
| **Free image-to-3D** (TripoSR / TRELLIS via HF `gradio_client`) | Outputs un-riggable triangle soup — fine for static props, **useless for animatable characters** | 2.5D billboard sprites for the cast; real PBR + procedural geometry for the world |
| **Luma API** | Key wouldn't authenticate; Luma has no 3D export anyway | Dropped |
| **Gemini image generation** | Free-tier daily quota exhausted | Couldn't generate sprite frames / new art; blocked |
| **Gemini/Veo AI video** | 720p only, 10s max clips, **per-clip baked audio is incoherent** across clips, sparkle watermark, quota-limited | Used for a placeholder campus; replaced by real UNL footage. Lesson: **AI clips = visuals only; never trust their audio.** |
| **Generic stock footage** (Pexels) | Downloaded 3 "university campus" clips — all modern/overcast/daytime (one had mountains). None fit our warm-autumn theme | Real UNL "Campus in Gold" was the answer. Lesson: generic stock ≠ on-theme. |
| **"Pixar in the browser"** | Real-time rasterization ≠ offline path-tracing. A medium gap, not a settings gap | Targeted "as real as a real-time WebGL scene gets" |
| **2.5D sprites doing "real walking"** | Billboards can't articulate legs without walk-cycle frames (art) or 3D rigs | Procedural weight/rhythm (footfall dips, swing anticipation) — the ceiling without more art |

## Process lessons (the ones that mattered most)
1. **The verify-by-frames loop is everything.** Building the 3D world "blind" only worked because a reviewer kept grabbing render frames and giving a frame-by-frame read. Every quality jump came from that loop.
2. **One discipline makes or breaks it:** *one palette (warm/sepia), one fidelity, everything grounded with contact shadows, nothing default-saturated.* When held → reads real. When broken on newly-added objects (cyan orb, red forge, floating mirrored sign) → instantly reads "amateur / work-in-progress."
3. **Audio is its own layer.** One continuous score over the whole intro (calm under campus → swell into the descent), clips muted. Don't let AI clips own the soundtrack.
4. **Grade restraint:** already-graded footage doesn't want a second heavy grade — a film contrast curve (lift blacks / roll highlights) + gentle split-tone beats a warm-push that over-cooks it.
5. **Emotional arc for the intro:** day → dusk → underground. Don't slam from sunny noon into a candlelit cavern; ease down.

## Security / secrets
- API keys (Gemini, Luma, HF) live **only** in gitignored `.env` — never committed, never in memory/Notion. Verified clean before first push.
- Any key pasted into chat during dev should be **rotated**.
- **Consent-gating:** team names/photos and UNL footage go public only with each person's consent + UNL Comms/Marketing sign-off.
