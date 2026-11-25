# Docs PR metrics: design

## TL;DR

- **What it measures:** how much Frances revises Claude's first draft on docs PRs for backend changes, before and after the `skills-archive-2026-10` skill rework. Every number is normalized per 100 doc lines changed.
- **First result, 2026-11-24:** revision after the draft fell from 205 to 56 lines per 100 doc lines. Draft words that reach the merge rose from 66% to 90%, or 81% counting only PRs revised after the draft. By kind (`quantification-design.md`), factual revisions fell from 15.0 to 5.8 per 100 doc lines, and copy edits rose from 8.1 to 19.5.
- **Caveat:** only 5 PRs follow the rework, against 16 before it, and they're smaller and add no new pages. Treat this as an early signal, and rerun once 8 or more new PRs have merged.
- **Scope:** only committed changes count. Session back-and-forth before Claude's first commit, force-pushed history, and feedback that changed nothing are missing, so the figures likely undercount Frances's effort.
- **Run it:** `python3 scripts/docs_pr_metrics/metrics.py --refresh --as-of <date>`, then `python3 scripts/docs_pr_metrics/classify.py` for the breakdown by kind.

## Question

Did the skill changes made around the `skills-archive-2026-10` release reduce the back-and-forth between Claude's first draft and Frances's edits on docs PRs that respond to a backend change?

## Population

Merged `sensible-hq/sensible-docs` PRs whose title or body references a PR in `sensible-hq/sensible` or `sensible-hq/sensible-app`, in any of these forms:

- `https://github.com/sensible-hq/sensible/pull/3519`
- `sensible-hq/sensible#3519`, `sensible-hq/sensible-app#120`
- `sensible#3519`, `sensible-app#120`
- A list continuing a reference: `sensible#3519, #3533 and #3540`
- The docs skill's invocation: `/update-docs-from-pr 3235`

A referencing PR that changes no doc files, such as a rubric template, is excluded and listed in the report. Backend references start in February 2026, so the "before" period effectively starts there.

## Period split

The cutoff is the creation date of the `skills-archive-2026-10` tag (2026-10-27): the snapshot taken before the skill rework. A PR belongs to "after" when it was **created** after the cutoff, so a PR drafted with the old skills and merged later still counts as "before". The cutoff is fixed here, before any results were read, so it can't be tuned to flatter the numbers. `--cutoff` overrides it for a sensitivity check, such as the later `pre-style-cleanup-2026-11-17` tag.

## Doc files

A file counts as documentation when it's under `docs/` and ends in `.md`, or is an OpenAPI spec `reference/*.json`. Generated `reference/**/*.md`, assets, scripts, tests, and `.claude/` files are excluded: they're tooling, not the copy Frances edits.

## Metrics, per PR

| Metric | Definition |
|---|---|
| Doc lines changed | Additions plus deletions on doc files, PR merge base to PR head. The size every other metric is normalized by. |
| New doc pages | Doc files the PR adds. Separates new-page PRs from edits to existing pages. |
| Commits | All PR commits. |
| Commits after the draft | Doc-touching commits after the AI draft: the PR's revision rounds. |
| Revision lines | Doc lines added plus deleted in every commit after the draft, whoever made it. The main back-and-forth measure. |
| Lines Frances committed herself | Doc lines in commits without a `Co-Authored-By: Claude` trailer. A floor on her hand edits, never the headline. |
| Draft survival, words | Share of the draft's added words that the merged PR still adds, in order. The headline survival number. |
| Draft survival, whole lines | Share of the draft's added lines that the merged PR still adds unchanged. Kept as a stricter companion. |
| Post-merge fixes | Later merged docs PRs, within 30 days, that change lines this PR added. |
| Lag | Days from the latest referenced backend PR's merge to this PR's merge. |

Every count metric is also reported per 100 doc lines changed. Each period gets two aggregates: the median per PR, which weighs every PR equally, and the pooled rate, the period's total over its total doc lines, which weighs large PRs more.

### The AI draft

The draft is the PR's first commit that touches doc files, when Claude co-authored it. Every later commit is revision, whoever made it. A PR whose first doc commit is Frances's has no AI draft and no survival score.

Word survival compares, per file, the words of the draft commit's added lines with the words of the merged PR's net added lines, and counts the words in matching blocks (`difflib.SequenceMatcher`, with `autojunk` off so no heuristic changes the result). Line survival is a multiset match of whitespace-trimmed lines of 15 or more characters with a letter, against the same net added lines.

Both compare against what the PR adds, not the whole final file, so a draft line identical to one already on the page can't survive by coincidence. A PR with no commits after the draft scores 1.0 by construction, so the report also gives pooled survival over revised PRs only.

### What counts as a revision

The tool reads commits, not conversations or comments. A revision is any change to a doc file committed to the PR branch after the draft, however it got there:

