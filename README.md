# RumorRemover

Open-source rumor triage for the 2026 Ebola Bundibugyo response. A landing page
plus a rumor checker that verifies community claims against a locally-stored,
skill-governed knowledge base using the Anthropic API.

- `index.html` — landing page
- `verify.html` — rumor checker UI (calls `/api/check`)
- `RumorRemover_skill.md` — authoritative governance rules sent to the model
- `verification-context.md` — point-in-time factual reference sent to the model
- `api/_core.py` — shared verification logic (Anthropic Messages API)
- `api/check.py`, `api/health.py` — Vercel serverless functions
- `server.py` — equivalent local dev server (imports `api/_core`)

## Configuration

Set these as environment variables (Vercel) or in a local `.env` (gitignored):

| Variable | Required | Default | Notes |
|---|---|---|---|
| `AI_KEY` | yes | — | Anthropic API key, sent as the `x-api-key` header |
| `LLM_MODEL` | yes | — | e.g. `claude-sonnet-4-6` |
| `BASE_URL` | no | `https://api.anthropic.com/v1` | API base |
| `PORT` | no | `4321` | local server only |

See `.env.example`.

## Run locally

```bash
cp .env.example .env   # then fill in AI_KEY and LLM_MODEL
python3 server.py      # http://localhost:4321
```

No dependencies — Python standard library only.

## Deploy on Vercel

1. Import the repo into Vercel (framework preset: **Other**).
2. In **Project Settings → Environment Variables**, add `AI_KEY`, `LLM_MODEL`,
   and optionally `BASE_URL`.
3. Deploy. Static files are served from the repo root; `api/check.py` and
   `api/health.py` run as Python serverless functions. `vercel.json` bundles the
   two Markdown reference files into the `api/check` function via `includeFiles`.

> Note: `verify.html` requires the `/api/*` functions — a static-only host
> (e.g. GitHub Pages) will not serve the backend.

All AI outputs are drafts and must be reviewed by a qualified human health
officer before broadcast.
