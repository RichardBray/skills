import sys, os, json, tempfile
from unittest.mock import patch
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))


def test_trending_score_reads_from_json():
    from score import trending_score, _load_trends
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
            _load_trends.cache_clear()
            score = trending_score("this changes everything about coding")
            assert score >= 75
    finally:
        os.unlink(tmp_path)
        _load_trends.cache_clear()


def test_trending_score_fallback_when_no_file():
    from score import trending_score, _load_trends
    with patch("score.TRENDS_PATH", "/nonexistent/path.json"):
        _load_trends.cache_clear()
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
            assert score > 50
    finally:
        os.unlink(tmp_path)
        _load_trends.cache_clear()
