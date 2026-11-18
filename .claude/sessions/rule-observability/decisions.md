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

## RO-012 Weekly usage files hold counts only

The repo is public. `style-rules/usage/<week>.json` holds rule ids, docs paths, sources, and outcomes. Frances's messages and the agent's text never leave her machine; the pushback excerpts appear only in the local report the skill opens.

## RO-013 Usage is collected per ISO week, Monday to Sunday UTC

A rolling "last 7 days" would overlap from one run to the next. The default is the last complete week; `--week` backfills any week still within the 30-day transcript window. W42 to W46 were backfilled; W41 had no sessions left.

## RO-014 The hook reports each alert once per session

Keyed by rule, message, and the text of the flagged line, so an edit that moves the line doesn't bring the alert back. The report adds a count of alerts still open. A false positive Claude chose to keep stops costing a re-read after every edit; a new session hears about it again.

## RO-015 "Email" leaves Google.WordListCase

The entry `(?:e-mail|Email|E-mail)` with `ignorecase: true` flagged every capitalized "Email" at the start of a sentence, table cell, or bold label (file-types.md had 3). The entry now targets the hyphenated forms only. A mid-sentence "Email" is no longer caught; that's rarer than the false positive.

## RO-016 The judge gates on probability, not confidence

TypeSafe's guidance: confidence measures how concentrated an answer is, not whether it's right. A violation is now the violation choices' probabilities summing to 0.70; unsure from 0.30 or when the top choice is a violation. Recalibrated from the existing recordings (no request changed): gerunds became trusted (recall 0.25 to 0.50 on 7 cases), no-table lost precision (1.00 to 0.67, still advisory). Gerunds can now fail a run on 7 Claude-written labels; worth a look when the labels are reviewed.

## RO-017 Keep `other`; no companion question yet

`probe_companion.py` asked each labeled case three ways (with `other`, without it, and with a yes-or-no "does any choice fit?"). Verdict agreement: 0.79 with `other`, 0.80 without, over 100 cases; `other` takes 2% of the probability on average. No label expects "nothing fits", so the probe can't show what the companion question would catch. Revisit when labels include null cases. Cost: $0.003.

## RO-018 Two choice names collided; renamed

`mechanism` meant "describes what the API returns" in opening-sentence and "starts with configuration" in scenario-first; opening-sentence's is now `returns-output`. label-method's `other` meant "no, or the page is about Label" (a pass), unlike every other spec's `other`; it's now `not-listed`, with `other` added back as "none of these". Both rules were re-recorded live; calibration unchanged.

## RO-019 Relations: four pairs resolved, two detectors fixed

The first live relations run (64 rules, 4,032 directed pairs, $0.033) called four pairs conflicting. Two were real tensions in detectors: no-table's added-tables detector would flag the standard example download table, and integrate-before-heading's added-headings detector would flag example headings. Both detectors now skip those. The other two (heading levels and example headings; Label and method-name capitals) are compatible. All four are recorded under `relations` with reasons, for Frances to review. A relations recording covers a rule against the statements as they were; changing any statement means re-recording the new rule's relations, so the gate replays only new rules and the weekly run checks every pair live.

## RO-020 Copied labels are reported for existing rules, blocked for new ones

12 labeled cases across 9 rules are copied from their spec's criteria or examples. Removing them would cut most rules below the trust minimum overnight, so the weekly report lists them and the new-rule gate blocks a new rule that has any.

## RO-021 Prose rules registered from the two reference guides

22 rules from `style-guide-overview.md` and `sentence-word-guidance.md`, each `kind: prose`, with its quote and marker. Three more statements were already registered rules stated in another place, so they became extra `stated_in` entries (explicit-actor twice, filler once). The coverage check still lists 26 rule-like sentences, mostly in the templates; many are template instructions rather than rules.
