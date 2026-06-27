#!/usr/bin/env python3
"""Call a PixelLab MCP tool directly via JSON-RPC (bypasses the Claude Code MCP loader).
Reads PIXELLAB_TOKEN from env (never hardcode — repo is public).

Usage:
  export PIXELLAB_TOKEN=...   # from ~/.claude.json
  python3 scripts/pixellab_rpc.py <tool_name> '<json args>'
e.g.
  python3 scripts/pixellab_rpc.py get_balance '{}'
  python3 scripts/pixellab_rpc.py create_character '{"description":"...","body_type":"humanoid"}'
"""
import json, sys, os, urllib.request, urllib.error

TOK = os.environ.get("PIXELLAB_TOKEN")
if not TOK:
    sys.exit("set PIXELLAB_TOKEN in env")
name = sys.argv[1]
args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                   "params": {"name": name, "arguments": args}}).encode()
req = urllib.request.Request("https://api.pixellab.ai/mcp", data=body, headers={
    "Authorization": "Bearer " + TOK, "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"})
try:
    raw = urllib.request.urlopen(req, timeout=180).read().decode()
except urllib.error.HTTPError as e:
    sys.exit(f"HTTP {e.code}: {e.read().decode()[:400]}")
out = None
for line in raw.splitlines():
    if line.startswith("data:"):
        d = json.loads(line[5:].strip())
        out = d.get("result", d.get("error"))
if isinstance(out, dict) and "content" in out:
    for c in out["content"]:
        if c.get("type") == "text":
            print(c["text"])
else:
    print(json.dumps(out)[:2000] if out is not None else raw[:800])
