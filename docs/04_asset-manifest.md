# Asset Manifest — Dr. Mineral visual library

35 files in `/assets/`: 34 source PNGs (Nano Banana / Gemini renders of the squirrel) + `index.html` (the self-contained landing page). The animation frames are **embedded as base64 inside index.html**, so the page travels as one file; the PNGs are the source/variant library behind it.

**Background legend:** `KEYED` = transparent (checkerboard), drop-in ready · `GREEN` = chroma green, needs keying · `WHITE` = plain white, needs keying. Use the `ai-render-keying` skill for GREEN/WHITE.
**Canon legend:** `CLEAN` = acorn/discovery pose, on-canon for the universe · `CHAIN` = wrapped in the blockchain-pun chain, **off-canon** (cohort page only — see registry flag).

| # | File (`Gemini_Generated_Image_…`) | Pose family | BG | Canon |
|--|--|--|--|--|
| 1 | …208j9q… | Hang / climb a vertical line, acorn | GREEN | CLEAN |
| 2 | …38izxz… | Boo / arms-up reveal | KEYED | CLEAN |
| 3 | …3a4x7e… | Hang, reaching arm up | GREEN | CLEAN |
| 4 | …3b9rr6… | Run / leap right, acorn | GREEN | CLEAN |
| 5 | …3z13ox… | Walk / stand, acorn | WHITE | CLEAN |
| 6 | …5lfpag… | Walk / idle, acorn in mouth | WHITE | CLEAN |
| 7 | …5qlgnh… | Walk / crouch forward, acorn | KEYED | CLEAN |
| 8 | …7knnxk… | Climb with chain | GREEN | CHAIN |
| 9 | …85pwne… | Hang from line, acorn | GREEN | CHAIN |
| 10 | …asv668… | Boo / arms-up, eyes closed | GREEN | CLEAN |
| 11 | …c3ihwj… | Run with chain | GREEN | CHAIN |
| 12 | …c3ihwj_1… | **Duplicate of #11** | GREEN | CHAIN |
| 13 | …db3d6h… | Boo / arms-up, acorn | KEYED | CLEAN |
| 14 | …dwycmi… | Walk frame, acorn | KEYED | CLEAN |
| 15 | …e7lfa8… | Run / leap mid-stride, acorn | KEYED | CLEAN |
| 16 | …f9d7k0… | Walk frame, acorn | KEYED | CLEAN |
| 17 | …fed80p… | Walk frame, acorn | KEYED | CLEAN |
| 18 | …fed80p_1… | **Duplicate of #17** | KEYED | CLEAN |
| 19 | …g7m9ny… | Run / leap with chain | GREEN | CHAIN |
| 20 | …iqzgb9… | Run low with chain | GREEN | CHAIN |
| 21 | …ir4l8l… | Pull-up / climb onto ledge, chain | GREEN | CHAIN |
| 22 | …j9nyqw… | Hang from ledge, reaching | GREEN | CHAIN |
| 23 | …kb1as1… | Run with chain | GREEN | CHAIN |
| 24 | …kgb3sy… | Run / leap with chain | GREEN | CHAIN |
| 25 | …lid1wl… | Run with chain, acorn | GREEN | CHAIN |
| 26 | …lrzy4g… | Climb vertical line | GREEN | CLEAN |
| 27 | …nbhoys… | Run, long chain trailing | GREEN | CHAIN |
| 28 | …nmerll… | Boo / arms-up, acorn | KEYED | CLEAN |
| 29 | …nvpb71… | Run with chain, acorn | GREEN | CHAIN |
| 30 | …rh6cx9… | Pull-up onto ledge, chain below | GREEN | CHAIN |
| 31 | …rulyw6… | Run, chain loop | GREEN | CHAIN |
| 32 | …whxxj0… | Run with chain | GREEN | CHAIN |
| 33 | …xp0jx2… | Run, chain loop trailing | GREEN | CHAIN |
| 34 | …xwk8h7… | **Seated idle hero pose**, acorn, tail up | KEYED | CLEAN |

## Quick reads
- **Best single hero image:** #34 (clean, keyed, classic seated portrait). Use for the character sheet / first public face.
- **Cleanest ready-to-use set (KEYED + CLEAN):** #2, #7, #13, #14, #15, #16, #17, #28, #34. A walk + run + boo + idle vocabulary already transparent.
- **Pose families present:** idle, walk (several frames), run/leap, boo/reveal, hang/dangle, pull-up/climb.
- **Housekeeping:** #12 and #18 are exact duplicates — drop them.
- **Keying backlog:** all GREEN tiles need the `ai-render-keying` pass before compositing.

## On `index.html`
Self-contained dark-premium landing page; 8 keyed frames baked in as base64; Three.js hero, starfield, and a RAF state-machine squirrel that wanders page elements (walk / hang / boo). Currently built as the **Lab Reward Token (cohort)** page. For the universe, it's the candidate **first public surface** — but it must be re-skinned to canon (drop chain/token framing, lead with Dr. Mineral + discovery) before it represents the universe rather than the cohort.

## Hang/pull note
The memory of two "still-needed" poses (`hang`, `pull`) is partly already covered here — hang candidates (#1, #3) and pull-up candidates (#21, #30, #26) exist, but on GREEN and some are CHAIN. Decide: key the clean ones (#1, #3, #26) to canon, or regenerate clean hang/pull frames matched to the 5-phase hang sequence. (See asset-request protocol in the instructions.)
