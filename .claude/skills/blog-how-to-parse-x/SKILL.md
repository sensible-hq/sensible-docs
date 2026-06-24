---
name: blog-how-to-parse-x
description: Generates a "how to extract data from X" blog post draft for Sensible. Takes a document type as input and either fetches the matching prebuilt config from the open-source library, or accepts an explicit config file/URL and optional PDF path via --config and --pdf flags. Invoke whenever the user wants to write or draft a "how to parse/extract X" blog post.
argument-hint: <document type> [--config <path-or-url>] [--pdf <path>]
allowed-tools: Bash, Read, Write, WebFetch, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-create-pages, mcp__claude_ai_Notion__notion-update-page
---

Generate a "how to extract data from [document type]" blog post draft.

## Parse arguments

**$ARGUMENTS** supports two input modes:

**Mode A — document type only** (skill fetches config from the open-source library):
```
pay stubs
"commission statements"
```

**Mode B — explicit config and/or PDF** (skip library lookup):
```
pay stubs --config /path/to/config.json
pay stubs --config https://raw.githubusercontent.com/.../config.json
pay stubs --config /path/to/config.json --pdf /path/to/example.pdf
```

Parse the document type from everything before `--config` or `--pdf`. If `--config` is provided, skip Steps 2–3 and use it directly. If `--pdf` is provided, note the path for use in Step 4 when writing the example document section.

## Step 1 — Read style guidance

Read these files in parallel before writing anything:
- `.claude/style-guide/blog-post-template.md` — structure, section patterns, and verbatim boilerplate sentences
- `.claude/style-guide/json5-comments-reference.md` — canonical inline comments for every SenseML parameter

## Step 2 — Look up the document type in the config library

_Skip this step if `--config` was provided._

Fetch the config library index to find the matching category and document type:

```
https://raw.githubusercontent.com/sensible-hq/sensible-configuration-library/main/README.md
```

Find the entry for the requested document type. Note the category and the exact folder name used in the library.

## Step 3 — Fetch a prebuilt config

_Skip this step if `--config` was provided._

Browse the configurations directory for the matched document type:

```
https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/[Category]/[Doc Type]/configurations
```

Pick one configuration file and fetch its raw content:

```
https://raw.githubusercontent.com/sensible-hq/sensible-configuration-library/main/templates/[Category]/[Doc Type]/configurations/[filename].json
```

**If `--config` was provided**, read or fetch it now instead of the above.

Produce a full field inventory before selecting examples. Structure it in two parts:

**Top-level fields** (a table of all fields at the root of `"fields": []`):

| Field | Type | Method | Notes |
|---|---|---|---|
| `field_id` | type | method + key params | one-line note on demo value |

**One block per `sections` field** (do not merge sections sub-fields into the top-level table):

> **`[sections_field_id]` — sections field** (one sentence describing what it repeats over):
>
> | Sub-field | Type | Method | Notes |
> |---|---|---|---|
> | `sub_field_id` | type | method + key params | one-line note |

After the inventory, propose 2–4 fields to demonstrate and state explicit reasoning for each choice — e.g. method complexity, reader value, uniqueness to the document type. Eliminate fields with redundant methods unless there's a specific reason to include them.

**Pause here and present the inventory + proposed fields to the user for approval before continuing.** Ask:
> "Does this field selection look right? Any you'd swap in or out before I proceed?"

Do not move to Step 4 until the user confirms or adjusts the selection.

Also note:
- Whether the config uses LLM-based methods (`queryGroup`, `list`, `nlpTable`) — determines whether the title includes "with LLMs and Sensible" or just "with Sensible"
- The specific vendor/variant used, if any (e.g., "ADP pay stubs")
- Whether a `fingerprint` is present — if so, it must appear in the "Putting it all together" code block

## Step 4 — Upload config and run live extraction

**Do this before writing any output block.** Never invent or infer output — all output blocks must come from real API responses.

If a `--pdf` was provided:

```bash
python3 .claude/skills/blog-how-to-parse-x/upload_and_extract.py \
  --doc-type [doc-type-slug] \
  --config [config-path] \
  --pdf [pdf-path] \
  --config-name [config-stem] \
  --output [output-path.json]
```

Save the full `parsed_document` from `--output` — you will use it verbatim in Step 5. Print the Sensible app URL the script emits to the terminal for the writer to verify (do NOT embed it in the draft).

If no `--pdf` was provided, leave output blocks as `[OUTPUT: run extraction to get real values]` placeholders and note this in the Step 6 summary.

## Step 5 — Draft the blog post

