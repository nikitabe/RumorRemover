"""Vercel serverless function: POST /api/check"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _core  # noqa: E402


class handler(BaseHTTPRequestHandler):
    def _send(self, status, obj):
        payload = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        try:
            length = int(self.headers.get("content-length", 0))
            raw = self.rfile.read(length) if length else b"{}"
            data = json.loads(raw.decode("utf-8"))
            rumor = (data.get("rumor") or "").strip()
        except Exception:
            self._send(400, {"error": "Invalid JSON body."})
            return
        if not rumor:
            self._send(400, {"error": "Missing 'rumor' in request body."})
            return
        status, payload = _core.call_llm(rumor)
        self._send(status, payload)
