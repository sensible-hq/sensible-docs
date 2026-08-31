"""Tests for check_excerpt, add_excerpt, and sync_description scripts."""

import textwrap
from pathlib import Path

import pytest

import check_excerpt
import add_excerpt
import sync_description


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
