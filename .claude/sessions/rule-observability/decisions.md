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

## RO-022 Skill restatements are judged per section against every rule

Frances's call (2026-11-19): extend the PR to skills. A regex over imperatives can't tell "Third person or second person, pick one" contradicts the actor rule, so Jev judges each section of each skill, template, and preference file against every registered rule. Code decides: restates at 0.70 needs a marker; contradicts at 0.70 is a problem, 0.50 to 0.70 is listed for review. A first wording of the question flagged sections for how they were written (a skill's own em dashes); the question now says to judge what the section tells the agent to write.

## RO-023 Pointers for rule checklists, markers for the rest

Three sections listed the writing rules as a checklist: api-spec's "Prose quality in descriptions", blog-how-to-parse-x's 6.7b, and blog-short's 5b and 5c. Each now points to `writing-rules.md` and `glossary.md` instead, since a summary drifts. 60 other sections restate a rule because the skill needs the wording in place (a template's frontmatter, a step's image format); they carry the rule's marker, and the registry lists the section (quote: its heading). Markers took three rounds: adding one changes the section, and Jev then tied a few more rules to it.

## RO-024 Contradictions: three fixed, the rest cleared with reasons

Fixed: blog-short's "Third person or second person, pick one" (contradicts the actor rule; now "you" for the reader and "Sensible" for the platform, with "we" allowed in blogs); the reference template's "Opening: imperative verb, Extracts…" (Extracts is third person, which the opening-sentence rule asks for); em dashes in the blog template's integration bullets, which posts copy verbatim. 23 pairs are cleared in `skill-exceptions.yaml`; the ones marked "Review:" are Frances's call: whether code-fences and filler apply to blog posts (they're scoped to docs pages but the blog drafts run the same Vale rules), the blog boilerplate "Check it out!", and the integration guide's "Congratulations, your integration is now published and running!", which is a docs page.

## RO-025 Skill scan recordings aren't committed

A full scan is 393 requests and 3 MB of recordings, and any change to a rule statement invalidates all of them. CI judges only the sections a change touched, live with the repo's key (about $0.0007 a section); the weekly cleanup scans everything live (about $0.25). The routing recordings (41 small files) are committed, since descriptions change rarely.

## RO-026 Routing: who handles what

Applied to the descriptions:
- update-docs-from-pr is the router when the request doesn't say whether the PR needs new pages or changes to existing ones; create-new-doc and update-existing-doc when it does.
- api-spec handles new API endpoints and new specs; update-docs-from-pr updates existing specs for changed parameters (its body already edits `reference/*.json`).
- blog-how-to-parse-x is the technical post with code; blog-short is the no-code overview; create-concept-doc writes a docs page, not a post.
- revise-doc-style restyles; json5-commenter adds the canonical comments; docs-checker checks terminology and doesn't edit code blocks.
Before: 10 requests where a second skill matched within 0.20 of the expected one. After: none. The expected skill won all 39 requests that expect one, before and after.

## RO-027 A collision is a close runner-up, not any second match

Requests like "update the docs for PR 3474" match the router and a specialist; that's by design when the router wins clearly. A collision is a runner-up at 0.50 or more within 0.20 of the top; a runner-up further behind is listed as close.

## RO-028 Corrections attributed to instructions outside the repo

A correction is a typed message matching the pushback pattern after a docs edit in the same turn. It's attributed to a repo rule (an alert on that page in the turn), a repo skill (one in use in the session), or otherwise to outside instructions, listed by name: instruction files outside the repo (`~/.claude/CLAUDE.md`), user and plugin skills, the output style. No content from those files is recorded. The backfilled weeks have no corrections that match the pattern, so the section starts empty; the pattern may be too narrow.

## RO-029 api-spec's frontmatter wasn't valid YAML

Its description had an unquoted ": ", which a strict YAML parser rejects. Quoted. `skill_overlap.py` reports a frontmatter that doesn't parse.

## RO-030 Jev spend

Tonight's extension: about $0.58 (two full skill scans while tuning the question, the marker rounds, the gate's skill scan for the 22 new rules, and four routing runs). Each push of this PR costs about $0.13 in CI (the gate's skill scan for 22 new rules, and the changed sections); a typical PR with one new rule or one skill edit costs a cent or two. The weekly cleanup is about $0.30.
