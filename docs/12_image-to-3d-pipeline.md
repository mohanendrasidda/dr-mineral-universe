# Free Image-to-3D Pipeline (research + working setup)

How we turn our 2D character renders into real 3D `.glb` models — **free, automated from Claude Code**, no subscription. From a deep-research pass (late 2025/2026) + live testing.

## TL;DR (ranked, free)
| Tool | Quality | Automatable from terminal | Notes |
|---|---|---|---|
| **TRELLIS** (`trellis-community/TRELLIS`) | ⭐ best free | ✅ `gradio_client` → `/generate_and_extract_glb` | Textured GLB. **Needs a free HF token** for ZeroGPU quota |
| **Hunyuan3D-2** (`tencent/Hunyuan3D-2`) | high (PBR) | ✅ `/generation_all`, `/shape_generation` | Hit a server-side NameError on `/generation_all`; `/shape_generation` may work |
| **TripoSR** (`stabilityai/TripoSR`) | low/fast | ✅ `/preprocess`→`/generate` (works anonymously) | **Already working** — our first `dr-mineral.glb` |
| InstantMesh (`TencentARC/InstantMesh`) | mid | ✅ Space; GLB export unconfirmed (may be .obj) | ~10s; CUDA-only locally |

- **GLB/GLTF** are first-class HF image-to-3D outputs.
- **ZeroGPU is free but metered** (~120s/job daily, anonymous). A **free HF token** (hf.co/settings/tokens) raises quota — required for TRELLIS. PRO ($9/mo) only adds more; not required.
- **Local (macOS Apple Silicon):** Hunyuan3D-2 `--device mps` does *untextured* shape (~6GB, 2–5 min); texturing needs CUDA (won't build on M-series). InstantMesh is CUDA-only.
- fal.ai TripoSR = paid API ($0.07/gen), not free.
- Sources: huggingface.co/spaces/{microsoft/TRELLIS, trellis-community/TRELLIS, tencent/Hunyuan3D-2, TencentARC/InstantMesh}, huggingface.co/blog/daggr, huggingface.co/tasks/image-to-3d.

## Our working pipeline
`scripts/img_to_3d.py` (stdlib + gradio_client; run via uv):
```bash
# fast / low-fi (works anonymously — already used for dr-mineral.glb):
uv run --with gradio_client python scripts/img_to_3d.py assets/raw/char-drmineral-hero-v1.png assets/models/dr-mineral.glb triposr
# best free quality (textured) — needs HF_TOKEN in .env:
uv run --with gradio_client python scripts/img_to_3d.py assets/keyed/char-drmineral-hero-v1.png assets/models/dr-mineral.glb trellis
```
Models load in `site/world/index.html` via `GLTFLoader`.

## The one blocker for quality
TRELLIS (and topping up TripoSR quota) needs a **free Hugging Face token**: create at https://huggingface.co/settings/tokens (read scope is enough), add `HF_TOKEN=hf_...` to the gitignored `.env`. Then the whole cast can be generated at TRELLIS quality, automated, free.
