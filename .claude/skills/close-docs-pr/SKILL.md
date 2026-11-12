---
name: close-docs-pr
description: Wrap up a merged sensible-docs PR. Checks the PR is merged, finds or creates a sensible-docs issue that records the work, closes it, swaps the label on each source PR (engine PRs in sensible-hq/sensible, app PRs in sensible-hq/sensible-app) from doc_changes_needed to docs_done, then cleans up the worktree. Invoke when Frances says she has squashed and merged a docs PR and is done with it ("merged, I'm done", "squashed and merged", "close it out"), or when update-docs-from-pr reaches its wrap-up step.
argument-hint: "[docs-pr-number] (defaults to the PR for the current branch)"
allowed-tools: Bash(gh pr view:*), Bash(gh api:*), Bash(gh issue create:*), Bash(git worktree:*), Bash(git branch:*), Bash(git pull:*), Read, Edit
---

You are closing the loop on a docs PR that Frances has already squash-merged. Four outward-facing things happen: an issue is created or closed in `sensible-hq/sensible-docs`, labels change on the source PRs in `sensible-hq/sensible` and `sensible-hq/sensible-app`, and the local worktree is deleted. Frances saying "I'm done" is the go-ahead for all of it. Don't ask again, but stop and ask if anything below doesn't match what you expect.

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

If you find none, ask Frances which source PR it was, or whether there isn't one. Without a source PR, still do Steps 3 and 5 and skip Step 4.

## Step 3 — Find or create the docs issue, then close it

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
- Any follow-ups the session recorded: changelog entries, test configs, deliberately undocumented behavior.

Mentioning `#<N>` in the body cross-references the issue and PR in both timelines. That's the only link available: a merged PR can't gain a "Closes #X" Development link after the fact.

## Step 4 — Swap each source PR's label

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

## Step 5 — Clean up the worktree

Follow the worktree cleanup flow from memory. Run from the main repo directory (`~/GitHub/sensible-docs`), not the worktree:
1. `git -C <worktree> status --short`. If anything is uncommitted, stop and show it. Don't discard work.
2. `git worktree remove <worktree-path>`
3. `git branch -D <branch>`. Use `-D`: squash merges leave the branch looking unmerged, so `-d` refuses.
4. Remove the worktree path from `permissions.additionalDirectories` in `.claude/settings.json`. Edit it as JSON (load, remove the entry, dump), not with a line delete. Other sessions add entries to the same file, and deleting a line can leave a trailing comma that breaks the JSON. Keep everyone else's entries.
5. `git pull` on `v0`.
6. Check whether the remote branch still exists (`git ls-remote --heads origin <branch>`). GitHub usually auto-deletes it. If it's still there, mention it but don't delete it.

## Step 6 — Report

Give Frances one short summary covering:
- **Issue:** created or found, number and URL, and closed.
- **Source PR labels:** before and after, for each engine and app PR.
- **Worktree:** removed, the branch deleted, and v0 pulled.
- **Anything skipped or needing a decision:** for example, an unexpected label, several candidate issues, or leftover test configs in the Sensible account.
