---
title: "Spreadsheet extraction"
hidden: false
---

For large spreadsheets with tens of thousands of rows, the Cell Rows field type extracts rows under a specified column-headings row. Sensible extracts rows until the end of the document. The Cell Rows field type is a speedier alternative to general-purpose SenseML methods, which you can use with smaller spreadsheets.

**Notes**:

This method doesn't work with PDFs. You must upload the spreadsheet to Sensible as one of the [supported](doc:file-types) spreadsheet file types.

Parameters
====


| key                      | value                                                        | description                                                  |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)        | string                                                       | Specifies an ID for a group of rows to extract in the spreadsheet. Sensible ignores empty rows and extracts data under the specified Header Row to the end of the worksheet. |
| type  (**required**)     | `cellRows`                                                   | Specifies that this field extracts spreadsheet rows.         |
| headerRow (**required**) | Anchor object                                                | Specifies the row containing column headers, by matching the specified line or lines in the row. Sensible ignores empty cells in the header row. Contains the following parameters:<br/>-`match`: A [Match](doc:match) object or array of Match objects. |
| headerRowsCount          | integer. default: 1                                          | Specifies the number of consecutive header rows. You can specify a match in the Field object's Header parameter for any header row. |
| stop                     | [Match object](doc:match) or array of Match objects. default: none | Stops extraction at the end of the row above the matched line. Excludes the row containing the matched line. |
| fields                   | array of [computed fields](doc:computed-field-methods) or  spreadsheet-specific fields | Specifies either:<br/><br/><br/>- fields that use a spreadsheet-specific method, `cell`. The cell method extracts a cell under the specified header for each extracted row. It contains the following parameters:<br/>`id`: `cell`. Note: The [method](doc:method) object's global parameters aren't available for this method.<br/>`header`:  A [Match](doc:match) object that specifies the column heading under which you want to extract cells. For an example, see the following section.<br/><br/><br/>- fields that use [computed fields methods](doc:computed-field-methods).<br/> |

## Examples

The following example shows using a Cell Rows field to extract rows from a spreadsheet.

**Config**

```json
{
  "fields": [
    {
      "id": "bestselling_books",
      "type": "cellRows",
      /* Sensible extracts specified cells from all the rows under the row that contains the matching strings "book" and "author", until the end of the document */
      "headerRow": {
        "match": [
          {
            "type": "startsWith",
            "text": "book"
          },
          {
            "type": "startsWith",
            "text": "author"
          }
        ],
      },
      "fields": [
        {
          "id": "book",
          "method": {
            "id": "cell",
            /* for each row, extract the cell under the header that starts with 
               the text `book` (skips empty rows)  */
            "header": {
              "type": "startsWith",
              "text": "book",
            },
          }
        },
        {
          "id": "first_published",
          "method": {
            "id": "cell",
            /* for each row, extract the cell under the header containing `published` */
            "header": {
              "type": "includes",
              "text": "published",
            },
          }
        },
        {
          /* get the raw sales data,
           which includes footnotes, e.g., 50 million[47] */
          "id": "_sales_raw",
          "method": {
            "id": "cell",
            /* for each row, extract the cell under the header that starts with 
               the text `approximate` (skips empty rows)  */
            "header": {
              "type": "startsWith",
              "text": "approximate",
            },
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
          /* for cleaner output, hide the raw sales data */
          "id": "hide_fields",
          "method": {
            "id": "suppressOutput",
            "source_ids": [
              "_sales_raw"
            ]
          }
        }
      ]
    },
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/cell_rows.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/cell_rows.xlsx) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "bestselling_books": [
    {
      "book": {
        "value": "A Tale of Two Cities",
        "type": "string"
      },
      "first_published": {
        "value": "1859",
        "type": "string"
      },
      "sales": {
        "value": ">200 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "The Little Prince (Le Petit Prince)",
        "type": "string"
      },
      "first_published": {
        "value": "1943",
        "type": "string"
      },
      "sales": {
        "value": "200 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "The Alchemist (O Alquimista)",
        "type": "string"
      },
      "first_published": {
        "value": "1988",
        "type": "string"
      },
      "sales": {
        "value": "150 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "Harry Potter and the Philosopher's Stone",
        "type": "string"
      },
      "first_published": {
        "value": "1997",
        "type": "string"
      },
      "sales": {
        "value": "120 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "And Then There Were None",
        "type": "string"
      },
      "first_published": {
        "value": "1939",
        "type": "string"
      },
      "sales": {
        "value": "100 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "Dream of the Red Chamber (紅樓夢)",
        "type": "string"
      },
      "first_published": {
        "value": "1791",
        "type": "string"
      },
      "sales": {
        "value": "100 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "The Hobbit",
        "type": "string"
      },
      "first_published": {
        "value": "1937",
        "type": "string"
      },
      "sales": {
        "value": "100 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "Alice's Adventures in Wonderland",
        "type": "string"
      },
      "first_published": {
        "value": "1865",
        "type": "string"
      },
      "sales": {
        "value": "100 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "Between 50 million and 100 million copies",
        "type": "string"
      },
      "first_published": null,
      "sales": null
    },
    {
      "book": {
        "value": "The Lion, the Witch and the Wardrobe",
        "type": "string"
      },
      "first_published": {
        "value": "1950",
        "type": "string"
      },
      "sales": {
        "value": "85 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "She: A History of Adventure",
        "type": "string"
      },
      "first_published": {
        "value": "1887",
        "type": "string"
      },
      "sales": {
        "value": "83 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "The Da Vinci Code",
        "type": "string"
      },
      "first_published": {
        "value": "2003",
        "type": "string"
      },
      "sales": {
        "value": "80 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "Harry Potter and the Chamber of Secrets",
        "type": "string"
      },
      "first_published": {
        "value": "1998",
        "type": "string"
      },
      "sales": {
        "value": "77 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "The Catcher in the Rye",
        "type": "string"
      },
      "first_published": {
        "value": "1951",
        "type": "string"
      },
      "sales": {
        "value": "65 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "The Bridges of Madison County",
        "type": "string"
      },
      "first_published": {
        "value": "1992",
        "type": "string"
      },
      "sales": {
        "value": "60 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "One Hundred Years of Solitude (Cien años de soledad)",
        "type": "string"
      },
      "first_published": {
        "value": "1967",
        "type": "string"
      },
      "sales": {
        "value": "50 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "Lolita",
        "type": "string"
      },
      "first_published": {
        "value": "1955",
        "type": "string"
      },
      "sales": {
        "value": "50 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "Heidi",
        "type": "string"
      },
      "first_published": {
        "value": "1880",
        "type": "string"
      },
      "sales": {
        "value": "50 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "The Common Sense Book of Baby and Child Care",
        "type": "string"
      },
      "first_published": {
        "value": "1946",
        "type": "string"
      },
      "sales": {
        "value": "50 million",
        "type": "string"
      }
    },
    {
      "book": {
        "value": "attribution:",
        "type": "string"
      },
      "first_published": null,
      "sales": null
    }
  ]
}
```
