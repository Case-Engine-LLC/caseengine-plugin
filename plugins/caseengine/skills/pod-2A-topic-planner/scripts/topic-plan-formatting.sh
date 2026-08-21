#!/usr/bin/env bash
# topic-plan-formatting.sh
# Re-upload local markdown to a Doc + .md sibling (preserving fileIds), then
# rebuild the branded Case Engine cover page on the Doc, apply Roboto across
# the body, style every table (CE Blue header row, zebra body rows), and mark
# the `# INTERNAL` H1 with a CE Blue top border.
#
# Applies the branded Case Engine cover page + formatting to the topic-plan Doc.
# (Same patterns, same anti-noise filters, same revise-in-place upload rule.)
# Notes:
#   - SUBTITLE = "Podcast Topic Plan"
#   - HEADER  = "Case Engine | Podcast Topic Plan | {anchor}"
#   - No client-cover-image phase (topic plans have no cover art)
#   - Adds Phase E: table styling (header row + zebra rows)
#   - Adds Phase F: INTERNAL marker (CE Blue, bold, 28pt, 1.5pt top border)
#     — bumped 14pt → 28pt 2026-05-15 so the H1 is unmistakably more
#     prominent than any H2 below it. AMs doing share-prep must spot
#     the truncation boundary at a glance.
#
# Idempotent: safe to re-run. Strips Drive auto-injected H1 title + bookmark
# anchors. Re-runs nuke and rebuild the cover from fresh markdown via files.update.
#
# Usage:
#   topic-plan-formatting.sh \
#     --doc-id <docId> \
#     --md-id <mdId> \
#     --md-path <path> \
#     --firm-name "Law Offices of Todd K. Mohink, PA" \
#     --location-display "Glen Burnie, Maryland (Anne Arundel + Howard County)" \
#     --header-anchor "Maryland" \
#     --date "May 14, 2026" \
#     [--logo-id <driveId>]

set -euo pipefail

LOGO_ID_DEFAULT="1pAZESV-Roq_fh0-1n8xMcMCJvtOiWAN2"

# CE Brand
CE_BLUE_R="0.2078"
CE_BLUE_G="0.4510"
CE_BLUE_B="1.0"
DARK_R="0.0588"
DARK_G="0.0902"
DARK_B="0.1647"
# Zebra body row tint #F5F7FA
ZEBRA_R="0.9608"
ZEBRA_G="0.9686"
ZEBRA_B="0.9804"

DOC_ID=""
MD_ID=""
MD_PATH=""
FIRM_NAME=""
LOCATION_DISPLAY=""
HEADER_ANCHOR=""
DATE_STR=""
LOGO_ID="$LOGO_ID_DEFAULT"

usage() {
  sed -n '2,30p' "$0"
  exit 1
}

while [ $# -gt 0 ]; do
  case "$1" in
    --doc-id) DOC_ID="$2"; shift 2 ;;
    --md-id) MD_ID="$2"; shift 2 ;;
    --md-path) MD_PATH="$2"; shift 2 ;;
    --firm-name) FIRM_NAME="$2"; shift 2 ;;
    --location-display) LOCATION_DISPLAY="$2"; shift 2 ;;
    --header-anchor) HEADER_ANCHOR="$2"; shift 2 ;;
    --date) DATE_STR="$2"; shift 2 ;;
    --logo-id) LOGO_ID="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown arg: $1" >&2; usage ;;
  esac
done

for var in DOC_ID MD_ID MD_PATH FIRM_NAME LOCATION_DISPLAY HEADER_ANCHOR DATE_STR; do
  if [ -z "${!var}" ]; then
    echo "Missing required arg: --$(echo $var | tr '[:upper:]_' '[:lower:]-')" >&2
    usage
  fi
done

if [ ! -f "$MD_PATH" ]; then
  echo "Markdown file not found: $MD_PATH" >&2
  exit 2
fi

LOGO_URI="https://drive.google.com/uc?export=view&id=${LOGO_ID}"

# strip stderr noise from gws (keyring + warnings)
strip_noise() {
  grep -v '^Using keyring' | grep -v '^Warning:' || true
}

BATCH_CHUNK=150
# batch_update <docId> <bodyVarName>
# `bodyVarName` is the NAME of a shell variable holding the request-body JSON
# (pass the bare name, no `$`). The body is written to a temp FILE and python
# reads it from disk - the body never crosses an argv OR an environ boundary,
# both of which are bounded by ARG_MAX (the kernel caps the combined size of
# argv + envp at exec time). A large topic plan's table-style body is ~1.8MB;
# passing it as a positional arg OR as an exported env var fails the exec with
# E2BIG before the call runs. A file path is a few bytes - always safe.
# python then splits the `requests` array into <=BATCH_CHUNK-request batches,
# one gws call per chunk (each chunk's small --json arg is well under ARG_MAX).
# Mirrors the chunking lib_doc_table.py already does.
batch_update() {
  local doc_id="$1" body_var="$2"
  local bu_file
  bu_file=$(mktemp -t topic-plan-batch-XXXXXX.json)
  printf '%s' "${!body_var}" > "$bu_file"
  BU_FILE="$bu_file" BU_DOC="$doc_id" BU_CHUNK="$BATCH_CHUNK" python3 <<'PYEOF'
import json, os, subprocess, sys
doc_id = os.environ["BU_DOC"]
chunk = int(os.environ["BU_CHUNK"])
with open(os.environ["BU_FILE"]) as f:
    body = json.load(f)
reqs = body.get("requests", [])
if not reqs:
    sys.exit(0)
for i in range(0, len(reqs), chunk):
    part = json.dumps({"requests": reqs[i:i + chunk]})
    p = subprocess.run(
        ["gws", "docs", "documents", "batchUpdate",
         "--params", json.dumps({"documentId": doc_id}),
         "--json", part],
        capture_output=True, text=True)
    if p.returncode != 0:
        sys.stderr.write(p.stderr or p.stdout)
        sys.exit(p.returncode)
PYEOF
  local rc=$?
  rm -f "$bu_file"
  return $rc
}

