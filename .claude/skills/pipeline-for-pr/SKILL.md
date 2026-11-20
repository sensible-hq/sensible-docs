---
name: pipeline-for-pr
description: Take one sensible-hq/sensible engine PR from research to a tested docs PR by running the docs skills in order, stopping for Frances's review after each step. Research the PR, upload its extractor, comment the example config, write the example page, draft the docs, extract testable claims, then add tests. Invoke when Frances asks to run the pipeline, or to take an engine PR "all the way" or "end to end".
argument-hint: <engine-pr-number> [hints about affected doc areas or related PRs]
disable-model-invocation: true
---

Repos and paths come from environment variables in `.claude/settings.json`: `$DOCS_REPO`, `$DOCS_DIR`, `$ENGINE_REPO`, `$APP_REPO`, `$SOURCE_LABELS`. See `.claude/repos.md`.

This skill runs other skills in order. It adds no writing rules of its own: each step follows the named skill's `SKILL.md` and its rules. Run a step by reading that file and following it, because most of these skills can't be invoked from another skill.

Parse **$ARGUMENTS** as follows:
- **First token**: the engine PR number.
- **Remaining text** (optional): hints about the affected doc areas or related PRs. Pass them on to every step that takes hints.

## How the steps hand off

Stop after every step. Report what the step produced and what Frances should check, then wait for her to reply. Her reply is input to the next step: carry her corrections forward, and don't start the next step until she says to. She can skip a step or jump to one by name.

Keep one docs branch, one worktree, and one docs PR for the whole run. Step 4 creates them, and every later step reuses them.

Track the run in `.claude/sessions/<session-name>/checklist.md` in the worktree, with one line per step. Before step 4 exists, keep the checklist in the main checkout and move it into the worktree when step 4 creates it.

## Step 1 — Research the PR

Follow steps 1 and 2 of `.claude/skills/update-docs-from-pr/SKILL.md` to read the PR, its related PRs, and the docs it affects. Then find out where the change stands:

```
gh pr view <pr-number> --repo "$ENGINE_REPO" --json state,mergedAt,baseRefName,labels,files
gh pr list --repo "$DOCS_REPO" --state all --search "sensible#<pr-number>" --json number,title,state
```

Report:
- Whether the change is merged into the engine's default branch, or is still in an open PR.
- What changed for users: new or changed parameters, behaviors, and defaults.
- The doc pages it affects, and whether a docs PR already covers it.
- Any extractor directories under `extractors/` in the PR. Step 2 uploads these.

## Step 2 — Upload the extractor

Follow `.claude/skills/upload-pr-extractor/SKILL.md` with the PR number.

If the PR has no extractor directory with both a config and a golden PDF, adapt instead of stopping. Build a config from the PR's tests and Frances's feedback on step 1, pick a sample PDF with her, and upload them with `scripts/upload_pr_extractor.py`.

Report the Sensible app URLs. Frances works on the example in the app until she settles on a config. Her reply names that config: a file, a pasted config, or a document type and config name in her Sensible account.

## Step 3 — Comment the example config

Put the settled config in a fenced `json` block in `drafts/<pr-number>-example.md` in the main checkout. Follow `.claude/skills/json5-commenter/SKILL.md` on that file.

Report the commented config. Frances may change the comments. Repeat until she settles on them.

## Step 4 — Write the example page

Create the docs branch and worktree as `CLAUDE.md` describes, then follow `.claude/skills/create-docs-example/SKILL.md`. Use the settled config and comments from step 3 rather than the extractor directory's config. If Frances wants a standalone example page rather than an example section on an existing page, create the page in the docs area she names and add it to that area's `index.md`.

Commit, push, and open the docs PR. List the source PR as `sensible-hq/sensible#<pr-number>` in the body, because `close-docs-pr` finds the PRs to relabel from these references.

## Step 5 — Draft the docs

Follow `.claude/skills/update-docs-from-pr/SKILL.md` from its step 3, in the step 4 worktree. It pushes to the open docs PR rather than opening a new one.

## Step 6 — Extract testable claims

Follow `.claude/skills/extract-testable-claims/SKILL.md` with the docs PR number and the engine PR number. Frances picks the claims to test.

## Step 7 — Add tests

If `.claude/skills/add-doc-tests/SKILL.md` exists, follow it for the claims Frances picked, and push the tests to the docs PR.

If it doesn't exist, stop and say so: the skill is in draft PR #749 and isn't on `v0` yet. Leave the picked claims in the checklist, so they can be tested once the skill lands.

## Step 8 — Hand off for merge

Report the docs PR URL, the checklist, and anything still open. Frances reviews and merges the PR herself.

When she says she has squashed and merged it, follow `.claude/skills/close-docs-pr/SKILL.md` with the docs PR number.
