# Sentence-Level and Word-Level Guidance

This file covers how to write parameter descriptions, terminology rules, and specific phrasing patterns for SenseML reference docs. It is consumed by LLM agents writing or updating reference pages.

---

## Parameter table: how to write each column

### key column
- Write the JSON key in camelCase as it appears in the config: `position`, `sortLines`, `textAlignment`
- Mark required parameters: `paramName (**required**)`
- Mark deprecated parameters: `**(Deprecated)** paramName`
- Do not backtick the key name in the key column (the table formatting is sufficient)
- **Preprocessors**: the identifying parameter uses key `type`, not `id`. Example: `type (**required**)` with value `mergeLines`.

### value column
Write the type and, for optional params, the default. Use these exact formats:

| Situation | Format in value column |
| --------- | ---------------------- |
| Required enum | `` `above`, `below`, `left`, `right` `` |
| Optional enum with default | `` `above`, `below`, `left`, `right`. default: `first` `` |
| Boolean with default | `` boolean. default: `false` `` |
| Number with default | `` number. default: `0` `` |
| Number in inches with default | `` number in inches. default: `0.08` `` |
| String (any value) | `string` |
| Object | `object` |
| Array of objects | `array of objects` |
| Array of strings | `string array` |
| Multiple distinct types | Use `<br/>or<br/>` between types |
| Integer or ordinal options | `` integer (zero-based index)<br/>or<br/>`first`, `second`, `third`, `last`<br/>or<br/>`>`, `<` `` |

When a parameter accepts multiple distinct types with meaningfully different behavior, stack them with `<br/>or<br/>` separating each type.

### description column

**Lead with what it does.** Don't start with "This parameter..." or "Use this to...". Start with a verb or noun phrase:
- "Specifies the direction of the target data relative to the anchor point."
- "Filters out the specified lines from the method's output."
- "The number of top-scoring document chunks Sensible combines as context."
- "Merges lines that aren't perfectly aligned at the same height on the page."

**For enum values:** After the overview sentence, describe each option. Use `<br/>` for line breaks within a cell:
```
Specifies [what]. <br/>For `value1`, [what happens]. <br/>For `value2`, [what happens].
```

**For boolean flags:** State what happens when true. The default is usually false, so describe the non-default behavior:
- "Specifies whether to include the anchor text in the output."
- "Makes the offsets relative to the 0,0 origin at the top left of the page rather than to the Start parameter."
- "Set this parameter to true to troubleshoot optional character recognition (OCR) in a table."

**For interactions and incompatibilities:** When a parameter only works under certain conditions, or is incompatible with others, say so at the end of the description:
- "Use with `\"position\": \"below\"`."
- "If you configure this parameter, then the Confidence Signals parameter isn't supported."
- "Sensible ignores this parameter when searching for a field's anchor."
- "Not supported if you specify the Multimodal Engine parameter or Source Ids parameter."

For methods with many interactions, move interaction notes to a 4th `interactions` column rather than putting them in the description.

**Referencing a global param without duplicating it:**
When a method's table lists a global param for completeness, use this shorthand in both value and description columns:
```markdown
| tiebreaker | For information about this global parameter, see [Method](doc:method#parameters). | For information about this global parameter, see [Method](doc:method#parameters). |
```

**Cross-references:** Link to related pages when mentioning a named concept: `[Match object](doc:match)`, `[types](doc:types)`, `[JsonLogic](doc:jsonlogic)`, `[context](doc:prompt)`.

---

## Terminology: use these words consistently

| Concept | Use this term | Avoid |
| ------- | ------------- | ----- |
| The JSON configuration file | "config" or "configuration" | "template", "schema" (schema has a specific meaning) |
| The result Sensible returns | "output", "extracted field", "field" | "result object", "response" (that's the API response) |
| The text Sensible matches to find a location | "anchor", "anchor line", "anchor point" | "reference text", "marker" |
| The document text sent to an LLM | "context" | "prompt context", "input" |
| A scored portion of the document for LLM use | "chunk" | "segment", "section" (has a specific SenseML meaning) |
| The SenseML data output type | "type" (e.g., "currency type", "date type") | "data type", "field type" |
| A defined extraction unit | "field" | "extraction", "key" |
| Repeated document structures | "sections" | "repeating groups", "loops" |
| An extraction that returned nothing | "null" | "empty", "undefined", "no value" |
| The Sensible product | "Sensible" (always capitalized) | "sensible", "the tool", "the engine" |
| The document excerpt Sensible renders visually | "the Sensible app" | "the UI", "the editor" |
| JSON path into extracted output | "dot notation" (e.g., `claims.columns.3.values`) | "object path", "key path" |

---

## Describing required vs. optional clearly

In prose (outside the parameter table):

**Required:** "The Start parameter is required." / "You must also specify `\"type\": \"table\"` in the field's parameters."
**Optional:** "If unspecified, defaults to `first`." / "By default, Sensible [does X]."
**Conditional:** "Required if you configure the Multimodal Engine parameter." / "Required when you specify a Stop parameter."

---

## Describing what a method returns when no match is found

State null behavior explicitly when it's non-obvious:
- "Returns null if the anchor isn't present in the document."
- "Sensible returns null for the fields in this query group if the anchor isn't present."
- "If the source field doesn't exist or is null, Sensible ignores this parameter and always returns null."

---

## Notes and callouts

Use `**Note:**` (bold inline) for important context within a section. Do not use `> ` blockquote syntax.

Standard note before layout-based method parameter tables:
```
**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.
```

Standard note before computed field method parameter tables:
```
The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter:
```

NLP preprocessor note (when params apply at both config and field level):
```
The following parameters are available both on the config level and for each individual field through the method's parameters. Setting a parameter at the method level overrides it at the config level.
```

---

## Describing interactions between parameters

Describe interactions in the description of the more specific/subordinate parameter, not the parent. Cross-reference with a link or with plain text referring to the parameter by Title Case name.

Example from `query-group`:
- In `source_ids` description: "If you configure this parameter, then the following parameters aren't supported: Anchor parameter, Confidence Signals, Multimodal Engine parameter..."
- In `multimodalEngine` description: "If you configure this parameter, then the Confidence Signals parameter isn't supported."

For methods with many interdependencies, use the 4-column table format with an explicit `interactions` column.

---

## Numbers and measurements

- Inch measurements: decimal numbers with units — "0.2 inches", "0.1 inches", "0.08 inches". Not "two-tenths of an inch".
- Zero-based indexes: always say "zero-based index" on first use.
- Percentages: "90%" not "90 percent".
- Fractions used in threshold descriptions: state as decimals — "0.667" not "two-thirds".

---

## Code examples: inline comments

Use `//` for single-line comments and `/* */` for multi-line comments in JSON configs. The Sensible engine accepts relaxed JSON. Comment to explain non-obvious choices, not to restate what the parameter name already says.

Good: `/* Use a multimodal LLM to troubleshoot problems with OCR */`
Good: `/* Ensure the document type's OCR Engine parameter is set to Google for this example */`
Redundant: `/* set position to below */`

---

## Describing the `id` parameter for methods

The `id` parameter description for layout-based methods often describes a proximity constraint or key behavior rather than the method name itself. Example from label:

```markdown
| id (**required**) | `label` | The gap between the borders of the target line and the anchor line must be 0.2 inches or less. |
```

If there's no meaningful constraint to state, leave the description blank or write a one-sentence summary that restates the opening paragraph's core point. Do not write "Specifies the method type" — that's obvious from the value.
