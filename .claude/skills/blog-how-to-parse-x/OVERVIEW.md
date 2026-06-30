# blog-how-to-parse-x: Skill Overview

Generates a "how to extract data from [document type]" blog post for Sensible. Takes a document type as input, finds or accepts a SenseML config, runs a live extraction, writes the draft, enriches it with inline comments, and publishes to Notion.

---

## Steps at a glance

| Step | What happens | Type |
|---|---|---|
| 1 | Read style guide and JSON5 comment reference | Deterministic |
| 2 | Look up document type in the config library | Deterministic |
| 3 | Fetch config → produce field inventory → propose fields with line counts | **Judgment** |
| 3 (pause) | Present field selection + intro framing variant to user for approval | Human gate |
| 4 | Upload config + PDF via `upload_and_extract.py`, save real output | Deterministic |
| 5 | Write full draft using real field names and real output values | **Judgment** |
| 6 | Run `json5-commenter` skill to enrich all code blocks | Deterministic |
| 6.5 | Extract combined config from draft via `extract_config_from_draft.py`, re-upload, write `drafts/blog-[slug]-meta.json` with PDF path, config path, and app URLs | Deterministic |
| 6.6 | Cross-check individual output blocks against combined extraction | Deterministic |
| 6.7 | Vale, writing rules, naming conventions, code comment style, glossary, line count check | Mostly deterministic |
| 7 | Print summary to user | Deterministic |
| 8 | Strip HTML comments, publish to Notion via `publish_to_notion.py` or MCP fallback | Deterministic |

---

## Judgment-dependent steps

These steps require Claude to make decisions and pause for user input:

**Step 3 — Field selection**
- Produce a full field inventory (all top-level fields + sections sub-fields)
- Propose 2–4 fields to demonstrate, with explicit reasoning
- Show line count per field; flag anything over 75 lines
- Constraints: no nested sections (sections-within-sections); prefer flat or single-level Sections; no redundant methods
- **Wait for user approval before continuing**

**Step 3 — Intro framing variant**
- Determine whether the config is deterministic-primary (A), LLM-primary (B), or hybrid (C)
- State the implied P3 framing and get user confirmation
- **Wait for user approval before continuing**

**Step 5 — Draft writing**
- Write intro (3-paragraph structure: P1 description+problem / P2 boilerplate / P3 lead-in+framing)
- Write one section per demonstrated field
- Keep individual code blocks under 75 lines
- Use real output values from Step 4 — never invented

---

## Key constraints

- **75-line limit** on individual field code blocks (not counting "Putting it all together")
- **No repeated comments** within a single code block — comment on first use only
- **No nested sections** as demonstrated fields — structural wrapper overhead makes them too long
- **No invented output** — all output blocks must come from a real extraction (Step 4)
- **Draft is source of truth** for the combined config — enrich draft first, then sync via Step 6.5

---

## Scripts

| Script | Purpose |
|---|---|
| `upload_and_extract.py` | Uploads config to Sensible, runs extraction against PDF, returns parsed output + app URL |
| `extract_config_from_draft.py` | Extracts the "Putting it all together" code block from the draft and writes it to a file |
| `publish_to_notion.py` | Publishes draft to Notion Content Tracker; preferred over MCP fallback |
| `test_blog_output.py` | Extracts combined config from draft, runs it against golden PDF, diffs output against draft |

---

## Companion files

| File | Purpose |
|---|---|
| `SKILL.md` | Operative instructions for Claude — the step-by-step execution protocol |
| `checklist.md` | Open and completed skill improvement items |
| `intro-rewrite-feedback.md` | Verbatim accepted intro example with structure breakdown (use to update template) |
| `friction-log.md` | Past failure modes and edge cases encountered during skill runs |
