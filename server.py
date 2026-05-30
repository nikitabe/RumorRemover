#!/usr/bin/env python3
"""
RumorRemover backend (local dev).

A dependency-free server (Python standard library only) that:
  - serves the static site (index.html, verify.html, etc.)
  - exposes POST /api/check  -> verifies a rumor against the reference files
  - exposes GET  /api/health -> reports whether the server is configured

For local development only. On Vercel the same logic runs as serverless
functions (api/check.py, api/health.py); the shared implementation lives in
api/_core.py and is imported here so there is a single source of truth.

Configuration (environment variables, optionally via a local .env file):
  AI_KEY      (required) Anthropic API key, sent as the x-api-key header
  BASE_URL    (optional) default: https://api.anthropic.com/v1
  LLM_MODEL   (required) e.g. claude-sonnet-4-6
  PORT        (optional) default: 4321

Run:  AI_KEY=... LLM_MODEL=... python3 server.py
"""

import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))


# ---- minimal .env loader (no dependencies); must run before importing _core ----
def load_dotenv(path):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key, val = key.strip(), val.strip().strip('"').strip("'")
            # .env values take precedence so a stale/empty shell var can't shadow them
            os.environ[key] = val


load_dotenv(os.path.join(ROOT, ".env"))

sys.path.insert(0, os.path.join(ROOT, "api"))
import _core  # noqa: E402

PORT = int(os.environ.get("PORT", "4321"))


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def _send_json(self, status, obj):
        payload = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path == "/api/health":
            self._send_json(200, _core.health())
            return
        super().do_GET()

    def do_POST(self):
        if self.path != "/api/check":
            self._send_json(404, {"error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length else b"{}"
            data = json.loads(raw.decode("utf-8"))
            rumor = (data.get("rumor") or "").strip()
        except Exception:
            self._send_json(400, {"error": "Invalid JSON body."})
            return
        if not rumor:
            self._send_json(400, {"error": "Missing 'rumor' in request body."})
            return
        status, payload = _core.call_llm(rumor)
        self._send_json(status, payload)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main():
    h = _core.health()
    print(f"RumorRemover server on http://localhost:{PORT}")
    print(f"  Base URL : {h['baseUrl']}")
    print(f"  Model    : {h['model'] or '(not set)'}")
    print(f"  API key  : {'set' if h['configured'] else 'NOT SET — /api/check will return 503'}")
    if not h["configured"]:
        print("  -> Set AI_KEY and LLM_MODEL (env or .env) to enable rumor checking.")
    ThreadingHTTPServer(("", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
