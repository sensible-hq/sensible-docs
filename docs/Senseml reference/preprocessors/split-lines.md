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

| key                      | value                                                        | description                                                  |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| type (**required**)      | `splitLines`                                                 | splits lines distributed along a horizontal axis.            |
| minSpaces (**required**) | number                                                       | The number of consecutive whitespace characters (` `) at or above which to split lines. |
| separator                | string                                                       | Modifies the Min Spaces parameter to split on the specified character, for example "-", instead of the default whitespace character. For example, if you specify `"-"` for this parameter and `2` for the Min Spaces parameter, then Sensible splits lines when it finds `--`. |
| match<br/>or<br/>range   | A [Match](doc:match) object or array of Match objects<br/><br/>or<br/><br/>Range object | Specifies the matching pages or repeating document ranges ("sections") in which to run this preprocessor.<br/><br/>`match`: Sensible runs this preprocessor on each page containing the matched text.<br/><br/>`range`: Sensible runs this preprocessor in the specified repeating document ranges, leaving lines outside the range unchanged. For information about this option's parameters, see the [Range](doc:sections#range-parameters) parameters for horizontal sections. For an example, see [Example 2](doc:split-lines#example-2). |

#### Limitations

When you configure the Split Lines preprocessor, the Sensible app's [line](doc:line) rendering is approximate and can be inaccurate. To accurately view a line's raw text, [select](doc:color#purple-box) the line.

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

The following example shows using the Range parameter to split lines in specified sections of a typewritten, scanned musical instrument cover order forms. This configuration enables you to extract repeating data from multiple order forms.

**PROBLEM**

Without the Split Lines preprocessor, the OCR preprocessor merges the lines too aggressively, so that the Nearest Checkbox method can't recognize which checkbox belongs to which label in the Length and Circumference sections of the document:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/split_lines_range_1.png)

However, if you apply Split Lines preprocessor to the entire document, Sensible splits lines too aggressively, so that individual words are split into letters:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/split_lines_range_2.png)

**SOLUTION**

Two Split Line preprocessors use the Range parameter to specify only the Length and Circumference sections, splitting the overmerged sections and leaving the rest of the document unaffected.

**Config**

```json
{
  "zip": [
    {
      "length": {
        "value": "15in",
        "type": "string"
      },
      "circumference": {
        "value": "17.5in",
        "type": "string"
      },
      "side": {
        "value": "right_side",
        "type": "string"
      }
    },
    {
      "length": {
        "value": "13.5in",
        "type": "string"
      },
      "circumference": {
        "value": "16in",
        "type": "string"
      },
      "side": {
        "value": "left_side",
        "type": "string"
      }
    }
  ]
}
```

**Example document**

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/split_lines_range.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/split_lines_range.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------------------ |

**Output**

```json
{
  "length_sections": [
    {
      "length": {
        "value": "15in",
        "type": "string"
      }
    },
    {
      "length": {
        "value": "13.5in",
        "type": "string"
      }
    }
  ],
  "circumference_sections": [
    {
      "circumference": {
        "value": "17.5in",
        "type": "string"
      }
    },
    {
      "circumference": {
        "value": "16in",
        "type": "string"
      }
    }
  ],
  "side_sections": [
    {
      "side": {
        "value": "right_side",
        "type": "string"
      }
    },
    {
      "side": {
        "value": "left_side",
        "type": "string"
      }
    }
  ]
}
```
