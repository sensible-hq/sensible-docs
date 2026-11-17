"""Unit tests for scripts/style: python3 -m pytest -q scripts/style/test"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_code_blocks as cb  # noqa: E402
import check_excerpts as ce  # noqa: E402


def test_line_comments_ignores_urls_and_block_comments():
    lines = [
        '{ "url": "https://example.com/a",',
        '  "x": 1, /* see https://docs */',
        '  "y": 2, // real comment',
        '  /* a block comment that mentions // inside',
        '     and ends here */ "z": 3',
    ]
    assert cb.line_comments(lines) == [2]


def test_check_flags_json5_fence_comments_and_repeated_header(tmp_path):
    page = tmp_path / "p.md"
    page.write_text(
        "# T\n\n```json5\n{ \"a\": 1 }\n```\n\n"
        "```json\n/* Sensible uses JSON5 to support in-line comments*/\n{ \"b\": 2 // no\n}\n```\n\n"
        "```json\n/* Sensible uses JSON5 to support in-line comments*/\n{}\n```\n\n"
        "```\n// JavaScript is fine\n```\n"
    )
    problems = cb.check(page)
    assert any(":3: use a ```json fence" in p for p in problems)
    assert any(":9: use /* */" in p for p in problems)
    assert any(":14: the JSON5 header comment" in p for p in problems)
    assert len(problems) == 3


def test_self_named():
    assert ce.self_named("Region", "Use the Region method to extract a rectangle")
    assert ce.self_named("Query Group", "Query Group extracts answers with an LLM")
    assert not ce.self_named("Region", "Extract text from a rectangle set in inches")
    assert not ce.self_named("Lines", "Lines of text are grouped by height")  # sentence-initial ordinary word


def test_element_page():
    assert ce.element_page("docs/Senseml reference/layout-based-methods/region.md")
    assert not ce.element_page("docs/Senseml reference/concepts/ocr.md")
    assert not ce.element_page("docs/welcome/overview.md")


def _tree(tmp_path, guide_text):
    (tmp_path / ".claude/style-guide").mkdir(parents=True)
    (tmp_path / ".github/styles/Sensible").mkdir(parents=True)
    (tmp_path / "style-rules/tests").mkdir(parents=True)
    (tmp_path / ".claude/style-guide/rules.md").write_text(guide_text)
    (tmp_path / ".github/styles/Sensible/EmDash.yml").write_text("extends: existence\n")
    (tmp_path / "style-rules/tests/em.md").write_text("<!-- rules: Sensible.EmDash -->\n")
    return [{"id": "em", "statement": "No em dashes.", "kind": "deterministic", "gate": "block",
             "enforced_by": {"vale": ["Sensible.EmDash"]}, "fixture": "style-rules/tests/em.md",
             "stated_in": [{"file": ".claude/style-guide/rules.md", "quote": "Don't use em dashes."}]}]


def test_registry_detects_drift(tmp_path, monkeypatch):
    import check_registry as cr
    monkeypatch.setattr(cr, "ROOT", tmp_path)
    monkeypatch.setattr(cr, "STYLES", tmp_path / ".github/styles")
    registry = _tree(tmp_path, "Don't use em dashes.\n<!-- rule: em -->\n")
    assert cr.check(registry) == []
    # The guide is reworded: the quote no longer matches.
    (tmp_path / ".claude/style-guide/rules.md").write_text("Avoid em dashes.\n<!-- rule: em -->\n")
    assert any("quote not found" in p for p in cr.check(registry))
    # The marker is gone, or names a rule the registry doesn't have.
    (tmp_path / ".claude/style-guide/rules.md").write_text("Don't use em dashes.\n<!-- rule: emm -->\n")
    problems = cr.check(registry)
    assert any("no <!-- rule: em --> marker" in p for p in problems)
    assert any("unknown rule emm" in p for p in problems)
    # A Vale rule nobody registered.
    (tmp_path / ".claude/style-guide/rules.md").write_text("Don't use em dashes.\n<!-- rule: em -->\n")
    (tmp_path / ".github/styles/Sensible/Orphan.yml").write_text("extends: existence\n")
    assert any("Sensible.Orphan: no registry entry" in p for p in cr.check(registry))
