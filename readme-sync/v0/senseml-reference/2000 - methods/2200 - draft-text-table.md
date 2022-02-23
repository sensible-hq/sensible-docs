---
title: "Text Table"
hidden: true
---
Use this method when other Table methods can't recognize a table. This method's advantage is that it's faster than other Table methods because it doesn't use table recognition. Its disadvantage is that it's more limited than other table methods, because it relies on strict line alignment within the table.

[**Parameters**](doc:text-table#parameters)
[**Examples**](doc:text-table#examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                    | value                                                      | description                                                  |
| :--------------------- | :--------------------------------------------------------- | :----------------------------------------------------------- |
| i*d **required***      | *`table`*                                                  | *When you specify this method, you must also specify `"type": "table"` in the field's parameters.* |
| *columns **required*** | *array*                                                    | *An array of objects with the following parameters:<br/> -`id` (**required**): The id for the column in the extraction output.<br/> -`minX` (**required**):  The distance in inches on the page from the left edge of the page to the left edge of the column. To determine this coordinate, open the PDF in a viewer, such as Preview or Gimp, that displays cursor coordinates.  <br/>  -`maxX` (**required**):  The distance in inches on the page from the left edge of the page to the right edge of the column. To determine this coordinate, open the PDF in a viewer, such as Preview or Gimp, that displays cursor coordinates <br/>  -`type`: The table cell's type. For more information about types, see [Field query object](doc:field-query-object).<br/>   -`isRequired` (default false):  If true, Sensible omits a row if its cell is empty in this column. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for all columns, even if the row had content under other columns.* |
| *offsetY*              | *number*                                                   | *Defines a starting point from which to search down the page and recognize a  table. The starting point is offset in inches along a Y-axis from the anchor line's lower boundary.* |
| *stop*                 | *Match object, array of Match objects, or number (inches)* | *(**Recommended**) Line to match or number in inches to stop table recognition.  Specify this parameter to prevent false positive results and to enable recognizing a table that spans pages.<br/>  A Match object or array specifies to stop table recognition when Sensible matches text.<br/> A number specifies the end of the table as the number of the inches offset along a Y-axis from the start of the table.* |
| *startOnRow*           | *integer. default: 0*                                      | *Zero-indexed row number at which to start table extraction. For example, use this to exclude column headings from the output. As a stricter alternative, set the Is Required parameter on a column and set a type on the column (see example in Examples section).* |
| detectMultilineCells   | boolean. default: false                                    | If true, Sensible detects if a table cell contains multiple lines. If the vertical gap between two lines is less than half the height of the second line, Sensible treats them as belonging to the same cell and adjusts the row height to accommodate the tallest cell.<br/>Set this to false if row gutters are narrow (for example, line breaks inside the cells are the same width as row gutters), or else Sensible can incorrectly merge multiple rows into one. |

Examples
====

The following example shows extracting two columns from a difficult-to-recognize table in the Sensible app:

- Since this method doesn't recognize cells with more than one line of data, Sensible returns dollar limits in separate rows. TODO: update
- To prevent Sensible from returning unwanted term matches, the config specifies a Stop parameter.

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
        "columns": [
          {
            "id": "col2_limits",
            "minX": 2.5,
            "maxX": 4.1,
            "type": "currency"
          },
          {
            "id": "col4_premiums",
            "minX": 6,
            "maxX": 7,
            "type": "currency"
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

**PDF**

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
          null,
          {
            "source": "$25,000",
            "value": 25000,
            "unit": "$",
            "type": "currency"
          },
          {
            "source": "$50",
            "value": 50,
            "unit": "$",
            "type": "currency"
          },
          {
            "source": "0",
            "value": 0,
            "unit": "$",
            "type": "currency"
          },
          null,
          {
            "source": "$20,000",
            "value": 20000,
            "unit": "$",
            "type": "currency"
          },
          null,
          null
        ]
      },
      {
        "id": "col4_premiums",
        "values": [
          null,
          {
            "source": "$100",
            "value": 100,
            "unit": "$",
            "type": "currency"
          },
          null,
          null,
          null,
          {
            "source": "$10",
            "value": 10,
            "unit": "$",
            "type": "currency"
          },
          null,
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









