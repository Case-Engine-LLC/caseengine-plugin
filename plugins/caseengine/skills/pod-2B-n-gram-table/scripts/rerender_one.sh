#!/usr/bin/env bash
# rerender_one.sh <manifest_index>
# Re-render an already-uploaded n-gram Doc IN PLACE: re-prep md (metadata
# line dropped), files.update the body into the existing Doc (preserves
# fileId + URL), re-apply branded cover.
set -uo pipefail
IDX="$1"
WORK="/tmp/ngram-backfill"
strip_noise() { grep -v '^Using keyring' | grep -v '^Warning:' || true; }

RESULT="$WORK/results/$IDX.json"
DOC_ID=$(python3 -c "import json;print(json.load(open('$RESULT'))['doc_id'])")
ROW=$(python3 -c "import json;print(json.dumps(json.load(open('$WORK/manifest.json'))[$IDX]))")
SRC_MD=$(echo "$ROW" | python3 -c "import json,sys;print(json.load(sys.stdin)['src_md'])")
LEAF=$(echo "$ROW"   | python3 -c "import json,sys;print(json.load(sys.stdin)['scope_leaf'])")
PA=$(echo "$ROW"     | python3 -c "import json,sys;print(json.load(sys.stdin)['practice_area'])")

# resolve scope (Topic Only / Location / Extension) - authoritative, passed
# into prep_ngram.py so it knows whether to render the Local Anchors block.
case "$LEAF" in
  "Topic Only") SCOPE="Topic Only";  SCOPE_LINE="Topic Only - Foundation Table"; HANCHOR="$PA, Topic Only" ;;
  Locations/*)  SCOPE="Location";    L="${LEAF#Locations/}"; SCOPE_LINE="$L (Location)";  HANCHOR="$L" ;;
  Extensions/*) SCOPE="Extension";   L="${LEAF#Extensions/}"; SCOPE_LINE="$L (Extension)"; HANCHOR="$L" ;;
  *)            SCOPE="";            SCOPE_LINE="$LEAF"; HANCHOR="$LEAF" ;;
esac

# re-prep (metadata line dropped; INTERNAL rendered with the locked 4 blocks)
PREP_MD="$WORK/prepped/$IDX.md"
META=$(python3 "$WORK/prep_ngram.py" "$SRC_MD" "$PREP_MD" "$SCOPE")
TOPIC=$(echo "$META" | python3 -c "import json,sys;print(json.load(sys.stdin)['topic'])")

# files.update the body into the existing Doc (auto-convert, fileId preserved)
gws drive files update \
  --params "{\"fileId\":\"$DOC_ID\",\"supportsAllDrives\":true,\"fields\":\"id\"}" \
  --upload "$PREP_MD" --upload-content-type "text/markdown" 2>&1 | strip_noise > /dev/null

# re-apply branded cover
RUNDATE=$(date +"%B %-d, %Y")
bash "$WORK/ngram_cover.sh" --doc-id "$DOC_ID" --subtitle "$TOPIC" \
  --scope "$SCOPE_LINE" --date "$RUNDATE" --header-anchor "$HANCHOR" >/dev/null 2>&1
echo "{\"idx\":$IDX,\"doc_id\":\"$DOC_ID\",\"cover_rc\":$?}"
