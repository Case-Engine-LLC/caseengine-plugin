#!/usr/bin/env python3
"""
gws_helpers.py — thin wrappers around the `gws` CLI that get the
--params (query) vs --json (body) split right, and handle Shared Drive
names with apostrophes/commas/ampersands safely (no shell quoting).

Subcommands:
  ensure-folder <name> <parent_id>      -> prints folder id
  create-doc    <name> <parent_id> <md> -> prints doc id (md auto-converts)
  upload-raw    <name> <parent_id> <path> <mime> -> prints file id
"""
import sys, json, subprocess, tempfile, os

def gws(args, json_body=None, upload=None, upload_ct=None):
    cmd = ["gws"] + args
    tmp = None
    if json_body is not None:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(json_body, tmp)
        tmp.close()
        cmd += ["--json", "@" + tmp.name]
    if upload:
        cmd += ["--upload", upload]
        if upload_ct:
            cmd += ["--upload-content-type", upload_ct]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    finally:
        if tmp:
            os.unlink(tmp.name)
    # strip keyring/warning noise
    lines = [l for l in out.stdout.splitlines()
             if not l.startswith("Using keyring") and not l.startswith("Warning:")]
    return "\n".join(lines), out.stderr, out.returncode

def gws_json(args, **kw):
    """gws but with --json passed inline (gws supports @file OR inline)."""
    cmd = ["gws"] + args
    if "json_body" in kw and kw["json_body"] is not None:
        cmd += ["--json", json.dumps(kw["json_body"])]
    if kw.get("upload"):
        cmd += ["--upload", kw["upload"]]
        if kw.get("upload_ct"):
            cmd += ["--upload-content-type", kw["upload_ct"]]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    lines = [l for l in out.stdout.splitlines()
             if not l.startswith("Using keyring") and not l.startswith("Warning:")]
    return "\n".join(lines), out.stderr, out.returncode

FOLDER_MIME = "application/vnd.google-apps.folder"
DOC_MIME = "application/vnd.google-apps.document"

def q_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")

def ensure_folder(name, parent):
    # search
    q = (f"name='{q_escape(name)}' and '{parent}' in parents and "
         f"mimeType='{FOLDER_MIME}' and trashed=false")
    params = json.dumps({"q": q, "fields": "files(id,name)",
                         "supportsAllDrives": True,
                         "includeItemsFromAllDrives": True})
    out, err, rc = gws_json(["drive", "files", "list", "--params", params])
    try:
        files = json.loads(out).get("files", [])
    except Exception:
        files = []
    if files:
        return files[0]["id"]
    # create
    params = json.dumps({"supportsAllDrives": True, "fields": "id"})
    body = {"name": name, "mimeType": FOLDER_MIME, "parents": [parent]}
    out, err, rc = gws_json(["drive", "files", "create", "--params", params],
                            json_body=body)
    return json.loads(out)["id"]

def create_doc(name, parent, md_path):
    params = json.dumps({"supportsAllDrives": True, "fields": "id"})
    body = {"name": name, "mimeType": DOC_MIME, "parents": [parent]}
    out, err, rc = gws_json(["drive", "files", "create", "--params", params],
                            json_body=body, upload=md_path,
                            upload_ct="text/markdown")
    return json.loads(out)["id"]

def upload_raw(name, parent, path, mime):
    params = json.dumps({"supportsAllDrives": True, "fields": "id"})
    body = {"name": name, "parents": [parent]}
    out, err, rc = gws_json(["drive", "files", "create", "--params", params],
                            json_body=body, upload=path, upload_ct=mime)
    return json.loads(out)["id"]

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "ensure-folder":
        print(ensure_folder(sys.argv[2], sys.argv[3]))
    elif cmd == "create-doc":
        print(create_doc(sys.argv[2], sys.argv[3], sys.argv[4]))
    elif cmd == "upload-raw":
        print(upload_raw(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))
    else:
        sys.exit(f"unknown: {cmd}")
