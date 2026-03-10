# Sensible SenseML Reference Docs — Style Guide Overview

This file covers page structure, voice, formatting conventions, and cross-reference syntax for SenseML reference pages. It is consumed by LLM agents writing or updating reference docs.

---

## Page structure

Every SenseML reference page follows this section order. Sections marked *(optional)* appear on some pages but not all.

1. **YAML frontmatter** (required)
2. **Opening paragraph** (required) — 1–3 sentences
3. **Use-case or tip block** *(optional)* — bullet list of when/why to use this feature, or "Prompt Tips" for LLM methods
4. **Jump links** *(optional)* — inline links to `#parameters`, `#examples`, `#notes`
5. **`# Parameters`** (required) — parameter table(s)
6. **`# Examples`** (required) — one or more named examples
7. **`# Notes`** *(optional)* — how-it-works explanations, implementation details

Use H1 (`#`) for all top-level sections (Parameters, Examples, Notes). Use H2 (`##`) for named subsections within Examples (e.g., `## Example: Extract from images`) and for conceptual groupings within a long Parameters section.

### When to add jump links

Add the jump link block when the page has a Notes section or more than two named examples. Omit it for short pages. Format:

```
[**Parameters**](doc:page-slug#parameters)\
[**Examples**](doc:page-slug#examples)\
[**Notes**](doc:page-slug#notes)
```

Note the backslash line break (not a blank line) between each link — this renders them as stacked inline links, not a list.

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

**Opening paragraph:** Use imperative third-person present tense. Start with a verb. Examples:
- "Extracts lines or parts of lines proximate to the anchor point."
- "Extracts data in a rectangular region, defined in inches."
- "Define your own computed field method using JsonLogic."
- "Ignores pages outside the start page and end page."

Do not start with "The X method..." or "This method...". Lead with what it does.

**Parameter descriptions:** Mix of second person ("You can use this parameter to...") and third person ("Sensible returns...", "Sensible ignores..."). Use "Sensible" as the subject when describing engine behavior. Use "you" when giving guidance about how to configure something.

**Examples:** Introduce each example in third person: "The following example shows [doing X]." or "The following example shows using the X parameter to [do Y]."

**Tone:** Terse and precise. No filler. No "please note that" or "it's important to remember". State facts directly.

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

This applies even though the JSON key is camelCase (`sortLines`, `textAlignment`).

### Method and feature names in prose
Capitalize method names and major feature names: "the Label method", "the Box method", "the Region method", "the Query Group method", "Sections", "the Multicolumn preprocessor".

---

## Image format

```markdown
![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/filename.png)
```

Always use `![Click to enlarge]` as the alt text. Images live in `assets/images/final/`. Use the GitHub raw URL on the `v0` branch.

---

## Example document download table

Every example that references a PDF uses this exact table:

```markdown
| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/filename.pdf) |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------- |
```

Place this table immediately after the example document image (or after the `**Example document**` heading if there is no image).

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

Example section structure (use bold subheadings, not headings):

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

Note: `**Example document**\` uses a backslash line break so the image follows on the next line without a blank line gap.

Preprocessor examples sometimes omit the Example document section when the visual isn't necessary to understand the config.
