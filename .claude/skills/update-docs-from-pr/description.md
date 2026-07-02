# update-docs-from-pr — How it works

This skill takes a pull request number from the `sensible-hq/sensible` engine repo and produces a docs PR in `sensible-docs`. It runs six steps.

---

## Step 1 — Fetch the PR (deterministic)

Runs two fixed `gh` commands in parallel to get the PR's metadata and full diff, then scans the PR body for references to related PRs and fetches those too. This is mechanical: the commands either succeed or fail, and the output is fixed given a PR number.

## Step 2 — Identify affected docs (non-deterministic)

Claude reads the diff and infers which doc files need updating — by searching for existing mentions of changed features/parameters and mapping the code changes to the doc taxonomy (preprocessors, methods, field types, API, etc.). This is a judgment call. The same PR could reasonably lead to different conclusions about which pages need attention. Hints passed as arguments steer this step.

## Step 3 — Plan the changes (non-deterministic)

Claude loads the style guide (overview, template, sentence guidance, editorial preferences) and decides for each affected area whether to create a new page, update an existing page, or both. Writing or editing content to accurately reflect the engine change — including choosing what to say, what to emphasize, and what examples to include — is inherently generative and non-deterministic.

## Step 4 — Create a branch and make the changes (mixed)

Branch creation is deterministic (`git checkout -b fe_<slug>_docs`). The actual file edits are non-deterministic: Claude writes or rewrites doc content, follows the style guide, and decides how to structure new parameters and examples.

## Step 5 — Style check (mostly deterministic)

Vale is run on every modified file via the MCP server. Errors and warnings are fixed; this is largely rule-driven and deterministic. Applying suggestions (the "maybe fix" tier) requires judgment — Claude decides whether a suggestion fits existing conventions — so that part is non-deterministic.

## Step 6 — Commit and open a PR (deterministic)

Stages only the changed files, commits with a fixed message format referencing the source PR, pushes the branch, and opens a docs PR with a structured body. All of this is mechanical.

---

## Summary

| Step | Nature |
|------|--------|
| 1. Fetch PR + related PRs | Deterministic |
| 2. Identify affected docs | Non-deterministic |
| 3. Plan and write content | Non-deterministic |
| 4. Branch creation | Deterministic |
| 4. File edits | Non-deterministic |
| 5. Vale errors/warnings | Deterministic |
| 5. Vale suggestions | Non-deterministic |
| 6. Commit, push, open PR | Deterministic |

The riskiest non-deterministic steps are 2 and 3 — if Claude misidentifies which docs need updating, or misreads what the engine change means, everything downstream will be wrong. Review the PR diff yourself if the change is subtle.
