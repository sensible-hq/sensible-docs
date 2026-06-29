---
name: blog-how-to-parse-x
description: Generates a "how to extract data from X" blog post draft for Sensible. Takes a document type as input and either fetches the matching prebuilt config from the open-source library, or accepts an explicit config file/URL and optional PDF path via --config and --pdf flags. Invoke whenever the user wants to write or draft a "how to parse/extract X" blog post.
argument-hint: <document type> [--config <path-or-url>] [--pdf <path>]
allowed-tools: Bash, Read, Write, WebFetch, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-create-pages, mcp__claude_ai_Notion__notion-update-page, mcp__vale__check_file
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

**Pause here and present the following to the user for approval before continuing:**

1. The field inventory and proposed fields (as above).

2. **Intro framing variant** — state which variant applies and show the evidence:
   - List any LLM methods present (`queryGroup`, `list`, `nlpTable`), or confirm none if the config is fully deterministic.
   - State the implied variant: A (deterministic-primary), B (LLM-primary), or C (hybrid).
   - Give a one-sentence summary of what the framing paragraph will say.

3. **Title form** — "with LLMs and Sensible" or "with Sensible", and why.

4. **Vendor/variant** — the specific variant used, if any (e.g., "Sun Life commission statements").

5. **Fingerprint** — present or absent; if present, it will appear in "Putting it all together".

Ask:
> "Does this field selection look right? And for the intro framing: I'm planning **Variant [X]** — [one-sentence summary]. Does that match what you had in mind? Any adjustments before I proceed?"

Do not move to Step 4 until the user confirms or adjusts both the field selection and the intro framing.

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

Save the full `parsed_document` from `--output` — you will use it verbatim in Step 5.

**Mandatory checkpoint — do this before Step 5:** Parse the Sensible app URL from the script's stdout (the line starting "View in Sensible app:") and output it to the user in a response. Do not proceed to Step 5 until you have explicitly printed the URL. Do NOT embed it in the draft.

If no `--pdf` was provided, leave output blocks as `[OUTPUT: run extraction to get real values]` placeholders and note this in the Step 6 summary.

## Step 5 — Draft the blog post

Write the full draft following `.claude/style-guide/blog-post-template.md` exactly. Use:
- Real field names and SenseML queries from the fetched config (Step 3), not invented examples
- Verbatim boilerplate sentences from the template, with `[variables]` filled in
- `[IMAGE: description]` markers as placeholders for screenshots — do not omit these
- Real output values from the Step 4 extraction — never invented

**Code block length:** Individual field code blocks must not exceed 75 lines (not counting the "Putting it all together" block). For sections fields with many sub-fields, choose 1–2 of the most illustrative ones. For deeply nested sections (3+ levels), limit to 1 sub-field — the structural wrapper alone consumes ~40 lines before any fields are added.

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

Then upload the combined config and run extraction to get the verifiable app URL for the post:

```bash
python3 .claude/skills/blog-how-to-parse-x/upload_and_extract.py \
  --doc-type [doc-type-slug] \
  --config [combined-post-config-path] \
  --pdf [pdf-path] \
  --config-name [doc-type-slug]_blog \
  --output /tmp/[doc-type-slug]_blog_extraction.json
```

**Mandatory checkpoint:** Parse the "View in Sensible app:" URL from the script's stdout and output it to the user in a response before proceeding. This is the URL the writer uses to verify the post's config — it must point to the combined blog config, not the original full config.

## Step 6.6 — Cross-check individual output blocks

The "Putting it all together" output block is the source of truth — it comes from a real extraction of the full combined config. Go back through each individual field section in the draft and verify that every output value matches the corresponding field in the "Putting it all together" output. Update any individual block that disagrees.

Do this before moving to Step 7 — do not present a draft where individual and combined outputs contradict each other.

## Step 6.7 — Style and terminology check

Run all checks in order. Fix issues before proceeding to Step 7.

**6.7a — Vale:**

Use `mcp__vale__check_file` on `drafts/blog-[doc-type-slug].md`. Fix all **errors** and **warnings**. Suggestions are optional — apply if clearly right, skip if they conflict with existing blog conventions.

**6.7b — Writing rules:**

Read `.claude/style-guide/writing-rules.md`. Check the draft for: em dashes (split into two sentences), passive voice (use "Sensible" or "you" as explicit subject), extraction phrasing ("using" not "against"), gerunds over nominalizations, and tone (no filler phrases). Fix all violations.

**6.7c — Naming conventions:**

Read the "Formatting conventions" section of `.claude/style-guide/style-guide-overview.md`. Apply these rules to the draft prose:
- **Method and feature names:** Title Case, never camelCase-in-backticks. "the Query Group method", not "the `` `queryGroup` `` method". "Sections", not "`sections`".
- **Parameter names:** Title Case in prose, no backticks. "the Stop parameter", not "the `stop` parameter".
- **JSON keys and enum values:** backtick in prose — `"position"`, `"below"`.