# Pre-process markdown: strip any `![...](drive-url)` image embeds before
# upload. Topic plan markdowns generally have none, but keep the guard.
TMP_MD=$(mktemp -t topic-plan-md-XXXXXX.md)
trap 'rm -f "$TMP_MD"' EXIT
sed -E '/^!\[.*\]\(https:\/\/drive\.google\.com\/.*\)/d' "$MD_PATH" > "$TMP_MD"

echo ">> [1/9] Re-uploading markdown to .md sibling (fileId=$MD_ID)"
gws drive files update \
  --params "{\"fileId\":\"$MD_ID\",\"supportsAllDrives\":true,\"fields\":\"id,name\"}" \
  --upload "$TMP_MD" \
  --upload-content-type "text/markdown" 2>&1 | strip_noise > /dev/null

echo ">> [2/9] Re-uploading markdown to Doc as Google Doc (fileId=$DOC_ID, auto-convert)"
gws drive files update \
  --params "{\"fileId\":\"$DOC_ID\",\"supportsAllDrives\":true,\"fields\":\"id,name\"}" \
  --upload "$TMP_MD" \
  --upload-content-type "text/markdown" 2>&1 | strip_noise > /dev/null

# Brief pause to ensure Drive's conversion settles before Docs API reads/writes
sleep 2

echo ">> [3/9] Building cover page on Doc"

