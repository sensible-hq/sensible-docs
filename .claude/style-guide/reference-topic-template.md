# Reference Topic Template

Use this template when creating a new SenseML reference page. Replace all `[PLACEHOLDER]` text. Comments in `<!-- -->` are guidance — remove them from the final file.

See `style-guide-overview.md` for formatting conventions and `sentence-word-guidance.md` for how to write parameter descriptions.

---

## Template

```markdown
---
title: [Method Name]
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: '[short phrase, 4–7 words, lowercase except proper nouns]'
  robots: index
next:
  description: ''
---
<!-- Opening sentence: imperative verb, 1–3 sentences. What does this method do?
     Lead with the verb. Examples: "Extracts...", "Merges...", "Maps...", "Ignores...", "Define..."
     Acceptable: "This LLM-based method extracts..." or "Use the Conditional method to..."
     Do NOT default to "The X method..." -->
[OPENING SENTENCE.]

<!-- Use-case block (OPTIONAL): bullet list of when to use this vs. alternatives. -->
<!-- Example:
In general, use this method:
- for faster performance compared to the Box method
- when the target region's formatting doesn't fit other SenseML methods
-->

<!-- Limitations block (OPTIONAL): for LLM-based methods with output limits or constraints. -->
<!-- Example:
#### Limitations
- Sensible can output lists of different maximum lengths depending on how you configure...
-->

<!-- Jump links (OPTIONAL): add when the page has a Notes section or many examples. -->
<!-- Example:
[**Parameters**](doc:[page-slug]#parameters)\
[**Examples**](doc:[page-slug]#examples)\
[**Notes**](doc:[page-slug]#notes)
-->

# Parameters

<!-- Standard note for layout-based methods: -->
**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

<!-- For computed field methods, use instead: -->
<!-- The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: -->

<!-- For the NLP preprocessor, use instead: -->
<!-- The following parameters are available both on the config level and for each individual field through the method's parameters. Setting a parameter at the method level overrides it at the config level. -->

<!-- For other preprocessors and object pages (anchor, match): omit the note. -->

| key | value | description |
| :-- | :---- | :---------- |
| id (**required**) | `[methodId]` | [One-sentence description, or leave blank if the opening paragraph covers it.] |
| [param1] (**required**) | [value type or enum] | [Description. See sentence-word-guidance.md.] |
| [param2] | [type]. default: `[default]` | [Description.] |

<!--
Column guidelines:
- "key": param name in camelCase. Mark required with (**required**). Mark deprecated with **(Deprecated)**.
- "value": type ("boolean", "string", "number", "object", "array of objects", "string array")
  or enum values separated by commas. Append ". default: `value`" for optional params with defaults.
- "description": what it does. For enum values with distinct behaviors, describe each option
  using <br/> line breaks within the cell. For params with documented incompatibilities with
  other params, add an interactions note at the end of the description.

For preprocessors, the identifying param key is "type" (not "id"):
| type (**required**) | `mergeLines` | [description] |

To reference a global param without duplicating its full description:
| tiebreaker | | For information about this global parameter, see [Method](doc:method#parameters). |
-->

# Examples

<!-- Simple method (single example): -->
The following example shows [what this example demonstrates].

**Config**

```json
{
  "fields": [
    {
      "id": "[field_id]",
      "anchor": "[anchor text]",
      "method": {
        "id": "[methodId]",
        "[param1]": "[value1]"
      }
    }
  ]
}
```

**Example document**\
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/[filename].png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/[filename].pdf) |
| ---------------- | -------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "[field_id]": {
    "type": "string",
    "value": "[example output value]"
  }
}
```

<!-- Multiple examples: use H2 subheadings.
     Format: "## Example: [Descriptive name]" or "## Example 1" / "## Example 2".
     Each follows the same Config / Example document / Output structure. -->

<!-- Troubleshooting example (PROBLEM/SOLUTION pattern):
Use when the example demonstrates a before/after fix.

**PROBLEM**

[What goes wrong without the parameter/setting]

[config showing the problem]

**SOLUTION**

[What to configure to fix it]

[corrected config and output]
-->

<!-- # Notes (OPTIONAL)
Add when the method has non-obvious behavior that doesn't fit in parameter descriptions —
e.g., how the algorithm works, performance characteristics, edge cases, related methods.
Use H2 subheadings within Notes for multiple topics. -->
```

---

## Method category variations

### Layout-based method
- Opening: imperative verb — "Extracts...", "Matches...", "Returns..."
- Uses the global parameters note
- Identifying param key is `id` (not `type`)
- Example always includes config + output; example document section included when a visual helps
- Notes section is common for performance guidance and related-methods references

### LLM-based method
- Opening: imperative or "This LLM-based method extracts..." both acceptable
- Often includes a Limitations subsection before Parameters
- May include "Prompt Tips" guidance before Parameters
- Parameter table may have two sub-tables (field-level params + method object params)
- Complex methods (query-group) use the 4-column `interactions` table and section separator rows
- Notes section common for how-it-works explanation

### Computed field method
- Opening: "Define...", "Maps...", "Concatenates...", "Returns..."
- Uses the computed field global method note (not layout-based note)
- Identifying param key is `id`
- Config examples use `"computed_fields": [...]` array, not `"fields": [...]`
- Commonly accesses `parsed_document` in examples

### Preprocessor
- Opening: imperative — "Merges...", "Ignores...", "Configures..."
- No global parameters note
- Identifying param key is `type` (not `id`), e.g., `"type": "mergeLines"`
- Config examples use `"preprocessors": [...]` array
- Examples often use PROBLEM/SOLUTION pattern for troubleshooting scenarios
- Parameters section uses `# Parameters` (H1)

### Object page (anchor, match)
- Opening: defines what the object is — "An anchor is a string, Match object, or array of Match objects."
- Uses `## Parameters` (H2), not H1
- May use `values` (plural) in the value column header — but prefer `value` (singular) for new pages
- Includes code examples inline (simple syntax shown before the parameters table)
- Notes section for advanced usage links

### Sections
- Opening: describes what "sections" are as a concept
- Config examples use `"type": "sections"` on a field with a nested `"fields"` array
- Often includes diagrams showing horizontal vs. vertical section directions
- Examples are extensive — links to separate example pages rather than inline examples
