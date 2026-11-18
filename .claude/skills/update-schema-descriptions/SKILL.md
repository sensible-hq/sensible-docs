---
name: update-schema-descriptions
description: Given a sensible-hq/sensible PR that adds or renames SenseML parameters or types, add descriptions for them as /** */ doc comments in src/engine/types.ts, regenerate the config schemas, check that the diff changes only descriptions, and open a draft PR against the engine repo. Use after the parameter's docs are drafted, so the description can follow the docs wording. Triggers on "update types.ts descriptions", "add schema descriptions for <param>", "open an engine PR for the param descriptions".
argument-hint: <engine-pr-number> [path to the docs page that documents the parameter]
disable-model-invocation: true
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh pr list:*), Bash(gh pr create:*), Bash(git:*), Bash(bash .claude/skills/update-schema-descriptions/regenerate.sh:*), Bash(python3 .claude/skills/update-schema-descriptions/check_schema_diff.py:*), Read, Grep, Edit
---

You are adding descriptions for new SenseML parameters to the engine's `src/engine/types.ts`. `ts-json-schema-generator` turns each `/** */` comment on a property into a `description` in the generated config schema, which `scripts/deploy-schema.ts` publishes to the schema server.

The arguments are: **$ARGUMENTS**. The first token is the engine PR number. The optional second token is the docs page that documents the parameter.

Repos and paths come from `.claude/settings.json`: `$ENGINE_REPO`, `$ENGINE_DIR`, `$DOCS_REPO`, `$DOCS_DIR`. See `.claude/repos.md`.

**Engine code stays with Claude.** Don't send engine source, diffs, or types.ts excerpts to Jev or any other outside service (`scripts/style/judge.py` included). Jev is approved for docs text only.

## Step 1 — Find the parameters, under their current names

```bash
gh pr view <pr> --repo "$ENGINE_REPO" --json title,body,state,mergedAt,files
gh pr diff <pr> --repo "$ENGINE_REPO" -- src/engine/types.ts
```

List every property or type the PR adds to `types.ts`. Then check whether a later PR renamed or removed any of them: search merged PRs that mention the PR number or the parameter name (`gh pr list --repo "$ENGINE_REPO" --state merged --search "<pr> OR <name>"`), and grep `types.ts` on `origin/main` for each name. Document the names on `origin/main`, not the names in the PR. Example: sensible-hq/sensible#3519 added `omit`, and #3533 renamed it `ocrIfMissing`.

If a property already has a `/** */` comment on `origin/main`, leave it unless it's wrong; say which in your report.

## Step 2 — Write each description

**Source.** Start from the parameter's row on the docs page (the second argument, or find it with Grep under `$DOCS_DIR/docs/`; check open docs branches with `gh pr list --repo "$DOCS_REPO" --search <name>` if `v0` doesn't have it yet). If no docs exist, use the engine PR description. Read `.claude/style-guide/writing-rules.md`; the same rules apply.

**Verify every claim against the engine code on `origin/main`**: the branch in the types.ts union, the generated schema's `additionalProperties` and `required`, and the code that reads the parameter. Record the file and line for each claim; the PR body cites them. Don't state a claim you can't point to.

**Shape:**
- Plain text, one to three sentences, about 300 characters at most. Editors show it on hover, so lead with what the parameter does.
- No Markdown links, `<br/>`, or `doc:` slugs; they don't render in the schema. Name other parameters by their JSON key in backticks, for example `engine`.
- State compatibility as what the parameter *can* be combined with, not what it can't.
- End with `See https://docs.sensible.so/docs/<page-slug>.` for the docs page. The slug is the page's file name without `.md`.

Example, for `ocrIfMissing`:

```ts
      /**
       * If Sensible doesn't find this text in the document's embedded text, it OCRs every page. If it
       * finds the text, it OCRs nothing. Can be combined only with `engine`. An empty array OCRs nothing.
       * See https://docs.sensible.so/docs/ocr-preprocessor.
       */
      ocrIfMissing: AnchorMatch;
```

Show Frances the descriptions before editing, and wait for her go-ahead.

## Step 3 — Make a worktree

```bash
git -C "$ENGINE_DIR" fetch origin
git -C "$ENGINE_DIR" worktree add "$ENGINE_DIR-<slug>" -b fe_<slug>_schema_descriptions origin/main
```

Work only in `$ENGINE_DIR-<slug>` from here on.

## Step 4 — Check the toolchain reproduces the schemas

Before editing anything:

```bash
bash .claude/skills/update-schema-descriptions/regenerate.sh "$ENGINE_DIR-<slug>"
git -C "$ENGINE_DIR-<slug>" status --short
```

The status must be empty. If the script changed a schema, stop: its output doesn't match how the engine generates schemas, so it can't be trusted, and a PR built on it would carry unrelated changes. Report the diff to Frances.

## Step 5 — Edit types.ts and regenerate

Add each `/** */` comment directly above its property. If a `//` comment above the property says the same thing, replace it; a `//` comment never reaches the schema. Change nothing else in the file.

```bash
bash .claude/skills/update-schema-descriptions/regenerate.sh "$ENGINE_DIR-<slug>"
python3 .claude/skills/update-schema-descriptions/check_schema_diff.py "$ENGINE_DIR-<slug>"
```

The check must print `ok`. It fails on any change that isn't a comment in `types.ts` or a description in the schemas. It allows one kind of churn: `NonEmptyPartialUnion<…>` definitions are named after byte offsets in `types.ts`, so any edit that changes the file's length renames them (14 lines in each recent schema commit). Confirm the number of description lines it reports matches the number of comments you added.

## Step 6 — Tests

The engine repo's `CLAUDE.md` requires unit tests and extractor tests before pushing any change under `src/engine/`, and makes no exception for comments. If the worktree has `node_modules`, run `pnpm project:compile`, `pnpm test:unit`, and `scripts/extract-all.ts`, and record the results. If it doesn't, don't install or push on your own: tell Frances, and let her choose between installing and running the tests, or opening the PR as a draft that says the tests weren't run. Never write that tests passed unless you ran them.

## Step 7 — Commit and open a draft PR

Check the branch has no merged PR (`gh pr view --repo "$ENGINE_REPO" --json state,mergeCommit` from the worktree), then:

```bash
git -C "$ENGINE_DIR-<slug>" add src/engine/types.ts src/engine/__generated__/
git -C "$ENGINE_DIR-<slug>" commit -m "Add schema descriptions for <params>

<Co-Authored-By line from this session's attribution instructions>"
git -C "$ENGINE_DIR-<slug>" push -u origin fe_<slug>_schema_descriptions
gh pr create --repo "$ENGINE_REPO" --draft --head fe_<slug>_schema_descriptions --title "Add schema descriptions for <params>" --body-file <file>
```

PR body:
- **Summary:** the parameters described, and the source PRs in full form (`sensible-hq/sensible#<n>`), plus the docs PR if there is one (`sensible-hq/sensible-docs#<n>`).
- **Evidence:** for each claim in each description, the file and line on `origin/main` that supports it, as permalinks at the commit you branched from.
- **Diff check:** the output of `check_schema_diff.py`, and a sentence explaining the `NonEmptyPartialUnion` renames so reviewers don't have to wonder.
- **Tests:** what you ran and the result, or that you didn't run them.
- The PR attribution line from this session's instructions.

Don't request reviewers or add labels unless Frances asks.

## Step 8 — Report

Give Frances the PR URL, the descriptions as written, the check output, and the test status. Remove the worktree only after the PR merges.
