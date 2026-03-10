---
name: update-existing-doc
description: Given a sensible-hq/sensible PR number, update existing sensible-docs pages to reflect changes to existing features, parameters, or behaviors — then open a PR. Use this skill when you already know the PR only affects existing docs (no new pages needed). If you're not sure whether to create or update, use update-docs-from-pr instead.
argument-hint: <pr-number> [hints about affected doc areas or related PRs]
disable-model-invocation: true
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh pr create:*), Bash(git checkout:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Read, Glob, Grep, Edit, Write
---

You are updating existing sensible-docs pages based on a pull request from the sensible-hq/sensible engine repo. Your job is to make targeted, accurate edits — not to rewrite working content.

Parse **$ARGUMENTS** as follows:
- **First token**: the PR number to analyze
- **Remaining text** (optional): hints about which doc areas are affected, or related PRs to read

## Step 1 — Fetch the PR and any related PRs

Run in parallel:
```
gh pr view <pr-number> --repo sensible-hq/sensible --json title,body,files,commits
gh pr diff <pr-number> --repo sensible-hq/sensible
```

Scan the PR body for related PR references (`follow up of`, `based on`, `see also`, `#NNNN`). Fetch any that add important context.

Identify:
- What parameters, behaviors, or defaults were added or changed on **existing** features
- Which engine components are affected (preprocessors, matchers, methods, field types, API, email processing, etc.)

## Step 2 — Find and read the affected docs

The full `docs/` directory structure:

**SenseML reference** (`docs/Senseml reference/`):
- `preprocessors/`, `field-query-object/`, `layout-based-methods/`, `llm-based-methods/`, `computed-field-methods/`, `advanced-computed-field-methods/`, `concepts/`, `config-settings/`, `document-type-settings/`, `sections/`

**Other doc areas**:
- `docs/Email extraction/`, `docs/document extraction/`, `docs/document type classification/`, `docs/api/`, `docs/integrations/`, `docs/monitor and qa/`, `docs/welcome/`

Use Grep to search for existing mentions of the changed features/parameters across the docs tree. Read every file you'll edit before touching it.

## Step 3 — Load your guidance

Read these files before writing anything:
- `.claude/style-guide/style-guide-overview.md` — page structure, voice, formatting, cross-reference syntax
- `.claude/style-guide/sentence-word-guidance.md` — parameter descriptions, terminology, capitalization
- `.claude/preferences/editorial-preferences.md` — Frances's editorial corrections and preferences

Pay particular attention to the preferences file. It documents specific choices Frances has made that override default instincts.

## Step 4 — Plan and make the changes

For each file you're editing, think through:

**Where to put new content.**
Integrate new parameters into the existing parameter table in the correct position. Integrate new behavioral notes into existing explanatory sections rather than creating new headings, unless the new content has enough substance (3+ distinct concepts, a parameter table, or a code example) to stand alone. See the preferences file's "Information architecture" section.

**Whether to update the example.**
If the PR changes behavior the existing example exercises, update the example output or config. If the PR adds a new capability the example doesn't cover, consider extending the existing example rather than adding a second one. See the preferences file's "Examples" section.

**What not to touch.**
Don't rewrite sentences that are correct and well-phrased. Don't restructure sections that aren't affected by the PR. The scope of your edits should match the scope of the PR.

## Step 5 — Branch, commit, and open a PR

Branch naming: `fe_<short_description>_docs` (Frances's initials, since you're acting on her behalf).

```
git checkout -b fe_<short_description>_docs
git add <files>
git commit -m "docs: <summary>\n\nBased on sensible-hq/sensible#<pr-number>.\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push -u origin fe_<short_description>_docs
gh pr create --title "..." --body "..."
```

PR body should include:
- Bullet summary of what was added/changed
- Reference to the source PR (`sensible-hq/sensible#<pr-number>`)
- A test plan checklist for the reviewer

Return the PR URL to the user.
