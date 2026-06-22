---
name: blog-how-to-parse-x
description: Generates a "how to extract data from X" blog post draft for Sensible. Takes a document type as input and either fetches the matching prebuilt config from the open-source library, or accepts an explicit config file/URL and optional PDF path via --config and --pdf flags. Invoke whenever the user wants to write or draft a "how to parse/extract X" blog post.
argument-hint: <document type> [--config <path-or-url>] [--pdf <path>]
allowed-tools: Bash, Read, Write, WebFetch
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
python3 scripts/upload_pr_extractor.py \
  --doc-type [doc-type-slug] \
  --config [config-path] \
  --golden [pdf-path] \
  --config-name [config-stem]
```

Then run a live extraction against the golden PDF:

```bash
curl -s -X POST "https://api.sensible.so/v0/extract/[doc-type-slug]?configuration_name=[config-stem]" \
  -H "Authorization: Bearer ${SENSIBLE_API_KEY}" \
  -H "Content-Type: application/pdf" \
  --data-binary @"[pdf-path]" | python3 -m json.tool
```

Save the full `parsed_document` response — you will use it verbatim in Step 5. Print the Sensible app URL from `upload_pr_extractor.py` output to the terminal for the writer to verify (do NOT embed it in the draft).

If no `--pdf` was provided, leave output blocks as `[OUTPUT: run extraction to get real values]` placeholders and note this in the Step 6 summary.

## Step 5 — Draft the blog post

Write the full draft following `.claude/style-guide/blog-post-template.md` exactly. Use:
- Real field names and SenseML queries from the fetched config (Step 3), not invented examples
- Verbatim boilerplate sentences from the template, with `[variables]` filled in
- `[IMAGE: description]` markers as placeholders for screenshots — do not omit these
- Real output values from the Step 4 extraction — never invented

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

1. Find the fenced ` ```json5 ` block immediately following "Here's the complete SenseML config combining everything we've covered:" in the draft.
2. Write the block content (without the fences) to the combined post config path used in Step 4.

This ensures one enrichment pass covers everything — never enrich the draft and the config file separately.

## Step 7 — Present to user

Print the path to the saved draft and a short summary:
- Document type and variant used
- Fields demonstrated
- Which SenseML methods appear in the post
- Sensible app URL for the writer to verify the extraction
- Any config fields you flagged as unclear or that may need screenshot attention
