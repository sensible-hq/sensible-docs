---
title: "NLP Table"
hidden: true
---


Parameters
====


| key               | value  | description                                                  |
| :---------------- | :----- | :----------------------------------------------------------- |
| pageSpanThreshold | object | Configure this parameter for advanced multi-page table extraction edge cases.<br/>By default, Sensible detects multi-page tables by checking if the table is near the top or bottom of the page. If it is, Sensible searches previous and succeeding pages for continuations of the table.<br/> Sometimes, a multi-page table is separated from the top or bottom of the page by intervening non-table text, such as footnotes or text box inserts. To account for the extra space taken up by non-table text, use the following parameters:<br/>- `top`: number. default: 0.4. By default, Sensible searches the previous page for a continuation of a multi-page table if the table starts in the top 40% of the page. Change the percent using this parameter.<br/>-  `bottom`: number. default: 0.8. By default, Sensible searches the next page for a continuation of a multi-page table if the table ends in the bottom 20% of the page. Change the percent using this parameter.<br/>Sensible keep merging the multi-page table until the Page Span Threshold conditions are no longer met. |
|                   |        |                                                              |
|                   |        |                                                              |
|                   |        |                                                              |
|                   |        |                                                              |
|                   |        |                                                              |
|                   |        |                                                              |
|                   |        |                                                              |
|                   |        |                                                              |
|                   |        |                                                              |



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
        /* overall description of table's contents */
        "description": "insured vehicles",
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
        "description": "transactions for insurance account",
        "columns": [
          {
            "id": "transaction_date",
            /* note GPT has some limitations due to its training data. 
               For example, if it doesn't know the current year 
               it makes one up in the output */
            "description": "transaction date. If there's no year, append the current year.",
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

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/nlp_table.pdf) |
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


1. To optimize performance, Sensible makes a list of the pages that are most likely to contain your target table. To make the list:
   - Sensible concatenates all your column descriptions with your overall table description. 
   - Sensible splits the document into equal-sized, overlapping chunks. 
   - Sensible scores your concatenated table descriptions against each chunk using the OpenAI Embeddings API.
   - Sensible gets a list of page numbers from the top-scoring chunks.
2. Sensible extracts all the tables on the pages most likely to contain your table, using an Amazon OCR provider. Sensible supports multi-page tables.

3. For each extracted table, Sensible extracts the table title, if present.  In detail:

   -  Sensible extracts lines contained in a rectangular region immediately above each table, since that region is likely to contain the table title. 
   -  The height of that region equals the line height of the first non-empty cell of the table + 0.1 inches, and the region extends down to the top boundary of the table.
   -  For information about how Sensible determines if lines are "contained" in a region, see [Region](doc:region).

4. Sensible scores each table by how well it matches the descriptions you provide of the data you want to extract. To create the score:

   - Sensible concatenates all your column descriptions with your overall table description. 

   - Sensible concatenates the first two rows of the table with the table title.

   - Sensible compares the two concatenations using the OpenAI Embeddings API. 

5. Sensible creates a full prompt for GPT-4 that includes the top-scoring table, page hinting data, and your prompts. For more information about the full prompt, see [Advanced prompt configuration](doc:prompt). The full prompt instructs GPT-4 to restructure the best-scoring table based on your column descriptions and your overall table description. 

6. Sensible returns the restructured table.