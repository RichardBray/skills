# YouTube Trending Data for Title Scorer — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the static `TRENDING_PHRASES` list in `score.py` with dynamically-fetched YouTube trending data, so the scorer reflects what's actually working on YouTube right now.

**Architecture:** A new `scripts/fetch_trends.py` script calls the YouTube Data API to pull trending video titles, extracts frequent 2-gram/3-gram phrases and recurring topics, and writes them to `data/trends.json`. The existing `score.py` reads this file at scoring time, falling back to the static list if it's missing or stale (>14 days old).

**Tech Stack:** Python 3 (stdlib only: `urllib`, `json`, `re`, `collections`). YouTube Data API v3 (free tier, API key auth).

---

## File Structure

| File | Action | Responsibility |
|---|---|---|
| `scripts/fetch_trends.py` | Create | Fetch YouTube trending titles, extract phrases + topics, write JSON |
| `scripts/score.py` | Modify | Read `data/trends.json` in `trending_score()`, fallback to static list |
| `data/trends.json` | Generated | Weekly snapshot of trending phrases and topics (gitignored) |
| `.gitignore` | Create | Ignore `data/trends.json` |
| `SKILL.md` | Modify | Document the `fetch_trends.py` script and `YOUTUBE_API_KEY` setup |
| `tests/test_fetch_trends.py` | Create | Unit tests for phrase/topic extraction logic |
| `tests/test_trending_score.py` | Create | Unit tests for the updated `trending_score()` function |

---

### Task 1: Create `.gitignore` and `data/` directory

**Files:**
- Create: `.gitignore`
- Create: `data/.gitkeep`

- [ ] **Step 1: Create `.gitignore`**

```
data/trends.json
```

- [ ] **Step 2: Create `data/.gitkeep` so the directory is tracked**

```bash
mkdir -p data
touch data/.gitkeep
```

- [ ] **Step 3: Commit**

```bash
git add .gitignore data/.gitkeep
git commit -m "chore: add .gitignore and data directory for trending data"
```

---

### Task 2: Build phrase/topic extraction functions

These are the pure-logic functions that `fetch_trends.py` will use. Build and test them before adding any API code.

**Files:**
- Create: `scripts/fetch_trends.py` (extraction functions only)
- Create: `tests/test_fetch_trends.py`

- [ ] **Step 1: Write failing test for `extract_ngrams`**

`extract_ngrams` takes a list of title strings and returns a list of `{"phrase": str, "count": int}` dicts, sorted by count descending, filtered to count >= `min_count`.

```python
# tests/test_fetch_trends.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from fetch_trends import extract_ngrams

def test_extract_ngrams_basic():
    titles = [
        "This Changes Everything About Python",
        "React Changes Everything We Know",
        "Why This Changes Everything in 2026",
        "Unrelated Title Here",
    ]
    result = extract_ngrams(titles, min_count=2)
    phrases = [r["phrase"] for r in result]
    assert "changes everything" in phrases
    # "unrelated title here" appears only once, should be excluded
    assert all("unrelated" not in p for p in phrases)

def test_extract_ngrams_returns_counts():
    titles = [
        "Nobody Expected This Result",
        "Nobody Expected That Outcome",
        "Nobody Expected The Change",
    ]
    result = extract_ngrams(titles, min_count=2)
    match = [r for r in result if r["phrase"] == "nobody expected"]
    assert len(match) == 1
    assert match[0]["count"] == 3

def test_extract_ngrams_empty_input():
    assert extract_ngrams([], min_count=2) == []
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/robray/skills/title-score
python3 -m pytest tests/test_fetch_trends.py -v
```

Expected: `ModuleNotFoundError` or `ImportError` — `fetch_trends` doesn't exist yet.

- [ ] **Step 3: Implement `extract_ngrams` in `scripts/fetch_trends.py`**

