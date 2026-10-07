#!/usr/bin/env python3
"""Real YouTube Shorts titles with view counts, for title research.

usage: shorts_titles.py "query one" "query two" ...

Scrapes YouTube search filtered to Shorts (sp=EgIQCQ) via the firecrawl CLI and
prints `views | title`, highest first. The general title-research skill searches
long-form results, which is the wrong pattern pool for a Short.
"""
import re, subprocess, sys
from urllib.parse import quote_plus


def views(text):
    m = re.match(r"([\d.]+)\s*([KMB]?)\s+views", text.strip())
    if not m:
        return 0
    return int(float(m.group(1)) * {"": 1, "K": 1e3, "M": 1e6, "B": 1e9}[m.group(2)])


seen, rows = set(), []
for q in sys.argv[1:]:
    url = f"https://www.youtube.com/results?search_query={quote_plus(q + ' #shorts')}&sp=EgIQCQ%253D%253D"
    md = subprocess.run(["firecrawl", "scrape", url, "--format", "markdown"], capture_output=True, text=True, timeout=180).stdout
    title = None
    for line in md.splitlines():
        t = re.match(r"^### \[(.+?)\]\(https://www\.youtube\.com/shorts/", line)
        if t:
            title = t.group(1).replace("\\#", "#").replace("\\", "")
            continue
        if title and re.search(r"\bviews$", line.strip()):
            if title not in seen:
                seen.add(title)
                rows.append((views(line), line.strip(), title, q))
            title = None

if not rows:
    sys.exit("no Shorts parsed: YouTube may have served a consent page; fall back to `firecrawl search 'site:youtube.com/shorts <q>'` (no view counts)")
for v, raw, title, q in sorted(rows, reverse=True)[:30]:
    print(f"{raw:>12} | {title}   [{q}]")
