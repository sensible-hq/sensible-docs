---
title: "NLP Table"
hidden: false
---
Extracts a table based on your natural-language description of the data you want to extract. This method can extract tables that span multiple pages.

For tips on authoring this method in Sensible Instruct, see [Table tips](doc:list-tips).

**Advantages**

- Low code. 
- Can reformat or filter extracted column data based on your natural-language instructions. 
- Doesn't require an [anchor](doc:anchor).

**Limitations**

- Can have a moderate impact on performance. For more information, see [Optimizing extraction performance](doc:performance).
- Suited to tables that have a header row, where each row is a data element. Not suited to tables where the header is in the first column and the columns are data elements.

**Alternatives**

-   [Fixed Table](doc:fixed-table) or [Text Table](doc:text-table) methods.
- To extract complex tables, for example tables-inside-tables or tables with labeled rows and columns, see [Sections](doc:sections#examples).

**How it works**

For more information about how this method works, see [Notes ](doc:nlp-table#notes).

[**Parameters**](doc:nlp-table#parameters)
[**Examples**](doc:nlp-table#examples)
[**Notes**](doc:nlp-table#notes)

Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.


| key                    | value                             | description                                                  |
| :--------------------- | :-------------------------------- | :----------------------------------------------------------- |
| id (**required**)      | `nlpTable`                        | The Anchor parameter is optional for fields that use this method. If you specify an anchor, Sensible ignores it. |
| description            | string                            | A prompt that describes the table's subject matter as a whole. As part of finding the best-matching table, Sensible compares the table title, if present, to this description. For more details about how Sensible uses the description, see the Notes section. |
| columns (**required**) | array                             | An array of objects with the following parameters: <br/> -`id` (**required**): A user-friendly ID for the column in the extraction output. <br/>  -`description` (**required**):  A prompt that describes the data you want to extract from the column. This prompt can include instructions to reformat or filter the column's data. For example, provide prompts like `" transaction amount. return the absolute value"` or `"vehicle make (not model)"`.  <br/> -`type`: The table cell's type. For more information, see [types](doc:types). <br/>  -`isRequired` (default false): If true, Sensible omits a row if its cell is empty in this column, or if the contents don't match the value you specify in this column's Type parameter. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for *all* columns, even if the row had content under other columns. |
| promptIntroduction     |                                   | TODO                                                         |
| contextDescription     |                                   | TODO - this is the start of the commonNLPparameters          |
| pageHinting            |                                   | TODO                                                         |
| chunkCount             | number. default: `5`              | Configures context's size. For details about context and chunks, see the Notes section.<br/>The number of top-scoring chunks Sensible combines as context for the prompt it poses to a large-language model (LLM).<br/>Often, chunk count and chunk size are related. For example, if you know that your target data are spread over 7-10 pages, and occupy a small portion of those pages, you can specify a chunk count of 10 and a quarter- or half-page  chunk size. |
| chunkSize              | `0.5`, `1` default: `0.5`         | Configures context's size. For details about context and chunks, see the Notes section.<br/>The size of the chunks Sensible splits the document into, as a page fraction. For example, `0.5` specifies each chunk is half a page. <br/>Often, chunk count and chunk size are related. For example, if you know that the data you seek is contained in one cover page, you can set chunk size to 1 and a chunk count to 1. |
| chunkOverlapPercentage | `0`, `0.25`, `0.5` default: `0.5` | Configures context's size. For details about context and chunks, see the Notes section<br/>The extent to which chunks overlap, as a percentage of the chunks' height. For example, `0.5` specifies each chunk overlaps by half its height. <br/>Sensible recommends setting a non-zero overlap to avoid splitting data across chunks. Set overlap to 0 solely if you're confident that your document layout doesn't flow across page boundaries and you're using a one-page chunk size. |
| confidenceSignal       |                                   | TODO is it really supposed to be there                       |
|                        |                                   |                                                              |


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


1. To optimize performance, Sensible makes a list of the pages that are most likely to contain your target table. To make the list:
   - Sensible concatenates all your column descriptions with your overall table description. 
   - Sensible splits the document into equal-sized, overlapping chunks. 
   - Sensible scores your concatenated table descriptions against each chunk using the OpenAI Embeddings API.
   - Sensible gets a list of page numbers from the top-scoring chunks.
2. Sensible extracts all the tables on the pages most likely to contain your table, using an Amazon OCR provider. 

3. For each extracted table, Sensible extracts the table title, if present.  In detail:

   -  Sensible extracts lines contained in a rectangular region immediately above each table, since that region is likely to contain the table title. 
   -  The height of that region equals the line height of the first non-empty cell of the table + 0.1 inches, and the region extends down to the top boundary of the table.
   -  For information about how Sensible determines if lines are "contained" in a region, see [Region](doc:region).

4. Sensible scores each table by how well it matches the descriptions you provide of the data you want to extract. To create the score:

   - Sensible concatenates all your column descriptions with your overall table description. 

   - Sensible concatenates the first two rows of the table with the table title.

   - Sensible compares the two concatenations using the OpenAI Embeddings API. 

5. Sensible uses GPT-4 to restructure the best-scoring table based on your column descriptions and your overall table description. Sensible returns the restructured table.