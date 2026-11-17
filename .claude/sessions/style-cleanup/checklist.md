# Style cleanup checklist

Session: style-cleanup (Claude Code session `cec011d3-0e56-45f1-aa31-0fc712c29141`)
Worktree: `~/GitHub/sensible-docs-style-cleanup`, branch `style-cleanup`, stacked on `style-map` (PR #808)
Plan: `design/style-cleanup/implementation-plan.md`

- [x] M0 Baseline corpus counts (`style-rules/corpus-before.tsv`)
- [x] M1 Fixture test harness (`scripts/style/test_rules.py`)
- [x] M2 Fix existing Vale rules: AgainstPhrasing, WordList, EmDash
- [x] M3 New Vale rules: 15 added; rejected candidates in D-012
- [x] M4 Registry and `check_registry.py`
- [x] M5 Guide and skill edits, with markers
- [x] M6 Scripts: code blocks, excerpts, `_order.yaml`, parameter wording detector
- [x] M7 Write-time hook `vale_gate.py`; doctor updated
- [x] M8 Judgment specs (12)
- [x] M9 Corpus counts after, progress table, PR

Open, for Frances:

- [ ] Review the contradiction resolutions in the guides (D-numbers in `decisions.md`; the map's C1–C9)
- [ ] Decide on D-013 (pre-write hook) against the `vale-setup` memory
- [ ] Apply or reject the proposed memory edits
- [ ] Pick backlog fixes from `progress.md`
- [ ] When #808 merges: rebase this branch onto `v0` and retarget the PR
