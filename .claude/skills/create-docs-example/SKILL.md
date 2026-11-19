---
name: create-docs-example
description: Given an extractor directory path from the sensible engine repo, create or update a full-fledged documentation example — copying the golden PDF, generating a screenshot, assessing and redacting PII, and writing the example section with JSON5 comments. Handles single doc type extractors and portfolio extractors (a `multi.json`), and can write the example as a standalone draft page.
argument-hint: "<path/to/extractor/dir> [doc-page-path | standalone]"
disable-model-invocation: true
allowed-tools: Bash(pdftotext:*), Bash(pdftoppm:*), Bash(python3:*), Bash(cp:*), Bash(curl:*), Read, Glob, Edit, Write
---

You are adding or updating a documentation example in the sensible-docs repo based on an extractor directory from the sensible engine repo.

The arguments are: **$ARGUMENTS**

Parse the arguments as follows:
- **First token**: the extractor directory path (for example, `extractors/sensible/removeLines`)
- **Second token** (optional): the path to the target doc page to update (for example, `docs/Senseml reference/preprocessors/remove-lines.md`). If provided, skip Step 2 and use this path directly. The word `standalone` instead means: write the example as a new hidden draft page, `docs/<section>/draft-<slug>-example.md` with `hidden: true` in its front matter and no `_order.yaml` entry, in the section where the feature's docs will live.

The sensible engine repo is at `../sensible` relative to this repo. So the full path to the extractor dir is `../sensible/<extractor-dir>`.

## Step 1 — Read the extractor

Read the config file(s) (for example, `all.json`) and list the golden PDFs from the extractor directory:

```
../sensible/<extractor-dir>/
├── all.json          (or other named configs)
└── goldens/
    └── *.pdf
```

If there are multiple golden PDFs, use the first one unless the user specifies otherwise.

**Portfolio extractors.** A directory with a `multi.json` instead of a config is a portfolio test. `multi.json` lists the portfolio's doc types in `types` plus any portfolio options, such as `fallback_type`. Each doc type's configs live in a sibling directory, `../sensible/<customer>/<doc_type>/`. Read those too, and read the golden's `.extracted.csv` for the expected page ranges.

## Step 2 — Identify the target doc page

*Skip this step if a doc page path was provided as the second argument.*

Parse the extractor path to determine the doctype (the last path segment, for example, `removeLines`).

Look for an existing doc page that corresponds to this feature. Likely locations:
- `docs/Senseml reference/preprocessors/`
- `docs/Senseml reference/layout-based-methods/`
- `docs/Senseml reference/llm-based-methods/`
- `docs/Senseml reference/computed-field-methods/`
- `docs/Senseml reference/field-query-object/`

If no existing page is found, note this and ask the user where to create it before proceeding.

## Step 3 — Copy the PDF and generate a screenshot

Choose a short, slug-style name for the assets (for example, `remove_lines` for `removeLines`).

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
- Real institution names that shouldn't be published (for example, real college names in a student record)
- Any other sensitive personal details

**If PII is found:** Generate appropriate fake replacements. Use clearly fictional values:
- Names: common, generic names that are obviously placeholders (for example, "García, Ana López" as a Spanish-language Jane Doe equivalent, "Smith, Jane" for English)
- IDs: obviously fake numbers (for example, `A12345678`, `123-45-6789`)
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

**If the PII can't be redacted** — for example, it's in scanned pages, which `redact_pdf.py` can't edit, or it's on so many pages that the document stops being useful — don't publish the golden. Build a substitute from documents already published in `assets/pdfs/` that shows the same behavior, and write configs for it. For a portfolio, combine pages with `pdfseparate` and `pdfunite`, and prefer extending an example the docs already have, such as the Fingerprint example in `docs/document extraction/portfolio.md`. Tell the user the golden was replaced, and why.

## Step 5 — Upload config and get actual extraction output

Upload the config and the (potentially redacted) golden to the Sensible account, then run a live extraction to get the JSON output to use in the example.

