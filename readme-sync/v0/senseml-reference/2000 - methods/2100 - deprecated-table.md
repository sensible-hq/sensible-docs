---
title: "(Deprecated) Table"
hidden: true
---
# Deprecated

This method is deprecated. To duplicate this method's function, use the [NLP Table ](doc:nlp-table)method and set the Rewrite Table parameter to false.

## Description

Extracts tables based on bag-of-words scoring and returns their collated column contents. Anchor either on the table title or on a table column heading.

 Use the Table method for tables that have variable column formatting.  

For alternatives to this method, see [Choosing a table method](doc:table-methods). 

[**Parameters**](doc:deprecated-table#parameters)
[**Examples**](doc:deprecated-table#examples)


Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                      | value                                               | description                                                  |
| :----------------------- | :-------------------------------------------------- | :----------------------------------------------------------- |
| id (**required**)        | `table`                                             | When you specify this method, you must also specify `"type": "table"` in the field's parameters. See the Stop parameter for details about how Sensible recognizes a table. |
| columns (**required**)   | array                                               | An array of objects with the following parameters: <br/> -`id` (**required**): The id for the column in the extraction output. <br/>  -`terms` (**required**): An array of terms to score positively during column recognition. Usually, you include column heading terms in this array. For more information about the NLP approach, see [bag of words](doc:bag-of-words). <br/> -`stopTerms`: An array of terms to score negatively during column recognition. For more information about the NLP approach, see [bag of words](doc:bag-of-words). <br/> -`type`: The table cell's type. For more information, see [types](doc:types). <br/>  -`isRequired` (default false): If true, Sensible omits a row if its cell is empty in this column, or if the contents don't match the value you specify in this column's Type parameter. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for *all* columns, even if the row had content under other columns. |
| stop                     | [Match object](doc:match) or array of Match objects | (**Recommended**)  Stops table recognition at the matched line. Otherwise, Sensible searches all pages for tables, which can impact performance.<br/>When you specify a stop, Sensible  uses an Amazon Web Service OCR  provider to perform table recognition. When you omit a stop, Sensible uses a Microsoft OCR provider.<br/>When you specify a stop, Sensible supports:<br/>- merged cells in tables. Sensible populates "empty" spanned cells with the spanned value. For an example, see [Merged cell example](doc:fixed-table#example-merged-cells).<br/> - checkboxes in cells. Returns checkbox selection status as `[true]` or `[false]`. |
| startOnRow               | integer. default: 0                                 | Zero-indexed row number at which to start table extraction. For example, use this to exclude column headings from the output. As a stricter alternative, set the Is Required parameter on a column and set a type on the column (see example in Examples section). |
| detectTableStructureOnly | boolean. default: false                             | Set this parameter to true to troubleshoot optional character recognition (OCR) in a table. If true, Sensible bypasses the text output by the table recognition OCR provider. Sensible instead recognizes the table's text using the  [OCR engine](doc:ocr-engine) specified by your document type, or by using text embedded in the document file if present. |

Examples
====

## Example: Variable columns

The following example shows extracting two columns from a table that updates monthly with a variable number of columns in the Sensible app.

- To omit column headings, the config specifies `"type": "number"` and `"isRequired": true` for the column `rank_this_month`. You can also use `"startOnRow":1` to omit headings.
- To improve performance, the config specifies a Stop parameter.


**Config**

```json
{
  "fields": [
    {
      "id": "agile_risks_table_updates_monthly",
      "anchor": "agile software",
      "type": "table",
      "method": {
        "id": "table",
        "columns": [
          {
            "id": "col1_risk_description",
            "terms": [
              "risk",
              "description"
            ],
          },
          {
            "id": "rank_this_month",
            "terms": [
              "this month"
            ],
            "type": "number",
            "isRequired": true
          }
        ],
        "stop": {
          "type": "startsWith",
          "text": "project managers"
        }
      }
    }
  ]
}
```
**Example document**

The following image shows the example document used with this example config: ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/table_dynamic.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/table_dynamic.pdf) |
| --------------------- | ------------------------------------------------------------ |

**Output**
```json
{
  "agile_risks_table_updates_monthly": {
    "columns": [
      {
        "id": "col1_risk_description",
        "values": [
          {
            "value": "Poor task point estimation",
            "type": "string"
          },
          {
            "value": "Poor epic scope definition",
            "type": "string"
          },
          {
            "value": "Inadequate scrum master training",
            "type": "string"
          }
        ]
      },
      {
        "id": "rank_this_month",
        "values": [
          {
            "source": "3",
            "value": 3,
            "type": "number"
          },
          {
            "source": "1",
            "value": 1,
            "type": "number"
          },
          {
            "source": "2",
            "value": 2,
            "type": "number"
          }
        ]
      }
    ]
  }
}
```




Notes
====

For alternatives to this method, see [Choosing a table method](doc:table-methods). 

