#!/usr/bin/env python3
"""Image -> 3D (.glb), FREE, automated via open-source HuggingFace Spaces.
No subscription. Reads HF_TOKEN from env (.env) for more ZeroGPU quota / TRELLIS.

Usage:
  uv run --with gradio_client python scripts/img_to_3d.py <in.png> <out.glb> [model] [mc/texsize]
    model = triposr  (default; fast, low-fidelity, works anonymously)
          = trellis  (best free quality, textured GLB; needs HF_TOKEN + ZeroGPU quota)
"""
import sys, os, shutil
from gradio_client import Client, handle_file

if len(sys.argv) < 3:
    sys.exit("usage: img_to_3d.py <in.png> <out.glb> [triposr|trellis] [param]")
src, out = sys.argv[1], sys.argv[2]
model = (sys.argv[3] if len(sys.argv) > 3 else "triposr").lower()
token = os.environ.get("HF_TOKEN") or None


def find_glb(x):
    o = []
    if isinstance(x, str) and os.path.exists(x) and x.lower().endswith(".glb"):
        o.append(x)
    elif isinstance(x, dict):
        for v in x.values():
            o += find_glb(v)
    elif isinstance(x, (list, tuple)):
        for i in x:
            o += find_glb(i)
    return o


os.makedirs(os.path.dirname(out) or ".", exist_ok=True)

if model == "trellis":
    if not token:
        print("WARN: no HF_TOKEN — TRELLIS needs one for ZeroGPU quota (free at hf.co/settings/tokens)")
    c = Client("trellis-community/TRELLIS", hf_token=token, verbose=False)
    try:
        c.predict(api_name="/start_session")
    except Exception:
        pass
    tex = float(sys.argv[4]) if len(sys.argv) > 4 else 1024.0
    print("generating with TRELLIS (textured GLB)...")
    res = c.predict(
        image=handle_file(src), multiimages=[], seed=0,
        ss_guidance_strength=7.5, ss_sampling_steps=12,
        slat_guidance_strength=3.0, slat_sampling_steps=12,
        multiimage_algo="stochastic", mesh_simplify=0.95, texture_size=tex,
        api_name="/generate_and_extract_glb")
    glbs = find_glb(res)
    if not glbs:
        sys.exit("no GLB returned: " + str(res)[:300])
    shutil.copy(glbs[0], out)
else:  # triposr
    mc = float(sys.argv[4]) if len(sys.argv) > 4 else 256.0
    c = Client("stabilityai/TripoSR", hf_token=token, verbose=False)
    print("preprocessing...")
    proc = c.predict(handle_file(src), True, 0.85, api_name="/preprocess")
    print("generating mesh...")
    _obj, glb = c.predict(handle_file(proc), mc, api_name="/generate")
    shutil.copy(glb, out)

print(f"saved {out} ({os.path.getsize(out)} bytes) via {model}")
