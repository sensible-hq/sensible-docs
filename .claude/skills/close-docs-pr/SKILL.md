---
name: close-docs-pr
description: Wrap up a merged sensible-docs PR. Checks the PR is merged, attaches the doc-test evidence (a link to the rendered HTML test report) to the PR, finds or creates a sensible-docs issue that records the work, closes it, swaps the label on each source PR (engine PRs in sensible-hq/sensible, app PRs in sensible-hq/sensible-app) from doc_changes_needed to docs_done, then cleans up the worktree. Invoke when Frances says she has squashed and merged a docs PR and is done with it ("merged, I'm done", "squashed and merged", "close it out"), or when update-docs-from-pr reaches its wrap-up step.
argument-hint: "[docs-pr-number] (defaults to the PR for the current branch)"
allowed-tools: Bash(gh pr view:*), Bash(gh api:*), Bash(gh issue create:*), Bash(git worktree:*), Bash(git branch:*), Bash(git pull:*), Read, Edit
---

You are closing the loop on a docs PR that Frances has already squash-merged. Five outward-facing things happen: a comment with the doc-test evidence goes on the docs PR, an issue is created or closed in `sensible-hq/sensible-docs`, labels change on the source PRs in `sensible-hq/sensible` and `sensible-hq/sensible-app`, and the local worktree is deleted. Frances saying "I'm done" is the go-ahead for all of it. Don't ask again, but stop and ask if anything below doesn't match what you expect.

**Use `gh api` (REST) for edits.** `gh pr edit` and some other `gh` edit commands fail in these repos with a GraphQL "Projects (classic) is being deprecated" error. `gh issue create` and `gh pr view` work.

## Step 1 — Identify the docs PR and confirm it's merged

- Docs PR number: first token of **$ARGUMENTS**. If there isn't one, use the PR for the current branch: `gh pr view --json number`. If you're in the main repo on `v0` (the worktree is gone), ask for the number.
- Confirm the merge:
  ```bash
  gh api repos/sensible-hq/sensible-docs/pulls/<N> --jq '{state, merged, merge_commit_sha, title, body}'
  ```
  If `merged` is false, stop and tell Frances. Don't close anything for an unmerged PR.

## Step 2 — Find the source PR(s)

Scan the docs PR's body and title for source PR references in both repos:
- **Engine** (`sensible-hq/sensible`): `sensible-hq/sensible#NNNN`, `sensible#NNNN`, or `github.com/sensible-hq/sensible/pull/NNNN`.
- **App** (`sensible-hq/sensible-app`): `sensible-hq/sensible-app#NNNN`, `sensible-app#NNNN`, or `github.com/sensible-hq/sensible-app/pull/NNNN`.

Match the repo name exactly: `sensible-hq/sensible#` must not match `sensible-hq/sensible-app#`. Ignore bare `#NNNN`, which refers to sensible-docs itself. Keep track of which repo each PR number belongs to; the steps below call it `<repo>`.

If you find none, ask Frances which source PR it was, or whether there isn't one. Without a source PR, still do Steps 3, 4, and 6, and skip Step 5.

## Step 3 — Attach the doc-test evidence

The HTML report from the page's doc tests is the evidence that the merge is OK. Frances wants a link that opens it as a rendered page, on the docs PR, once it merges. Skip this step if an earlier run already attached it: look for a PR comment starting `**Doc-test evidence**`.

1. **Find the tested pages the PR changed.** List the PR's files, and keep the docs pages that are in `scripts/doc-detective/test-pages.json` at the merge commit, plus any saved report the PR changed:
   ```bash
   gh api repos/sensible-hq/sensible-docs/pulls/<N>/files --paginate --jq '.[].filename'
   git show <merge-sha>:scripts/doc-detective/test-pages.json
   ```
   No tested page and no saved report among the files means there's no evidence to attach. Say so in the report (Step 7) and go on to Step 4.

