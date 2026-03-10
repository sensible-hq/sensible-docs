# Sentence-Level and Word-Level Guidance

This file covers how to write parameter descriptions, terminology rules, and specific phrasing patterns for SenseML reference docs. It is consumed by LLM agents writing or updating reference pages.

---

## Parameter table: how to write each column

### key column
- Write the JSON key in camelCase as it appears in the config: `position`, `sortLines`, `textAlignment`
- Mark required parameters: `paramName (**required**)`
- Mark deprecated parameters: `**(Deprecated)** paramName`
- Do not backtick the key name in the key column (the table formatting is sufficient)

### value column
Write the type and, for optional params, the default. Use these exact formats:

| Situation | Format in value column |
| --------- | ---------------------- |
| Required enum | `above`, `below`, `left`, `right` |
| Optional enum with default | `above`, `below`, `left`, `right`. default: `first` |
| Boolean with default | boolean. default: `false` |
| Number with default | number. default: `0` |
| String (any value) | string |
| Object | object |
| Array of objects | array of objects |
| Array of strings | string array |
| Multiple allowed types | `integer` (zero-based index)<br/>or<br/>`first`, `second`, `third`, `last`<br/>or<br/>`>`, `<` |

When a parameter accepts multiple distinct types with meaningfully different behavior, use `<br/>or<br/>` between each type. This renders as stacked options in the table.

### description column

**Lead with what it does.** Don't start with "This parameter..." or "Use this to...". Start with a verb or noun phrase:
- "Specifies the direction of the target data relative to the anchor point."
- "Filters out the specified lines from the method's output."
- "The number of top-scoring document chunks Sensible combines as context."

**For enum values:** After the overview sentence, describe each option. Use `<br/>` for line breaks within a cell. Use a consistent pattern:
```
Specifies [what].
For `value1`, [what happens].
For `value2`, [what happens].
```

**For boolean flags:** State what happens when true. The default is usually false, so describe the non-default behavior:
- "Specifies whether to include the anchor text in the output." (for includeAnchor)
- "Makes the offsets relative to the 0,0 origin at the top left of the page rather than to the Start parameter." (for isAbsoluteOffset)

**For interactions:** When a parameter only applies in certain conditions, or is incompatible with other parameters, say so directly:
- "Use with `\"position\": \"below\"`."
- "If you configure this parameter, then the Confidence Signals parameter isn't supported."
- "Sensible ignores this parameter when searching for a field's anchor."

**Cross-references:** Link to related pages when you mention a named concept the user might need to look up. Use `doc:` slugs: `[Match object](doc:match)`, `[types](doc:types)`, `[JsonLogic](doc:jsonlogic)`.

---

## Terminology: use these words consistently

| Concept | Use this term | Avoid |
| ------- | ------------- | ----- |
| The JSON configuration file | "config" or "configuration" | "template", "schema" (schema refers to something else) |
| The result Sensible returns | "output", "extracted field", "field" | "result object", "response" (that's the API response) |
| The text Sensible matches to find a location | "anchor", "anchor line", "anchor point" | "reference text", "marker" |
| The document text Sensible sends to an LLM | "context" | "prompt context", "input" |
| A portion of the document for LLM scoring | "chunk" | "segment", "section" (section has a specific SenseML meaning) |
| The SenseML data output type | "type" (e.g., "currency type", "date type") | "data type", "field type" (redundant) |
| A defined extraction unit | "field" | "extraction", "key" |
| Repeated document structures | "sections" | "repeating groups", "loops" |
| An extraction that returned nothing | "null" | "empty", "undefined", "no value" |
| The Sensible product | "Sensible" (always capitalized) | "sensible", "the tool", "the engine" |

---

## Describing required vs. optional clearly

In prose (outside the parameter table), use these patterns:

**Required:** "The Start parameter is required." / "You must specify..."
**Optional:** "If unspecified, defaults to `first`." / "By default, Sensible [does X]."
**Conditional:** "Required if you configure the Multimodal Engine parameter." / "Optional when [condition]."

---

## Describing what a method returns when no match is found

Always state null behavior explicitly in parameter or method descriptions when it's non-obvious:
- "Returns null if the anchor isn't present in the document."
- "Sensible returns null for the fields in this query group if the anchor isn't present."

---

## Notes and callouts

Use `**Note:**` (bold, not a blockquote) for in-line notes that add important context within a section:

```markdown
**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.
```

Do not use `> ` blockquote syntax for notes — the existing docs don't use it.

---

## Describing interactions between parameters

When two parameters interact, describe the interaction in the description of the more specific/subordinate parameter, not the parent. Cross-reference with a link.

Example from `query-group`:
- In `source_ids` description: "If you configure this parameter, then the following parameters aren't supported: Anchor parameter, Confidence Signals, Multimodal Engine parameter..."
- In `multimodalEngine` description: "If you configure this parameter, then the Confidence Signals parameter isn't supported."

---

## Numbers and measurements

- Inch measurements: always write as decimal numbers with units: "0.2 inches", "0.1 inches". Not "two-tenths of an inch".
- Zero-based indexes: always say "zero-based index" on first use in a description.
- Percentages: write as "90%" not "90 percent".

---

## Code examples: inline comments

Use `//` for single-line comments and `/* */` for multi-line comments in JSON configs. The Sensible engine accepts relaxed JSON. Use comments to explain non-obvious config choices — not to restate what the parameter name already says.

Good comment: `/* Use a multimodal LLM to troubleshoot problems with OCR. */`
Redundant comment: `/* set position to below */`

Inline comment style in the existing docs tends toward brief explanatory notes rather than step-by-step narration. Only comment things a reader might wonder about.
