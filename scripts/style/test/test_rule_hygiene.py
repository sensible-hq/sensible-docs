"""Tests for rule_hygiene.py: offline, from recorded Jev answers and Vale."""
import shutil
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import rule_hygiene as rh  # noqa: E402


def spec(rid, criteria, violation, examples=None):
    return {"id": rid, "check": {"question": {"ask": "?", "criteria": criteria}, "verdicts": {"violation": violation}},
            "examples": examples or {}}


def test_catalog_flags_one_name_with_two_meanings_and_copied_cases():
    specs = {"a": spec("a", {"bad": "x", "other": "none of these"}, ["bad"], {"fail": "Please note that it works."}),
             "b": spec("b", {"bad": "something else", "other": "none of these"}, ["bad"])}
    labels = {"a": [{"text": "Please note that it works.", "expected": "bad"}, {"text": "A fresh sentence here.", "expected": "bad"}]}
    out = rh.catalog(specs, labels)
    assert len(out["problems"]) == 1 and "'bad'" in out["problems"][0]
    assert out["copied"] == [("a", "Please note that it works.")]


def test_overlap_separates_near_duplicates_from_unsure(monkeypatch):
    s = spec("a", {"bad": "", "worse": "", "good": ""}, ["bad", "worse"])
    answers = [{"probabilities": {"bad": 0.4, "worse": 0.4, "good": 0.2}}] * 2 + [{"probabilities": {"bad": 0.5, "good": 0.5}}] * 2
    monkeypatch.setattr(rh, "answers_for", lambda rid, spec, cases: [({}, a) for a in answers])
    out = rh.overlap({"a": s}, {"a": [{}] * 4})
    assert out["problems"] == ["a: choices 'bad' and 'worse' split the probability on 2 of 4 cases"]
    assert ("a", "bad", "good", 2, 4, False) in out["rows"]  # opposite sides: reported, not a problem


def test_relations_block_unresolved_conflicts(monkeypatch):
    registry = [{"id": "x", "statement": "Do X."}, {"id": "y", "statement": "Never X."}, {"id": "z", "statement": "Z."}]

    def fake(state, questions):
        rid = state["rule"]["id"]
        ans = {}
        for k in questions:
            pair = {rid, k}
            p = {"conflicting": 0.8, "independent": 0.2} if pair == {"x", "y"} else {"independent": 0.9, "conflicting": 0.1}
            ans[k] = {"choice": max(p, key=p.get), "probabilities": p}
        return {"answers": ans}
    monkeypatch.setattr(rh, "call_state", fake)
    out = rh.relations(registry)
    assert len(out["problems"]) == 1 and out["problems"][0].startswith("x and y: conflicting")
    registry[0]["relations"] = [{"rule": "y", "relation": "independent", "reason": "different pages"}]
    assert rh.relations(registry)["problems"] == []


def test_recorded_relations_cover_every_rule_and_are_resolved(monkeypatch):
    """Every pair of registered rules has a recorded answer, and no unresolved pair blocks."""
    monkeypatch.setenv("JEV_REPLAY", str(rh.RELATIONS_FIXTURES))
    monkeypatch.delenv("JEV_RECORD", raising=False)
    out = rh.relations(rh.load_registry())
    assert out["problems"] == []


def test_choice_overlap_and_catalog_are_clean_for_this_repo(monkeypatch):
    monkeypatch.setenv("JEV_REPLAY", str(HERE / "fixtures/jev"))
    specs, labels = rh.judge.load_specs(), rh.load_labels()
    assert rh.catalog(specs, labels)["problems"] == []
    assert rh.overlap(specs, labels)["problems"] == []


@pytest.mark.skipif(not (shutil.which("vale") or (Path.home() / ".local/bin/vale").is_file()), reason="needs Vale")
def test_crossfire_finds_a_pass_line_another_rule_breaks():
    fixture = rh.TESTS / "zz-crossfire-probe.md"
    fixture.write_text("<!-- rules: Sensible.Numbers -->\n\n# Test\n\nThe score is 90% — split this. <!-- pass -->\n")
    try:
        out = rh.crossfire(rh.load_registry(), [fixture])
    finally:
        fixture.unlink()
    assert [c for _, _, _, c in out["contradictions"]] == ["Sensible.EmDash"]


@pytest.mark.skipif(not (shutil.which("vale") or (Path.home() / ".local/bin/vale").is_file()), reason="needs Vale")
def test_crossfire_is_clean_for_this_repo():
    assert rh.crossfire(rh.load_registry())["problems"] == []
