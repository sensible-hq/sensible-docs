"""Tests for skill_rules.py and skill_overlap.py, with Jev answers faked or replayed."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import skill_rules as sr  # noqa: E402

RULE = {"id": "sensible-em-dash", "statement": "Don't use em dashes."}


def test_sections_keep_file_line_numbers_and_skip_code(tmp_path):
    f = tmp_path / "SKILL.md"
    f.write_text("# Skill\n\nIntro text that is long enough to count as a section.\n\n```\n# not a heading\n```\n\n"
                 "## Step 2\n\n<!-- rule: sensible-em-dash -->\nDo the second step carefully, with enough words.\n")
    secs = sr.sections(f)
    assert [(s["heading"], s["line"]) for s in secs] == [("Skill", 1), ("Step 2", 9)]
    assert "not a heading" not in secs[0]["text"] and secs[1]["markers"] == {"sensible-em-dash"}


def fake(answers):
    def call(state, questions):
        p = answers.get(state["heading"], {"unrelated": 1.0})
        return {"answers": {k: {"choice": max(p, key=p.get), "probabilities": p} for k in questions}}
    return call


def test_restatement_needs_a_marker_and_contradiction_needs_an_exception(tmp_path, monkeypatch):
    f = sr.ROOT / "style-rules/tests/zz-skill-probe.md"
    f.write_text("# Marked\n\n<!-- rule: sensible-em-dash -->\nSplit sentences instead of joining them with dashes.\n\n"
                 "## Unmarked\n\nSplit sentences instead of joining them with long dashes.\n\n"
                 "## Contra\n\nJoin related clauses with an em dash whenever you like.\n")
    try:
        monkeypatch.setattr(sr.jev, "call", fake({"Marked": {"restates": 0.9, "unrelated": 0.1},
                                                   "Unmarked": {"restates": 0.9, "unrelated": 0.1},
                                                   "Contra": {"contradicts": 0.8, "unrelated": 0.2}}))
        monkeypatch.setattr(sr, "load_exceptions", lambda: [])
        res = sr.scan([f], [RULE])
        assert [p.split(" (")[1].split(")")[0] for p in res["problems"]] == ["Unmarked", "Contra"]
        monkeypatch.setattr(sr, "load_exceptions", lambda: [{"file": str(f.relative_to(sr.ROOT)), "heading": "Contra", "rule": RULE["id"]}])
        assert len(sr.scan([f], [RULE])["problems"]) == 1
    finally:
        f.unlink()
