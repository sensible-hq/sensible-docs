---
name: update-docs-from-pr
description: Given a sensible-hq/sensible PR number, analyze the engine/API changes and update the sensible-docs repo accordingly, then open a PR.
argument-hint: <pr-number>
disable-model-invocation: true
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh pr create:*), Bash(git checkout:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Read, Glob, Grep, Edit, Write
---

You are updating the sensible-docs repo based on a pull request from the sensible-hq/sensible engine repo.

The PR number to analyze is: **$ARGUMENTS**

## Step 1 — Fetch the PR

Run both of these in parallel:
```
gh pr view $ARGUMENTS --repo sensible-hq/sensible --json title,body,files,commits
gh pr diff $ARGUMENTS --repo sensible-hq/sensible
```

Read the output carefully. Identify:
- What new features, parameters, or behaviors were added or changed
- Which parts of the engine are affected (preprocessors, matchers, methods, field types, etc.)

## Step 2 — Identify affected docs

The sensible-docs directory structure is under `docs/`. Key subdirectories for the SenseML reference under `docs/senseml/` include:
- `preprocessors/` — one `.md` per preprocessor, plus `index.md`
- `field-query-object/` — `match.md`, `anchor.md`, `method.md`, `types.md`
- `layout-based-methods/` — one `.md` per method
- `llm-based-methods/`
- `computed-field-methods/`
- `advanced-computed-field-methods/`
- `concepts/`

Read the existing files that are relevant to the PR's changes. Understand the writing style, parameter table format, and example structure before making any edits.

## Step 3 — Plan the changes

For each doc change needed, determine whether to:
- **Create** a new `.md` file (for a new preprocessor, method, etc.)
- **Update** an existing file (for new parameters on an existing feature)
- **Update `index.md`** for the relevant section (whenever a new page is added)

Follow these conventions from the existing docs:
- Frontmatter: `title`, `excerpt: ''`, `deprecated: false`, `hidden: false`, `metadata` (title, description, robots), `next: {description: ''}`
- Parameters are documented in markdown tables with columns: `key`, `value`/`values`, `description`
- Required parameters are marked **required** in the key column
- Examples use fenced ```json blocks with `**Config**`, `**Example document**`, `**Output**` subheadings
- Cross-references use `doc:` links, e.g. `[Match](doc:match)`

## Step 4 — Create a branch and make the changes

Branch naming: `fe_<short_description>_docs` (Frances's initials, since you're acting on her behalf).

```
git checkout -b fe_<short_description>_docs
```

Make all file edits and creations. Be thorough — cover all parameters and include at least one example per new feature.

## Step 5 — Commit and open a PR

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
