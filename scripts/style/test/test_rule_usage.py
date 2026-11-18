"""Tests for rule_usage.py, on a synthetic transcript."""
import datetime
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import rule_usage as u  # noqa: E402

PROJ = HERE / "fixtures/transcripts/-home-x-GitHub-sensible-docs"
NOW = datetime.datetime(2026, 11, 18, tzinfo=datetime.timezone.utc)


def test_project_dirs_skip_other_repos(tmp_path):
    for name in ("-home-x-GitHub-sensible-docs", "-home-x-GitHub-sensible-docs-xlsb", "-home-x-GitHub-sensible-docs-gen",
                 "-home-x-GitHub-sensible-docs-gen-m2", "-home-x-GitHub-sensible-docs-sandbox", "-home-x-GitHub-sensible-docs-private-test"):
        (tmp_path / name).mkdir()
    assert [d.name for d in u.project_dirs(tmp_path)] == ["-home-x-GitHub-sensible-docs", "-home-x-GitHub-sensible-docs-xlsb"]


def test_collect_dedupes_and_scores_outcomes():
    os.utime(PROJ / "s1.jsonl", (NOW.timestamp(), NOW.timestamp()))
    data = u.collect("2026-W47", [PROJ], None, now=NOW)
    assert data["sessions"] == 1 and data["guide_reads"] == {"writing-rules.md": 1}
    by = {f["check"]: f for f in data["firings"]}
    assert len(data["firings"]) == 2  # the Acronyms alert appears 5 times in the transcript
    assert by["Sensible.EmDash"]["source"] == "deny" and by["Sensible.EmDash"]["outcome"] == "acted"
    assert by["Sensible.EmDash"]["pushback"]  # "put it back" follows the fix
    assert by["Google.Acronyms"]["outcome"] == "ignored"  # still reported after the last edit
    assert data["rules"]["sensible-em-dash"]["firings"] == 1


def test_the_committed_file_has_no_message_text():
    os.utime(PROJ / "s1.jsonl", (NOW.timestamp(), NOW.timestamp()))
    data = u.collect("2026-W47", [PROJ], None, now=NOW)
    local = data.pop("_local")
    text = json.dumps(data)
    assert "put it back" not in text and "please write" not in text and "JPEG" not in text
    assert local and "put it back" in local[0]["pushback_text"]


def test_report_renders_weeks():
    os.utime(PROJ / "s1.jsonl", (NOW.timestamp(), NOW.timestamp()))
    data = u.collect("2026-W47", [PROJ], None, now=NOW)
    data.pop("_local")
    html_text = u.render_html([data])
    assert "Rules that fired" in html_text and "sensible-em-dash" in html_text
    assert "Latest week 2026-W47" in u.summary([data], None)


def test_default_week_is_the_last_complete_one():
    assert u.week_bounds(None, NOW)[0] == "2026-W46"  # NOW is Wednesday of W47
    name, start, end = u.week_bounds("2026-W47")
    assert (name, start.date().isoformat(), end.date().isoformat()) == ("2026-W47", "2026-11-16", "2026-11-23")
