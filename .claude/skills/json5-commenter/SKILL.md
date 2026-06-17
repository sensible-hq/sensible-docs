---
name: json5-commenter
description: Enriches JSON5 code blocks in a Sensible doc or blog post draft with canonical inline comments. Reads the comment reference, finds every fenced code block in the target file, and adds the canonical comment for each parameter that has one. Does not invent comments — only uses comments from the reference file. Use this skill before publishing any doc or blog post that contains SenseML code examples.
argument-hint: <path/to/draft.md>
allowed-tools: Read, Edit
---

Enrich the JSON5 code blocks in the file at **$ARGUMENTS**.

## Step 1 — Read inputs

Read both files in parallel:
- The target file: **$ARGUMENTS**
- The comment reference: `.claude/style-guide/json5-comments-reference.md`

## Step 2 — Find all JSON5 code blocks

Identify every fenced code block in the target file (` ```json `, ` ```json5 `, or ` ``` ` blocks that contain SenseML). Ignore non-SenseML blocks (e.g. shell commands, plain JSON output blocks showing extraction results).

## Step 3 — Enrich each block

For each code block, apply these rules in order:

**3a. Add the JSON5 header comment** if the block doesn't already have it as its first line:
```
/* Sensible uses JSON5 to support in-line comments*/
```

**3b. For each parameter key in the block**, look it up in the reference file. If a canonical comment exists for that key:
- Add it inline at the end of that line, as `/* comment text */`
- Preserve any existing comment — if a comment is already present, skip that line (don't replace it)
- Only use comments verbatim from the reference. Do not invent or paraphrase.

**3c. Do not comment output blocks.** Output blocks show extraction results (they contain fields like `"value"`, `"type"`, `"confidenceSignal"`). Leave these uncommented.

## Step 4 — Write changes

Use Edit to write back each modified code block. Make one Edit call per code block changed — don't rewrite the whole file.

## Step 5 — Report

After all edits, print a short summary:
- How many code blocks were found
- How many were modified
- For each modified block: which parameters got comments added
- Flag any parameters that appear in the code blocks but have no entry in the reference (don't add comments for these, just flag them)
