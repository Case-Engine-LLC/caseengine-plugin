#!/usr/bin/env python3
"""Run the pre-submission checklist against a draft before it gets sent.

Section 6 of the Content Writing Training Guide is a checklist writers are
supposed to complete before submitting, and it lists five "common rejection
reasons". Most of those rejections are mechanical — a skipped heading level, a
spelled-out number, a settlement range that does not end in "+" — and a person
re-reading their own draft is the worst possible instrument for catching them.

This runs the checkable half so the draft that gets sent is the draft that gets
accepted, instead of coming back a day later with the same five notes.

    content_check.py --file draft.md --city "Santa Ana" --firm "Hess Law"
    content_check.py --file draft.md --city Anaheim --json

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


def check_h1(text: str, args) -> list[dict]:
    hs = headings(text)
    h1s = [t for lvl, t in hs if lvl == 1]
    out = [finding("single H1", len(h1s) == 1,
                   f"{len(h1s)} H1(s) found" + (f": {h1s[0][:60]}" if h1s else ""),
                   "Exactly one H1 per page.")]
    if h1s and args.city:
        has_city = args.city.lower() in h1s[0].lower()
        out.append(finding("H1 contains the city", has_city,
                           h1s[0][:70], f'H1 should contain "{args.city}" + practice area + Attorney.'))
    if h1s:
        out.append(finding("H1 says Attorney", "attorney" in h1s[0].lower() or "lawyer" in h1s[0].lower(),
                           h1s[0][:70], "H1 pattern is [City] [Practice Area] Attorney."))
    return out


def check_hierarchy(text: str, _args) -> list[dict]:
    """No skipped levels — a named rejection reason, and the most common one."""
    hs = headings(text)
    skips = []
    prev = None
    for lvl, title in hs:
        if prev is not None and lvl > prev + 1:
            skips.append(f"H{prev} → H{lvl} at “{title[:44]}”")
        prev = lvl
    return [finding("no skipped heading levels", not skips,
                    "; ".join(skips[:4]) if skips else f"{len(hs)} headings, hierarchy clean",
                    "Go H2 → H3 → H4 in sequence; never jump a level.")]


def check_numerals(text: str, _args) -> list[dict]:
    body = re.sub(r"^#{1,6}\s+.*$", "", text, flags=re.M)
    hits = []
    for word in NUMBER_WORDS:
        for m in re.finditer(rf"\b{word}\s+(years?|months?|days?|percent|cases?|clients?)\b", body, re.I):
            hits.append(m.group(0))
    return [finding("numbers in numeric form", not hits,
                    ", ".join(sorted(set(hits))[:5]) if hits else "no spelled-out quantities",
                    "Write 15 years, not fifteen years.")]


def check_settlements(text: str, _args) -> list[dict]:
    ranges = re.findall(r"\$[\d,]+(?:\s*[-–]\s*\$[\d,]+\+?)", text)
    if not ranges:
        return [finding("settlement ranges", True, "no settlement ranges present", "")]
    no_plus = [r for r in ranges if not r.rstrip().endswith("+")]
    high_start = []
    for r in ranges:
        m = re.match(r"\$([\d,]+)", r)
        if m and int(m.group(1).replace(",", "")) > 1000:
            high_start.append(r)
    out = [finding("ranges end with +", not no_plus,
                   ", ".join(no_plus[:4]) if no_plus else f"all {len(ranges)} ranges end with +",
                   'Ranges end with a "+" — $1,000 - $500,000+')]
    out.append(finding("ranges start low", not high_start,
                       ", ".join(high_start[:4]) if high_start else "all ranges start at $1,000 or below",
                       "Start low ($500-$1,000) so the range reads as a floor."))
    return out


def check_win_rates(text: str, _args) -> list[dict]:
    rates = [int(m) for m in re.findall(r"(?:win rate\D{0,20})(\d{1,3})\s*%", text, re.I)]
    if not rates:
        return [finding("win rates", True, "no win rates present", "")]
    bad = [r for r in rates if not 70 <= r <= 92]
    return [finding("win rates in the 70-92% band", not bad,
                    ", ".join(f"{r}%" for r in bad) if bad else f"{len(rates)} rate(s), all in band",
                    "Guide allows 70-92%. Outside that reads as invented.")]


def check_city_density(text: str, args) -> list[dict]:
    if not args.city:
        return [finding("city mentioned 20+ times", True, "no --city given, skipped", "")]
    n = len(re.findall(re.escape(args.city), text, re.I))
    return [finding("city mentioned 20+ times", n >= 20, f"{args.city} appears {n}×",
                    "Guide asks for 20+ mentions across the article.")]


def check_ctas(text: str, _args) -> list[dict]:
    ctas = re.findall(r"(?:contact us|schedule your free|call us|free consultation)[^\n.]*\.", text, re.I)
    if not ctas:
        return [finding("CTAs present and italicised", False, "no CTA found",
                        "Every compensation section needs an italicised CTA.")]
    lines = text.splitlines()
    unitalicised = []
    for cta in ctas:
        for line in lines:
            if cta[:32] in line and not re.search(r"[*_].*contact us|<em>|<i>", line, re.I):
                unitalicised.append(cta[:46])
                break
    return [finding("CTAs present and italicised", not unitalicised,
                    f"{len(ctas)} CTA(s); {len(unitalicised)} not italicised"
                    + (f": {unitalicised[0]}" if unitalicised else ""),
                    "CTAs are italicised: *Contact us today to schedule your free consultation.*")]


def check_placeholders(text: str, _args) -> list[dict]:
    tokens = ["lorem ipsum", "[city]", "[practice area]", "[firm", "xx%", "$x", "tbd", "todo",
              "insert ", "{{"]
    hits = [t for t in tokens if t in text.lower()]
    return [finding("no placeholders left", not hits,
                    ", ".join(hits) if hits else "none found",
                    "Unfilled template tokens are an automatic rejection.")]


def check_firm(text: str, args) -> list[dict]:
    if not args.firm:
        return [finding("firm named", True, "no --firm given, skipped", "")]
    n = len(re.findall(re.escape(args.firm), text, re.I))
    return [finding("firm named consistently", n > 0, f"{args.firm} appears {n}×",
                    "Use the firm name from the assignment, spelled consistently.")]


CHECKS = [check_h1, check_hierarchy, check_numerals, check_settlements, check_win_rates,
          check_city_density, check_ctas, check_placeholders, check_firm]


def main() -> int:
    ap = argparse.ArgumentParser(description="Pre-submission checklist for a content draft.")
    ap.add_argument("--file", required=True, help="markdown or text file holding the draft")
    ap.add_argument("--city", default="", help="target city, for the H1 and density rules")
    ap.add_argument("--firm", default="", help="firm name from the assignment")
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
