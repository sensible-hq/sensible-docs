---
title: "Merge lines"
hidden: false
---

Merges lines distributed along a horizontal axis more aggressively than the built-in line merger. This preprocessor solves line-recognition problems caused by poor-quality document scans, handwritten text, and other formatting issues. For example, this preprocessor solves:

- oversplit lines
- lines overlapping on the x-axis
- "jittery" lines misaligned on the y-axis

 There are limitations to the combinations of parameter values you can set. For more information, see the Notes section.

As an alternative to this preprocessor, use a multimodal LLM. See the Query Group method's [Multimodal Engine](doc:query-group#parameters) parameter for more information.

[**Parameters**](doc:merge-lines#parameters)
[**Examples**](doc:merge-lines#examples)
[**Notes**](doc:merge-lines#notes)

Parameters
====

| key                                      | value                                  | description                                                  |
| ---------------------------------------- | -------------------------------------- | ------------------------------------------------------------ |
| type (**required**)                      | `mergeLines`                           | merges lines distributed along a horizontal axis.            |
| directlyAdjacentThreshold (**required**) | number >= 0.16                         | Threshold for merging adjacent lines when you don't want the output lines separated by whitespaces. For example, use this parameter to merge one-letter lines into a one-word line. Choosing a larger number merges more aggressively.<br/>If you configure the document type's OCR engine to use Google, then Sensible recommends using this parameter's default value. <br/>In detail, if the distance between two adjacent lines is equal to or smaller than the threshold defined in this parameter, Sensible merges the lines. This parameter expresses the distance as a fraction of the lines' height.<br/>For limitations on the values you can set for this parameter, see the Notes section. |
| adjacentThreshold (**required**)         | number >= 0.6                          | Threshold for merging adjacent lines when you want the output lines separated by whitespaces. For example, use this to merge cells in a row into one line. Sensible joins the lines returned by the method using one whitespace as the separator. Choosing a larger number merges more aggressively. <br/>In detail, the behavior of this parameter is the same as for the Directly Adjacent Threshold parameter, except that Sensible inserts a whitespace between merged lines.<br/>For limitations on the values you can set for this parameter, see the Notes section. |
| yOverlapThreshold                        | number between 0 and 1.0. default: 1.0 | Merges lines that aren't perfectly aligned at the same height on the page. <br/> Specifies the y overlap above which the Merge Lines preprocessor merges two adjacent lines. Y overlap is the section of the joint y-axis range of two lines that's occupied by both lines. For example, if two lines share the same minimum and maximum y-axis values, their overlap is 1. If one line's extent is from 0 to 10 and the other line’s extent is from 2 to 12 on the y-axis, their overlap is .667 (8 / 12). <br/>For an example, see the Examples section. |
| minXGapThreshold                         | number in inches                       | Configure this parameter if two lines overlap on an x-axis. The default behavior is to merge these overlapping lines into one line. To split them instead, set a cap on the amount of allowable overlap. For example:<br/>0 - splits lines if their line boundaries are touching but not overlapping.<br/>0.1 - splits lines if their boundaries overlap a little, up to 0.1 inches.<br/>2.0 - splits lines even when they overlap a lot, up to 2.0 inches. |

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
        /* Ensure the document type's OCR Engine parameter is set to Google for this example */
      
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