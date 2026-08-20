#!/usr/bin/env python3
"""The two draft checks a model cannot do by reading.

Everything about *style* — the banned-phrase blocklist, the 48 Algorithmic
Authorship rules, heading integration, bold usage, clause placement — lives in
the `legal-content-review` and `algorithmic-authorship` skills this plugin
ships. Claude reads those and applies them with judgment, which is better than
a regex and, more importantly, stays correct when Maja edits the skill. A copy
of her rules in Python would be wrong the first week she changed one.

What is left here is the part reading cannot do:

  uniqueness    word-shingle overlap against the client's other drafts, the
                same method and 60% floor as uniqueness_checker.py on the VPS
  city density  counting one token across a long document

This runs the checkable half so the draft that gets sent is the draft that gets
accepted, instead of coming back a day later with the same five notes.

    content_check.py --file draft.md --city "Santa Ana" --against output/hess_law/

Reads markdown or plain text; for a Google Doc, export as markdown or paste the
body into a file first. Dependency-free.

What it cannot judge: whether the writing is any good, whether the argument
holds, whether a client will like it. That is the editor's job and always was.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NUMBER_WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
                "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
                "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty"]


def finding(rule: str, ok: bool, detail: str, fix: str = "") -> dict:
    return {"rule": rule, "status": "pass" if ok else "fail", "detail": detail, "fix": fix}


def headings(text: str) -> list[tuple[int, str]]:
    """(level, title) for markdown ATX headings and HTML h1-h6."""
    found = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)", line.strip())
        if m:
            found.append((len(m.group(1)), m.group(2).strip()))
            continue
        m = re.search(r"<h([1-6])[^>]*>(.*?)</h\1>", line, re.I)
        if m:
            found.append((int(m.group(1)), re.sub(r"<[^>]+>", "", m.group(2)).strip()))
    return found


def check_city_density(text: str, args) -> list[dict]:
    if not args.city:
        return [finding("city mentioned 20+ times", True, "no --city given, skipped", "")]
    n = len(re.findall(re.escape(args.city), text, re.I))
    return [finding("city mentioned 20+ times", n >= 20, f"{args.city} appears {n}×",
                    "Guide asks for 20+ mentions across the article.")]


def _shingles(text: str, n: int = 5) -> set:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {tuple(words[i:i + n]) for i in range(max(0, len(words) - n + 1))}


def check_uniqueness(text: str, args) -> list[dict]:
    """Uniqueness against the client's other drafts, the way the VPS checker does it.

    The engine reuses the same sentence skeletons across a client's city and
    practice-area pages, and that is the biggest controllable cause of a low
    originality score. Word-shingle overlap against sibling files catches it
    before anything reaches a paid scanner.
    """
    if not args.against:
        return [finding("uniqueness vs sibling pages", True,
                        "no --against directory given, skipped", "")]
    folder = Path(args.against).expanduser()
    if not folder.is_dir():
        return [finding("uniqueness vs sibling pages", True, f"{folder} is not a directory", "")]
    mine = _shingles(text)
    if not mine:
        return [finding("uniqueness vs sibling pages", True, "draft too short to score", "")]
    worst, worst_name = 0.0, ""
    for sib in sorted(folder.glob("*.md")):
        if sib.resolve() == Path(args.file).expanduser().resolve():
            continue
        overlap = len(mine & _shingles(sib.read_text(encoding="utf-8", errors="replace")))
        score = overlap / len(mine)
        if score > worst:
            worst, worst_name = score, sib.name
    unique_pct = round((1 - worst) * 100)
    return [finding(f"uniqueness ≥ {args.threshold}%", unique_pct >= args.threshold,
                    f"{unique_pct}% unique"
                    + (f"; closest sibling {worst_name} shares {round(worst * 100)}%" if worst_name else ""),
                    "Rewrite the repeated passages — reused skeletons across a client's "
                    "pages are the main cause of low originality scores.")]


CHECKS = [check_city_density, check_uniqueness]


def main() -> int:
    ap = argparse.ArgumentParser(description="Pre-submission checklist for a content draft.")
    ap.add_argument("--file", required=True, help="markdown or text file holding the draft")
    ap.add_argument("--city", default="", help="target city, for the H1 and density rules")
    ap.add_argument("--against", default="",
                    help="directory of the client's other drafts, for the uniqueness score")
    ap.add_argument("--threshold", type=int, default=60,
                    help="minimum uniqueness percent (default 60, matching the pipeline)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        text = Path(args.file).expanduser().read_text(encoding="utf-8")
    except Exception as exc:
        print(f"could not read {args.file}: {exc}", file=sys.stderr)
        return 2

    results: list[dict] = []
    for check in CHECKS:
        results.extend(check(text, args))
    failed = [r for r in results if r["status"] == "fail"]

    if args.json:
        print(json.dumps({"file": args.file, "passed": len(results) - len(failed),
                          "failed": len(failed), "results": results}, indent=2))
        return 1 if failed else 0

    print(f"\npre-submission check · {args.file}")
    if failed:
        print(f"\n{len(failed)} to fix before sending:\n")
        for r in failed:
            print(f"  ✗ {r['rule']}")
            print(f"      {r['detail']}")
            if r["fix"]:
                print(f"      → {r['fix']}")
    passes = [r for r in results if r["status"] == "pass"]
    if passes:
        print(f"\n{len(passes)} clean: " + ", ".join(r["rule"] for r in passes))
    print(f"\n{len(passes)} passed, {len(failed)} failed")
    if not failed:
        print("Ready to send.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
