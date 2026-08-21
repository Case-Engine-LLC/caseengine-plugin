#!/usr/bin/env bash
# process_one.sh <manifest_index>
# Prep one n-gram table -> create Drive folder chain -> upload branded
# Google Doc + raw source .md (+ .json) -> apply branded cover.
set -uo pipefail
IDX="$1"
WORK="/tmp/ngram-backfill"
H="$WORK/gws_helpers.py"

ROW=$(python3 -c "import json;print(json.dumps(json.load(open('$WORK/manifest.json'))[$IDX]))")
SRC_MD=$(echo "$ROW"   | python3 -c "import json,sys;print(json.load(sys.stdin)['src_md'])")
SRC_JSON=$(echo "$ROW" | python3 -c "import json,sys;r=json.load(sys.stdin);print(r['src_json'] or '')")
DRIVE_PATH=$(echo "$ROW" | python3 -c "import json,sys;print(json.load(sys.stdin)['drive_path'])")
PA=$(echo "$ROW"   | python3 -c "import json,sys;print(json.load(sys.stdin)['practice_area'])")
EP=$(echo "$ROW"   | python3 -c "import json,sys;print(json.load(sys.stdin)['episode'])")
LEAF=$(echo "$ROW" | python3 -c "import json,sys;print(json.load(sys.stdin)['scope_leaf'])")

# --- scope (Topic Only / Location / Extension) + scope line + header anchor ---
# SCOPE is authoritative and passed into prep_ngram.py - it decides whether
# the Local Anchors INTERNAL block renders.
case "$LEAF" in
  "Topic Only") SCOPE="Topic Only";  SCOPE_LINE="Topic Only - Foundation Table"; HANCHOR="$PA, Topic Only" ;;
  Locations/*)  SCOPE="Location";    L="${LEAF#Locations/}"; SCOPE_LINE="$L (Location)";  HANCHOR="$L" ;;
  Extensions/*) SCOPE="Extension";   L="${LEAF#Extensions/}"; SCOPE_LINE="$L (Extension)"; HANCHOR="$L" ;;
  *)            SCOPE="";            SCOPE_LINE="$LEAF"; HANCHOR="$LEAF" ;;
esac

# --- prep markdown ---
PREP_MD="$WORK/prepped/$IDX.md"
mkdir -p "$WORK/prepped"
META=$(python3 "$WORK/prep_ngram.py" "$SRC_MD" "$PREP_MD" "$SCOPE")
if [ $? -ne 0 ]; then echo "{\"idx\":$IDX,\"error\":\"prep failed\"}"; exit 1; fi
TOPIC=$(echo "$META"    | python3 -c "import json,sys;print(json.load(sys.stdin)['topic'])")
ROWCOUNT=$(echo "$META" | python3 -c "import json,sys;print(json.load(sys.stdin)['row_count'])")

# --- Drive folder chain ---
ROOT_FOLDER="1gATbaPKlcwGBLkStF5d2l68Y-qyLkqYE"
PA_ID=$(python3 "$H" ensure-folder "$PA" "$ROOT_FOLDER")
EP_ID=$(python3 "$H" ensure-folder "$EP" "$PA_ID")
if [[ "$LEAF" == */* ]]; then
  GRP="${LEAF%%/*}"; LOCNAME="${LEAF#*/}"
  GRP_ID=$(python3 "$H" ensure-folder "$GRP" "$EP_ID")
  DEST_ID=$(python3 "$H" ensure-folder "$LOCNAME" "$GRP_ID")
else
  DEST_ID=$(python3 "$H" ensure-folder "$LEAF" "$EP_ID")
fi
if [ -z "$DEST_ID" ]; then echo "{\"idx\":$IDX,\"error\":\"folder chain failed\"}"; exit 1; fi

# --- branded Google Doc ---
DOC_ID=$(python3 "$H" create-doc "N-Gram Table - $TOPIC" "$DEST_ID" "$PREP_MD")
if [ -z "$DOC_ID" ]; then echo "{\"idx\":$IDX,\"error\":\"doc create failed\"}"; exit 1; fi

RUNDATE=$(date +"%B %-d, %Y")
bash "$WORK/ngram_cover.sh" --doc-id "$DOC_ID" --subtitle "$TOPIC" \
  --scope "$SCOPE_LINE" --date "$RUNDATE" --header-anchor "$HANCHOR" >/dev/null 2>&1
COVER_RC=$?

# --- raw source .md ---
MD_ID=$(python3 "$H" upload-raw "$(basename "$SRC_MD")" "$DEST_ID" "$SRC_MD" "text/markdown")

# --- raw source .json (if present) ---
JSON_ID=""
if [ -n "$SRC_JSON" ] && [ -f "$SRC_JSON" ]; then
  JSON_ID=$(python3 "$H" upload-raw "$(basename "$SRC_JSON")" "$DEST_ID" "$SRC_JSON" "application/json")
fi

python3 -c "
import json
print(json.dumps({'idx':$IDX,'topic':'''$TOPIC''','rows':$ROWCOUNT,
  'drive_path':'''$DRIVE_PATH''','dest_id':'$DEST_ID','doc_id':'$DOC_ID',
  'md_id':'$MD_ID','json_id':'$JSON_ID','cover_rc':$COVER_RC}))
"
