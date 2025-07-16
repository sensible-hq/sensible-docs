---
title: "Text table"
hidden: true
---


| key                       | value                                      | description                                                  |
| :------------------------ | :----------------------------------------- | :----------------------------------------------------------- |
| id **required**           | `table`                                    | When you specify this method, you must also specify `"type": "table"` in the field's parameters. |
| columns **required**      | array                                      | An array of objects with the following parameters:<br/> -`id` (**required**): The id for the column in the extraction output. <br/>**To specify fallbacks, use the same ID for multiple columns. Succeeding columns act as fallbacks if the first returns null.** <br/> |
| detectMultipleLinesPerRow | boolean, or<br/>object<br/> default: false | If true, Sensible detects table cells containing multiple lines, rather than the default of treating each line as a new row. By default, Sensible detects that a cell contains multiple lines if the vertical gap between two lines is less than half the height of the second line.<br/>Set this to false if row gutters are narrow. For example, if vertical gaps between lines in the cells are the same height as row gutters, Sensible can incorrectly merge multiple rows into one.<br/>To configure the vertical gap, you can set `"detectMultipleLinesPerRow": maxGap: /* fraction_of_inches */ `. If configured, Sensible considers multiple lines to belong to the same cell if the vertical gap is less than or equal to the specified number in inches. |
|                           |                                            |                                                              |
|                           |                                            |                                                              |
|                           |                                            |                                                              |
|                           |                                            |                                                              |





  

  

  

  







