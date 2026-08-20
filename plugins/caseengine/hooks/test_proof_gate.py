#!/usr/bin/env python3
"""Tests for the proof gate.

Run: python3 plugins/caseengine/hooks/test_proof_gate.py

The gate sits in front of every task close, so the property that matters most
is not that it blocks — it is that it *only* blocks in the one situation it is
meant to, and allows everything else including its own failures.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE = HERE / "proof_gate.py"
RECORD = HERE / "record.py"

TASK = "005de0fd-b2bb-4a61-9d5a-a534137f7c9e"
OTHER_TASK = "4b536373-6aa5-4d69-8c73-ce5d79089602"

passed = 0
failed: list[str] = []


def run_gate(payload, env_extra=None, raw=None):
    env = dict(os.environ)
    env.update(env_extra or {})
    stdin = raw if raw is not None else json.dumps(payload)
    proc = subprocess.run(
        [sys.executable, str(GATE)],
        input=stdin,
        capture_output=True,
        text=True,
        env=env,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def record(task, status="pass", observed="https://example.com/", env_extra=None):
    env = dict(os.environ)
    env.update(env_extra or {})
    subprocess.run(
        [
            sys.executable, str(RECORD),
            "--task", task,
            "--status", status,
            "--observed", observed,
            "--note", "test observation",
        ],
        capture_output=True, text=True, env=env, check=True,
    )


def check(name, condition, detail=""):
    global passed
    if condition:
        passed += 1
        print(f"  ok   {name}")
    else:
        failed.append(name)
        print(f"  FAIL {name}{(' — ' + detail) if detail else ''}")


def close_call(task=TASK, status="done", tool="mcp__caseengine-tasks__work_transition_task"):
    return {"tool_name": tool, "tool_input": {"task_id": task, "status": status}}


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        env = {"CASEENGINE_EVIDENCE_DIR": tmp, "CASEENGINE_PROOF_MODE": "enforce"}
        warn = dict(env, CASEENGINE_PROOF_MODE="warn")
        off = dict(env, CASEENGINE_PROOF_MODE="off")

        print("\nfails open on anything it doesn't understand")
        rc, _ = run_gate(None, env, raw="not json at all")
        check("malformed stdin allows", rc == 0, f"rc={rc}")
        rc, _ = run_gate({"tool_name": "Bash", "tool_input": {"command": "ls"}}, env)
        check("unrelated tool allows", rc == 0, f"rc={rc}")
        rc, _ = run_gate({"tool_name": "mcp__caseengine-tasks__work_list_items", "tool_input": {}}, env)
        check("read-only CE tool allows", rc == 0, f"rc={rc}")
        rc, _ = run_gate(close_call(status="in_progress"), env)
        check("non-completion transition allows", rc == 0, f"rc={rc}")
        rc, _ = run_gate({"tool_name": "mcp__caseengine-tasks__work_transition_task",
                          "tool_input": {"status": "done"}}, env)
        check("no identifiable task id allows", rc == 0, f"rc={rc}")
        rc, _ = run_gate({"tool_name": "mcp__caseengine-tasks__work_transition_task",
                          "tool_input": "not-a-dict"}, env)
        check("malformed tool_input allows", rc == 0, f"rc={rc}")

        print("\nblocks exactly the case it is for")
        rc, out = run_gate(close_call(), env)
        check("close with no evidence denies", rc == 2, f"rc={rc}")
        check("denial names the task", TASK in out)
        check("denial tells you what to run", "/caseengine:prove" in out)

        rc, _ = run_gate(close_call(status="approved"), env)
        check("approve with no evidence denies", rc == 2, f"rc={rc}")
        rc, _ = run_gate(close_call(tool="mcp__caseengine-tasks__work_approve_step"), env)
        check("approve_step with no evidence denies", rc == 2, f"rc={rc}")

        print("\nevidence satisfies it")
        record(TASK, observed="https://panterlaw.com/expect-mediation-personal-injury-case/", env_extra=env)
        rc, out = run_gate(close_call(), env)
        check("close after recording allows", rc == 0, f"rc={rc}")
        check("allow message cites the observation", "panterlaw.com" in out)

        print("\nevidence is not transferable")
        rc, _ = run_gate(close_call(task=OTHER_TASK), env)
        check("other task still denied", rc == 2, f"rc={rc}")

        print("\na failing observation is not proof")
        record(OTHER_TASK, status="failed", observed="https://example.com/broken", env_extra=env)
        rc, _ = run_gate(close_call(task=OTHER_TASK), env)
        check("failed observation does not satisfy", rc == 2, f"rc={rc}")

        print("\nmodes")
        with tempfile.TemporaryDirectory() as tmp2:
            w = {"CASEENGINE_EVIDENCE_DIR": tmp2, "CASEENGINE_PROOF_MODE": "warn"}
            rc, out = run_gate(close_call(), w)
            check("warn allows but says so", rc == 0 and "proof gate" in out.lower(), f"rc={rc}")
        with tempfile.TemporaryDirectory() as tmp3:
            o = {"CASEENGINE_EVIDENCE_DIR": tmp3, "CASEENGINE_PROOF_MODE": "off"}
            rc, out = run_gate(close_call(), o)
            check("off is silent", rc == 0 and out.strip() == "", f"rc={rc} out={out!r}")
        with tempfile.TemporaryDirectory() as tmp4:
            b = {"CASEENGINE_EVIDENCE_DIR": tmp4, "CASEENGINE_PROOF_MODE": "enforce",
                 "CASEENGINE_PROOF_BYPASS": "1"}
            rc, out = run_gate(close_call(), b)
            check("bypass allows", rc == 0, f"rc={rc}")
            ledger = list(Path(tmp4).glob("*.jsonl"))
            recorded = any("bypass" in p.read_text() for p in ledger)
            check("bypass is recorded, not silent", recorded)

    print(f"\n{passed} passed, {len(failed)} failed")
    for name in failed:
        print(f"  - {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
