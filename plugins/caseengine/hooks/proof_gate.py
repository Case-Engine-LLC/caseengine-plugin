#!/usr/bin/env python3
"""PreToolUse gate: a task does not reach a completion status without evidence.

The rule this enforces is the one the sitechange packet already enforces for
website work, generalised and moved into the plugin so it arrives by
installation rather than by per-project configuration:

    A task is not done because a job succeeded.
    It is done because somebody observed the outcome.

Scope is deliberately narrow. This looks at exactly one thing — an attempt to
transition a Case Engine task into `done` or `approved` through the dashboard's
MCP tools. It never inspects file edits, shell commands, or anything else. If
you want the broader website-mutation gate, that is sitechange_guard.py in
caseengine-cli; this is the task-closing half.

MODES
  warn     (default) allow the close, tell the model evidence is missing
  enforce  refuse the close with exit 2 and explain how to record evidence
  off      do nothing

Set with CASEENGINE_PROOF_MODE, or `mode` in ~/.claude/caseengine/proof.json.
Default is warn on purpose: a hard block shipped to everyone on day one would
stop real work before the habit exists. Move to enforce per-person, then
globally, once the evidence path is comfortable.

FAILING OPEN
Every unexpected condition — bad JSON, an unknown tool shape, a missing task id,
an unreadable ledger — allows the call. A hook that guesses wrong must cost
nothing. The only path that ever blocks is: enforce mode, a recognised close
tool, a task id we could read, and no passing observation for it.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ledger import (  # noqa: E402
    COMPLETION_STATUSES,
    append,
    evidence_for_task,
    find_task_id,
    ttl_hours,
)

# The dashboard MCP tools that can finish a task. Suffix-matched so the
# server-prefix form (mcp__caseengine-tasks__work_transition_task) and any
# future namespacing both resolve.
CLOSING_TOOLS = ("work_transition_task", "work_approve_step")

CONFIG_PATH = Path.home() / ".claude" / "caseengine" / "proof.json"


def load_config() -> dict:
    try:
        if CONFIG_PATH.exists():
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def resolve_mode(config: dict) -> str:
    mode = (os.environ.get("CASEENGINE_PROOF_MODE") or config.get("mode") or "warn").strip().lower()
    return mode if mode in {"warn", "enforce", "off"} else "warn"


def is_closing_tool(tool_name: str) -> bool:
    return any(tool_name == t or tool_name.endswith("__" + t) for t in CLOSING_TOOLS)


def target_status(tool_input: dict) -> str:
    for key in ("status", "to_status", "target_status", "new_status"):
        value = tool_input.get(key)
        if isinstance(value, str):
            return value.strip().lower()
    return ""


def allow(reason: str | None = None) -> None:
    """Exit 0. Emits the structured allow envelope when there is something worth
    saying; clients that don't read it simply see a permitted call."""
    if reason:
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "allow",
                        "permissionDecisionReason": reason,
                    }
                }
            )
        )
        sys.stderr.write(reason + "\n")
    sys.exit(0)


def deny(message: str) -> None:
    sys.stderr.write(message + "\n")
    sys.exit(2)


def missing_evidence_message(task_id: str, status: str, enforcing: bool) -> str:
    lead = (
        "BLOCKED by the Case Engine proof gate"
        if enforcing
        else "Case Engine proof gate (warning only)"
    )
    tail = (
        "Record what you observed, then retry."
        if enforcing
        else "This close is being allowed, but nothing was recorded. Record what you observed."
    )
    return (
        f"{lead}: moving task {task_id} to '{status}' with no evidence on record "
        f"from the last {ttl_hours()}h.\n\n"
        "A task is not done because the work ran. It is done because someone "
        "looked at the result. Do that, then write down what you looked at:\n\n"
        "  /caseengine:prove <task>          you checked it yourself\n"
        "  /caseengine:approved <task>       a client approved it in Slack or via an AM\n\n"
        "Or record it directly:\n\n"
        f'  python3 "$CLAUDE_PLUGIN_ROOT/hooks/record.py" \\\n'
        f'    --task {task_id} --status pass \\\n'
        f'    --observed "<the URL, screenshot, id or query you checked>" \\\n'
        f'    --note "<what it showed>"\n\n'
        f"{tail}\n"
        "Genuinely nothing observable here? Re-run with CASEENGINE_PROOF_BYPASS=1 "
        "— that is recorded, not silent."
    )


def main() -> None:
    config = load_config()
    mode = resolve_mode(config)
    if mode == "off":
        sys.exit(0)

    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # never block on malformed input

    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        sys.exit(0)

    if not is_closing_tool(tool_name):
        sys.exit(0)

    status = target_status(tool_input)
    if status not in COMPLETION_STATUSES:
        sys.exit(0)  # movement, not completion

    task_id = find_task_id(tool_input)
    if not task_id:
        sys.exit(0)  # cannot identify the subject; not our place to guess

    if os.environ.get("CASEENGINE_PROOF_BYPASS"):
        append(
            {
                "kind": "bypass",
                "task_id": task_id,
                "status": status,
                "tool": tool_name,
                "note": "closed with CASEENGINE_PROOF_BYPASS set",
            }
        )
        allow(
            f"Case Engine proof gate bypassed for task {task_id}. "
            "The bypass has been recorded in the evidence ledger."
        )

    try:
        evidence = evidence_for_task(task_id)
    except Exception:
        sys.exit(0)  # ledger unreadable — fail open

    if evidence:
        latest = evidence[-1]
        allow(
            f"Case Engine proof gate satisfied for task {task_id}: "
            f"{len(evidence)} passing observation(s) on record, most recently "
            f"{latest.get('observed') or 'an unnamed check'} at {latest.get('ts')}."
        )

    enforcing = mode == "enforce"
    message = missing_evidence_message(task_id, status, enforcing)
    if enforcing:
        deny(message)
    allow(message)


if __name__ == "__main__":
    main()
