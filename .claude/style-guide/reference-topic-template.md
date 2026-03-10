# Reference Topic Template

Use this template when creating a new SenseML reference page. Replace all `[PLACEHOLDER]` text. Comments in `<!-- -->` are guidance for you — remove them from the final file.

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
     Do NOT start with "The X method" or "This method". Lead with the verb.
     Examples: "Extracts...", "Ignores...", "Defines...", "Returns..." -->
[OPENING SENTENCE. What the method extracts or does, in 1–3 sentences.]

<!-- Use-case block (OPTIONAL): Add bullet points if there are meaningful "when to use this vs. X"
     decisions a user needs to make. Skip for simple methods. -->
<!-- Example:
In general, use this method:
- for faster performance compared to the Box method
- when the target region's formatting doesn't fit other SenseML methods
-->

<!-- Jump links (OPTIONAL): Add when the page has a Notes section or many examples. -->
<!-- Example:
[**Parameters**](doc:[page-slug]#parameters)\
[**Examples**](doc:[page-slug]#examples)\
[**Notes**](doc:[page-slug]#notes)
-->

# Parameters

<!-- Standard note for methods. Use the layout-based or LLM variant as appropriate. -->
<!-- For layout-based and computed field methods: -->
**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

<!-- For preprocessors: -->
<!-- (no standard note — just go straight to the table) -->

<!-- For computed field methods, use instead: -->
<!-- The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: -->

| key | value | description |
| :-- | :---- | :---------- |
| id (**required**) | `[methodId]` | [One sentence saying what the method does at the key level, or leave blank if obvious from the opening paragraph.] |
| [param1] (**required**) | [value type or enum] | [Description. See sentence-word-guidance.md for how to write this.] |
| [param2] | [value type or enum]. default: `[default]` | [Description.] |

<!--
Column guidelines:
- "key" column: param name as it appears in JSON (camelCase). Mark required with (**required**). Mark deprecated with **(Deprecated)**.
- "value" column: the type ("boolean", "string", "number", "object", "array of objects") or enum values separated by commas. Append ". default: `value`" for optional params with defaults.
- "description" column: what it does, when to use it, what each enum value means.
  - For enum values with distinct behaviors, describe each option on its own line or with <br/> breaks.
  - For params that interact with other params, end with a note: "For more information, see [param X] parameter."
-->

# Examples

<!-- Simple method (one example): -->
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

<!-- Multiple examples: Use H2 subheadings with descriptive names.
     Format: "## Example: [Descriptive name]" or "## Example 1" / "## Example 2" if not easily named.
     Each example follows the same Config / Example document / Output structure above. -->

<!-- # Notes (OPTIONAL) -->
<!-- Add a Notes section when the method has non-obvious behavior that doesn't fit in parameter
     descriptions — e.g., how the algorithm works, performance characteristics, edge cases.
     Use H2 subheadings within Notes for multiple topics. -->
```

---

## Method category variations

### Layout-based method
- Opening: imperative, describes physical extraction ("Extracts lines...", "Extracts data in a rectangular region...")
- Always references Global parameters note
- Example always includes an actual PDF config + output

### LLM-based method
- Opening: describes what kinds of data the method extracts, and may note when to use multimodal or chaining
- Often includes a "Prompt Tips" subsection before Parameters
- Parameter table may have multiple sub-tables (one for the field-level params, one for the method object params)
- Notes section is common, explaining how context-finding works

### Computed field method
- Opening: "Define..." or "Returns..." — describes the computation
- Uses different note before Parameters ("in the computed field's global Method parameter")
- Config examples use `"computed_fields": [...]` array, not `"fields": [...]`
- Commonly references `parsed_document` in descriptions

### Preprocessor
- Opening: imperative, describes what it does to the document before extraction
- No "Global parameters" note (preprocessors don't share a global method object)
- Config examples show the preprocessor in a `"preprocessors": [...]` array
- Examples often omit the Example document section if the visual isn't helpful

### Sections
- Opening: describes what "sections" are and what the method enables
- Config examples use `"type": "sections"` on a field with a nested `"fields"` array
- Often includes diagrams showing horizontal vs. vertical section directions