# Cover composition: standard CE cover shape.
read -r SUB_S SUB_E TITLE_S TITLE_E LOC_S LOC_E PREP_S PREP_E DATE_S DATE_E TOTAL_END < <(python3 -c "
firm = '''$FIRM_NAME'''
loc = '''$LOCATION_DISPLAY'''
date = '''$DATE_STR'''
lines = [
    ('spacer1', '\n'),
    ('spacer2', '\n'),  # spacer2 holds the CE logo (inserted at index 2)
    ('spacer3', '\n'),
    ('subtitle', 'Podcast Topic Plan\n'),
    ('title', firm + '\n'),
    ('spacer_mid', '\n'),
    ('location', loc + '\n'),
    ('spacer5', '\n'),
    ('prepared', 'Prepared by Case Engine\n'),
    ('date', date + '\n'),
]
cur = 1
spans = {}
for name, content in lines:
    s = cur
    e = cur + len(content)
    spans[name] = (s, e)
    cur = e
def text_only(span_name):
    s, e = spans[span_name]
    return s, e - 1
print(*text_only('subtitle'), *text_only('title'),
      *text_only('location'),
      *text_only('prepared'), *text_only('date'), cur)
")

COVER_TEXT=$'\n\n\nPodcast Topic Plan\n'"$FIRM_NAME"$'\n\n'"$LOCATION_DISPLAY"$'\n\nPrepared by Case Engine\n'"$DATE_STR"$'\n'

# Phase A: insert cover text + page break
PHASE_A=$(python3 <<PYEOF
import json
text = """$COVER_TEXT"""
total_end = $TOTAL_END
body = {
  "requests": [
    {"insertText": {"location": {"index": 1}, "text": text}},
    {"insertPageBreak": {"location": {"index": total_end}}}
  ]
}
print(json.dumps(body))
PYEOF
)

batch_update "$DOC_ID" PHASE_A 2>&1 | strip_noise > /dev/null

# Phase B: style the cover + insert image
PHASE_B=$(python3 <<PYEOF
import json
sub_s, sub_e = $SUB_S, $SUB_E
title_s, title_e = $TITLE_S, $TITLE_E
loc_s, loc_e = $LOC_S, $LOC_E
prep_s, prep_e = $PREP_S, $PREP_E
date_s, date_e = $DATE_S, $DATE_E
total_end = $TOTAL_END

dark = {"red": $DARK_R, "green": $DARK_G, "blue": $DARK_B}
blue = {"red": $CE_BLUE_R, "green": $CE_BLUE_G, "blue": $CE_BLUE_B}

def color(rgb):
    return {"color": {"rgbColor": rgb}}

requests = []

requests.append({
  "updateParagraphStyle": {
    "range": {"startIndex": 1, "endIndex": total_end},
    "paragraphStyle": {"alignment": "CENTER"},
    "fields": "alignment"
  }
})

requests.append({
  "updateTextStyle": {
    "range": {"startIndex": 1, "endIndex": total_end},
    "textStyle": {
      "weightedFontFamily": {"fontFamily": "Roboto", "weight": 400},
      "foregroundColor": color(dark)
    },
    "fields": "weightedFontFamily,foregroundColor"
  }
})

# Subtitle (Podcast Topic Plan) — CE Blue 24pt bold
requests.append({
  "updateTextStyle": {
    "range": {"startIndex": sub_s, "endIndex": sub_e},
    "textStyle": {
      "bold": True,
      "fontSize": {"magnitude": 24, "unit": "PT"},
      "weightedFontFamily": {"fontFamily": "Roboto", "weight": 700},
      "foregroundColor": color(blue)
    },
    "fields": "bold,fontSize,weightedFontFamily,foregroundColor"
  }
})

# Firm name — dark 18pt bold
requests.append({
  "updateTextStyle": {
    "range": {"startIndex": title_s, "endIndex": title_e},
    "textStyle": {
      "bold": True,
      "fontSize": {"magnitude": 18, "unit": "PT"},
      "weightedFontFamily": {"fontFamily": "Roboto", "weight": 700},
      "foregroundColor": color(dark)
    },
    "fields": "bold,fontSize,weightedFontFamily,foregroundColor"
  }
})

# Location — 14pt normal
requests.append({
  "updateTextStyle": {
    "range": {"startIndex": loc_s, "endIndex": loc_e},
    "textStyle": {
      "bold": False,
      "fontSize": {"magnitude": 14, "unit": "PT"},
      "weightedFontFamily": {"fontFamily": "Roboto", "weight": 400},
      "foregroundColor": color(dark)
    },
    "fields": "bold,fontSize,weightedFontFamily,foregroundColor"
  }
})

# Prepared by Case Engine — 11pt normal
requests.append({
  "updateTextStyle": {
    "range": {"startIndex": prep_s, "endIndex": prep_e},
    "textStyle": {
      "bold": False,
      "fontSize": {"magnitude": 11, "unit": "PT"},
      "weightedFontFamily": {"fontFamily": "Roboto", "weight": 400},
      "foregroundColor": color(dark)
    },
    "fields": "bold,fontSize,weightedFontFamily,foregroundColor"
  }
})

# Date — 11pt normal
requests.append({
  "updateTextStyle": {
    "range": {"startIndex": date_s, "endIndex": date_e},
    "textStyle": {
      "bold": False,
      "fontSize": {"magnitude": 11, "unit": "PT"},
      "weightedFontFamily": {"fontFamily": "Roboto", "weight": 400},
      "foregroundColor": color(dark)
    },
    "fields": "bold,fontSize,weightedFontFamily,foregroundColor"
  }
})

requests.append({
  "insertInlineImage": {
    "location": {"index": 2},
    "uri": "$LOGO_URI",
    "objectSize": {
      "width": {"magnitude": 216, "unit": "PT"},
      "height": {"magnitude": 55.5, "unit": "PT"}
    }
  }
})

print(json.dumps({"requests": requests}))
PYEOF
)

batch_update "$DOC_ID" PHASE_B 2>&1 | strip_noise > /dev/null

# Phase C: Strip Drive's auto-injected H1 title (markdown→Doc adds one from
# the filename). Then apply Roboto across the remaining body.
echo ">> [4/9] Stripping auto-injected title + applying Roboto across body"

DOC_JSON_FILE=$(mktemp)
trap 'rm -f "$TMP_MD" "$DOC_JSON_FILE"' EXIT
gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 | strip_noise > "$DOC_JSON_FILE"

read -r AUTO_H1_S AUTO_H1_E < <(python3 -c "
import json
total_end = $TOTAL_END
with open('$DOC_JSON_FILE') as f:
    d = json.load(f)
content = d['body']['content']
auto_s = auto_e = 0
for e in content:
    si = e.get('startIndex', 0)
    if si <= total_end:
        continue
    if 'paragraph' not in e:
        continue
    p = e['paragraph']
    style = p.get('paragraphStyle', {}).get('namedStyleType', '')
    text = ''
    for el in p.get('elements', []):
        if 'textRun' in el:
            text += el['textRun'].get('content', '')
    if not text.strip():
        continue
    if style == 'HEADING_1':
        auto_s, auto_e = e['startIndex'], e['endIndex']
    break
print(auto_s, auto_e)
")

if [ "$AUTO_H1_S" -gt 0 ]; then
  echo "   stripping auto-H1 at [$AUTO_H1_S, $AUTO_H1_E)"
  STRIP_REQ=$(python3 -c "
import json
print(json.dumps({'requests':[{'deleteContentRange':{'range':{'startIndex': $AUTO_H1_S, 'endIndex': $AUTO_H1_E}}}]}))
")
  batch_update "$DOC_ID" STRIP_REQ 2>&1 | strip_noise > /dev/null
  gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 | strip_noise > "$DOC_JSON_FILE"
fi

BODY_END=$(python3 -c "
import json
with open('$DOC_JSON_FILE') as f:
    d = json.load(f)
content = d['body']['content']
print(content[-1].get('endIndex', 1))
")

PHASE_C=$(python3 <<PYEOF
import json
body_end = $BODY_END
total_end = $TOTAL_END
start = total_end + 1
end = max(body_end - 1, start + 1)
requests = [{
  "updateTextStyle": {
    "range": {"startIndex": start, "endIndex": end},
    "textStyle": {"weightedFontFamily": {"fontFamily": "Roboto", "weight": 400}},
    "fields": "weightedFontFamily"
  }
}]
print(json.dumps({"requests": requests}))
PYEOF
)

batch_update "$DOC_ID" PHASE_C 2>&1 | strip_noise > /dev/null

# Phase C.5: Show Identity labels render bold (format-feedback item, 2026-05-20).
# The five `## Show Identity` fields are authored in markdown as bold inline
# labels — `**Podcast Name:**`, `**Tagline:**`, `**Podcast Description:**`,
# `**Audience:**`, `**Topic Mix:**` — each followed by normal-weight content.
#
# Root cause this pass fixes: Google Drive's markdown→Doc auto-conversion
# SPLITS the paragraph at the colon (so `Podcast Name:` becomes its own text
# run) but intermittently DROPS the `bold:true` on that leading run when the
# bold span is the first segment of a paragraph immediately followed by
# non-bold text. The Phase C Roboto pass only sets weightedFontFamily (its
# `fields` does not include `bold`), so nothing re-asserts bold and the labels
# silently render normal-weight. This pass re-applies bold to exactly the
# label token + colon for all five fields, after the markdown import has
# settled, so a render reliably produces bold inline labels.
#
# Also self-heals the recurring `### Audience` regression: if `Audience` was
# authored (or reverted) as an H3 heading, Drive renders it as a HEADING_3
# paragraph with text "Audience" (no colon). This pass detects that, demotes
# the paragraph to NORMAL_TEXT, appends the missing colon, and bolds the
# label so Audience matches the other four fields.
echo ">> [5.5/8] Bolding Show Identity labels (re-assert bold dropped by md import)"

gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 | strip_noise > "$DOC_JSON_FILE"

# Exported so the quoted ('PYEOF') Python heredoc below can read the path via
# os.environ without shell interpolation (the Python body uses { } and quotes
# that would clash with an unquoted heredoc).
export DOC_JSON_FILE

SI_REQ=$(python3 <<'PYEOF'
import json, os
with open(os.environ['DOC_JSON_FILE']) as f:
    d = json.load(f)

# Canonical Show Identity labels, in locked order. Each must render as a bold
# inline label (label token + trailing colon bold; value after stays normal).
LABELS = ['Podcast Name:', 'Tagline:', 'Podcast Description:', 'Audience:', 'Topic Mix:']
# Bare forms (no colon) — what an H3-reverted `### Audience` produces.
LABEL_BARE = {l[:-1]: l for l in LABELS}   # {'Podcast Name': 'Podcast Name:', ...}

content = d['body']['content']

# Locate the `## Show Identity` H2 and the next H2 (section boundary).
si_start_idx = None
si_end_idx = None
for i, elem in enumerate(content):
    if 'paragraph' not in elem:
        continue
    p = elem['paragraph']
    style = p.get('paragraphStyle', {}).get('namedStyleType', '')
    text = ''.join(
        el['textRun'].get('content', '')
        for el in p.get('elements', []) if 'textRun' in el
    ).strip()
    if style == 'HEADING_2' and text.lower() == 'show identity':
        si_start_idx = i
        continue
    if si_start_idx is not None and i > si_start_idx and style in ('HEADING_1', 'HEADING_2'):
        si_end_idx = i
        break
if si_end_idx is None:
    si_end_idx = len(content)

requests = []
found = {l: False for l in LABELS}

if si_start_idx is not None:
    for elem in content[si_start_idx + 1:si_end_idx]:
        if 'paragraph' not in elem:
            continue
        p = elem['paragraph']
        style = p.get('paragraphStyle', {}).get('namedStyleType', '')
        runs = [el for el in p.get('elements', []) if 'textRun' in el]
        if not runs:
            continue
        para_text = ''.join(r['textRun'].get('content', '') for r in runs)
        stripped = para_text.strip()
        para_start = elem['startIndex']

        # Case 1: paragraph already carries one of the colon-form labels as its
        # leading text — bold exactly the label token + colon.
        matched_label = None
        for lbl in LABELS:
            if stripped.startswith(lbl):
                matched_label = lbl
                break

        # Case 2: an H3-reverted bare label (e.g. heading "Audience", no colon).
        bare_heading = None
        if matched_label is None and style.startswith('HEADING'):
            if stripped in LABEL_BARE:
                bare_heading = stripped

        if matched_label:
            # The label sits at the very start of the paragraph. Compute the
            # absolute range covering label token + colon, regardless of how
            # Drive split the runs (it usually splits exactly at the colon).
            # leading-whitespace offset inside the paragraph:
            lead = len(para_text) - len(para_text.lstrip())
            lbl_abs_start = para_start + lead
            lbl_abs_end = lbl_abs_start + len(matched_label)
            requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": lbl_abs_start, "endIndex": lbl_abs_end},
                    "textStyle": {"bold": True},
                    "fields": "bold"
                }
            })
            found[matched_label] = True

        elif bare_heading:
            # H3 regression: demote the heading paragraph to NORMAL_TEXT, append
            # the missing colon, and bold the label so it matches the other 4.
            full_label = LABEL_BARE[bare_heading]   # e.g. 'Audience:'
            lead = len(para_text) - len(para_text.lstrip())
            heading_abs_start = para_start + lead
            heading_abs_end = heading_abs_start + len(bare_heading)
            # 1) insert the colon immediately after the bare label
            requests.append({
                "insertText": {
                    "location": {"index": heading_abs_end},
                    "text": ":"
                }
            })
            # 2) demote paragraph H3 -> NORMAL_TEXT (range covers whole paragraph)
            requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": para_start, "endIndex": elem['endIndex']},
                    "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
                    "fields": "namedStyleType"
                }
            })
            # 3) bold the label token + the inserted colon
            requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": heading_abs_start,
                              "endIndex": heading_abs_end + 1},
                    "textStyle": {"bold": True},
                    "fields": "bold"
                }
            })
            found[full_label] = True