**6.7d — Code comment style:**

Read the "Code examples: inline comments" section of `.claude/style-guide/sentence-word-guidance.md`. Comments must explain non-obvious choices, not restate what the parameter name already says. Remove or rewrite redundant comments (e.g., `/* set position to below */`).

**6.7e — Glossary:**

Read `.claude/style-guide/glossary.md`. Fix any term in the prose (not in code blocks) that appears in the "Avoid" column.

**6.7f — Code block length:**

Run this check. Any individual field code block over 75 lines must be trimmed before proceeding:

```bash
python3 -c "
import re
content = open('drafts/blog-[doc-type-slug].md').read()
content = re.sub(r'## Putting it all together.*?(?=\n## |\Z)', '', content, flags=re.DOTALL)
tick3 = chr(96) * 3
blocks = re.findall(tick3 + r'(?:json|json5)\n(.*?)\n' + tick3, content, re.DOTALL)
for i, b in enumerate(blocks, 1):
    n = b.count('\n') + 1
    print(f'Block {i}: {n} lines' + ('  *** OVER LIMIT' if n > 75 else ''))
"
```

Only proceed to Step 7 once all checks are clean.

## Step 7 — Present to user

Print the path to the saved draft and a short summary:
- Document type and variant used
- Fields demonstrated
- Which SenseML methods appear in the post
- Sensible app URL for the writer to verify the extraction
- Any config fields you flagged as unclear or that may need screenshot attention

## Step 8 — Publish draft to Notion

Push the draft to the Sensible Content Tracker so the blog writer can review and track it.

**Preferred path:** If `NOTION_API_KEY` is available (a Notion internal integration token), use `publish_to_notion.py` — it parses markdown into proper Notion block types and is fully deterministic:

```bash
python3 .claude/skills/blog-how-to-parse-x/publish_to_notion.py \
  --draft drafts/blog-[doc-type-slug].md \
  --parent-id [main-page-id]
```

**Fallback path (no API key):** Use the MCP tools with the verbatim-passthrough protocol described below.

---

### MCP fallback protocol

The only reason MCP publishes have gone wrong is Claude rewriting draft content from memory instead of reading it from disk. The protocol below prevents that.

**8a — Search for an existing Content Tracker entry:**

Use `notion-search` with the blog post title, scoped to the Content Tracker data source:
- `query`: the blog post title
- `data_source_url`: `collection://31bc7dd4-9788-8031-9dd4-000b769e5374`

**8b — If no main page exists (first publish):**

Create the main Content Tracker entry with `notion-create-pages`:
- `parent`: `{ "type": "data_source_id", "data_source_id": "31bc7dd4-9788-8031-9dd4-000b769e5374" }`
- `properties`:
  - `Content`: blog post title
  - `Category`: `Document Type Blog Posts`
  - `Status`: `In progress`
- `content`: `Draft versions are in child pages below.`

Save the returned page ID as `[main-page-id]`.

**8c — Preprocess the draft:**

Strip HTML comments — they silently truncate all Notion page content after the first `<!--` tag:

```bash
python3 -c "
import re
content = open('drafts/blog-[doc-type-slug].md').read()
print(re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL))
" > /tmp/[doc-type-slug]_notion.md
```

**8d — Read the preprocessed file:**

Use the Read tool on `/tmp/[doc-type-slug]_notion.md`. Do this immediately before the Notion tool call — do NOT use draft content from memory or from earlier in context.

**8e — Create the child page:**

Use `notion-create-pages` with the content read verbatim from the file in 8d:
- `parent`: `{ "type": "page_id", "page_id": "[main-page-id]" }`
- `title`: `Draft v[N] — [YYYY-MM-DD]` (determine N by fetching children of `[main-page-id]` and finding the highest existing version)
- `content`: **the exact text returned by Read in step 8d — do not paraphrase, summarize, or reconstruct any part of it**

The Notion markdown parser treats fenced code blocks as literal — `/* */` inline comments inside ` ```json ` blocks are preserved as-is without any special handling.

After publishing, print the new child page URL so the writer can review it.

Note: Notion displays child pages oldest-first in the sidebar. The writer can manually drag child pages to reorder them in the Notion UI.

## Maintaining this skill

If you modify any script in this directory (`upload_and_extract.py`, `extract_config_from_draft.py`, `test_blog_output.py`, `publish_to_notion.py`), run the test suite before committing:

```bash
python3 -m pytest .claude/skills/blog-how-to-parse-x/tests/ -v
```

All tests are fast and fully mocked — no API key needed. Integration tests (marked `@pytest.mark.integration`) are skipped by default.
