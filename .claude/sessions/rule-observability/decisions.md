# Rule observability decisions

## RO-001 The weekly Jev cleanup runs in GitHub Actions and opens an issue

Frances's call (2026-11-18). `TYPESAFE_API_KEY` is a repo secret. One standing issue labeled `style-weekly` gets a comment per run.

## RO-002 Usage comes from local agent transcripts, and only the derived scores are committed

Frances's call (2026-11-18): she prefers agent logs over a log the hook writes. Transcripts last 30 days, so a weekly run loses nothing, and the weekly JSON in `style-rules/usage/` keeps the history. Transcripts never leave her machine.

## RO-003 Every report is a standalone HTML artifact, like the doc tests

Frances's call (2026-11-18). Each workflow copies one self-contained `report.html` to `$RUNNER_TEMP/<name>-report.html`, uploads it with `actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` (v7.0.1) and `archive: false`, and links the artifact URL from `$GITHUB_STEP_SUMMARY`. The weekly issue links it too. The usage report renders in a workflow triggered by a push of the weekly JSON. The CSS is imported from `scripts/doc-detective/codetests/reports/html.py`, so a style change there reaches every report.

## RO-004 "Without labeling" means a new rule is blocked until it's registered, labeled, and checked against the others

Reading of Frances's "not allowed to add new rules w/ labeling/adding them to registry AND testing them for duplication/contradiction". The gate (`new_rule_gate.py`) runs in CI through pytest.

## RO-005 Enforcement is derived, not stored

The hierarchy needs an enforcement column, but `enforced_by` already says it. A stored copy would be one more field to drift, so `rule_map.enforcement()` computes it. Scope is stored, because nothing else says it.

## RO-006 Three scopes

`general` (every page), `page-type` (one kind of page: changelog, blog, integration guide, reference), `construct` (one element, term, or parameter). More levels would need a judgment call per rule that nobody could check.

## RO-007 Rule relations are judged from the statements, by Jev, one request per rule

Jev reads the rule's statement and every other statement, and answers one choice question per other rule. Code decides what a `conflicting` or `same-requirement` answer blocks. Comparing statements, not examples, because every rule has a statement and only some have examples. A pair can be marked resolved in the registry (`relations: [{rule, relation, reason}]`).

## RO-008 A copied label case doesn't count

A label whose text appears in the spec's own criteria or examples tests the wording it was copied from. The catalog lint lists them. For existing rules they're reported, not removed, so trust doesn't change overnight; a new rule fails the gate if it has any.

## RO-009 Fixture cross-fire uses gating rules only

Pass lines are short and often trip suggestion-level Google rules (Passive, Acronyms) that don't gate anything. Only Sensible and Google rules with registry gate `block` or `warn` count as a contradiction.

## RO-010 Transcript projects: sensible-docs and its worktrees only

`~/.claude/projects/-home-franc-GitHub-sensible-docs` and `-home-franc-GitHub-sensible-docs-<branch>`, except `-gen*`, `-sandbox`, and `-private*`, which are other repos. Subagent transcripts (`<session>/subagents/*.jsonl`) count.

## RO-011 The "Vale: N alert(s) in the docs this PR changes" hook isn't in any repo

It fired on every Bash call in session `1e71441a` (the xlsb worktree, now deleted) and produced most of the 566 WordList mentions. No copy remains in this repo's history, `~/.claude`, or the other worktrees, so it can't be fixed here. The usage parser counts its alerts once per session.
