"""Tests for scripts/docs_triage/triage.py (offline: no GitHub or Jev calls)."""

import pytest

import triage

TRIGGERS = ("T-config", "T-behavior", "T-api", "T-inputs", "T-models", "T-output")
EXCLUSIONS = ("X-internal", "X-hidden", "X-bugfix", "X-in-progress", "X-customer")


def scores(**overrides) -> dict:
    """Build a full score dict: every question at 0.05 except the ones given.

    Keyword names use `_` for `-`, so `T_config=0.95` sets `T-config`.
    """
    out = {k: 0.05 for k in TRIGGERS + EXCLUSIONS}
    out.update({k.replace("_", "-"): v for k, v in overrides.items()})
    return out


class TestCriteria:
    """load_criteria reads criteria.md."""

    def test_loads_every_trigger_and_exclusion(self):
        """criteria.md has exactly the questions decide expects."""
        assert set(triage.load_criteria()) == set(TRIGGERS + EXCLUSIONS)

    def test_ignores_prose_lines(self, tmp_path):
        """Headings, prose, and bullets without an id aren't questions."""
        p = tmp_path / "c.md"
        p.write_text("# Title\n\nSome prose.\n- [T-a] Question one?\n- not a criterion\n- **bold** rule\n")
        assert triage.load_criteria(p) == {"T-a": "Question one?"}

    def test_confident_triggers_and_hard_exclusions_exist(self):
        """Every id the decision rule names is a real question."""
        crit = triage.load_criteria()
        assert set(triage.CONFIDENT_TRIGGERS + triage.HARD_EXCLUSIONS) <= set(crit)


class TestDecide:
    """decide maps scores to docs_needed_ai, docs_triage_ai, or no label."""

    def test_confident_config_change_is_needed(self):
        """A clear new SenseML setting with no exclusion earns docs_needed_ai."""
        assert triage.decide(scores(T_config=0.95)) == triage.NEEDED

    def test_needed_threshold_is_inclusive(self):
        """A confident trigger at exactly 0.90 is enough."""
        assert triage.decide(scores(T_inputs=0.90)) == triage.NEEDED

    def test_less_precise_trigger_only_triages(self):
        """T-api alone never earns docs_needed_ai, however high it scores."""
        assert triage.decide(scores(T_api=0.99)) == triage.TRIAGE

    def test_soft_exclusion_demotes_to_triage(self):
        """A likely bug fix, WIP, hidden, or one-customer PR goes to a human, not to no label."""
        for x in ("X_hidden", "X_bugfix", "X_in_progress", "X_customer"):
            assert triage.decide(scores(T_config=0.95, **{x: 0.8})) == triage.TRIAGE, x

    def test_any_exclusion_at_clear_blocks_needed(self):
        """docs_needed_ai needs every exclusion below 0.30, not just below 0.70."""
        assert triage.decide(scores(T_config=0.95, X_bugfix=0.30)) == triage.TRIAGE

    def test_internal_rules_out(self):
        """A PR Jev calls internal-only gets no label, even with a high trigger."""
        assert triage.decide(scores(T_config=0.95, X_internal=0.8)) is None

    def test_below_threshold_gets_nothing(self):
        """No trigger at 0.70 means no label."""
        assert triage.decide(scores(T_config=0.69)) is None

    def test_triage_threshold_is_inclusive_and_adjustable(self):
        """A trigger at exactly the threshold triages; --threshold moves the bar."""
        assert triage.decide(scores(T_output=0.70)) == triage.TRIAGE
        assert triage.decide(scores(T_output=0.70), triage_threshold=0.8) is None


class TestBuildState:
    """build_state assembles the text Jev judges."""

    PR = {"number": 1, "title": "Add foo", "body": "Adds foo.\nReviewer: labeled doc_changes_needed\nDone."}

    def test_redacts_label_mentions(self):
        """Lines naming a docs label are dropped; the rest of the description stays."""
        state = triage.build_state(self.PR, [], [])
        assert "doc_changes_needed" not in state
        assert "Adds foo." in state and "Done." in state

    def test_redacts_ai_labels_too(self):
        """The script's own labels count as label mentions."""
        assert "docs_needed_ai" not in triage.redact("see docs_needed_ai\nkeep")

    def test_omits_goldens_and_lockfiles(self):
        """Golden outputs and lockfiles are counted but not shown."""
        files = [{"filename": "extractors/x/y/goldens/a.pdf.extracted.json", "patch": "GOLDEN"},
                 {"filename": "pnpm-lock.yaml", "patch": "LOCK"},
                 {"filename": "src/engine/methods/foo.ts", "patch": "+code"}]
        state = triage.build_state(self.PR, files, [])
        assert "GOLDEN" not in state and "LOCK" not in state and "+code" in state
        assert "3; 2 golden/cache/lock files omitted" in state

    def test_schema_diff_comes_first(self):
        """The config schema's diff is shown before API code, whatever the file order."""
        files = [{"filename": "src/api/x.ts", "patch": "+api_patch"},
                 {"filename": "src/engine/__generated__/configuration.schema.json", "patch": "+schema_patch"}]
        state = triage.build_state(self.PR, files, [])
        assert state.index("+schema_patch") < state.index("+api_patch")

    def test_respects_budget(self):
        """The diff excerpt stops at the character budget."""
        files = [{"filename": f"src/engine/f{i}.ts", "patch": "x" * 5000} for i in range(10)]
        state = triage.build_state(self.PR, files, [], budget=6000)
        assert state.count("x") <= 6000 + 50

    def test_missing_patch_is_noted(self):
        """Files GitHub sends without a patch are marked, not skipped silently."""
        state = triage.build_state(self.PR, [{"filename": "src/engine/big.ts"}], [])
        assert "(no patch: binary or too large)" in state


class TestPublicEndpoints:
    """public_endpoints reads the published OpenAPI specs."""

    def test_reads_published_specs(self):
        """Real operations are listed; path-level `parameters` entries aren't."""
        eps = triage.public_endpoints()
        assert "POST /extract/{document_type}" in eps
        assert not any(e.startswith("PARAMETERS") for e in eps)


class TestCandidate:
    """candidate decides which merged PRs get scored."""

    def test_skips_prs_with_a_docs_label(self):
        """A PR with any docs label, human or AI, isn't scored again."""
        for label in triage.DOCS_LABELS:
            assert not triage.candidate({"labels": [{"name": label}], "user": {"login": "someone"}}), label

    def test_skips_bots(self):
        """Dependabot PRs aren't scored."""
        assert not triage.candidate({"labels": [], "user": {"login": "dependabot[bot]"}})

    def test_keeps_unlabeled_human_prs(self):
        """A human PR with only unrelated labels is scored."""
        assert triage.candidate({"labels": [{"name": "bug"}], "user": {"login": "someone"}})


class TestJev:
    """ask_jev's failure handling."""

    def test_fails_closed_without_key(self, monkeypatch):
        """With no API key, Jev is unavailable; the script never guesses a score."""
        monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
        with pytest.raises(triage.JevUnavailable):
            triage.ask_jev("state", {"T-a": "q"})
