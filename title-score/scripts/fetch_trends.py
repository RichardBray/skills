#!/usr/bin/env python3
"""Fetch YouTube trending titles and extract trending phrases/topics.

Usage: YOUTUBE_API_KEY=... python3 scripts/fetch_trends.py
Writes: data/trends.json
"""
import json
import re
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from urllib.request import urlopen
from urllib.parse import urlencode

STOPWORDS = {
    "a","an","the","of","in","on","at","to","for","with","and","or","but",
    "is","are","was","were","be","been","being","it","its","as","by","from",
    "that","this","these","those","i","you","he","she","we","they","my","your",
    "his","her","our","their","me","him","us","them","do","does","did","has",
    "have","had","will","would","could","should","can","may","might","so","if",
    "not","no","just","also","very","too","about","up","out","how","what","why",
    "when","where","who","which","all","each","every","some","any","new",
}

GENERIC_CAPS = {
    "best", "worst", "top", "new", "free", "easy", "simple", "quick",
    "fast", "big", "small", "great", "good", "bad", "real", "full",
    "old", "first", "last", "next", "only", "every", "many", "most",
    "much", "way", "day", "time", "thing", "things", "people", "world",
}


def _tokenize(title: str) -> list[str]:
    """Lowercase and split into alpha-numeric tokens."""
    return [w.lower() for w in re.findall(r"[A-Za-z0-9']+", title)]


def extract_ngrams(titles: list[str], min_count: int = 3) -> list[dict]:
    """Extract 2-gram and 3-gram phrases from titles, filtered by frequency."""
    counter: Counter = Counter()
    for title in titles:
        tokens = _tokenize(title)
        for n in (2, 3):
            for i in range(len(tokens) - n + 1):
                gram = tokens[i:i + n]
                if all(w in STOPWORDS for w in gram):
                    continue
                counter[" ".join(gram)] += 1
    return [
        {"phrase": phrase, "count": count}
        for phrase, count in counter.most_common()
        if count >= min_count
    ]


def extract_topics(titles: list[str], min_count: int = 3) -> list[dict]:
    """Extract proper-noun-like terms that recur across titles."""
    counter: Counter = Counter()
    for title in titles:
        words = re.findall(r"[A-Za-z0-9']+", title)
        seen_in_title: set[str] = set()
        for i, word in enumerate(words):
            if not word[0].isupper():
                continue
            if word.lower() in STOPWORDS:
                continue
            if word.lower() in GENERIC_CAPS:
                continue
            if len(word) < 2:
                continue
            if word not in seen_in_title:
                counter[word] += 1
                seen_in_title.add(word)
    return [
        {"topic": topic, "count": count}
        for topic, count in counter.most_common()
        if count >= min_count
    ]


YT_API_BASE = "https://www.googleapis.com/youtube/v3"


def _recent_date() -> str:
    """ISO date string for 7 days ago (for search recency filter)."""
    from datetime import timedelta
    dt = datetime.now(timezone.utc) - timedelta(days=7)
    return dt.strftime("%Y-%m-%dT00:00:00Z")


def fetch_trending_titles(
    api_key: str,
    max_results: int = 50,
    category_id: str | None = None,
    search_query: str | None = None,
) -> list[str]:
    """Fetch video titles from YouTube Data API."""
    if search_query:
        params = {
            "part": "snippet",
            "type": "video",
            "order": "viewCount",
            "maxResults": max_results,
            "q": search_query,
            "publishedAfter": _recent_date(),
            "key": api_key,
        }
        url = f"{YT_API_BASE}/search?{urlencode(params)}"
    else:
        params = {
            "part": "snippet",
            "chart": "mostPopular",
            "maxResults": max_results,
            "regionCode": "US",
            "key": api_key,
        }
        if category_id:
            params["videoCategoryId"] = category_id
        url = f"{YT_API_BASE}/videos?{urlencode(params)}"

    with urlopen(url) as resp:
        data = json.loads(resp.read())
    return [item["snippet"]["title"] for item in data.get("items", [])]


SEARCH_QUERIES = ["programming", "developer tools", "coding tutorial", "software engineering"]
TECH_CATEGORY_ID = "28"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_PATH = os.path.join(DATA_DIR, "trends.json")


def build_trends(api_key: str) -> dict:
    """Fetch trending titles and extract phrases + topics."""
    all_titles: list[str] = []

    all_titles.extend(fetch_trending_titles(api_key, max_results=50))
    all_titles.extend(fetch_trending_titles(api_key, max_results=50, category_id=TECH_CATEGORY_ID))
    for query in SEARCH_QUERIES:
        all_titles.extend(fetch_trending_titles(api_key, max_results=25, search_query=query))

    return {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "phrases": extract_ngrams(all_titles, min_count=3),
        "topics": extract_topics(all_titles, min_count=3),
    }


def main():
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        print("Error: YOUTUBE_API_KEY environment variable is required", file=sys.stderr)
        sys.exit(1)

    print("Fetching trending YouTube data...")
    trends = build_trends(api_key)
    print(f"Found {len(trends['phrases'])} trending phrases, {len(trends['topics'])} trending topics")

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(trends, f, indent=2)
    print(f"Written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
