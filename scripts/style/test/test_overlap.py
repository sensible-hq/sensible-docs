"""Tests for scripts/style/check_overlap.py and the .claude/hooks/rule_gate.py hook."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts/style"))
import check_overlap as co  # noqa: E402

A = {"id": "rule-a", "statement": "Don't use em dashes in prose.", "applies": ["prose"]}
B = {"id": "rule-b", "statement": "Never use em dashes in prose text.", "overrides": ["rule-c"], "applies": ["prose"]}
C = {"id": "rule-c", "statement": "Use an em dash between a term and its definition.", "applies": ["prose"]}
D = {"id": "rule-d", "statement": "Fence code as json.", "applies": ["code"]}
P = {"id": "rule-p", "statement": "Register every page.", "applies": ["whole-page"]}


def test_pair_hash_ignores_order_and_tracks_wording():
    assert co.pair_hash(A, B) == co.pair_hash(B, A)
    assert co.pair_hash(A, B) != co.pair_hash({**A, "statement": "Avoid em dashes."}, B)


def test_settled_pair_reopens_when_a_statement_changes(tmp_path, monkeypatch):
    by_id = {r["id"]: r for r in (A, B)}
    f = tmp_path / "overlaps.yaml"
    f.write_text(f"- pair: [rule-b, rule-a]\n  verdict: distinct\n  hash: {co.pair_hash(A, B)}\n")
    monkeypatch.setattr(co, "SETTLED", f)
    settled, stale = co.load_settled(by_id)
    assert ("rule-a", "rule-b") in settled and not stale
    settled, stale = co.load_settled({**by_id, "rule-a": {**A, "statement": "Avoid em dashes."}})
    assert not settled and "statement changed" in stale[0]


def test_wording_finds_restatements_only():
    found = co.wording_findings({r["id"]: r for r in (A, B, C)})
    assert [(a, b) for a, b, *_ in found] == [("rule-a", "rule-b")]


def test_jev_layer_averages_both_orders_and_flags_unstable(monkeypatch):
    def fake(first, second):
        same = 0.9 if first["id"] == "rule-a" else 0.2  # order flips the answer
        return {"same": same, "conflict": 0.1}
    monkeypatch.setattr(co, "ask", fake)
    found = co.jev_findings({r["id"]: r for r in (A, B)}, workers=1)
    assert [f[2] for f in found] == ["unstable duplicate"]


def test_override_silences_contradiction(tmp_path, monkeypatch, capsys):
    reg = tmp_path / "registry.yaml"
    reg.write_text(json.dumps([A, B, C]))
    monkeypatch.setattr(co, "REGISTRY", reg)
    monkeypatch.setattr(co, "SETTLED", tmp_path / "none.yaml")
    monkeypatch.setattr(co, "ask", lambda f, s: {"same": 0.1, "conflict": 0.9})
    co.main(["--jev", "--no-fixtures", "--rules", "rule-b,rule-c", "--cache", str(tmp_path / "c.json")])
    assert "Nothing to review." in capsys.readouterr().out


def test_only_rules_that_share_text_are_compared():
    pairs = co.candidate_pairs({r["id"]: r for r in (A, D, P)})
    assert pairs == [("rule-a", "rule-p"), ("rule-d", "rule-p")]


def test_cached_answers_are_reused_until_a_rule_changes(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(co, "ask", lambda f, s: calls.append(1) or {"same": 0.1, "conflict": 0.1})
    cache, stats = tmp_path / "c.json", {}
    rules = {r["id"]: r for r in (A, B)}
    co.jev_findings(rules, workers=1, cache_path=cache, stats=stats)
    co.jev_findings(rules, workers=1, cache_path=cache, stats=stats)
    assert len(calls) == 2 and stats["cached"] == 2
    co.jev_findings({**rules, "rule-a": {**A, "statement": "Avoid em dashes."}}, workers=1, cache_path=cache)
    assert len(calls) == 4


def hook(path: Path) -> subprocess.CompletedProcess:
    event = {"hook_event_name": "PostToolUse", "tool_input": {"file_path": str(path)}}
    return subprocess.run([sys.executable, str(REPO / ".claude/hooks/rule_gate.py")], input=json.dumps(event),
                          capture_output=True, text=True)


def test_hook_ignores_files_that_carry_no_rules():
    assert hook(REPO / "docs/README.md").returncode == 0
    assert hook(REPO / ".claude/sessions/x/checklist.md").returncode == 0


def test_hook_passes_a_clean_carrier():
    r = hook(REPO / "CLAUDE.md")
    assert r.returncode == 0, r.stderr
