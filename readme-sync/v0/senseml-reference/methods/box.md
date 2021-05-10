---
title: "Box"
hidden: false
---
Use the box method to grab lines inside a box. This method works best with boxes that have a light background and dark, continuous borders.  

Examples
---


The following config grabs a dollar amount from a box based on text matching in the box:

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

The following image shows this example in the Sensible app:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/box_1099.png)





Parameters
----

| key               | value                           | description                                                  |
| ----------------- | ------------------------------- | ------------------------------------------------------------ |
| id (**required**) | `box`                           |                                                              |
| offsetX        | number. Default: 0              | The offset in inches along the X axis, from the starting point defined by `position` . |
| offsetY           | number. Default: 0              | The offset in inches along the Y axis, from the starting point  defined by `position`. |
| offsetBoxes       | object. Default: none           | An object with the keys:<br/>\- `direction`: The `Direction` to search in relative to the starting box<br/>\- `number`: The number of boxes to offset by<br/> |
| position          | `right`, `left`, `below`, `above` | A `Direction` specifying where to start relative to the anchor point. `right` starts at the middle of the right edge, `below` starts at the middle of the bottom edge, and so forth |
| darknessThreshold | a number between 0 and 1. Default: 0.9 | The brightness threshold below which to consider a pixel a box boundary (white is 1.0). Configure this when you have a box with a dark background. |

Notes
----

The box method is similar to the [Region method](doc:region), but requires less configuration and is slightly slower. Use the Region method instead of the Box method if the borders of the box are compromised in some way (incomplete, discontinuous, or otherwise broken, for example). 