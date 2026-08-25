"""Tests for scripts/sdk_check/check_sdk_readme.py"""

import sys
from unittest.mock import patch, MagicMock

import pytest

import check_sdk_readme

MARKER = check_sdk_readme.SYNC_MARKER
MARKER_LINE = MARKER + "\n"

# ── strip_frontmatter() ───────────────────────────────────────────────────────

class TestStripFrontmatter:
    def test_strips_yaml_block(self):
        content = "---\ntitle: Foo\n---\nBody text"
        assert check_sdk_readme.strip_frontmatter(content) == "Body text"

    def test_strips_leading_newlines_after_frontmatter(self):
        content = "---\ntitle: Foo\n---\n\n\nBody text"
        assert check_sdk_readme.strip_frontmatter(content) == "Body text"

    def test_no_frontmatter_returns_unchanged(self):
        content = "# Title\n\nBody text"
        assert check_sdk_readme.strip_frontmatter(content) == "# Title\n\nBody text"



# ── split_on_marker() ─────────────────────────────────────────────────────────

class TestSplitOnMarker:
    def test_returns_content_after_marker(self):
        text = f"intro\n{MARKER_LINE}body content\n"
        assert check_sdk_readme.split_on_marker(text, "test") == "body content\n"

    def test_marker_at_start(self):
        text = f"{MARKER_LINE}body"
        assert check_sdk_readme.split_on_marker(text, "test") == "body"

    def test_empty_body_after_marker(self):
        text = f"intro\n{MARKER_LINE}"
        assert check_sdk_readme.split_on_marker(text, "test") == ""

    def test_missing_marker_exits(self):
        with pytest.raises(SystemExit):
            check_sdk_readme.split_on_marker("no marker here", "test-source")


# ── build_issue_body() ────────────────────────────────────────────────────────

class TestBuildIssueBody:
    def _make_sdk(self, tmp_path, name, source_body, readme_body=None):
        source = tmp_path / f"{name}.md"
        source.write_text(f"---\ntitle: {name}\n---\n{source_body}")
        return {
            "name": name,
            "readme_url": f"https://raw.githubusercontent.com/sensible-hq/{name}/main/README.md",
            "source_path": str(source),
            "edit_url": f"https://github.com/sensible-hq/{name}/edit/main/README.md",
            "readme_body": readme_body if readme_body is not None else source_body,
        }

    def test_contains_edit_url(self, tmp_path):
        sdk = self._make_sdk(tmp_path, "sensible-api-py", "## SDK overview\nbody\n")
        body = check_sdk_readme.build_issue_body([sdk])
        assert sdk["edit_url"] in body

    def test_contains_sdk_body_content(self, tmp_path):
        sdk = self._make_sdk(tmp_path, "sensible-api-py", "## SDK overview\nbody content here\n")
        body = check_sdk_readme.build_issue_body([sdk])
        assert "body content here" in body

    def test_contains_marker_instruction(self, tmp_path):
        sdk = self._make_sdk(tmp_path, "sensible-api-py", "body\n")
        body = check_sdk_readme.build_issue_body([sdk])
        assert MARKER in body

    def test_multiple_sdks_both_appear(self, tmp_path):
        sdks = [
            self._make_sdk(tmp_path, "sensible-api-py", "python body\n"),
            self._make_sdk(tmp_path, "sensible-api-js", "node body\n"),
        ]
        body = check_sdk_readme.build_issue_body(sdks)
        assert "sensible-api-py" in body
        assert "sensible-api-js" in body
        assert "python body" in body
        assert "node body" in body

    def test_strips_frontmatter_from_source(self, tmp_path):
        sdk = self._make_sdk(tmp_path, "sensible-api-py", "real body\n")
        body = check_sdk_readme.build_issue_body([sdk])
        assert "title:" not in body

    def test_diff_shown_before_copy_paste(self, tmp_path):
        sdk = self._make_sdk(
            tmp_path, "sensible-api-py",
            source_body="## SDK overview\nnew line\n",
            readme_body="## SDK overview\nold line\n",
        )
        body = check_sdk_readme.build_issue_body([sdk])
        diff_pos = body.find("```diff")
        paste_pos = body.find("````markdown")
        assert diff_pos != -1 and paste_pos != -1
        assert diff_pos < paste_pos


# ── main() ────────────────────────────────────────────────────────────────────

class TestMain:
    def _make_source(self, tmp_path, name, body):
        f = tmp_path / f"{name}.md"
        f.write_text(f"---\ntitle: {name}\n---\n{body}")
        return str(f)

    def _readme(self, body):
        return f"# Title\n\nIntro\n\n{MARKER_LINE}{body}"

    def test_passes_when_in_sync(self, tmp_path):
        body = "## SDK overview\nbody content\n"
        py_path = self._make_source(tmp_path, "py", body)
        js_path = self._make_source(tmp_path, "js", body)

        sdks = [
            {**check_sdk_readme.SDKS[0], "source_path": py_path},
            {**check_sdk_readme.SDKS[1], "source_path": js_path},
        ]
        with patch("check_sdk_readme.SDKS", sdks), \
             patch("check_sdk_readme.fetch", side_effect=[self._readme(body), self._readme(body)]):
            check_sdk_readme.main()  # should not raise

    def test_fails_when_out_of_sync(self, tmp_path):
        source_body = "## SDK overview\nnew content\n"
        readme_body = "## SDK overview\nold content\n"
        py_path = self._make_source(tmp_path, "py", source_body)
        js_path = self._make_source(tmp_path, "js", source_body)

        sdks = [
            {**check_sdk_readme.SDKS[0], "source_path": py_path},
            {**check_sdk_readme.SDKS[1], "source_path": js_path},
        ]
        with patch("check_sdk_readme.SDKS", sdks), \
             patch("check_sdk_readme.fetch", return_value=self._readme(readme_body)), \
             patch("check_sdk_readme.open_or_update_issue", return_value="https://github.com/issues/1"):
            with pytest.raises(SystemExit) as exc:
                check_sdk_readme.main()
            assert exc.value.code == 1

    def test_only_drifted_sdks_reported(self, tmp_path):
        body = "## SDK overview\nbody\n"
        new_body = "## SDK overview\nnew body\n"
        py_path = self._make_source(tmp_path, "py", body)
        js_path = self._make_source(tmp_path, "js", new_body)

        sdks = [
            {**check_sdk_readme.SDKS[0], "source_path": py_path},
            {**check_sdk_readme.SDKS[1], "source_path": js_path},
        ]
        captured = []
        with patch("check_sdk_readme.SDKS", sdks), \
             patch("check_sdk_readme.fetch", side_effect=[self._readme(body), self._readme(body)]), \
             patch("check_sdk_readme.open_or_update_issue", side_effect=lambda sdks: captured.extend(sdks) or "url"):
            with pytest.raises(SystemExit):
                check_sdk_readme.main()

        assert len(captured) == 1
        assert captured[0]["name"] == check_sdk_readme.SDKS[1]["name"]
