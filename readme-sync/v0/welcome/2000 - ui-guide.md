---
title: "UI guide"
hidden: false
---

This topic describes the color-coded symbols in the Sensible app that visually represent how SenseML queries operate on PDFs. Use these symbols to author and troubleshoot queries.

| Symbol                                            | Represents                           |
| ------------------------------------------------- | ------------------------------------ |
| [Yellow box](doc:ui-guide#yellow-box)             | anchor                               |
| [Blue box](doc:ui-guide#blue-box)                 | captured method data                 |
| [Green box](doc:ui-guide#green-box)               | box or region                        |
| [Green point](doc:ui-guide#green-point)           | starting point for recognizing a box |
| [Light box](doc:ui-guide#light-blue-box)          | discarded method data                |
| [Light yellow box](doc:ui-guide#light-yellow-box) | discarded anchor data                |
| [Purple box](doc:ui-guide#purple-box)             | line details                         |

Yellow box
====

***Yellow boxes*** represent anchors. For more information about anchors, see [Anchors](doc:anchor).

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

Blue box
====

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

Green box
====

***Green boxes*** represent boxes or regions.

Green point
====

***Green points*** represent the following:

-  a starting point for recognizing a box or checkbox

- a starting point for defining the coordinates of a region

Green points can be useful for troubleshooting. For example, in the following image, Sensible can't recognize the box. The green dot provides a visual clue about the problem: the green dot is *on* the box border itself, as specified by (`"position": "left"`).

 ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/box_position_left.png)

If you specify to find the box borders by starting from the right edge of the anchor line's boundaries (`"position": "right"`), the green dot is far enough inside the borders for Sensible to recognize the box:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/box_position_right.png)



Light blue box
===

***Light blue boxes*** represent discarded method data. Sensible methods filter out captured data depending on parameters you set in the field, the anchor, and the method.

For example, in the following image, a Row method captures everything to the right of the text "Python", but a tiebreaker selects "0" (dark blue box) and discards "first" (light blue box).

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/ui_filtered_method.png)

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



Light yellow box
===

***Light yellow boxes*** represent discarded anchor data, for example for queries that return null. 

In the following image, there are two filtered out "python" strings surrounded by light yellow boxes. Sensible filters out the strings because they don't meet the Label method's proximity requirements:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/ui_filtered_anchor.png)

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
-  the method's id (for example, a Label method filters out all lines that aren't closely proximate to other lines)





Purple box
====

If you hover on a line (text surrounded by a gray box), it changes to a ***purple box*** if it has details to display. Click on the line to show:

- underlying extracted text
- coordinates of the line's boundaries
- SenseML and extracted output that relies on that text



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/changelog_July2021_x-ray_mode.png)

