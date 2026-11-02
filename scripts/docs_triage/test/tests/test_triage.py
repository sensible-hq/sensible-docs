"""Tests for scripts/docs_triage/triage.py (offline: no GitHub or Jev calls)."""

import pytest

import triage


class TestCriteria:
    def test_loads_every_trigger_and_exclusion(self):
        crit = triage.load_criteria()
        assert {"T-config", "T-behavior", "T-api", "T-inputs", "T-models", "T-output",
                "X-internal", "X-hidden"} == set(crit)

    def test_ignores_prose_lines(self, tmp_path):
        p = tmp_path / "c.md"
        p.write_text("# Title\n\nSome prose.\n- [T-a] Question one?\n- not a criterion\n")
        assert triage.load_criteria(p) == {"T-a": "Question one?"}


class TestNeedsTriage:
    def test_one_trigger_flags(self):
        assert triage.needs_triage({"T-config": 0.9, "T-api": 0.1, "X-internal": 0.1})

    def test_exclusion_wins(self):
        assert not triage.needs_triage({"T-config": 0.9, "X-internal": 0.8})

    def test_below_threshold_passes(self):
        assert not triage.needs_triage({"T-config": 0.69, "X-internal": 0.0})

    def test_threshold_is_inclusive(self):
        assert triage.needs_triage({"T-config": 0.7, "X-hidden": 0.0})


class TestBuildState:
    PR = {"number": 1, "title": "Add foo", "body": "Adds foo.\nReviewer: labeled doc_changes_needed\nDone."}

    def test_redacts_label_mentions(self):
        state = triage.build_state(self.PR, [], [])
        assert "doc_changes_needed" not in state
        assert "Adds foo." in state and "Done." in state

    def test_omits_goldens_and_lockfiles(self):
        files = [{"filename": "extractors/x/y/goldens/a.pdf.extracted.json", "patch": "GOLDEN"},
                 {"filename": "pnpm-lock.yaml", "patch": "LOCK"},
                 {"filename": "src/engine/methods/foo.ts", "patch": "+code"}]
        state = triage.build_state(self.PR, files, [])
        assert "GOLDEN" not in state and "LOCK" not in state and "+code" in state
        assert "3; 2 golden/cache/lock files omitted" in state

    def test_schema_diff_comes_first(self):
        files = [{"filename": "src/api/x.ts", "patch": "+api_patch"},
                 {"filename": "src/engine/__generated__/configuration.schema.json", "patch": "+schema_patch"}]
        state = triage.build_state(self.PR, files, [])
        assert state.index("+schema_patch") < state.index("+api_patch")

    def test_respects_budget(self):
        files = [{"filename": f"src/engine/f{i}.ts", "patch": "x" * 5000} for i in range(10)]
        state = triage.build_state(self.PR, files, [], budget=6000)
        assert state.count("x") <= 6000 + 50


class TestPublicEndpoints:
    def test_reads_published_specs(self):
        eps = triage.public_endpoints()
        assert "POST /extract/{document_type}" in eps
        assert not any(e.startswith("PARAMETERS") for e in eps)


class TestCandidate:
    def test_skips_prs_with_a_docs_decision(self):
        for label in triage.DOCS_LABELS:
            assert not triage.candidate({"labels": [{"name": label}], "user": {"login": "someone"}})

    def test_skips_bots(self):
        assert not triage.candidate({"labels": [], "user": {"login": "dependabot[bot]"}})

    def test_keeps_unlabeled_human_prs(self):
        assert triage.candidate({"labels": [{"name": "bug"}], "user": {"login": "someone"}})


class TestJev:
    def test_fails_closed_without_key(self, monkeypatch):
        monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
        with pytest.raises(triage.JevUnavailable):
            triage.ask_jev("state", {"T-a": "q"})
