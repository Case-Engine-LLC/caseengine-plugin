#!/usr/bin/env python3
"""
What: Fetches Reddit posts and top comments for topic queries
Input: JSON with {"queries": ["topic 1", ...], "subreddits": ["legaladvice", ...]}
       via stdin or file argument
Output: JSON with posts and comments to stdout
Re-run: Safe — stateless, no side effects
Env: REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET required
"""

import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
import time

CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET", "")
USER_AGENT = "ce-virality-research/1.0 (by Case Engine)"

_token = None
_token_expires = 0


def get_token():
    """Get OAuth2 token using client_credentials grant."""
    global _token, _token_expires
    if _token and time.time() < _token_expires:
        return _token

    data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(
        "https://www.reddit.com/api/v1/access_token",
        data=data,
        method="POST",
    )
    # Basic auth with client_id:client_secret
    import base64
    creds = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    req.add_header("Authorization", f"Basic {creds}")
    req.add_header("User-Agent", USER_AGENT)

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            _token = result["access_token"]
            _token_expires = time.time() + result.get("expires_in", 3600) - 60
            return _token
    except Exception as e:
        print(f"Reddit auth error: {e}", file=sys.stderr)
        return None


def api_get(path, params=None):
    """Make authenticated GET to Reddit's OAuth API."""
    token = get_token()
    if not token:
        return None

    url = f"https://oauth.reddit.com{path}"
    if params:
        url += f"?{urllib.parse.urlencode(params)}"

    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("User-Agent", USER_AGENT)

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 429:
            retry_after = int(e.headers.get("Retry-After", 5))
            print(f"Rate limited. Waiting {retry_after}s...", file=sys.stderr)
            time.sleep(retry_after)
            return api_get(path, params)
        body = e.read().decode() if e.fp else ""
        print(f"Reddit API error {e.code}: {body[:200]}", file=sys.stderr)
        return None


def search_posts(query, subreddits=None, sort="relevance", limit=25):
    """Search Reddit for posts matching query."""
    params = {
        "q": query,
        "sort": sort,
        "limit": limit,
        "t": "year",  # last year
        "type": "link",
    }
    if subreddits:
        # Search within specific subreddits
        sr_string = "+".join(subreddits)
        path = f"/r/{sr_string}/search"
        params["restrict_sr"] = "on"
    else:
        path = "/search"

    data = api_get(path, params)
    if not data:
        return []

    posts = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        posts.append({
            "id": post.get("id", ""),
            "title": post.get("title", ""),
            "subreddit": post.get("subreddit", ""),
            "score": post.get("score", 0),
            "num_comments": post.get("num_comments", 0),
            "selftext_preview": (post.get("selftext", "") or "")[:500],
            "url": f"https://reddit.com{post.get('permalink', '')}",
            "created_utc": post.get("created_utc", 0),
        })

    return posts


def get_top_comments(post_id, subreddit, limit=10):
    """Get top-level comments for a post, sorted by best."""
    path = f"/r/{subreddit}/comments/{post_id}"
    params = {"sort": "best", "limit": limit, "depth": 1}

    data = api_get(path, params)
    if not data or len(data) < 2:
        return []

    comments = []
    for child in data[1].get("data", {}).get("children", []):
        if child.get("kind") != "t1":
            continue
        c = child.get("data", {})
        if c.get("score", 0) < 3:  # skip low-score comments
            continue
        comments.append({
            "body": (c.get("body", "") or "")[:500],
            "score": c.get("score", 0),
        })

    return sorted(comments, key=lambda x: x["score"], reverse=True)[:limit]


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print(json.dumps({
            "error": "REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET required",
            "posts": [],
        }))
        sys.exit(1)

    # Read input
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            config = json.load(f)
    else:
        config = json.load(sys.stdin)

    queries = config.get("queries", [])
    subreddits = config.get("subreddits", None)
    max_posts = config.get("max_posts_per_query", 25)
    fetch_comments_for_top = config.get("fetch_comments_for_top", 5)

    if not queries:
        print(json.dumps({"error": "No queries provided", "posts": []}))
        sys.exit(1)

    print(f"Searching {len(queries)} queries across {subreddits or 'all of Reddit'}...", file=sys.stderr)

    all_posts = {}  # dedup by post ID

    for query in queries:
        print(f"  Searching: {query}", file=sys.stderr)

        # Search by relevance
        posts = search_posts(query, subreddits, sort="relevance", limit=max_posts)
        for p in posts:
            p["query"] = query
            if p["id"] not in all_posts or p["score"] > all_posts[p["id"]]["score"]:
                all_posts[p["id"]] = p

        # Also search by hot for trending signal
        hot_posts = search_posts(query, subreddits, sort="hot", limit=max_posts)
        for p in hot_posts:
            p["query"] = query
            if p["id"] not in all_posts or p["score"] > all_posts[p["id"]]["score"]:
                all_posts[p["id"]] = p

        time.sleep(0.5)  # be polite

    # Sort by score and fetch comments for top N
    posts_list = sorted(all_posts.values(), key=lambda x: x["score"], reverse=True)

    print(f"Found {len(posts_list)} unique posts. Fetching comments for top {fetch_comments_for_top}...", file=sys.stderr)

    for post in posts_list[:fetch_comments_for_top]:
        post["top_comments"] = get_top_comments(post["id"], post["subreddit"])
        time.sleep(0.3)

    print(f"Done. {len(posts_list)} posts collected.", file=sys.stderr)

    output = {
        "posts": posts_list,
        "total_posts": len(posts_list),
        "queries_run": len(queries),
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
