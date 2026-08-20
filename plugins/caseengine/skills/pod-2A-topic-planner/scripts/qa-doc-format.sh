#!/usr/bin/env bash
# qa-doc-format.sh
# ---------------------------------------------------------------------------
# Post-render Google Doc QA validator for the pod-2A-topic-planner deliverable.
#
# Fetches a finished topic-plan Google Doc via `gws docs documents get` and runs
# nine mechanical checks against the canonical "what good looks like" spec
# (reference standard: Sutliff & Stout v2 Doc 1DXv0msqUswR4weN0H3tCNYre4ORPZotQ0vILbu1RI6k).
#
# Built 2026-05-21 after a batch of 12 v2 Docs shipped with the branding
# formatter bypassed (pandoc md->docx->Doc workaround). See iteration-log
# entries 2026-05-21-001 and 2026-05-21-002, and the audit report at
# ~/Desktop/claude_code/route/audit-reports/topic-plan-design-disconnect-2026-05-21.md
#
# Each check is mechanical and runnable. Exit 0 = all pass; exit 1 = one or
# more FAILs (every failure printed). Wire this in as the final step of
# `## Ship` so a formatter-bypassed Doc can never ship again.
#
# Usage:
#   qa-doc-format.sh <doc_id>
#
# Exit codes:
#   0  all checks passed
#   1  one or more checks failed
#   2  bad args / usage
#   3  could not fetch the Doc
# ---------------------------------------------------------------------------
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: qa-doc-format.sh <doc_id>" >&2
  exit 2
fi
DOC_ID="$1"

strip_noise() { grep -v '^Using keyring' | grep -v '^Warning:' || true; }

DOC_JSON=$(mktemp -t qa-doc-format-XXXXXX.json)
trap 'rm -f "$DOC_JSON"' EXIT

gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 \
  | strip_noise > "$DOC_JSON"

if ! python3 -c "import json,sys; json.load(open('$DOC_JSON'))" 2>/dev/null; then
  echo "FATAL: could not fetch a valid Doc JSON for $DOC_ID" >&2
  exit 3
fi

python3 - "$DOC_JSON" "$DOC_ID" <<'PYEOF'
import json
import re
import sys

doc_json_path, doc_id = sys.argv[1], sys.argv[2]
doc = json.load(open(doc_json_path))
body = doc.get("body", {}).get("content", [])

CE_BLUE = (0.20784314, 0.4509804, 1.0)
fails = []
passes = []

def approx(c, target, tol=0.04):
    """True if an rgbColor dict c matches target within tolerance."""
    if not c:
        return False
    return (abs(c.get("red", -9) - target[0]) < tol
            and abs(c.get("green", -9) - target[1]) < tol
            and abs(c.get("blue", -9) - target[2]) < tol)

def para_text(el):
    return "".join(r.get("textRun", {}).get("content", "")
                   for r in el.get("paragraph", {}).get("elements", [])).strip()

def para_style(el):
    return el.get("paragraph", {}).get("paragraphStyle", {}).get("namedStyleType", "")

# ---- gather paragraphs / headings -----------------------------------------
paras = [el for el in body if "paragraph" in el]
tables = [el for el in body if "table" in el]
headings = [(para_style(el), para_text(el)) for el in paras
            if para_style(el).startswith("HEADING")]
h2s = [t for s, t in headings if s == "HEADING_2"]
h1s = [t for s, t in headings if s == "HEADING_1"]

# index of the `## Show Identity` heading and the `INTERNAL` H1 in body order
show_identity_i = next((i for i, el in enumerate(body)
                        if "paragraph" in el
                        and para_text(el) == "Show Identity"
                        and para_style(el) == "HEADING_2"), None)
internal_i = next((i for i, el in enumerate(body)
                   if "paragraph" in el
                   and para_text(el).upper() == "INTERNAL"
                   and para_style(el) == "HEADING_1"), None)

# ===========================================================================
# CHECK 1 - cover page present
#   The formatter inserts a cover block (centered text + a page break) before
#   `## Show Identity`. A formatter-bypassed Doc starts with a plain
#   `# Podcast Topic Plan` H1 and has no page break and no centered cover text.
# ===========================================================================
def check_cover():
    if show_identity_i is None:
        return ("FAIL", "no `## Show Identity` heading found - cannot locate cover region")
    pre = body[:show_identity_i]
    has_pagebreak = False
    centered_lines = 0
    for el in pre:
        if "paragraph" not in el:
            continue
        for e in el["paragraph"].get("elements", []):
            if "pageBreak" in e:
                has_pagebreak = True
        align = el["paragraph"].get("paragraphStyle", {}).get("alignment", "")
        if align == "CENTER" and para_text(el):
            centered_lines += 1
    if not has_pagebreak:
        return ("FAIL", "no page break before `## Show Identity` - cover page missing "
                        "(formatter Phase A skipped, likely a pandoc bypass)")
    if centered_lines < 3:
        return ("FAIL", "fewer than 3 centered cover lines before `## Show Identity` "
                        "(found %d) - cover block not built" % centered_lines)
    return ("PASS", "cover page present (%d centered lines + page break)" % centered_lines)

