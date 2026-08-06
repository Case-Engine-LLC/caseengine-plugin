# Case Engine plugin for Claude Code

Connects Claude Code to the **Case Engine dashboard** (`tool.caseengine.com`)
so you can pull your task queue, read tasks and approvals, dump a client
profile, and drive content generation — without leaving the terminal.

This is why "pull the tasks from the CE dashboard" used to come back *not
connected*: nothing was wired up. This plugin is the wiring.

## Install

```bash
claude plugin marketplace add Case-Engine-LLC/caseengine-plugin
```

```bash
claude plugin install caseengine@caseengine
```

## Connect

> **Heads up — this changes in v0.2.** Pasting a key is temporary. Per-user
> OAuth is being built: you'll sign in to your own Case Engine account in the
> browser and Claude Code will handle the token, with no key to copy and no
> environment variable to set. When that ships, update the plugin, run
> `/caseengine:connect` once more to sign in, and delete
> `CASE_ENGINE_MCP_KEY` — the keys issued below get revoked at cutover.

Run `/caseengine:connect` and follow it. In short:

1. Sign in to <https://tool.caseengine.com>.
2. Open the Copilot widget (bottom-right), click the **plug** icon.
3. Click **Generate my MCP key**, copy the `ce_mcp_...` value — shown once.
4. Put it in your environment as `CASE_ENGINE_MCP_KEY`, then start a fresh
   session.

```powershell
setx CASE_ENGINE_MCP_KEY "ce_mcp_..."
```

```bash
export CASE_ENGINE_MCP_KEY="ce_mcp_..."
```

## Commands

| Command | Does |
|---|---|
| `/caseengine:connect` | Mint a key, set it, verify the connection end-to-end |
| `/caseengine:my-tasks` | Your open work queue, or one client's |
| `/caseengine:meeting-doc` | Build a client meeting doc from live board data |

You do not have to use the commands. With the plugin installed, "what's on my
plate in CE?" or "pull Wolf's open tasks" routes correctly on its own.

## What it can do

**`caseengine-tasks`** — `work_list_items`, `work_get_task`,
`work_list_approvals`, `client_get_profile`, plus (capability-gated)
`work_create_task`, `work_transition_task`, `work_approve_step`.

**`caseengine-content`** — list/get content pieces, poll and start generation
jobs, cancel a job, transition a piece.

## What it deliberately can't do

- **Publish to WordPress.** Not exposed. `content_transition_piece` does not
  accept `'published'`.
- **Approve your own work.** Enforced in the underlying service, not just
  here.
- **Write anything on a read-only key.** Self-serve keys are read-only and
  scoped to `tasks` + `content_generation`. `tasks_write` / `tasks_approve`
  are grants from Connor.
- **Touch site changes.** Separate superadmin domain, not bundled here.
- **Touch ClickUp.** Retired.

## Security

The key is a per-user credential tied to your dashboard account — every write
is attributed to you. Keep it in the environment, never in a repo, never
pasted into a chat. Revoke from the same plugin panel that minted it. Max 5
active keys per user.

## Not to be confused with

The **Content Generator MCP** at `contentgenapi.caseengine.com` — a separate
external server with its own shared secret, configured at
`/content-generation/setup` in the dashboard. Different thing.