Write the full draft following `.claude/style-guide/blog-post-template.md` exactly. Use:
- Real field names and SenseML queries from the fetched config (Step 3), not invented examples
- Verbatim boilerplate sentences from the template, with `[variables]` filled in
- `[IMAGE: description]` markers as placeholders for screenshots — do not omit these
- Real output values from the Step 4 extraction — never invented

**If the config has a `fingerprint`:** include the `## [CONDITIONAL] Identify and classify incoming [doc types]` section from the template. Place it before the first field extraction section. The fingerprint must also appear in the "Putting it all together" code block.

In the "Putting it all together" section, wrap the `json5` code block with extraction markers:

```
<!-- CONFIG:START -->
```json5
...
```<!-- CONFIG:END -->
```

Save the draft to:
```
drafts/blog-[doc-type-slug].md
```

## Step 6 — Enrich JSON5 comments

After saving the draft, invoke the `json5-commenter` skill on it:

```
json5-commenter drafts/blog-[doc-type-slug].md
```

This adds canonical inline comments to every SenseML code block using `.claude/style-guide/json5-comments-reference.md` as the source. Do not skip this step.

## Step 6.5 — Sync combined config file from draft

The draft is the single source of truth for SenseML configs. After json5-commenter completes, extract the enriched "Putting it all together" code block and overwrite the combined post config file so both are identical:

```bash
python .claude/skills/blog-how-to-parse-x/extract_config_from_draft.py \
  drafts/blog-[doc-type-slug].md \
  [combined-post-config-path]
```

This ensures one enrichment pass covers everything — never enrich the draft and the config file separately.

## Step 6.6 — Cross-check individual output blocks

The "Putting it all together" output block is the source of truth — it comes from a real extraction of the full combined config. Go back through each individual field section in the draft and verify that every output value matches the corresponding field in the "Putting it all together" output. Update any individual block that disagrees.

Do this before moving to Step 7 — do not present a draft where individual and combined outputs contradict each other.

## Step 7 — Present to user

Print the path to the saved draft and a short summary:
- Document type and variant used
- Fields demonstrated
- Which SenseML methods appear in the post
- Sensible app URL for the writer to verify the extraction
- Any config fields you flagged as unclear or that may need screenshot attention

## Step 8 — Publish draft to Notion

Push the draft to the Sensible Content Tracker so the blog writer can review and track it.

**8a — Search for an existing Content Tracker entry:**

Use `notion-search` with the blog post title, scoped to the Content Tracker data source:
- `query`: the blog post title
- `data_source_url`: `collection://31bc7dd4-9788-8031-9dd4-000b769e5374`

**8b — If no page exists (first publish):**

Use `notion-create-pages` with:
- `parent`: `{ "type": "data_source_id", "data_source_id": "31bc7dd4-9788-8031-9dd4-000b769e5374" }`
- `properties`:
  - `Content`: blog post title
  - `Category`: `Document Type Blog Posts`
  - `Status`: `In progress`
- `content`: version header followed by the full draft content:

```
**Draft v1 — [YYYY-MM-DD]**

[full draft content verbatim from drafts/blog-[doc-type-slug].md]
```

**8c — If a page already exists (revision):**

The page accumulates versions — each publish prepends a new version at the top; all prior versions remain below dividers. Do NOT replace the page content.

1. Use `notion-fetch` on the existing page ID to find the current version number. The fetch result may be very large — use `python3` to read just the first 500 characters from the saved result file and grep for a line matching `**Draft vN**`:

```bash
python3 -c "
import json, re, sys
with open('[tool-result-file]') as f:
    text = json.load(f)[0]['text']
m = re.search(r'\*\*Draft v(\d+)', text[:500])
print(m.group(1) if m else 'not found')
"
```

2. Increment the version number by 1.

3. Use `notion-update-page` with `insert_content` at start — the new block ends with a `---` divider so it separates cleanly from the prior version below:

```
notion-update-page
  page_id: [existing page ID]
  command: insert_content
  position: { type: start }
  content:
    **Draft v[N+1] — [YYYY-MM-DD]**

    [full draft content verbatim from drafts/blog-[doc-type-slug].md]

    ---
```

After publishing, print the Notion page URL so the writer can review it.

## Maintaining this skill

If you modify any script in this directory (`upload_and_extract.py`, `extract_config_from_draft.py`, `test_blog_output.py`), run the test suite before committing:

```bash
python3 -m pytest .claude/skills/blog-how-to-parse-x/tests/ -v
```

All tests are fast and fully mocked — no API key needed. Integration tests (marked `@pytest.mark.integration`) are skipped by default.
