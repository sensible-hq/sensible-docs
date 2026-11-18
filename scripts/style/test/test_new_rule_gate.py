"""Tests for new_rule_gate.py: which rules count as new, and what blocks them. Offline (recordings)."""
import sys
from pathlib import Path

import shutil

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import new_rule_gate as gate  # noqa: E402
import rule_hygiene as rh  # noqa: E402


def base_without(*ids):
    registry = rh.load_registry()
    return {"ids": {r["id"] for r in registry} - set(ids),
            "vale": {v for r in registry for v in (r.get("enforced_by") or {}).get("vale") or []},
            "specs": {s for r in registry for s in (r.get("enforced_by") or {}).get("judgment") or []}}


@pytest.fixture
def replay(monkeypatch):
    monkeypatch.delenv("JEV_RECORD", raising=False)
    monkeypatch.delenv("JEV_REPLAY", raising=False)


def test_nothing_new_passes(monkeypatch, replay):
    monkeypatch.setattr(gate, "base_state", lambda base: base_without())
    assert gate.run("base") == {}


def test_a_new_vale_rule_or_spec_counts_as_new():
    registry = [{"id": "a", "enforced_by": {"vale": ["Sensible.New"]}}, {"id": "b", "enforced_by": {"judgment": ["style-rules/judgment/b.yaml"]}},
                {"id": "c", "enforced_by": {"vale": ["Google.Passive"]}}]
    base = {"ids": {"a", "b", "c"}, "vale": set(), "specs": set()}
    assert [r["id"] for r in gate.new_rules(registry, base)] == ["a", "b"]


@pytest.mark.skipif(not (shutil.which("vale") or (Path.home() / ".local/bin/vale").is_file()), reason="needs Vale (cross-fire)")
def test_a_judgment_rule_with_copied_labels_is_blocked(monkeypatch, replay):
    """sensible-filler's labels include its spec's own examples, so as a new rule it wouldn't pass."""
    monkeypatch.setattr(gate, "base_state", lambda base: base_without("sensible-filler"))
    problems = gate.run("base")["sensible-filler"]
    assert any("copied from the spec" in p for p in problems)


def test_a_prose_rule_without_a_relations_recording_is_blocked(monkeypatch, replay):
    registry = rh.load_registry()
    registry.append({"id": "sensible-test-new", "statement": "Write every heading in sentence case.", "kind": "prose",
                     "scope": "general", "stated_in": [{"file": "x.md", "quote": "q"}]})
    monkeypatch.setattr(rh, "load_registry", lambda: registry)
    monkeypatch.setattr(gate, "base_state", lambda base: base_without("sensible-test-new"))
    monkeypatch.setattr(gate.check_registry, "check", lambda reg: [])
    problems = gate.run("base")["sensible-test-new"]
    assert any("no recorded relations check" in p for p in problems)


def test_this_branchs_new_prose_rules_pass(monkeypatch, replay):
    """The prose rules registered from the reference style guides have their relations recorded."""
    monkeypatch.setattr(gate, "base_state", lambda base: base_without("sensible-jump-links", "sensible-null-behavior"))
    assert gate.run("base") == {"sensible-jump-links": [], "sensible-null-behavior": []}
