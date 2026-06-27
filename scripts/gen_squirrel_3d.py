#!/usr/bin/env python3
"""Generate a higher-quality 3D Dr. Mineral via Hunyuan3D-2 (free HF Space) once the ZeroGPU quota allows.

Idempotent + self-quieting: exits early if the output already exists, so it can be run on a daily timer and
becomes a no-op after it succeeds. Reads HF_TOKEN from the repo .env. Input is the A-pose front crop.
"""
import os, sys, shutil, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, "assets/models/drmineral_hunyuan.glb")
IMG  = os.path.join(ROOT, "assets/models/refs/drmineral-front.png")

if os.path.exists(OUT):
    print(f"[{time.ctime()}] already generated: {OUT}"); sys.exit(0)

# load HF token from .env
envf = os.path.join(ROOT, ".env")
if os.path.exists(envf):
    for line in open(envf):
        line = line.strip()
        if line.startswith(("HF_TOKEN=", "HUGGING_FACE_HUB_TOKEN=")):
            tok = line.split("=", 1)[1].strip()
            os.environ.setdefault("HF_TOKEN", tok)
            os.environ.setdefault("HUGGING_FACE_HUB_TOKEN", tok)

from gradio_client import Client, handle_file

def find_glb(x):
    if isinstance(x, str) and x.endswith(".glb") and os.path.exists(x): return x
    if isinstance(x, dict):
        for v in x.values():
            r = find_glb(v)
            if r: return r
    if isinstance(x, (list, tuple)):
        for v in x:
            r = find_glb(v)
            if r: return r
    return None

def try_space(space):
    print(f"[{time.ctime()}] trying {space}")
    c = Client(space, verbose=False)
    ep = c.view_api(return_format="dict").get("named_endpoints", {})
    def out3d(info): return any(('filepath' in str(r.get('python_type', {})) or 'odel3' in str(r.get('component', ''))) for r in info.get('returns', []))
    cand = [(n, i) for n, i in ep.items() if out3d(i)]
    cand.sort(key=lambda x: (('all' not in x[0].lower()), ('gen' not in x[0].lower())))
    if not cand:
        print("  no 3D endpoint"); return False
    name, info = cand[0]; print("  endpoint:", name)
    args = []; img_used = False
    for p in info.get("parameters", []):
        pt = str(p.get("python_type", {})) + str(p.get("component", ""))
        if (not img_used) and (('path' in pt and 'url' in pt) or 'Image' in pt):
            args.append(handle_file(IMG)); img_used = True
        elif p.get("parameter_has_default"):
            args.append(p.get("parameter_default"))
        else:
            args.append("")
    res = c.predict(*args, api_name=name)
    glb = find_glb(res)
    if glb:
        shutil.copy(glb, OUT); print(f"  SAVED {OUT} ({os.path.getsize(OUT)} B)"); return True
    print("  no glb in result:", str(res)[:160]); return False

for sp in ["tencent/Hunyuan3D-2", "tencent/Hunyuan3D-2.1"]:
    try:
        if try_space(sp): sys.exit(0)
    except Exception as e:
        msg = repr(e)[:200]; print("  FAIL:", msg)
        if "quota" in msg.lower(): print("  (ZeroGPU quota not reset yet — will retry next run)")
print(f"[{time.ctime()}] not generated this run."); sys.exit(1)
