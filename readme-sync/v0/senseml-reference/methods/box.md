---
title: "Box"
hidden: false
---
Use the box method to grab lines inside a box. This method works best with boxes that have a light background and dark, continuous borders. 

**Example**

The following config grabs a dollar amount from a box based on text matching in the box:

 ```json
{
  "fields": [
    {
      "id": "rents",
      "type": "currency",
      "method": {
        "id": "box",
        "position": "below"
      },
      "anchor": {
        "match": "rents"
      }
    },
  ]
}
 ```

The following image shows this example in the Sensible app:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/box_1099.png)





**Components**

| key               | value                           | description                                                  |
| ----------------- | ------------------------------- | ------------------------------------------------------------ |
| id (**required**) | box                             |                                                              |
| offsetX        | number                          | The offset in inches along the X axis, from the starting point defined by `position` . Default: 0 |
| offsetY           | number                          | The offset in inches along the Y axis, from the starting point  defined by `position`. Default: 0 |
| offsetBoxes       | object                          | An object with the keys:<br/>\- `direction`: The `Direction` to search in relative to the starting box<br/>\- `number`: The number of boxes to offset by<br/> Default: none |
| position          | `right`, `left`, `below`, `above` | A `Direction` specifying where to start relative to the anchor point. `right` starts at the middle of the right edge, `below` starts at the middle of the bottom edge, and so forth |
| darknessThreshold | a number between 0 and 1        | The brightness threshold below which to consider a pixel a box boundary (white is 1.0). Configure this when you have a box with a dark background. Default: 0.9 |