2. **Link the saved report, if the PR has one.** A page's saved report is `scripts/doc-detective/reports/<slug>.html`, with its results in `<slug>.json`. Get the slug with `python3 scripts/doc-detective/test_matrix.py slug "<page>"`. Read the results at the merge commit (`git show <merge-sha>:scripts/doc-detective/reports/<slug>.json`) for `overall`, `commit`, `tested_at`, and `uncommitted`. Link the report two ways, both pinned to the merge commit, so each link shows exactly what merged and never changes:
   - Rendered: `https://rawcdn.githack.com/sensible-hq/sensible-docs/<merge-sha>/scripts/doc-detective/reports/<slug>.html`. GitHub shows a committed HTML file as source, so the rendered link goes through githack, which serves public repo files as web pages. The report's links to fixture files resolve at the same commit. Check the link before posting it with a GET, since githack answers HEAD requests with 403: `curl -sL -o /dev/null -w '%{http_code} %{content_type}' <url>` prints `200 text/html`.
   - Source: `https://github.com/sensible-hq/sensible-docs/blob/<merge-sha>/scripts/doc-detective/reports/<slug>.html`.

   Say plainly, in the comment and the report, anything that weakens it as evidence: the PR didn't update the report (it's older evidence), `overall` isn't `pass`, `uncommitted` is true, or the tested commit isn't in the PR's history.

3. **If it wasn't done already, run the tests now.** For a tested page the PR changed without saving its report, run the page's tests in CI on the merged `v0`, and link that run's report:
   ```bash
   gh workflow run doc-tests.yml --repo sensible-hq/sensible-docs --ref v0 -f page="<page>"
   gh run list --repo sensible-hq/sensible-docs --workflow doc-tests.yml --limit 1 --json databaseId,url,headSha
   gh run watch <run-id> --repo sensible-hq/sensible-docs --exit-status
   gh api repos/sensible-hq/sensible-docs/actions/runs/<run-id>/artifacts --jq '.artifacts[] | select(.name | endswith("report.html")) | .id'
   ```
   The report's link is `https://github.com/sensible-hq/sensible-docs/actions/runs/<run-id>/artifacts/<artifact-id>`. It opens as a rendered page for anyone signed in to GitHub, but it expires after 90 days, so say so in the comment. Then ask Frances whether to save a permanent report (`DOC_TESTS_SAVE_REPORT=1 scripts/doc-detective/run.sh "<page>"` on `v0`, committed in a follow-up PR). Don't open that PR unasked. A failed run is the finding: post it with the run's link, and flag it in the report rather than closing the loop as if it passed.

4. **Post one comment on the docs PR,** with a line per tested page:
   ```bash
   gh api repos/sensible-hq/sensible-docs/issues/<N>/comments -F body=@<scratchpad>/evidence.md
   ```
   ```markdown
   **Doc-test evidence**

   - `<page>`: [rendered report](<rendered url>) · [source](<source url>) · <overall>, tested at commit <commit> on <tested_at date>
   ```
   Add the same lines to the issue in Step 4.

## Step 4 — Find or create the docs issue, then close it

**Look for an existing issue**, in this order:
1. Issues that cross-reference the docs PR:
   ```bash
   gh api repos/sensible-hq/sensible-docs/issues/<N>/timeline --paginate \
     --jq '[.[] | select(.event=="cross-referenced" and .source.issue.pull_request == null) | {number: .source.issue.number, state: .source.issue.state, title: .source.issue.title}]'
   ```
2. Issues that mention a source PR, using its repo name (`sensible` or `sensible-app`):
   ```bash
   gh api -X GET search/issues -f q='repo:sensible-hq/sensible-docs is:issue "<repo-name>#<NNNN>"' --jq '.items[] | {number, state, title}'
   ```
   Also search for the feature name from the PR title if nothing comes back.

If several candidates turn up and it's unclear which one tracks this work, list them and ask.

