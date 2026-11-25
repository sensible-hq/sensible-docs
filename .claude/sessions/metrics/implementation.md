# Docs PR metrics: implementation

How `scripts/docs_pr_metrics/metrics.py` computes what `design.md` defines.

## Data sources

- **PR list.** One `gh pr list --state merged` call returns every merged PR's number, title, body, creation and merge times, and merge commit. It's cached in `--cache` as JSON so reruns don't hit GitHub.
- **PR commits.** `git fetch origin pull/<n>/head:refs/pr/<n>` for each PR in the population. GitHub keeps these refs after the branch is deleted, so squash-merged PRs still have their full commit history.
- **Backend merge dates.** `gh pr view -R sensible-hq/<repo> <n> --json mergedAt`, cached the same way.

## The three trees per PR

| Tree | Commit |
|---|---|
| Base | The merge base of the PR head and the merge commit's first parent. |
| Draft | The PR's first commit that touches doc files, when Claude co-authored it. |
| Final | The merge commit on `v0`. |

Net PR change is `diff(merge_commit^1, merge_commit)`, which is what the PR changed on `v0` regardless of merge strategy. Draft additions are `diff(draft^, draft)`. Revision lines and Frances's lines are `--numstat` sums per commit, with merges excluded so a `v0` merge into the branch doesn't count.

A PR whose first doc commit is Frances's has no AI draft, and its survival is blank rather than 0 or 100.

## Post-merge fixes

For each population PR P, the candidate later PRs are every merged PR, in the population or not, merged within 30 days after P, whose net change touches 10 or fewer doc files. A candidate is a fix when it deletes a line that P's net change added. To keep table rules, fences, and `}` from matching by accident, only lines of 15 or more characters after stripping, with at least one letter, count.

## Code layout

Pure functions, with no git or network access, hold the logic: reference parsing, the doc-file filter, the trailer test, draft selection, word and line survival, pooled rates, fix matching, period assignment, and the report. `Git` and `GitHub` classes wrap the subprocess calls. The tests cover the pure functions directly and use a throwaway git repo for draft selection and survival end to end.

## Running it

```bash
python3 scripts/docs_pr_metrics/metrics.py --refresh --as-of 2026-11-24   # reproducible run
python3 scripts/docs_pr_metrics/metrics.py --cutoff pre-style-cleanup-2026-11-17
python3 -m pytest scripts/docs_pr_metrics/test
```
