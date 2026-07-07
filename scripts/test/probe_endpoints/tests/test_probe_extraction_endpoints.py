"""Tests for probe_extraction_endpoints.py"""

import json
import sys
import time
import urllib.error
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, call

import probe_extraction_endpoints as probe


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_mock_response(data: dict, status: int = 200):
    """Simulate a successful urllib.request.urlopen context manager result."""
    mock = MagicMock()
    mock.status = status
    mock.read.return_value = json.dumps(data).encode()
    mock.__enter__ = lambda s: s
    mock.__exit__ = MagicMock(return_value=False)
    return mock


def make_http_error(data: dict, code: int):
    return urllib.error.HTTPError(
        url="https://api.sensible.so/v0/test",
        code=code,
        msg="Error",
        hdrs=MagicMock(),
        fp=MagicMock(read=lambda: json.dumps(data).encode()),
    )


# ── normalize() ───────────────────────────────────────────────────────────────

class TestNormalize:
    def test_replaces_volatile_keys(self):
        data = {"id": "abc-123", "status": "COMPLETE"}
        assert probe.normalize(data) == {"id": "<omitted>", "status": "COMPLETE"}

    def test_preserves_non_volatile_values(self):
        data = {"actor": "api_key: my key", "type": "w2s", "status": "COMPLETE"}
        assert probe.normalize(data) == data

    def test_recursive_in_nested_dict(self):
        data = {"outer": {"id": "x", "actor": "user@example.com"}}
        result = probe.normalize(data)
        assert result["outer"]["id"] == "<omitted>"
        assert result["outer"]["actor"] == "user@example.com"

    def test_recursive_in_list(self):
        data = {"extractions": [{"id": "a", "type": "w2s"}, {"id": "b", "type": "w2s"}]}
        result = probe.normalize(data)
        assert result["extractions"][0]["id"] == "<omitted>"
        assert result["extractions"][1]["id"] == "<omitted>"
        assert result["extractions"][0]["type"] == "w2s"

    def test_all_volatile_keys_omitted(self):
        data = {k: "some-value" for k in probe.VOLATILE_KEYS}
        result = probe.normalize(data)
        assert all(v == "<omitted>" for v in result.values())

    def test_non_dict_values_pass_through(self):
        assert probe.normalize("string") == "string"
        assert probe.normalize(42) == 42
        assert probe.normalize(True) is True
        assert probe.normalize(None) is None

    def test_empty_dict(self):
        assert probe.normalize({}) == {}

    def test_empty_list(self):
        assert probe.normalize([]) == []


# ── save_snapshot() / compare_snapshot() / write_diff_summary() ──────────────

