---
name: sensible-style-guide-generator
description: Generates or refreshes the Sensible SenseML docs style guide by reading existing reference pages from the published docs and analyzing their conventions. Use this skill whenever asked to generate, update, or refresh the style guide, or when the style guide files at .claude/style-guide/ are missing or stale. Also invoke before writing a batch of new SenseML reference pages from scratch.
---

You are generating or refreshing the local style guide for Sensible SenseML reference documentation. The output files are consumed by LLM agents — particularly the `update-docs-from-pr` skill — when writing new reference pages. Pre-seeded versions already exist at `.claude/style-guide/`; your job is to re-analyze the published docs and update them if conventions have drifted.

## Output location

Write (or overwrite) these three files:

- `/home/franceselliott/GitHub/sensible-docs/.claude/style-guide/style-guide-overview.md`
- `/home/franceselliott/GitHub/sensible-docs/.claude/style-guide/reference-topic-template.md`
- `/home/franceselliott/GitHub/sensible-docs/.claude/style-guide/sentence-word-guidance.md`

---

## Step 1: Find page URLs

Fetch `https://docs.sensible.so/llms.txt`. It lists every doc page as a direct markdown URL in the format `https://docs.sensible.so/docs/[slug].md`.

Find the URLs for these pages:

**Layout-based methods:** label, region, box, row, fixed-table
**LLM-based methods:** query-group, list, nlp-table
**Computed field methods:** custom-computation, mapper, concatenate
**Field query object:** method, anchor
**Preprocessors:** page-range, merge-lines, nlp
**Complex features:** sections, conditional

---

## Step 2: Fetch all pages in parallel

Fetch all the `.md` URLs from Step 1 in parallel using WebFetch. Each returns raw markdown — the published source for that reference page.

---

## Step 3: Analyze for patterns

Before rewriting the output files, look for these things across the pages:

**Page structure**
- What sections appear, in what order? Which are present on every page vs optional?
- Are `# Parameters` and `# Examples` always H1? Are there H2 variants and, if so, when?
- Which pages have jump links (the `[**Parameters**](doc:...)` block) after the opening paragraph?
- Does the parameter table always use `key`, `value`, `description` as column headers? Note any exceptions.

**Voice and tone**
- What grammatical form are opening sentences?
- When does "you" appear vs "Sensible" as the subject?
- Any passive voice? Where?

**Conventions**
- How are parameter names capitalized in prose?
- When are JSON values/strings backtick-quoted vs plain?
- What is the exact wording of the note that precedes parameter tables?
- What is the exact format of the example document download table?

**Terminology**
- What specific nouns are used consistently for key concepts?
- Are any terms used inconsistently? Flag them.

---

## Step 4: Rewrite the output files

Use the pre-seeded content as a baseline. Update or correct anything that has changed, and add patterns you observed that weren't captured. Remove anything that turns out not to be a real convention.

Write for an LLM agent reader: direct, rule-based, with real examples quoted from the docs. A rule like "use `boolean. default: \`false\``" is more useful than "defaults are noted in the value column."