# Note on ordering: an insertText shifts every index after it. To stay correct
# the requests are applied bottom-up. We sort all requests by their primary
# index descending so later (higher-index) edits land before earlier ones.
def req_index(r):
    if 'insertText' in r:
        return r['insertText']['location']['index']
    if 'updateTextStyle' in r:
        return r['updateTextStyle']['range']['startIndex']
    if 'updateParagraphStyle' in r:
        return r['updateParagraphStyle']['range']['startIndex']
    return 0
requests.sort(key=req_index, reverse=True)

missing = [l for l, ok in found.items() if not ok]
print(json.dumps({
    "found": [l for l, ok in found.items() if ok],
    "missing": missing,
    "body": {"requests": requests}
}))
PYEOF
)

SI_FOUND=$(echo "$SI_REQ" | python3 -c "import json,sys; print(','.join(json.load(sys.stdin)['found']) or 'none')")
SI_MISSING=$(echo "$SI_REQ" | python3 -c "import json,sys; print(','.join(json.load(sys.stdin)['missing']) or 'none')")
echo "   bolded labels: $SI_FOUND"
[ "$SI_MISSING" != "none" ] && echo "   WARNING: Show Identity labels not found in Doc: $SI_MISSING"

SI_REQ_COUNT=$(echo "$SI_REQ" | python3 -c "import json,sys; print(len(json.load(sys.stdin)['body']['requests']))")
if [ "$SI_REQ_COUNT" -gt 0 ]; then
  SI_BODY=$(echo "$SI_REQ" | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin)['body']))")
  batch_update "$DOC_ID" SI_BODY 2>&1 | strip_noise > /dev/null
  echo "   applied $SI_REQ_COUNT Show Identity label request(s)"
fi

# Phase D: Strip Drive auto-injected bookmark anchors
echo ">> [5/9] Stripping Drive auto-injected bookmark anchors"

gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 | strip_noise > "$DOC_JSON_FILE"

STRIP_BOOKMARKS_REQ=$(python3 <<PYEOF
import json
with open('$DOC_JSON_FILE') as f:
    d = json.load(f)

ranges = []
def walk(content):
    for elem in content:
        if 'paragraph' in elem:
            for el in elem['paragraph'].get('elements', []):
                if 'bookmark' in el:
                    ranges.append((el['startIndex'], el['endIndex']))
        if 'table' in elem:
            for row in elem['table'].get('tableRows', []):
                for cell in row.get('tableCells', []):
                    walk(cell.get('content', []))
walk(d['body']['content'])

ranges.sort(key=lambda r: r[0], reverse=True)
requests = [
    {'deleteContentRange': {'range': {'startIndex': s, 'endIndex': e}}}
    for s, e in ranges
]
print(json.dumps({'count': len(ranges), 'body': {'requests': requests}}))
PYEOF
)

BM_COUNT=$(echo "$STRIP_BOOKMARKS_REQ" | python3 -c "import json,sys; print(json.load(sys.stdin)['count'])")
echo "   found $BM_COUNT bookmark anchor(s)"

