"""Tests for check_excerpt, add_excerpt, sync_description, fix_frontmatter, and shorten_excerpt scripts."""

import textwrap
from pathlib import Path

import pytest
import yaml

import check_excerpt
import add_excerpt
import sync_description
import fix_frontmatter
import shorten_excerpt


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_md(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(textwrap.dedent(content), encoding="utf-8")
    return p


FM_WITH_EXCERPT = """\
    ---
    title: Test Page
    excerpt: A fine excerpt
    deprecated: false
    hidden: false
    metadata:
      title: ''
      description: A fine excerpt
      robots: index
    ---
    Body text.
    """

FM_NO_EXCERPT = """\
    ---
    title: Test Page
    deprecated: false
    hidden: false
    metadata:
      title: ''
      description: ''
      robots: index
    ---
    Body text.
    """

FM_EMPTY_EXCERPT = """\
    ---
    title: Test Page
    excerpt: ''
    deprecated: false
    hidden: false
    metadata:
      title: ''
      description: ''
      robots: index
    ---
    Body text.
    """

FM_HIDDEN = """\
    ---
    title: Hidden Page
    hidden: true
    metadata:
      robots: index
    ---
    Body text.
    """

FM_WITH_EXCERPT_STALE_DESC = """\
    ---
    title: Test Page
    excerpt: New excerpt text
    deprecated: false
    hidden: false
    metadata:
      title: ''
      description: Old description text
      robots: index
    ---
    Body text.
    """

FM_WITH_EXCERPT_NO_DESC = """\
    ---
    title: Test Page
    excerpt: My excerpt
    deprecated: false
    hidden: false
    metadata:
      title: ''
      robots: index
    ---
    Body text.
    """


# ---------------------------------------------------------------------------
# check_excerpt
# ---------------------------------------------------------------------------

class TestCheckExcerpt:
    def _run(self, tmp_path, docs_files=None, reference_files=None):
        repo_root = tmp_path
        (repo_root / "docs").mkdir()
        (repo_root / "reference").mkdir()

        for name, content in (docs_files or {}).items():
            make_md(repo_root / "docs", name, content)
        for name, content in (reference_files or {}).items():
            make_md(repo_root / "reference", name, content)

        issues, _ = check_excerpt.check_excerpts(repo_root, ignore_list=set())
        return issues

    def test_docs_missing_excerpt_key_flagged(self, tmp_path):
        issues = self._run(tmp_path, docs_files={"page.md": FM_NO_EXCERPT})
        assert len(issues) == 1
        assert issues[0]["reason"] == "Missing excerpt key"

    def test_docs_empty_excerpt_flagged(self, tmp_path):
        issues = self._run(tmp_path, docs_files={"page.md": FM_EMPTY_EXCERPT})
        assert len(issues) == 1
        assert issues[0]["reason"] == "Empty excerpt"

    def test_docs_populated_excerpt_passes(self, tmp_path):
        issues = self._run(tmp_path, docs_files={"page.md": FM_WITH_EXCERPT})
        assert issues == []

    def test_docs_hidden_file_skipped(self, tmp_path):
        issues = self._run(tmp_path, docs_files={"hidden.md": FM_HIDDEN})
        assert issues == []

    def test_reference_missing_excerpt_key_skipped(self, tmp_path):
        issues = self._run(tmp_path, reference_files={"page.md": FM_NO_EXCERPT})
        assert issues == []

    def test_reference_empty_excerpt_flagged(self, tmp_path):
        issues = self._run(tmp_path, reference_files={"page.md": FM_EMPTY_EXCERPT})
        assert len(issues) == 1
        assert issues[0]["reason"] == "Empty excerpt"


# ---------------------------------------------------------------------------
# add_excerpt
# ---------------------------------------------------------------------------

class TestAddExcerpt:
    def test_updates_existing_excerpt(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_WITH_EXCERPT)
        result = add_excerpt.update_file_with_excerpt(f, "Updated excerpt")
        assert result is True
        content = f.read_text()
        assert "excerpt: Updated excerpt" in content

    def test_inserts_excerpt_when_absent(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_NO_EXCERPT)
        result = add_excerpt.update_file_with_excerpt(f, "Brand new excerpt")
        assert result is True
        content = f.read_text()
        assert "excerpt: Brand new excerpt" in content
        # Should appear right after the title line
        lines = content.splitlines()
        title_idx = next(i for i, l in enumerate(lines) if l.startswith("title:"))
        excerpt_idx = next(i for i, l in enumerate(lines) if l.startswith("excerpt:"))
        assert excerpt_idx == title_idx + 1

    def test_replaces_empty_excerpt(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_EMPTY_EXCERPT)
        result = add_excerpt.update_file_with_excerpt(f, "Filled in")
        assert result is True
        assert "excerpt: Filled in" in f.read_text()

    def test_replaces_multiline_yaml_excerpt(self, tmp_path):
        # Regression: multi-line YAML scalar excerpts left the continuation
        # line behind, duplicating part of the old value alongside the new one.
        content = (
            "---\n"
            "title: Test Page\n"
            "excerpt: Old first line of a long excerpt that wraps,\n"
            "  covering many topics in the second line.\n"
            "deprecated: false\n"
            "---\nBody.\n"
        )
        f = tmp_path / "page.md"
        f.write_text(content, encoding="utf-8")
        result = add_excerpt.update_file_with_excerpt(f, "New short excerpt")
        assert result is True
        text = f.read_text()
        assert "excerpt: New short excerpt" in text
        assert "covering many topics" not in text  # old continuation must be gone

    def test_crlf_body_preserved(self, tmp_path):
        # Regression: files with CRLF line endings in their body (e.g. code blocks
        # pasted from Windows) must not have those endings stripped when only the
        # front matter is updated.
        content = (
            "---\n"
            "title: Test Page\n"
            "excerpt: Old excerpt\n"
            "deprecated: false\n"
            "---\n"
            "## Body\r\n"
            "\r\n"
            "```json\r\n"
            '{"key": "value"}\r\n'
            "```\r\n"
        )
        f = tmp_path / "page.md"
        f.write_bytes(content.encode("utf-8"))
        result = add_excerpt.update_file_with_excerpt(f, "New excerpt")
        assert result is True
        raw = f.read_bytes().decode("utf-8")
        assert "excerpt: New excerpt" in raw
        assert "```json\r\n" in raw  # CRLF must survive the rewrite

    def test_no_frontmatter_returns_false(self, tmp_path):
        f = tmp_path / "plain.md"
        f.write_text("No front matter here.\n", encoding="utf-8")
        result = add_excerpt.update_file_with_excerpt(f, "some text")
        assert result is False


# ---------------------------------------------------------------------------
# sync_description
# ---------------------------------------------------------------------------

class TestSyncDescription:
    def test_copies_excerpt_to_description(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_WITH_EXCERPT_STALE_DESC)
        result = sync_description.sync_description(f, dry_run=False)
        assert result is True
        content = f.read_text()
        assert "description: New excerpt text" in content

    def test_inserts_description_when_absent(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_WITH_EXCERPT_NO_DESC)
        result = sync_description.sync_description(f, dry_run=False)
        assert result is True
        assert "description: My excerpt" in f.read_text()

    def test_creates_metadata_block_when_absent(self, tmp_path):
        # Regression: files with no metadata block raised KeyError and aborted the workflow.
        f = make_md(tmp_path, "page.md", """\
            ---
            title: Test Page
            excerpt: My excerpt
            link:
              new_tab: false
            ---
            Body text.
            """)
        assert sync_description.sync_description(f, dry_run=False) is True
        fm = yaml.safe_load(f.read_text().split("---")[1])
        assert fm["metadata"] == {"description": "My excerpt"}
        assert fm["link"] == {"new_tab": False}

    def test_no_change_when_already_in_sync(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_WITH_EXCERPT)
        result = sync_description.sync_description(f, dry_run=False)
        assert result is False

    def test_skips_file_with_no_excerpt(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_NO_EXCERPT)
        result = sync_description.sync_description(f, dry_run=False)
        assert result is False

    def test_dry_run_does_not_write(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_WITH_EXCERPT_STALE_DESC)
        original = f.read_text()
        result = sync_description.sync_description(f, dry_run=True)
        assert result is True
        assert f.read_text() == original


# ---------------------------------------------------------------------------
# fix_frontmatter
# ---------------------------------------------------------------------------

FM_UNDERINDENTED_CONTINUATION = """\
    ---
    title: Go-live checklist
    excerpt: Essential checklist for deploying configs,
      covering publishing and logging.
    hidden: false
    metadata:
      title: ''
      description: Essential checklist for deploying configs,
      covering publishing and logging.
      robots: index
    ---
    Body text.
    """

FM_UNQUOTED_COLON = """\
    ---
    title: Test Page
    excerpt: Note: this value has a colon
    hidden: false
    ---
    Body text.
    """

FM_BLOCK_SCALAR = """\
    ---
    title: Test Page
    excerpt: |
      Line one
      Line two
    hidden: false
    metadata:
      description: Broken,
      continuation
    ---
    Body text.
    """


def load_fm(path: Path) -> dict:
    content = path.read_text(encoding="utf-8")
    fm_text, _, _ = fix_frontmatter.split_frontmatter(content)
    return yaml.safe_load(fm_text)


class TestFixFrontmatter:
    def test_valid_file_untouched(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_WITH_EXCERPT)
        original = f.read_text()
        assert fix_frontmatter.fix_file(f, dry_run=False) == ("ok", None)
        assert f.read_text() == original

    def test_joins_underindented_continuation(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_UNDERINDENTED_CONTINUATION)
        status, _ = fix_frontmatter.fix_file(f, dry_run=False)
        assert status == "fixed"
        fm = load_fm(f)
        expected = "Essential checklist for deploying configs, covering publishing and logging."
        assert fm["excerpt"] == expected
        assert fm["metadata"]["description"] == expected
        assert fm["metadata"]["robots"] == "index"
        assert f.read_text().endswith("---\nBody text.\n")

    def test_quotes_value_with_colon(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_UNQUOTED_COLON)
        status, _ = fix_frontmatter.fix_file(f, dry_run=False)
        assert status == "fixed"
        assert load_fm(f)["excerpt"] == "Note: this value has a colon"

    def test_block_scalar_preserved(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_BLOCK_SCALAR)
        status, _ = fix_frontmatter.fix_file(f, dry_run=False)
        assert status == "fixed"
        fm = load_fm(f)
        assert fm["excerpt"] == "Line one\nLine two\n"
        assert fm["metadata"]["description"] == "Broken, continuation"

    def test_crlf_preserved(self, tmp_path):
        f = tmp_path / "page.md"
        crlf = textwrap.dedent(FM_UNDERINDENTED_CONTINUATION).replace("\n", "\r\n")
        f.write_bytes(crlf.encode("utf-8"))
        status, _ = fix_frontmatter.fix_file(f, dry_run=False)
        assert status == "fixed"
        raw = f.read_bytes().decode("utf-8")
        assert "\n" not in raw.replace("\r\n", "")

    def test_dry_run_does_not_write(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_UNDERINDENTED_CONTINUATION)
        original = f.read_text()
        assert fix_frontmatter.fix_file(f, dry_run=True)[0] == "fixed"
        assert f.read_text() == original

    def test_unfixable_reported_and_untouched(self, tmp_path):
        f = make_md(tmp_path, "page.md", """\
            ---
            title: [unclosed
            ---
            Body text.
            """)
        original = f.read_text()
        status, error = fix_frontmatter.fix_file(f, dry_run=False)
        assert status == "unfixable"
        assert error
        assert f.read_text() == original


# ---------------------------------------------------------------------------
# shorten_excerpt
# ---------------------------------------------------------------------------

class TestShortenExcerpt:
    def test_short_text_unchanged(self):
        text = "Learn how to use the Row method, including examples."
        assert shorten_excerpt.shorten(text) == text

    def test_drops_opener_when_that_is_enough(self):
        text = "Learn how to " + "x" * 150
        assert shorten_excerpt.shorten(text) == "X" + "x" * 149

    def test_prefers_sentence_end(self):
        text = (
            "For corner cases, the Deskew preprocessor corrects skewed document alignment in Sensible. "
            "In most cases Sensible applies default, automatic correction for skewed documents."
        )
        assert shorten_excerpt.shorten(text) == (
            "For corner cases, the Deskew preprocessor corrects skewed document alignment in Sensible."
        )

    def test_clause_cut_outside_list(self):
        text = (
            "Concatenate method joins outputs of two or more fields into a single string or array, "
            "with configurable delimiters and support for mixed string and array inputs."
        )
        assert shorten_excerpt.shorten(text) == (
            "Concatenate method joins outputs of two or more fields into a single string or array."
        )

    def test_list_cut_restores_oxford_conjunction(self):
        text = (
            "Overview of Sensible's LLM-powered features for document data extraction and classification, "
            "including tables, lists, multimodal data, confidence signals, and portfolio segmentation."
        )
        assert shorten_excerpt.shorten(text) == (
            "Sensible's LLM-powered features for document data extraction and classification, "
            "including tables, lists, multimodal data, and confidence signals."
        )

    def test_list_cut_two_items_no_comma(self):
        text = (
            "Checkbox method extracts boolean selection status from PDF checkboxes using form metadata "
            "or pixel recognition, with parameters for position, size, and darkness threshold."
        )
        assert shorten_excerpt.shorten(text) == (
            "Checkbox method extracts boolean selection status from PDF checkboxes using form metadata "
            "or pixel recognition, with parameters for position and size."
        )

    def test_phrase_cut(self):
        text = (
            "Scale preprocessor documentation explaining how to correct text size variations in scanned "
            "documents like ID cards and receipts to enable accurate coordinate-based data extraction."
        )
        assert shorten_excerpt.shorten(text) == (
            "Scale preprocessor documentation explaining how to correct text size variations in scanned "
            "documents like ID cards and receipts."
        )

    def test_word_cut_fallback(self):
        text = " ".join(["word"] * 50)
        result = shorten_excerpt.shorten(text)
        assert len(result) <= 160
        assert result.endswith("word.")

    def test_results_fit_and_are_idempotent(self):
        texts = [
            "Learn how " + ", ".join(f"item{i}" for i in range(40)) + ", and last.",
            "a " * 100,
            "Learn how to do things, " + "with " * 40 + "end.",
        ]
        for text in texts:
            once = shorten_excerpt.shorten(text)
            assert len(once) <= 160
            assert shorten_excerpt.shorten(once) == once

    def test_shortens_file_fields(self, tmp_path):
        long = "Learn how to " + "use this feature well " * 10
        f = make_md(tmp_path, "page.md", f"""\
            ---
            title: Test Page
            excerpt: {long}
            hidden: false
            metadata:
              title: ''
              description: {long}
              robots: index
            ---
            Body text.
            """)
        changes = shorten_excerpt.shorten_file(f, dry_run=False)
        assert [c[0] for c in changes] == ["excerpt", "metadata.description"]
        fm = yaml.safe_load(f.read_text().split("---")[1])
        assert len(fm["excerpt"]) <= 160
        assert fm["excerpt"] == fm["metadata"]["description"]
        assert fm["metadata"]["robots"] == "index"
        assert f.read_text().endswith("---\nBody text.\n")

    def test_dry_run_does_not_write(self, tmp_path):
        f = make_md(tmp_path, "page.md", f"""\
            ---
            title: Test Page
            excerpt: {"x " * 100}
            ---
            Body text.
            """)
        original = f.read_text()
        assert shorten_excerpt.shorten_file(f, dry_run=True)
        assert f.read_text() == original