**If an open issue exists:** comment that it's done, then close it:
```bash
gh api repos/sensible-hq/sensible-docs/issues/<issue>/comments -f body="Done in #<N>."
gh api -X PATCH repos/sensible-hq/sensible-docs/issues/<issue> -f state=closed -f state_reason=completed
```

**If a closed issue exists:** leave it alone and report it.

**If no issue exists:** create one, then close it with the same PATCH as above. Match Frances's issue style: short, informal, and no labels. Write the body to a file in the scratchpad and pass it with `--body-file`:
```bash
gh issue create --repo sensible-hq/sensible-docs \
  --title "Document <feature> (<repo-name>#<NNNN>)" \
  --body-file <scratchpad>/issue_body.md
```
Body contents:
- One line saying what was documented, citing every source PR in full form (`sensible-hq/sensible#<NNNN>`, `sensible-hq/sensible-app#<NNNN>`).
- `Done in #<N> (squash-merged as <short merge sha>):` followed by a `- [x]` list of the actual changes. Build it from the docs PR body and diff, not from memory.
- The doc-test evidence lines from Step 3, if any.
- Any follow-ups the session recorded: changelog entries, test configs, deliberately undocumented behavior.

Mentioning `#<N>` in the body cross-references the issue and PR in both timelines. That's the only link available: a merged PR can't gain a "Closes #X" Development link after the fact.

## Step 5 — Swap each source PR's label

For each source PR from Step 2, where `<repo>` is `sensible-hq/sensible` or `sensible-hq/sensible-app`:
```bash
gh api repos/<repo>/issues/<NNNN>/labels --jq '[.[].name]'
```

- **Has `doc_changes_needed`:** remove it and add `docs_done`:
  ```bash
  gh api -X DELETE repos/<repo>/issues/<NNNN>/labels/doc_changes_needed --silent
  gh api -X POST repos/<repo>/issues/<NNNN>/labels -f 'labels[]=docs_done' --silent
  ```
- **Already has `docs_done`:** nothing to do. Report it.
- **Has `docs_dont_publicly_doc`, `docs_future_not_yet_blocked`, or no docs label:** don't change anything. Report what's there and ask. A docs PR for a PR labeled "don't publicly doc" is a mismatch worth flagging.

Re-read the labels afterward and report the final set.

The docs label names are the same in both repos: `doc_changes_needed`, `docs_done`, `docs_dont_publicly_doc` and `docs_future_not_yet_blocked`. If a call fails with a missing label, re-check them with `gh label list --repo <repo> --search doc`.

## Step 6 — Clean up the worktree

Follow the worktree cleanup flow from memory. Run from the main repo directory (`~/GitHub/sensible-docs`), not the worktree:
1. `git -C <worktree> status --short`. If anything is uncommitted, stop and show it. Don't discard work.
2. `git worktree remove <worktree-path>`
3. `git branch -D <branch>`. Use `-D`: squash merges leave the branch looking unmerged, so `-d` refuses.
4. Remove the worktree path from `permissions.additionalDirectories` in `.claude/settings.json`. Edit it as JSON (load, remove the entry, dump), not with a line delete. Other sessions add entries to the same file, and deleting a line can leave a trailing comma that breaks the JSON. Keep everyone else's entries.
5. `git pull` on `v0`.
6. Check whether the remote branch still exists (`git ls-remote --heads origin <branch>`). GitHub usually auto-deletes it. If it's still there, mention it but don't delete it.

## Step 7 — Report

Give Frances one short summary covering:
- **Doc-test evidence:** the rendered report link and result for each tested page, or that the PR changed no tested page.
- **Issue:** created or found, number and URL, and closed.
- **Source PR labels:** before and after, for each engine and app PR.
- **Worktree:** removed, the branch deleted, and v0 pulled.
- **Anything skipped or needing a decision:** for example, an unexpected label, several candidate issues, or leftover test configs in the Sensible account.
