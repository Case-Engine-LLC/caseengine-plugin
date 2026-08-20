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
| `/caseengine:client` | Everything on file for a client — websites, hosting, tracking, team, brand |
| `/caseengine:blogs` | A client's blog inventory: published, scheduled, still an idea |
| `/caseengine:podcast` | Episodes and the run of show for each, and what the slate is waiting on |
| `/caseengine:ebook` | eBook and run-of-show generation runs, and where each one is |
| `/caseengine:approved` | Record a client approval that came in via Slack or an account manager |
| `/caseengine:check` | Run the automated QA checks against a live URL and record the results |
| `/caseengine:queue` | Your queue grouped by what it actually is, not 200 identical rows |

You do not have to use the commands. With the plugin installed, "what's on my
plate in CE?" or "pull Wolf's open tasks" routes correctly on its own.

## The proof harness

A task is not done because the work ran. It is done because someone observed
the outcome. Since 0.4.0 the plugin carries that rule with it, so it arrives by
installing rather than by wiring something into each project.

Four pieces:

- **`/caseengine:prove <task>`** — resolves the task, works out what would
  settle whether it worked, checks it, and writes down what it saw.
- **A `proof` skill** — teaches the discipline, including what counts as
  evidence for each of our deliverables, and applies to ordinary knowledge work
  as much as to websites.
- **A `PreToolUse` gate** — watches for a task being transitioned to `done` or
  `approved` and looks for passing evidence recorded against it.
- **`hooks/checks.py`** — eight automated checks against a live URL (reachable,
  tracking, indexable, sitemap, schema, custom 404, placeholders, https images).
  These are the mechanical half of the QA checklist, and they settle it by
  looking rather than by someone ticking. Dependency-free; `--record` writes each
  verdict to the ledger. Roughly 575 checklist task rows across the corpus are of
  this kind, and since three quarters of all tasks are template redeployments, a
  check written once pays off on every future client.

Two kinds of evidence count. A **verify** is something observed on a public
surface — a URL returned 200, an API confirmed the post. An **attestation** is a
person approving something, captured with who said it, where, and a link. Most
client approvals here are the second kind, and recording whether you heard it
first-hand or it was relayed keeps the chain visible.

Evidence lives in an append-only ledger at
`~/.claude/caseengine/evidence/<date>.jsonl`. Record one directly with:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/hooks/record.py" \
  --task <uuid> --status pass \
  --observed "https://client.com/the-page/" \
  --note "HTTP 200, headline matches the brief"
```

### A note on how the queue actually looks

Worth knowing before relying on any of this. For production staff the queue is
not a list of different jobs — it is a few jobs repeated many times, with
identical names. In current production: Clarence has **207 open tasks with 9
distinct names**, Jennifer **94 with 8**, Melanie **65 with 13**. One cluster is
59 tasks all called `IR: Full Episode Video Approval v1.0`, sharing a milestone
name, with nothing on the task identifying which episode it is.

Management queues look nothing like this — Gabe's 60 open tasks are 60 distinct
names. Tooling built for one of those two shapes does not serve the other.

`/caseengine:queue` groups rather than lists, and says out loud when a cluster is
indistinguishable instead of formatting it prettily. The real fix is upstream:
episode and instance identity belongs on the task.

### Known limits, in plain terms

**The ledger is per-machine.** Evidence recorded on one person's laptop is
invisible to everyone else. If the designer checks a page and the account
manager closes the task, the gate sees nothing and blocks the wrong person.
Point `CASEENGINE_EVIDENCE_DIR` at a shared or synced directory as a stopgap;
the real fix is writing evidence to Supabase next to the task, so it is a fact
about the work rather than a file on somebody's machine.

**It only governs work done through Claude.** Someone clicking Done in the
dashboard never touches this hook. The database trigger on website tasks
governs everything regardless of client — this does not.

**Evidence expires after 72 hours** by default, which covers a weekend. Change
it with `CASEENGINE_EVIDENCE_TTL_HOURS` or `ttl_hours` in `proof.json`.

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

**`caseengine-tasks`, deliverable inventories** — `client_list_blogs`
(`client_content_inventory`), `client_list_podcast_episodes`
(`client_podcast_inventory`, with a derived run of show), `client_list_websites`.
`client_list_generation_runs` (`content_generation_jobs` — eBooks and podcast
run-of-shows; there is no separate eBook table). These are the deliverables
themselves rather than the tasks about them, and they share the tasks OAuth
grant.

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
- **See client approvals that happened in Slack.** `approved_at` reflects only
  dashboard sign-off, and across 928 generation runs just 27 carry one — because
  approvals arrive in Slack or through an account manager and never come back.
  `/caseengine:approved` exists to close that loop, but it only captures what
  somebody bothers to record.
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
