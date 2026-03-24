# Sensible SenseML Reference Docs — Style Guide Overview

This file covers page structure, voice, formatting conventions, and cross-reference syntax for SenseML reference pages. It is consumed by LLM agents writing or updating reference docs.

---

## Page structure

Every SenseML reference page follows this section order. Sections marked *(optional)* appear on some pages but not all.

1. **YAML frontmatter** (required)
2. **Opening paragraph** (required) — 1–3 sentences
3. **Use-case or tip block** *(optional)* — bullet list of when/why to use this feature, or "Prompt Tips" for LLM methods; or a Limitations subsection
4. **Jump links** *(optional)* — inline links to `#parameters`, `#examples`, `#notes`
5. **Parameters section** (required)
6. **Examples section** (required)
7. **Notes section** *(optional)*

### Parameters heading level

- Use `# Parameters` (H1) for standalone methods: layout-based methods, LLM-based methods, preprocessors, computed field methods.
- Use `## Parameters` (H2) for object pages (anchor, match) and for subsections within a multi-table parameters section (e.g., a "Query group parameters" table nested under a top-level `# Parameters`).
- Use `## Examples` and `# Notes` (H1) for their respective sections.

### When to add jump links

Add the jump link block when the page has a Notes section, or when it has more than two named examples. Omit it for short, simple pages. Format:

```
[**Parameters**](doc:page-slug#parameters)\
[**Examples**](doc:page-slug#examples)\
[**Notes**](doc:page-slug#notes)
```

Note the backslash line break (not a blank line) between each link — this renders them as stacked inline links, not a list. Only include links to sections that actually exist on the page.

---

## Frontmatter

Always use this exact structure. Only `title` and `metadata.description` vary per page.

```yaml
---
title: Method Name
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Short phrase describing what the method does'
  robots: index
next:
  description: ''
---
```

`metadata.description` is a short phrase (4–7 words), lowercase except for proper nouns. Examples: `'Extract labeled values'`, `'Extract repeating document sections'`, `'Limit extraction to page ranges'`.

---

## Voice and tone

**Opening paragraph:** Use imperative present tense. Start with a verb. Examples:
- "Extracts lines or parts of lines proximate to the anchor point."
- "Extracts data in a rectangular region, defined in inches."
- "Merges lines distributed along a horizontal axis more aggressively than the built-in line merger."
- "Maps output from source fields using a case-sensitive lookup table."
- "Define your own computed field method using JsonLogic."
- "Ignores pages outside the start page and end page."

Acceptable variations when the imperative form is awkward:
- "This LLM-based method extracts repeating data..." (list method)
- "Use the Conditional method to handle document variations..." (conditional method)

Do not start with "The X method..." as a default. Lead with what it does.

**Parameter descriptions:** Mix of second person ("You can use this parameter to...") and third person ("Sensible returns...", "Sensible ignores..."). Use "Sensible" as the subject when describing engine behavior. Use "you" when giving configuration guidance.

**Examples:** Introduce each example in third person: "The following example shows [doing X]." or "The following example shows using the X parameter to [do Y]."

**Tone:** Terse and precise. No filler. No "please note that" or "it's important to remember". State facts directly.

**Em dashes:** Do not use em dashes to join compound clauses. Split them into two sentences instead.
- Avoid: "a fixed layout — the same fields appear in the same positions across issuers."
- Prefer: "a fixed layout. The same fields appear in the same positions across issuers."

---

## Parameter table formats

### Standard table (most pages)

Three columns: `key`, `value`, `description`. Left-align all columns.

```markdown
| key | value | description |
| :-- | :---- | :---------- |
```

Note: The `region` page uses `id` as the first column header instead of `key`. This is an inconsistency in the existing docs — use `key` for all new pages.

The `anchor` page uses `values` (plural) as the second column header. Use `value` (singular) for all new pages.

### Four-column table with interactions (complex LLM methods)

For methods with many parameter interactions (e.g., query-group), add an `interactions` column:

```markdown
| key | value | description | interactions |
| :-- | :---- | :---------- | :----------- |
```

Use this sparingly — only when multiple parameters have documented incompatibilities that would clutter individual description cells.

### Section separator rows in parameter tables

For long parameter tables, use bold separator rows to group related parameters visually:

```markdown
| | | ***CHAIN PROMPTS*** | |
```

This is an empty row with bold italic text in the description cell, used to label a cluster of related parameters. Use it only for very long tables (8+ rows) where grouping genuinely aids comprehension.

### Referencing global parameters in a row

Rather than duplicating global parameter descriptions, reference them inline:

