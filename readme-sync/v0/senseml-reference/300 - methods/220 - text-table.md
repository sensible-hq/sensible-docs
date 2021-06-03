---
title: "Text Table"
hidden: false
---
Matches tables based on coordinates in inches. Choose anchor text that precedes the table, for example, a table title.  

Use this method when other Table methods can't recognize a table. This method is faster than other Table methods because it does not use OCR. However, it is more limited than other table methods because it relies on strict line alignment within the table. It therefore can't recognize multiple lines as belonging to a single cell. In the case of a multi-line cell, this method treats each line as its own row. For an example, see the [Examples section](doc:text-table#section-examples).

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method-object#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| key                  | value                           | description                                                  |
| :------------------- | :------------------------------ | :----------------------------------------------------------- |
| id **required**      | `table`                         | When you specify the Table method in a Field query object, you must also specify `"type": "table"` in the field's parameters. |
| columns **required** | array                           | An array of objects with the following parameters:<br/> -`id` (**required**): The id for the column in the extraction output<br/> -`minX` (**required**):  The distance in inches on the page from the left edge of the page to the left edge of the column.  <br/>  -`maxX` (**required**):  The distance in inches on the page from the left edge of the page to the right edge of the column.  <br/>  -`type`: The type of the value in the table cell. For more information about types, see [Field query object](doc:field-query-object).<br/>   -`isRequired` (default false):  If true, SenseML does not return rows in which a value is not present in this column. If false, SenseML returns nulls for rows in which a value is not present. Bear in mind that if you set this parameter to true for an empty row in one column, SenseML leaves out that row for all other columns as well, even if that row had content under a different column. |
| offsetY              | number                          | Defines a starting point from which to recognize table. The starting point is  offset in inches along a Y-axis from the anchor line. |
| stop                 | Match object or number (inches) | **Recommended** [Match object](doc:anchor-object#section-match-object)  or number in inches to stop table recognition.   Specify this parameter to prevent false positive results.<br/>  A match object specifies to stop table recognition when SenseML matches text.<br/> A number specifies the end of the table as the number of the inches offset along a Y-axis from the start of the table. |

Examples
====

The following image shows extracting two columns from a difficult-to-recognize table in the Sensible app. Since this method does not recognize multiline cells, dollar limits are returned in separate rows: 

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/review/readme-sync/assets/v0/images/text_table_example.png)


You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for text table | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/example_text_table_2.pdf) |
| -------------------------- | ------------------------------------------------------------ |

This example uses the following config:

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

