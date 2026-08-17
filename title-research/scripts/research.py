#!/usr/bin/env python3
"""Research top-performing YouTube titles for a topic using the Firecrawl CLI.

Strategy:
1. Scrape YouTube search results for the query (optionally filtered by view count).
2. Interact with the rendered page to extract title | channel | views.
3. Fall back to `firecrawl search site:youtube.com ...` if interact fails
   (YouTube scrapes often die with "Job not found" / 401 consent pages).

Usage:
  python3 research.py "web scraping AI" [--sort views] [--limit 20]
  python3 research.py "convex tutorial" --dump raw

Output: one line per video -> "title | channel | views"
"""
import argparse
import re
import subprocess
import sys

SORT_FILTERS = {
    # YouTube `sp` params: sort by view count + this week/month, etc.
    "views": "CAMSAhAB",        # sort by view count
    "views_week": "CAMSBAgCEAE%3D",
    "relevance": "",
}


def run(cmd: list[str], timeout: int = 120) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return ""


def scrape_youtube(query: str, sort: str) -> str:
    from urllib.parse import quote_plus
    sp = SORT_FILTERS.get(sort, "")
    url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
    if sp:
        url += f"&sp={sp}"
    out = run(["firecrawl", "scrape", url], timeout=90)
    m = re.search(r"Scrape ID: ([0-9a-f-]+)", out)
    return m.group(1) if m else ""


def interact_extract(scrape_id: str) -> str:
    prompt = (
        "Extract all video titles visible on this page with channel names and "
        "view counts. List them one per line as: title | channel | views"
    )
    return run(
        ["firecrawl", "interact", "--scrape-id", scrape_id,
         "--prompt", prompt, "--timeout", "120"],
        timeout=150,
    )


def search_fallback(query: str, limit: int) -> str:
    return run(
        ["firecrawl", "search", f"site:youtube.com {query}",
         "--limit", str(limit)],
        timeout=90,
    )


def parse_lines(text: str) -> list[str]:
    """Pull 'title | channel | views' rows from interact output."""
    rows = []
    for line in text.splitlines():
        line = line.strip().lstrip("*-• ").strip()
        # interact format: **Title** | Channel | 12K views  /  Title | Channel | views
        m = re.match(r"^\**(.+?)\**\s*\|\s*(.+?)\s*\|\s*([\d.,KMB]+\s*views?)", line)
        if m:
            title = re.sub(r"\*+", "", m.group(1)).strip()
            rows.append(f"{title} | {m.group(2).strip()} | {m.group(3).strip()}")
            continue
    return rows


def parse_search_headings(text: str) -> list[str]:
    """From `firecrawl search` output grab result titles (first line of each block)."""
    titles = []
    for block in text.split("\n\n"):
        first = block.strip().splitlines()[0] if block.strip() else ""
        first = first.strip()
        if first and not first.startswith(("http", "URL:", "Scrape")):
            clean = re.sub(r"^[\d.\-*\s]+", "", first).strip()
            if 10 < len(clean) < 120:
                titles.append(clean)
    return titles


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--sort", default="views", choices=SORT_FILTERS.keys())
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--dump", action="store_true", help="print raw output")
    args = ap.parse_args()

    scrape_id = scrape_youtube(args.query, args.sort)
    rows: list[str] = []
    if scrape_id:
        out = interact_extract(scrape_id)
        if args.dump:
            print(out, file=sys.stderr)
        rows = parse_lines(out)

    if not rows:
        # interact failed; stop the session then fall back to search
        run(["firecrawl", "interact", "stop"], timeout=30)
        out = search_fallback(args.query, args.limit)
        if args.dump:
            print(out, file=sys.stderr)
        for t in parse_search_headings(out):
            rows.append(f"{t} | (unknown channel) | (unknown views)")

    if not rows:
        print("No titles extracted. Run with --dump to inspect raw output.",
              file=sys.stderr)
        sys.exit(1)

    for r in rows[: args.limit * 2]:
        print(r)


if __name__ == "__main__":
    main()