```markdown
| tiebreaker | | For information about this global parameter, see [Method](doc:method#parameters). |
```

Use this pattern when a method's parameter table includes a global param for completeness but the full description lives on the method object page.

---

## Formatting conventions

### Backtick quoting
- JSON keys: always backtick in prose — `"position"`, `"id"`, `"stop"`
- Enum values: always backtick — `"below"`, `"readingOrderLeftToRight"`, `true`, `false`
- Method IDs: always backtick — `"label"`, `"queryGroup"`, `"customComputation"`
- Parameter names: do NOT backtick in prose — write "the Stop parameter", not "the `stop` parameter"

### Parameter name capitalization in prose
Capitalize parameter names as Title Case when referring to them by name in running text:
- "the Sort Lines parameter"
- "the Text Alignment parameter"
- "the Stop parameter"
- "the Multimodal Engine parameter"
- "the Directly Adjacent Threshold parameter"

This applies even though the JSON key is camelCase (`sortLines`, `textAlignment`).

### Method and feature names in prose
Capitalize method names and major feature names: "the Label method", "the Box method", "the Region method", "the Query Group method", "Sections", "the Multicolumn preprocessor", "the Merge Lines preprocessor".

**Never use camelCase with backticks for method or preprocessor names in running prose.** Convert to spaced Title Case instead:

| Wrong | Right |
| ----- | ----- |
| the `` `customCompute` `` method | the Custom Compute method |
| the `` `removeHeaders` `` preprocessor | the Remove Headers preprocessor |
| the `` `queryGroup` `` method | the Query Group method |
| the `` `mergeLines` `` preprocessor | the Merge Lines preprocessor |

This applies to parameter names too — see the Parameter name capitalization section above.

### Inline links for method and preprocessor names

Where possible, link method and preprocessor names inline on first mention. Use `doc:` slugs (not `.md` file paths). To find the correct slug for a page, consult [https://docs.sensible.so/llms.txt](https://docs.sensible.so/llms.txt) and use the slug portion of the URL (the part after `docs.sensible.so/`), **without** the `.md` extension.

Examples:
- `[Custom Compute method](doc:custom-compute)`
- `[Remove Headers preprocessor](doc:remove-headers)`
- `[Query Group method](doc:query-group)`

Link on first meaningful mention per page. Do not re-link on every subsequent mention.

---

## Image format

The standard authoring format for images is:

```markdown
![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/filename.png)
```

Always use `![Click to enlarge]` as the alt text. Images live in `assets/images/final/`. Use the GitHub raw URL on the `v0` branch.

Note: some existing pages use `<Image alt="Click to enlarge" border={false} src="..." />` (JSX syntax). This is a publishing artifact — use the standard markdown `![]()` syntax when authoring.

---

## Example document download table

Every example that references a PDF uses this exact table:

```markdown
| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/filename.pdf) |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------- |
```

Place this table immediately after the example document image (or after the `**Example document**` heading if there is no image).

---

## Example section structure

### Standard example

Use bold subheadings (not headings). The backslash after `**Example document**\` creates a line break so the image follows immediately.

```markdown
**Config**

```json
{ ... }
```

**Example document**\
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/...)

| Example document | [Download link](https://raw.githubusercontent.com/...) |
| ---------------- | ------------------------------------------------------ |

**Output**

```json
{ ... }
```
```

### Troubleshooting example (PROBLEM/SOLUTION pattern)

For examples that demonstrate a fix to a specific issue, use this variant:

```markdown
**PROBLEM**

[Description of the problem]

**Config**  (or just Config without bold, matching surrounding style)

[config]

**SOLUTION**

[Description of the solution or the fix applied]

**Config**

[corrected config]

**Output**

[output]
```

This pattern appears in merge-lines and box pages. Use it when the example's purpose is to show before/after contrast for a troubleshooting scenario.

### Multiple examples

Use H2 subheadings: `## Example: Descriptive name` or `## Example 1` / `## Example 2` when names aren't meaningful.

Preprocessor examples often omit the Example document section when the visual isn't necessary to understand the config.

---

## Cross-references

Use `doc:` slugs for links to other docs pages:
- `[Match object](doc:match)`
- `[Global parameters for methods](doc:method#global-parameters-for-methods)`
- `[JsonLogic](doc:jsonlogic)`

Use `ref:` slugs for API reference links. Use full `https://` URLs only for external sites (MDN, GitHub, etc.).

---

## Code blocks in examples

Always use fenced ` ```json ` blocks. Inline comments in JSON configs (using `//` or `/* */`) are acceptable and encouraged for complex configs — they help readers understand non-obvious choices. The Sensible engine accepts relaxed JSON.
