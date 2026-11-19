---
name: docs-checker
description: 'Checks Sensible documentation files for terminology violations before publishing. Invoke whenever the user wants to check, review, validate, or proofread a Sensible doc (changelog, reference page, integration guide, concept topic), or asks whether a file uses correct terminology. Accepts a file path, pasted content, or both. Also invoke if the user asks to "run the checker" or "check terminology". It checks terminology and doesn''t edit code blocks; to add JSON5 comments, use json5-commenter.'
---

# Sensible Docs Terminology Checker

<!-- rule: sensible-terminology -->

Check a doc for terminology violations and optionally fix them. Vale does the lookup; you judge only the terms a pattern can't settle.

## Step 1: Get the content

- If the user gave a file path, use it.
- If the user pasted content, write it to a scratch file named `check.md` (or `check-changelog.md` for a changelog, so the changelog rules apply) and use that.

## Step 2: Run Vale's terminology rules

<!-- rule: sensible-terminology -->

From the repo root:

```bash
vale --output=line --filter='.Name in ["Sensible.Terminology","Sensible.UINames","Sensible.ModelNames","Sensible.InternalTerms","Vale.Avoid"]' <file>
```

These rules carry every avoid-term in `.claude/style-guide/glossary.md` that a pattern settles, plus the vocabulary's reject list (`Vale.Avoid`: "parse", "dashboard", and others). They skip code blocks, inline code, and frontmatter.

## Step 3: Judge the context terms

Some glossary terms have a legitimate meaning elsewhere, so no pattern can flag them. <!-- rule: sensible-context-terms --> Search the prose (not code) for these and decide each hit:

| term | fine when | wrong when |
| ---- | --------- | ---------- |
| response | it means the API response envelope | it means the extracted output ("the response contains your fields") → "output" |
| segment | it means a portfolio segment | it means a scored portion of the document → "chunk" |
| section | it means the SenseML Sections feature | it means a chunk |
| key | it means a JSON key | it means a field → "field" |
| empty | it describes a string or array | it means an extraction returned nothing → "null" |
| free form / free-form | hyphenated before a noun ("free-form documents"), open after a verb ("is free form") | the other way round |

The full rule is `style-rules/judgment/sensible-context-terms.yaml`.

## Step 4: Report

<!-- rule: sensible-terminology --> <!-- rule: sensible-ui-names -->

If you found violations, output this table, then a summary line:

| Line | Found | Should be | Source |
|------|-------|-----------|--------|
| 12 | "the UI" | "the Sensible app" | Vale |
| 34 | "response" | "output" | judgment |

If there are none, say "No terminology violations found."

## Step 5: Offer to fix

<!-- rule: sensible-terminology -->

Ask: "Fix all, fix specific lines, or skip?"

If fixing:
1. Apply the substitutions.
2. When a term maps to more than one replacement ("config" or "configuration"), ask which to use.
3. Keep the original capitalization.
4. Show the diff before writing, and write only after the user confirms.
