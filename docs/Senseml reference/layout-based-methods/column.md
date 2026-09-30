---
title: Column
excerpt: Learn how the Column method extracts lines above or below an anchor line
  based on x extent alignment or 50% overlap, with parameters and examples.
deprecated: false
hidden: false
metadata:
  title: ''
  description: Learn how the Column method extracts lines above or below an anchor
    line based on x extent alignment or 50% overlap, with parameters and examples.
  robots: index
next:
  description: ''
---
Extracts all lines below or above the anchor line on the current page if:

* The anchor line's left and right boundaries ("x extent") contain the target lines' x extent, or vice versa. 

  Or:

* The anchor line and target lines overlap by at least 50% of the narrower line's x extent.

By default, the method extracts to the edge of the page. To stop extracting at a specific line, such as the next label in a single-column form, use the Stop parameter.

[**Parameters**](doc:column#parameters)\
[**Examples**](doc:column#examples)

# Parameters

| key               | value                              | description                                                  |
| :---------------- | :--------------------------------- | :----------------------------------------------------------- |
| id (**required**) | `column`                           |                                                              |
| tiebreaker        | tiebreaker                         | For information about this global parameter, see [Method](doc:method#parameters). |
| includeAnchor     | `true`, `false`. default: false    | Includes the anchor line in the method output                |
| position          | `below`, `above`. default: `below` | Matches above or below the anchor line. For example, if you anchor on the bottom line of a column, set this to `above` to extract the column. |
| stop              | [Match object](doc:match)          | Stops extraction at the closest matching line in the direction you specify with the Position parameter. The matched line isn't included in the method output. For example, use this parameter on a single-column form to stop at the next label, so that the method doesn't also extract that label and its value.<br/>For `"position": "below"`, stops at the top boundary of the matched line. For `"position": "above"`, stops at the bottom boundary of the matched line.<br/>The matched line doesn't need to align with the anchor line. Sensible searches all lines on the page below or above the anchor, so a matching line in a neighboring column also stops extraction.<br/>If the matched line immediately follows the anchor line, for example because the document leaves the value blank, returns null.<br/>If you don't specify this parameter, or if no line matches, extracts to the edge of the page. |

# Examples

## Example: Extract a column

The following example shows that:

* By default, Sensible returns the entire column as a joined string.
* Specifying a tiebreaker returns single element in the column.

**Config**

```json
{
  "fields": [
    {
      "id": "example_column",
      "anchor": "may 2020",
      "type": "string",
      "method": {
        "id": "column"
      }
    },
    {
      "id": "example_column_2",
      "anchor": "may 2020",
      "type":"number",
      "method": {
        "id": "column",
        "tiebreaker": ">"
      }
    }
  ]
}
```

**Example document**\
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/column.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/row_column.pdf) |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "example_column": {
    "type": "string",
    "value": "1 3 2 4 5"
  },
  "example_column_2": {
    "source": "5",
    "value": 5,
    "type": "number"
  }
}
```

## Example: Stop at the next label

The following example shows using the Stop parameter to extract a value from a single-column form, where each value appears on the line after its label. Without the Stop parameter, the `vehicle_type` field returns `Sedan Coverage: Full`. With the Stop parameter, the field stops at the Coverage label and returns `Sedan`.

If the document leaves the vehicle type blank, then the Coverage label immediately follows the Type label, and the field returns null instead of extracting the Coverage label and its value.

**Config**

```json
{
  "fields": [
    {
      "id": "vehicle_type",
      "anchor": "type:",
      "type": "string",
      "method": {
        "id": "column",
        /* stop before the next label in the column */
        "stop": {
          "type": "startsWith",
          "text": "coverage"
        }
      }
    }
  ]
}
```

**Output**

```json
{
  "vehicle_type": {
    "type": "string",
    "value": "Sedan"
  }
}
```
