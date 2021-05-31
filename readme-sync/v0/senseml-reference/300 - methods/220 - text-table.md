---
title: "Text Table"
hidden: false
---
Matches tables based on coordinates in inches. Use this method when other Table methods can't recognize a table.

Parameters
=====

| key                  | value        | description                                                  |
| :------------------- | :----------- | :----------------------------------------------------------- |
| id **required**      | `table`      | When you specify the Table method in a Field query object, you must also specify `"type": "table"` in the field's parameters. |
| columns **required** | array        | An array of objects with the following parameters:<br/> *`id` (**required**): The id for the column in the extraction output<br/> *`minX` (**required**):  The distance in inches on the page from the left edge of the page to the left edge of the column.  <br/>  *`maxX` (**required**):  The distance in inches on the page from the left edge of the page to the right edge of the column.  <br/>  *`type`: The type of the value in the table cell. For more information about types, see [Field query object](doc:field-query-object).<br/>   *`isRequired` (default false):  If true, the extraction will not return rows where a value is not present in this column |
| offsetY              | number       | The offset, in inches, along a Y-axis from the anchor text, from which to start recognizing the table. |
| stop                 | Match object | **Recommended** [Match object](doc:anchor-object#section-match-object)  to stop table recognition. OCR is a prerequisite for table recognition. With `stop` defined, the engine selectively OCRs the pages from the starting anchor to the page with the stop match. Otherwise, the engine OCRs all pages, which can impact performance. |

Examples
====

The following example shows extracting two columns from a table in the Sensible app:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/review/readme-sync/assets/v0/images/text_table_example.png)


You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for box recognition | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/example_text_table_2.pdf) |
| ------------------------------- | ------------------------------------------------------------ |

This example uses the following config:

```json
{
  "fields": [
    {
      "id": "agile_risks_table_updates_monthly",
      "anchor": "outline",
      "type": "table",
      "method": {
        "id": "textTable",
        "columns": [
          {
            "id": "col2_limits",
            "minX": 2.5,
            "maxX": 4.1
          },
          {
            "id": "col4_premiums",
            "minX": 6,
            "maxX": 7
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


