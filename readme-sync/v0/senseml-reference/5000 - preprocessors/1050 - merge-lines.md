---
title: "Merge lines"
hidden: false
---

Merges lines distributed along a horizontal axis more aggressively than the built-in line merger. This preprocessor solves line-recognition problems caused by poor-quality document scans, handwritten text, and other formatting issues. For example, this preprocessor solves:

- oversplit lines
- lines overlapping on the x-axis
- "jittery" lines misaligned on the y-axis

 There are limitations to the combinations of parameter values you can set. For more information, see the Notes section.

[**Parameters**](doc:merge-lines#parameters)
[**Examples**](doc:merge-lines#examples)
[**Notes**](doc:merge-lines#notes)

Parameters
====

| key                                      | value                                  | description                                                  |
| ---------------------------------------- | -------------------------------------- | ------------------------------------------------------------ |
| type (**required**)                      | `mergeLines`                           | merges lines distributed along a horizontal axis.            |
| directlyAdjacentThreshold (**required**) | number >= 0.16                         | Merges adjacent lines that aren't separated by whitespace in the source text.  For example, merges one-letter lines into a one-word line. Choosing a larger number merges more aggressively.<br/>If you configure the document type's OCR engine to use Google, then Sensible recommends using this parameter's default value. <br/>In detail, this parameter specifies the fraction of line height under which to merge two adjacent lines distributed along an x-axis.<br/>For limitations on the values you can set for this parameter, see the Notes section. |
| adjacentThreshold (**required**)         | number >= 0.6                          | Merges adjacent lines separated by whitespace in the source text. For example, merges cells in a row into one line. Sensible joins the lines returned by the method using one whitespace as the separator. Choosing a larger number merges more aggressively. <br/>In detail, specifies the fraction of line height under which to merge two adjacent lines distributed along an x-axis.<br> For an example, see the Examples section.<br/>For limitations on the values you can set for this parameter, see the Notes section. |
| yOverlapThreshold                        | number between 0 and 1.0. default: 1.0 | Merges lines that aren't perfectly aligned at the same height on the page. <br/> Specifies the y overlap above which the Merge Lines preprocessor merges two adjacent lines. Y overlap is the section of the joint y-axis range of two lines that's occupied by both lines. For example, if two lines share the same minimum and maximum y-axis values, their overlap is 1. If one line's extent is from 0 to 10 and the other line’s extent is from 2 to 12 on the y-axis, their overlap is .667 (8 / 12). <br/>For an example, see the Examples section. |
| minXGapThreshold                         | number in inches                       | Configure this parameter if two lines overlap on an x-axis. The default behavior is to merge these overlapping lines into one line. To split them instead, set a cap on the amount of allowable overlap. For example:<br/>0 - splits lines if their line boundaries are touching but not overlapping.<br/>0.1 - splits lines if their boundaries overlap a little, up to 0.1 inches.<br/>2.0 - splits lines even when they overlap a lot, up to 2.0 inches.<br/>For an example, see the Examples section. |

Examples
====

Handwriting OCR 
----

Use the Merge Lines preprocessor to clean up OCRed handwriting text. This preprocessor is useful for Google OCR, which by default groups text into words rather than lines.

**PROBLEM**

Without a Merge Line preprocessor, the placeholder handwritten data in an example document is oversplit by Google OCR:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/merge_lines_ocr_2.png)

For example, the phrase `Name (First, Middle, Last, Suffix, Trust or Custodian)` isn't one line, but is instead split on words.

**SOLUTION**

CONFIG

```json
{
  "preprocessors": [
    {
      "type": "mergeLines",
      "directlyAdjacentThreshold": 0.15,
      "adjacentThreshold": 0.8,
      "yOverlapThreshold": 0.8,
      "minXGapThreshold": 0.1
    }
  ],
  "fields": [
    {
      "id": "name_line",
      "anchor": "Name",
      "method": {
        "id": "label",
        "position": "right",
        "includeAnchor": true
      },
    }
]
}
```

Example document

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/merge_lines_ocr.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/merge_lines_ocr.pdf) |
| ----------- | ------------------------------------------------------------ |

To run this example, verify that the document type uses Google OCR (click the gear icon for the Document Type and select **Google**): 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/merge_lines_ocr_1.png)

OUTPUT

