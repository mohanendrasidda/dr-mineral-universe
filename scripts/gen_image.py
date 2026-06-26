#!/usr/bin/env python3
"""Generate an image via the Gemini API (Nano Banana) from Claude Code.
Usage: GEMINI_API_KEY=... python3 scripts/gen_image.py "<prompt>" out.png [model]
Default model: gemini-2.5-flash-image. No third-party deps (stdlib only).
"""
import sys, os, json, base64, urllib.request, urllib.error

API = os.environ.get("GEMINI_API_KEY")
if not API:
    sys.exit("set GEMINI_API_KEY (it's in the gitignored .env)")
if len(sys.argv) < 3:
    sys.exit('usage: gen_image.py "<prompt>" <out.png> [model]')
prompt, out = sys.argv[1], sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else os.environ.get("GEN_MODEL", "gemini-2.5-flash-image")
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API}"

def call(gencfg):
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    if gencfg is not None:
        body["generationConfig"] = gencfg
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=180)), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode()[:300]}"

# try a few response-modality configs for compatibility across image models
data = err = None
for cfg in ({"responseModalities": ["IMAGE"]},
            {"responseModalities": ["TEXT", "IMAGE"]},
            None):
    data, err = call(cfg)
    if data:
        break
if not data:
    sys.exit("generation failed: " + str(err))

parts = (data.get("candidates") or [{}])[0].get("content", {}).get("parts", [])
img = None
for p in parts:
    d = p.get("inlineData") or p.get("inline_data")
    if d and d.get("data"):
        img = d["data"]; break
if not img:
    sys.exit("no image in response: " + json.dumps(data)[:400])

os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
with open(out, "wb") as f:
    f.write(base64.b64decode(img))
print(f"wrote {out} ({os.path.getsize(out)} bytes) via {model}")
