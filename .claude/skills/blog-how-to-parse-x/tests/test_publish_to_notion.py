"""Tests for publish_to_notion.py"""

import os
import pytest
from unittest.mock import MagicMock, call, patch

import publish_to_notion as ptn


# ── Helpers ────────────────────────────────────────────────────────────────────

def mock_get_response(data: dict) -> MagicMock:
    m = MagicMock()
    m.ok = True
    m.json.return_value = data
    m.raise_for_status.return_value = None
    return m


# ── _preprocess ────────────────────────────────────────────────────────────────

class TestPreprocess:
    def test_strips_single_line_comment(self):
        assert ptn._preprocess("before<!-- comment -->after") == "beforeafter"

    def test_strips_config_markers(self):
        content = "intro\n<!-- CONFIG:START -->\n```json\n{}\n```\n<!-- CONFIG:END -->\noutro"
        result = ptn._preprocess(content)
        assert "CONFIG:START" not in result
        assert "CONFIG:END" not in result
        assert "intro" in result
        assert "outro" in result
        assert "```json" in result

    def test_strips_multiline_comment(self):
        content = "A<!-- line1\nline2\nline3 -->B"
        assert ptn._preprocess(content) == "AB"

    def test_no_comments_unchanged(self):
        content = "# Heading\n\nSome text.\n\n```json\n{}\n```"
        assert ptn._preprocess(content) == content

    def test_multiple_comments_all_stripped(self):
        content = "a<!-- x -->b<!-- y -->c"
        assert ptn._preprocess(content) == "abc"


# ── _parse_inline ──────────────────────────────────────────────────────────────

class TestParseInline:
    def test_plain_text(self):
        result = ptn._parse_inline("hello world")
        assert len(result) == 1
        assert result[0]["text"]["content"] == "hello world"
        assert "annotations" not in result[0]

    def test_bold(self):
        result = ptn._parse_inline("use **SenseML** to extract")
        texts = [(r["text"]["content"], r.get("annotations", {})) for r in result]
        assert ("SenseML", {"bold": True}) in texts

    def test_inline_code(self):
        result = ptn._parse_inline("set `residential_appraisal_reports`")
        code_items = [r for r in result if r.get("annotations", {}).get("code")]
        assert len(code_items) == 1
        assert code_items[0]["text"]["content"] == "residential_appraisal_reports"

    def test_link(self):
        result = ptn._parse_inline("[Sensible](https://sensible.so)")
        link_items = [r for r in result if r["text"].get("link")]
        assert len(link_items) == 1
        assert link_items[0]["text"]["content"] == "Sensible"
        assert link_items[0]["text"]["link"]["url"] == "https://sensible.so"

    def test_mixed(self):
        result = ptn._parse_inline("Install with **pip**, then call `extract()`.")
        contents = [r["text"]["content"] for r in result]
        assert "pip" in contents
        assert "extract()" in contents

    def test_empty_string(self):
        result = ptn._parse_inline("")
        assert result == [{"type": "text", "text": {"content": ""}}]


# ── _chunk_code ────────────────────────────────────────────────────────────────

class TestChunkCode:
    def test_short_content_single_chunk(self):
        chunks = ptn._chunk_code("short code")
        assert len(chunks) == 1
        assert chunks[0]["text"]["content"] == "short code"

    def test_long_content_split_at_limit(self):
        content = "x" * 4500
        chunks = ptn._chunk_code(content)
        assert len(chunks) == 3  # 2000 + 2000 + 500
        assert chunks[0]["text"]["content"] == "x" * 2000
        assert chunks[1]["text"]["content"] == "x" * 2000
        assert chunks[2]["text"]["content"] == "x" * 500

    def test_empty_content_returns_empty_element(self):
        chunks = ptn._chunk_code("")
        assert chunks == [{"type": "text", "text": {"content": ""}}]

    def test_exactly_at_limit(self):
        content = "a" * 2000
        chunks = ptn._chunk_code(content)
        assert len(chunks) == 1


# ── _code block builder ────────────────────────────────────────────────────────

