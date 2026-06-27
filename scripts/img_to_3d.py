#!/usr/bin/env python3
"""Image -> 3D (.glb), fully automated & FREE via the open-source TripoSR
HuggingFace Space. No subscription, no manual download.

Usage:
  uv run --with gradio_client python scripts/img_to_3d.py <in.png> <out.glb> [mc_resolution]
  (mc_resolution 32-320, default 256 — higher = more detail, slower)
"""
import sys, os, shutil
from gradio_client import Client, handle_file

if len(sys.argv) < 3:
    sys.exit("usage: img_to_3d.py <in.png> <out.glb> [mc_resolution 32-320]")
src, out = sys.argv[1], sys.argv[2]
mc = float(sys.argv[3]) if len(sys.argv) > 3 else 256.0

c = Client("stabilityai/TripoSR", verbose=False)
print("preprocessing", src, "...")
proc = c.predict(handle_file(src), True, 0.85, api_name="/preprocess")
print("generating mesh ...")
_obj, glb = c.predict(handle_file(proc), mc, api_name="/generate")
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
shutil.copy(glb, out)
print(f"saved {out} ({os.path.getsize(out)} bytes)")