if [ "$BM_COUNT" -gt 0 ]; then
  BM_BODY=$(echo "$STRIP_BOOKMARKS_REQ" | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin)['body']))")
  batch_update "$DOC_ID" BM_BODY 2>&1 | strip_noise > /dev/null
  echo "   stripped $BM_COUNT bookmark(s)"
fi

# Phase E: Table styling — CE Blue header row, zebra body rows, small padding
echo ">> [6/9] Styling tables (header CE Blue + zebra body rows + padding)"

gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 | strip_noise > "$DOC_JSON_FILE"

TABLE_STYLE_REQ=$(python3 <<PYEOF
import json
with open('$DOC_JSON_FILE') as f:
    d = json.load(f)

CE_BLUE = {"red": $CE_BLUE_R, "green": $CE_BLUE_G, "blue": $CE_BLUE_B}
WHITE   = {"red": 1.0, "green": 1.0, "blue": 1.0}
DARK    = {"red": $DARK_R, "green": $DARK_G, "blue": $DARK_B}
ZEBRA   = {"red": $ZEBRA_R, "green": $ZEBRA_G, "blue": $ZEBRA_B}

requests = []
tables_found = 0

def collect_tables(content, out):
    for elem in content:
        if 'table' in elem:
            out.append(elem)
            for row in elem['table'].get('tableRows', []):
                for cell in row.get('tableCells', []):
                    collect_tables(cell.get('content', []), out)
        elif 'paragraph' in elem:
            pass

tables = []
collect_tables(d['body']['content'], tables)
tables_found = len(tables)

for tbl_elem in tables:
    table = tbl_elem['table']
    table_start = tbl_elem['startIndex']
    rows = table.get('tableRows', [])
    if not rows:
        continue

    # Spec: header row = CE Blue + white text + bold.
    # Body rows: row_idx 1 = first body row = zebra; row_idx 2 = white;
    # so body even/odd is computed relative to body position (row_idx - 1).
    for row_idx, row in enumerate(rows):
        is_header = (row_idx == 0)
        if is_header:
            bg = CE_BLUE
            fg = WHITE
            bold = True
            weight = 700
        else:
            body_pos = row_idx - 1
            bg = WHITE if (body_pos % 2 == 0) else ZEBRA
            fg = DARK
            bold = False
            weight = 400

        for col_idx, cell in enumerate(row.get('tableCells', [])):
            cell_loc = {
                "tableStartLocation": {"index": table_start},
                "rowIndex": row_idx,
                "columnIndex": col_idx
            }
            # Background + padding
            requests.append({
                "updateTableCellStyle": {
                    "tableCellStyle": {
                        "backgroundColor": {"color": {"rgbColor": bg}},
                        "paddingTop":    {"magnitude": 2, "unit": "PT"},
                        "paddingBottom": {"magnitude": 2, "unit": "PT"},
                        "paddingLeft":   {"magnitude": 6, "unit": "PT"},
                        "paddingRight":  {"magnitude": 6, "unit": "PT"}
                    },
                    "fields": "backgroundColor,paddingTop,paddingBottom,paddingLeft,paddingRight",
                    "tableRange": {
                        "tableCellLocation": cell_loc,
                        "rowSpan": 1,
                        "columnSpan": 1
                    }
                }
            })
            # Text style: Roboto 10pt, color + bold per row type, across the cell content
            cell_start = cell.get('startIndex')
            cell_end   = cell.get('endIndex')
            if cell_start is None or cell_end is None or cell_end <= cell_start + 1:
                continue
            requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": cell_start, "endIndex": cell_end - 1},
                    "textStyle": {
                        "bold": bold,
                        "fontSize": {"magnitude": 9, "unit": "PT"},
                        "weightedFontFamily": {"fontFamily": "Roboto", "weight": weight},
                        "foregroundColor": {"color": {"rgbColor": fg}}
                    },
                    "fields": "bold,fontSize,weightedFontFamily,foregroundColor"
                }
            })

print(json.dumps({"count": tables_found, "body": {"requests": requests}}))
PYEOF
)

TBL_COUNT=$(echo "$TABLE_STYLE_REQ" | python3 -c "import json,sys; print(json.load(sys.stdin)['count'])")
echo "   found $TBL_COUNT table(s)"

if [ "$TBL_COUNT" -gt 0 ]; then
  TBL_BODY=$(echo "$TABLE_STYLE_REQ" | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin)['body']))")
  batch_update "$DOC_ID" TBL_BODY 2>&1 | strip_noise > /dev/null
  echo "   styled $TBL_COUNT table(s)"
fi

# Phase E.5: Column widths — detect main / bonus tables by their FULL ordered
# header signature and apply the canonical compact widths so the # column hugs
# digits, Topic takes the slack, and Keywords doesn't waste space.
# Profile (US Letter, 1" margins, 468pt usable width):
#   Main 5-col (#, Topic, Theme, Keywords, Rationale):
#     32 / 134 / 70 / 116 / 116 = 468pt    (# wide enough to fit "12" on a single line)
#   Bonus 4-col (Topic, Theme, Keywords, Rationale):
#     150 / 80 / 128 / 110 = 468pt
#
# v4 format change (2026-05-20): the standalone `Search Volume` column was
# DROPPED from both episode tables. Its summed value now renders inside the
# `Keywords` cell as a bold first line (`**Total Search Demand:** {sum}`)
# followed by a <br> and the comma-separated keyword list.
#
# v4.4.0 format change (2026-05-28): the `Swaps for` column was DROPPED from the
# Additional Topics table - it went 5 cols -> 4 cols and the freed 48pt was
# redistributed across the four survivors (150 / 80 / 128 / 110 = 468pt). Swap
# relationships now live only in the INTERNAL `## Topic Ideas` Notes column.
#
# Detection (v4): match the WHOLE ordered header row, not just the first cell.
# The old logic keyed bonus off "first header cell starts with 'topic'", which
# also matches the v4 INTERNAL `## Research Sources` table (6 cols, header
# Topic | Scope | Entity Research | Keyword Research | Virality Research |
# N-Gram Tables) — so Research Sources was silently given BONUS_WIDTHS. The five
# topic-plan table types and their exact header signatures:
#   Main 12-Episode Plan : # | Topic | Theme | Keywords | Rationale                            -> MAIN_WIDTHS
#   Additional Topics    : Topic | Theme | Keywords | Rationale                                 -> BONUS_WIDTHS
#   Research Sources     : Name | URL | Notes                                                 -> natural width
#   Topic Ideas      : Rank | Topic | Theme | Score | Rationale | Notes                    -> SCORE_WIDTHS
#   Episode Breakdown    : Question | Search Phrases | Rationale  (episodes 2-12 + additional) -> natural width
#   Episode Breakdown E1 : Question | Rationale                  (founder interview, E1 only) -> natural width
# Main, Additional Topics, and Topic Ideas get fixed widths. Topic Ideas
# pins its `Rank` column to a fixed narrow 32pt (sized to the word "Rank") so the
# rank digits hug a tight column instead of taking a proportional slice. The
# `## Topics by Theme` table was removed from the skill entirely (v5, 2026-05-20)
# — the formatter has no handling for it. The two question tables are explicitly
# recognized and left at natural width — recognized so they can never be
# misclassified, not styled because their content wraps fine on its own.
echo ">> [6.5/8] Setting compact column widths on main + bonus + score tables"

gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 | strip_noise > "$DOC_JSON_FILE"

WIDTH_REQ=$(python3 <<PYEOF
import json
with open('$DOC_JSON_FILE') as f:
    d = json.load(f)

MAIN_WIDTHS  = [32, 134, 70, 116, 116]   # #, Topic, Theme, Keywords, Rationale
BONUS_WIDTHS = [150, 80, 128, 110]       # Topic, Theme, Keywords, Rationale (v4.4.0: Swaps for dropped)
# Topic Ideas (6-col): Rank pinned to a fixed narrow 32pt (sized to the word
# "Rank"); the remaining 5 columns split the rest of the 468pt content width.
SCORE_WIDTHS = [32, 176, 74, 46, 90, 50]  # Rank, Topic, Theme, Score, Rationale, Notes

# Full ordered header signatures (lower-cased, stripped) for every topic-plan
# table type. Detection matches the WHOLE row so no table is misclassified.
SIG_MAIN    = ['#', 'topic', 'theme', 'keywords', 'rationale']
SIG_BONUS   = ['topic', 'theme', 'keywords', 'rationale']
SIG_SOURCES = ['name', 'url', 'notes']
SIG_SCORE   = ['rank', 'topic', 'theme', 'score', 'rationale', 'notes']
SIG_QUEST   = ['question', 'search phrases', 'rationale']
SIG_QUEST_E1 = ['question', 'rationale']

def collect_tables(content, out):
    for elem in content:
        if 'table' in elem:
            out.append(elem)
            for row in elem['table'].get('tableRows', []):
                for cell in row.get('tableCells', []):
                    collect_tables(cell.get('content', []), out)

def cell_text(cell):
    text = ''
    for el in cell.get('content', []):
        if 'paragraph' in el:
            for run in el['paragraph'].get('elements', []):
                if 'textRun' in run:
                    text += run['textRun'].get('content', '')
    return text.strip()

def header_signature(tbl_elem):
    """Full ordered list of lower-cased header-cell texts for row 0."""
    rows = tbl_elem['table'].get('tableRows', [])
    if not rows:
        return []
    return [cell_text(c).lower() for c in rows[0].get('tableCells', [])]

tables = []
collect_tables(d['body']['content'], tables)

requests = []
applied = {"main": 0, "bonus": 0, "score": 0, "natural": 0, "skipped": 0}

for tbl_elem in tables:
    table = tbl_elem['table']
    table_start = tbl_elem['startIndex']
    sig = header_signature(tbl_elem)
    if sig == SIG_MAIN:
        widths = MAIN_WIDTHS
        applied["main"] += 1
    elif sig == SIG_BONUS:
        widths = BONUS_WIDTHS
        applied["bonus"] += 1
    elif sig == SIG_SCORE:
        # Topic Ideas — Rank column pinned to a fixed narrow 32pt.
        widths = SCORE_WIDTHS
        applied["score"] += 1
    elif sig in (SIG_SOURCES, SIG_QUEST, SIG_QUEST_E1):
        # Recognized topic-plan table — left at natural width by design.
        applied["natural"] += 1
        continue
    else:
        # Unrecognized table (e.g., an ad-hoc INTERNAL table) — leave alone.
        applied["skipped"] += 1
        continue
    for col_idx, w in enumerate(widths):
        requests.append({
            "updateTableColumnProperties": {
                "tableStartLocation": {"index": table_start},
                "columnIndices": [col_idx],
                "tableColumnProperties": {
                    "widthType": "FIXED_WIDTH",
                    "width": {"magnitude": w, "unit": "PT"}
                },
                "fields": "widthType,width"
            }
        })

print(json.dumps({"summary": applied, "body": {"requests": requests}}))
PYEOF
)

WIDTH_SUMMARY=$(echo "$WIDTH_REQ" | python3 -c "import json,sys; s=json.load(sys.stdin)['summary']; print(f\"main={s['main']} bonus={s['bonus']} score={s['score']} natural={s['natural']} skipped={s['skipped']}\")")
echo "   $WIDTH_SUMMARY"

WIDTH_REQ_COUNT=$(echo "$WIDTH_REQ" | python3 -c "import json,sys; print(len(json.load(sys.stdin)['body']['requests']))")
if [ "$WIDTH_REQ_COUNT" -gt 0 ]; then
  WIDTH_BODY=$(echo "$WIDTH_REQ" | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin)['body']))")
  batch_update "$DOC_ID" WIDTH_BODY 2>&1 | strip_noise > /dev/null
  echo "   applied $WIDTH_REQ_COUNT column-width request(s)"
fi

# Phase F: INTERNAL marker — find the `INTERNAL` HEADING_1 paragraph (Drive
# converts `# INTERNAL` to namedStyleType=HEADING_1, text "INTERNAL"). Style
# it CE Blue + bold + 28pt + 1.5pt CE Blue top border + 6pt top padding.
# Intentionally MORE prominent than any H2 below it — this is the
# truncation boundary AMs scan for when prepping a client share.
echo ">> [7/9] Styling INTERNAL marker (28pt + 1.5pt top border)"

gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 | strip_noise > "$DOC_JSON_FILE"

read -r INT_S INT_E < <(python3 -c "
import json
with open('$DOC_JSON_FILE') as f:
    d = json.load(f)
found_s = found_e = 0
for elem in d['body']['content']:
    if 'paragraph' not in elem:
        continue
    p = elem['paragraph']
    style = p.get('paragraphStyle', {}).get('namedStyleType', '')
    if style != 'HEADING_1':
        continue
    text = ''
    for el in p.get('elements', []):
        if 'textRun' in el:
            text += el['textRun'].get('content', '')
    if text.strip().upper() == 'INTERNAL':
        found_s = elem['startIndex']
        found_e = elem['endIndex']
        break
print(found_s, found_e)
")

if [ "$INT_S" -gt 0 ]; then
  echo "   styling INTERNAL marker at [$INT_S, $INT_E) — 28pt CE Blue bold + 1.5pt top border"
  INT_REQ=$(python3 <<PYEOF
import json
s, e = $INT_S, $INT_E
blue = {"red": $CE_BLUE_R, "green": $CE_BLUE_G, "blue": $CE_BLUE_B}
requests = [
  {"updateTextStyle": {
     "range": {"startIndex": s, "endIndex": e - 1},
     "textStyle": {
       "bold": True,
       "fontSize": {"magnitude": 28, "unit": "PT"},
       "weightedFontFamily": {"fontFamily": "Roboto", "weight": 700},
       "foregroundColor": {"color": {"rgbColor": blue}}
     },
     "fields": "bold,fontSize,weightedFontFamily,foregroundColor"
  }},
  {"updateParagraphStyle": {
     "range": {"startIndex": s, "endIndex": e - 1},
     "paragraphStyle": {
       "borderTop": {
         "color": {"color": {"rgbColor": blue}},
         "width": {"magnitude": 1.5, "unit": "PT"},
         "padding": {"magnitude": 6, "unit": "PT"},
         "dashStyle": "SOLID"
       },
       "spaceAbove": {"magnitude": 6, "unit": "PT"}
     },
     "fields": "borderTop,spaceAbove"
  }}
]
print(json.dumps({"requests": requests}))
PYEOF
)
  batch_update "$DOC_ID" INT_REQ 2>&1 | strip_noise > /dev/null
else
  echo "   no INTERNAL H1 found — skipping"
fi

echo ">> [8/9] Setting running header and footer"

gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 | strip_noise > "$DOC_JSON_FILE"

HEADER_ID=$(python3 -c "
import json
with open('$DOC_JSON_FILE') as f:
    d = json.load(f)
headers = d.get('headers', {})
print(next(iter(headers.keys()), ''))
")
FOOTER_ID=$(python3 -c "
import json
with open('$DOC_JSON_FILE') as f:
    d = json.load(f)
footers = d.get('footers', {})
print(next(iter(footers.keys()), ''))
")

if [ -z "$HEADER_ID" ] || [ -z "$FOOTER_ID" ]; then
  CREATE_HF='{"requests":[{"createHeader":{"type":"DEFAULT"}},{"createFooter":{"type":"DEFAULT"}}]}'
  HF_RESP=$(gws docs documents batchUpdate \
    --params "{\"documentId\":\"$DOC_ID\"}" \
    --json "$CREATE_HF" 2>&1 | strip_noise)
  HEADER_ID=$(echo "$HF_RESP" | python3 -c "
import json, sys
d = json.load(sys.stdin)
for r in d.get('replies', []):
    if 'createHeader' in r:
        print(r['createHeader']['headerId']); break
")
  FOOTER_ID=$(echo "$HF_RESP" | python3 -c "
import json, sys
d = json.load(sys.stdin)
for r in d.get('replies', []):
    if 'createFooter' in r:
        print(r['createFooter']['footerId']); break
")
fi

HEADER_TEXT="Case Engine | Podcast Topic Plan | $HEADER_ANCHOR"
FOOTER_TEXT="Case Engine | Confidential    Page "

PHASE_HF=$(python3 <<PYEOF
import json
header_id = "$HEADER_ID"
footer_id = "$FOOTER_ID"
header_text = """$HEADER_TEXT"""
footer_text = """$FOOTER_TEXT"""
header_len = len(header_text)
footer_len = len(footer_text)
dark = {"red": $DARK_R, "green": $DARK_G, "blue": $DARK_B}

requests = [
  {"insertText": {"location": {"index": 0, "segmentId": header_id}, "text": header_text}},
  {"updateTextStyle": {
     "range": {"startIndex": 0, "endIndex": header_len, "segmentId": header_id},
     "textStyle": {
       "italic": True,
       "fontSize": {"magnitude": 9, "unit": "PT"},
       "weightedFontFamily": {"fontFamily": "Roboto", "weight": 400},
       "foregroundColor": {"color": {"rgbColor": dark}}
     },
     "fields": "italic,fontSize,weightedFontFamily,foregroundColor"
  }},
  {"updateParagraphStyle": {
     "range": {"startIndex": 0, "endIndex": header_len, "segmentId": header_id},
     "paragraphStyle": {"alignment": "END"},
     "fields": "alignment"
  }},
  {"insertText": {"location": {"index": 0, "segmentId": footer_id}, "text": footer_text}},
  {"updateTextStyle": {
     "range": {"startIndex": 0, "endIndex": footer_len, "segmentId": footer_id},
     "textStyle": {
       "fontSize": {"magnitude": 9, "unit": "PT"},
       "weightedFontFamily": {"fontFamily": "Roboto", "weight": 400},
       "foregroundColor": {"color": {"rgbColor": dark}}
     },
     "fields": "fontSize,weightedFontFamily,foregroundColor"
  }},
  {"updateParagraphStyle": {
     "range": {"startIndex": 0, "endIndex": footer_len, "segmentId": footer_id},
     "paragraphStyle": {"alignment": "START"},
     "fields": "alignment"
  }}
]
print(json.dumps({"requests": requests}))
PYEOF
)

batch_update "$DOC_ID" PHASE_HF 2>&1 | strip_noise > /dev/null

# Phase G: Research Sources URL column — convert markdown links to real Docs
# hyperlinks. The INTERNAL `## Research Sources` table authors each URL cell as
# a markdown link `[label](url)`. Drive's markdown→Doc auto-conversion (Phase
# [2/9]) usually turns body-text markdown links into real hyperlinks, but its
# handling of links INSIDE table cells is unreliable — it can leave the literal
# `[label](url)` text as plain, non-clickable text. This phase self-heals: it
# scans the Research Sources table's URL column (column index 1), and for any
# cell whose text is a literal `[label](url)` markdown link, it replaces the
# cell text with just `label` and applies a real Docs hyperlink over it. Cells
# that Drive already converted to a real hyperlink (run carries textStyle.link)
# are left untouched. Only the URL column of the Research Sources table is
# touched — Name and Notes columns and every other table are never modified.
echo ">> [9/9] Converting Research Sources URL column to clickable hyperlinks"

gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 | strip_noise > "$DOC_JSON_FILE"

# Quoted heredoc ('PYEOF') so the regex/comment `[label](url)` is never glob-
# or command-substitution-expanded by the shell. The doc-JSON path is read
# from the exported env var (set above for Phase C.5) instead of being shell-
# interpolated into the body.
export DOC_JSON_FILE
RS_LINK_REQ=$(python3 <<'PYEOF'
import json, os, re
with open(os.environ['DOC_JSON_FILE']) as f:
    d = json.load(f)

content = d['body']['content']

def para_text(elem):
    return ''.join(
        el['textRun'].get('content', '')
        for el in elem.get('paragraph', {}).get('elements', [])
        if 'textRun' in el
    )

# Locate the `Research Sources` heading, then the first table after it.
rs_idx = None
for i, e in enumerate(content):
    if 'paragraph' not in e:
        continue
    style = e['paragraph'].get('paragraphStyle', {}).get('namedStyleType', '')
    if style.startswith('HEADING') and para_text(e).strip() == 'Research Sources':
        rs_idx = i
        break

requests = []
converted = 0
skipped_existing = 0
table = None
if rs_idx is not None:
    for j in range(rs_idx + 1, len(content)):
        if 'table' in content[j]:
            table = content[j]['table']
            break

# A markdown link occupying the whole cell text: [label](url)
MD_LINK = re.compile(r'^\[([^\]]+)\]\((https?://[^)\s]+)\)$')

if table is not None:
    rows = table.get('tableRows', [])
    # Row 0 is the header (Name | URL | Notes); data rows start at row 1.
    for ri, row in enumerate(rows):
        if ri == 0:
            continue
        cells = row.get('tableCells', [])
        if len(cells) < 2:
            continue
        url_cell = cells[1]  # URL is column index 1
        # Gather text runs inside the cell.
        runs = []
        for ce in url_cell.get('content', []):
            for el in ce.get('paragraph', {}).get('elements', []):
                if 'textRun' in el:
                    runs.append(el)
        if not runs:
            continue
        # If any run already carries a real link, the cell is already clickable.
        if any(r['textRun'].get('textStyle', {}).get('link') for r in runs):
            skipped_existing += 1
            continue
        cell_text = ''.join(r['textRun'].get('content', '') for r in runs)
        stripped = cell_text.rstrip('\n')
        m = MD_LINK.match(stripped)
        if not m:
            continue
        label, url = m.group(1), m.group(2)
        # The literal markdown text starts at the first run's startIndex.
        text_start = runs[0]['startIndex']
        text_end = text_start + len(stripped)  # exclusive, excludes trailing newline
        # Replace literal `[label](url)` with just `label`, then link it.
        requests.append({"deleteContentRange": {
            "range": {"startIndex": text_start, "endIndex": text_end}}})
        requests.append({"insertText": {
            "location": {"index": text_start}, "text": label}})
        requests.append({"updateTextStyle": {
            "range": {"startIndex": text_start, "endIndex": text_start + len(label)},
            "textStyle": {"link": {"url": url}},
            "fields": "link"}})
        converted += 1

# Index-shifting safety: each row's edits are independent, but a delete+insert
# shifts every index after it. Apply the requests strictly bottom-up.
def req_index(r):
    if 'deleteContentRange' in r:
        return r['deleteContentRange']['range']['startIndex']
    if 'insertText' in r:
        return r['insertText']['location']['index']
    if 'updateTextStyle' in r:
        return r['updateTextStyle']['range']['startIndex']
    return 0
requests.sort(key=req_index, reverse=True)

print(json.dumps({
    "found_table": table is not None,
    "converted": converted,
    "skipped_existing": skipped_existing,
    "body": {"requests": requests}
}))
PYEOF
)

RS_FOUND=$(echo "$RS_LINK_REQ" | python3 -c "import json,sys; print(json.load(sys.stdin)['found_table'])")
RS_CONVERTED=$(echo "$RS_LINK_REQ" | python3 -c "import json,sys; print(json.load(sys.stdin)['converted'])")
RS_SKIPPED=$(echo "$RS_LINK_REQ" | python3 -c "import json,sys; print(json.load(sys.stdin)['skipped_existing'])")

if [ "$RS_FOUND" != "True" ]; then
  echo "   no Research Sources table found — skipping"
else
  echo "   $RS_CONVERTED markdown link(s) converted, $RS_SKIPPED already-clickable cell(s) left as-is"
  RS_REQ_COUNT=$(echo "$RS_LINK_REQ" | python3 -c "import json,sys; print(len(json.load(sys.stdin)['body']['requests']))")
  if [ "$RS_REQ_COUNT" -gt 0 ]; then
    RS_BODY=$(echo "$RS_LINK_REQ" | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin)['body']))")
    batch_update "$DOC_ID" RS_BODY 2>&1 | strip_noise > /dev/null
    echo "   applied $RS_REQ_COUNT URL-column hyperlink request(s)"
  fi
fi

echo ">> Done. Doc: https://docs.google.com/document/d/$DOC_ID/edit"
