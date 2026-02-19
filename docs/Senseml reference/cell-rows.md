---
title: Spreadsheet extraction
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Extract from large spreadsheets'
  robots: index
next:
  description: ''
---
For large spreadsheets with tens of thousands of rows, the Cell Rows field type extracts cells under specified column headings. This method has the following limitations:

* The spreadsheet must have a simple columnar layout, where the first row or rows contains your target column headers. This method extracts cells in each specified column until the end of the sheet. 
* This method extracts solely from the first tab in multi-tab spreadsheets. 
* You must upload the spreadsheet to Sensible as one of the [supported](doc:file-types) spreadsheet file types. This method doesn't support PDFs. 

The Cell Rows field type is a speedier alternative to general-purpose SenseML methods, which you can use with smaller spreadsheets. 

# Parameters

| key                      | value                                                        | description                                                  |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)        | string                                                       | Specifies an ID for a group of rows to extract in the spreadsheet. Sensible ignores empty rows and extracts data under the specified Header Row to the end of the worksheet. |
| type  (**required**)     | `cellRows`                                                   |                                                              |
| headerRow (**required**) | Anchor object                                                | Specifies the row containing column headers, by matching the specified line or lines in the row. Sensible ignores empty cells in the header row. Contains the following parameters:<br/>-`match`: A [Match](doc:match) object or array of Match objects. |
| headerRowsCount          | integer. default: 1                                          | Specifies the number of consecutive header rows. You can specify a match in the Field object's Header parameter for any header row. |
| stop                     | [Match object](doc:match) or array of Match objects. default: none | Stops extraction at the end of the row above the matched line. Excludes the row containing the matched line. |
| fields                   | array of fields that use any of the following methods:<br/>-  the `cell` method<br/>[computed field-methods](doc:computed-field-methods)<br/>- [custom computation group](doc:custom-computation-group) method | Specifies fields that use one or more of the following methods, all of which operate row-by-row:<br/><br/>- **`cell`**: A spreadsheet-specific method that extracts a cell under the specified header for each extracted row. Parameters:<br/>`id`: `cell`. Note: The [method](doc:method) object's global parameters aren't available for this method.<br/>`header`:  A [Match](doc:match) object that specifies the column heading under which you want to extract cells. For an example, see the following section.<br/><br/>- **Computed field methods**: Fields that use [computed field methods](doc:computed-field-methods), such as the Split, Suppress Output, or Custom Computation methods, operate on the already-extracted cell values for each row. Each field adds a computed field to each row's output.<br/><br/>- **Custom Computation Group method:** Fields that use the [Custom Computation Group](doc:custom-computation-group) method operate on the already-extracted cell values for each row. Because each field can add multiple computed fields to each row's output, this method offers more concise syntax and faster performance than the Custom Computation method. For an example, see [Custom computation group example](#custom-computation-group-example). |



## Example

The following example extracts bestselling book data from a spreadsheet. It uses `customComputationGroup` to convert the raw sales figures (stored in millions in the column header) to actual copy counts and to flag books with over 50 million copies sold.

**Config**

```json
{
  "fields": [
    {
      "id": "bestselling_books",
      "type": "cellRows",
      /* specify the column headings row: contains the lines 'author(s)' and 'genre */
      "headerRow": {
        "match": [
          {
            "type": "startsWith",
            "text": "author"
          },
          {
            "type": "includes",
            "text": "genre"
          }
        ]
      },
      "fields": [
        {
          "id": "book_title",
          "method": {
            "id": "cell",
            /* extract all the cells under the column header that starts with 
               the text `book` until the end of the sheet (skips empty rows)  */
            "header": {
              "type": "startsWith",
              "text": "book"
            }
          }
        },
        {
          "id": "first_published",
          "method": {
            "id": "cell",
            /* extract the cells under the header containing `published` */
            "header": {
              "type": "includes",
              "text": "published"
            }
          }
        },
        {
          /* get the raw sales data,
           which includes footnotes, e.g., 50 million[47] */
          "id": "_sales_raw",
          "method": {
            "id": "cell",
            /* extract the cells under the header that starts with 
               the text `approximate`  */
            "header": {
              "type": "startsWith",
              "text": "approximate"
            }
          }
        },
        {
          /* strip the footnotes from the sales data
             by splitting the extracted _sales_raw string 
             on the start of the first footnote ([)] */
          "id": "sales",
          "method": {
            "id": "split",
            "source_id": "_sales_raw",
            "separator": "[",
            "index": 0
          }
        },
        {
          /* the column header says 'in millions', so multiply by 1,000,000
             to get the actual copy count, and flag blockbuster titles */
          "method": {
            "id": "customComputationGroup",
            "jsonLogic": {
              "eachKey": {
                "sales_copies": {"*": [{"var": "_sales_raw.value"}, 1000000]},
                "over_50_million": {">": [{"var": "_sales_raw.value"}, 50]}
              }
            }
          }
        },
        {
          /* for cleaner output, hide the raw sales data */
          "id": "hide_fields",
          "method": {
            "id": "suppressOutput",
            "source_ids": ["_sales_raw"]
          }
        }
      ]
    }
  ]
}

```

**Example document**\
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/cell_rows.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/cell_rows.xlsx) |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "bestselling_books": [
    {
      "book_title": {
        "value": "A Tale of Two Cities",
        "type": "string"
      },
      "first_published": {
        "value": "1859",
        "type": "string"
      },
      "sales": {
        "value": "200",
        "type": "string"
      },
      "sales_copies": {
        "value": 200000000,
        "type": "number"
      },
      "over_50_million": {
        "value": true,
        "type": "boolean"
      }
    },
    {
      "book_title": {
        "value": "The Alchemist (O Alquimista)",
        "type": "string"
      },
      "first_published": {
        "value": "1988",
        "type": "string"
      },
      "sales": {
        "value": "150",
        "type": "string"
      },
      "sales_copies": {
        "value": 150000000,
        "type": "number"
      },
      "over_50_million": {
        "value": true,
        "type": "boolean"
      }
    },
    "..."
  ]
}
```