**Which account.** Use `SENSIBLE_TEST_API_KEY` and `https://api.sensible.so/v0` unless the user names another account. A feature that isn't in production yet needs the dev API, `https://api.sensible.so/dev`, with the dev key the user names, such as `SENSIBLE_DEV_API_KEY`. `upload_pr_extractor.py` reads `SENSIBLE_API_KEY` and `/v0`, so for any other account, run it through a small wrapper that sets its `API_BASE` and `get_api_key` before calling `main()`. Never print a key.

```bash
python3 scripts/upload_pr_extractor.py \
  --doc-type <doctype> \
  --config ../sensible/<extractor-dir>/<config>.json \
  --golden assets/pdfs/<slug>.pdf \
  --config-name <config_stem>
```

The script creates the document type if it doesn't exist, publishes the config to production, and uploads the golden as a reference document. It prints a Sensible app URL — open it to visually confirm the extraction looks correct before writing the example.

Then run a live extraction to get the JSON output:

```bash
curl -s -X POST "https://api.sensible.so/v0/extract/<doctype>" \
  -H "Authorization: Bearer ${SENSIBLE_API_KEY}" \
  -H "Content-Type: application/pdf" \
  --data-binary @assets/pdfs/<slug>.pdf | python3 -m json.tool
```

For a portfolio, upload each doc type's configs, then run an asynchronous portfolio extraction instead: `POST /generate_upload_url` with `types`, `content_type`, and any portfolio options from `multi.json`, `PUT` the PDF to the returned `upload_url`, and poll `GET /documents/<id>` until `status` is `COMPLETE`. Compare each document's `documentType`, `configuration`, `startPage`, and `endPage` with the expected page ranges before you write anything. When the feature changes which pages are extracted, also run the request without the feature, so the page can say what happens without it.

Use the `parsed_document` from this response as the **Output** in the example. Strip metadata fields (`classificationSummary`, `coverage`, `errors`, `fileMetadata`, etc.) — show only the extracted field values.

## Step 6 — Write the example section

Update the `# Examples` section of the target doc page. Follow these conventions exactly:

**One example, one config.** Don't split into sub-examples with `##` headings unless the features are truly independent. If the extractor config uses multiple preprocessors or options together, present them as a single unified example.

**Intro:** One short paragraph (2–4 sentences) describing what the example shows and why. Use a bullet list if there are multiple distinct things happening in the config (for example, two preprocessors doing different things). Reference the actual document type (for example, "academic transcript", "insurance quote") not just "a document".

**Config block:** Use ` ```json ` fenced code blocks. Add `/* inline comments */` (JSON5 style) to label each significant section or preprocessor — this repo supports JSON5. Comments should explain the *why*, not just restate the key name.

**Example document section:**

```markdown
**Example document**

<one sentence describing what to notice in the document — for example, what will be removed or changed by the preprocessor>

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/<slug>.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/<slug>.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------- |
```

**Portfolio example layout:** follow the Fingerprint example in `docs/document extraction/portfolio.md`: a `### Config` section with a `**_Document type N_**` block per doc type (doc type, config name, config content, or a link to where an existing example defines it), an example document table, then `### Output` with the numbered `extract_from_url` and `GET /documents` curl steps. The request names the doc types and every portfolio option the example needs. Show the output per document under `#### Page N | <doc type> | <config>` headings, as the LLM example on that page does, with 1-based page numbers in the headings, and say that the response's `startPage` and `endPage` are zero-based.

**Output block:** Use the actual extraction output. If the output value is a long string, truncate it with `...` after ~200 characters. Strip metadata fields (`classificationSummary`, `coverage`, `errors`, `fileMetadata`, etc.) — show only the `parsedDocument` contents. Use the redacted values in the output if you redacted the PDF.

## Step 7 — Commit

Stage only the files you changed:

```bash
git add assets/pdfs/<slug>.pdf assets/images/final/<slug>.png "<doc-page-path>"
git commit -m "docs: add example for <feature>

<Co-Authored-By line from this session's attribution instructions>"
git push
```

Report back with what was done, whether PII was found and redacted, and the path to the updated doc page.
