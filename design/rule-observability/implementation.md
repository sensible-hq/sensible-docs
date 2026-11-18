# Rule observability: implementation

Concept: [concept.md](concept.md). Branch `rule-observability`. Each step lands with its tests; every commit passes the checks in `style-rules/README.md`.

## Step 1: scope and coverage in the registry

- `style-rules/registry.yaml`: every entry gets `scope: general | page-type | construct`, and `applies_to` (a short phrase) for the last two. Enforcement isn't stored: `rule_map.enforcement(entry)` derives `vale`, `jev`, `script`, `manual`, or `prose` from `enforced_by`.
- Register the prose rules that `writing-rules.md`, `style-guide-overview.md`, and `sentence-word-guidance.md` state without a marker, as `kind: prose`, with quotes and markers.
- `check_registry.py`: fail on a missing or unknown scope, a missing `applies_to`, or a stale `HIERARCHY.md`. Keep the existing checks.
- `scripts/style/rule_map.py`: loads the registry, specs, labels, and Vale rules into one model; `coverage()` lists imperative sentences in the style guides with no marker.

## Step 2: hierarchy page

- `scripts/style/rule_map.py hierarchy` writes `style-rules/HIERARCHY.md` (renders on GitHub) and, with `--html`, a standalone report.
- The HTML reuses the CSS of `scripts/doc-detective/codetests/reports/html.py` by import, so the reports look the same.

## Step 3: Jev hygiene

`scripts/style/rule_hygiene.py`, one command per test, each returning problems and a table:

- `catalog`: every choice name, its criteria, and the specs that use it. Fails on one name with different criteria (`other` included), and on a label case whose text appears in its spec's criteria or examples.
- `overlap`: replays each spec's calibration requests (`JEV_REPLAY`) and counts cases where two choices both get probability ≥ 0.25. Flags a pair above one third of the cases.
- `relations`: one Jev request per rule. State: that rule's statement and every other rule's statement, keyed by id. One choice question per other rule: `same-requirement`, `overlapping`, `conflicting`, `independent`. Recorded under `scripts/style/test/fixtures/jev-relations/`. A pair listed under the rule's `relations` in the registry, with a reason, is resolved.
- `crossfire`: lints each Vale fixture's pass lines with every Sensible rule whose gate is `block` or `warn`; an alert from a rule other than the fixture's own is a contradiction.

Judge gate (`judge.py`, `calibrate.py`): a violation is `sum(probabilities[c] for c in verdicts.violation) >= 0.70`, unsure between 0.30 and 0.70. Recalibrate from the existing recordings; no new calls are needed, because the requests don't change.

Companion question probe (`scripts/style/probe_companion.py`, run once, live): for each spec with labels, ask the current question, the question without `other`, and a yes-or-no question "Does any of these choices describe the marked text?" in one request per case. Report agreement with the labels for each design. Record responses. Budget: under $0.10.

## Step 4: new-rule gate

`scripts/style/new_rule_gate.py [--base origin/v0]`:

1. New rules: registry ids not in the base registry, plus Vale rules and specs not in the base.
2. For each: `check_registry.py` problems that name it; scope present; a fixture (Vale) or a label file with ≥ 6 cases and ≥ 3 violations; no copied label cases; `crossfire` clean for its fixture; `relations` for it with no unresolved `same-requirement` or `conflicting`.
3. Exit 1 on any problem; `--html` writes the report.

Wired in: a pytest test runs the gate in replay mode against `origin/v0` when it's available, so CI fails a PR that adds an ungated rule. `style-rules/README.md` "Adding a rule" points to it.

## Step 5: weekly Jev cleanup workflow

`.github/workflows/style-weekly.yml`, Mondays 14:00 UTC and on demand:

1. Install Vale 3.25.1 (release tarball, checksum pinned) and Python deps.
2. `scripts/style/weekly_cleanup.py` with `TYPESAFE_API_KEY`: live calibration (no write), judge over `docs/`, relations, overlap, catalog, unreviewed labels. Writes `report.html` and `issue.md`.
3. Copy to `$RUNNER_TEMP/style-weekly-report.html`, upload with `actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` (`archive: false`), write the run summary with the artifact URL, and open or comment on the `style-weekly` issue with the link.

## Step 6: usage from transcripts

- `scripts/style/rule_usage.py collect [--since 7d]`: reads `~/.claude/projects/<sensible-docs project dirs>/**/*.jsonl`, writes `style-rules/usage/<ISO week>.json`. Project dirs: `sensible-docs` and its worktrees, not `sensible-docs-gen`, `-sandbox`, or `-private*`, which are other repos.
- Events parsed: PreToolUse denials (tool result text), PostToolUse reports (`hook_blocking_error` attachments), let-through context (`hook_additional_context`), judge runs (Bash tool results from `judge.py`), and Read calls on `.claude/style-guide/*.md`.
- Outcomes per firing: acted, ignored, reverted, pushback, unknown (concept section 6).
- `rule_usage.py report` renders the HTML from every committed week.
- `.claude/skills/rule-usage/SKILL.md`: the weekly local run (collect, commit, push).
- `.github/workflows/style-usage-report.yml`: on a push that changes `style-rules/usage/**`, and on demand, renders and uploads the report.

## Step 7: hook and false-positive fixes

- `vale_gate.py` PostToolUse: remember the alerts already reported for a file in the session (state file beside the denial counter) and report only new ones, with a count of those still open.
- `Google.WordListCase`: drop `Email` from the `e-mail` entry, since a capitalized "Email" starts a sentence, a table cell, or a bold label. Fixture lines for both.

## Tests

All offline: unit tests for each command with small fixtures, a synthetic transcript for `rule_usage.py`, replayed Jev recordings for relations and overlap, and `--check` for the generated page.
