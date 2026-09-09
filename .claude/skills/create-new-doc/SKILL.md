---
name: create-new-doc
description: Given a sensible-hq/sensible PR number, create new sensible-docs reference pages for new methods, preprocessors, or other features introduced by the PR — then open a PR. Use this skill when you already know the PR adds something new that needs a new doc page. If you're not sure whether to create or update, use update-docs-from-pr instead.
argument-hint: <pr-number> [hints about what's being added or related PRs]
disable-model-invocation: true
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh pr create:*), Bash(gh issue list:*), Bash(git checkout:*), Bash(git worktree:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Read, Glob, Grep, Edit, Write, mcp__vale__check_file
---

You are creating new sensible-docs reference pages based on a pull request from the sensible-hq/sensible engine repo.

Parse **$ARGUMENTS** as follows:
- **First token**: the PR number to analyze
- **Remaining text** (optional): hints about what's being added, related PRs, or which doc category it belongs to

## Step 1 — Fetch the PR and any related PRs

Run in parallel:
```
gh pr view <pr-number> --repo sensible-hq/sensible --json title,body,files,commits
gh pr diff <pr-number> --repo sensible-hq/sensible
```

Fetch any related PRs referenced in the body. Identify:
- What new feature is being introduced (method, preprocessor, field type, config option, etc.)
- All its parameters, defaults, and behaviors
- Which doc category it belongs to (layout-based methods, LLM methods, preprocessors, computed field methods, etc.)

## Step 2 — Orient yourself in the docs tree

Locate the right subdirectory under `docs/Senseml reference/<category>/`. Check what's already there. Read `index.md` for that category — you'll add a link to it. Read 1–2 nearby pages in the same category so your new page matches their conventions.

The full `docs/` structure:

**SenseML reference** (`docs/Senseml reference/`):
- `preprocessors/`, `field-query-object/`, `layout-based-methods/`, `llm-based-methods/`, `computed-field-methods/`, `advanced-computed-field-methods/`, `concepts/`, `config-settings/`, `document-type-settings/`, `sections/`

**Other doc areas**:
- `docs/Email extraction/`, `docs/document extraction/`, `docs/document type classification/`, `docs/api/`, `docs/integrations/`, `docs/monitor and qa/`, `docs/welcome/`

## Step 3 — Draft the user brief

Before writing the page, draft a user brief at `.claude/briefs/<slug>.md` (slug = the filename you'll create, without extension).

Use `.claude/briefs/brief-template.md` as your scaffold. Pull from these sources in parallel:
- The PR body and diff — for feature context and intended use cases
- GitHub issues: `gh issue list --repo sensible-hq/sensible --search "<feature name>" --json number,title,body` and `gh issue list --repo sensible-hq/sensible-docs --search "<feature name>" --json number,title,body`
- Adjacent pages in the same category (already read in Step 2) — who reads those pages implies who reads this one

The brief defines who you're writing for before you write a word. Everything in Step 5 (the page itself) flows from it — depth, vocabulary, what to include, what to omit.

**When the brief shapes a content decision,** say so in the PR description — e.g., "Brief notes readers arrive from search and may not have an existing config set up, so the example uses a minimal starting config."

## Step 4 — Load guidance (required reads — do not skip)

Call Read on each path below before writing any doc content. Do not proceed to Step 4 until all reads are complete.

**Always required:**
1. Read `.claude/style-guide/style-guide-overview.md` — page structure, voice, formatting, cross-reference syntax
2. Read `.claude/style-guide/sentence-word-guidance.md` — parameter descriptions, value column formats, terminology
3. Read `.claude/style-guide/writing-rules.md` — cross-cutting prose rules (em dashes, passive voice, gerunds, tone)
4. Read `.claude/style-guide/glossary.md` — canonical terms; the "Avoid" column lists violations to fix
5. Read `.claude/preferences/editorial-preferences.md` — Frances's editorial corrections and preferences

**Then read the template that matches the page type:**
6. Read `.claude/style-guide/reference-topic-template.md` for a SenseML reference page (new method, preprocessor, field type, etc.) — includes category-specific variants (layout-based, LLM-based, computed field, preprocessor, object page)
   OR read `.claude/style-guide/integration-guide-template.md` for an integration guide (new Zapier/SDK/API tutorial)

Use the template that matches the type of page you're creating.

## Step 5 — Write the new page

Use the template as your scaffold. Cover:
- All parameters: required/optional/deprecated status, types, defaults
- At least one complete example with config + output (+ example document image if it's a visual/layout method)
- A Notes section if there are edge cases, performance characteristics, or related-method guidance that doesn't fit cleanly in parameter descriptions

For the example:
- Choose data that illustrates *why* the feature is useful, not just that it runs
- Truncate output to 2–3 representative rows + `"..."` if the result is a list or array
- One well-chosen example is better than a "basic" + "advanced" pair

After writing the page, update `index.md` for the category to include a link to the new page.

## Step 6 — Style check before committing

Run vale on every `.md` file you created or modified. Use the vale MCP server's `check_file` tool for each file:
- Fix all **errors** and **warnings** before committing
- Suggestions are optional — apply if clearly right, skip if they conflict with existing doc conventions

Also scan each file for glossary violations (the "Avoid" column in `.claude/style-guide/glossary.md`). You already read this file in Step 4 — apply what you learned.

Only proceed once all errors and warnings are resolved.

## Step 7 — Branch, commit, and open a PR

Branch naming: `fe_<short_description>_docs` (Frances's initials, since you're acting on her behalf).

```
git checkout -b fe_<short_description>_docs
git add <files>
git commit -m "docs: add <feature> reference page\n\nBased on sensible-hq/sensible#<pr-number>.\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push -u origin fe_<short_description>_docs
gh pr create --title "..." --body "..."
```

PR body should include:
- What page was created and what feature it documents
- Reference to the source PR (`sensible-hq/sensible#<pr-number>`)
- A test plan checklist for the reviewer

Return the PR URL to the user.
