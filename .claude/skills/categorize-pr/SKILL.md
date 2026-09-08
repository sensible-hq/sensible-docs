---
name: categorize-pr
description: Given a PR number from sensible-hq/sensible (or sensible-hq/sensible-app), returns a disposition — document, investigate, or skip — with a brief reason. Used by the changelog fetch flow and the docs auto-scanner to decide whether a PR needs documentation work.
argument-hint: <pr-number> [sensible|sensible-app] (repo defaults to sensible)
disable-model-invocation: true
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*)
---

Given a PR, determine whether it needs documentation work.

Parse **$ARGUMENTS**:
- **First token**: PR number
- **Second token** (optional): `sensible` or `sensible-app` — defaults to `sensible`

## Step 1 — Fetch the PR

```bash
gh pr view <pr-number> --repo sensible-hq/<repo> --json number,title,body,labels,mergedAt,files
```

Read the title, body, labels, and changed files. Note any labels — a `docs_needed` label is a direct signal to return `document`.

## Step 2 — Read the categorization rules

Read `.claude/skills/changelog/references/categorization-rules.md` before making any call. Apply the rules as written.

## Step 3 — Return the disposition

Output exactly this format:

```
PR #NNNN — <title>

Disposition: document | investigate | skip
Reason: <one sentence>
```

If `document`, also add:
```
Docs action: update existing page | create new page | both
Likely affected area: <e.g. "layout-based-methods/region.md", "preprocessors/", "api/">
```

Do not add any other commentary. The caller (scanner or human) uses this output to decide next steps.
