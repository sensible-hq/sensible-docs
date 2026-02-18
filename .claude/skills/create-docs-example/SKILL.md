---
name: create-docs-example
description: Given an extractor directory path from the sensible engine repo, create or update a full-fledged documentation example — copying the golden PDF, generating a screenshot, assessing and redacting PII, and writing the example section with JSON5 comments.
argument-hint: <path/to/extractor/dir> [doc-page-path]
disable-model-invocation: true
allowed-tools: Bash(pdftotext:*), Bash(pdftoppm:*), Bash(python3:*), Bash(cp:*), Read, Glob, Edit, Write
---

You are adding or updating a documentation example in the sensible-docs repo based on an extractor directory from the sensible engine repo.

The arguments are: **$ARGUMENTS**

Parse the arguments as follows:
- **First token**: the extractor directory path (e.g. `extractors/sensible/removeLines`)
- **Second token** (optional): the path to the target doc page to update (e.g. `docs/Senseml reference/preprocessors/remove-lines.md`). If provided, skip Step 2 and use this path directly.

The sensible engine repo is at `../sensible` relative to this repo. So the full path to the extractor dir is `../sensible/<extractor-dir>`.

## Step 1 — Read the extractor

Read the config file(s) (e.g. `all.json`) and list the golden PDFs from the extractor directory:

```
../sensible/<extractor-dir>/
├── all.json          (or other named configs)
└── goldens/
    └── *.pdf
```

If there are multiple golden PDFs, use the first one unless the user specifies otherwise.

## Step 2 — Identify the target doc page

*Skip this step if a doc page path was provided as the second argument.*

Parse the extractor path to determine the doctype (the last path segment, e.g. `removeLines`).

Look for an existing doc page that corresponds to this feature. Likely locations:
- `docs/Senseml reference/preprocessors/`
- `docs/Senseml reference/layout-based-methods/`
- `docs/Senseml reference/llm-based-methods/`
- `docs/Senseml reference/computed-field-methods/`
- `docs/Senseml reference/field-query-object/`

If no existing page is found, note this and ask the user where to create it before proceeding.

## Step 3 — Copy the PDF and generate a screenshot

Choose a short, slug-style name for the assets (e.g. `remove_lines` for `removeLines`).

```bash
cp ../sensible/<extractor-dir>/goldens/<golden>.pdf assets/pdfs/<slug>.pdf
pdftoppm -r 150 -png -f 1 -l 1 assets/pdfs/<slug>.pdf /tmp/<slug>
cp /tmp/<slug>-1.png assets/images/final/<slug>.png
```

Then **view the rendered PNG** using the Read tool to see what the document looks like.

## Step 4 — Assess the PDF for PII

Extract the full text of the PDF:

```bash
pdftotext ../sensible/<extractor-dir>/goldens/<golden>.pdf -
```

Read the output carefully and assess whether the document contains personally identifiable information (PII) that should be redacted before publishing, including:
- Real names (student, patient, employee, customer, etc.)
- Government or institutional IDs (SSN, student IDs, employee IDs, etc.)
- Real addresses, phone numbers, or email addresses
- Real institution names that shouldn't be published (e.g. real college names in a student record)
- Any other sensitive personal details

**If PII is found:** Generate appropriate fake replacements. Use clearly fictional values:
- Names: common, generic names that are obviously placeholders (e.g. "García, Ana López" as a Spanish-language Jane Doe equivalent, "Smith, Jane" for English)
- IDs: obviously fake numbers (e.g. `A12345678`, `123-45-6789`)
- Institutions: "Fictional College", "Sample Company", etc.
- Keep the overall structure realistic — don't replace so much that the document loses its illustrative value

Then call the redaction script. Set `"bold": true` for text that appears bold in the PDF:

```bash
python3 scripts/redact_pdf.py \
  --input  assets/pdfs/<slug>.pdf \
  --output assets/pdfs/<slug>.pdf \
  --replacements '[
    {"find": "Real Name",   "replace": "Fake Name",   "bold": true},
    {"find": "REAL-ID-123", "replace": "FAKE-ID-000", "bold": true}
  ]'
```

After redacting, regenerate the screenshot:

```bash
pdftoppm -r 150 -png -f 1 -l 1 assets/pdfs/<slug>.pdf /tmp/<slug>_redacted
cp /tmp/<slug>_redacted-1.png assets/images/final/<slug>.png
```

View the new screenshot to confirm the redactions look correct.

**If no PII is found:** skip redaction and proceed.

## Step 5 — Write the example section

Update the `# Examples` section of the target doc page. Follow these conventions exactly:

**One example, one config.** Don't split into sub-examples with `##` headings unless the features are truly independent. If the extractor config uses multiple preprocessors or options together, present them as a single unified example.

**Intro:** One short paragraph (2–4 sentences) describing what the example shows and why. Use a bullet list if there are multiple distinct things happening in the config (e.g. two preprocessors doing different things). Reference the actual document type (e.g. "academic transcript", "insurance quote") not just "a document".

**Config block:** Use ` ```json ` fenced code blocks. Add `/* inline comments */` (JSON5 style) to label each significant section or preprocessor — this repo supports JSON5. Comments should explain the *why*, not just restate the key name.

**Example document section:**

```markdown
**Example document**

<one sentence describing what to notice in the document — e.g. what will be removed or changed by the preprocessor>

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/<slug>.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/<slug>.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------- |
```

**Output block:** Use the actual extraction output. If the output value is a long string, truncate it with `...` after ~200 characters. Strip metadata fields (`classificationSummary`, `coverage`, `errors`, `fileMetadata`, etc.) — show only the `parsedDocument` contents. Use the redacted values in the output if you redacted the PDF.

## Step 6 — Commit

Stage only the files you changed:

```bash
git add assets/pdfs/<slug>.pdf assets/images/final/<slug>.png "<doc-page-path>"
git commit -m "docs: add example for <feature>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push
```

Report back with what was done, whether PII was found and redacted, and the path to the updated doc page.
