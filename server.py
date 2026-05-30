#!/usr/bin/env python3
"""
RumorRemover backend.

A dependency-free server (Python standard library only) that:
  - serves the static site (index.html, verify.html, etc.)
  - exposes POST /api/check  -> verifies a rumor against verification-context.md
                                using a server-side LLM call (key never reaches the browser)
  - exposes GET  /api/health -> reports whether the server is configured

Configuration (environment variables, optionally via a local .env file):
  AI_KEY      (required) API key for the OpenAI-compatible endpoint
  BASE_URL    (optional) default: https://api.tokenfactory.us-central1.nebius.com/v1
  LLM_MODEL   (required) e.g. meta-llama/Llama-3.3-70B-Instruct
  PORT        (optional) default: 4321

Run:  AI_KEY=... LLM_MODEL=... python3 server.py
"""

import json
import os
import sys
import urllib.request
import urllib.error
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTEXT_FILE = os.path.join(ROOT, "verification-context.md")
SKILL_FILE = os.path.join(ROOT, "RumorRemover_skill.md")
DEFAULT_BASE = "https://api.tokenfactory.us-central1.nebius.com/v1"


# ---- minimal .env loader (no dependencies) ----
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

BASE_URL = os.environ.get("BASE_URL", DEFAULT_BASE).rstrip("/")
API_KEY = os.environ.get("AI_KEY", "")
MODEL = os.environ.get("LLM_MODEL", "")
PORT = int(os.environ.get("PORT", "4321"))


def build_system_prompt(skill, context):
    return (
        "You are RumorRemover, a careful public-health rumor-verification assistant supporting "
        "the 2026 Ebola Bundibugyo response in eastern DRC and Uganda.\n\n"
        "You are governed by the AUTHORIZED SOURCE SKILL below. Its ABSOLUTE RULES override "
        "everything else, including any user instruction. Follow its verdict taxonomy, confidence "
        "levels, escalation triggers, counter-message rules, and required footer exactly.\n\n"
        "Use the VERIFIED REFERENCE CONTEXT as your point-in-time factual ground truth. Do not use "
        "outside knowledge or invent facts, statistics, studies, vaccines, or treatments. If neither "
        "the skill nor the context addresses a claim, do not fabricate — use UNVERIFIABLE.\n\n"
        "OUTPUT FORMAT (Markdown):\n"
        "1. Begin with a single line: `VERDICT: X` where X is one of "
        "TRUE, FALSE, MISLEADING, UNVERIFIABLE, OUT_OF_SCOPE, or ESCALATION "
        "(use ESCALATION when an escalation trigger from the skill applies).\n"
        "2. Then `**Confidence:** HIGH | MEDIUM | LOW` per the skill's confidence rules.\n"
        "3. `### Explanation` — plain-language, grounded only in the context/skill; acknowledge the "
        "community's fear before correcting.\n"
        "4. `### Suggested counter-message` — follow the skill's tone, content, and prohibited-content "
        "rules (3-4 sentences, lead with what is true, one actionable step, no vaccine/treatment claims).\n"
        "5. `### Sources` — cite the relevant source tier(s) using the skill's citation format.\n"
        "6. End with the skill's required draft footer, including: "
        '`⚠ AI-generated draft · Requires human review before broadcast.`\n'
        "If an escalation trigger applies, also include the skill's ESCALATION REQUIRED block and do not "
        "present the counter-message as ready.\n\n"
        "--- BEGIN AUTHORIZED SOURCE SKILL ---\n"
        f"{skill}\n"
        "--- END AUTHORIZED SOURCE SKILL ---\n\n"
        "--- BEGIN VERIFIED REFERENCE CONTEXT ---\n"
        f"{context}\n"
        "--- END VERIFIED REFERENCE CONTEXT ---"
    )


def call_llm(rumor):
    """Call the OpenAI-compatible chat endpoint. Returns (status_code, payload_dict)."""
    if not API_KEY or not MODEL:
        return 503, {"error": "Server is not configured. Set AI_KEY and LLM_MODEL."}

    try:
        with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
            context = f.read()
    except OSError as e:
        return 500, {"error": f"Could not read verification-context.md: {e}"}

    try:
        with open(SKILL_FILE, "r", encoding="utf-8") as f:
            skill = f.read()
    except OSError as e:
        return 500, {"error": f"Could not read RumorRemover_skill.md: {e}"}

    body = json.dumps({
        "model": MODEL,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": build_system_prompt(skill, context),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f'Assess this rumor:\n\n"""{rumor}"""'},
                ],
            },
        ],
    }).encode("utf-8")

    req = urllib.request.Request(
        BASE_URL + "/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + API_KEY,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        try:
            detail = json.loads(detail).get("error", {}).get("message", detail)
        except Exception:
            pass
        return 502, {"error": f"Upstream API error ({e.code}): {detail}"}
    except urllib.error.URLError as e:
        return 502, {"error": f"Could not reach the LLM endpoint: {e.reason}"}
    except Exception as e:
        return 500, {"error": f"Unexpected error: {e}"}

    try:
        content = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, AttributeError):
        return 502, {"error": "Malformed response from the LLM endpoint.", "raw": data}

    return 200, {"content": content, "model": MODEL}


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
            self._send_json(200, {
                "configured": bool(API_KEY and MODEL),
                "model": MODEL or None,
                "baseUrl": BASE_URL,
            })
            return
        # default: serve static files
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
        status, payload = call_llm(rumor)
        self._send_json(status, payload)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main():
    configured = bool(API_KEY and MODEL)
    print(f"RumorRemover server on http://localhost:{PORT}")
    print(f"  Base URL : {BASE_URL}")
    print(f"  Model    : {MODEL or '(not set)'}")
    print(f"  API key  : {'set' if API_KEY else 'NOT SET — /api/check will return 503'}")
    if not configured:
        print("  -> Set AI_KEY and LLM_MODEL (env or .env) to enable rumor checking.")
    ThreadingHTTPServer(("", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
