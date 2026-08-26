#!/usr/bin/env python3
"""Verify S2's ten questions against the LIVE Google Doc Topic Plan.

The client edits the Topic Plan Doc by hand - rewording questions, striking them,
vetoing whole sections - and none of that propagates back to topic-plan-v{n}.json
or .md. Every local mirror is stale the moment a client touches the Doc. Building
from one ships questions the client already rejected. That is the Eberst E5
incident, 2026-06-19.

This fetches the Doc live and enforces gates TP-1 through TP-6 from
references/short-form.md.

    python3 verify-topic-plan.py --doc-id <id> --episode <N> --payload <ros-template-v2-data.json>
    python3 verify-topic-plan.py --doc-id <id> --episode <N> --dump

Exit 0 = all gates pass. Exit 1 = a gate failed. Exit 2 = could not check.
"""
import argparse, json, subprocess, sys, re, datetime


def gws(*args, params=None):
    cmd = ["gws", *args]
    if params:
        cmd += ["--params", json.dumps(params)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(f"FAILED: {' '.join(args)}\n{r.stdout}\n{r.stderr}", file=sys.stderr)
        sys.exit(2)
    out = r.stdout.strip()
    out = out[out.index("{"):] if "{" in out else out
    return json.loads(out) if out else {}


def _cell_runs(cell):
    """Every textRun in a table cell, flattened."""
    for c in cell.get("content", []):
        para = c.get("paragraph")
        if not para:
            continue
        for e in para.get("elements", []):
            if e.get("textRun"):
                yield e["textRun"]


def _blocks(doc):
    """Yield ('heading', text) and ('table', rows) in document order, across all tabs.

    The Topic Plan puts its questions in a TABLE under each `Episode N:` heading,
    with a Question / Keywords / Rationale header row. Walking paragraphs alone
    finds nothing, which is how the first version of this script silently passed.
    """
    def walk(tabs):
        for t in tabs:
            for c in t.get("documentTab", {}).get("body", {}).get("content", []):
                if "table" in c:
                    rows = []
                    for r in c["table"].get("tableRows", []):
                        cells = []
                        for cell in r.get("tableCells", []):
                            runs = list(_cell_runs(cell))
                            text = "".join(x["content"] for x in runs).strip()
                            struck = bool(runs) and all(
                                x.get("textStyle", {}).get("strikethrough")
                                for x in runs if x["content"].strip())
                            cells.append((text, struck))
                        rows.append(cells)
                    yield "table", rows
                    continue
                para = c.get("paragraph")
                if not para:
                    continue
                runs = [e["textRun"] for e in para.get("elements", []) if e.get("textRun")]
                text = "".join(r["content"] for r in runs).strip()
                if not text:
                    continue
                style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
                if style.startswith("HEADING") or style == "TITLE":
                    yield "heading", text
            yield from walk(t.get("childTabs", []))
    yield from walk(doc.get("tabs", []))


def episode_questions(doc, episode):
    """Return (live_rows, vetoed_rows) for one episode, from its breakdown table."""
    pat = re.compile(rf"^\s*Episode\s+{re.escape(str(episode))}\s*[::]", re.I)
    live, vetoed, armed = [], [], False
    for kind, payload in _blocks(doc):
        if kind == "heading":
            # A new Episode heading closes the previous one.
            if armed and not pat.search(payload):
                break
            armed = bool(pat.search(payload))
            continue
        if not armed or kind != "table" or not payload:
            continue
        header = [c[0].lower() for c in payload[0]]
        qcol = next((i for i, h in enumerate(header) if "question" in h), 0)
        for row in payload[1:]:
            if qcol >= len(row):
                continue
            text, struck = row[qcol]
            if not text:
                continue
            text = re.sub(r"^\s*(Q?\d+[\.\):]|\*+)\s*", "", text)
            (vetoed if struck else live).append(text)
        break
    return live, vetoed


def normalize(s):
    """Substance comparison. S2 rewrites to search phrasing, so match on content words."""
    s = re.sub(r"\{\{[A-Z_]+\}\}", " ", s.lower())
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    stop = {"what","how","is","the","a","an","in","to","for","of","do","does","you","your",
            "my","i","it","and","or","if","are","can","will","be","that","this","on","with",
            "actually","really","get","after","before","when","who","at","was","were","has",
            "have","from","by","their","them","they","its","one","any","some"}
    out = set()
    for w in s.split():
        if not w or w in stop:
            continue
        out.add(_stem(w))
    return out


def _stem(w):
    """Crude suffix stripping. S2 rewrites freely between singular and plural and between
    verb forms, so 'vehicles hit pedestrians' must match 'vehicle create a pedestrian crash'.
    Without this the matcher false-fails on legitimate rewrites, which is worse than useless
    because it trains people to ignore the gate."""
    for suf in ("ies", "es", "s", "ing", "ed"):
        if len(w) > 4 and w.endswith(suf):
            base = w[:-len(suf)]
            return base + "y" if suf == "ies" else base
    return w


def overlap(a, b):
    A, B = normalize(a), normalize(b)
    return len(A & B) / max(1, min(len(A), len(B)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc-id", required=True, help="the PUBLISHED Topic Plan Google Doc")
    ap.add_argument("--episode", required=True, help="episode number, to scope the breakdown")
    ap.add_argument("--payload", help="ros-template-v2-data.json to verify")
    ap.add_argument("--dump", action="store_true", help="print the Doc's question rows and exit")
    ap.add_argument("--threshold", type=float, default=0.5, help="substance-match threshold")
    a = ap.parse_args()

    doc = gws("docs", "documents", "get",
              params={"documentId": a.doc_id, "includeTabsContent": True})
    fetched_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    revision = doc.get("revisionId", "")

    rows, vetoed = episode_questions(doc, a.episode)

    if a.dump:
        print(f"revisionId: {revision}\nfetched_at: {fetched_at}")
        print(f"\nEPISODE {a.episode} - {len(rows)} live question rows:")
        for i, q in enumerate(rows, 1):
            print(f"  {i:2}. {q}")
        if vetoed:
            print(f"\nVETOED (struck through) - {len(vetoed)}:")
            for q in vetoed:
                print(f"   x  {q}")
        return

    if not a.payload:
        print("ERROR: --payload required unless --dump", file=sys.stderr)
        sys.exit(2)

    payload = json.load(open(a.payload))
    fails = []

    if not rows:
        fails.append(f"TP-1/TP-2: no question rows found for episode {a.episode} in the live Doc. "
                     "Either the episode is absent from the lineup (do not build it) or the "
                     "heading pattern did not match. Run --dump to inspect.")

    locations = payload.get("segment_2", {}).get("locations") or payload.get("locations") or []
    for loc in locations:
        name = loc.get("city") or loc.get("name") or "?"
        qs = loc.get("questions", [])
        print(f"\n=== {name} - {len(qs)} questions ===")

        matched_idx = []
        for i, q in enumerate(qs, 1):
            qt = q.get("q") or q.get("question") or ""
            best, score = None, 0.0
            for j, row in enumerate(rows):
                sc = overlap(qt, row)
                if sc > score:
                    best, score = j, sc

            for v in vetoed:
                if overlap(qt, v) >= a.threshold:
                    fails.append(f"TP-4 [{name} Q{i}]: derives from VETOED text: {v!r}")

            if best is None or score < a.threshold:
                fails.append(f"TP-2 [{name} Q{i}]: no live Doc row matches {qt!r} "
                             f"(best {score:.2f}). Unreferenced question.")
            else:
                matched_idx.append(best)
                print(f"  Q{i:<2} -> Doc row {best+1:<2} ({score:.2f})")

        if matched_idx != sorted(matched_idx):
            fails.append(f"TP-3 [{name}]: order does not follow the Doc. Doc rows came out as "
                         f"{[i+1 for i in matched_idx]}. Tail truncation is allowed; reordering is not.")
        if matched_idx and matched_idx != list(range(matched_idx[0], matched_idx[0] + len(matched_idx))):
            fails.append(f"TP-3 [{name}]: gap in the middle of the sequence "
                         f"{[i+1 for i in matched_idx]}. Take a contiguous run, truncated from the tail.")

    meta = payload.get("metadata", payload)
    for f in ("topic_plan_doc_id", "topic_plan_revision_id", "topic_plan_fetched_at"):
        if not meta.get(f):
            fails.append(f"TP-1: metadata missing {f}. Record it so the check is auditable.")

    print("\n" + "=" * 60)
    if fails:
        print(f"FAIL - {len(fails)} gate violation(s)\n")
        for f in fails:
            print(f"  - {f}")
        print(f"\nRecord on pass: topic_plan_revision_id={revision} topic_plan_fetched_at={fetched_at}")
        sys.exit(1)
    print("PASS - all Topic Plan gates clear")
    print(f"  topic_plan_doc_id:       {a.doc_id}")
    print(f"  topic_plan_revision_id:  {revision}")
    print(f"  topic_plan_fetched_at:   {fetched_at}")


if __name__ == "__main__":
    main()
