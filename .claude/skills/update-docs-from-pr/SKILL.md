---
name: update-docs-from-pr
description: Given a sensible-hq/sensible PR number, analyze the engine/API changes and update the sensible-docs repo accordingly, then open a PR. Handles both updating existing pages and creating new pages. If you already know which type of change is needed, use update-existing-doc or create-new-doc directly for a more focused workflow.
argument-hint: <pr-number> [hints about affected doc areas or related PRs]
disable-model-invocation: true
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh pr create:*), Bash(git checkout:*), Bash(git worktree:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Read, Glob, Grep, Edit, Write, Bash(vale:*), Bash(python3 scripts/style/judge.py:*)
---

You are updating the sensible-docs repo based on a pull request from the sensible-hq/sensible engine repo. This skill handles both updating existing pages and creating new pages — use it when you're not sure which is needed, or when a PR requires both.

Parse **$ARGUMENTS** as follows:
- **First token**: the PR number to analyze
- **Remaining text** (optional): free-form hints about which doc areas are likely affected, or mentions of related PRs to also read. Use these to guide your search — don't ignore them.

## Step 1 — Fetch the PR and any related PRs

Run these in parallel:
```
gh pr view <pr-number> --repo sensible-hq/sensible --json title,body,files,commits
gh pr diff <pr-number> --repo sensible-hq/sensible
```

Then scan the PR body for references to related PRs (look for phrases like "follow up of", "based on", "see also", or bare `#NNNN` links). Fetch any referenced PRs that add important context:
```
gh pr view <related-pr-number> --repo sensible-hq/sensible --json title,body,files
```

Read all output carefully. Identify:
- What new features, parameters, or behaviors were added or changed
- Which parts of the engine are affected (preprocessors, matchers, methods, field types, API, email processing, etc.)

## Step 2 — Identify affected docs

The full `docs/` directory structure is:

**SenseML reference** (`docs/Senseml reference/`):
- `preprocessors/` — one `.md` per preprocessor, plus `index.md`
- `field-query-object/` — `match.md`, `anchor.md`, `method.md`, `types.md`
- `layout-based-methods/` — one `.md` per method
- `llm-based-methods/`
- `computed-field-methods/`
- `advanced-computed-field-methods/`
- `concepts/` — `file-types.md`, `ocr.md`, `lines.md`, and others
- `config-settings/`
- `document-type-settings/`
- `sections/`

**Other doc areas**:
- `docs/Email extraction/` — email-specific extraction docs
- `docs/document extraction/` — general extraction guides and best practices
- `docs/document type classification/`
- `docs/api/` — API reference and tutorials
- `docs/integrations/`
- `docs/monitor and qa/`
- `docs/welcome/`

**API reference** (`reference/`):
- OpenAPI JSON spec files (glob `reference/*.json`)

If the PR touches API request/response shapes (new parameters, new fields, changed types, new endpoints), glob `reference/*.json` to find all spec files, then grep them for affected parameter or field names to determine which need updating.

Use the hints from `$ARGUMENTS` and the PR content to determine which areas are relevant. Use Grep to search for existing mentions of changed features/parameters across both `docs/` and `reference/` before deciding what to update.

Read the existing files that are relevant to the PR's changes.

## Step 3 — Plan the changes

**Load the style guide.** Before writing anything, read these three files:
- `.claude/style-guide/style-guide-overview.md` — page structure, voice, formatting, cross-reference syntax
- `.claude/style-guide/reference-topic-template.md` — fillable template for new reference pages
- `.claude/style-guide/sentence-word-guidance.md` — parameter descriptions, terminology, capitalization

For **updating existing pages**, also read:
- `.claude/preferences/editorial-preferences.md` — Frances's editorial corrections and preferences

Apply this guidance when writing or editing. For new pages, use the template as your starting structure.

For each doc change needed, determine whether to:
- **Create** a new `.md` file (for a new preprocessor, method, etc.)
- **Update** an existing file (for new parameters on an existing feature)
- **Update `index.md`** for the relevant section (whenever a new page is added)

## Step 4 — Create a branch and make the changes

Branch naming: `fe_<short_description>_docs` (Frances's initials, since you're acting on her behalf).

Create the branch in a worktree that sits next to the main repo, not with `git checkout -b`. Run from `~/GitHub/sensible-docs`:

```
git pull
git worktree add ../sensible-docs-<short-description> -b fe_<short_description>_docs
```

Then add the worktree path to `permissions.additionalDirectories` in `.claude/settings.json`, and do all remaining work in the worktree.

Make all file edits and creations. Be thorough — cover all parameters and include at least one example per new feature.

## Step 5 — Style check before committing

The Vale hook already reports on each `docs/` page as you edit it. Before committing, run Vale on every `.md` file you created or modified in `docs/`: `vale --minAlertLevel=warning <file>`.
- Fix all **errors** and **warnings** on the lines you changed before committing
- Suggestions are optional: apply them if clearly right, and skip them if they conflict with existing doc conventions

The glossary's avoid-terms are part of Vale's `Sensible.Terminology` rule. Terms that depend on context ("response", "section", "key") still need a read against `.claude/style-guide/glossary.md`.

Don't run Vale on `reference/**/*.md`: those pages are generated from the OpenAPI JSON specs. Edit the JSON instead.

Then run the Jev judge on the same files: `python3 scripts/style/judge.py <files> --base origin/v0`. It checks the judgment rules in `style-rules/judgment/` (opening sentence, explicit actor, scenario-first, and others) and needs `TYPESAFE_API_KEY`.
- Fix every `violation`. These come only from rules whose calibration earned trust.
- Read each `unsure`, `review`, and `(advisory)` line, and fix it if you agree. Leave it if you don't, and say why in the PR body.
- Exit code 3 means Jev was unavailable. Say so in the PR body; it isn't a pass.

Only proceed to the commit once all errors and warnings are resolved.

## Step 6 — Commit and open a PR

Stage only the files you changed:
```
git add <files>
git commit -m "docs: <summary>\n\nBased on sensible-hq/sensible#<pr-number>.\n\n<Co-Authored-By line from this session's attribution instructions>"
git push -u origin <branch>
gh pr create --title "..." --body "..."
```

PR body should include:
- Bullet summary of what was added/changed
- Reference to the source PR (`sensible-hq/sensible#<pr-number>`), plus any related app PRs in full form (`sensible-hq/sensible-app#<pr-number>`). `close-docs-pr` finds the PRs to relabel from these references.
- A test plan checklist for the reviewer

Return the PR URL to the user.

## Step 7 — Wrap up after merge

When Frances says she has squashed and merged the docs PR and is done, run the `close-docs-pr` skill (`.claude/skills/close-docs-pr/SKILL.md`) with the docs PR number. It confirms the merge, finds or creates a sensible-docs issue for the work and closes it, swaps the `doc_changes_needed` label for `docs_done` on each source PR (engine PRs in `sensible-hq/sensible`, app PRs in `sensible-hq/sensible-app`), and removes the worktree.
