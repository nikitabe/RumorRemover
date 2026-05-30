"""
Shared rumor-verification logic used by both the local server (server.py)
and the Vercel serverless functions (api/check.py, api/health.py).

Dependency-free (Python standard library only). Calls the Anthropic Messages API.

Configuration via environment variables (Vercel project settings, or a local .env):
  AI_KEY     (required) Anthropic API key, sent as the x-api-key header
  BASE_URL   (optional) default: https://api.anthropic.com/v1
  LLM_MODEL  (required) e.g. claude-sonnet-4-6
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

DEFAULT_BASE = "https://api.anthropic.com/v1"
ANTHROPIC_VERSION = "2023-06-01"
# Generous budget: reasoning models (e.g. Kimi) spend tokens on a hidden
# reasoning trace before emitting the answer, so a small cap can truncate
# the actual content. Non-reasoning models only use what they need.
MAX_TOKENS = 8000


def _find_file(name):
    """Locate a bundled data file across local + serverless layouts."""
    here = os.path.dirname(os.path.abspath(__file__))     # .../api
    root = os.path.dirname(here)                           # repo root / /var/task
    candidates = [
        os.path.join(root, name),
        os.path.join(here, name),
        os.path.join(os.getcwd(), name),
        name,
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(f"{name} not found in: {candidates}")


def _read_dotenv():
    """Parse the local .env fresh (if present) so config — including the model —
    can be switched between requests without restarting. On hosts without a .env
    file (e.g. Vercel), this returns {} and we fall back to os.environ."""
    here = os.path.dirname(os.path.abspath(__file__))
    for path in (os.path.join(os.path.dirname(here), ".env"), os.path.join(os.getcwd(), ".env")):
        if os.path.exists(path):
            vals = {}
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, _, v = line.partition("=")
                        vals[k.strip()] = v.strip().strip('"').strip("'")
            except OSError:
                pass
            return vals
    return {}


def get_config():
    # .env (read per call) takes precedence; otherwise the process environment.
    env = _read_dotenv()
    def g(key, default=""):
        return env.get(key) or os.environ.get(key, default)
    return {
        "base_url": g("BASE_URL", DEFAULT_BASE).rstrip("/"),
        "api_key": g("AI_KEY", ""),
        "model": g("LLM_MODEL", ""),
    }


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


def health():
    cfg = get_config()
    return {
        "configured": bool(cfg["api_key"] and cfg["model"]),
        "model": cfg["model"] or None,
        "baseUrl": cfg["base_url"],
    }


def list_models():
    """List model ids available from the configured provider. Returns (status, payload)."""
    cfg = get_config()
    if not cfg["api_key"]:
        return 503, {"error": "Server is not configured. Set AI_KEY."}
    is_anthropic = "anthropic.com" in cfg["base_url"]
    endpoint = cfg["base_url"] + "/models"
    headers = (
        {"x-api-key": cfg["api_key"], "anthropic-version": ANTHROPIC_VERSION}
        if is_anthropic else {"authorization": "Bearer " + cfg["api_key"]}
    )
    req = urllib.request.Request(endpoint, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return 502, {"error": f"Could not list models ({e.code}).", "current": cfg["model"], "models": []}
    except Exception as e:
        return 502, {"error": f"Could not list models: {e}", "current": cfg["model"], "models": []}
    items = data.get("data", data if isinstance(data, list) else [])
    ids = sorted({m.get("id") for m in items if isinstance(m, dict) and m.get("id")})
    return 200, {"models": ids, "current": cfg["model"]}


def call_llm(rumor, model=None):
    """Verify a rumor. `model` (optional) overrides the configured model for this
    request. Returns (status_code, payload_dict)."""
    cfg = get_config()
    model = (model or "").strip() or cfg["model"]
    if not cfg["api_key"] or not model:
        return 503, {"error": "Server is not configured. Set AI_KEY and LLM_MODEL."}

    overall_start = time.monotonic()
    try:
        with open(_find_file("verification-context.md"), "r", encoding="utf-8") as f:
            context = f.read()
        with open(_find_file("RumorRemover_skill.md"), "r", encoding="utf-8") as f:
            skill = f.read()
    except OSError as e:
        return 500, {"error": f"Could not read reference files: {e}"}

    system_prompt = build_system_prompt(skill, context)
    user_text = f'Assess this rumor:\n\n"""{rumor}"""'
    is_anthropic = "anthropic.com" in cfg["base_url"]

    if is_anthropic:
        # Anthropic Messages API: system is a top-level field; auth via x-api-key.
        endpoint = cfg["base_url"] + "/messages"
        body = json.dumps({
            "model": model,
            "max_tokens": MAX_TOKENS,
            "temperature": 0.2,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": user_text}]},
            ],
        }).encode("utf-8")
        headers = {
            "content-type": "application/json",
            "x-api-key": cfg["api_key"],
            "anthropic-version": ANTHROPIC_VERSION,
        }
    else:
        # OpenAI-compatible Chat Completions (e.g. Nebius Token Factory).
        endpoint = cfg["base_url"] + "/chat/completions"
        body = json.dumps({
            "model": model,
            "max_tokens": MAX_TOKENS,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [{"type": "text", "text": user_text}]},
            ],
        }).encode("utf-8")
        headers = {
            "content-type": "application/json",
            "authorization": "Bearer " + cfg["api_key"],
        }

    req = urllib.request.Request(endpoint, data=body, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        try:
            detail = json.loads(detail).get("error", {}).get("message", detail)
        except Exception:
            pass
        sys.stderr.write(
            f"[LLM ERROR] {e.code} from {endpoint} "
            f"(key prefix {cfg['api_key'][:10]!r}, len {len(cfg['api_key'])}): {detail}\n"
        )
        return 502, {"error": f"Upstream API error ({e.code}): {detail}"}
    except urllib.error.URLError as e:
        sys.stderr.write(f"[LLM ERROR] could not reach endpoint: {e.reason}\n")
        return 502, {"error": f"Could not reach the LLM endpoint: {e.reason}"}
    except Exception as e:
        sys.stderr.write(f"[LLM ERROR] unexpected: {e}\n")
        return 500, {"error": f"Unexpected error: {e}"}

    try:
        if is_anthropic:
            content = "".join(
                b.get("text", "") for b in data["content"] if b.get("type") == "text"
            ).strip()
        else:
            content = data["choices"][0]["message"]["content"].strip()
        if not content:
            raise ValueError("empty content")
    except (KeyError, IndexError, AttributeError, TypeError, ValueError):
        return 502, {"error": "Malformed response from the LLM endpoint.", "raw": data}

    elapsed_ms = round((time.monotonic() - overall_start) * 1000)
    return 200, {"content": content, "model": model, "elapsedMs": elapsed_ms}
