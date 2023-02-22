---
title: "NLP Table"
hidden: true
---
Uses GPT3 to extract a table, based on your natural-language description of the data you want to extract.

Use this method as a low-code alternative to layout-based Table methods, such as [Fixed Table](doc:fixed-table).

**Advantages**

- Low code. 
- You can use natural-language instructions to reformat or filter extracted column data.
- Doesn't require an [anchor](doc:anchor).

**Limitations**

- Can impact performance, because it triggers OCR for the entire document.
- Suited to simple tables where the first row in each column is a header that describes the contents of the column.
- Doesn't support tables that span pages.

**Alternatives**

-  [Table](doc:table) or [Fixed Table](doc:fixed-table) methods
- To extract complex tables, for example tables-inside-tables or tables with labeled rows and columns, see [Sections](doc:sections#examples).

**How it works**

1. Sensible uses an Microsoft OCR provider to find all the tables in the document. Sensible ignores any OCR settings you configure for the document type and uses Microsoft to OCR the entire document.
2. Sensible scores each table by how well it matches the descriptions you provide of the data you want to extract. To create the score, Sensible compares your concatenated descriptions against the concatenated first two rows of the table using an OpenAPI embedding API. 
3. Sensible inputs the raw text of the highest-scoring table to GPT-3, and instructs GPT3 to output a new  table as follows:  `rearrange the below data into a tabular format where each row of the table answers the question posed in the header of the table. If the below data don't contain an answer to the question, just leave that cell of the table blank`
4. Sensible reformats the table returned by GPT3 to:
   1. format it in standard SenseML table format
   2.  remove the original table's column headers 

Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.


| key                    | value      | description                                                  |
| :--------------------- | :--------- | :----------------------------------------------------------- |
| id (**required**)      | `nlpTable` | The Anchor parameter is optional for fields that use this method. If you omit an anchor, Sensible searches the entire document for the data you want to extract. TODO: is that true |
| columns (**required**) | array      | An array of objects with the following parameters: <br/> -`id` (**required**): A user-friendly ID for the column in the extraction output. <br/>  -`description` (**required**):  a natural-language description of the data you want to extract from the column. The description can include instructions to reformat or filter the column's data. For example, provide descriptions like `"The transaction amount. return the absolute values of the monetary amount"` or `"return the car make but not the model from this column"`.  <br/> -`type`: The table cell's type. For more information, see [types](doc:types). <br/>  -`isRequired` (default false): If true, Sensible omits a row if its cell is empty in this column, or if the contents don't match the value you specify in this column's Type parameter. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for *all* columns, even if the row had content under other columns. |


Examples
====

Example 1
---

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
               and a description of the data you want to extract from the column */
            "id": "manufacturer",
            "description": "the make of the vehicle, not the model",
          },
          {
            "id": "year",
            "description": "the year of manufacture of the vehicle",
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
               For example, it doesn't know the current year so it makes one up in the output */
            "description": "the date of the transaction. If there's no year, append the current year.",
          },
          {
            "id": "description",
            "description": "the description of the monetary transaction."
          },
          {
            "id": "amount",
            "description": "the monetary amount of the transaction, as an absolute value",
            "type": "currency"
          }
        ]
      }
    }
  ],
  "computed_fields": [
    /* optional: for cleaner output, zip each table into an array of rows objects */
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
      "description": {
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
      "description": {
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



