---
name: sensible-style-guide-generator
description: Generates or refreshes the Sensible SenseML docs style guide by fetching and analyzing existing reference pages via the sensible-docs MCP server. Use this skill whenever asked to generate, update, or refresh the style guide, or when the style guide files at .claude/style-guide/ are missing or stale. Also invoke before writing a batch of new SenseML reference pages from scratch.
---

You are generating or refreshing the local style guide for Sensible SenseML reference documentation. The output files are consumed by LLM agents — particularly the `update-docs-from-pr` skill — when writing new reference pages. Pre-seeded versions already exist at `.claude/style-guide/`; your job is to re-analyze the live docs and update them if conventions have drifted.

## Output location

Write (or overwrite) these three files:

- `/home/franceselliott/GitHub/sensible-docs/.claude/style-guide/style-guide-overview.md`
- `/home/franceselliott/GitHub/sensible-docs/.claude/style-guide/reference-topic-template.md`
- `/home/franceselliott/GitHub/sensible-docs/.claude/style-guide/sentence-word-guidance.md`

---

## Step 1: Fetch representative pages

Use the `mcp__sensible-docs__fetch` tool to fetch the following pages. Fetch all in parallel.

**Layout-based methods:** label, region, box, row, fixed-table
**LLM-based methods:** query-group, list, nlp-table
**Computed field methods:** custom-computation, mapper, concatenate
**Field query object:** method, anchor
**Preprocessors:** page-range, merge-lines, nlp
**Complex features:** sections, conditional

---

## Step 2: Analyze for patterns

Before rewriting the output files, look for these things across the fetched pages:

**Page structure**
- What sections appear, in what order? Which are present on every page vs optional?
- Are `# Parameters` and `# Examples` always H1? Are there H2 variants and, if so, when?
- Which pages have jump links (the `[**Parameters**](doc:...)` block) after the opening paragraph? Is there a rule — e.g., only pages with a Notes section, or only pages above a certain length?
- Does the parameter table always use `key`, `value`, `description` as column headers? Note any exceptions.

**Voice and tone**
- What grammatical form are opening sentences? (Imperative "Extracts...", third-person "The X method extracts...", or both?)
- When does "you" appear vs "Sensible" as the subject? Is there a pattern by section?
- Are there passive-voice sentences? Where?

**Conventions**
- How are parameter names capitalized in prose (Title Case, lowercase, backticked)?
- When are JSON values/strings backtick-quoted vs plain in prose?
- What is the exact wording of the note that precedes parameter tables ("**Note:** For additional parameters...")?
- What is the exact format of the example document download table?

**Terminology**
- What specific nouns are used consistently for: the JSON config, the extracted result, the text Sensible searches for, a document excerpt sent to an LLM?
- Are any terms used inconsistently across pages? Flag them.

---

## Step 3: Rewrite the output files

Use the pre-seeded content as a baseline. Update or correct anything that has changed, and add patterns you observed that weren't captured. Remove anything that turns out not to be a real convention.

Write for an LLM agent reader: direct, rule-based, with real examples quoted from the docs. A rule like "use `boolean. default: \`false\``" is more useful than "defaults are noted in the value column."
