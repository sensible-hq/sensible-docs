---
title: Split lines
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Split merged text lines'
  robots: index
next:
  description: ''
---
Splits lines distributed along a horizontal axis. This preprocessor is most useful for typewriter-style documents that use whitespaces for formatting. 

# Parameters

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                      | value                                                 | description                                                                                                                                                                                                                                                                    |
| ------------------------ | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| type (**required**)      | `splitLines`                                          | splits lines distributed along a horizontal axis.                                                                                                                                                                                                                              |
| minSpaces (**required**) | number                                                | The number of consecutive whitespace characters (` `) at or above which to split lines.                                                                                                                                                                                   |
| separator                | string                                                | Modifies the Min Spaces parameter to split on the specified character, for example "-", instead of the default whitespace character. For example, if you specify `"-"` for this parameter and `2` for the Min Spaces parameter, then Sensible splits lines when it finds `--`. |
| match<br/>or<br/>range   | A [Match](doc:match) object or array of Match objects<br/><br/>or<br/><br/>Range object | Specifies the matching pages or repeating document ranges ("sections") in which to run this preprocessor.<br/><br/>`match`: Sensible runs this preprocessor on each page containing the matched text.<br/><br/>`range`: Sensible runs this preprocessor in the specified repeating document ranges, leaving lines outside the range unchanged. For information about this option's parameters, see the [Range](doc:sections#range-parameters) parameters for horizontal sections. |

# Examples

## Example 1

The following example shows solving undersplit lines in a "typewritten" style document. The Split Lines preprocessor preserves columns and rows in this document.

**PROBLEM**

Without the Split Lines preprocessor, Sensible merges the lines too aggressively:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/split_lines_2.png)

**SOLUTION**

**Config**

```json
{
  "preprocessors": [
    {
      "type": "splitLines",
      "minSpaces": 3
    }
  ],
  "fields": [
    {
      "id": "policy_number",
      "method": {
        "id": "row",
      },
      "anchor": "policy number",
    }
  ]
}
```

**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/split_lines.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/split_lines.pdf) |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "policy_number": {
    "type": "string",
    "value": "18-376-190"
  }
}
```

## Example 2

The following example shows using the `range` parameter to split lines in specific sections of a typewritten instrument cover order form. OCR collapses the measurement labels and checkboxes in the cover length and cover circumference sections into single merged lines, preventing `nearestCheckbox` from locating individual labels. Two `splitLines` preprocessors with `range` target only those sections, leaving the rest of the document unaffected.

**Config**

```json
{
  "preprocessors": [
    {
      /* this document is a scan */
      "type": "ocr",
      "matchAll": true,
      "match": ""
    },
    {
      /* OCR merges measurement labels and checkboxes into a single line in this section.
         Use range to target only the length section, leaving other sections unchanged. */
      "type": "splitLines",
      "minSpaces": 1,
      "range": {
        "anchor": {
          "match": {
            "type": "includes",
            "text": "cover length"
          }
        },
        "stop": {
          "type": "includes",
          "text": "cover circumference"
        }
      }
    },
    {
      /* target only the circumference section */
      "type": "splitLines",
      "minSpaces": 1,
      "range": {
        "anchor": {
          "match": {
            "type": "includes",
            "text": "cover circumference"
          }
        },
        "stop": {
          "type": "includes",
          "text": "cover shape"
        }
      }
    }
  ],
  "fields": [
    {
      "id": "_length_section",
      "type": "sections",
      "range": {
        "anchor": { "match": { "text": "cover length", "type": "includes" } },
        "stop": { "text": "cover circumference", "type": "includes" },
        "stopOffsetY": -0.1
      },
      "fields": [
        { "id": "13in", "anchor": { "match": { "text": "13in", "type": "equals" } }, "method": { "id": "nearestCheckbox", "position": "left", "offsetY": -0.25 } },
        { "id": "13.5in", "anchor": { "match": { "text": "13.5in", "type": "equals" } }, "method": { "id": "nearestCheckbox", "position": "left", "offsetY": -0.25 } },
        { "id": "14in", "anchor": { "match": { "text": "14in", "type": "equals" } }, "method": { "id": "nearestCheckbox", "position": "left", "offsetY": -0.25 } },
        {
          /* a production config lists all sizes (10in–20in) as source_ids */
          "id": "length",
          "method": { "id": "pickValues", "source_ids": ["13in", "13.5in", "14in"], "match": "one" }
        }
      ]
    },
    {
      "id": "_circumference_section",
      "type": "sections",
      "range": {
        "anchor": { "match": { "text": "cover circumference", "type": "includes" } },
        "stop": { "text": "cover shape", "type": "includes" },
        "stopOffsetY": -0.2
      },
      "fields": [
        { "id": "15.5in", "anchor": { "match": { "text": "15.5in", "type": "equals" } }, "method": { "id": "nearestCheckbox", "position": "left", "offsetY": -0.25 } },
        { "id": "16in", "anchor": { "match": { "text": "16in", "type": "equals" } }, "method": { "id": "nearestCheckbox", "position": "left", "offsetY": -0.25 } },
        { "id": "16.5in", "anchor": { "match": { "text": "16.5in", "type": "equals" } }, "method": { "id": "nearestCheckbox", "position": "left", "offsetY": -0.25 } },
        {
          "id": "circumference",
          "method": { "id": "pickValues", "source_ids": ["15.5in", "16in", "16.5in"], "match": "one" }
        }
      ]
    },
    {
      "id": "length",
      "method": { "id": "customComputation", "jsonLogic": { "var": "_length_section.0.length.value" } }
    },
    {
      "id": "circumference",
      "method": { "id": "customComputation", "jsonLogic": { "var": "_circumference_section.0.circumference.value" } }
    },
    {
      "id": "clean",
      "method": { "id": "suppressOutput", "source_ids": { "pattern": "^_.*" } }
    }
  ]
}
```

**Example document**

In sections 2 and 3, OCR collapses measurement labels and their checkboxes into a single merged line. The `range` parameter targets only those sections for splitting.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/split_lines_range.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/split_lines_range.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------------------ |

**Output**

```json
{
  "length": {
    "value": "13.5in",
    "type": "string"
  },
  "circumference": {
    "value": "16in",
    "type": "string"
  }
}
```
