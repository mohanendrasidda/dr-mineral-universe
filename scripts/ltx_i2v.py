#!/usr/bin/env python3
"""Image -> short cinematic video clip, FREE, via LTX-Video on HuggingFace Spaces.

Turns a still (a concept render or a footage frame) into a ~5s moving shot with a
prompt-directed camera/atmosphere. Uses free ZeroGPU; reads HF_TOKEN from env (.env)
to stretch the daily quota (free account ~5 min GPU/day ~= 3-4 clips/day).

Usage:
  set -a; . ./.env; set +a
  uv run --with gradio_client python scripts/ltx_i2v.py <in.png> <out.mp4> "<prompt>" [duration_s]
"""
import os, sys, shutil
from gradio_client import Client, handle_file

if len(sys.argv) < 4:
    sys.exit('usage: ltx_i2v.py <in.png> <out.mp4> "<prompt>" [duration_s]')
img, out, prompt = sys.argv[1], sys.argv[2], sys.argv[3]
dur = float(sys.argv[4]) if len(sys.argv) > 4 else 5.0
NEG = "worst quality, blurry, jittery, distorted, deformed, morphing, text, watermark, cartoon, oversaturated"

c = Client("Lightricks/ltx-video-distilled")   # HF_TOKEN picked up from env
print(f"generating from {img} ({dur}s)...")
res = c.predict(
    prompt=prompt, negative_prompt=NEG,
    input_image_filepath=handle_file(img),
    height_ui=704, width_ui=1216, duration_ui=dur, ui_guidance_scale=3.0,
    api_name="/image_to_video",
)

def find_mp4(x):
    if isinstance(x, str) and x.endswith(".mp4") and os.path.exists(x):
        return x
    if isinstance(x, dict):
        for v in x.values():
            r = find_mp4(v)
            if r:
                return r
    if isinstance(x, (list, tuple)):
        for v in x:
            r = find_mp4(v)
            if r:
                return r
    return None

mp4 = find_mp4(res)
if not mp4:
    sys.exit("no mp4 in result: " + str(res)[:200])
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
shutil.copy(mp4, out)
print("saved", out, os.path.getsize(out), "bytes")
