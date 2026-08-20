#!/usr/bin/env python3
"""Run the pre-submission checklist against a draft before it gets sent.

Three rulesets live behind this, and none of them were being checked
automatically: Section 6 of the Content Writing Training Guide (the
pre-submission checklist and its five named rejection reasons), Maja's
legal-content-review skill (the Algorithmic Authorship rules and the banned
phrase blocklist), and the pipeline's own uniqueness threshold. Most of those rejections are mechanical — a skipped heading level, a
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

# Maja's legal-content-review skill: the Algorithmic Authorship blocklist.
# These are "automatic failure" phrases — the replacement matters as much as the
# ban, so the checker hands back what to write instead rather than just objecting.
BANNED = {
    "for example": "integrate the example into the sentence",
    "for instance": "list examples directly after a declaration",
    "maximum compensation": "full compensation",
    "maximum recovery": "fair compensation",
    "maximize your compensation": "the compensation you deserve",
    "maximize recovery": "complete recovery",
    "maximum damages": "fair damages",
    "maximum settlement": "the settlement you're entitled to",
    "maximizing your": "recovering your full",
    "maximizing compensation": "pursuing fair compensation",
    "expert attorney": "experienced attorney",
    "expert lawyer": "skilled lawyer",
    "attorney expert": "knowledgeable attorney",
    "lawyer expert": "seasoned lawyer",
    "our experts": "our attorneys",
    "legal experts": "legal professionals",
    "expertise in": "experience with",
    "specialized expertise": "focused experience",
    "specialist attorney": "qualified attorney",
    "specialist lawyer": "dedicated lawyer",
    "in conclusion": "just state the content",
    "in summary": "just state the content",
    "it's important to note": "state the fact directly",
    "it's crucial to": "state the requirement directly",
    "when it comes to": "remove and rephrase",
    "navigating the": "use a specific action verb",
    "comprehensive approach": "describe the specific actions",
    "complex legal": "be specific about what is complex",
}

# Allowed, but rationed — three per document.
RATIONED = {"such as": 3, "including but not limited to": 3, "moreover": 3,
            "furthermore": 3, "additionally": 3}

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


def check_banned(text: str, _args) -> list[dict]:
    body = text.lower()
    hits = [(b, r) for b, r in BANNED.items() if b in body]
    detail = "; ".join(f'"{b}" → {r}' for b, r in hits[:4])
    if len(hits) > 4:
        detail += f" (+{len(hits) - 4} more)"
    return [finding("no banned phrases", not hits,
                    detail if hits else f"clean against {len(BANNED)} blocked phrases",
                    "Algorithmic Authorship blocklist — these are automatic rejections.")]


def check_rationed(text: str, _args) -> list[dict]:
    body = text.lower()
    over = [f'"{w}" ×{body.count(w)}' for w, cap in RATIONED.items() if body.count(w) > cap]
    return [finding("connectives within their limit", not over,
                    ", ".join(over) if over else "all within 3 per document",
                    "such as / moreover / furthermore / additionally: three per document.")]


def check_em_dash(text: str, _args) -> list[dict]:
    n = len(re.findall(r"—|(?<!-)--(?!-)", text))
    return [finding("no em-dashes", n == 0, f"{n} found" if n else "none",
                    "Use commas, semicolons or parentheses instead.")]


def check_heading_integration(text: str, _args) -> list[dict]:
    """Rule: the first sentence after a heading must pick up words from it."""
    lines = text.splitlines()
    misses = []
    for i, line in enumerate(lines):
        m = re.match(r"^#{2,6}\s+(.*)", line.strip())
        if not m:
            continue
        title = m.group(1)
        words = {w.lower() for w in re.findall(r"[A-Za-z]{4,}", title)}
        if not words:
            continue
        nxt = next((l.strip() for l in lines[i + 1:i + 5]
                    if l.strip() and not l.strip().startswith(("#", "-", "*", "|"))), "")
        if not nxt:
            continue
        first = nxt.split(".")[0].lower()
        if not any(w in first for w in words):
            misses.append(title[:40])
    return [finding("first sentence echoes its heading", not misses,
                    "; ".join(misses[:4]) if misses else "every section opens on its heading",
                    "The sentence after a heading must reuse key words from it.")]


def check_bold_usage(text: str, _args) -> list[dict]:
    """Bold is for headings and list labels only, never mid-paragraph."""
    bad = []
    for line in text.splitlines():
        st = line.strip()
        if not st or st.startswith(("#", "-", "*", "|", ">")):
            continue
        if re.search(r"\*\*[^*]+\*\*", st) and not st.startswith("**"):
            bad.append(st[:52])
    return [finding("bold only on headings and labels", not bad,
                    f"{len(bad)} paragraph(s) with inline bold" + (f": {bad[0]}" if bad else ""),
                    "Bold headings and list headwords; never bold inside prose.")]


def check_clause_placement(text: str, _args) -> list[dict]:
    """Rules 1-2: if/when/because/as clauses move to the END of the sentence."""
    hits = re.findall(r"(?:^|\.\s+)((?:If|When|Because|As)\s+[^.]{10,70}\.)", text)
    return [finding("subordinate clauses at the end", len(hits) <= 2,
                    f"{len(hits)} sentence(s) open with if/when/because/as"
                    + (f': "{hits[0][:50]}"' if hits else ""),
                    "Move the clause to the end: 'You may recover damages if...'")]


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


CHECKS = [check_h1, check_hierarchy, check_numerals, check_settlements, check_win_rates,
          check_city_density, check_ctas, check_placeholders, check_firm,
          check_banned, check_rationed, check_em_dash, check_heading_integration,
          check_bold_usage, check_clause_placement, check_uniqueness]


def main() -> int:
    ap = argparse.ArgumentParser(description="Pre-submission checklist for a content draft.")
    ap.add_argument("--file", required=True, help="markdown or text file holding the draft")
    ap.add_argument("--city", default="", help="target city, for the H1 and density rules")
    ap.add_argument("--firm", default="", help="firm name from the assignment")
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
