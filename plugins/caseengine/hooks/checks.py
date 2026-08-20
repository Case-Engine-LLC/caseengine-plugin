#!/usr/bin/env python3
"""Automated checks that turn QA checkboxes into evidence.

A large share of the Case Engine checklist is not judgment. "Is GTM installed",
"is this page in the sitemap", "does the 404 work", "is there a placeholder left
in the copy" — these are assertions about a live site that a machine can settle
faster and more honestly than a person clicking through a list. Roughly 575 task
rows across the corpus are of that kind, and because three quarters of all tasks
are template redeployments, a check written once pays off on every future client.

Each check answers one question against a live URL and returns a verdict that
can be recorded as evidence. Deliberately dependency-free — urllib and re — so
it runs on any machine with Python and no install step.

    checks.py --url https://client.com/ --check tracking --expect-gtm GTM-XXXX
    checks.py --url https://client.com/ --check all --json
    checks.py --url https://client.com/page/ --check sitemap --task <uuid> --record

`--record` writes the result into the evidence ledger, which is what makes a
check count toward closing a task rather than just printing to a terminal.

What this deliberately does NOT do: decide whether a site passes ADA, whether
copy is good, or whether a design works. Those are judgment and stay with
people. A scanner that claims otherwise is worse than no scanner.
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

UA = "Mozilla/5.0 (compatible; CaseEngineChecks/1.0; +https://caseengine.com)"
TIMEOUT = 20


def fetch(url: str, bust: bool = True) -> tuple[int, dict, str]:
    """GET a URL, cache-busted by default. Returns (status, headers, body).

    Cache-busting matters more than it sounds: nearly every client site is
    behind a CDN, and checking a cached copy is how you confirm a change that
    isn't actually live yet.
    """
    target = url
    if bust:
        target += ("&" if "?" in url else "?") + "cechk=1"
    request = urllib.request.Request(target, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            raw = response.read()
            if response.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            charset = response.headers.get_content_charset() or "utf-8"
            return response.status, dict(response.headers), raw.decode(charset, "replace")
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", "replace")
        except Exception:
            pass
        return exc.code, dict(exc.headers or {}), body
    except Exception as exc:
        return 0, {}, f"__fetch_error__ {exc}"


def result(name: str, ok: bool, summary: str, **detail) -> dict:
    return {"check": name, "status": "pass" if ok else "failed", "summary": summary, **detail}


# --------------------------------------------------------------------------- #
# checks
# --------------------------------------------------------------------------- #

def check_reachable(url: str, _args) -> dict:
    status, _headers, body = fetch(url)
    if body.startswith("__fetch_error__"):
        return result("reachable", False, f"could not fetch: {body[16:][:120]}", http_status=0)
    return result("reachable", 200 <= status < 300, f"HTTP {status}", http_status=status)


TAG_PATTERNS = {
    "gtm": re.compile(r"GTM-[A-Z0-9]{4,10}"),
    "ga4": re.compile(r"G-[A-Z0-9]{8,12}"),
    "clarity": re.compile(r"clarity\.ms/tag/([a-z0-9]+)", re.I),
    "callrail": re.compile(r"callrail\.com/companies/(\d+)", re.I),
}


def check_tracking(url: str, args) -> dict:
    """Presence of a tag is not proof — the *right* container is.

    The corpus is full of tasks like "please add this client's GTM, for some
    reason they have none", which is exactly the failure a nightly version of
    this catches on the day it happens rather than at the next audit.
    """
    status, _headers, body = fetch(url)
    if status == 0:
        return result("tracking", False, "could not fetch the page")
    found = {name: sorted(set(m if isinstance(m, str) else m for m in pattern.findall(body)))
             for name, pattern in TAG_PATTERNS.items()}
    found = {k: v for k, v in found.items() if v}

    expected = {k: v for k, v in {"gtm": args.expect_gtm, "ga4": args.expect_ga4}.items() if v}
    if not expected:
        ok = bool(found)
        return result("tracking", ok,
                      "found " + ", ".join(f"{k}={v[0]}" for k, v in found.items()) if ok
                      else "no tracking tags found in page source",
                      found=found, note="no expected IDs given, so presence only")

    mismatches = []
    for key, want in expected.items():
        got = found.get(key, [])
        if want not in got:
            mismatches.append(f"expected {key.upper()} {want}, found {got or 'none'}")
    return result("tracking", not mismatches,
                  "all expected tags present and correct" if not mismatches else "; ".join(mismatches),
                  found=found, expected=expected)


def check_indexable(url: str, _args) -> dict:
    status, headers, body = fetch(url)
    if status == 0:
        return result("indexable", False, "could not fetch the page")
    blockers = []
    robots_header = headers.get("X-Robots-Tag", "")
    if "noindex" in robots_header.lower():
        blockers.append(f"X-Robots-Tag: {robots_header}")
    for match in re.findall(r'<meta[^>]+name=["\']robots["\'][^>]*>', body, re.I):
        if "noindex" in match.lower():
            blockers.append(match.strip()[:120])
    return result("indexable", not blockers,
                  "page is indexable" if not blockers else "; ".join(blockers),
                  blockers=blockers, http_status=status)


def check_sitemap(url: str, _args) -> dict:
    """Does a sitemap exist, and is this URL in it?"""
    parsed = urlparse(url)
    root = f"{parsed.scheme}://{parsed.netloc}"
    candidates = ["/sitemap_index.xml", "/sitemap.xml", "/sitemap-index.xml", "/wp-sitemap.xml"]
    seen: list[str] = []
    urls: set[str] = set()
    for path in candidates:
        status, _headers, body = fetch(urljoin(root, path), bust=False)
        if status != 200 or "<" not in body:
            continue
        seen.append(path)
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body)
        for loc in locs:
            if loc.endswith(".xml"):
                sub_status, _h, sub_body = fetch(loc, bust=False)
                if sub_status == 200:
                    urls.update(re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sub_body))
            else:
                urls.add(loc)
        break
    if not seen:
        return result("sitemap", False, "no sitemap found at any usual path", tried=candidates)
    target = url.split("?")[0].rstrip("/")
    present = any(u.split("?")[0].rstrip("/") == target for u in urls)
    return result("sitemap", present,
                  f"sitemap {seen[0]} has {len(urls)} URLs; this page is "
                  + ("present" if present else "MISSING"),
                  sitemap=seen[0], total_urls=len(urls), page_present=present)


def check_schema(url: str, _args) -> dict:
    """JSON-LD present, parseable, and free of obvious placeholders."""
    status, _headers, body = fetch(url)
    if status == 0:
        return result("schema", False, "could not fetch the page")
    blocks = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', body, re.I | re.S
    )
    if not blocks:
        return result("schema", False, "no JSON-LD found on the page")
    types, broken, placeholders = [], 0, []
    for block in blocks:
        try:
            parsed = json.loads(block.strip())
        except json.JSONDecodeError:
            broken += 1
            continue
        text = json.dumps(parsed)
        for token in ("example.com", "lorem ipsum", "{{", "YOUR_", "PLACEHOLDER", "TODO"):
            if token.lower() in text.lower():
                placeholders.append(token)
        for item in parsed if isinstance(parsed, list) else [parsed]:
            if isinstance(item, dict) and item.get("@type"):
                found_type = item["@type"]
                types.extend(found_type if isinstance(found_type, list) else [found_type])
    ok = broken == 0 and not placeholders
    parts = [f"{len(blocks)} JSON-LD block(s)", f"types: {', '.join(sorted(set(types))) or 'none'}"]
    if broken:
        parts.append(f"{broken} failed to parse")
    if placeholders:
        parts.append(f"placeholders: {', '.join(sorted(set(placeholders)))}")
    return result("schema", ok, "; ".join(parts),
                  types=sorted(set(types)), invalid_blocks=broken,
                  placeholders=sorted(set(placeholders)))


def check_404(url: str, _args) -> dict:
    parsed = urlparse(url)
    root = f"{parsed.scheme}://{parsed.netloc}"
    probe = urljoin(root, "/this-page-should-not-exist-ce-check/")
    status, _headers, body = fetch(probe, bust=False)
    styled = len(body) > 1000
    ok = status == 404
    return result("custom_404", ok,
                  f"garbage URL returned HTTP {status}"
                  + (", with a real page body" if ok and styled else "")
                  + ("" if ok else " — should be 404"),
                  http_status=status, body_bytes=len(body))


PLACEHOLDER_TOKENS = ["lorem ipsum", "dolor sit amet", "your business name here",
                      "insert text", "coming soon...", "[client]", "{{"]


def check_placeholders(url: str, _args) -> dict:
    status, _headers, body = fetch(url)
    if status == 0:
        return result("placeholders", False, "could not fetch the page")
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", body, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    hits = [token for token in PLACEHOLDER_TOKENS if token in text.lower()]
    return result("placeholders", not hits,
                  "no placeholder text found" if not hits else f"found: {', '.join(hits)}",
                  found=hits)


def check_https_images(url: str, _args) -> dict:
    status, _headers, body = fetch(url)
    if status == 0:
        return result("https_images", False, "could not fetch the page")
    insecure = sorted(set(re.findall(r'<img[^>]+src=["\'](http://[^"\']+)', body, re.I)))
    return result("https_images", not insecure,
                  "all image URLs are https" if not insecure
                  else f"{len(insecure)} image(s) served over http",
                  insecure=insecure[:10])


CHECKS = {
    "reachable": check_reachable,
    "tracking": check_tracking,
    "indexable": check_indexable,
    "sitemap": check_sitemap,
    "schema": check_schema,
    "custom_404": check_404,
    "placeholders": check_placeholders,
    "https_images": check_https_images,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run automated checks against a live URL.")
    parser.add_argument("--url", required=True)
    parser.add_argument("--check", default="all", help=f"one of {sorted(CHECKS)} or 'all'")
    parser.add_argument("--expect-gtm", default="", help="expected GTM container id")
    parser.add_argument("--expect-ga4", default="", help="expected GA4 measurement id")
    parser.add_argument("--task", default="", help="campaign_task UUID to record evidence against")
    parser.add_argument("--record", action="store_true", help="write results to the evidence ledger")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    names = sorted(CHECKS) if args.check == "all" else [args.check]
    unknown = [n for n in names if n not in CHECKS]
    if unknown:
        print(f"unknown check(s): {', '.join(unknown)}", file=sys.stderr)
        return 2

    results = [CHECKS[name](args.url, args) for name in names]
    failed = [r for r in results if r["status"] != "pass"]

    if args.record:
        if not args.task:
            print("--record needs --task", file=sys.stderr)
            return 2
        from ledger import append  # noqa: E402
        for item in results:
            append({
                "kind": "verify",
                "task_id": args.task.strip(),
                "status": item["status"],
                "observed": args.url,
                "note": f"{item['check']}: {item['summary']}",
                "method": "caseengine checks.py",
                "detail": item,
            })

    if args.json:
        print(json.dumps({"url": args.url, "passed": len(results) - len(failed),
                          "failed": len(failed), "results": results}, indent=2))
        return 1 if failed else 0

    print(f"\n{args.url}")
    for item in results:
        mark = "PASS" if item["status"] == "pass" else "FAIL"
        print(f"  [{mark}] {item['check']:14s} {item['summary']}")
    print(f"\n{len(results) - len(failed)} passed, {len(failed)} failed")
    if args.record:
        print(f"recorded against task {args.task}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
