---
title: "Text Table"
hidden: true
---


| key                  | value   | description                                                  |
| :------------------- | :------ | :----------------------------------------------------------- |
| id **required**      | `table` | When you specify this method, you must also specify `"type": "table"` in the field's parameters. |
| columns **required** | array   | An array of objects with the following parameters:<br/> -`id` (**required**): The id for the column in the extraction output. <br/>**To specify fallbacks, use the same ID for multiple columns. Succeeding columns act as fallbacks if the first returns null.** <br/> -`minX` (**required**):  The distance in inches on the page from the left edge of the page to the left edge of the column. To visually determine this coordinate, click a point in the document in the Sensible app, then drag to display inch dimensions.  <br/>  -`maxX` (**required**):  The distance in inches on the page from the left edge of the page to the right edge of the column. To visually determine this coordinate, click a point in the document in the Sensible app, then drag to display inch dimensions. <br/>  -`type`: The table cell's type. For more information about types, see [Types](doc:types). <br/>   -`isRequired` (default false):  If true, Sensible omits a row if its cell is empty in this column. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for *all* columns, even if the row had content under other columns.<br/><br/>**Tip:** You can define columns with overlapping coordinates, for example in order to output data in a single column as multiple columns. For more information, see the Examples section. |
|                      |         |                                                              |
|                      |         |                                                              |
|                      |         |                                                              |
|                      |         |                                                              |
|                      |         |                                                              |

You can output the issuing financial institution and the displayed account number as separate columns, with a configuration like the following configuration.

Notes
====

- To extract complex tables, for example tables inside tables or tables with labeled rows and columns, see [Sections](doc:sections#examples).





  

  

  

  







