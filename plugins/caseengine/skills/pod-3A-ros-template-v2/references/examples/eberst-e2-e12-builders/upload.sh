#!/bin/bash
# upload.sh <docx> <title>  -> creates a Google Doc in the [TEST] folder, prints the link.
# Revisions must use files.update against the existing fileId, never create-and-replace.
set -e
DOCX="$1"; TITLE="$2"; PARENT="0ANhQ9dGZ4GGaUk9PVA"
DOCXMIME="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
EXISTING=$(gws drive files list --params "{\"q\":\"name = '$TITLE' and trashed = false\",\"supportsAllDrives\":true,\"includeItemsFromAllDrives\":true,\"fields\":\"files(id)\"}" 2>/dev/null | python3 -c "import sys,json;d=sys.stdin.read();d=d[d.index('{'):];f=json.loads(d).get('files',[]);print(f[0]['id'] if f else '')")
if [ -n "$EXISTING" ]; then
  gws drive files update --params "{\"fileId\":\"$EXISTING\",\"supportsAllDrives\":true}" --upload "$DOCX" --upload-content-type "$DOCXMIME" >/dev/null
  echo "UPDATED https://docs.google.com/document/d/$EXISTING/edit"
else
  NEW=$(gws drive files create --json "{\"name\":\"$TITLE\",\"mimeType\":\"application/vnd.google-apps.document\",\"parents\":[\"$PARENT\"]}" --upload "$DOCX" --upload-content-type "$DOCXMIME" 2>/dev/null | python3 -c "import sys,json;d=sys.stdin.read();d=d[d.index('{'):];print(json.loads(d)['id'])")
  echo "CREATED https://docs.google.com/document/d/$NEW/edit"
fi
