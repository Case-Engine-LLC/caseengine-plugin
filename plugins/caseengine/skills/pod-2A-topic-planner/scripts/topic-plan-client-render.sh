#!/usr/bin/env bash
# topic-plan-client-render.sh
# Produce a CLIENT-SAFE clone of a topic plan markdown by truncating everything
# from the `# INTERNAL` H1 onward, then upload the truncated md as a NEW Google
# Doc named "Podcast Topic Plan - {Firm} (Client Share)" into the same parent
# folder as the source Doc.
#
# Use case: the master topic plan Doc carries an INTERNAL block (full topic
# library by practice area, held in reserve). Before sharing with the client,
# we ship them a copy that ends cleanly at the curated 12-episode plan + bonus
# episodes — no inventory leakage.
#
# This script does NOT touch the master Doc. It only writes:
#   1. Local sibling markdown:  {md-path-dir}/topic-plan-v1-client-share.md
#   2. New Google Doc:          "Podcast Topic Plan - {firm} (Client Share)"
#                               inside the same parent folder as --source-doc-id
#
# Branded cover + Roboto + table styling + headers/footers can be applied to
# the client-share Doc by re-running topic-plan-formatting.sh against the
# returned client doc + md ids. This script intentionally stops at "raw doc
# uploaded" to keep responsibilities separated.
#
# Usage:
#   topic-plan-client-render.sh \
#     --md-path <path-to-master-md> \
#     --source-doc-id <master-doc-id> \
#     --firm-name "Law Offices of Todd K. Mohink, PA"
#
# Optional:
#   --output-md-path <override>     default: sibling at {md-dir}/topic-plan-v1-client-share.md
#   --doc-name-override <override>  default: "Podcast Topic Plan - {firm} (Client Share)"

set -euo pipefail

MD_PATH=""
SOURCE_DOC_ID=""
FIRM_NAME=""
OUTPUT_MD_PATH=""
DOC_NAME_OVERRIDE=""

usage() {
  sed -n '2,33p' "$0"
  exit 1
}

while [ $# -gt 0 ]; do
  case "$1" in
    --md-path) MD_PATH="$2"; shift 2 ;;
    --source-doc-id) SOURCE_DOC_ID="$2"; shift 2 ;;
    --firm-name) FIRM_NAME="$2"; shift 2 ;;
    --output-md-path) OUTPUT_MD_PATH="$2"; shift 2 ;;
    --doc-name-override) DOC_NAME_OVERRIDE="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown arg: $1" >&2; usage ;;
  esac
done

for var in MD_PATH SOURCE_DOC_ID FIRM_NAME; do
  if [ -z "${!var}" ]; then
    echo "Missing required arg: --$(echo $var | tr '[:upper:]_' '[:lower:]-')" >&2
    usage
  fi
done

if [ ! -f "$MD_PATH" ]; then
  echo "Markdown file not found: $MD_PATH" >&2
  exit 2
fi

# Default output path = sibling of source md
if [ -z "$OUTPUT_MD_PATH" ]; then
  MD_DIR=$(dirname "$MD_PATH")
  MD_BASE=$(basename "$MD_PATH" .md)
  OUTPUT_MD_PATH="${MD_DIR}/${MD_BASE}-client-share.md"
fi

if [ -z "$DOC_NAME_OVERRIDE" ]; then
  DOC_NAME="Podcast Topic Plan - ${FIRM_NAME} (Client Share)"
else
  DOC_NAME="$DOC_NAME_OVERRIDE"
fi

strip_noise() {
  grep -v '^Using keyring' | grep -v '^Warning:' || true
}

echo ">> [1/4] Truncating markdown at '# INTERNAL'"
# Truncate at the first line that is exactly `# INTERNAL` (no leading/trailing
# spaces). Everything before that line (exclusive) is kept. Trailing whitespace
# trimmed to keep the file clean.
python3 - "$MD_PATH" "$OUTPUT_MD_PATH" <<'PYEOF'
import sys, pathlib, re
src = pathlib.Path(sys.argv[1])
dst = pathlib.Path(sys.argv[2])
lines = src.read_text().splitlines()
out = []
cut_marker = re.compile(r'^# INTERNAL\s*$')
for line in lines:
    if cut_marker.match(line):
        break
    out.append(line)
# Trim trailing blank lines
while out and not out[-1].strip():
    out.pop()
dst.write_text("\n".join(out) + "\n")
print(f"   wrote {dst} ({len(out)} lines)")
PYEOF

if [ ! -s "$OUTPUT_MD_PATH" ]; then
  echo "ERROR: Truncated md is empty — '# INTERNAL' may have matched the very first line, or md is malformed." >&2
  exit 3
fi

echo ">> [2/4] Resolving parent folder of source Doc (fileId=$SOURCE_DOC_ID)"
PARENT_FOLDER_ID=$(gws drive files get \
  --params "{\"fileId\":\"$SOURCE_DOC_ID\",\"fields\":\"id,name,parents\",\"supportsAllDrives\":true}" 2>&1 \
  | strip_noise \
  | python3 -c "import json,sys; d=json.load(sys.stdin); ps=d.get('parents',[]); print(ps[0] if ps else '')")

if [ -z "$PARENT_FOLDER_ID" ]; then
  echo "ERROR: Could not resolve parent folder for source Doc $SOURCE_DOC_ID" >&2
  exit 4
fi
echo "   parent folder: $PARENT_FOLDER_ID"

echo ">> [3/4] Creating client-share Google Doc '$DOC_NAME' in parent folder"
# files.create with mimeType=application/vnd.google-apps.document on a
# text/markdown upload triggers Drive's auto-convert (md → Google Doc).
CREATE_PARAMS=$(python3 -c "
import json
print(json.dumps({
  'fields': 'id,name,webViewLink,parents',
  'supportsAllDrives': True
}))
")

CREATE_BODY=$(python3 -c "
import json
print(json.dumps({
  'name': '''$DOC_NAME''',
  'mimeType': 'application/vnd.google-apps.document',
  'parents': ['$PARENT_FOLDER_ID']
}))
")

CREATE_RESP=$(gws drive files create \
  --params "$CREATE_PARAMS" \
  --body "$CREATE_BODY" \
  --upload "$OUTPUT_MD_PATH" \
  --upload-content-type "text/markdown" 2>&1 | strip_noise)

NEW_DOC_ID=$(echo "$CREATE_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('id',''))")
NEW_DOC_URL=$(echo "$CREATE_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('webViewLink',''))")

if [ -z "$NEW_DOC_ID" ]; then
  echo "ERROR: files.create did not return an id. Raw response:" >&2
  echo "$CREATE_RESP" >&2
  exit 5
fi

echo "   created Doc id: $NEW_DOC_ID"
echo "   url: $NEW_DOC_URL"

echo ">> [4/4] Done."
echo ""
echo "Truncated md:      $OUTPUT_MD_PATH"
echo "Client-share Doc:  $NEW_DOC_URL"
echo ""
echo "NEXT: apply branded cover + Roboto + table styling by running:"
echo "  topic-plan-formatting.sh \\"
echo "    --doc-id $NEW_DOC_ID \\"
echo "    --md-id <upload the truncated md as a .md sibling first, then pass its id here> \\"
echo "    --md-path $OUTPUT_MD_PATH \\"
echo "    --firm-name \"$FIRM_NAME\" \\"
echo "    --location-display \"...\" \\"
echo "    --header-anchor \"...\" \\"
echo "    --date \"...\""
