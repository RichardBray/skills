import sys, os, json
from unittest.mock import patch, MagicMock
from io import BytesIO
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from fetch_trends import fetch_trending_titles, build_trends


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