# ===========================================================================
# CHECK 2 - CE logo present on the cover
#   Phase B inserts an inline image on the cover. No inlineObjects = no logo.
# ===========================================================================
def check_logo():
    inline = doc.get("inlineObjects", {})
    if not inline:
        return ("FAIL", "no inline image objects in the Doc - CE logo missing from cover")
    # the cover image lands before `## Show Identity`
    if show_identity_i is not None:
        for el in body[:show_identity_i]:
            if "paragraph" not in el:
                continue
            for e in el["paragraph"].get("elements", []):
                if "inlineObjectElement" in e:
                    return ("PASS", "CE logo present on cover")
    return ("FAIL", "an inline image exists but none before `## Show Identity` - "
                    "CE logo not on the cover")

# ===========================================================================
# CHECK 3 - font is Roboto across the body
#   Phase C + the per-table render set weightedFontFamily=Roboto everywhere.
#   A pandoc Doc keeps the default Arial/Calibri.
# ===========================================================================
def check_font():
    roboto = 0
    other = 0
    other_samples = []
    def scan_runs(elements):
        nonlocal roboto, other
        for e in elements:
            tr = e.get("textRun")
            if not tr or not tr.get("content", "").strip():
                continue
            fam = tr.get("textStyle", {}).get("weightedFontFamily", {}).get("fontFamily", "")
            if fam == "Roboto":
                roboto += 1
            elif fam:
                other += 1
                if len(other_samples) < 3:
                    other_samples.append("%r=%s" % (tr["content"][:24], fam))
            # fam == "" -> inherited/unstyled; not counted as a hard fail
    for el in paras:
        scan_runs(el.get("paragraph", {}).get("elements", []))
    for tel in tables:
        for row in tel["table"].get("tableRows", []):
            for cell in row.get("tableCells", []):
                for para in cell.get("content", []):
                    if "paragraph" in para:
                        scan_runs(para["paragraph"].get("elements", []))
    total = roboto + other
    if total == 0:
        return ("FAIL", "no font-family found on any text run - cannot confirm Roboto")
    # allow a tiny tolerance for stray runs; >5% non-Roboto = formatter skipped
    if other > max(3, total * 0.05):
        return ("FAIL", "%d/%d styled runs are NOT Roboto (e.g. %s) - Roboto pass "
                        "skipped (Phase C bypassed)" % (other, total, "; ".join(other_samples)))
    return ("PASS", "Roboto applied (%d/%d styled runs)" % (roboto, total))

# ===========================================================================
# CHECK 4 - data tables styled (CE Blue header row + zebra body)
#   Phase E. A pandoc Doc ships plain unstyled tables.
# ===========================================================================
def check_tables():
    if not tables:
        return ("FAIL", "no tables found in the Doc")
    bad = []
    checked = 0
    for ti, tel in enumerate(tables):
        rows = tel["table"].get("tableRows", [])
        if len(rows) < 2:
            continue  # skip degenerate 1-row tables
        checked += 1
        # header row background
        hdr_cells = rows[0].get("tableCells", [])
        hdr_blue = any(approx(c.get("tableCellStyle", {})
                              .get("backgroundColor", {})
                              .get("color", {}).get("rgbColor", {}), CE_BLUE)
                       for c in hdr_cells)
        if not hdr_blue:
            bad.append("table #%d header row is not CE Blue" % (ti + 1))
            continue
        # zebra: at least one even-indexed body row shaded non-white
        zebra = False
        for ri in range(2, len(rows), 2):
            for c in rows[ri].get("tableCells", []):
                bg = (c.get("tableCellStyle", {}).get("backgroundColor", {})
                       .get("color", {}).get("rgbColor", {}))
                if bg and not approx(bg, (1.0, 1.0, 1.0), 0.02):
                    zebra = True
        if len(rows) >= 4 and not zebra:
            bad.append("table #%d has no zebra body shading" % (ti + 1))
    if bad:
        return ("FAIL", "tables unstyled - " + "; ".join(bad)
                        + " (Phase E skipped)")
    return ("PASS", "all %d data tables styled (CE Blue header + zebra)" % checked)

