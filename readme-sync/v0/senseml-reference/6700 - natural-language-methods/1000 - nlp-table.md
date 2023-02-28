---
title: "NLP Table"
hidden: false
---
Extracts a table based on your natural-language description of the data you want to extract.

Use this method as a low-code alternative to layout-based Table methods, such as [Text Table](doc:text-table).

**Advantages**

- Low code. 
- Can reformat or filter extracted column data based on your natural-language instructions. 
- Doesn't require an [anchor](doc:anchor).

**Limitations**

- Can impact performance, because it performs table recognition for the entire document.
- Suited to tables that have a header row, where each row is a data element. Not suited to tables where the header is in the first column and the columns are data elements.
- Doesn't support tables that span pages.

**Alternatives**

-   [Fixed Table](doc:fixed-table) or [Text table](doc:text-table) methods.
- To extract complex tables, for example tables-inside-tables or tables with labeled rows and columns, see [Sections](doc:sections#examples).

**How it works**

For more information about how this method works, see [Notes ](doc:nlp-table#notes).

[**Parameters**](doc:nlp-table#parameters)
[**Examples**](doc:nlp-table#examples)
[**Notes**](doc:nlp-table#notes)

Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.


| key                    | value      | description                                                  |
| :--------------------- | :--------- | :----------------------------------------------------------- |
| id (**required**)      | `nlpTable` | The Anchor parameter is optional for fields that use this method. If you don't specify an anchor, Sensible searches the whole document for the table.<br/>If you specify an anchor, Sensible ignores any tables before the anchor and starts searching for candidate tables after the anchor. In detail, Sensible ignores a table if 1. it occurs on a page previous to the page containing the anchor, or 2. if on the same page, it ignores the table if the table's lower boundary is higher on the page than the lower boundary of the anchor line. |
| columns (**required**) | array      | An array of objects with the following parameters: <br/> -`id` (**required**): A user-friendly ID for the column in the extraction output. <br/>  -`description` (**required**):  A natural-language description of the data you want to extract from the column. The description can include instructions to reformat or filter the column's data. For example, provide descriptions like `" transaction amount. return the absolute value"` or `"vehicle make (not model)"`.  <br/> -`type`: The table cell's type. For more information, see [types](doc:types). <br/>  -`isRequired` (default false): If true, Sensible omits a row if its cell is empty in this column, or if the contents don't match the value you specify in this column's Type parameter. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for *all* columns, even if the row had content under other columns. |


Examples
====

The following example shows using the NLP Table method to extract information from tables about insured vehicles and insurance transactions.

**Config**

```json
{
  "fields": [
    {
      /* the id is a user-friendly name for the target table */
      "id": "insured_vehicles_table",
      "type": "table",
      "method": {
        "id": "nlpTable",
        "columns": [
          {
            /* for each column, provide a user-friendly ID
               and a description of the data you want to extract from the column 
               and optional instructions to filter or reformat the data*/
            "id": "manufacturer",
            "description": "vehicle make (not model)",
          },
          {
            "id": "year",
            "description": "year of manufacture",
          }
        ]
      }
    },
    {
      "id": "transactions_table",
      "type": "table",
      "method": {
        "id": "nlpTable",
        "columns": [
          {
            "id": "transaction_date",
            /* note GPT3 has some limitations due to its training data. 
               For example, it doesn't know the current year 
               so it makes one up in the output */
            "transaction_description": "transaction date. If there's no year, append the current year.",
          },
          {
            "id": "transaction_description",
            "description": "transaction description"
          },
          {
            "id": "amount",
            "description": "transaction amount, returned as an absolute value",
            "type": "currency"
          }
        ]
      }
    }
  ],
  "computed_fields": [
    /* optional: for cleaner output, zip each table 
       into an array of rows objects */
    {
      "id": "zipped_insured_vehicles",
      "method": {
        "id": "zip",
        "source_ids": [
          "insured_vehicles_table",
        ]
      }
    },
    {
      "id": "zipped_transactions",
      "method": {
        "id": "zip",
        "source_ids": [
          "transactions_table",
        ]
      }
    },
    /* optional: for cleaner output, remove the source
       tables. */
    {
      "id": "hide_fields",
      "method": {
        "id": "suppressOutput",
        "source_ids": [
          "transactions_table",
          "insured_vehicles_table"
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/nlp_table.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/nlp_table.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "zipped_insured_vehicles": [
    {
      "manufacturer": {
        "value": "Toyota",
        "type": "string"
      },
      "year": {
        "value": "2010",
        "type": "string"
      }
    },
    {
      "manufacturer": {
        "value": "Honda",
        "type": "string"
      },
      "year": {
        "value": "2015",
        "type": "string"
      }
    },
    {
      "manufacturer": {
        "value": "VW",
        "type": "string"
      },
      "year": {
        "value": "2020",
        "type": "string"
      }
    }
  ],
  "zipped_transactions": [
    {
      "transaction_date": {
        "value": "02/19/2019",
        "type": "string"
      },
      "transaction_description": {
        "value": "Paid premium",
        "type": "string"
      },
      "amount": {
        "source": "$100.01",
        "value": 100.01,
        "unit": "$",
        "type": "currency"
      }
    },
    {
      "transaction_date": {
        "value": "01/03/2019",
        "type": "string"
      },
      "transaction_description": {
        "value": "Amount awarded for claim #123456789",
        "type": "string"
      },
      "amount": {
        "source": "$200.67",
        "value": 200.67,
        "unit": "$",
        "type": "currency"
      }
    }
  ]
}
```



Notes
===

For an overview of how the NLP Table method works, see the following steps:


1. Sensible finds all tables in the document using a Microsoft OCR provider.

2. Sensible scores each table by how well it matches the descriptions you provide of the data you want to extract. To create the score, Sensible compares your concatenated descriptions against the concatenated first two rows of the table using the OpenAPI Embeddings API. 

3. Sensible uses GPT-3 to restructure the table based on your column descriptions. Sensible returns the result in Sensible's standard table output format.

   