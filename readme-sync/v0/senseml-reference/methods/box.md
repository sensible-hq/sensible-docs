---
title: "Box"
hidden: false
---
Use the box method to grab lines inside a box. This method works by default with boxes that have a light background and dark, continuous borders.  

Examples
---

**Simple box**

The following image shows a config that grabs a dollar amount from a box in a 1099 form, based on anchor text matching in the box:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/box_1099.png)

The config for the preceding example is:

 ```json
{
  "fields": [
    {
      "id": "rents_income",
      "type": "currency",
      "method": {
        "id": "box",
        "position": "below"
      },
      "anchor": "rents"
    }
  ]
}
 ```



**Dark box**

The following image shows extracting text from a box with a dark background and light text using the `darknessThreshold` parameter:



![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/box_dark.png)

The config for the preceding example is:

```json
{
  "fields": [
    {
      "id": "dark_box",
      "method": {
        "id": "box",
        "position": "below",
        "darknessThreshold": 0.8
      },
      "anchor": "dark box with light text",
    }
  ]

```

**Offset box**

The following image shows extracting text from boxes using the `boxOffset` parameter. 

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/box_offset.png)

The config for the preceding example is:

```json
{
  "fields": [
    {
      "id": "offset_boxes_test_2",
      "anchor": "auto only",
      "method": {
        "id": "box",
        "position": "right",
        "offsetBoxes": {
          "direction": "right",
          "number": 1
        }
      }
    },
    {
      "id": "offset_boxes_test",
      "anchor": "dollar amount",
      "method": {
        "id": "box",
        "position": "right",
        "offsetBoxes": {
          "direction": "below",
          "number": 2
        }
      }
    },
  ]
}
```



Parameters
----

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method-object#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| key               | value                           | description                                                  |
| ----------------- | ------------------------------- | ------------------------------------------------------------ |
| id (**required**) | `box`                           |                                                              |
| position | `right`, `left`, `below`, `above` | A `Direction` specifying where to start relative to the anchor line. `right` starts at the middle of the right edge, `below` starts at the middle of the bottom edge, and so forth. |
| offsetX        | number. default: 0              | The offset in inches along the X axis, from the starting point defined by `position` . |
| offsetY           | number. default: 0              | The offset in inches along the Y axis, from the starting point  defined by `position`. |
| offsetBoxes       | object. default: `none`         | The offset, in boxes, from the anchoring box. For example, use this parameter for tables or grids formatted such that continuous borders surround every cell. This parameter does not work for boxes separated from each other by whitespaces. In other words, the boxes must share borders.  Has these parameters:<br/>\- `direction`: The `Direction` to search in, relative to the starting box.<br/>\- `number`: The number of boxes to offset by.<br/> |
| darknessThreshold | a number between 0 and 1. default: 0.9 | The brightness threshold below which to consider a pixel a box boundary (white is 1.0). Configure this when you have a box with a dark background. |

Notes
----

The box method is similar to the [Region method](doc:region), but requires less configuration and is slightly slower. Use the Region method instead of the Box method if the borders of the box are compromised in some way (incomplete, discontinuous, or otherwise broken, for example). 