# ===========================================================================
# CHECK 5 - `# INTERNAL` marker styled (28pt CE Blue bold + top border)
#   Phase F.
# ===========================================================================
def check_internal_marker():
    if internal_i is None:
        return ("FAIL", "no `INTERNAL` HEADING_1 found - INTERNAL cut marker missing")
    el = body[internal_i]
    pstyle = el["paragraph"].get("paragraphStyle", {})
    has_border = bool(pstyle.get("borderTop"))
    size_ok = False
    color_ok = False
    bold_ok = False
    for e in el["paragraph"].get("elements", []):
        ts = e.get("textRun", {}).get("textStyle", {})
        sz = ts.get("fontSize", {}).get("magnitude", 0)
        if sz >= 20:
            size_ok = True
        rgb = ts.get("foregroundColor", {}).get("color", {}).get("rgbColor", {})
        if approx(rgb, CE_BLUE):
            color_ok = True
        if ts.get("bold"):
            bold_ok = True
    missing = []
    if not size_ok:
        missing.append("not enlarged (<20pt)")
    if not color_ok:
        missing.append("not CE Blue")
    if not bold_ok:
        missing.append("not bold")
    if not has_border:
        missing.append("no top border")
    if missing:
        return ("FAIL", "`INTERNAL` marker unstyled - " + ", ".join(missing)
                        + " (Phase F skipped)")
    return ("PASS", "`INTERNAL` marker styled (28pt CE Blue bold + top border)")

# ===========================================================================
# CHECK 6 - search volume present in the per-episode question tables
#   The `## Episode Breakdown` question tables (episodes 2+) must carry
#   MSV-joined Keywords cells. Defective batch shipped raw n-gram phrases with
#   zero volume. Also flags the wrong column name `Search Phrases`.
# ===========================================================================
def _table_header_texts(tel):
    """Lower-cased text of each cell in a table's row 0."""
    rows = tel["table"].get("tableRows", [])
    if not rows:
        return []
    out = []
    for c in rows[0].get("tableCells", []):
        t = "".join(r.get("textRun", {}).get("content", "")
                    for p in c.get("content", []) if "paragraph" in p
                    for r in p["paragraph"].get("elements", [])).strip().lower()
        out.append(t)
    return out

def _nearest_heading_before(idx):
    """Walk back from body index idx, return the nearest non-empty heading
    text. Tolerant of named-style drift - any paragraph that looks like an
    `Episode N` / `Additional` label counts."""
    for j in range(idx - 1, -1, -1):
        el = body[j]
        if "paragraph" not in el:
            continue
        txt = para_text(el)
        if not txt:
            continue
        if (para_style(el).startswith("HEADING")
                or re.match(r"(Episode|Additional)\b", txt)):
            return txt
    return ""

def check_question_volume():
    # locate the `## Episode Breakdown` heading
    eb_i = next((i for i, el in enumerate(body)
                 if "paragraph" in el
                 and para_text(el) == "Episode Breakdown"
                 and para_style(el) == "HEADING_2"), None)
    if eb_i is None:
        return ("FAIL", "no `## Episode Breakdown` section found")
    end = internal_i if internal_i is not None else len(body)
    # Identify question tables by header SIGNATURE, not by the H3 heading -
    # heading named-style drifts in correctly-rendered Docs. A question table
    # is a 3-col table whose header is Question / (Keywords|Search Phrases) /
    # Rationale. The Episode-1 table is 2-col (Question / Rationale) and is
    # correctly skipped because it never matches the 3-col signature.
    novol = []
    wrong_col = []
    checked = 0
    for i in range(eb_i, end):
        el = body[i]
        if "table" not in el:
            continue
        hdr = _table_header_texts(el)
        if len(hdr) != 3 or hdr[0] != "question" or hdr[2] != "rationale":
            continue  # not a question table (E1 2-col table skipped here)
        if hdr[1] not in ("keywords", "search phrases"):
            continue
        label = _nearest_heading_before(i)[:48] or "(table #%d)" % (checked + 1)
        checked += 1
        if hdr[1] == "search phrases":
            wrong_col.append(label)
        rows = el["table"].get("tableRows", [])
        body_txt = ""
        for row in rows[1:]:
            for c in row.get("tableCells", []):
                for p in c.get("content", []):
                    if "paragraph" in p:
                        body_txt += "".join(
                            r.get("textRun", {}).get("content", "")
                            for r in p["paragraph"].get("elements", []))
        if not re.search(r"/mo", body_txt):
            novol.append(label)
    if checked == 0:
        return ("FAIL", "no per-episode question tables (3-col Question/Keywords/"
                        "Rationale) found under `## Episode Breakdown`")
    msgs = []
    if novol:
        msgs.append("%d question table(s) have ZERO search volume: %s"
                    % (len(novol), "; ".join(novol[:4])))
    if wrong_col:
        msgs.append("%d table(s) use the wrong column name `Search Phrases` "
                    "(canonical is `Keywords`): %s"
                    % (len(wrong_col), "; ".join(wrong_col[:4])))
    if msgs:
        return ("FAIL", " | ".join(msgs)
                        + " - n-gram phrases shipped raw, MSV never joined")
    return ("PASS", "search volume present in all %d question tables" % checked)

