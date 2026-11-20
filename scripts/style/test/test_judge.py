"""Tests for the Jev judge, offline: every Jev answer comes from a recorded response."""
import os
import sys
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import calibrate  # noqa: E402
import jev  # noqa: E402
import judge  # noqa: E402

REF = judge.ROOT / "docs/Senseml reference"
PAGES = [REF / "layout-based-methods/region.md", REF / "advanced-computed-field-methods/extra-data.md",
         REF / "config-settings/fingerprint.md", REF / "advanced-computed-field-methods/copy-to-section.md"]


@pytest.fixture
def replay(monkeypatch):
    def use(name):
        monkeypatch.setenv("JEV_REPLAY", str(HERE / "fixtures" / name))
        monkeypatch.delenv("JEV_RECORD", raising=False)
    return use


def test_missing_recording_fails_closed(replay, tmp_path, monkeypatch):
    monkeypatch.setenv("JEV_REPLAY", str(tmp_path))
    with pytest.raises(jev.JevUnavailable):
        jev.call("text", {"q": jev.choice_question("ask", {"a": "x"})})


def test_sentences_keep_line_numbers():
    page = judge.parse("---\ntitle: T\n---\nFirst one. Second one\nwraps here. Third.\n\n## H\n\nFourth.\n")
    prose = [b for b in page["blocks"] if b["kind"] == "prose"]
    assert judge.sentences(prose[0]) == [(4, "First one."), (4, "Second one\nwraps here."), (5, "Third.")]
    assert page["title"] == "T" and judge.sentences(prose[1]) == [(9, "Fourth.")]


def test_verdicts():
    spec = {"check": {"verdicts": {"violation": ["bad"], "review": ["maybe"]}}}
    assert judge.verdict(spec, {"choice": "bad", "confidence": 0.9}) == "violation"
    assert judge.verdict(spec, {"choice": "bad", "confidence": 0.5}) == "unsure"
    assert judge.verdict(spec, {"choice": "maybe", "confidence": 0.9}) == "review"
    assert judge.verdict(spec, {"choice": "good", "confidence": 0.9}) == "ok"


def test_trust_needs_precision_recall_and_enough_cases():
    good = {"precision": 1.0, "recall": 0.6, "cases": 8, "violations": 5}
    assert judge.trusted({"calibration": good})
    assert not judge.trusted({"calibration": {**good, "precision": 0.8}})
    assert not judge.trusted({"calibration": {**good, "recall": 0.4}})
    assert not judge.trusted({"calibration": {**good, "cases": 4}})
    assert not judge.trusted({"calibration": {**good, "violations": 2}})
    assert not judge.trusted({})


def test_judge_on_real_pages(replay):
    replay("jev-pages")
    out = judge.judge(PAGES, judge.load_specs())
    got = {(Path(r["path"]).name, r["rule"]): r["verdict"] for r in out["results"]}
    assert got[("extra-data.md", "sensible-opening-sentence")] == "review"
    assert got[("region.md", "sensible-opening-sentence")] == "ok"
    assert not any(r["verdict"] == "violation" and r.get("trusted") for r in out["results"])


def test_section_openers_skip_parameter_sections():
    spec = judge.load_specs({"sensible-scenario-first"})["sensible-scenario-first"]
    page = judge.parse(PAGES[2].read_text())
    cands, _ = judge.find_candidates(spec, PAGES[2], page, None)
    assert not any("contains a Tests parameter" in c["text"] for c in cands)


def test_diff_detectors(monkeypatch, tmp_path):
    page_text = ("# T\n\nIntro.\n\n### New thing\n\nOne sentence about it.\n\n## Modes\n\n"
                 "| Mode | Meaning |\n| --- | --- |\n| a | b |\n")
    f = judge.ROOT / "docs" / "zz-judge-test.md"
    monkeypatch.setattr(judge, "added_lines", lambda path, base: set(range(5, 14)) if base else None)
    try:
        f.write_text(page_text)
        page = judge.parse(page_text)
        specs = judge.load_specs({"sensible-integrate-before-heading", "sensible-no-table-for-unconfigurable"})
        heads, _ = judge.find_candidates(specs["sensible-integrate-before-heading"], f, page, "v0")
        tables, _ = judge.find_candidates(specs["sensible-no-table-for-unconfigurable"], f, page, "v0")
        _, why = judge.find_candidates(specs["sensible-no-table-for-unconfigurable"], f, page, None)
    finally:
        f.unlink()
    assert [c["line"] for c in heads] == [5]
    assert [c["line"] for c in tables] == [11]
    assert why == "needs --base"


def test_calibration_in_specs_matches_the_recordings(replay):
    """The calibration numbers stored in each spec come from the recorded responses."""
    replay("jev")
    for rid, spec in judge.load_specs().items():
        labels = calibrate.LABELS / f"{rid}.yaml"
        if not labels.exists():
            continue
        res = calibrate.calibrate(rid, spec, yaml.safe_load(labels.read_text())["cases"])
        cal = spec["calibration"]
        assert (res["precision"], res["recall"], res["cases"]) == (cal["precision"], cal["recall"], cal["cases"]), rid
