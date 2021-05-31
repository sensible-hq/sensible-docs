---
title: "Checkbox"
hidden: false
---
Looks for a checkbox next to the anchor and returns a boolean indicating if the checkbox contained a checkmark or not.  This method works by default with boxes that have a light background and dark, continuous borders.  

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method-object#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| key               | values                                  | description                                                  |
| ----------------- | --------------------------------------- | ------------------------------------------------------------ |
| id (**required**) | `checkbox`                              |                                                              |
| position          | `left`, `right`                         | The starting position from which Sensible expands outward to recognize a checkbox. <br/> In detail, the Position parameter defines a little cluster of pixels relative to the anchor line, from which to expand outward until dark pixels signifying the checkbox border are found.<br/> |
| offsetX           | number (decimals allowed). default: 0   | The offset in inches along the X axis, from the starting point defined by the Position parameter, from which to expand out and recognize a checkbox. |
| offsetY           | number (decimals allowed).   default: 0 | The offset in inches along the Y axis, from the starting point  defined by  the Position parameter, from which to expand out and recognize a checkbox. |
| darknessThreshold | number between 1 and 0. default 0.9     | The brightness threshold below which to consider a pixel a box boundary (white is 1.0). Configure this parameter when you have a checkbox with a dark background. |

