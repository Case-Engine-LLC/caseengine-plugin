# Case Engine plugin for Claude

Connects Claude to the **Case Engine dashboard** (`tool.caseengine.com`)
so you can pull your task queue, read tasks and approvals, dump a client
profile, and drive content generation from Claude Chat, Cowork, Desktop, or
Claude Code.

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

Run `/caseengine:connect` and follow it. In short:

1. Click **Connect** or **Sign in** when Claude prompts you.
2. Sign in to <https://tool.caseengine.com>.
3. Review the access request and click **Allow access**.
4. Return to Claude. No key or environment variable is required.

## Commands

| Command | Does |
|---|---|
| `/caseengine:connect` | Sign in with Case Engine and verify the connection end-to-end |
| `/caseengine:my-tasks` | Your open work queue, or one client's |
| `/caseengine:meeting-doc` | Build a client meeting doc from live board data |
| `/caseengine:approvals` | Pending approvals waiting on a decision, or one client's |
| `/caseengine:workload` | Open/overdue/awaiting-review counts per person on the team |
| `/caseengine:prove` | Check that a task's work actually landed, then record what you observed |

You do not have to use the commands. With the plugin installed, "what's on my
plate in CE?" or "pull Wolf's open tasks" routes correctly on its own.

## The proof harness

A task is not done because the work ran. It is done because someone observed
the outcome. Since 0.4.0 the plugin carries that rule with it, so it arrives by
installing rather than by wiring something into each project.

Three pieces:

- **`/caseengine:prove <task>`** — resolves the task, works out what would
  settle whether it worked, checks it, and writes down what it saw.
- **A `proof` skill** — teaches the discipline, including what counts as
  evidence for each of our deliverables, and applies to ordinary knowledge work
  as much as to websites.
- **A `PreToolUse` gate** — watches for a task being transitioned to `done` or
  `approved` and looks for a passing observation recorded against it in the last
  12 hours.

Observations live in an append-only ledger at
`~/.claude/caseengine/evidence/<date>.jsonl`. Record one directly with:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/hooks/record.py" \
  --task <uuid> --status pass \
  --observed "https://client.com/the-page/" \
  --note "HTTP 200, headline matches the brief"
```

### Modes

| `CASEENGINE_PROOF_MODE` | Behaviour |
|---|---|
| `warn` *(default)* | Allows the close, says evidence is missing |
| `enforce` | Refuses the close until an observation exists |
| `off` | Does nothing |

Also settable as `{"mode": "enforce"}` in `~/.claude/caseengine/proof.json`.

It ships in `warn` because a hard block delivered to everyone at once stops real
work before the habit exists. Move individuals to `enforce` as they get
comfortable, then make it the default.

The gate **fails open** on everything it does not understand — an unrecognised
tool, a task id it cannot read, malformed input, an unreadable ledger. The only
path that blocks is: enforce mode, a recognised close tool, a completion status,
a readable task id, and no passing observation. `CASEENGINE_PROOF_BYPASS=1`
allows a call and records the bypass, so an exit is visible rather than silent.

Tests: `python3 plugins/caseengine/hooks/test_proof_gate.py`

## What it can do

**`caseengine-tasks`** — `work_list_items`, `work_get_task`, `work_list_tasks`,
`work_list_people`, `work_team_workload`, `work_list_approvals`,
`client_get_profile`, plus (capability-gated) `work_create_task`,
`work_assign_task`, `work_transition_task`, `work_approve_step`. Creating or
assigning a task to someone else needs no special role beyond the standard
OAuth grant below — resolve their id with `work_list_people` first.

**`caseengine-content`** — list/get content pieces, poll and start generation
jobs, cancel a job, transition a piece.

## What it deliberately can't do

- **Publish to WordPress.** Not exposed. `content_transition_piece` does not
  accept `'published'`.
- **Approve your own work.** Enforced in the underlying service, not just
  here — this holds even though the OAuth grant below includes
  `tasks_approve`.
- **Write content generation through the default OAuth grant.** OAuth access
  for `content_generation` stays read-only.
- **Touch site changes.** Separate superadmin domain, not bundled here.
- **Touch ClickUp.** Retired.
- **Vouch for work it did not check.** The gate reads the evidence ledger; it
  cannot tell whether an observation was honest. That part is on us, and it is
  why the skill leads on not recording something you did not see.

## Security

OAuth is per-user and tied to the Case Engine account that approved access.
Claude receives opaque, short-lived access tokens and rotates refresh tokens;
no Case Engine password or copied API key is stored in the plugin.

## Not to be confused with

The **Content Generator MCP** at `contentgenapi.caseengine.com` — a separate
external server with its own shared secret, configured at
`/content-generation/setup` in the dashboard. Different thing.