# ===========================================================================
# CHECK 7 - section order (client-facing H2s + INTERNAL subsections)
# ===========================================================================
def check_section_order():
    client_canon = ["Show Identity",
                    "Methodology: How topics are selected",
                    "The 12-Episode Plan",
                    "Additional Topics",
                    "Episode Breakdown"]
    internal_canon = ["Research Sources"]  # first H2 under INTERNAL is fixed
    problems = []
    # client-facing: the five canonical H2s must appear in order before INTERNAL
    seen = [h for h in h2s if h in client_canon]
    # de-dup while preserving order
    seen_uniq = []
    for h in seen:
        if h not in seen_uniq:
            seen_uniq.append(h)
    if seen_uniq != client_canon:
        problems.append("client-facing H2 order is %s, expected %s"
                        % (seen_uniq, client_canon))
    # INTERNAL: first H2 after the INTERNAL H1 must be `Research Sources`
    if internal_i is not None:
        first_internal_h2 = next((para_text(el) for el in body[internal_i + 1:]
                                  if "paragraph" in el
                                  and para_style(el) == "HEADING_2"), None)
        if first_internal_h2 != "Research Sources":
            problems.append("first INTERNAL H2 is %r, expected 'Research Sources'"
                            % first_internal_h2)
    if problems:
        return ("FAIL", "section-order drift - " + "; ".join(problems))
    return ("PASS", "section order canonical")

# ===========================================================================
# CHECK 8 - running page header
#   Phase H sets a `Case Engine | Podcast Topic Plan | {anchor}` header.
# ===========================================================================
def check_page_header():
    headers = doc.get("headers", {})
    if not headers:
        return ("FAIL", "Doc has no running page header (Phase H skipped)")
    txt = ""
    for h in headers.values():
        for el in h.get("content", []):
            if "paragraph" in el:
                txt += "".join(r.get("textRun", {}).get("content", "")
                               for r in el["paragraph"].get("elements", []))
    txt = txt.strip()
    if "Case Engine" not in txt or "Podcast Topic Plan" not in txt:
        return ("FAIL", "page header text is %r, expected 'Case Engine | Podcast "
                        "Topic Plan | {anchor}'" % txt)
    return ("PASS", "running page header set (%r)" % txt[:60])

# ===========================================================================
# CHECK 9 - cover date is long-form, not ISO
#   The formatter expects `May 20, 2026`; the pandoc path shipped `2026-05-21`.
# ===========================================================================
def check_date_format():
    if show_identity_i is None:
        return ("FAIL", "cannot locate cover region to check the date")
    for el in body[:show_identity_i]:
        if "paragraph" not in el:
            continue
        t = para_text(el)
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", t):
            return ("FAIL", "cover date %r is ISO format - expected long form "
                            "e.g. 'May 20, 2026'" % t)
    return ("PASS", "cover date not ISO (long form or absent)")

CHECKS = [
    ("1  cover page",            check_cover),
    ("2  CE logo",               check_logo),
    ("3  Roboto font",           check_font),
    ("4  table styling",         check_tables),
    ("5  INTERNAL marker",       check_internal_marker),
    ("6  question-table volume", check_question_volume),
    ("7  section order",         check_section_order),
    ("8  page header",           check_page_header),
    ("9  cover date format",     check_date_format),
]

print("=" * 72)
print("topic-plan Doc QA  -  %s" % doc_id)
print("=" * 72)
for name, fn in CHECKS:
    try:
        status, msg = fn()
    except Exception as e:  # a check crash is itself a failure
        status, msg = "FAIL", "check raised %s: %s" % (type(e).__name__, e)
    line = "[%s] %-26s %s" % (status, name, msg)
    print(line)
    (passes if status == "PASS" else fails).append(name)

print("-" * 72)
print("%d passed, %d failed" % (len(passes), len(fails)))
if fails:
    print("FAILED checks:", ", ".join(c.split()[0] for c in fails))
    sys.exit(1)
print("ALL CHECKS PASSED")
sys.exit(0)
PYEOF
