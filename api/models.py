"""Vercel serverless function: GET /api/models"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _core  # noqa: E402


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, obj = _core.list_models()
        payload = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
