# Session hooks (contrib — not loaded by the plugin)

Nothing here is registered in `hooks/hooks.json`. These files are **not**
executed by installing the plugin; they are versioned here so a workstation
can be rebuilt and so the setup is reviewable. They are Windows/PowerShell and
carry machine-specific absolute paths and a hard-coded person id — read them
before copying, do not assume they run as-is elsewhere.

## What problem they solve

A session was answering task questions out of whatever context happened to load
at startup — a personal brain snapshot, handoff notes — instead of the actual
queue. These make the queue load first and label everything else as background.

| File | Role |
|---|---|
| `load-native-tasks.ps1` | SessionStart. Emits Connor's open `campaign_task` rows as the leading context block, explicitly labelled as the authoritative queue. |
| `load-brain-context.ps1` | SessionStart. The pre-existing brain loader, with a framing line prepended inside `additionalContext` so it reads as background, never as work. |
| `session-regrounding.CLAUDE.md` | The `~/.claude/CLAUDE.md` re-grounding block. It reloads reliably across `/clear`, so it restates the same split for when a hook silently no-ops. |

Install by copying the two `.ps1` files to `~/.claude/hooks/` and registering
them under `hooks.SessionStart` in `~/.claude/settings.json` with matcher
`startup|resume|clear|compact` — **`load-native-tasks.ps1` first**, so the
queue block lands above the brain block.

## Caveat: the task pull does not go through this plugin

`load-native-tasks.ps1` queries `public.campaign_task` on Supabase directly
(via `caseengine-cli/sbsql.py`, the Management API). That deliberately sidesteps
`work_list_items`, and it contradicts the rule in `skills/caseengine/SKILL.md`
that the dashboard is reached through MCP and not through a Supabase query.

The reason is narrow: a SessionStart hook runs before — and independently of —
MCP auth, so it cannot call `work_list_items` at all, and an unauthorized
session would otherwise start with no queue. It covers **delivery rows only**,
not marker / request / approval items, and it is a snapshot for orientation.

Anything interactive should still go through `/caseengine:my-tasks` and the
MCP aggregator. If SessionStart ever gains access to authenticated MCP tools,
this fallback should be deleted rather than kept in parallel.
