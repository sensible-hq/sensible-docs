"""Tests for the scripts/descriptions excerpt pipeline."""

import textwrap
from pathlib import Path

import pytest
import yaml

import check_excerpt
import frontmatter
import generate_excerpts
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

        return check_excerpt.check_excerpts(repo_root)

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

    def test_reference_missing_keys_skipped(self, tmp_path):
        issues = self._run(tmp_path, reference_files={"page.md": FM_HIDDEN.replace("hidden: true", "hidden: false")})
        assert issues == []

    def test_reference_empty_excerpt_flagged(self, tmp_path):
        issues = self._run(tmp_path, reference_files={"page.md": FM_EMPTY_EXCERPT})
        assert len(issues) == 1
        assert issues[0]["reason"] == "Empty excerpt"

    def test_reference_empty_description_without_excerpt_flagged(self, tmp_path):
        # Previously handled by check_descriptions.py in sync-llmstxt.yml.
        issues = self._run(tmp_path, reference_files={"page.md": FM_NO_EXCERPT})
        assert len(issues) == 1
        assert issues[0]["reason"] == "Empty metadata.description"

    def test_missing_title_flagged(self, tmp_path):
        issues = self._run(tmp_path, docs_files={"page.md": FM_WITH_EXCERPT.replace("    title: Test Page\n", "")})
        assert [i["reason"] for i in issues] == ["Missing title key"]

    def test_reference_api_page_without_title_skipped(self, tmp_path):
        issues = self._run(tmp_path, reference_files={"page.md": "---\napi:\n  file: spec.json\nhidden: false\n---\n"})
        assert issues == []

    def test_invalid_yaml_flagged(self, tmp_path):
        issues = self._run(tmp_path, docs_files={"page.md": "---\ntitle: [unclosed\n---\nBody.\n"})
        assert len(issues) == 1
        assert issues[0]["reason"].startswith("Invalid YAML frontmatter")


# ---------------------------------------------------------------------------
# frontmatter
# ---------------------------------------------------------------------------

def write_excerpt(path: Path, excerpt: str) -> bool:
    doc = frontmatter.read(path)
    if doc.fm is None:
        return False
    frontmatter.write(doc, frontmatter.set_excerpt(doc.fm, excerpt))
    return True


class TestFrontmatter:
    def test_updates_existing_excerpt(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_WITH_EXCERPT)
        assert write_excerpt(f, "Updated excerpt")
        assert "excerpt: Updated excerpt" in f.read_text()

    def test_inserts_excerpt_after_title(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_NO_EXCERPT)
        assert write_excerpt(f, "Brand new excerpt")
        lines = f.read_text().splitlines()
        title_idx = next(i for i, l in enumerate(lines) if l.startswith("title:"))
        assert lines[title_idx + 1] == "excerpt: Brand new excerpt"

    def test_replaces_multiline_yaml_excerpt(self, tmp_path):
        # Regression: multi-line YAML scalar excerpts left the continuation
        # line behind, duplicating part of the old value alongside the new one.
        f = tmp_path / "page.md"
        f.write_text(
            "---\ntitle: Test Page\nexcerpt: Old first line of a long excerpt that wraps,\n"
            "  covering many topics in the second line.\ndeprecated: false\n---\nBody.\n",
            encoding="utf-8",
        )
        assert write_excerpt(f, "New short excerpt")
        text = f.read_text()
        assert "excerpt: New short excerpt" in text
        assert "covering many topics" not in text

    def test_long_values_not_wrapped(self, tmp_path):
        # Regression: yaml.dump wrapped long values at 80 columns, which later broke go-live.md.
        f = make_md(tmp_path, "page.md", FM_WITH_EXCERPT)
        long = "word " * 40
        assert write_excerpt(f, long.strip())
        assert f"excerpt: {long.strip()}\n" in f.read_text()

    def test_crlf_body_preserved(self, tmp_path):
        # Regression: CRLF line endings in the body must survive a front matter rewrite.
        f = tmp_path / "page.md"
        f.write_bytes(
            "---\ntitle: Test Page\nexcerpt: Old excerpt\n---\n## Body\r\n\r\n```json\r\n{}\r\n```\r\n".encode()
        )
        assert write_excerpt(f, "New excerpt")
        raw = f.read_bytes().decode("utf-8")
        assert "excerpt: New excerpt" in raw
        assert "```json\r\n" in raw

    def test_no_frontmatter(self, tmp_path):
        f = tmp_path / "plain.md"
        f.write_text("No front matter here.\n", encoding="utf-8")
        assert not write_excerpt(f, "some text")

    def test_write_adds_hidden_false(self, tmp_path):
        f = make_md(tmp_path, "page.md", """\
            ---
            title: Test Page
            link:
              new_tab: false
            ---
            Body text.
            """)
        assert write_excerpt(f, "New")
        fm = frontmatter.read(f).fm
        assert list(fm) == ["title", "excerpt", "hidden", "link"]
        assert fm["hidden"] is False

    def test_write_keeps_existing_hidden(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_HIDDEN)
        assert write_excerpt(f, "New")
        assert frontmatter.read(f).fm["hidden"] is True

    def test_set_description_creates_metadata(self):
        fm = frontmatter.set_description({"title": "T"}, "D")
        assert fm == {"title": "T", "metadata": {"title": "", "description": "D", "robots": "index"}}

    @pytest.mark.parametrize("rel, fm, expected", [
        ("docs/a.md", {"title": "T"}, "excerpt"),
        ("docs/a.md", {"excerpt": "  "}, "excerpt"),
        ("docs/a.md", {"excerpt": "Fine"}, None),
        ("docs/a.md", {"hidden": True}, None),
        ("reference/a.md", {"title": "T"}, None),
        ("reference/a.md", {"excerpt": ""}, "excerpt"),
        ("reference/a.md", {"excerpt": "Fine", "metadata": {"description": ""}}, None),
        ("reference/a.md", {"metadata": {"description": ""}}, "metadata.description"),
        ("reference/a.md", {"metadata": {"description": "Fine"}}, None),
    ])
    def test_missing_field(self, rel, fm, expected):
        assert frontmatter.missing_field(rel, fm) == expected


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
        assert list(fm["metadata"].items()) == [("title", ""), ("description", "My excerpt"), ("robots", "index")]
        assert fm["link"] == {"new_tab": False}
        assert list(fm) == ["title", "excerpt", "hidden", "link", "metadata"]
        assert fm["hidden"] is False

    def test_inserts_description_after_title(self, tmp_path):
        f = make_md(tmp_path, "page.md", FM_WITH_EXCERPT_NO_DESC)
        assert sync_description.sync_description(f, dry_run=False) is True
        fm = yaml.safe_load(f.read_text().split("---")[1])
        assert list(fm["metadata"]) == ["title", "description", "robots"]

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
    return frontmatter.read(path).fm


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

    def test_shortens_excerpt_only(self, tmp_path):
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
        old, new = shorten_excerpt.shorten_file(f, dry_run=False)
        assert old == long.strip() and len(new) <= 160
        fm = yaml.safe_load(f.read_text().split("---")[1])
        assert fm["excerpt"] == new
        # sync_description.py owns metadata.description.
        assert fm["metadata"]["description"] == long.strip()
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