| Source | Counted? |
|---|---|
| An edit Frances asks for in a Claude Code session, which Claude commits | Yes, once committed after the draft |
| A direct edit Frances commits, in the GitHub web editor or locally | Yes |
| A change Claude makes after a PR review comment | Yes, the change. The comment itself isn't counted. |
| A change Claude makes on its own initiative, such as a Vale or style-skill fix | Yes, though it isn't Frances's feedback |
| Back-and-forth in a session before Claude's first commit | No: it shapes the draft, which then looks better than the first thing Claude wrote |
| Commits replaced by an amend or force-push | No: GitHub keeps only the history that was pushed last. #612 had 1 force-push and #715 had 3. |
| A session request or PR comment that produced no change, such as a question or a rejected suggestion | No |
| GitHub review comments, as a count | No |

So revision lines undercount Frances's effort: they miss session iteration before the first commit, and every round of feedback that changed nothing. They also overcount it in two ways. Claude's own fixes are counted as revisions, and moved text counts twice. Of the two, the undercount is likely larger, but nothing in the PR history can measure the gap. The session transcripts can, from 2026-10-26 on.

### Post-merge fixes

A later PR counts as a fix when it:

1. merged within 30 days of this PR,
2. changes 10 or fewer doc files, which excludes repo-wide sweeps like the style cleanup, and
3. deletes a line this PR added. Only lines of 15 or more characters with at least one letter count, so table rules and code fences don't match by accident.

Each candidate is listed in the report, so a reader can strike false positives such as an unrelated feature on the same page. A PR whose 30-day window hasn't closed yet is marked `open`, and its fix count is a floor.

### Lag

Lag is noisy. A docs PR can wait on a release or on Frances's queue, so it's reported, never used as the headline.

## Confounds, reported next to the numbers

- **Size and type.** Each period's table shows median doc lines changed and the new-page share, so a reader can see whether the periods compare like with like.
- **Practice effect.** Frances has gotten better at prompting over time, which no PR metric can separate from the skill changes. The report says so.
- **Sample size.** The report prints n per period, flags a period under 8 PRs, and gives medians beside pooled rates, because one 60-commit PR dominates a pooled rate.

## Audit, 2026-11-24

Frances flagged hand-edit rates as suspiciously low and survival as suspiciously high. An adversarial review of the first version confirmed both, and found these causes:

| Defect in v1 | Effect | Fix |
|---|---|---|
| The draft was the whole first run of Claude commits. Dictated revisions are Claude commits, so for most PRs the "draft" was nearly the final. | #590 scored 0.97 survival after 10 revision commits; #626 and #742 scored 1.0. | The draft is the first doc commit only. |
| Survival matched draft lines against the whole final file. | Repeated lines such as `"type": "string",` survived because the page already had them. | Match against the PR's net added lines. |
| Fences, table rules, and braces counted as lines. | Trivial lines inflated survival. | Line survival counts only lines of 15 or more characters with a letter. |
| Whole-line matching. | One reworded word lost a whole table row (#800: "Claude 5.5 Sonnet" became "Claude Sonnet 5.5"). | Word survival is the headline; line survival stays beside it. |
| Hand edits counted only commits without the Claude trailer. | Dictated copy edits ("where" to "in which") and editor edits Claude committed were invisible. | Revision lines count every commit after the draft. |
| Medians only. | A median of 0 hid #825's and #798's edits. | Pooled rates next to medians. |
| Fix windows closed against the clock, and the PR list cache never refreshed. | Two runs on different days disagreed, and new PRs never appeared. | `--as-of` pins the date; `--refresh` refetches; the report prints both. |
| Reference parsing missed `sensible#3190, #3237` lists and `/update-docs-from-pr 3235`. | Docs PRs dropped from the population. | Both forms parse. |

Two runs with the same `--as-of` and cache produce byte-identical reports.

## Not measured

- **Correction turns in Claude Code sessions.** The transcripts in `~/.claude/projects/` only go back about 30 days, because Claude Code deletes older ones by default (`cleanupPeriodDays`). The "before" period has no transcripts, so this metric can't make a before-and-after comparison.
- **Factual errors, by type.** Telling a factual fix from a copy edit needs a classifier. A stacked PR classifies each revision commit with Jev.
- **Docs work committed straight to `v0`.** Of the 34 backend PRs labeled `docs_done` and merged in 2026, about 10 have no docs PR that mentions them. Their docs likely went straight to `v0`, and they have no PR history to measure.

## Output

`scripts/docs_pr_metrics/metrics.py` writes:

- `per_pr.csv`: one row per PR, with every metric above.
- `report.md`: per-period medians, normalized rates, the confound columns, the fix candidates, and the caveats.

Both go to `--out` (default: `scripts/docs_pr_metrics/output/`, which git ignores). The report is regenerated, not hand-edited.
