---
title: Visual troubleshooting in the SenseML editor
excerpt: >-
  Learn how to trace extracted fields to their source text with color-coded
  overlays, and how to test and troubleshoot configs with the SenseML editor's
  options
deprecated: false
hidden: false
metadata:
  title: ''
  description: >-
    Learn how to trace extracted fields to their source text with color-coded
    overlays, and how to test and troubleshoot configs with the SenseML editor's
    options
  robots: index
next:
  description: ''
---
Sensible displays the source text for extracted fields using color-coded symbols overlaid on the rendered document in the SenseML editor. Use the editor's options to control which symbols display, and to test configs on reference documents.

# Source text traceability

The SenseML editor uses color-coded overlays to visually represent how SenseML queries operate on documents. Use these symbols to author queries, troubleshoot queries, and to trace extractions to their source text. To control which symbols display, see [Test and troubleshoot configs](doc:color#test-and-troubleshoot-configs).

| symbol                                                        | represents                                                                |
| ------------------------------------------------------------- | ------------------------------------------------------------------------- |
| [Yellow box](doc:color#yellow-box)                            | anchor                                                                    |
| [Blue box](doc:color#blue-box)                                | captured method data                                                      |
| [Green box](doc:color#green-box)                              | box, region, table, or chunk                                              |
| [Green point](doc:color#green-point)                          | starting point for extracting a box or region                             |
| [Green brackets or yellow brackets](doc:color#green-brackets) | ranges for sections                                                       |
| [Dotted blue box](doc:color#dotted-blue-box)                  | discarded method data                                                     |
| [Dotted yellow box](doc:color#dotted-yellow-box)              | discarded anchor data                                                     |
| [Pink box](doc:color#pink-box)                                | fingerprint                                                               |
| [Violet box](doc:color#violet-box)                            | section anchor                                                            |
| [Purple box](doc:color#purple-box)                            | location highlighting of source text for an extracted field; line details |

## Yellow box

**_Yellow boxes_** represent anchors. For more information about anchors, see [Anchors](doc:anchor).

For example, the following image shows:

* an anchor line highlighted with a yellow outline ("Here is a good candidate"). The outline shows the anchor's "bounding box", or the boundaries of the anchor line.
* a line output by the Label method outlined in blue ("And here's the text below")

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/ui_label_and_method_1.png)

The query used for the preceding image is:

```json
{
  "fields": [
    {
      "id": "simple_label",
      "anchor": "here is a good candidate",
      "method": {
        "id": "label",
        "position": "below"
      }
    }
  ]
}    
```

## Blue box

**_Blue boxes_** represent method output. For more information about method, see [Method object](doc:method).

For example, the following image shows:

* an anchor line outlined in yellow ("Here is a good candidate")
* a line output by the Label method outlined in blue ("And here's the text below")

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/ui_label_and_method_1.png)

The query used for the preceding image is:

```json
{
  "fields": [
    {
      "id": "simple_label",
      "anchor": "here is a good candidate",
      "method": {
        "id": "label",
        "position": "below"
      }
    }
  ]
}    
```

## Green box

**_Green boxes_** represent boxes, regions, tables, or [chunks](doc:prompt#full-prompt).

## Green point

**_Green points_** represent the following:

* a starting point for recognizing a box or checkbox

* a starting point for defining the coordinates of a region

Green points can be useful for troubleshooting. For example, in the following image, Sensible can't recognize the box. The green dot provides a visual clue about the problem: the green dot is _on_ the box border itself, as specified by (`"position": "left"`).

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/box_position_left.png)

If you specify to find the box borders by starting from the right edge of the anchor line's boundaries (`"position": "right"`), the green dot is far enough inside the borders for Sensible to recognize the box:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/box_position_right.png)

## Green brackets

**Green brackets** represent the start and end of each section in a section group:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/ui_sections.png)

Yellow brackets denote sections' external ranges, which is an advanced configuration option.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/sections_external_range_dynamic.png)

## Dotted blue box

**_Dotted blue boxes_** represent discarded method data. Sensible methods filter out captured data depending on parameters you set in the field, the anchor, and the method. Sensible hides discarded data by default. To display it, see [Show unextracted lines](doc:color#show-unextracted-lines).

For example, in the following image, a Row method captures everything to the right of the text "Python", but a tiebreaker selects "0" (dark blue box) and discards "first" (dotted blue box).

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/ui_filtered_method.png)

The query used for the preceding image is:

```json
{
  "fields": [
    {
      "id": "filtered_by_tiebreaker",
      "anchor": "javascript",
      "method": {
        "id": "row",
        "position": "right",
        "tiebreaker": "second"
      }
    }
  ]
}
```

Common parameters resulting in filtering include:

* the field's data type (currency, date, address, etc)
* the method's stop
* the method's tiebreaker

## Dotted yellow box

**_Dotted yellow boxes_** represent discarded anchor data, for example for queries that return null. Sensible hides discarded data by default. To display it, see [Show unextracted lines](doc:color#show-unextracted-lines).

For example, for the following config and example document:

```json
{
  "fields": [
    {
      "id": "anchors_candidates_filtered_by_method",
      "anchor": "python",
      "match": "first",
      "method": {
        "id": "label",
        "position": "right"
      }
    }
  ]
}
```

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/row_column.pdf) |
| ---------------- | ---------------------------------------------------------------------------------------------------------- |

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/ui_filtered_anchor.png)

Sensible discards the "python" string since it doesn't meet the Label method's proximity requirements.  In this instance, use the Row method instead to capture the data.

Common parameters resulting in discarded anchors include:

* the field's data type (currency, date, address, etc)
* the field's match method (first, last, all)
* the anchor's start and end
* the method's ID (for example, the Checkbox method filters out all anchor lines that aren't near a checkbox)

## Pink box

**_Pink boxes_** represent matching fingerprint tests.<br />In the following image, the pink text is a matching fingerprint.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/ui_fingerprint.png)

The query used for the preceding image is:

```json
fingerprint": {
    "tests": [
      {
        "page": "first",
        "match": [
          {
            "text": "anyco auto insurance",
            "type": "startsWith"
          }
        ]
      }
    ]
  
```

**Note** Sensible doesn't support fingerprint highlighting if you use preprocessors that change line indices, such as Split Lines and Merge Lines.

## Violet box

**_Violet boxes_** represent the line each section anchors on in a [sections](doc:sections) group. Sensible hides section anchors by default. To display them, see [Show section anchors](doc:color#show-section-anchors).

## Purple box

Purple boxes represet a selected line. To select a line:

* Click a line directly in the rendered document.

* (Location highlighting) In the visual output pane, click the location icon to the right of the output of a query field to jump to its source text in the rendered document.

* (Location highlighting) In the JSON output pane, click the gutter to the left of a field ID to jump to its source text in the rendered document.

A selected line shows the following details:

* underlying extracted text
* coordinates of the line's boundaries
* SenseML and extracted output that relies on that text

You can select multiple lines to see their combined details.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_July2021_x-ray_mode.png)

# Location highlighting

Sensible can highlight the location of the source text for an LLM's response. Note the following limitations for location highlighting for LLM-based methods:

* In general, since LLMs are indeterminate,Sensible selects source text for LLM-based methods using a variety of best-guess approaches:

  * For the Query group method, Sensible uses fuzzy matching, since the LLM's output can transform the source text. For example, if the LLM returns `4387-09-22-33`, Sensible matches the line `Policy Number: 4387-09-22-33` in the document.
  * For the NLP Table method, Sensible uses the top-scoring table sourced from an OCR provider. For more information, see the NLP Table method's [Notes](doc:nlp-table#notes).

* Sensible doesn't support location highlighting for the List method.

* For the Query Group method, Sensible can highlight the incorrect location under the following circumstances:

  * If the extracted data is in a different format from the source text (for example, you prompt the LLM to reformat the source text in the document or use a [type](doc:types)), then Sensible can fail to find a match or can find an inaccurate match.

  * If the document contains multiple candidates fuzzy matches (for example, two instances of `April 7`), Sensible chooses the top-scoring match. If candidates have similar scores, Sensible uses page location as a tie breaker and chooses the earliest match in the document.

  * If the LLM returns text that's not in the document, then location highlighting is inapplicable.

# Test and troubleshoot configs

Click the **Options** dropdown in the middle pane of the SenseML editor. The dropdown contains the following options:

* [Upload sample doc](doc:color#upload-sample-doc)
* [Download sample doc](doc:color#download-sample-doc)
* [Hide bounding boxes](doc:color#hide-bounding-boxes)
* [Show unextracted lines](doc:color#show-unextracted-lines)
* [Show section anchors](doc:color#show-section-anchors)
* [Validate fingerprints](doc:color#validate-fingerprints)

## Upload sample doc

Uploads a reference document to the config so that you can test the config's queries on it.

## Download sample doc

Downloads the reference document displayed in the editor.

## Hide bounding boxes

Hides all color-coded symbols and the gray boxes that represent each [line's](doc:lines) boundary box, so that you can read the rendered document without overlays. To display the symbols and boundary boxes again, select **Show bounding boxes**.

## Show unextracted lines

Displays data that Sensible captured and then discarded, as [dotted blue boxes](doc:color#dotted-blue-box) for method data and [dotted yellow boxes](doc:color#dotted-yellow-box) for anchor data. Use this option to troubleshoot fields that return null or unexpected output.

## Show section anchors

Highlights the line each section anchors on with a [violet box](doc:color#violet-box). Sensible hides section anchors by default, since for repeating sections, such as line items, they can obscure other symbols. Use this option to troubleshoot [sections](doc:sections) when parameters such as Offset Y shift each section's start away from its anchor line.

## Validate fingerprints

Tests a config's [fingerprint](doc:fingerprint) against multiple reference documents at once. Select **Validate fingerprints**, select reference documents, and click **Validate**. For each document, Sensible reports whether the fingerprint matches, partially matches, or doesn't match. You can expand each result to see which matches found text, how many lines they matched, and on which page. To check for false positives, select reference documents that belong to other configs. The validator tests fingerprints the way Sensible runs them for standalone documents, so it ignores the Page parameter in [portfolio](doc:portfolio) fingerprints.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/fingerprint_validation_1.png)
