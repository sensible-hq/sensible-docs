"""Tests for weekly_cleanup.py's reports, from a recorded run's results (no Jev, no Vale)."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import report_html  # noqa: E402
import rule_hygiene as rh  # noqa: E402
import weekly_cleanup as w  # noqa: E402

RESULTS = json.loads((HERE / "fixtures/weekly/results.json").read_text())


def test_drift_is_a_precision_drop_or_a_trust_change():
    base = {"rule": "r", "stored_precision": 1.0, "stored_recall": 0.5, "precision": 1.0, "recall": 0.83,
            "trusted": True, "stored_trusted": True}
    results = {**RESULTS, "calibration": [{**base, "drift": False}], "relations": {"problems": [], "pairs": {}},
               "overlap": {"problems": [], "rows": []}, "catalog": {"problems": [], "copied": []},
               "crossfire": {"problems": [], "contradictions": [], "overlaps": []}}
    assert w.problems(results) == []
    results["calibration"] = [{**base, "precision": 0.8, "trusted": False, "drift": True}]
    assert w.problems(results) == ["calibration drift: r precision 1.0 → 0.8, recall 0.5 → 0.83, no longer trusted"]


def test_summary_links_the_report_and_the_issue_names_the_week():
    text = w.summary(RESULTS, "https://example.test/report", "https://example.test/run")
    assert "[Open the full HTML report](https://example.test/report)" in text and "Labels not yet reviewed" in text


def test_html_report_is_standalone_in_the_house_style():
    html_text = w.render_html(RESULTS, rh.load_registry())
    assert report_html.CSS in html_text and "<script src" not in html_text
    for section in ("Calibration", "Docs corpus", "Choice catalog", "Rule relations", "Labels to review"):
        assert section in html_text
