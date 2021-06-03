---
title: "Checkbox"
hidden: false
---
Looks for a checkbox next to the anchor and returns a boolean indicating if the checkbox contains a checkmark or not.  This method works by default with boxes that have a light background and dark, continuous borders.  

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method-object#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| key               | values                                  | description                                                  |
| ----------------- | --------------------------------------- | ------------------------------------------------------------ |
| id (**required**) | `checkbox`                              |                                                              |
| position          | `left`, `right`                         | The starting position from which Sensible expands outward to recognize a checkbox. <br/>  `left`  specifies a starting point at the midpoint of the left boundary of the anchor line. SenseML then searches to the left along a horizontal line drawn through the starting point. <br/> `right`  specifies a starting point at the midpoint of the right boundary of the anchor line. SenseML then searches to the right along a horizontal line drawn through the starting point.<br/> SenseML continues searching until it finds a dark pixel signifying the checkbox border. It then crosses the border and finds the outline of the checkbox. |
| offsetX           | number (decimals allowed). default: 0   | The offset in inches along the X axis, from the starting point defined by the Position parameter, from which to expand out and recognize a checkbox. When you define both offsetX and offsetY, Sensible expands out directly from the point specified to find the checkbox borders, rather than search in a line for a border. |
| offsetY           | number (decimals allowed).   default: 0 | The offset in inches along the Y axis, from the starting point  defined by  the Position parameter, from which to expand out and recognize a checkbox. When you define both offsetX and offsetY, Sensible expands out directly from the point specified to find the checkbox borders, rather than search in a line for a border. |
| darknessThreshold | number between 1 and 0. default 0.9     | The brightness threshold below which to consider a pixel a box boundary (white is 1.0). Configure this parameter when you have a checkbox with a dark background. |
