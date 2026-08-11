"""Tests for scripts/llms_txt/check_links.py"""

import urllib.error
from unittest.mock import MagicMock, patch

import pytest

import check_links


def _mock_response(status: int):
    resp = MagicMock()
    resp.status = status
    resp.__enter__ = lambda s: s
    resp.__exit__ = MagicMock(return_value=False)
    return resp


# ── extract_urls() ────────────────────────────────────────────────────────────

class TestExtractUrls:
    def test_finds_https_urls(self):
        urls = check_links.extract_urls("see https://example.com for details")
        assert urls == ["https://example.com"]

    def test_finds_http_urls(self):
        urls = check_links.extract_urls("http://example.com")
        assert urls == ["http://example.com"]

    def test_deduplicates_preserving_order(self):
        content = "https://a.com https://b.com https://a.com"
        assert check_links.extract_urls(content) == ["https://a.com", "https://b.com"]

    def test_returns_empty_for_no_urls(self):
        assert check_links.extract_urls("no links here") == []

    def test_handles_markdown_link_syntax(self):
        urls = check_links.extract_urls("[Title](https://example.com): desc")
        assert "https://example.com" in urls

    def test_multiple_urls_on_same_line(self):
        content = "https://a.com https://b.com https://c.com"
        assert check_links.extract_urls(content) == ["https://a.com", "https://b.com", "https://c.com"]


# ── check_url() ───────────────────────────────────────────────────────────────

class TestCheckUrl:
    def test_200_returns_status_no_error(self):
        with patch("urllib.request.urlopen", return_value=_mock_response(200)):
            url, status, error = check_links.check_url("https://example.com")
        assert url == "https://example.com"
        assert status == 200
        assert error is None

    def test_404_returns_status_no_error(self):
        exc = urllib.error.HTTPError("https://example.com", 404, "Not Found", {}, None)
        with patch("urllib.request.urlopen", side_effect=exc):
            url, status, error = check_links.check_url("https://example.com")
        assert status == 404
        assert error is None

    def test_429_returns_status_no_error(self):
        exc = urllib.error.HTTPError("https://example.com", 429, "Too Many Requests", {}, None)
        with patch("urllib.request.urlopen", side_effect=exc):
            url, status, error = check_links.check_url("https://example.com")
        assert status == 429
        assert error is None

    def test_network_error_returns_none_status_and_error_string(self):
        with patch("urllib.request.urlopen", side_effect=Exception("Connection refused")):
            url, status, error = check_links.check_url("https://example.com")
        assert status is None
        assert "Connection refused" in error

    def test_returns_url_unchanged(self):
        with patch("urllib.request.urlopen", return_value=_mock_response(200)):
            url, _, _ = check_links.check_url("https://example.com/path")
        assert url == "https://example.com/path"


# ── main() ────────────────────────────────────────────────────────────────────

class TestMain:
    def test_returns_0_when_all_urls_ok(self, tmp_path):
        (tmp_path / "llms.txt").write_text("- [Page](https://example.com): desc\n")
        with patch("check_links.find_repo_root", return_value=tmp_path), \
             patch("urllib.request.urlopen", return_value=_mock_response(200)):
            assert check_links.main() == 0

    def test_returns_1_on_404(self, tmp_path):
        (tmp_path / "llms.txt").write_text("- [Page](https://example.com): desc\n")
        exc = urllib.error.HTTPError("https://example.com", 404, "Not Found", {}, None)
        with patch("check_links.find_repo_root", return_value=tmp_path), \
             patch("urllib.request.urlopen", side_effect=exc):
            assert check_links.main() == 1

    def test_429_does_not_cause_failure(self, tmp_path):
        (tmp_path / "llms.txt").write_text("- [Page](https://example.com): desc\n")
        exc = urllib.error.HTTPError("https://example.com", 429, "Too Many Requests", {}, None)
        with patch("check_links.find_repo_root", return_value=tmp_path), \
             patch("urllib.request.urlopen", side_effect=exc):
            assert check_links.main() == 0

    def test_network_error_causes_failure(self, tmp_path):
        (tmp_path / "llms.txt").write_text("- [Page](https://example.com): desc\n")
        with patch("check_links.find_repo_root", return_value=tmp_path), \
             patch("urllib.request.urlopen", side_effect=Exception("timeout")):
            assert check_links.main() == 1

    def test_duplicate_urls_checked_only_once(self, tmp_path):
        (tmp_path / "llms.txt").write_text(
            "https://example.com\nhttps://example.com\n"
        )
        with patch("check_links.find_repo_root", return_value=tmp_path), \
             patch("urllib.request.urlopen", return_value=_mock_response(200)) as mock_open:
            check_links.main()
        assert mock_open.call_count == 1

    def test_returns_0_for_empty_file(self, tmp_path):
        (tmp_path / "llms.txt").write_text("no urls here\n")
        with patch("check_links.find_repo_root", return_value=tmp_path):
            assert check_links.main() == 0
