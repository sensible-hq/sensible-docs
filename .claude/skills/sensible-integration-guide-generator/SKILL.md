---
name: sensible-integration-guide-generator
description: Generates or refreshes the Sensible integration guide template by reading existing integration guide pages from the published docs and analyzing their conventions. Use this skill whenever asked to generate, update, or refresh the integration guide template, or when .claude/style-guide/integration-guide-template.md is missing or stale. Also invoke before writing a new integration guide from scratch.
---

You are generating or refreshing the local integration guide template for Sensible docs. The output file is consumed by LLM agents writing new integration guides. A pre-seeded version already exists at `.claude/style-guide/integration-guide-template.md`; your job is to re-analyze the live docs and update it if conventions have drifted.

## Output location

Write (or overwrite) this file:

- `/home/franceselliott/GitHub/sensible-docs/.claude/style-guide/integration-guide-template.md`

---

## Step 0: Ask for the example document type

Before doing anything else, ask the user which document type they want to use as the example throughout the integration guide. Read `.claude/style-guide/config-library-supported-document-types.md` and display the full list grouped by category. Wait for their answer before proceeding.

Use the chosen doc type consistently wherever a specific document type appears as an example — for instance, in step instructions, **Document type** field values, and the opening sentence of any guide drafted from this template.

---

## Step 0.5: Fetch sample field names for the chosen doc type

Look up the category for the chosen doc type in `.claude/style-guide/config-library-supported-document-types.md`. Then browse the configurations directory on GitHub:

`https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/[Category]/[Doc Type]/configurations`

Pick one configuration file (any is fine) and fetch its raw content from:

`https://raw.githubusercontent.com/sensible-hq/sensible-configuration-library/main/templates/[Category]/[Doc Type]/configurations/[filename].json`

Extract the field names (the `"id"` values inside the `"fields"` arrays). Keep a working list of 3–6 representative field names to use as concrete examples throughout the guide — for instance, as output field names shown in a Zapier action step or an API response snippet.

---

## Step 1: Find page URLs

Fetch `https://docs.sensible.so/llms.txt`. It lists every doc page as a direct markdown URL in the format `https://docs.sensible.so/docs/[slug].md`.

Find the URLs for these integration guide pages:
- `zapier-getting-started` (basic Zapier tutorial)
- `zapier-tutorial-2` (advanced Zapier tutorial)
- `quickstart` (API quickstart)
- Any other pages under the integrations section

---

## Step 2: Fetch all pages in parallel

Fetch all the `.md` URLs from Step 1 in parallel using WebFetch. Each returns raw markdown — the published source for that page.

---

## Step 3: Analyze for patterns

Before rewriting the output file, look for these things across the pages:

**Page structure**
- What sections appear, in what order? Which are present on every page vs optional?
- How are prerequisites labeled — `## Prerequisite: X` or `## Before you begin` or something else?
- Are main steps organized by platform/system (H2 per platform) or as a single flat numbered list?
- What heading level is Notes — H1 or H2?

**Step formatting**
- How are numbered steps structured? Flat list, or nested with sub-steps?
- Are UI element names bolded (`**App**`, `**Trigger event**`)? Always?
- How are the Setup/Configure/Test sub-sections labeled — bold inline headers or H4?

**Voice and tone**
- What grammatical form are opening sentences? ("This topic describes...", imperative, or other?)
- Are sections introduced with "Take the following steps to..." or just the heading + numbered list?

**Images**
- Where do images appear relative to steps — before, after, or inline?
- Do captions follow images, or is the image standalone?

**Notes section**
- Is it `# Notes` (H1) or `## Notes` (H2)?
- Are sub-topics within Notes bold inline headers or H3?

---

## Step 4: Rewrite the output file

Use the pre-seeded content as a baseline. Update or correct anything that has changed, and add patterns you observed that weren't captured. Remove anything that turns out not to be a real convention.

Write for an LLM agent reader: direct, rule-based, with real examples quoted from the docs. Structural rules ("Prerequisites use `## Prerequisite: [action]` headings") are more useful than vague descriptions ("there are prerequisites before the main steps").
