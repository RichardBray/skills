import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from fetch_trends import extract_ngrams, extract_topics


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
    assert "The" not in topics


def test_extract_topics_empty_input():
    assert extract_topics([], min_count=2) == []
