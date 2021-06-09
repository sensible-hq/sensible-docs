---
title: "Merge lines"
hidden: false
---


Merges nearby lines more aggressively than the built-in line merger. Use this preprocessor when the PDF contains oversplit lines, lines overlapping on the x-axis, or "jittery" lines misaligned on the y-axis. This preprocessor does not override the built-in line merge, but instead evaluates after it. This means you can configure the Merge Lines preprocessor to be aggressive than the built-in line merger, but not less aggressive.

Parameters
----

| key                                        | value                                  | description                                                  |
| ------------------------------------------ | -------------------------------------- | ------------------------------------------------------------ |
| `type` (**required**)                      | string                                 | "mergeLines"                                                 |
| `directlyAdjacentThreshold` (**required**) | number >= 0.16                         | Fraction of line height under which two adjacent lines (i.e., horizontally distributed along an x-axis) are merged without a space.  For example, at 0.16 two lines are merged without a space in between their contents when they are less than 16% of the line height apart from one another. The built-in merger uses 0.16, so choosing a larger number merges more aggressively. <br/>Under the hood, Sensible uses the default setting for this parameter to transform separate tokens output from OCR into lines. It's relatively uncommon to need to adjust the default value for this parameter. |
| `adjacentThreshold` (**required**)         | number >= 0.6                          | Fraction of line height under which two adjacent lines (i.e., horizontally distributed along an x-axis) are merged with a space. The built-in merger uses 0.6, so choosing a larger number merges more aggressively.<br> Use this parameter to correct oversplit lines. For an example, see the Examples section. |
| `yOverlapThreshold`                        | number between 0 and 1.0. default: 1.0 | Configure this parameter if lines are not perfectly aligned at the same height on the page. The Y Overlap Threshold is the y overlap above which the Merge Lines preprocessor merges two adjacent lines. Y overlap is the portion of the joint y-axis range of two lines that is occupied by both lines. For example, if two lines share the same minimum and maximum y-axis values, they will have an overlap of 1. If one line's extent is from 0 to 10 and the other line’s extent is from 2 to 12 on the y-axis, they will have an overlap of .667 (8 / 12).   For an example, see the Examples section. |
| `minXGapThreshold`                         | number in inches                       | Configure this parameter if two lines overlap on an x-axis. The default behavior is to merge these overlapping lines into two lines. If you want to split them instead, set a cap on the amount of overlap you want to allow. For example<br/>0 means to split lines if there is no gap between them and their line boundaries are touching but not overlapping.<br/>0.1 means to split the lines if their boundaries overlap just a little bit, up to 0.1 inches<br/>2.0 means to split the lines including when they overlap a lot, up to 2.0 inches.<br/>For an example, see the Examples section. |

Examples
====

Oversplit lines
----

The following image shows a PDF that has oversplit lines. For example, the phrase "premium driver discount" is split into three lines even though to the human eye it reads as one line:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/merge_lines_example_oversplit_1.png)

The following image shows using the Merge Lines preprocessor to fix the oversplit lines and find a discount amount for a specific vehicle:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/merge_lines_example_oversplit_2.png)

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

The following image shows using the Y Overlap parameter to ignore "jitter" on the y-axis, where two lines that should be perfectly aligned are not  (for example, as the result of a low-quality scan or because of handwriting).

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/merge_lines_example_yoverlap.png)


You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

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

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/merge_lines_minxgap_example.png)

But since the overlapping lines are part of a two-column table, it's better to split them into  two lines using the Min X Gap Threshold parameter. That way, you can use the Row method on the lines, as in the preceding image.

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