class TestSnapshot:
    def test_save_snapshot_writes_normalized_json(self, tmp_path, monkeypatch):
        monkeypatch.setattr(probe, "SNAPSHOT_DIR", tmp_path / "snapshots")
        probe.save_snapshot("test_ep", {"id": "abc", "actor": "api_key: foo"})
        saved = json.loads((tmp_path / "snapshots" / "test_ep.json").read_text())
        assert saved["id"] == "<omitted>"
        assert saved["actor"] == "api_key: foo"

    def test_compare_snapshot_ok_when_matches(self, tmp_path, monkeypatch, capsys):
        snap_dir = tmp_path / "snapshots"
        snap_dir.mkdir()
        monkeypatch.setattr(probe, "SNAPSHOT_DIR", snap_dir)
        data = {"actor": "api_key: foo", "status": "COMPLETE"}
        (snap_dir / "test_ep.json").write_text(json.dumps(probe.normalize(data), indent=2))
        probe.compare_snapshot("test_ep", data)
        assert "OK" in capsys.readouterr().out

    def test_compare_snapshot_changed_when_new_field(self, tmp_path, monkeypatch, capsys):
        snap_dir = tmp_path / "snapshots"
        snap_dir.mkdir()
        monkeypatch.setattr(probe, "SNAPSHOT_DIR", snap_dir)
        monkeypatch.setattr(probe, "_diff_lines", [])
        old = {"status": "COMPLETE"}
        (snap_dir / "test_ep.json").write_text(json.dumps(old, indent=2))
        new = {"status": "COMPLETE", "actor": "api_key: foo"}
        probe.compare_snapshot("test_ep", new)
        out = capsys.readouterr().out
        assert "CHANGED" in out
        assert probe._diff_lines  # diff was accumulated

    def test_compare_snapshot_missing_snapshot(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setattr(probe, "SNAPSHOT_DIR", tmp_path / "snapshots")
        probe.compare_snapshot("nonexistent", {"status": "COMPLETE"})
        assert "NO SNAPSHOT" in capsys.readouterr().out

    def test_write_diff_summary_saves_file(self, tmp_path, monkeypatch):
        run_dir = tmp_path / "2026-01-01_extraction"
        monkeypatch.setattr(probe, "RUN_DIR", run_dir)
        monkeypatch.setattr(probe, "REPO_ROOT", tmp_path)
        monkeypatch.setattr(probe, "_diff_lines", ["line1\n", "line2\n"])
        probe.write_diff_summary()
        assert (run_dir / "diff.txt").read_text() == "line1\nline2\n"

    def test_write_diff_summary_silent_when_no_diffs(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setattr(probe, "_diff_lines", [])
        probe.write_diff_summary()
        assert capsys.readouterr().out == ""


# ── _request() ───────────────────────────────────────────────────────────────

class TestRequest:
    def test_includes_auth_header_by_default(self, monkeypatch):
        monkeypatch.setattr(probe, "API_KEY", "test-key")
        mock_resp = make_mock_response({"ok": True})
        with patch("probe_extraction_endpoints.urllib.request.urlopen", return_value=mock_resp) as m:
            probe._request("GET", "https://api.sensible.so/v0/test")
        req = m.call_args[0][0]
        assert req.get_header("Authorization") == "Bearer test-key"

    def test_omits_auth_header_when_auth_false(self, monkeypatch):
        monkeypatch.setattr(probe, "API_KEY", "test-key")
        mock_resp = make_mock_response({})
        with patch("probe_extraction_endpoints.urllib.request.urlopen", return_value=mock_resp) as m:
            probe._request("PUT", "https://s3.amazonaws.com/upload", body=b"bytes", auth=False)
        req = m.call_args[0][0]
        assert req.get_header("Authorization") is None

    def test_returns_status_and_parsed_json(self, monkeypatch):
        monkeypatch.setattr(probe, "API_KEY", "k")
        mock_resp = make_mock_response({"actor": "api_key: foo"}, status=200)
        with patch("probe_extraction_endpoints.urllib.request.urlopen", return_value=mock_resp):
            status, body = probe._request("GET", "https://api.sensible.so/v0/test")
        assert status == 200
        assert body == {"actor": "api_key: foo"}

    def test_handles_http_error(self, monkeypatch):
        monkeypatch.setattr(probe, "API_KEY", "k")
        err = make_http_error({"error": "unauthorized"}, 401)
        with patch("probe_extraction_endpoints.urllib.request.urlopen", side_effect=err):
            status, body = probe._request("GET", "https://api.sensible.so/v0/test")
        assert status == 401
        assert body == {"error": "unauthorized"}

    def test_json_body_sets_content_type(self, monkeypatch):
        monkeypatch.setattr(probe, "API_KEY", "k")
        mock_resp = make_mock_response({})
        with patch("probe_extraction_endpoints.urllib.request.urlopen", return_value=mock_resp) as m:
            probe._request("POST", "https://api.sensible.so/v0/test", body={"key": "val"})
        req = m.call_args[0][0]
        assert req.get_header("Content-type") == "application/json"

    def test_bytes_body_uses_provided_content_type(self, monkeypatch):
        monkeypatch.setattr(probe, "API_KEY", "k")
        mock_resp = make_mock_response({})
        with patch("probe_extraction_endpoints.urllib.request.urlopen", return_value=mock_resp) as m:
            probe._request("POST", "https://api.sensible.so/v0/test",
                           body=b"%PDF", content_type="application/pdf")
        req = m.call_args[0][0]
        assert req.get_header("Content-type") == "application/pdf"


# ── poll_until_done() ─────────────────────────────────────────────────────────

class TestPollUntilDone:
    def test_returns_immediately_on_complete(self, monkeypatch):
        monkeypatch.setattr(probe, "API_KEY", "k")
        body = {"status": "COMPLETE", "actor": "api_key: foo"}
        mock_resp = make_mock_response(body)
        with patch("probe_extraction_endpoints.urllib.request.urlopen", return_value=mock_resp):
            result = probe.poll_until_done("extraction-id-123")
        assert result == body

    def test_returns_on_failed_status(self, monkeypatch):
        monkeypatch.setattr(probe, "API_KEY", "k")
        body = {"status": "FAILED", "errors": []}
        mock_resp = make_mock_response(body)
        with patch("probe_extraction_endpoints.urllib.request.urlopen", return_value=mock_resp):
            result = probe.poll_until_done("extraction-id-123")
        assert result["status"] == "FAILED"

    def test_polls_multiple_times_before_complete(self, monkeypatch):
        monkeypatch.setattr(probe, "API_KEY", "k")
        monkeypatch.setattr(probe, "POLL_INTERVAL", 0)
        responses = [
            make_mock_response({"status": "WAITING"}),
            make_mock_response({"status": "PROCESSING"}),
            make_mock_response({"status": "COMPLETE", "actor": "user@example.com"}),
        ]
        with patch("probe_extraction_endpoints.urllib.request.urlopen", side_effect=responses):
            result = probe.poll_until_done("abc")
        assert result["status"] == "COMPLETE"

    def test_raises_timeout_error(self, monkeypatch):
        monkeypatch.setattr(probe, "API_KEY", "k")
        monkeypatch.setattr(probe, "POLL_INTERVAL", 0)
        monkeypatch.setattr(probe, "POLL_TIMEOUT", 0)
        mock_resp = make_mock_response({"status": "WAITING"})
        with patch("probe_extraction_endpoints.urllib.request.urlopen", return_value=mock_resp):
            with pytest.raises(TimeoutError):
                probe.poll_until_done("abc")


# ── save_raw() ────────────────────────────────────────────────────────────────

class TestSaveRaw:
    def test_saves_json_to_run_dir(self, tmp_path, monkeypatch):
        run_dir = tmp_path / "2026-01-01_extraction"
        monkeypatch.setattr(probe, "RUN_DIR", run_dir)
        probe.save_raw("extract_sync", {"actor": "api_key: foo", "id": "real-id"})
        saved = json.loads((run_dir / "extract_sync.json").read_text())
        assert saved["id"] == "real-id"   # raw — not normalized
        assert saved["actor"] == "api_key: foo"

    def test_creates_run_dir_if_missing(self, tmp_path, monkeypatch):
        run_dir = tmp_path / "new_run_dir"
        monkeypatch.setattr(probe, "RUN_DIR", run_dir)
        probe.save_raw("test", {})
        assert run_dir.exists()


# ── main() ────────────────────────────────────────────────────────────────────

class TestMain:
    def test_exits_without_api_key(self, monkeypatch):
        monkeypatch.delenv("SENSIBLE_API_KEY", raising=False)
        with pytest.raises(SystemExit):
            probe.main()

    def test_run_dir_contains_extraction_label(self, monkeypatch, tmp_path):
        """RUN_DIR name should include 'extraction' so runs from different scripts are identifiable."""
        monkeypatch.setenv("SENSIBLE_API_KEY", "test-key")
        monkeypatch.setattr(probe, "OUTPUT_DIR", tmp_path)

        complete_body = {"status": "COMPLETE", "actor": "api_key: foo", "parsed_document": {}}
        initial_body = {"id": "fake-id", "status": "WAITING", "upload_url": "https://s3.example.com/upload"}
        portfolio_initial = {"id": "fake-portfolio-id", "status": "WAITING", "upload_url": "https://s3.example.com/p"}
        list_body = {"extractions": []}

        def fake_urlopen(req):
            url = req.full_url if hasattr(req, "full_url") else str(req)
            if "s3" in url:
                return make_mock_response({}, status=200)
            if "extract_from_url" in url or "generate_upload_url" in url:
                return make_mock_response(initial_body)
            if "/documents/" in url:
                return make_mock_response(complete_body)
            if "/extractions" in url:
                return make_mock_response(list_body)
            if "/extract/" in url:
                return make_mock_response(complete_body)
            return make_mock_response({})

        dummy_pdf = tmp_path / "dummy.pdf"
        dummy_pdf.write_bytes(b"%PDF")
        monkeypatch.setattr(probe, "SINGLE_DOC_LOCAL", dummy_pdf)
        monkeypatch.setattr(probe, "PORTFOLIO_DOC_LOCAL", dummy_pdf)
        monkeypatch.setattr(probe, "SNAPSHOT_DIR", tmp_path / "snapshots")
        monkeypatch.setattr(probe, "REPO_ROOT", tmp_path)
        monkeypatch.setattr(probe, "POLL_INTERVAL", 0)

        with patch("probe_extraction_endpoints.urllib.request.urlopen", side_effect=fake_urlopen):
            with patch("sys.argv", ["probe_extraction_endpoints.py", "--update"]):
                probe.main()

        assert "extraction" in probe.RUN_DIR.name


# ── Integration (live API, skipped by default) ────────────────────────────────

@pytest.mark.integration
class TestIntegration:
    """Live API tests — run with: pytest -m integration"""

    def test_compare_mode_exits_cleanly(self):
        import os
        if not os.environ.get("SENSIBLE_API_KEY"):
            pytest.skip("SENSIBLE_API_KEY not set")
        with patch("sys.argv", ["probe_extraction_endpoints.py"]):
            probe.main()   # should not raise
