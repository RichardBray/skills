import sys, os, json, tempfile, shutil
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))


def test_end_to_end_trending_pipeline():
    """Mock the YouTube API, run the pipeline, and verify the scorer uses the output."""
    from fetch_trends import build_trends
    from score import score_title, _load_trends

    fake_titles = [
        "Claude Code Changes Everything About Development",
        "Why Claude Code Changes Everything Now",
        "Claude Code Changes Everything for Engineers",
        "How Claude Code Is Taking Over Programming",
        "Claude Code vs GitHub Copilot: The Real Winner",
    ]

    with patch("fetch_trends.fetch_trending_titles", return_value=fake_titles):
        trends = build_trends("fake-key")

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
