import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import classify as C  # noqa: E402


def test_parse_hunks_splits_per_hunk_and_skips_non_doc_files():
    diff = "\n".join([
        "diff --git a/docs/a.md b/docs/a.md", "--- a/docs/a.md", "+++ b/docs/a.md",
        "@@ -1 +1 @@", "-old one", "+new one",
        "@@ -5,0 +6,2 @@", "+added a", "+added b",
        "diff --git a/scripts/x.py b/scripts/x.py", "--- a/scripts/x.py", "+++ b/scripts/x.py",
        "@@ -1 +1 @@", "-a", "+b",
        "diff --git a/docs/gone.md b/docs/gone.md", "--- a/docs/gone.md", "+++ /dev/null",
        "@@ -1 +0,0 @@", "-bye",
    ])
    assert C.parse_hunks(diff) == [
        ("docs/a.md", ["old one"], ["new one"]),
        ("docs/a.md", [], ["added a", "added b"]),
        ("docs/gone.md", ["bye"], []),
    ]


@pytest.mark.parametrize("before, after, expected", [
    ("", "New paragraph.", "addition"),
    ("Old paragraph.", "  ", "deletion"),
    ("Use **bold** here", "Use *bold* here", "formatting"),
    ("```json", "```text", "formatting"),
    ('"content": {x', '"content": {', "typo"),
    ("a example", "an example", "typo"),
    ("| TIFF | ✅ |", "| TIFF | ❌ |", None),          # one character, but a different value
    ("Gemini 2.5 Flash", "Gemini 3.1 Flash", None),   # digits stay with Jev
    ("the min value", "the max value", None),         # a replacement, not a typo
    ("teh value", "the value", "typo"),               # a transposition is one deletion plus one insertion
    ("Before.", "Completely different after.", None),
])
def test_precheck(before, after, expected):
    assert C.precheck(before, after) == expected


def answers(contra, same, adds, drops):
    return {"contradicts": contra, "same_meaning": same, "adds_information": adds, "drops_information": drops}


@pytest.mark.parametrize("a, expected", [
    (answers(0.9, 0.9, 0.1, 0.1), "factual"),        # contradiction wins even when wording is close
    (answers(0.5, 0.8, 0.1, 0.1), "copy_edit"),
    (answers(0.1, 0.2, 0.9, 0.1), "elaboration"),
    (answers(0.1, 0.2, 0.1, 0.9), "deletion"),
    (answers(0.1, 0.2, 0.9, 0.9), "rewrite"),
    (answers(0.1, 0.5, 0.5, 0.5), "unsettled"),
    (answers(0.5, 0.2, 0.9, 0.5), "unsettled"),
    (answers(0.1, 0.2, 0.2, 0.2), "unsettled"),
])
def test_decide_covers_every_row(a, expected):
    assert C.decide(a) == expected


def test_decide_is_total_over_a_grid():
    grid = [0.0, 0.3, 0.5, 0.7, 1.0]
    for c in grid:
        for s in grid:
            for ad in grid:
                for d in grid:
                    assert C.decide(answers(c, s, ad, d)) in C.CLASSES


def test_questions_are_all_nouls_and_match_hunk_fields():
    assert all(q["type"] == "noul" for q in C.QUESTIONS.values())
    fields = C.Hunk.__dataclass_fields__
    assert all(k in fields for k in C.QUESTIONS)


def test_clip_flags_truncation():
    text, cut = C.clip("x" * (C.MAX_SIDE_CHARS + 1))
    assert cut and len(text) == C.MAX_SIDE_CHARS
    assert C.clip("short") == ("short", False)


def test_replay_without_recording_raises(tmp_path, monkeypatch):
    monkeypatch.setenv("JEV_REPLAY", str(tmp_path))
    h = C.Hunk(pr=1, period="after", commit="abc", claude=True, path="docs/a.md",
               before="The default is five.", after="The default is ten pages.", lines=2)
    with pytest.raises(C.jev.JevUnavailable):
        C.classify([h])
