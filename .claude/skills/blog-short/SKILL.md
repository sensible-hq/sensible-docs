---
name: blog-short
description: Generates a short conceptual blog post ("Automating Data Extraction from X") for Sensible. Covers a document type and the primary Sensible feature that addresses its extraction challenge. No code blocks or screenshots — 400–600 words. Invoke whenever the user wants to write a short/editorial/overview-style blog post about a document type.
argument-hint: <document type> [--feature <sensible feature>] [--context "<notes>"]
allowed-tools: Bash, Read, Write, WebSearch, WebFetch, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-create-pages, mcp__claude_ai_Notion__notion-update-page, mcp__vale__check_file
---

Generate a short conceptual blog post about automating data extraction from [document type].

## Parse arguments

**$ARGUMENTS** format:

```
<document type>
<document type> --feature <sensible feature>
<document type> --feature <sensible feature> --context "<additional notes>"
```

- `<document type>` — everything before `--feature` or `--context`
- `--feature` — optional; the primary Sensible feature to highlight (e.g., "Sections", "NLP Table", "Query Group"). If omitted, infer it in Step 2.
- `--context` — optional; additional notes about the document type, industry, or angle

## Step 1 — Read template and style guidance

Read these files in parallel before writing anything:

- `.claude/skills/blog-short/blog-short-template.md` — structure, section patterns, and verbatim boilerplate
- `.claude/style-guide/writing-rules.md` — em dashes, passive voice, extraction phrasing, gerunds, tone
- `.claude/style-guide/glossary.md` — canonical terms (config not template, sections not repeating groups, etc.)

## Step 2 — Research the document type

Use WebSearch and/or WebFetch to understand:

1. **What the document is** — who produces it, what it summarizes, what data it contains
2. **Who uses the data and why** — which downstream workflows or decisions depend on it
3. **Structural challenges** — what makes it hard to extract from programmatically (table complexity, repeating structures, layout variability across issuers, nested data, variable row/column counts)
4. **Which Sensible feature fits** — if `--feature` was not provided, determine which Sensible feature most directly addresses the structural challenge:
   - **Sections** — repeating structures (claims, line items, transactions) with variable counts
   - **NLP Table** — tables with inconsistent column ordering or merged cells
   - **Query Group** — free-form or variable-layout documents needing LLM reasoning
   - **Region / Row** — fixed-position fields in consistent carrier/vendor layouts
   - **Fingerprint** — multi-carrier or multi-format documents needing classification before extraction

Also check whether the prebuilt config library has an entry for this document type — it often reveals which methods the real config uses and what fields are extracted:

```
https://raw.githubusercontent.com/sensible-hq/sensible-configuration-library/main/README.md
```

**Do not write yet.** Synthesize findings into a concise internal summary: document description, key challenges, chosen feature, potential advantage angle.

## Step 3 — Propose framing (human gate)

Present the following for user approval before writing:

1. **Title** — `Automating Data Extraction from [Doc Types]`
2. **Challenges** — proposed 3–4 bullet points with bold lead phrases; each names a concrete structural property of the document
3. **Feature angle** — the primary Sensible feature and one sentence on how it maps to the challenge
4. **Advantage section** — present or absent; if present, one sentence on what the differentiating capability is
5. **Conclusion CTA** — what next step you'll point readers toward (demo, sign-up, docs)

Ask:
> "Here's the framing I'm planning. Does this match what you had in mind? Any adjustments before I write?"

Do not move to Step 4 until the user confirms or adjusts.

## Step 4 — Write the draft

Write the full post following `.claude/skills/blog-short/blog-short-template.md` exactly. Use:

- Real document-type details from Step 2 research — do not invent challenges or feature behaviors
- Verbatim boilerplate sentence patterns from the template, with `[variables]` filled in
- Third person or second person — pick one and stay consistent throughout

**No code blocks. No screenshot placeholders. No SenseML.**

Target: 400–600 words. Every sentence earns its place.

Save the draft to:
```
drafts/blog-[doc-type-slug].md
```

## Step 5 — Style and terminology check

Run all checks in order. Fix issues before Step 6.

**5a — Vale:**

Use `mcp__vale__check_file` on `drafts/blog-[doc-type-slug].md`. Fix all **errors** and **warnings**. Suggestions are optional — apply if clearly right, skip if they conflict with established blog conventions.

**5b — Writing rules:**

Read `.claude/style-guide/writing-rules.md`. Check the draft for:
- Em dashes: split into two sentences
- Passive voice: use "Sensible" or "you" as explicit subject
- Extraction phrasing: "using" not "against"
- Gerunds over nominalizations: "automating extracting" not "automates the extraction of"
- Tone: no filler phrases ("please note that", "it's important to remember")

**5c — Glossary:**

Read `.claude/style-guide/glossary.md`. Fix any term in the prose that appears in the "Avoid" column. Key ones to watch:
- "config" not "template" or "schema"
- "sections" not "repeating groups" or "loops"
- "the Sensible app" not "the UI" or "the dashboard"
- "output" not "result object" or "response"

Only proceed to Step 6 once all checks are clean.

## Step 6 — Present to user

Print the path to the saved draft and a short summary:
- Document type
- Feature highlighted
- Word count
- Whether an advantage section was included

## Step 7 — Publish draft to Notion

Push the draft to the Sensible Content Tracker.

**Preferred path:** If `NOTION_API_KEY` is available, use `publish_to_notion.py` from the `blog-how-to-parse-x` skill — it handles markdown-to-Notion conversion correctly:

```bash
python3 .claude/skills/blog-how-to-parse-x/publish_to_notion.py \
  --draft drafts/blog-[doc-type-slug].md \
  --parent-id [main-page-id]
```

**Fallback path (no API key):** Use the MCP protocol below.

---

### MCP fallback protocol

**7a — Search for an existing Content Tracker entry:**

Use `notion-search` with the blog post title, scoped to the Content Tracker data source:
- `query`: the blog post title
- `data_source_url`: `collection://31bc7dd4-9788-8031-9dd4-000b769e5374`

**7b — If no main page exists (first publish):**

Create the main Content Tracker entry with `notion-create-pages`:
- `parent`: `{ "type": "data_source_id", "data_source_id": "31bc7dd4-9788-8031-9dd4-000b769e5374" }`
- `properties`:
  - `Content`: blog post title
  - `Category`: `Document Type Blog Posts`
  - `Status`: `In progress`
- `content`: `Draft versions are in child pages below.`

Save the returned page ID as `[main-page-id]`.

**7c — Read the draft immediately before publishing:**

Use the Read tool on `drafts/blog-[doc-type-slug].md` immediately before calling the Notion tool. Do NOT use draft content from memory or from earlier in context.

**7d — Create the child page:**

Use `notion-create-pages`:
- `parent`: `{ "type": "page_id", "page_id": "[main-page-id]" }`
- `title`: `Draft v[N] — [YYYY-MM-DD]` (determine N by fetching children of `[main-page-id]` and finding the highest existing version)
- `content`: the exact text returned by Read in step 7c — do not paraphrase, summarize, or reconstruct any part of it

After publishing, print the new child page URL.