class TestCodeBlock:
    def test_json5_normalized_to_json(self):
        block = ptn._code("{}", "json5")
        assert block["code"]["language"] == "json"

    def test_json_kept_as_json(self):
        block = ptn._code("{}", "json")
        assert block["code"]["language"] == "json"

    def test_other_language_preserved(self):
        block = ptn._code("print('hi')", "python")
        assert block["code"]["language"] == "python"

    def test_inline_comments_preserved_verbatim(self):
        code = '/* Sensible uses JSON5 to support in-line comments*/\n{\n  "id": "file #"  /* user-friendly ID */\n}'
        block = ptn._code(code, "json")
        full_content = "".join(c["text"]["content"] for c in block["code"]["rich_text"])
        assert "/* Sensible uses JSON5 to support in-line comments*/" in full_content
        assert "/* user-friendly ID */" in full_content

    def test_block_type_is_code(self):
        block = ptn._code("x", "json")
        assert block["type"] == "code"


# ── parse_blocks ───────────────────────────────────────────────────────────────

class TestParseBlocks:
    def test_h1(self):
        blocks = ptn.parse_blocks("# My Title")
        assert blocks[0]["type"] == "heading_1"
        assert blocks[0]["heading_1"]["rich_text"][0]["text"]["content"] == "My Title"

    def test_h2(self):
        blocks = ptn.parse_blocks("## Section")
        assert blocks[0]["type"] == "heading_2"

    def test_h3_and_h4_both_produce_heading_3(self):
        b3 = ptn.parse_blocks("### Sub")
        b4 = ptn.parse_blocks("#### Deep")
        assert b3[0]["type"] == "heading_3"
        assert b4[0]["type"] == "heading_3"

    def test_paragraph(self):
        blocks = ptn.parse_blocks("Plain text here.")
        assert blocks[0]["type"] == "paragraph"
        assert blocks[0]["paragraph"]["rich_text"][0]["text"]["content"] == "Plain text here."

    def test_bullet_dash(self):
        blocks = ptn.parse_blocks("- item one")
        assert blocks[0]["type"] == "bulleted_list_item"

    def test_bullet_star(self):
        blocks = ptn.parse_blocks("* item two")
        assert blocks[0]["type"] == "bulleted_list_item"

    def test_numbered_list_becomes_bullet(self):
        blocks = ptn.parse_blocks("1. first\n2. second")
        for b in blocks:
            assert b["type"] == "bulleted_list_item"

    def test_divider(self):
        blocks = ptn.parse_blocks("---")
        assert blocks[0]["type"] == "divider"

    def test_blank_lines_skipped(self):
        blocks = ptn.parse_blocks("A\n\nB")
        assert len(blocks) == 2

    def test_code_block_language_and_content(self):
        md = "```json\n{\"id\": \"file #\"}\n```"
        blocks = ptn.parse_blocks(md)
        assert len(blocks) == 1
        assert blocks[0]["type"] == "code"
        assert blocks[0]["code"]["language"] == "json"
        content = blocks[0]["code"]["rich_text"][0]["text"]["content"]
        assert '{"id": "file #"}' in content

    def test_code_block_preserves_inline_comments(self):
        md = (
            "```json\n"
            "/* Sensible uses JSON5 to support in-line comments*/\n"
            "{\n"
            '  "id": "file #",  /* user-friendly ID */\n'
            "}\n"
            "```"
        )
        blocks = ptn.parse_blocks(md)
        full = "".join(c["text"]["content"] for c in blocks[0]["code"]["rich_text"])
        assert "/* Sensible uses JSON5 to support in-line comments*/" in full
        assert "/* user-friendly ID */" in full

    def test_code_block_json5_language_normalized(self):
        md = "```json5\n{}\n```"
        blocks = ptn.parse_blocks(md)
        assert blocks[0]["code"]["language"] == "json"

    def test_html_comment_stripped_before_parse(self):
        md = "intro\n<!-- CONFIG:START -->\n```json\n{}\n```\n<!-- CONFIG:END -->\noutro"
        # preprocess first, as main() does
        blocks = ptn.parse_blocks(ptn._preprocess(md))
        types = [b["type"] for b in blocks]
        assert "code" in types
        # confirm no stray comment text leaks into a paragraph
        paragraphs = [b for b in blocks if b["type"] == "paragraph"]
        for p in paragraphs:
            for rt in p["paragraph"]["rich_text"]:
                assert "CONFIG" not in rt["text"]["content"]

    def test_mixed_document(self):
        md = (
            "# Title\n"
            "\n"
            "Intro paragraph.\n"
            "\n"
            "## Section\n"
            "\n"
            "- bullet one\n"
            "- bullet two\n"
            "\n"
            "```json\n"
            "{}\n"
            "```\n"
        )
        blocks = ptn.parse_blocks(md)
        types = [b["type"] for b in blocks]
        assert "heading_1" in types
        assert "heading_2" in types
        assert "paragraph" in types
        assert "bulleted_list_item" in types
        assert "code" in types


