# Scripts - Virality Research

Bundled Python helpers the skill executes when the live-API ingestion tier is reachable. Self-contained, stdlib only - no `pip install` needed.

| Script | Purpose | Env required |
|---|---|---|
| `youtube-virality-fetch.py` | Fetch YouTube video metrics + titles for topic queries via the YouTube Data API v3. Costs 100 quota units per `search.list` call (10K daily quota). Keep topic-level queries to 3-5, not per-question. | `YOUTUBE_API_KEY` |
| `reddit-virality-fetch.py` | Fetch Reddit posts + top comments for topic queries via the Reddit OAuth API. Adds 0.3-0.5s delays between requests. Uses configured User-Agent. | `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET` |

## Credentials - 1Password only

There is no skill-folder `.env` (removed per the CE no-env-files rule). Both scripts read their API keys from environment variables passed by the caller. The caller pulls those values from 1Password at runtime via `op read` and exports them for the script process - it never reads a `.env`.

```bash
YOUTUBE_API_KEY="$(op read 'op://<vault>/<item>/credential')"
REDDIT_CLIENT_ID="$(op read 'op://<vault>/<item>/client_id')"
REDDIT_CLIENT_SECRET="$(op read 'op://<vault>/<item>/client_secret')"
```

## How they're invoked

Both scripts read JSON from stdin, write JSON to stdout.

```bash
echo '{"queries": ["car accident lawyer houston", ...], "max_results": 10}' | \
  YOUTUBE_API_KEY="$YOUTUBE_API_KEY" python3 scripts/youtube-virality-fetch.py

echo '{"queries": ["how do car accident settlements work", ...], "subreddits": ["legaladvice", "personalinjury"]}' | \
  REDDIT_CLIENT_ID="$REDDIT_CLIENT_ID" REDDIT_CLIENT_SECRET="$REDDIT_CLIENT_SECRET" \
  python3 scripts/reddit-virality-fetch.py
```

## Degraded fallback

When the live-API ingestion tier is not reachable (no `op` access, vault locked, missing keys, no skill-folder filesystem in a sandbox), these scripts are skipped entirely; the skill leans on Content Gap MCP + LLM domain knowledge alone. Provenance is marked `youtube_api: skipped`, `reddit_api: skipped` in `metadata.json`.

## Failure handling

If either script fails (network blip, API quota exhausted, credentials missing), the skill marks the source `unreachable` / `skipped` in `metadata.json` and continues with reduced signals. Never block the run on API failure - this skill is OPTIONAL by design.

## Known papercut

If either script still hardcodes a `~/.claude/skills/.../.env` path internally, that is a tracked iteration-log papercut. The scripts must read caller-passed environment variables only - the credential source of truth is 1Password.
