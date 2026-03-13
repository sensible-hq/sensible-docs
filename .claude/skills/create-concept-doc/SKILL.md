---
name: create-concept-doc
description: Create a new concept topic page in docs/Senseml reference/concepts/ — for explanatory "how it works" topics, not reference pages. Use this skill when you need to document a concept, behavior, or feature overview (not a new method, preprocessor, or config option). If you're documenting a new method or preprocessor introduced by a PR, use create-new-doc instead.
argument-hint: "<concept-name> — <description of what to cover> [optional: PR #<number> for context]"
disable-model-invocation: true
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh pr create:*), Bash(git checkout:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Read, Glob, Grep, Edit, Write
---

You are writing a new concept topic page for the Sensible docs.

Parse **$ARGUMENTS** as follows:
- **Concept name**: the topic to document (e.g., "anchor nuances", "LLM token limits")
- **Description**: what the page should cover — may be free-form notes, a feature description, or a question to answer
- **Optional PR reference**: if the user says `PR #<number>`, fetch it for context

## Step 1 — Gather context

Run in parallel:

**Always:** Read 2 existing concept pages whose topic is most similar to the new page. Good choices:
- Factual/reference-style concept → read `coverage.md` and `ocr.md`
- Feature behavior concept → read `fallbacks.md` and `field-order.md`
- Visual/structural concept → read `lines.md` and `anchor-nuances.md`
- LLM-related concept → read `llm-features.md` and `prompt.md`

**If a PR number was given:** Fetch it for context:
```
gh pr view <pr-number> --repo sensible-hq/sensible --json title,body,files
gh pr diff <pr-number> --repo sensible-hq/sensible
```

## Step 2 — Load your guidance

Read in parallel:
- `.claude/style-guide/style-guide-overview.md` — frontmatter format, voice, formatting, cross-reference syntax
- `.claude/style-guide/concept-topic-template.md` — concept page structure, optional elements, file naming

## Step 3 — Write the page

Use the template from Step 2 as your scaffold. Apply the structural variant that fits the topic shape:

- **Process/how-it-works**: opening definition → numbered steps or ordered H2s → optional Troubleshooting H2
- **Feature overview**: opening summary → H2 per feature area → links out to related reference pages
- **Behavior with variants**: opening definition → "Default behavior" H2 → "Configurable behavior" H2 → Notes
- **Concept with formula**: opening definition → formula/calculation H2 → example H2 → Notes

Write the page at: `docs/Senseml reference/concepts/<slug>.md`

Where `<slug>` is a kebab-case filename derived from the concept name (e.g., `llm-token-limits`, `anchor-nuances`).

After writing the page, add the slug to `docs/Senseml reference/concepts/_order.yaml`. Insert it in a thematically logical position — group it near related concepts (e.g., LLM concepts near other LLM entries, layout concepts near lines/anchor entries).

## Step 4 — Branch, commit, and open a PR

Branch naming: `fe_<short_description>_docs` (Frances's initials, since you're acting on her behalf).

```
git checkout -b fe_<short_description>_docs
git add docs/Senseml\ reference/concepts/<slug>.md docs/Senseml\ reference/concepts/_order.yaml
git commit -m "docs: add <concept name> concept topic

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push -u origin fe_<short_description>_docs
gh pr create --title "docs: add <concept name> concept topic" --body "..."
```

PR body should include:
- What concept the page covers and why it's useful
- Reference to any source PR if one was provided (`sensible-hq/sensible#<pr-number>`)
- A short test plan checklist for the reviewer (check page renders, cross-links resolve, _order.yaml entry appears in nav)

Return the PR URL to the user.
