"""Shared evidence ledger for the Case Engine proof harness.

An *observation* is the thing somebody looked at to satisfy themselves a piece
of work actually landed: a URL that returned 200, a screenshot, an API response,
a row count. The ledger is where those observations are kept between the moment
they are made and the moment a task is closed on the strength of them.

It is deliberately local, append-only, and boring. It is not the system of
record — Supabase is. The ledger exists so a close attempt can answer one
question without a network round trip: *was anything actually observed for this
task, recently, in this session?*

Location: ~/.claude/caseengine/evidence/<YYYY-MM-DD>.jsonl
Override with CASEENGINE_EVIDENCE_DIR (used by the tests).
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCHEMA = "caseengine.evidence.v1"

# How long evidence stays good for.
#
# Originally 12 hours, which was wrong for how people actually work. A client
# approves something on Friday afternoon and the account manager closes it out
# Monday morning; under a 12-hour window that approval had expired and the
# person got blocked for doing nothing wrong. 72 hours covers a weekend, which
# is the shortest span that survives contact with a real week.
#
# Override with CASEENGINE_EVIDENCE_TTL_HOURS, or `ttl_hours` in proof.json.
DEFAULT_TTL_HOURS = 72


def ttl_hours(default: int = DEFAULT_TTL_HOURS) -> int:
    """Resolve the evidence window: env, then config file, then the default."""
    raw = os.environ.get("CASEENGINE_EVIDENCE_TTL_HOURS")
    if not raw:
        try:
            config_path = Path.home() / ".claude" / "caseengine" / "proof.json"
            if config_path.exists():
                raw = json.loads(config_path.read_text(encoding="utf-8")).get("ttl_hours")
        except Exception:
            raw = None
    try:
        value = int(raw)
        return value if value > 0 else default
    except (TypeError, ValueError):
        return default

# Statuses that mean "this work is finished" and therefore need evidence behind
# them. Mirrors TASK_TRANSITION_STATUSES in the webapp; anything not listed here
# (todo, in_progress, blocked, cancelled) is movement, not completion.
COMPLETION_STATUSES = {"done", "approved"}

UUID_RE = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I
)


def now() -> datetime:
    return datetime.now(timezone.utc)


def evidence_dir() -> Path:
    """Where the ledger lives.

    Defaults to this machine, which is the honest limitation of this version:
    evidence recorded on one person's laptop is invisible to everybody else. If
    the designer checks a page and the account manager closes the task, the gate
    sees nothing and blocks the wrong person.

    Pointing CASEENGINE_EVIDENCE_DIR at a shared or synced directory makes a
    team share one ledger, which is a workable stopgap. The real fix is writing
    evidence to Supabase alongside the task so it is simply a fact about the
    work rather than a file on somebody's machine.
    """
    override = os.environ.get("CASEENGINE_EVIDENCE_DIR")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".claude" / "caseengine" / "evidence"


def ledger_path(when: datetime | None = None) -> Path:
    when = when or now()
    return evidence_dir() / f"{when:%Y-%m-%d}.jsonl"


def append(entry: dict) -> None:
    """Append one observation. Never raises — a hook must not break a session
    because a disk write failed."""
    try:
        entry.setdefault("schema", SCHEMA)
        entry.setdefault("ts", now().isoformat(timespec="seconds"))
        path = ledger_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, sort_keys=True) + "\n")
    except Exception:
        pass


def read_recent(hours: int | None = None) -> list[dict]:
    """Every piece of evidence still inside the window. Reads back far enough
    to cover the window itself, so a Friday approval is still there on Monday."""
    window = hours if hours is not None else ttl_hours()
    cutoff = now() - timedelta(hours=window)
    entries: list[dict] = []
    for day_offset in range(0, int(window / 24) + 2):
        path = ledger_path(now() - timedelta(days=day_offset))
        if not path.exists():
            continue
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ts = entry.get("ts")
                if not ts:
                    continue
                try:
                    when = datetime.fromisoformat(ts)
                except ValueError:
                    continue
                if when.tzinfo is None:
                    when = when.replace(tzinfo=timezone.utc)
                if when >= cutoff:
                    entries.append(entry)
        except Exception:
            continue
    return entries


# Two things count as evidence, and they are not the same thing.
#
#   verify       something was observed on a public surface — a URL returned
#                200, an API confirmed the post, the PDF downloaded
#   attestation  a person said yes, and we captured who, when and where
#
# Attestations exist because a large share of Case Engine approvals arrive in
# Slack or come relayed by an account manager. There is no public surface to
# fetch for "the client is happy with the draft" — the evidence is the message.
# Refusing to record those would not make them more rigorous, it would just
# keep the strongest signal we have out of the system.
EVIDENCE_KINDS = ("verify", "attestation")


def evidence_for_task(task_id: str, hours: int | None = None) -> list[dict]:
    """Evidence bound to this task and still in date. Matching is exact on the
    task id — a screenshot of a different page is not evidence for this ticket,
    which is the whole point."""
    if not task_id:
        return []
    needle = task_id.strip().lower()
    return [
        e
        for e in read_recent(hours)
        if str(e.get("task_id", "")).strip().lower() == needle
        and e.get("kind") in EVIDENCE_KINDS
        and passing(e.get("status"))
    ]


PASS_STATUSES = {"pass", "passed", "ok", "complete", "completed", "verified"}


def passing(status) -> bool:
    return str(status or "").strip().lower() in PASS_STATUSES


def find_task_id(payload) -> str | None:
    """Pull a task id out of a tool_input without knowing its exact shape.

    Tool schemas drift; this hook must not become the reason a rename breaks
    everyone's close path. Preferred keys first, then any UUID-shaped value.
    """
    if not isinstance(payload, dict):
        return None
    for key in ("task_id", "taskId", "id", "campaign_task_id"):
        value = payload.get(key)
        if isinstance(value, str) and UUID_RE.fullmatch(value.strip()):
            return value.strip()
    for value in payload.values():
        if isinstance(value, str):
            match = UUID_RE.search(value)
            if match:
                return match.group(0)
    return None
