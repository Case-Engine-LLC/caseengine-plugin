#!/usr/bin/env python3
"""
What: Fetches YouTube video metrics and titles for topic queries
Input: JSON with {"queries": ["topic 1", ...], "max_results": 10}
       via stdin or file argument
Output: JSON with video metrics to stdout
Re-run: Safe — stateless, no side effects
Env: YOUTUBE_API_KEY required
"""

import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta

API_KEY = os.environ.get("YOUTUBE_API_KEY", "")
BASE_URL = "https://www.googleapis.com/youtube/v3"
quota_used = 0


def api_get(endpoint, params):
    """Make a GET request to the YouTube Data API."""
    global quota_used
    params["key"] = API_KEY
    url = f"{BASE_URL}/{endpoint}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"YouTube API error {e.code}: {body}", file=sys.stderr)
        return None


def search_videos(query, max_results=10):
    """Search for videos by query. Costs 100 quota units per call."""
    global quota_used
    one_year_ago = (datetime.utcnow() - timedelta(days=365)).strftime("%Y-%m-%dT00:00:00Z")
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "order": "relevance",
        "maxResults": max_results,
        "publishedAfter": one_year_ago,
        "relevanceLanguage": "en",
    }
    quota_used += 100
    data = api_get("search", params)
    if not data:
        return []
    return [item["id"]["videoId"] for item in data.get("items", [])]


def get_video_details(video_ids):
    """Get statistics and snippet for videos. Costs 1 unit per call (up to 50 IDs)."""
    global quota_used
    results = []
    # Batch in groups of 50
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        quota_used += 1
        params = {
            "part": "snippet,statistics,contentDetails",
            "id": ",".join(batch),
        }
        data = api_get("videos", params)
        if not data:
            continue
        for item in data.get("items", []):
            stats = item.get("statistics", {})
            snippet = item.get("snippet", {})
            content = item.get("contentDetails", {})
            results.append({
                "videoId": item["id"],
                "title": snippet.get("title", ""),
                "channelTitle": snippet.get("channelTitle", ""),
                "publishedAt": snippet.get("publishedAt", ""),
                "description": snippet.get("description", "")[:500],
                "viewCount": int(stats.get("viewCount", 0)),
                "likeCount": int(stats.get("likeCount", 0)),
                "commentCount": int(stats.get("commentCount", 0)),
                "duration": content.get("duration", ""),
            })
    return results


def main():
    if not API_KEY:
        print(json.dumps({"error": "YOUTUBE_API_KEY not set", "videos": [], "quota_used": 0}))
        sys.exit(1)

    # Read input
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            config = json.load(f)
    else:
        config = json.load(sys.stdin)

    queries = config.get("queries", [])
    max_results = config.get("max_results", 10)

    if not queries:
        print(json.dumps({"error": "No queries provided", "videos": [], "quota_used": 0}))
        sys.exit(1)

    print(f"Searching {len(queries)} queries, max {max_results} results each...", file=sys.stderr)

    # Collect all video IDs from searches
    all_video_ids = []
    query_map = {}  # videoId -> query that found it

    for query in queries:
        print(f"  Searching: {query}", file=sys.stderr)
        video_ids = search_videos(query, max_results)
        for vid in video_ids:
            if vid not in query_map:
                query_map[vid] = query
                all_video_ids.append(vid)

    print(f"Found {len(all_video_ids)} unique videos. Fetching details...", file=sys.stderr)

    # Get details for all videos
    videos = get_video_details(all_video_ids)

    # Add the query that found each video
    for v in videos:
        v["query"] = query_map.get(v["videoId"], "")

    # Sort by view count descending
    videos.sort(key=lambda x: x["viewCount"], reverse=True)

    print(f"Quota used: {quota_used} units", file=sys.stderr)

    output = {
        "videos": videos,
        "total_videos": len(videos),
        "queries_run": len(queries),
        "quota_used": quota_used,
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
