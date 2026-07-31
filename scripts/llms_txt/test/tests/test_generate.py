"""Tests for scripts/llms_txt/generate.py"""

import json
from pathlib import Path

import pytest

import generate
from conftest import FIXTURES, SNAPSHOTS


# ── parse_front_matter() ──────────────────────────────────────────────────────

class TestParseFrontMatter:
    def test_parses_basic_fields(self):
        content = "---\ntitle: My Page\nhidden: true\n---\nBody"
        fm = generate.parse_front_matter(content)
        assert fm["title"] == "My Page"
        assert fm["hidden"] is True

    def test_returns_empty_when_no_frontmatter(self):
        assert generate.parse_front_matter("Just body text") == {}

    def test_returns_empty_on_unclosed_frontmatter(self):
        assert generate.parse_front_matter("---\ntitle: No close") == {}

    def test_returns_empty_on_malformed_yaml(self):
        assert generate.parse_front_matter("---\n: bad: yaml:\n---\n") == {}

    def test_nested_metadata(self):
        content = "---\nmetadata:\n  description: A description\n---\n"
        fm = generate.parse_front_matter(content)
        assert fm["metadata"]["description"] == "A description"


# ── get_page_info() ───────────────────────────────────────────────────────────

class TestGetPageInfo:
    def test_returns_none_for_hidden_page(self, tmp_path):
        p = tmp_path / "page.md"
        p.write_text("---\ntitle: Draft\nhidden: true\n---\n")
        assert generate.get_page_info(p) is None

    def test_returns_info_for_visible_page(self, tmp_path):
        p = tmp_path / "page.md"
        p.write_text("---\ntitle: My Page\nmetadata:\n  description: A desc\n---\n")
        info = generate.get_page_info(p)
        assert info["title"] == "My Page"
        assert info["description"] == "A desc"
        assert info["path"] == "https://docs.sensible.so/docs/page.md"

    def test_falls_back_to_filename_title(self, tmp_path):
        p = tmp_path / "my-page.md"
        p.write_text("---\n---\n")
        info = generate.get_page_info(p)
        assert info["title"] == "My Page"

    def test_empty_description_when_missing(self, tmp_path):
        p = tmp_path / "page.md"
        p.write_text("---\ntitle: No Desc\n---\n")
        assert generate.get_page_info(p)["description"] == ""

    def test_returns_none_for_unreadable_file(self, tmp_path):
        assert generate.get_page_info(tmp_path / "nonexistent.md") is None

    def test_path_uses_stem_only_not_directory(self, tmp_path):
        # ReadMe URLs are slug-only — the category directory is not part of the URL
        subdir = tmp_path / "Senseml reference" / "concepts"
        subdir.mkdir(parents=True)
        p = subdir / "sections.md"
        p.write_text("---\ntitle: Sections\n---\n")
        info = generate.get_page_info(p)
        assert info["path"] == "https://docs.sensible.so/docs/sections.md"


# ── read_order() ──────────────────────────────────────────────────────────────

class TestReadOrder:
    def test_returns_slugs_from_valid_yaml(self, tmp_path):
        f = tmp_path / "_order.yaml"
        f.write_text("- overview\n- getting-started\n")
        assert generate.read_order(f) == ["overview", "getting-started"]

    def test_returns_empty_for_missing_file(self, tmp_path):
        assert generate.read_order(tmp_path / "_order.yaml") == []

    def test_returns_empty_for_malformed_yaml(self, tmp_path):
        f = tmp_path / "_order.yaml"
        f.write_text(": bad: yaml:\n")
        assert generate.read_order(f) == []

    def test_filters_non_string_items(self, tmp_path):
        f = tmp_path / "_order.yaml"
        f.write_text("- overview\n- 42\n- true\n")
        assert generate.read_order(f) == ["overview"]


# ── resolve_slug() ────────────────────────────────────────────────────────────

class TestResolveSlug:
    def test_resolves_md_file(self, tmp_path):
        (tmp_path / "overview.md").touch()
        assert generate.resolve_slug("overview", tmp_path) == tmp_path / "overview.md"

    def test_resolves_directory(self, tmp_path):
        (tmp_path / "methods").mkdir()
        assert generate.resolve_slug("methods", tmp_path) == tmp_path / "methods"

    def test_md_takes_precedence_over_directory(self, tmp_path):
        (tmp_path / "methods.md").touch()
        (tmp_path / "methods").mkdir()
        assert generate.resolve_slug("methods", tmp_path) == tmp_path / "methods.md"

    def test_index_resolves_to_index_md(self, tmp_path):
        (tmp_path / "index.md").touch()
        assert generate.resolve_slug("index", tmp_path) == tmp_path / "index.md"

    def test_index_returns_none_when_no_index_md(self, tmp_path):
        assert generate.resolve_slug("index", tmp_path) is None

    def test_returns_none_when_nothing_matches(self, tmp_path):
        assert generate.resolve_slug("nonexistent", tmp_path) is None


