---
title: "Box"
hidden: false
---
Use the box method to grab lines inside a box. This method works by default with boxes that have a light background and dark, continuous borders.  

Parameters
----

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method-object#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| key               | value                                                        | description                                                  |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**) | `box`                                                        |                                                              |
| position          | `right`, `left`, `below`, `above`. default: center of the anchor line's bounding box | Unlike the Position parameter for the Label method, this parameter *doesn't* specify where to find the data to grab relative to the anchor. Instead, it helps you fine tune how to recognize the box that surrounds the data you want to grab.  The Position parameter defines a little cluster of pixels relative to the anchor line, from which to expand outward until dark pixels signifying the box border are found.  A reason you might have for overriding the default position is if you're unlucky enough that the starting position for box recognition happens to be inside a letter with a continuous border like "O" or "D" such that SenseML interprets the *letter*  as a box and looks no further. <br/></br>  `right` starts at the middle of the right edge, `below` starts at the middle of the bottom edge, and so forth.  When you define a position, visually make sure in the Sensible app that there's ample whitespace between the position dot and the box's border. </br> For an example of how to use this parameter, see the following section. |
| offsetX           | number. default: 0                                           | The offset in inches along the X axis, from the starting point defined by `position` . TODO: elaborate. |
| offsetY           | number. default: 0                                           | The offset in inches along the Y axis, from the starting point  defined by `position`. |
| offsetBoxes       | object. default: `none`                                      | The offset, in boxes, from the anchoring box. For example, use this parameter for tables or grids formatted such that continuous borders surround every cell. This parameter does not work for isolated boxes that are separated from each other by whitespaces. In other words, the boxes must share borders.  Has these parameters:<br/>\- `direction`: The `Direction` to search in, relative to the starting box.<br/>\- `number`: The number of boxes to offset by.<br/>For an example of how to use this parameter, see the following section. |
| darknessThreshold | a number between 0 and 1. default: 0.9                       | The brightness threshold below which to consider a pixel a box boundary (white is 1.0). Configure this when you have a box with a dark background. For an example of how to use this parameter, see the following section. |

Examples
---

**Simple box**

The following image shows a config that grabs a dollar amount from a box in a 1099 form, based on anchor text matching in the box: TODO: remove position

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
      "id": "auto_limit_in_policy_1",
      "anchor": "auto only",
      "match": "first",
      "method": {
        "id": "box",
        "offsetBoxes": {
          "direction": "right",
          "number": 1
        }
      }
    },
    {
      "id": "injury_limit_in_policy_2",
      "anchor": "dollar amount",
      "match": "last",
      "method": {
        "id": "box",
        "offsetBoxes": {
          "direction": "below",
          "number": 2
        }
      }
    },
    {
      "id": "oddly_formatted_boxes",
      "anchor": "spanning multiple",
      "method": {
        "id": "box",
        "offsetBoxes": {
          "direction": "below",
          "number": 3
        }
      }
    },
  ]
}
```





TODO: left off with offsetY and offsetX

**Troubleshooting box recognition**

Use the Position parameter to finetune box recognition.

For example, in the following image, the config specifies to find the box by expanding outward from the left edge of the anchor line's bounding box  (`"position": "left"`) until SenseML finds dark borders. But the starting position (the green dot) is right on the box border itself, so SenseML can't find the box:

 ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/box_position_left.png)

However, if you ask SenseML to find the box borders by starting from the right edge of the anchor line's bounding box (`"position": "right"`), there's enough whitespace between the anchor and the box border for SenseML to find the box:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/box_position_right.png)

The oddly formatted boxes in this example illustrate how SenseML finds offset boxes after the first box:



![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/box_position_callouts.png)

1. Find the borders of the first box, expanding out from the starting position (in this case, the starting position is the default. The starting position is the green dot in the image). The expansion is in all directions, not just the cardinal directions shown  by the red arrows in the image.

2. Find the border that is shared with the second box, in the direction specified (below, in this case). Pick the middle of that border in term's of the first box's dimensions.

3. offset just a little from the shared border to get into the second box's whitespace, then expand out from that position (shown as a green dot in the image) to define the second box's borders.

4. repeat steps 2 and 3 for the third box, and so on.

Note that when boxes are inconsistently sized and aligned, as in the preceding image,  SenseML's determination of what constitutes a "box" and where the "middle" of the shared border is may be complex.  In such cases, examine the visual representation of the box and its starting position the Sensible app to understand SenseML's behavior, and keep in mind that another method might be a better fit for such a complex scenario.









Notes
----

The box method is similar to the [Region method](doc:region), but requires less configuration and is slightly slower. Use the Region method instead of the Box method if the borders of the box are compromised in some way (incomplete, discontinuous, or otherwise broken, for example). 