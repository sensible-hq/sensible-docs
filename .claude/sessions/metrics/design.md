# Docs PR metrics: design

## Question

Did the skill changes made around the `skills-archive-2026-10` release reduce the back-and-forth between Claude's first draft and Frances's edits on docs PRs that respond to a backend change?

## Population

Merged `sensible-hq/sensible-docs` PRs whose title or body references a PR in `sensible-hq/sensible` or `sensible-hq/sensible-app`, in any of these forms:

- `https://github.com/sensible-hq/sensible/pull/3519`
- `sensible-hq/sensible#3519`, `sensible-hq/sensible-app#120`
- `sensible#3519`, `sensible-app#120`

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
| Human commits | Commits whose message lacks a `Co-Authored-By: Claude` trailer. |
| Human doc lines | Additions plus deletions on doc files, summed over human commits only. Frances's hand edits. |
| Draft survival | Share of the lines the AI draft added to doc files that are still present, unchanged, in the merged PR head. |
| Commits after the draft | Doc-touching commits after the AI draft: the PR's revision rounds. A PR with none scores 100% survival trivially, so the report shows the share of PRs revised after the draft next to survival. |
| Post-merge fixes | Later merged docs PRs, within 30 days, that change lines this PR added. |
| Lag | Days from the latest referenced backend PR's merge to this PR's merge. |

Every count metric is also reported per 100 doc lines changed.

### The AI draft

The draft is the PR's state at the end of the first contiguous run of Claude-co-authored commits that touches doc files. Commits after that run, whoever wrote them, are revision. This catches edits Frances dictated to Claude, which land as Claude commits and so never show up in the human-commit counts.

Survival is a multiset match per file: each line added in the draft, relative to the merge base, survives when an identical line, ignoring surrounding whitespace, is present in the final file and not already claimed by another surviving line. Blank lines aren't counted. A moved line counts as surviving; a reworded line doesn't.

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
- **Sample size.** The report prints n per period and gives medians, not means, because one 60-commit PR dominates a mean.

## Not measured

- **Correction turns in Claude Code sessions.** The transcripts in `~/.claude/projects/` only go back about 30 days, because Claude Code deletes older ones by default (`cleanupPeriodDays`). The "before" period has no transcripts, so this metric can't make a before-and-after comparison.
- **Factual errors, by type.** Telling a factual fix from a copy edit means classifying each change, by hand or with an LLM. That's a follow-up. The fix lists and per-PR diffs this tool produces are the input for it.

## Output

`scripts/docs_pr_metrics/metrics.py` writes:

- `per_pr.csv`: one row per PR, with every metric above.
- `report.md`: per-period medians, normalized rates, the confound columns, the fix candidates, and the caveats.

Both go to `--out` (default: `scripts/docs_pr_metrics/output/`, which git ignores). The report is regenerated, not hand-edited.
