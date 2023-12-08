---
title: "Table"
hidden: false
---
Extracts tables based on bag-of-words scoring and returns their collated column contents. Anchor either on the table title or on a table column heading.

 Use the Table method for tables that have variable column formatting.  This method can extract tables that span multiple pages if the column headings repeat on each page.

[**Parameters**](doc:table#parameters)
[**Examples**](doc:table#examples)


Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                    | value                                               | description                                                  |
| :--------------------- | :-------------------------------------------------- | :----------------------------------------------------------- |
| id (**required**)      | `table`                                             | When you specify this method, you must also specify `"type": "table"` in the field's parameters. See the Stop parameter for details about how Sensible recognizes a table. |
| columns (**required**) | array                                               | An array of objects with the following parameters: <br/> -`id` (**required**): The id for the column in the extraction output. <br/>  -`terms` (**required**): An array of terms to score positively during column recognition. Usually, you include column heading terms in this array. For more information about the NLP approach, see [bag of words](doc:bag-of-words). <br/> -`stopTerms`: An array of terms to score negatively during column recognition. For more information about the NLP approach, see [bag of words](doc:bag-of-words). <br/> -`type`: The table cell's type. For more information, see [types](doc:types). <br/>  -`isRequired` (default false): If true, Sensible omits a row if its cell is empty in this column, or if the contents don't match the value you specify in this column's Type parameter. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for *all* columns, even if the row had content under other columns. |
| stop                   | [Match object](doc:match) or array of Match objects | (**Recommended**)  Stops table recognition at the matched line. Otherwise, Sensible searches all pages for tables, which can impact performance.<br/>When you specify a stop, Sensible  uses an Amazon Web Service OCR  provider to perform table recognition. When you omit a stop, Sensible uses a Microsoft OCR provider.<br/>When you specify a stop, Sensible supports merged cells in tables by populating "empty" spanned cells with the spanned value. For an example, see [Merged cell example](doc:table#example-merged-cells). |
| startOnRow             | integer. default: 0                                 | Zero-indexed row number at which to start table extraction. For example, use this to exclude column headings from the output. As a stricter alternative, set the Is Required parameter on a column and set a type on the column (see example in Examples section). |

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

## Example: Merged cells

The following example shows using the Stop parameter to improve output for merged cells:

**Config**

```json
{
  "fields": [
    {
      "id": "merged_cells_example",
      "anchor": "start of table",
      "type": "table",
      "method": {
        "id": "table",
        "columns": [
          {
            "id": "class",
            "terms": [
              "class",
            ],
          },
          {
            "id": "student",
            "terms": [
              "student"
            ],
          },
          {
            "id": "grades",
            "terms": [
              "test",
              "grades"
            ],
          }
        ],
        "stop": {
          "type": "startsWith",
          "text": "end of table"
        }
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/table_merged_cells.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/table_merged_cells.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

Without the Stop parameter, Sensible leaves "merged" cells empty:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/table_merged_cells_0.png)

With the Stop parmeter, Sensible populates "merged" cells:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/table_merged_cells_1.png)

The following JSON shows the "populated" output:

```json
{
  "merged_cells_example": {
    "columns": [
      {
        "id": "class",
        "values": [
          {
            "value": "A",
            "type": "string"
          },
          {
            "value": "A",
            "type": "string"
          },
          {
            "value": "A",
            "type": "string"
          },
          {
            "value": "A",
            "type": "string"
          },
          {
            "value": "B",
            "type": "string"
          },
          {
            "value": "B",
            "type": "string"
          },
          {
            "value": "B",
            "type": "string"
          },
          {
            "value": "B",
            "type": "string"
          }
        ]
      },
      {
        "id": "student",
        "values": [
          {
            "value": "Smith",
            "type": "string"
          },
          {
            "value": "Smith",
            "type": "string"
          },
          {
            "value": "Chavez",
            "type": "string"
          },
          {
            "value": "Chavez",
            "type": "string"
          },
          {
            "value": "Matthers",
            "type": "string"
          },
          {
            "value": "Matthers",
            "type": "string"
          },
          {
            "value": "Kumar",
            "type": "string"
          },
          {
            "value": "Kumar",
            "type": "string"
          }
        ]
      },
      {
        "id": "grades",
        "values": [
          {
            "value": "96",
            "type": "string"
          },
          {
            "value": "87",
            "type": "string"
          },
          {
            "value": "83",
            "type": "string"
          },
          {
            "value": "91",
            "type": "string"
          },
          {
            "value": "100",
            "type": "string"
          },
          {
            "value": "81",
            "type": "string"
          },
          {
            "value": "95",
            "type": "string"
          },
          {
            "value": "98",
            "type": "string"
          }
        ]
      }
    ]
  }
}
```




Notes
====

If tables always have the same column layout (same column headings in the same order, same number of columns), use the [Fixed Table method](doc:fixed-table) instead. 

To extract complex tables, for example tables inside tables or tables with labeled rows and columns, see [Sections](doc:sections#examples).

