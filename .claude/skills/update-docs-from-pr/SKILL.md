---
name: update-docs-from-pr
description: Given a sensible-hq/sensible PR number, analyze the engine/API changes and update the sensible-docs repo accordingly, then open a PR. Handles both updating existing pages and creating new pages. If you already know which type of change is needed, use update-existing-doc or create-new-doc directly for a more focused workflow.
argument-hint: <pr-number> [hints about affected doc areas or related PRs]
disable-model-invocation: true
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh pr create:*), Bash(git checkout:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Read, Glob, Grep, Edit, Write, mcp__vale__check_file
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

```
git checkout -b fe_<short_description>_docs
```

Make all file edits and creations. Be thorough — cover all parameters and include at least one example per new feature.

## Step 5 — Style check before committing

Run vale on every `.md` file you created or modified. Use the vale MCP server's `check_file` tool for each file:
- Fix all **errors** and **warnings** before committing
- Suggestions are optional — apply if clearly right, skip if they conflict with existing doc conventions

Also check each file against the Sensible terminology glossary at `.claude/style-guide/glossary.md`. Fix any violations in the "Avoid" column.

Only proceed to the commit once all errors and warnings are resolved.

## Step 6 — Commit and open a PR

Stage only the files you changed:
```
git add <files>
git commit -m "docs: <summary>\n\nBased on sensible-hq/sensible#$ARGUMENTS.\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push -u origin <branch>
gh pr create --title "..." --body "..."
```

PR body should include:
- Bullet summary of what was added/changed
- Reference to the source PR (`sensible-hq/sensible#$ARGUMENTS`)
- A test plan checklist for the reviewer

Return the PR URL to the user.