# ---------------------------------------------------------------------------
# generate_excerpts
# ---------------------------------------------------------------------------

class TestGenerateExcerpts:
    def test_retries_until_short_enough(self, tmp_path, monkeypatch):
        replies = iter(["x" * 200, "y" * 170, "Short enough."])
        calls = []

        def fake_call(messages, api_key):
            calls.append(list(messages))
            return next(replies)

        monkeypatch.setattr(generate_excerpts, "call_claude", fake_call)
        doc = frontmatter.read(make_md(tmp_path, "page.md", FM_NO_EXCERPT))
        assert generate_excerpts.generate_excerpt(doc, "key") == "Short enough."
        assert len(calls) == 3
        assert "200 characters" in calls[1][-1]["content"]

    def test_shortens_after_max_attempts(self, tmp_path, monkeypatch):
        long = "Learn how to " + "use this feature well " * 10
        monkeypatch.setattr(generate_excerpts, "call_claude", lambda messages, api_key: long)
        doc = frontmatter.read(make_md(tmp_path, "page.md", FM_NO_EXCERPT))
        assert generate_excerpts.generate_excerpt(doc, "key") == shorten_excerpt.shorten(long)

    @pytest.mark.parametrize("rel, fm, missing_only, expected", [
        ("docs/a.md", {"excerpt": "Fine"}, True, None),
        ("docs/a.md", {"excerpt": "Fine"}, False, "excerpt"),
        ("docs/a.md", {"hidden": True}, False, None),
        ("reference/a.md", {"title": "T"}, False, None),
        ("reference/a.md", {"metadata": {"description": "Old"}}, False, "metadata.description"),
    ])
    def test_target_field(self, rel, fm, missing_only, expected):
        assert generate_excerpts.target_field(rel, fm, missing_only) == expected

    def test_apply_docs_sets_both_fields(self):
        fm = generate_excerpts.apply("docs/a.md", {"title": "T"}, "excerpt", "New")
        assert list(fm) == ["title", "excerpt", "metadata"]
        assert fm["metadata"] == {"title": "", "description": "New", "robots": "index"}

    def test_apply_reference_does_not_add_description(self):
        fm = generate_excerpts.apply("reference/a.md", {"title": "T", "excerpt": ""}, "excerpt", "New")
        assert fm == {"title": "T", "excerpt": "New"}

    def test_apply_reference_description_only(self):
        fm = generate_excerpts.apply("reference/a.md", {"metadata": {"description": ""}}, "metadata.description", "New")
        assert fm == {"metadata": {"description": "New"}}