# ── collect_openapi_specs() ───────────────────────────────────────────────────

class TestCollectOpenApiSpecs:
    def test_picks_up_openapi_files(self, tmp_path):
        ref = tmp_path / "reference"
        ref.mkdir()
        (ref / "openapi_extraction.json").write_text(
            json.dumps({"info": {"title": "Extraction"}})
        )
        lines = generate.collect_openapi_specs(tmp_path)
        assert len(lines) == 1
        assert "[Extraction]" in lines[0]
        assert "openapi_extraction.json" in lines[0]

    def test_ignores_non_openapi_json(self, tmp_path):
        ref = tmp_path / "reference"
        ref.mkdir()
        (ref / "sensible.json").write_text(json.dumps({"info": {"title": "Other"}}))
        assert generate.collect_openapi_specs(tmp_path) == []

    def test_falls_back_to_stem_on_bad_json(self, tmp_path):
        ref = tmp_path / "reference"
        ref.mkdir()
        (ref / "openapi_broken.json").write_text("not json")
        lines = generate.collect_openapi_specs(tmp_path)
        assert "[openapi_broken]" in lines[0]

    def test_sorted_by_filename(self, tmp_path):
        ref = tmp_path / "reference"
        ref.mkdir()
        for name in ["openapi_z.json", "openapi_a.json"]:
            (ref / name).write_text(json.dumps({"info": {"title": name}}))
        lines = generate.collect_openapi_specs(tmp_path)
        assert "openapi_a.json" in lines[0]
        assert "openapi_z.json" in lines[1]


# ── check() ───────────────────────────────────────────────────────────────────

class TestCheck:
    def test_clean_fixture_tree_has_no_issues(self):
        issues = generate.check(FIXTURES)
        assert issues == []

    def test_detects_missing_category_directory(self, tmp_path):
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "_order.yaml").write_text("- nonexistent-category\n")
        (tmp_path / "reference").mkdir()
        (tmp_path / "reference" / "_order.yaml").write_text("")
        issues = generate.check(tmp_path)
        assert any("nonexistent-category" in i for i in issues)

    def test_detects_stale_slug_in_nested_order(self, tmp_path):
        docs = tmp_path / "docs"
        cat = docs / "mycat"
        cat.mkdir(parents=True)
        (docs / "_order.yaml").write_text("- mycat\n")
        (cat / "_order.yaml").write_text("- ghost-page\n")
        (tmp_path / "reference").mkdir()
        (tmp_path / "reference" / "_order.yaml").write_text("")
        issues = generate.check(tmp_path)
        assert any("ghost-page" in i for i in issues)

    def test_skips_docs_skip_entries(self, tmp_path):
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "_order.yaml").write_text("- llms.txt\n")
        (tmp_path / "reference").mkdir()
        (tmp_path / "reference" / "_order.yaml").write_text("")
        assert generate.check(tmp_path) == []

    def test_skips_reference_skip_entries(self, tmp_path):
        (tmp_path / "docs").mkdir()
        (tmp_path / "docs" / "_order.yaml").write_text("")
        ref = tmp_path / "reference"
        ref.mkdir()
        (ref / "_order.yaml").write_text("- ReadMeConfig\n")
        assert generate.check(tmp_path) == []


# ── generate() — snapshot ─────────────────────────────────────────────────────

class TestGenerate:
    SNAPSHOT = SNAPSHOTS / "generate.txt"

    def test_matches_snapshot(self):
        output = generate.generate(FIXTURES)
        if not self.SNAPSHOT.exists():
            self.SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
            self.SNAPSHOT.write_text(output)
            pytest.skip("Snapshot created — run again to verify")
        assert output == self.SNAPSHOT.read_text(), (
            "generate() output changed. If intentional, delete snapshots/generate.txt and re-run."
        )

    def test_hidden_page_excluded(self):
        output = generate.generate(FIXTURES)
        # welcome/index.md has hidden: true — its title must not appear
        assert "Welcome" not in output

    def test_index_md_included_before_children(self):
        # methods/ has an index.md — it should appear before anchor.md in the output
        output = generate.generate(FIXTURES)
        lines = output.splitlines()
        methods_idx = next(i for i, l in enumerate(lines) if "SenseML Methods" in l)
        anchor_idx = next(i for i, l in enumerate(lines) if "Anchor" in l)
        assert methods_idx < anchor_idx

    def test_llms_txt_category_excluded(self):
        # docs/_order.yaml includes "llms.txt" — should be skipped (DOCS_SKIP)
        assert "llms.txt" not in generate.generate(FIXTURES)

    def test_readmeconfig_excluded(self):
        # reference/_order.yaml includes ReadMeConfig — should be skipped (REFERENCE_SKIP)
        output = generate.generate(FIXTURES)
        assert "ReadMeConfig" not in output

    def test_api_reference_section_links_to_specs(self):
        output = generate.generate(FIXTURES)
        assert "## api reference" in output
        assert "openapi_extraction.json" in output
        assert "OpenAPI specification" in output
