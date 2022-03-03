---
title: "Text Table"
hidden: false
---
Matches tables based on coordinates in inches and returns their collated column contents.  Anchor on the table title, or use a negative Offset Y parameter to enable anchoring on a column heading.

This method's advantages are:

- It's faster than other Table methods because it doesn't use table recognition.
- It can extract unusally formatted tables that other Table methods can't recognize.

Its disadvantage is that it's more limited than other table methods, because it relies on line alignment to find the table. For an example, see the [Examples section](doc:text-table#examples).

[**Parameters**](doc:text-table#parameters)
[**Examples**](doc:text-table#examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                       | value                                                    | description                                                  |
| :------------------------ | :------------------------------------------------------- | :----------------------------------------------------------- |
| id **required**           | `table`                                                  | When you specify this method, you must also specify `"type": "table"` in the field's parameters. |
| columns **required**      | array                                                    | An array of objects with the following parameters:<br/> -`id` (**required**): The id for the column in the extraction output.<br/> -`minX` (**required**):  The distance in inches on the page from the left edge of the page to the left edge of the column. To determine this coordinate, open the PDF in a viewer, such as Preview or Gimp, that displays cursor coordinates.  <br/>  -`maxX` (**required**):  The distance in inches on the page from the left edge of the page to the right edge of the column. To determine this coordinate, open the PDF in a viewer, such as Preview or Gimp, that displays cursor coordinates <br/>  -`type`: The table cell's type. For more information about types, see [Field query object](doc:field-query-object).<br/>   -`isRequired` (default false):  If true, Sensible omits a row if its cell is empty in this column. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for *all* columns, even if the row had content under other columns. |
| offsetY                   | number in inches.                                        | Defines a starting point for recognizing a table, offset vertically from the anchor line's lower boundary. <br/>For example, if no table title precedes the table, then anchor instead on a column heading and use a negative Offset Y parameter to define a starting point above the table. |
| stop                      | Match object, array of Match objects, or number (inches) | (**Recommended**) Line to match or number in inches to stop table recognition.  Specify this parameter to prevent false positive results and to enable recognizing a table that spans pages.<br/>  A Match object or array specifies to stop table recognition when Sensible matches text.<br/> A number specifies the end of the table as the number of the inches offset along a Y-axis from the start of the table. |
| startOnRow                | integer. default: 0                                      | Zero-indexed row number at which to start table extraction. For example, use this to exclude column headings from the output. As a stricter alternative, set the Is Required parameter on a column and set a type on the column (see example in Examples section). |
| detectMultipleLinesPerRow | boolean. default: false                                  | If true, Sensible detects table cells containing multiple lines, rather than the default of treating each line as a new row.<br/>Set this to false if row gutters are narrow. For example, if vertical gaps between lines in the cells are the same height as row gutters, Sensible can incorrectly merge multiple rows into one. In detail, Sensible detects a cell with multiple lines if the vertical gap between two lines is less than half the height of the second line. Sensible adjusts the row height to accommodate the tallest cell. |
| columnsRelativeToAnchor   | boolean. Default: false                                  | If true, specifies that the column coordinates `minX` and `maxX` are relative to the left edge of the anchor line, rather than to the left edge of the page. For example, use this parameter to recognize nested tables inside tables. |

Examples
====

The following example shows extracting two columns from a difficult-to-recognize table in the Sensible app:

- To prevent Sensible from returning unwanted term matches, the config specifies a Stop parameter.
- To handle cells with multiple lines, the config specifies true for the Detect Multiple Lines Per Row parameter.
- To exclude column headings, the config sets the Is Required parameter to true for column 4 and specifies the cell contents must be a currency.

**Config**

```json
{
  "fields": [
    {
      "id": "text_table",
      "anchor": "outline",
      "type": "table",
      "method": {
        "id": "textTable",
        "detectMultipleLinesPerRow": true,
        "columns": [
          {
            "id": "col2_limits",
            "minX": 2.5,
            "maxX": 4.1
          },
          {
            "id": "col4_premiums",
            "minX": 6,
            "maxX": 7,
            "type": "currency",
            "isRequired": true
          }
        ],
        "stop": {
          "type": "startsWith",
          "text": "please"
        }
      }      
    }
  ]
}
```

**Example document**

The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/text_table.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/text_table_2.pdf) |
| -------------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "text_table": {
    "columns": [
      {
        "id": "col2_limits",
        "values": [
          {
            "value": "$25,000 each person/$50,00 0 each accident",
            "type": "string"
          },
          {
            "value": "$20,000 each accident",
            "type": "string"
          },
          {
            "value": "...................",
            "type": "string"
          }
        ]
      },
      {
        "id": "col4_premiums",
        "values": [
          {
            "source": "$100",
            "value": 100,
            "unit": "$",
            "type": "currency"
          },
          {
            "source": "$10",
            "value": 10,
            "unit": "$",
            "type": "currency"
          },
          {
            "source": "$150",
            "value": 150,
            "unit": "$",
            "type": "currency"
          }
        ]
      }
    ]
  }
}
```


Notes
====

For examples of extracting from complex tables, such as tables inside tables or tables with labled rows and columns, see [Sections](doc:sections#examples).







