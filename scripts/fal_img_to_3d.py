#!/usr/bin/env python3
"""Image -> 3D (.glb) via fal.ai (paid, reliable, no ZeroGPU quota).
Reads FAL_KEY from env (.env).

Usage:
  uv run --with fal-client python scripts/fal_img_to_3d.py <in.png> <out.glb> [trellis|rodin]
    trellis = fal-ai/trellis        (same model as the HF Space; cheap)
    rodin   = fal-ai/hyper3d/rodin  (Hyper3D Rodin; best quality, pricier)
"""
import sys, os, urllib.request
import fal_client

if len(sys.argv) < 3:
    sys.exit("usage: fal_img_to_3d.py <in.png> <out.glb> [trellis|rodin]")
src, out = sys.argv[1], sys.argv[2]
model = (sys.argv[3] if len(sys.argv) > 3 else "trellis").lower()

if not os.environ.get("FAL_KEY"):
    sys.exit("FAL_KEY not set in env")

os.makedirs(os.path.dirname(out) or ".", exist_ok=True)

def log(u):
    if isinstance(u, dict):
        for line in u.get("logs", []) or []:
            print("  ", line.get("message", ""))

print(f"uploading {src} ...")
url = fal_client.upload_file(src)
print("uploaded ->", url[:80])

if model == "rodin":
    endpoint = "fal-ai/hyper3d/rodin"
    args = {
        "input_image_urls": [url],
        "condition_mode": "concat",
        "geometry_file_format": "glb",
        "material": "PBR",
        "quality": "high",
        "tier": "Regular",
        "use_hyper": True,
    }
else:
    endpoint = "fal-ai/trellis"
    args = {
        "image_url": url,
        "ss_guidance_strength": 7.5,
        "ss_sampling_steps": 12,
        "slat_guidance_strength": 3.0,
        "slat_sampling_steps": 12,
        "mesh_simplify": 0.95,
        "texture_size": 1024,
    }

print(f"generating via {endpoint} ...")
res = fal_client.subscribe(endpoint, arguments=args, with_logs=True, on_queue_update=log)

# find the mesh url in the result
mesh = res.get("model_mesh") or res.get("mesh") or res.get("model")
if isinstance(mesh, dict):
    mesh_url = mesh.get("url")
elif isinstance(mesh, str):
    mesh_url = mesh
else:
    # rodin sometimes returns a list / different key
    mesh_url = None
    for v in res.values():
        if isinstance(v, dict) and str(v.get("url", "")).lower().endswith(".glb"):
            mesh_url = v["url"]; break
if not mesh_url:
    sys.exit("no GLB url in result: " + str(res)[:400])

print("downloading mesh ->", mesh_url[:80])
urllib.request.urlretrieve(mesh_url, out)
print(f"saved {out} ({os.path.getsize(out)} bytes) via {endpoint}")
