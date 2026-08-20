#!/usr/bin/env python3
"""Write one piece of evidence into the ledger.

This is the whole habit, reduced to a command: when you finish something, say
what you looked at to confirm it worked.

Two kinds. A `verify` is something you observed on a public surface. An
`attestation` is a person approving something, captured with who said it, where,
and a link — which is what most Case Engine client approvals actually are, since
they arrive in Slack or come relayed by an account manager.

    record.py --task <uuid> --status pass \
              --observed "https://client.com/new-page/" \
              --note "HTTP 200, headline matches the brief"

Called by /caseengine:prove, by automations after their verify step, and by
anyone who has just checked something by hand and wants it to count.

An observation needs three things to be worth keeping: what was checked
(--observed), what it showed (--note), and whether that constitutes a pass.
Everything else is bookkeeping this fills in.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ledger import PASS_STATUSES, append, ledger_path, passing  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Record an observation against a Case Engine task."
    )
    parser.add_argument("--task", required=True, help="campaign_task UUID this evidences")
    parser.add_argument(
        "--observed",
        required=True,
        help="what you actually checked — a URL, screenshot path, message id, query",
    )
    parser.add_argument("--note", default="", help="what it showed")
    parser.add_argument(
        "--status",
        default="pass",
        help=f"outcome; passing values are {sorted(PASS_STATUSES)} (default: pass)",
    )
    parser.add_argument("--method", default="", help="how you checked, e.g. 'curl -sI', 'browser'")
    parser.add_argument("--client", default="", help="client slug, if known")
    parser.add_argument(
        "--kind",
        default="verify",
        choices=["verify", "attestation"],
        help="verify = you observed it; attestation = a person approved it and you are recording that",
    )
    parser.add_argument("--approver", default="", help="attestation: who gave the approval")
    parser.add_argument(
        "--channel",
        default="",
        help="attestation: where it arrived — slack, email, call, meeting, account-manager",
    )
    parser.add_argument("--link", default="", help="attestation: permalink to the message or thread")
    parser.add_argument("--relayed-by", default="", dest="relayed_by",
                        help="attestation: who passed it on, if you did not hear it first-hand")
    parser.add_argument("--json", action="store_true", help="emit the entry as JSON")
    args = parser.parse_args()

    entry = {
        "kind": args.kind,
        "task_id": args.task.strip(),
        "status": args.status.strip().lower(),
        "observed": args.observed.strip(),
        "note": args.note.strip(),
        "method": args.method.strip(),
        "client": args.client.strip(),
    }
    if args.kind == "attestation":
        entry.update(
            {
                "approver": args.approver.strip(),
                "channel": args.channel.strip(),
                "link": args.link.strip(),
                "relayed_by": args.relayed_by.strip(),
                # First-hand means we can see the approval ourselves. Relayed
                # means somebody told us. Both are worth having; conflating
                # them is how "the client approved it" survives three retellings
                # without anyone able to point at the original.
                "first_hand": not args.relayed_by.strip(),
            }
        )
    append(entry)

    if args.json:
        print(json.dumps(entry, indent=2, sort_keys=True))
        return 0

    verdict = "PASS" if passing(entry["status"]) else entry["status"].upper()
    label = "attested" if entry["kind"] == "attestation" else "observed"
    print(f"[{verdict}] {entry['kind']} — task {entry['task_id']}")
    print(f"  {label}: {entry['observed']}")
    if entry["kind"] == "attestation":
        who = entry.get("approver") or "unnamed approver"
        where = entry.get("channel") or "unrecorded channel"
        print(f"  approver: {who} via {where}")
        if entry.get("relayed_by"):
            print(f"  relayed by: {entry['relayed_by']} (second-hand)")
        if entry.get("link"):
            print(f"  link:     {entry['link']}")
        elif entry.get("channel") in ("slack", "email"):
            print("  no link recorded — a permalink is what makes this checkable later")
    if entry["note"]:
        print(f"  showed:   {entry['note']}")
    print(f"  ledger:   {ledger_path()}")
    if not passing(entry["status"]):
        print(
            "\n  Note: this is not a passing status, so it will not satisfy the "
            "close gate. That is correct — record it, then fix the thing."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
