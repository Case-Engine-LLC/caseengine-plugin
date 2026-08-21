#!/usr/bin/env bash
# topic-plan-surgical-edit.sh
#
# Surgical text replacement inside a published topic-plan Google Doc.
# Uses Docs API `replaceAllText` so comments, suggested edits, collaborator
# in-flight edits, and Doc formatting all survive untouched.
#
# Run this for EVERY edit after the first publish of a topic-plan Doc.
# Never re-run `topic-plan-formatting.sh` on a published Doc — that script
# wipes the Doc and re-uploads from markdown, which destroys every comment
# and edit anyone has made.
#
# Usage:
#   topic-plan-surgical-edit.sh \
#     --doc-id <docId> \
#     --find "<exact text currently in the doc>" \
#     --replace "<new text>" \
#     [--case-sensitive]
#
# Pass --find with enough surrounding context to be UNIQUE in the doc — if
# the same string appears multiple times, every occurrence is replaced.
# `--case-sensitive` defaults to true; pass `--case-insensitive` to match
# loosely.
#
# To run multiple replacements in one batch, repeat --find / --replace
# pairs:
#   topic-plan-surgical-edit.sh --doc-id X \
#     --find "old1" --replace "new1" \
#     --find "old2" --replace "new2"
#
# Exit codes:
#   0 = success (replacement count in stdout)
#   1 = arg error
#   2 = no replacements occurred (find string not found, will warn)
#
# IMPORTANT: After every surgical edit, also update the local canonical
# markdown at `deliverables/podcast-topics/{slug}/topic-plan/topic-plan-v{n}.md`
# so the source-of-truth doesn't drift from the live Drive Doc.

set -euo pipefail

DOC_ID=""
CASE_SENSITIVE="true"
FINDS=()
REPLACES=()

usage() {
  sed -n '2,40p' "$0"
  exit 1
}

while [ $# -gt 0 ]; do
  case "$1" in
    --doc-id) DOC_ID="$2"; shift 2 ;;
    --find) FINDS+=("$2"); shift 2 ;;
    --replace) REPLACES+=("$2"); shift 2 ;;
    --case-sensitive) CASE_SENSITIVE="true"; shift ;;
    --case-insensitive) CASE_SENSITIVE="false"; shift ;;
    -h|--help) usage ;;
    *) echo "Unknown arg: $1" >&2; usage ;;
  esac
done

if [ -z "$DOC_ID" ]; then
  echo "Missing --doc-id" >&2
  usage
fi

if [ "${#FINDS[@]}" -eq 0 ] || [ "${#FINDS[@]}" -ne "${#REPLACES[@]}" ]; then
  echo "Need at least one matched --find / --replace pair (got ${#FINDS[@]} finds, ${#REPLACES[@]} replaces)" >&2
  usage
fi

strip_noise() {
  grep -v '^Using keyring' | grep -v '^Warning:' || true
}

# Build the batchUpdate body from the find/replace pairs.
BODY=$(python3 - "${FINDS[@]}" "${REPLACES[@]}" <<PYEOF
import json, sys
case_sensitive = "$CASE_SENSITIVE" == "true"
n = len(sys.argv) - 1
half = n // 2
finds = sys.argv[1:1+half]
replaces = sys.argv[1+half:1+2*half]
requests = []
for f, r in zip(finds, replaces):
    requests.append({
        "replaceAllText": {
            "containsText": {"text": f, "matchCase": case_sensitive},
            "replaceText": r
        }
    })
print(json.dumps({"requests": requests}))
PYEOF
)

# Send it
RESP=$(gws docs documents batchUpdate \
  --params "{\"documentId\":\"$DOC_ID\"}" \
  --json "$BODY" 2>&1 | strip_noise)

TOTAL=$(echo "$RESP" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
except Exception as e:
    print(f'parse-error: {e}', file=sys.stderr)
    sys.exit(2)
total = 0
for rep in d.get('replies', []):
    if 'replaceAllText' in rep:
        total += rep['replaceAllText'].get('occurrencesChanged', 0)
print(total)
")

echo "replacements applied: $TOTAL"

if [ "$TOTAL" -eq 0 ]; then
  echo "WARNING: zero replacements — verify the --find string matches the doc text exactly (including punctuation, smart quotes, em-dashes)." >&2
  exit 2
fi
