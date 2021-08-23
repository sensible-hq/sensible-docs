---
title: "Merge lines"
hidden: false
---

Merges nearby lines more aggressively than the built-in line merger. This preprocessor solves line-recognition problems caused poor-quality PDF scans, handwritten text, and other PDF formatting. This preprocessor solves:

- oversplit lines
- lines overlapping on the x-axis
- "jittery" lines misaligned on the y-axis

 There are limitations to the combinations of parameter values you can set. For more information, see the Notes section.

[**Parameters**](doc:merge-lines#section-parameters)
[**Examples**](doc:merge-lines#section-examples)
[**Notes**](doc:merge-lines#section-notes)

Parameters
====

| key                                        | value                                  | description                                                  |
| ------------------------------------------ | -------------------------------------- | ------------------------------------------------------------ |
| `type` (**required**)                      | `mergeLines`                           |                                                              |
| `directlyAdjacentThreshold` (**required**) | number >= 0.16                         | Usually, it's recommended to leave the default for this parameter (0.16).<br/>Sensible uses the default setting for this parameter to transform separate tokens output from Google OCR into lines.<br/>This parameter specifies the fraction of line height under which two adjacent lines distributed along an x-axis are merged without a space.  For example, at 0.16, this preprocessor merges two lines separated by a small gap whose width is less than 16% of the line height. Choosing a larger number merges more aggressively. <br/> |
| `adjacentThreshold` (**required**)         | number >= 0.6                          | Corrects oversplit lines. <br/>Specifies the fraction of line height under which two adjacent lines distributed along an x-axis are merged *with* a space. The built-in merger uses 0.6, so choosing a larger number merges more aggressively.<br> For an example, see the Examples section. |
| `yOverlapThreshold`                        | number between 0 and 1.0. default: 1.0 | Merges lines that are not perfectly aligned at the same height on the page. <br/> Specifies the y overlap above which the Merge Lines preprocessor merges two adjacent lines. Y overlap is the portion of the joint y-axis range of two lines that is occupied by both lines. For example, if two lines share the same minimum and maximum y-axis values, their overlap is 1. If one line's extent is from 0 to 10 and the other line’s extent is from 2 to 12 on the y-axis, their overlap is .667 (8 / 12). <br/>For an example, see the Examples section. |
| `minXGapThreshold`                         | number in inches                       | Configure this parameter if two lines overlap on an x-axis. The default behavior is to merge these overlapping lines into one line. To split them instead, set a cap on the amount of allowable overlap. For example:<br/>0 - splits lines if their line boundaries are touching but not overlapping.<br/>0.1 - splits lines if their boundaries overlap just a little bit, up to 0.1 inches.<br/>2.0 - splits lines even when they overlap a lot, up to 2.0 inches.<br/>For an example, see the Examples section. |

Examples
====

Handwriting OCR 
----

Use the Merge Lines preprocessor to clean up text extracted from handwriting using OCR. This preprocessor is particularly useful for output from Google OCR, which by default groups text into words rather than lines.

In the following image, the Merge Line preprocessor cleans up placeholder handwritten data extracted using Google OCR:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/merge_lines_ocr_example.png)

Without the preprocessor, the lines are oversplit:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/merge_lines_ocr_example_2.png)

Modify this example to observe the effects of the different parameters. For example:

- set `"adjacentThreshold": 0.1` to see oversplit lines. 

- set `"adjacentThreshold": 2.0` to see very aggressively merged lines. 

- revert Adjacent Threshold to the original setting, then set `"yOverlapThreshold": 0.2`  to observe how text that is misaligned in terms of height (like the email address) merges more aggressively.

  

Try out this example in the Sensible app using the following PDF and config: 

| Example PDF for OCR Merge Lines | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/merge_lines_ocr_example.pdf) |
| ------------------------------- | ------------------------------------------------------------ |

To duplicate this example, click **Edit Settings**  for the Document Type and set Google OCR: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/merge_lines_ocr_example_1.png)

This example uses the following config:

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
      "id": "all_lines_in_doc",
      "method": {
        "id": "documentRange",
        "includeAnchor": true
      },
      "anchor": {
        "match": {
          "type": "first"
        }
      }
    }
  ]
}
```




Oversplit lines
----

The following image shows oversplit lines. For example, the phrase "premium driver discount" is split into three lines even though the human eye reads it as one phrase:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/merge_lines_example_oversplit_1.png)

The following image shows using the Merge Lines preprocessor to fix the oversplit lines and find a discount amount for a specific vehicle:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/merge_lines_example_oversplit_2.png)

This example uses the following config:

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
      "method": {
        "id": "row"
      },
      "anchor": {
        "match": {
          "type": "includes",
          "text": "premier driver"
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
Jittery lines on a y-axis
----

The following image shows using the Y Overlap parameter to ignore vertical misalignment or "jitter" in lines (for example, as the result of a low-quality scan or because of handwriting).

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/merge_lines_example_yoverlap.png)


Try out this example in the Sensible app using the following PDF and config:

| Example PDF for Y Overlap | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/merge_lines_yoverlap_example.pdf) |
| ------------------------- | ------------------------------------------------------------ |

This example uses the following config:

```json
{
  "preprocessors": [
    {
      "type": "mergeLines",
      "directlyAdjacentThreshold": 0.16,
      "adjacentThreshold": 1.3,
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
Overlapping lines on an x-axis
----

The following image shows using the Min X Gap Threshold parameter to correctly extract overlapping text in a poorly formatted PDF. In this example, the built-in behavior without a Min X Gap Threshold is to merge the overlapping lines into one line (`Supplementary underinsured/uninsured motorist coverage500,000 USD Combined single limit incl. umbl`). 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/merge_lines_minxgap_example.png)

The Min X Gap Threshold preserves the intended PDF formatting, which is a two-column table. By preserving this format, you can consistently use the Row method on this document, as well as in other instances of this document in which the lines do not overlap.

You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for Min X Gap Threshold | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/merge_lines_minxgap_example.pdf) |
| ----------------------------------- | ------------------------------------------------------------ |

This example uses the following config:

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

Notes
====
Because the Merge Lines preprocessor evaluates after the built-in line merger, there are limitations to the combinations of parameter values you can set:

**yOverlapThreshold** 

In general, when you set `"yOverlapThreshold"` to 1 or leave its value unspecified, then you set `"adjacentThreshold"` to 0.6 or higher.

In this situation,   `"directlyAdjacentThreshold"` and `"adjacentThreshold"` have no effect if both their values are less than 0.6. In other words, the following configuration has **no** effect:

```json
    {
      "type": "mergeLines",
      "directlyAdjacentThreshold": 0.5,
      "adjacentThreshold": 0.5,
     "yOverlapThreshold": 1,

    }

```

