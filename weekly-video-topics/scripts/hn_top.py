#!/usr/bin/env python3
"""Top Hacker News stories from the last N days, optionally filtered by keywords.

Usage: hn_top.py [--days 7] [--min-points 150] [--query "AI agents"] [--limit 40]
Prints TSV: points, comments, date, title, story url, hn url.
"""
import argparse, json, time, urllib.parse, urllib.request

p = argparse.ArgumentParser()
p.add_argument("--days", type=int, default=7)
p.add_argument("--min-points", type=int, default=150)
p.add_argument("--query", action="append", default=[], help="repeatable; empty means all stories")
p.add_argument("--limit", type=int, default=40)
args = p.parse_args()

since = int(time.time()) - args.days * 86400
seen, hits = set(), []
for q in args.query or [""]:
    for page in range(5):
        params = {
            "tags": "story",
            "query": q,
            "numericFilters": f"created_at_i>{since},points>{args.min_points}",
            "hitsPerPage": 100,
            "page": page,
        }
        url = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(params)
        # Algolia returns an HTML error page to the default urllib agent.
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.load(urllib.request.urlopen(req, timeout=30))
        for h in data["hits"]:
            if h["objectID"] not in seen:
                seen.add(h["objectID"])
                hits.append(h)
        if page + 1 >= data.get("nbPages", 0):
            break

hits.sort(key=lambda h: -h["points"])
for h in hits[: args.limit]:
    print("\t".join([
        str(h["points"]), str(h["num_comments"]), h["created_at"][:10], h["title"],
        h.get("url") or "", f"https://news.ycombinator.com/item?id={h['objectID']}",
    ]))
