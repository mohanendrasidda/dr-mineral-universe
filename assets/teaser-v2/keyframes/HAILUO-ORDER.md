# Hailuo generation order — Teaser V2 "The Hidden Lab" (core-10)

All keyframes are renamed + ready in this folder. Work top to bottom. **8 start/end pairs + 2 single-image** = **10 clips.**
Save each finished clip as `S1.mp4`, `S3.mp4`, … into `../clips/`. Keep Hailuo on its **highest free resolution**; pick **~5s**.

| # | Clip | Hailuo mode | Frames to attach | Motion prompt to paste |
|---|---|---|---|---|
| 1 | **S1.mp4** | Start→End | `S1-start.png` → `S1-end.png` | Slow cinematic descent pushing through the storm toward the great oak; rain, drifting clouds, distant lightning. |
| 2 | **S3.mp4** | Start→End | `S3-start.png` → `S3-end.png` | The squirrel watches, then darts off the branch; rain falls, leaves scatter; camera holds. |
| 3 | **S6.mp4** | Start→End | `S6-start.png` → `S6-end.png` | Falling/descending as the warm golden glow swells up from below and fills the shaft; dust drifts. |
| 4 | **S7.mp4** | Start→End | `S7-start.png` → `S7-end.png` | Majestic slow crane-out revealing the vast glowing underground civilization; the chain of light shimmers. |
| 5 | **S10.mp4** | **Single image** | `S10.png` | The squirrel leans in toward the screen; the red crack pulses and spreads; she reacts, tense. |
| 6 | **S13.mp4** | Start→End | `S13-start.png` → `S13-end.png` | The beaver sets the crystal, then raises the great hammer overhead; forge blazes, sparks rise. |
| 7 | **S14.mp4** | **Single image** | `S14.png` | The hammer strikes down hard; sparks explode outward; the glowing link flares and locks into the chain. |
| 8 | **S15.mp4** | Start→End | `S15-start.png` → `S15-end.png` | He walks forward and turns to look directly into camera; warm light finds his face; dust drifts. |
| 9 | **S17.mp4** | Start→End | `S17-start.png` → `S17-end.png` | The coin spins; engraved symbols ignite and the glowing blocks begin to orbit it. |
| 10 | **S20.mp4** | Start→End | `S20-start.png` → `S20-end.png` | A golden coin rises from the roots; the student reaches toward it; aurora shimmers, snow drifts → hold (we cut to black). |

**Notes**
- **S10 + S14 are single-image** (Kling is out) — use Hailuo's normal image-to-video, paste the motion prompt.
- If **S7** drifts oddly, it's fine — both frames are full cavern wides, so it'll read as a slow camera move across the reveal.
- **S15-start is half-res (1600px)** while everything else is 3200px — see quality note below.

## Quality (max — no compromise)
- **Keyframes are 3200×1344** (sharper than 4K-wide) — excellent. Only `S15-start.png` is 1600px; **regenerate it at full res** (or we upscale it) so S15 matches.
- **Video:** free Hailuo outputs ~720–768p. To hit real-teaser quality I will: (1) feed it the full-res frames, (2) **AI-upscale every returned clip to crisp 1080p** (Real-ESRGAN, free), (3) final **1080p render + cinematic grade + 70mm grain**. True 4K = Hailuo HD (paid) or a heavier upscale pass — say the word.
