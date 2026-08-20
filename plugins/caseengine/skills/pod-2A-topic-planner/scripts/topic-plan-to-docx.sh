#!/usr/bin/env bash
# topic-plan-to-docx.sh
# Render a topic-plan markdown to .docx using pandoc + the canonical CE
# reference docx as the style template. Produces a Word/PDF-friendly local
# copy that inherits the same visual standard as the entity-research
# reference: Calibri/Roboto fonts, CE Blue (#4f81bd / #3573ff) headings,
# blue-bordered tables, page header + footer.
#
# Output is the third local artifact (alongside .md and .json) in the
# pod-3-topic-planner output contract. Word users open this directly; PDF
# distribution renders from this via Word's "Save as PDF" (or
# libreoffice --headless --convert-to pdf if installed).
#
# Reference docx lives baked-in at:
#   {skill-dir}/references/templates/topic-plan-reference.docx
# Copied from pod-1A-entity-research's gold-standard example so pod-3 is
# self-contained — no cross-skill runtime dependency.
#
# Usage:
#   topic-plan-to-docx.sh \
#     --md-path /path/to/topic-plan-v1.md \
#     [--out-path /path/to/topic-plan-v1.docx]    # default: md-path with .docx ext
#     [--reference-docx /path/override.docx]      # default: baked-in template
#     [--header-anchor "Maryland"]                # page header text after "Podcast Topic Plan |"
#                                                 # default: omits the anchor segment
#
# When --header-anchor is passed, the reference docx's page header is patched
# in-place from "Case Engine | Entity Research | Car Accidents, Topic Only"
# (the reference's literal text) to "Case Engine | Podcast Topic Plan |
# {anchor}". Footer text ("Case Engine | Confidential ... Page") is preserved
# verbatim — it's already correct for any CE deliverable.
#
# Exit codes:
#   0  success
#   1  bad args / usage
#   2  md-path missing
#   3  reference docx missing
#   4  pandoc not installed
#   5  pandoc render failed
#   6  post-render header patch failed

set -euo pipefail

# Resolve script dir so we can find the baked-in reference docx regardless
# of where the script is invoked from.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_REF_DOCX="$SCRIPT_DIR/../templates/topic-plan-reference.docx"

MD_PATH=""
OUT_PATH=""
REF_DOCX="$DEFAULT_REF_DOCX"
HEADER_ANCHOR=""

usage() {
  sed -n '2,40p' "$0"
  exit 1
}

while [ $# -gt 0 ]; do
  case "$1" in
    --md-path) MD_PATH="$2"; shift 2 ;;
    --out-path) OUT_PATH="$2"; shift 2 ;;
    --reference-docx) REF_DOCX="$2"; shift 2 ;;
    --header-anchor) HEADER_ANCHOR="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown arg: $1" >&2; usage ;;
  esac
done

if [ -z "$MD_PATH" ]; then
  echo "Missing required arg: --md-path" >&2
  usage
fi

if [ ! -f "$MD_PATH" ]; then
  echo "Markdown file not found: $MD_PATH" >&2
  exit 2
fi

if [ ! -f "$REF_DOCX" ]; then
  echo "Reference docx not found: $REF_DOCX" >&2
  echo "Expected baked-in template at: $DEFAULT_REF_DOCX" >&2
  exit 3
fi

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc not installed. Install via: brew install pandoc" >&2
  exit 4
fi

# Default out-path: same stem as md, .docx extension
if [ -z "$OUT_PATH" ]; then
  MD_DIR=$(dirname "$MD_PATH")
  MD_BASE=$(basename "$MD_PATH" .md)
  OUT_PATH="${MD_DIR}/${MD_BASE}.docx"
fi

echo ">> [1/3] Rendering $MD_PATH -> $OUT_PATH"
echo "         reference: $REF_DOCX"

# pandoc flags:
#   --from gfm           — parse as GitHub-flavored markdown (preserves
#                          pipe tables, the <br> tags pod-3 uses inside
#                          table cells for multi-line keyword lists)
#   --to docx            — render to Word/OOXML
#   --reference-doc      — inherit styles (fonts, colors, table style,
#                          headers/footers) from the canonical template
#   --standalone         — emit a complete document, not a fragment
if ! pandoc \
  --from gfm \
  --to docx \
  --reference-doc="$REF_DOCX" \
  --standalone \
  -o "$OUT_PATH" \
  "$MD_PATH"; then
  echo "ERROR: pandoc render failed" >&2
  exit 5
fi

if [ ! -s "$OUT_PATH" ]; then
  echo "ERROR: pandoc produced an empty file at $OUT_PATH" >&2
  exit 5
fi

# Post-render: patch header1.xml inside the docx to swap the reference's
# "Entity Research | Car Accidents, Topic Only" text for a topic-plan
# header. The reference docx's footer is generic ("Case Engine | Confidential
# ... Page N") and stays untouched.
echo ">> [2/3] Patching docx page header"
PATCH_OK=$(python3 - "$OUT_PATH" "$HEADER_ANCHOR" <<'PYEOF'
import sys, zipfile, shutil, re, tempfile, os, pathlib
docx_path = pathlib.Path(sys.argv[1])
anchor = sys.argv[2] if len(sys.argv) > 2 else ""

# Header text rule:
#   - If anchor provided:   "Case Engine | Podcast Topic Plan | {anchor}"
#   - If anchor empty:      "Case Engine | Podcast Topic Plan"
# Reference docx literal:   "Case Engine  |  Entity Research  |  Car Accidents, Topic Only"
# Pandoc uses two-space padding around the pipe — preserve that.
if anchor:
    new_text = f"Case Engine  |  Podcast Topic Plan  |  {anchor}"
else:
    new_text = "Case Engine  |  Podcast Topic Plan"

# Exact literal from the reference docx header (Case Engine | Entity
# Research | Car Accidents, Topic Only). Pattern is permissive: any
# "Case Engine ... Topic Only" substring inside header1.xml's <w:t> gets
# replaced. If the substring isn't found, we no-op silently (a different
# reference docx may have been swapped in).
ref_pattern = re.compile(
    r'(<w:t[^>]*>)Case Engine\s*\|\s*Entity Research[^<]*</w:t>',
    re.IGNORECASE
)

tmp_path = docx_path.with_suffix('.patched.docx')
patched_any = False
with zipfile.ZipFile(docx_path, 'r') as zin:
    with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.namelist():
            data = zin.read(item)
            if item.startswith('word/header') and item.endswith('.xml'):
                try:
                    text = data.decode('utf-8')
                    new_text_xml = re.sub(
                        ref_pattern,
                        lambda m: f"{m.group(1)}{new_text}</w:t>",
                        text
                    )
                    if new_text_xml != text:
                        patched_any = True
                        data = new_text_xml.encode('utf-8')
                except UnicodeDecodeError:
                    pass
            zout.writestr(item, data)
shutil.move(str(tmp_path), str(docx_path))
print("patched" if patched_any else "no-op")
PYEOF
) || {
  echo "ERROR: post-render header patch failed" >&2
  exit 6
}
echo "         header patch: $PATCH_OK"

echo ">> [3/3] Done."
echo ""
echo "Local .docx: $OUT_PATH"
