---
title: "Source text traceability"
hidden: false
---

Sensible displays the source text for extracted fields using color-coded symbols overlaid on the rendered document in the JSON editor

# Color coding

The JSON editor uses color-coded overlays to visually represent how SenseML queries operate on documents. Use these symbols to author queries, troubleshoot queries, and to trace extractions to their source text.

| symbol                                                       | represents                                    |
| ------------------------------------------------------------ | --------------------------------------------- |
| [Yellow box](doc:color#yellow-box)                           | anchor                                        |
| [Blue box](doc:color#blue-box)                               | captured method data                          |
| [Green box](doc:color#green-box)                             | box, region, table, or chunk                  |
| [Green point](doc:color#green-point)                         | starting point for extracting a box or region |
| [Green brackets or yellow brackets](doc:color#green-brackets) | ranges for sections                           |
| [Dotted blue box](doc:color#dotted-blue-box)                 | discarded method data                         |
| [Dotted yellow box](doc:color#dotted-yellow-box)             | discarded anchor data                         |
| [Pink box](doc:color#pink-box)                               | fingerprint                                   |
| [Purple box](doc:color#purple-box)                           | location highlighting of source text for an extracted field; line details                                  |

## Yellow box

***Yellow boxes*** represent anchors. For more information about anchors, see [Anchors](doc:anchor).

For example, the following image shows:

- an anchor line highlighted with a yellow outline ("Here is a good candidate"). The outline shows the anchor's "bounding box", or the boundaries of the anchor line.
- a line output by the Label method outlined in blue ("And here's the text below")

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/ui_label_and_method_1.png)

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

***Blue boxes*** represent method output. For more information about method, see [Method object](doc:method). 

For example, the following image shows:

- an anchor line outlined in yellow ("Here is a good candidate")
- a line output by the Label method outlined in blue ("And here's the text below")

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/ui_label_and_method_1.png)

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

***Green boxes*** represent boxes, regions, tables, or [chunks](doc:prompt#full-prompt).

## Green point

***Green points*** represent the following:

-  a starting point for recognizing a box or checkbox

- a starting point for defining the coordinates of a region

Green points can be useful for troubleshooting. For example, in the following image, Sensible can't recognize the box. The green dot provides a visual clue about the problem: the green dot is *on* the box border itself, as specified by (`"position": "left"`).

 ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/box_position_left.png)

If you specify to find the box borders by starting from the right edge of the anchor line's boundaries (`"position": "right"`), the green dot is far enough inside the borders for Sensible to recognize the box:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/box_position_right.png)


## Green brackets

**Green brackets** represent the start and end of each section in a section group:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/ui_sections.png)

Yellow brackets denote sections' external ranges, which is an advanced configuration option.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_external_range_dynamic.png)



## Dotted blue box


***Dotted blue boxes*** represent discarded method data. Sensible methods filter out captured data depending on parameters you set in the field, the anchor, and the method.

For example, in the following image, a Row method captures everything to the right of the text "Python", but a tiebreaker selects "0" (dark blue box) and discards "first" (dotted blue box).


![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/ui_filtered_method.png)

The query used for the preceding image is:

```json
{
  "fields": [
    {
      "id": "filtered_by_tiebreaker",
      "anchor": "Javascript",
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

- the field's data type (currency, date, address, etc)
- the method's stop
- the method's tiebreaker



## Dotted yellow box

***Dotted yellow boxes*** represent discarded anchor data, for example for queries that return null. 

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

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/row_column.pdf) |
| ---------------- | ------------------------------------------------------------ |

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/ui_filtered_anchor.png)



Sensible discards the "python" string since it doesn't meet the Label method's proximity requirements.  In this instance, use the Row method instead to capture the data.

Common parameters resulting in discarded anchors include:

-  the field's data type (currency, date, address, etc)
-  the field's match method (first, last, all)
-  the anchor's start and end
-  the method's ID (for example, the Checkbox method filters out all anchor lines that aren't near a checkbox) 



## Pink box

***Pink boxes*** represent matching fingerprint tests.  
In the following image, the pink text is a matching fingerprint. 


![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/ui_fingerprint.png)

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

## Purple box


Purple boxes represet a selected line. To select a line:

- Click a line directly in the rendered document.

- (Location highlighting) In the visual output pane, click the location icon to the right of the output of a query field to jump to its source text in the rendered document.

- (Location highlighting) In the JSON output pane, click the gutter to the left of a field ID to jump to its source text in the rendered document.


A selected line shows the following details:

- underlying extracted text
- coordinates of the line's boundaries
- SenseML and extracted output that relies on that text

You can select multiple lines to see their combined details.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/changelog_July2021_x-ray_mode.png)


### Location highlighting

Note the following limitations for location highlighting for LLM-based methods: 

- In general, since LLMs are indeterminate,Sensible selects source text for LLM-based methods using a variety of best-guess approaches:

  - For the Query group method, Sensible uses fuzzy matching, since the LLM's output can transform the source text. For example, if the LLM returns `4387-09-22-33`, Sensible matches the line `Policy Number: 4387-09-22-33` in the document.
  - For the NLP Table method, Sensible uses the top-scoring table sourced from an OCR provider. For more information, see the NLP Table method's [Notes](doc:nlp-table#notes).

- Sensible doesn't support location highlighting for the List method.

- For the Query Group method, Sensible can highlight the incorrect location under the following circumstances:

  - If the extracted data is in a different format from the source text (for example, you prompt the LLM to reformat the source text in the document or use a [type](doc:types)), then Sensible can fail to find a match or can find an inaccurate match.

  - If the document contains multiple candidates fuzzy matches (for example, two instances of `April 7`), Sensible chooses the top-scoring match. If candidates have similar scores, Sensible uses page location as a tie breaker and chooses the earliest match in the document.

  - If the LLM returns text that's not in the document, then location highlighting is inapplicable.

