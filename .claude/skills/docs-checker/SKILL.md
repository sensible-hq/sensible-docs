---
name: docs-checker
description: Checks Sensible documentation files for terminology violations before publishing. Invoke whenever the user wants to check, review, validate, or proofread a Sensible doc (changelog, reference page, integration guide, concept topic), or asks whether a file uses correct terminology. Accepts a file path, pasted content, or both. Also invoke if the user asks to "run the checker" or "check terminology".
---

# Sensible Docs Terminology Checker

Check a doc for terminology violations against the Sensible glossary and optionally fix them.

## Step 1: Load the glossary

Read `.claude/style-guide/glossary.md` from the project root. This is the single source of truth. Both sections apply — universal terms for all content, SenseML-specific terms when checking a reference page (method, preprocessor, computed field method, anchor/match object pages).

If the file doesn't exist, stop and tell the user the glossary is missing from `.claude/style-guide/`.

## Step 2: Get the content

- If the user gave a file path, read the file and track line numbers.
- If the user pasted content, use that. Line numbers still apply — count from 1.
- If both, check the file.

## Step 3: Scan for violations

For each term in the "Avoid" column of the glossary:
- Check whether any of those exact strings appear in the doc body.
- **Skip**: fenced code blocks (` ``` ` ... ` ``` `), inline backtick spans (`` `...` ``), and YAML frontmatter (`---` ... `---` at the top of the file). Violations inside code are intentional.
- The "Avoid" column may list multiple comma-separated terms — check for each one individually.
- Matching is case-insensitive, but record the original casing so you can fix it correctly.

**Free-form hyphenation** is position-dependent (adjective before noun: "free-form documents"; predicate: "the document is free form") and hard to check reliably. Flag it if you're confident about the context, but note uncertainty when it's ambiguous.

## Step 4: Report

If violations found, output this table, then a summary line:

---
**Terminology violations: N**

| Line | Found | Should be | Scope |
|------|-------|-----------|-------|
| 12 | "the UI" | "the Sensible app" | universal |
| 34 | "template" | "config" or "configuration" | universal |
| 67 | "segment" | "chunk" | SenseML-specific |

*N violations across N rules.*

---

If no violations: say so — "No terminology violations found."

SenseML-specific violations are errors in any doc type — a changelog that says "segment" instead of "chunk" is wrong regardless of context.

## Step 5: Offer to fix

After the report, ask:

> Fix all, fix specific lines, or skip?

If fixing:
1. Apply the substitutions.
2. When one avoided term maps to multiple valid replacements (e.g., "config" or "configuration"), ask which to use before applying.
3. Preserve capitalization of the original: if the avoided term was title-cased, title-case the replacement.
4. Show the diff before writing.
5. Write the file only after the user confirms.