# ── _get_child_version ─────────────────────────────────────────────────────────

class TestGetChildVersion:
    @patch.dict(os.environ, {"NOTION_API_KEY": "secret_test"})
    def test_no_children_returns_zero(self):
        with patch("requests.get", return_value=mock_get_response({"results": []})):
            assert ptn._get_child_version("page-id") == 0

    @patch.dict(os.environ, {"NOTION_API_KEY": "secret_test"})
    def test_picks_highest_version(self):
        results = [
            {"type": "child_page", "child_page": {"title": "Draft v1 — 2026-06-24"}},
            {"type": "child_page", "child_page": {"title": "Draft v2 — 2026-06-25"}},
        ]
        with patch("requests.get", return_value=mock_get_response({"results": results})):
            assert ptn._get_child_version("page-id") == 2

    @patch.dict(os.environ, {"NOTION_API_KEY": "secret_test"})
    def test_ignores_non_draft_child_pages(self):
        results = [
            {"type": "child_page", "child_page": {"title": "Notes"}},
            {"type": "child_page", "child_page": {"title": "Draft v3 — 2026-06-25"}},
        ]
        with patch("requests.get", return_value=mock_get_response({"results": results})):
            assert ptn._get_child_version("page-id") == 3

    @patch.dict(os.environ, {"NOTION_API_KEY": "secret_test"})
    def test_ignores_non_child_page_blocks(self):
        results = [
            {"type": "paragraph", "paragraph": {"rich_text": []}},
            {"type": "child_page", "child_page": {"title": "Draft v1 — 2026-06-01"}},
        ]
        with patch("requests.get", return_value=mock_get_response({"results": results})):
            assert ptn._get_child_version("page-id") == 1


# ── _append_blocks ─────────────────────────────────────────────────────────────

class TestAppendBlocks:
    @patch.dict(os.environ, {"NOTION_API_KEY": "secret_test"})
    def test_single_batch_for_small_input(self):
        blocks = [{"type": "paragraph"}] * 50
        mock_resp = mock_get_response({})
        with patch("requests.patch", return_value=mock_resp) as mock_patch:
            ptn._append_blocks("page-id", blocks)
        assert mock_patch.call_count == 1
        sent = mock_patch.call_args[1]["json"]["children"]
        assert len(sent) == 50

    @patch.dict(os.environ, {"NOTION_API_KEY": "secret_test"})
    def test_two_batches_for_150_blocks(self):
        blocks = [{"type": "paragraph"}] * 150
        mock_resp = mock_get_response({})
        with patch("requests.patch", return_value=mock_resp) as mock_patch:
            ptn._append_blocks("page-id", blocks)
        assert mock_patch.call_count == 2
        first_batch = mock_patch.call_args_list[0][1]["json"]["children"]
        second_batch = mock_patch.call_args_list[1][1]["json"]["children"]
        assert len(first_batch) == 100
        assert len(second_batch) == 50

    @patch.dict(os.environ, {"NOTION_API_KEY": "secret_test"})
    def test_raises_on_api_error(self):
        blocks = [{"type": "paragraph"}]
        mock_resp = MagicMock()
        mock_resp.ok = False
        mock_resp.status_code = 400
        mock_resp.text = "Bad Request"
        mock_resp.raise_for_status.side_effect = Exception("400 error")
        with patch("requests.patch", return_value=mock_resp):
            with pytest.raises(Exception, match="400 error"):
                ptn._append_blocks("page-id", blocks)


# ── _headers — missing API key ─────────────────────────────────────────────────

class TestHeaders:
    def test_exits_when_api_key_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("NOTION_API_KEY", None)
            with pytest.raises(SystemExit):
                ptn._headers()

    def test_includes_bearer_token(self):
        with patch.dict(os.environ, {"NOTION_API_KEY": "secret_abc"}):
            h = ptn._headers()
        assert h["Authorization"] == "Bearer secret_abc"
        assert h["Notion-Version"] == ptn.NOTION_VERSION


# ── Integration (skipped by default) ──────────────────────────────────────────

@pytest.mark.integration
class TestIntegration:
    """Live Notion API tests — only run with: pytest -m integration"""

    def test_real_publish(self, tmp_path):
        if not os.environ.get("NOTION_API_KEY"):
            pytest.skip("NOTION_API_KEY not set")
        pytest.skip("No fixture parent page registered for integration test yet")