```python
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

STOPWORDS = {
    "a","an","the","of","in","on","at","to","for","with","and","or","but",
    "is","are","was","were","be","been","being","it","its","as","by","from",
    "that","this","these","those","i","you","he","she","we","they","my","your",
    "his","her","our","their","me","him","us","them","do","does","did","has",
    "have","had","will","would","could","should","can","may","might","so","if",
    "not","no","just","also","very","too","about","up","out","how","what","why",
    "when","where","who","which","all","each","every","some","any","new",
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
                # skip grams that are all stopwords
                if all(w in STOPWORDS for w in gram):
                    continue
                counter[" ".join(gram)] += 1
    return [
        {"phrase": phrase, "count": count}
        for phrase, count in counter.most_common()
        if count >= min_count
    ]
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python3 -m pytest tests/test_fetch_trends.py -v
```

Expected: all 3 tests PASS.

- [ ] **Step 5: Write failing test for `extract_topics`**

`extract_topics` finds proper-noun-like terms (capitalized words that aren't sentence starters) appearing across multiple titles.

```python
# append to tests/test_fetch_trends.py
from fetch_trends import extract_topics

def test_extract_topics_finds_proper_nouns():
    titles = [
        "Why Claude Is Better Than You Think",
        "Claude Just Changed Everything",
        "Building Apps With Claude and React",
        "Some Random Title About Coding",
    ]
    result = extract_topics(titles, min_count=2)
    topics = [r["topic"] for r in result]
    assert "Claude" in topics

def test_extract_topics_skips_common_words():
    titles = [
        "The Best Way to Learn",
        "The Best Tool for Developers",
        "The Best Framework in 2026",
    ]
    result = extract_topics(titles, min_count=2)
    topics = [r["topic"] for r in result]
    # "The" and "Best" are common — "The" is a stopword, "Best" is too generic
    assert "The" not in topics

def test_extract_topics_empty_input():
    assert extract_topics([], min_count=2) == []
```

- [ ] **Step 6: Run test to verify it fails**

```bash
python3 -m pytest tests/test_fetch_trends.py::test_extract_topics_finds_proper_nouns -v
```

Expected: `ImportError` — `extract_topics` not defined yet.

- [ ] **Step 7: Implement `extract_topics`**

Add to `scripts/fetch_trends.py`:

```python
# Words that are capitalized in titles but aren't meaningful topics
GENERIC_CAPS = {
    "best", "worst", "top", "new", "free", "easy", "simple", "quick",
    "fast", "big", "small", "great", "good", "bad", "real", "full",
    "old", "first", "last", "next", "only", "every", "many", "most",
    "much", "way", "day", "time", "thing", "things", "people", "world",
}


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
```

- [ ] **Step 8: Run all tests to verify they pass**

```bash
python3 -m pytest tests/test_fetch_trends.py -v
```

Expected: all 6 tests PASS.

- [ ] **Step 9: Commit**

```bash
git add scripts/fetch_trends.py tests/test_fetch_trends.py
git commit -m "feat(trending): add phrase and topic extraction functions with tests"
```

---

### Task 3: Add YouTube Data API fetching

**Files:**
- Modify: `scripts/fetch_trends.py`
- Create: `tests/test_fetch_api.py`

- [ ] **Step 1: Write failing test for `fetch_trending_titles`**

This function calls the YouTube API. For testing, we mock `urllib.request.urlopen`.

```python
# tests/test_fetch_api.py
import sys, os, json
from unittest.mock import patch, MagicMock
from io import BytesIO
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from fetch_trends import fetch_trending_titles

def _mock_api_response(titles):
    """Build a fake YouTube API JSON response."""
    items = [{"snippet": {"title": t}} for t in titles]
    body = json.dumps({"items": items}).encode()
    mock_resp = MagicMock()
    mock_resp.read.return_value = body
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp

@patch("fetch_trends.urlopen")
def test_fetch_trending_titles_returns_titles(mock_urlopen):
    titles = ["Title One", "Title Two", "Title Three"]
    mock_urlopen.return_value = _mock_api_response(titles)
    result = fetch_trending_titles("fake-api-key", max_results=3, category_id=None, search_query=None)
    assert result == titles
    assert mock_urlopen.called

@patch("fetch_trends.urlopen")
def test_fetch_trending_titles_with_search_query(mock_urlopen):
    titles = ["Python Tutorial", "Python Crash Course"]
    mock_urlopen.return_value = _mock_api_response(titles)
    result = fetch_trending_titles("fake-key", max_results=2, category_id=None, search_query="python")
    assert result == titles
    call_url = mock_urlopen.call_args[0][0]
    assert "q=python" in call_url
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python3 -m pytest tests/test_fetch_api.py -v
```

Expected: `ImportError` — `fetch_trending_titles` not defined.

- [ ] **Step 3: Implement `fetch_trending_titles`**

Add to `scripts/fetch_trends.py`:

```python
from urllib.request import urlopen
from urllib.parse import urlencode

YT_API_BASE = "https://www.googleapis.com/youtube/v3"


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


def _recent_date() -> str:
    """ISO date string for 7 days ago (for search recency filter)."""
    from datetime import timedelta
    dt = datetime.now(timezone.utc) - timedelta(days=7)
    return dt.strftime("%Y-%m-%dT00:00:00Z")
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
python3 -m pytest tests/test_fetch_api.py -v
```

Expected: both tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch_trends.py tests/test_fetch_api.py
git commit -m "feat(trending): add YouTube Data API fetching function"
```

---

### Task 4: Build the main pipeline and JSON output

Wire the fetch + extraction functions together with a `main()` that writes `data/trends.json`.

**Files:**
- Modify: `scripts/fetch_trends.py`

- [ ] **Step 1: Write failing test for `build_trends`**

`build_trends` orchestrates: fetch titles → extract ngrams + topics → return dict.

```python
# append to tests/test_fetch_api.py
from fetch_trends import build_trends

@patch("fetch_trends.fetch_trending_titles")
def test_build_trends_structure(mock_fetch):
    mock_fetch.return_value = [
        "Claude Changes Everything About AI",
        "Why Claude Changes Everything Now",
        "Claude Changes Everything for Developers",
    ]
    result = build_trends("fake-key")
    assert "updated_at" in result
    assert "phrases" in result
    assert "topics" in result
    assert isinstance(result["phrases"], list)
    assert isinstance(result["topics"], list)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python3 -m pytest tests/test_fetch_api.py::test_build_trends_structure -v
```

Expected: `ImportError` — `build_trends` not defined.

- [ ] **Step 3: Implement `build_trends` and `main`**

Add to `scripts/fetch_trends.py`:

```python
SEARCH_QUERIES = ["programming", "developer tools", "coding tutorial", "software engineering"]
TECH_CATEGORY_ID = "28"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_PATH = os.path.join(DATA_DIR, "trends.json")


def build_trends(api_key: str) -> dict:
    """Fetch trending titles and extract phrases + topics."""
    all_titles: list[str] = []

    # Trending videos (general)
    all_titles.extend(fetch_trending_titles(api_key, max_results=50))
    # Trending videos (tech category)
    all_titles.extend(fetch_trending_titles(api_key, max_results=50, category_id=TECH_CATEGORY_ID))
    # Search-based popular videos for tech keywords
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
```

- [ ] **Step 4: Run all tests**

```bash
python3 -m pytest tests/ -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch_trends.py tests/test_fetch_api.py
git commit -m "feat(trending): wire up full pipeline with JSON output"
```

---

### Task 5: Update `score.py` to read `data/trends.json`

**Files:**
- Modify: `scripts/score.py:44-49,184-188`
- Create: `tests/test_trending_score.py`

- [ ] **Step 1: Write failing test for dynamic trending score**

```python
# tests/test_trending_score.py
import sys, os, json, tempfile
from unittest.mock import patch
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

def test_trending_score_reads_from_json():
    from score import trending_score, _load_trends, TRENDS_PATH
    trends_data = {
        "updated_at": "2026-05-10T12:00:00+00:00",
        "phrases": [
            {"phrase": "changes everything", "count": 7},
            {"phrase": "nobody expected", "count": 4},
        ],
        "topics": [
            {"topic": "Claude", "count": 5},
        ],
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(trends_data, f)
        tmp_path = f.name
    try:
        with patch("score.TRENDS_PATH", tmp_path):
            # clear any cached data
            _load_trends.cache_clear()
            score = trending_score("this changes everything about coding")
            assert score >= 75  # should get phrase match boost
    finally:
        os.unlink(tmp_path)
        _load_trends.cache_clear()

def test_trending_score_fallback_when_no_file():
    from score import trending_score, _load_trends
    with patch("score.TRENDS_PATH", "/nonexistent/path.json"):
        _load_trends.cache_clear()
        # should fall back to static TRENDING_PHRASES
        score = trending_score("were not okay")
        assert score >= 75
        _load_trends.cache_clear()

def test_trending_score_topic_boost():
    from score import trending_score, _load_trends
    trends_data = {
        "updated_at": "2026-05-10T12:00:00+00:00",
        "phrases": [],
        "topics": [{"topic": "Claude", "count": 5}],
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(trends_data, f)
        tmp_path = f.name
    try:
        with patch("score.TRENDS_PATH", tmp_path):
            _load_trends.cache_clear()
            score = trending_score("why claude is taking over")
            assert score > 50  # topic match should boost above baseline
    finally:
        os.unlink(tmp_path)
        _load_trends.cache_clear()
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python3 -m pytest tests/test_trending_score.py -v
```

Expected: `ImportError` — `_load_trends` and `TRENDS_PATH` don't exist in `score.py` yet.

- [ ] **Step 3: Modify `score.py` to read trends dynamically**

Replace the `TRENDING_PHRASES` constant and `trending_score` function in `scripts/score.py`. Add these imports at the top (alongside existing ones):

```python
from functools import lru_cache
from datetime import datetime, timezone
```

Replace `TRENDING_PHRASES` (lines 45-50) with:

```python
FALLBACK_TRENDING_PHRASES = [
    "were not okay", "was not okay", "uncomfortable truth",
    "nobody expected", "changes everything", "changed everything",
    "is not what you think", "here's why", "and it worked",
    "the real reason", "what happened next", "i was wrong",
]

TRENDS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "trends.json")
TRENDS_MAX_AGE_DAYS = 14
```

Replace the `trending_score` function (lines 184-188) with:

```python
@lru_cache(maxsize=1)
def _load_trends() -> dict | None:
    """Load trends.json, returning None if missing or stale."""
    try:
        with open(TRENDS_PATH) as f:
            data = json.load(f)
        updated = datetime.fromisoformat(data["updated_at"])
        age_days = (datetime.now(timezone.utc) - updated).days
        if age_days > TRENDS_MAX_AGE_DAYS:
            print(f"Warning: trends.json is {age_days} days old, falling back to static list", file=sys.stderr)
            return None
        return data
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return None


def trending_score(title_lower: str) -> float:
    trends = _load_trends()

    if trends is None:
        # Fallback to static list
        hits = sum(1 for p in FALLBACK_TRENDING_PHRASES if p in title_lower)
        if hits == 0: return 45
        if hits == 1: return 75
        return 85

    # Dynamic phrase matching
    phrase_hits = 0
    for entry in trends.get("phrases", []):
        if entry["phrase"] in title_lower:
            if entry["count"] >= 7:
                phrase_hits += 2  # high-frequency phrase counts double
            else:
                phrase_hits += 1

    # Topic matching (case-insensitive)
    topic_hits = sum(
        1 for entry in trends.get("topics", [])
        if entry["topic"].lower() in title_lower
    )

    if phrase_hits == 0 and topic_hits == 0:
        return 45
    base = 45
    if phrase_hits >= 1:
        base = 75 + min(phrase_hits - 1, 2) * 5  # 75-85
    if topic_hits >= 1:
        base += 10
    return min(95, base)
```

- [ ] **Step 4: Run all tests**

```bash
python3 -m pytest tests/ -v
```

Expected: all tests PASS (new trending tests + existing extraction tests).

- [ ] **Step 5: Smoke test with the scorer**

```bash
python3 scripts/score.py "This Changes Everything About Programming"
```

Expected: outputs a score with `trending=45` (no `trends.json` exists yet, falls back to static list).

- [ ] **Step 6: Commit**

```bash
git add scripts/score.py tests/test_trending_score.py
git commit -m "feat(trending): read dynamic trends.json with fallback to static list"
```

---

### Task 6: Update `SKILL.md` documentation

**Files:**
- Modify: `SKILL.md`

- [ ] **Step 1: Add fetch_trends documentation to SKILL.md**

Add a new section after the "How to score" section:

```markdown
## Refreshing trending data

The scorer uses a `data/trends.json` file for up-to-date YouTube trending phrases and topics. To refresh it:

1. Get a YouTube Data API key from [Google Cloud Console](https://console.cloud.google.com/) (enable YouTube Data API v3).
2. Run:

\```bash
YOUTUBE_API_KEY=your-key-here scripts/fetch_trends.py
\```

This fetches ~150 trending video titles, extracts recurring phrases and topics, and writes `data/trends.json`. The scorer reads this file automatically.

If `data/trends.json` is missing or older than 14 days, the scorer falls back to a built-in static phrase list. Refresh weekly for best results.
```

Update the "Factors" table to clarify the trending row:

```markdown
| trending | `trending_score` | hits in `data/trends.json` phrases/topics (dynamic) or `FALLBACK_TRENDING_PHRASES` (static) |
```

- [ ] **Step 2: Commit**

```bash
git add SKILL.md
git commit -m "docs: add trending data refresh instructions to SKILL.md"
```

---

### Task 7: End-to-end integration test

**Files:**
- Create: `tests/test_integration.py`

- [ ] **Step 1: Write integration test**

Tests the full flow: mock API → `build_trends` → write JSON → `score_title` reads it.

```python
# tests/test_integration.py
import sys, os, json, tempfile, shutil
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

def test_end_to_end_trending_pipeline():
    """Mock the YouTube API, run the pipeline, and verify the scorer uses the output."""
    from fetch_trends import build_trends
    from score import score_title, _load_trends

    # Mock fetch_trending_titles to return controlled data
    fake_titles = [
        "Claude Code Changes Everything About Development",
        "Why Claude Code Changes Everything Now",
        "Claude Code Changes Everything for Engineers",
        "How Claude Code Is Taking Over Programming",
        "Claude Code vs GitHub Copilot: The Real Winner",
    ]

    with patch("fetch_trends.fetch_trending_titles", return_value=fake_titles):
        trends = build_trends("fake-key")

    # Write to a temp file and point scorer at it
    tmp_dir = tempfile.mkdtemp()
    tmp_path = os.path.join(tmp_dir, "trends.json")
    try:
        with open(tmp_path, "w") as f:
            json.dump(trends, f)

        with patch("score.TRENDS_PATH", tmp_path):
            _load_trends.cache_clear()
            result = score_title("Claude Code Changes Everything for Teams")
            assert result["components"]["trending"] > 50
            _load_trends.cache_clear()
    finally:
        shutil.rmtree(tmp_dir)
```

- [ ] **Step 2: Run all tests**

```bash
python3 -m pytest tests/ -v
```

Expected: all tests PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/test_integration.py
git commit -m "test: add end-to-end integration test for trending pipeline"
```
