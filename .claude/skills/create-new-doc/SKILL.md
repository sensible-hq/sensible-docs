---
name: create-new-doc
description: Given a sensible-hq/sensible PR number, create new sensible-docs reference pages for new methods, preprocessors, or other features introduced by the PR — then open a PR. Use this skill when you already know the PR adds something new that needs a new doc page. If you're not sure whether to create or update, use update-docs-from-pr instead.
argument-hint: <pr-number> [hints about what's being added or related PRs]
disable-model-invocation: true
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh pr create:*), Bash(git checkout:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Read, Glob, Grep, Edit, Write
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

## Step 3 — Load your guidance

Read the shared style files:
- `.claude/style-guide/style-guide-overview.md` — page structure, voice, formatting, cross-reference syntax
- `.claude/style-guide/sentence-word-guidance.md` — parameter descriptions, value column formats, terminology

Then read the template that matches the page type:
- **SenseML reference page** (new method, preprocessor, field type, etc.): `.claude/style-guide/reference-topic-template.md` — includes category-specific variants (layout-based, LLM-based, computed field, preprocessor, object page)
- **Integration guide** (new Zapier/SDK/API tutorial): `.claude/style-guide/integration-guide-template.md`

Use the template that matches the type of page you're creating.

## Step 4 — Write the new page

Use the template as your scaffold. Cover:
- All parameters: required/optional/deprecated status, types, defaults
- At least one complete example with config + output (+ example document image if it's a visual/layout method)
- A Notes section if there are edge cases, performance characteristics, or related-method guidance that doesn't fit cleanly in parameter descriptions

For the example:
- Choose data that illustrates *why* the feature is useful, not just that it runs
- Truncate output to 2–3 representative rows + `"..."` if the result is a list or array
- One well-chosen example is better than a "basic" + "advanced" pair

After writing the page, update `index.md` for the category to include a link to the new page.

## Step 5 — Branch, commit, and open a PR

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
