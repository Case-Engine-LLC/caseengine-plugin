#!/usr/bin/env python3
"""Keywords Everywhere volume backfill for 2B keyword-research artifacts.

Fetches real Google Keyword Planner volume + CPC via the Keywords Everywhere
API (dataSource=gkp) and writes it into existing keyword-research.json files,
replacing the prior LLM-estimated volume.

The KE API key is NEVER hardcoded -- it is read from the env var KE_API_KEY,
which the caller resolves from 1Password ("Keywords Everywhere API Key",
caseengine account, Dev/Paid team vault) at runtime.

Usage:
    KE_API_KEY=$(...) python3 ke_volume_backfill.py [BASE_DIR]

Reusable: fetch_ke_volumes(keywords) is the standalone volume lookup helper.
"""
import os, sys, json, time, glob, urllib.request, urllib.parse

KE_URL = "https://api.keywordseverywhere.com/v1/get_keyword_data"
BATCH = 100


def fetch_ke_volumes(keywords, key):
    """keywords: list[str] -> {keyword_lower: {vol, cpc, competition, trend}}."""
    out, credits_used = {}, 0
    uniq = sorted({k for k in keywords if k and k.strip()})
    for i in range(0, len(uniq), BATCH):
        chunk = uniq[i:i + BATCH]
        params = [("dataSource", "gkp"), ("country", "us"), ("currency", "usd")]
        params += [("kw[]", k) for k in chunk]
        req = urllib.request.Request(
            KE_URL, data=urllib.parse.urlencode(params).encode(),
            headers={"Authorization": f"Bearer {key}"})
        resp = None
        for attempt in range(4):
            try:
                resp = json.load(urllib.request.urlopen(req, timeout=90))
                break
            except Exception as e:
                if attempt == 3:
                    raise
                time.sleep(4)
        for row in resp.get("data", []):
            cpc = row.get("cpc") or {}
            out[row["keyword"].strip().lower()] = {
                "vol": row.get("vol", 0) or 0,
                "cpc": cpc.get("value", 0) or 0,
                "competition": row.get("competition", 0) or 0,
                "trend": row.get("trend", []),
            }
        credits_used += resp.get("credits_consumed", 0)
        print(f"  batch {i // BATCH + 1}/{(len(uniq) + BATCH - 1) // BATCH}: "
              f"{len(chunk)} kw | credits remaining {resp.get('credits')}")
    print(f"unique keywords looked up: {len(uniq)} | credits consumed: {credits_used}")
    return out


def collect_scope_files(base):
    """The 19 batch scope keyword-research.json files (exclude tx-houston +
    the stray top-level scratch dir)."""
    files = []
    for f in sorted(glob.glob(os.path.join(base, "**", "keyword-research.json"),
                              recursive=True)):
        rel = os.path.relpath(f, base)
        if "tx-houston" in rel:          # pre-existing, not a batch scope
            continue
        if rel == os.path.join("02.5-keywords", "keyword-research.json"):
            continue                      # stray top-level scratch dir
        files.append(f)
    return files


def main():
    key = os.environ.get("KE_API_KEY")
    if not key:
        sys.exit("ERROR: KE_API_KEY env var not set")
    base = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
        "~/Desktop/claude_code/deliverables/podcast-research/car-accidents")

    files = collect_scope_files(base)
    print(f"{len(files)} keyword-research.json scope files:")
    for f in files:
        print("  ", os.path.relpath(f, base))
    if len(files) != 19:
        print(f"WARNING: expected 19 batch scopes, found {len(files)}")

    kw = set()
    for f in files:
        d = json.load(open(f))
        kw.update(k["query"] for k in d.get("keywords", []) if k.get("query"))
        kw.update(s["query"] for s in d.get("search_queries", []) if s.get("query"))
    print(f"\nfetching real volume for {len(kw)} unique keywords from Keywords Everywhere...")
    vmap = fetch_ke_volumes(list(kw), key)

    mapfile = os.path.join(base, "keyword-volume-map.json")
    json.dump(vmap, open(mapfile, "w"), indent=1, sort_keys=True)
    print(f"volume map saved: {mapfile}\n")

    for f in files:
        d = json.load(open(f))
        hit = miss = 0
        for k in d.get("keywords", []):
            v = vmap.get((k.get("query") or "").strip().lower())
            if v:
                k["msv"] = v["vol"]
                k["cpc"] = v["cpc"]
                k["data_source"] = "keywords_everywhere_gkp"
                hit += 1
            else:
                k["data_source"] = k.get("data_source", "llm_estimate")
                miss += 1
        for s in d.get("search_queries", []):
            v = vmap.get((s.get("query") or "").strip().lower())
            if v:
                s["monthly_volume"] = v["vol"]
                s["source"] = "keywords_everywhere_gkp"
        prov = d.setdefault("provenance", {})
        prov["volume_source"] = "keywords_everywhere_gkp"
        prov["volume_backfill_date"] = "2026-05-21"
        prov["data_source"] = "keywords_everywhere_gkp (volume/cpc); llm_estimate (kd)"
        json.dump(d, open(f, "w"), indent=2)
        print(f"  {os.path.relpath(f, base)}: {hit} updated, {miss} not found")
    print("\nbackfill complete.")


if __name__ == "__main__":
    main()
