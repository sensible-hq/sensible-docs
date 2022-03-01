---
title: "DRAFT Text Table"
hidden: true
---
Matches tables based on coordinates in inches and returns their collated column contents.  Anchor on the table title, or use a negative Offset Y parameter to enable anchoring on a column heading.

Use this method when other Table methods can't recognize a table. This method's advantage is that it's faster than other Table methods because it doesn't use table recognition. Its disadvantage is that it's more limited than other table methods, because it relies on line alignment in the table. For an example, see the [Examples section](doc:text-table#examples).

[**Parameters**](doc:text-table#parameters)
[**Examples**](doc:text-table#examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                         | value                                                      | description                                                  |
| :-------------------------- | :--------------------------------------------------------- | :----------------------------------------------------------- |
| columnsRelativeToAnchor     | boolean. Default: false                                    | If true, specifies that the column coordinates `minX` and `maxX` are relative to the left edge of the anchor line, rather than to the left edge of the page. For example, use this parameter to recognize nested tables inside tables. See TODO link to vertical nested tables. |
| *id **required***           | *`table`*                                                  | *When you specify this method, you must also specify `"type": "table"` in the field's parameters.* |
| *columns **required***      | *array*                                                    | *An array of objects with the following parameters:<br/> -`id` (**required**): The id for the column in the extraction output.<br/> -`minX` (**required**):  The distance in inches on the page from the left edge of the page to the left edge of the column. To determine this coordinate, open the PDF in a viewer, such as Preview or Gimp, that displays cursor coordinates.  <br/>  -`maxX` (**required**):  The distance in inches on the page from the left edge of the page to the right edge of the column. To determine this coordinate, open the PDF in a viewer, such as Preview or Gimp, that displays cursor coordinates <br/>  -`type`: The table cell's type. For more information about types, see [Field query object](doc:field-query-object).<br/>   -`isRequired` (default false):  If true, Sensible omits a row if its cell is empty in this column. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for all columns, even if the row had content under other columns.* |
| *offsetY*                   | *number in inches.*                                        | *Defines a starting point for recognizing a table, offset vertically from the anchor line's lower boundary. <br/>For example, if no table title precedes the table, then anchor instead on a column heading and use a negative Offset Y parameter to define a starting point above the table.* |
| *stop*                      | *Match object, array of Match objects, or number (inches)* | *(**Recommended**) Line to match or number in inches to stop table recognition.  Specify this parameter to prevent false positive results and to enable recognizing a table that spans pages.<br/>  A Match object or array specifies to stop table recognition when Sensible matches text.<br/> A number specifies the end of the table as the number of the inches offset along a Y-axis from the start of the table.* |
| *startOnRow*                | *integer. default: 0*                                      | *Zero-indexed row number at which to start table extraction. For example, use this to exclude column headings from the output. As a stricter alternative, set the Is Required parameter on a column and set a type on the column (see example in Examples section).* |
| *detectMultipleLinesPerRow* | *boolean. default: false*                                  | *If true, Sensible detects table cells containing multiple lines, rather than the default of treating each line as a new row.<br/>Set this to false if row gutters are narrow. For example, if vertical gaps between lines in the cells are the same height as row gutters, Sensible can incorrectly merge multiple rows into one. In detail, Sensible detects a cell with multiple lines if the vertical gap between two lines is less than half the height of the second line. Sensible adjusts the row height to accommodate the tallest cell.* |











