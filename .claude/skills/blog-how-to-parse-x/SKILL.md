---
name: blog-how-to-parse-x
description: Generates a "how to extract data from X" blog post draft for Sensible. Takes a document type as input, fetches the prebuilt SenseML config from the open-source library to get real field names and queries, and drafts the full post using the house template. Invoke whenever the user wants to write or draft a "how to parse/extract X" blog post.
argument-hint: <document type> [e.g. "pay stubs", "W-2s", "commission statements"]
allowed-tools: Bash, Read, Write, WebFetch
---

Generate a "how to extract data from [document type]" blog post draft.

Parse **$ARGUMENTS** as the document type to write about.

## Step 1 — Read style guidance

Read these files in parallel before writing anything:
- `.claude/style-guide/blog-post-template.md` — structure, section patterns, and verbatim boilerplate sentences
- `.claude/style-guide/json5-comments-reference.md` — canonical inline comments for every SenseML parameter

## Step 2 — Look up the document type in the config library

Fetch the config library index to find the matching category and document type:

```
https://raw.githubusercontent.com/sensible-hq/sensible-configuration-library/main/README.md
```

Find the entry for the requested document type. Note the category and the exact folder name used in the library.

## Step 3 — Fetch a prebuilt config

Browse the configurations directory for the matched document type:

```
https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/[Category]/[Doc Type]/configurations
```

Pick one configuration file and fetch its raw content:

```
https://raw.githubusercontent.com/sensible-hq/sensible-configuration-library/main/templates/[Category]/[Doc Type]/configurations/[filename].json
```

From the config, extract:
- 2–4 representative field names and their methods (to use as the post's extraction examples)
- Whether the config uses LLM-based methods (`queryGroup`, `list`, `nlpTable`) — determines whether the title includes "with LLMs and Sensible" or just "with Sensible"
- The specific vendor/variant used, if any (e.g., "ADP pay stubs")

## Step 4 — Draft the blog post

Write the full draft following `.claude/style-guide/blog-post-template.md` exactly. Use:
- Real field names and SenseML queries from the fetched config (Step 3), not invented examples
- Verbatim boilerplate sentences from the template, with `[variables]` filled in
- `[IMAGE: description]` markers as placeholders for screenshots — do not omit these

Save the draft to:
```
drafts/blog-[doc-type-slug].md
```

## Step 5 — Enrich JSON5 comments

After saving the draft, invoke the `json5-commenter` skill on it:

```
json5-commenter drafts/blog-[doc-type-slug].md
```

This adds canonical inline comments to every SenseML code block using `.claude/style-guide/json5-comments-reference.md` as the source. Do not skip this step.

## Step 6 — Present to user

Print the path to the saved draft and a short summary:
- Document type and variant used
- Fields demonstrated
- Which SenseML methods appear in the post
- Any config fields you flagged as unclear or that may need screenshot attention
