"""Tests for upload_and_extract.py"""

import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

import upload_and_extract


def make_mock_response(data: dict):
    """Return a mock that behaves like urllib.request.urlopen's context manager result."""
    mock = MagicMock()
    mock.read.return_value = json.dumps(data).encode()
    mock.__enter__ = lambda s: s
    mock.__exit__ = MagicMock(return_value=False)
    return mock


@pytest.fixture
def api_key_env(monkeypatch):
    monkeypatch.setenv("SENSIBLE_API_KEY", "test_key_abc123")


@pytest.fixture
def dummy_pdf(tmp_path):
    p = tmp_path / "sample.pdf"
    p.write_bytes(b"%PDF-1.4 fake pdf content")
    return p


class TestExtractDocument:
    def test_returns_full_response(self, api_key_env, dummy_pdf):
        response_data = {
            "parsed_document": {"departure": {"type": "date", "value": "2024-01-15T00:00:00.000Z"}},
            "configuration": "oocl_post",
        }
        mock_resp = make_mock_response(response_data)
        with patch("upload_and_extract.urllib.request.urlopen", return_value=mock_resp):
            result = upload_and_extract.extract_document("oocl_delivery_orders", "oocl_post", dummy_pdf)
        assert result == response_data

    def test_posts_to_correct_url(self, api_key_env, dummy_pdf):
        mock_resp = make_mock_response({"parsed_document": {}})
        with patch("upload_and_extract.urllib.request.urlopen", return_value=mock_resp) as mock_open:
            upload_and_extract.extract_document("my_doc_type", "my_config", dummy_pdf)
        req = mock_open.call_args[0][0]
        assert "my_doc_type" in req.full_url
        assert "my_config" in req.full_url
        assert req.method == "POST"

    def test_sends_pdf_binary(self, api_key_env, dummy_pdf):
        mock_resp = make_mock_response({"parsed_document": {}})
        with patch("upload_and_extract.urllib.request.urlopen", return_value=mock_resp) as mock_open:
            upload_and_extract.extract_document("doc", "cfg", dummy_pdf)
        req = mock_open.call_args[0][0]
        assert req.data == dummy_pdf.read_bytes()

    def test_exits_on_http_error(self, api_key_env, dummy_pdf):
        import urllib.error
        http_err = urllib.error.HTTPError(
            url="https://api.sensible.so/v0/extract/doc",
            code=401,
            msg="Unauthorized",
            hdrs={},
            fp=MagicMock(read=lambda: b"Unauthorized"),
        )
        with patch("upload_and_extract.urllib.request.urlopen", side_effect=http_err):
            with pytest.raises(SystemExit):
                upload_and_extract.extract_document("doc", "cfg", dummy_pdf)

    def test_includes_bearer_token(self, api_key_env, dummy_pdf):
        mock_resp = make_mock_response({"parsed_document": {}})
        with patch("upload_and_extract.urllib.request.urlopen", return_value=mock_resp) as mock_open:
            upload_and_extract.extract_document("doc", "cfg", dummy_pdf)
        req = mock_open.call_args[0][0]
        assert req.get_header("Authorization") == "Bearer test_key_abc123"


class TestParsedDocumentExtraction:
    def test_extracts_parsed_document_from_response(self, api_key_env, dummy_pdf, tmp_path):
        """main() should save only parsed_document, not the full response envelope."""
        config = tmp_path / "config.json"
        config.write_text('{"fields": []}')
        output = tmp_path / "output.json"

        full_response = {
            "parsed_document": {"vessel": {"type": "string", "value": "MSC AURORA"}},
            "configuration": "oocl_post",
            "status": "SUCCEEDED",
        }

        def fake_urlopen(req):
            url = req.full_url if hasattr(req, "full_url") else str(req)
            if "extract" in url:
                return make_mock_response(full_response)
            # For other API calls (doc type list, config create, golden), return minimal valid responses
            if req.method == "GET":
                return make_mock_response([])
            return make_mock_response({"id": "fake-id", "name": "fake"})

        with patch("upload_and_extract.urllib.request.urlopen", side_effect=fake_urlopen):
            with patch("upload_pr_extractor.urllib.request.urlopen", side_effect=fake_urlopen):
                upload_and_extract.main.__globals__  # ensure imported
                import sys as _sys
                _sys.argv = [
                    "upload_and_extract.py",
                    "--doc-type", "oocl_delivery_orders",
                    "--config", str(config),
                    "--pdf", str(dummy_pdf),
                    "--config-name", "oocl_post",
                    "--output", str(output),
                ]
                upload_and_extract.main()

        saved = json.loads(output.read_text())
        assert saved == full_response["parsed_document"]
        assert "configuration" not in saved


@pytest.mark.integration
class TestIntegration:
    """Live API tests — only run with: pytest -m integration"""

    def test_real_extraction_returns_parsed_document(self):
        import os
        if not os.environ.get("SENSIBLE_API_KEY"):
            pytest.skip("SENSIBLE_API_KEY not set")
        # Placeholder: wire up a real fixture PDF and config to run end-to-end
        pytest.skip("No fixture PDF registered for integration test yet")