```json
{
  "name_line": {
    "type": "string",
    "value": "Name (First, Middle, Last, Suffix, Trust or Custodian)"
  }
}
```

Modify this example to observe the effects of the different parameters on the output. For example:

- set `"adjacentThreshold": 0.1` to see oversplit lines. 

- set `"adjacentThreshold": 2.0` to see aggressively merged lines. 

- revert Adjacent Threshold to the original setting, then set `"yOverlapThreshold": 0.2`  to observe how lines with misaligned heights (like the email address) merges more aggressively.

  


Oversplit lines
----

**PROBLEM**

The following image shows oversplit lines. For example, Sensible splits the phrase "premium driver discount" into three lines even though the human eye perceives it as one phrase:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/merge_lines_oversplit_1.png)

**SOLUTION**

The following example shows using the Merge Lines preprocessor to fix the oversplit lines and find a discount amount for a specific vehicle.

CONFIG

```json
{
  "preprocessors": [
    {
      "type": "mergeLines",
      "directlyAdjacentThreshold": 0.16,
      "adjacentThreshold": 1
    }
  ],
  "fields": [
    {
      "id": "premier_driver_discount",
      "type": "currency",
      "method": {
        "id": "row"
      },
      "anchor": {
        "match": {
          "type": "includes",
          "text": "premier driver discount"
        },
        "end": {
          "type": "includes",
          "text": "vehicle 06"
        }
      }
    }
  ]
}
```

Example document

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/merge_lines_oversplit_2.png)

OUTPUT

```json
{
  "premier_driver_discount": {
    "source": "113.00",
    "value": 113,
    "unit": "$",
    "type": "currency"
  }
}
```
Jittery lines on a y-axis
----

The following example shows using the Y Overlap parameter to correct vertical misalignment or "jitter" in lines (for example, as the result of a low-quality scan or because of handwriting).

**Config**

```json
{
  "preprocessors": [
    {
      "type": "mergeLines",
      "directlyAdjacentThreshold": 0.16,
      "adjacentThreshold": 1.5,
      "yOverlapThreshold": 0.1
    }
  ],
  "fields": [
    {
      "id": "merged_line",
      "method": {
        "id": "label",
        "position": "right",
        "includeAnchor": true
      },
      "anchor": "these two"
    }
  ]
}
```



**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/merge_lines_yoverlap.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/merge_lines_yoverlap.pdf) |
| ------------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "merged_line": {
    "type": "string",
    "value": "These two lines are imperfectly aligned They have a y overlap less than 1"
  }
}
```
Overlapping lines on an x-axis
----

The following example shows using the Min X Gap Threshold parameter to extract overlapping text in a poorly formatted document. In this example, the built-in behavior without a Min X Gap Threshold is to merge the overlapping lines into one line (`Supplementary underinsured/uninsured motorist coverage500,000 USD Combined single limit incl. umbl`). 

The Min X Gap Threshold preserves the intended document formatting, which is a two-column table. By preserving this format, you can consistently use the Row method on the table in this document, as well as in other examples of this table in documents in which the lines don't overlap.

**Config**

```json
{
  "preprocessors": [
    {
      "type": "mergeLines",
      "directlyAdjacentThreshold": 0.16,
      "adjacentThreshold": 0.6,
      "minXGapThreshold": 1.0
    }
  ],
  "fields": [
    {
      "id": "underinsured_limit",
      "method": {
        "id": "row"
      },
      "anchor": "supplementary",
  
    }
  ]
}
```

**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/merge_lines_minxgap.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/merge_lines_minxgap.pdf) |
| ----------------------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "underinsured_limit": {
    "type": "string",
    "value": "500,000 USD Combined single limit incl. umbl"
  }
}
```

Notes
====
Because the Merge Lines preprocessor evaluates after the built-in line merger, there are limitations to the combinations of parameter values you can set:

**yOverlapThreshold** 

In general, when you set `"yOverlapThreshold":1.0` or leave its value unspecified, then you set `"adjacentThreshold"` to 0.6 or higher.

In this situation,   `"directlyAdjacentThreshold"` and `"adjacentThreshold"` have no effect if both their values are less than 0.6. In other words, the following configuration has **no** effect:

```json
    {
      "type": "mergeLines",
      "directlyAdjacentThreshold": 0.5,
      "adjacentThreshold": 0.5,
     "yOverlapThreshold": 1,

    }

```

