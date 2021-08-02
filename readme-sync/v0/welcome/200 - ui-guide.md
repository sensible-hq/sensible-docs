---
title: "UI guide"
hidden: false
---

This topic describes the color-coded symbols in the Sensible app that visually represent how SenseML queries operate on PDFs.  Use these symbols to to author and troubleshoot queries.

Anchors and matches
====

***Yellow boxes*** represent anchors. For more information about anchors, see [Anchors](doc:anchor).

***Blue boxes*** represent matches. For more information about matches, see [Match object](doc:match).

For example, the following image shows:

- an anchor line outlined in yellow ("Here is a good candidate..")
- a matched line outlined in blue ("And here's the text below..")

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/ui_label_and_method_1.png)

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

Points and boxes
====

***Green points*** represent the following:

-  a starting point for recognizing a box or checkbox

- a starting point for defining the coordinates of a region

***Green boxes*** represent boxes or regions. 

Green points can be useful for troubleshooting. For example, in the following image, Sensible can't recognize the box. The green dot provides a visual clue about the problem: the green dot is right on the box border itself.

 ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/box_position_left.png)

If you specify to find the box borders by starting from the right edge of the anchor line's boundaries (`"position": "right"`), the green dot is far enough away from the box borders for Sensible to recognize the box:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/box_position_right.png)



Line details
====

If you hover on a line (text surrounded by a gray box), it changes to a ***purple box*** if it has details to display.  Click on the line to show:

- underlying extracted text
- coordinates of the line's boundaries
- SenseML and extracted output that relies on that text



![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/changelog_July2021_x-ray_mode.png)



Discarded anchor data
===

***Light yellow boxes*** represent discarded anchor data. Sensible anchors filter out captured text depending on parameters you set in the field, the anchor, and the method. 

For example, in the following image, there are two filtered out "python" strings surrounded by light yellow boxes. They are filtered out because they do not meet the Label method's proximity requirements:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/ui_filtered_anchor.png)

The query used for the preceding image is:

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

Common parameters resulting in filtering include:

-  the field's data type (currency, date, address, etc)
-  the field's match method (first, last, all)
-  the anchor's start and end
-  the method's id (for example, a Label method filters out all lines that are not closely proximate to other lines)



Discarded method data
===

***Light blue boxes*** represent discarded method data.  Sensible methods filter out captured data depending on parameters you set in the field, the anchor, and the method.

For example, in the following image, a Row method captures everything to the right of the text "Python", but a tiebreaker selects "0" (dark blue box) and discards "first" (light blue box).

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/ui_filtered_method.png)

The query used for the preceding image is:

```json
{
  "fields": [
    {
      "id": "filtered_by_tiebreaker",
      "anchor": "Javascript",
      "match": "last",
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



