---
title: "NLP table"
hidden: false
---
Extracts a table based on your natural-language description of the data you want to extract. This method can extract tables that span multiple pages. This method is suited to tables that have a header row, where each row is a data element. Not suited to tables where the header is in the first column and the columns are data elements, or to other complex table layouts. For alternatives to this method, see [Table methods](doc:table-methods). 

#### Prompt Tips

- Extract all columns to get the best results. If you describe only a few of the columns, your results may be less accurate.

- Use the table titles or table column headers in the document as descriptions.

- For more information about how to write descriptions, or "prompts", see [Query Group](doc:query-group).

- For advanced options, see [Advanced LLM prompt configuration](doc:prompt).

For information about how this method works, see [Notes](doc:nlp-table#notes).

[**Parameters**](doc:nlp-table#parameters)
[**Examples**](doc:nlp-table#examples)
[**Notes**](doc:nlp-table#notes)

Parameters
====

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

**Note** You can configure some of the following parameters in both the [NLP](doc:nlp) preprocessor and in a field's method. If you configure both, the field's parameter overrides the NLP preprocessor's parameter.


| key                             | value                                                        | description                                                  | interactions                                                 |
| :------------------------------ | :----------------------------------------------------------- | :----------------------------------------------------------- | ------------------------------------------------------------ |
| id (**required**)               | `nlpTable`                                                   |                                                              |                                                              |
| description                     | string                                                       | A prompt that describes the table's subject matter as a whole. As part of finding the best-matching table, Sensible compares the table title, if present, to this description. For more details about how Sensible uses the description, see the Notes section. |                                                              |
| columns (**required**)          | array                                                        | An array of objects with the following parameters: <br/> -`id` (**required**): A user-friendly ID for the column in the extraction output. <br/>  -`description` (**required**):  A prompt that describes the data you want to extract from the column. This prompt can include instructions to reformat or filter the column's data. For example, provide prompts like `" transaction amount. return the absolute value"` or `"vehicle make (not model)"`.  <br/> -`type`: The table cell's type. For more information, see [types](doc:types). <br/>  -`isRequired` (default false): If true, Sensible omits a row if its cell is empty in this column, or if the contents don't match the value you specify in this column's Type parameter. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for *all* columns, even if the row had content under other columns. |                                                              |
|                                 |                                                              | ***TABLE RECOGNITION***                                      |                                                              |
| rewriteTable                    | Boolean. default: true | If true, you can use the column descriptions to prompt the LLM to split or merge columns or otherwise restructure the table.<br/><br/>Configure this to false to improve performance, to avoid LLM token overflow errors caused by tables that exceed 4,000 [tokens](https://platform.openai.com/tokenizer), or to troubleshoot an incomplete table extraction.<br/>If false, Sensible returns the table body unchanged from the OCR extraction, and the only change you can make is to rename the column headings using the columns' ID parameters. | If you set this parameter to true, Sensible overrides the LLM Engine parameter. For more information, see the Notes section. |
| pageSpanThreshold               | object                                                       | Configure the Page Span Threshold parameter to troubleshoot automatic multi-page table recognition. <br/>By default, Sensible detects multi-page tables by checking if the table is near the top or bottom of the page. If it is, Sensible searches previous and succeeding pages for continuations of the table. This default behavior fails when intervening, non-table text introduces a large vertical space between a multi-page table and the top or bottom of a page, bumping the table toward the center of the page. Examples of non-table text include footnotes and text box inserts. To allow for such large spaces, configure the following parameters:<br/>- `top`: number. default: 0.4. Sensible searches the previous page for a continuation of a multi-page table if the table starts in the top 40% of the page. Change the percent using this parameter.<br/>-  `bottom`: number. default: 0.2. Sensible searches the next page for a continuation of a multi-page table if the table ends in the bottom 20% of the page. Change the percent using this parameter.<br/>Sensible continues merging the multi-page table until the Page Span Threshold conditions are no longer met, or until Sensible encounters LLM token limits. |                                                              |
| detectTableStructureOnly        | boolean. default: false                                      | Set this parameter to true to troubleshoot optional character recognition (OCR) in a table. If true, Sensible bypasses the text output by the table recognition OCR provider. Sensible instead recognizes the table's text using the  [OCR engine](doc:ocr-engine) specified by your document type, or by using text embedded in the document file if present. For an example, see [Example: Troubleshoot Table OCR](doc:fixed-table#example-troubleshoot-table-ocr).<br/>If `"detectTableStructureOnly": true` causes incorrect [line sorting](doc:lines#line-sorting), set `annotateSuperscriptAndSubscript": true` to correct the line sorting.<br/> |                                                              |
| annotateSuperscriptAndSubscript | boolean. default: false                                      | Set to true only if the Detect Table Structure Only parameter is set to true. When true:<br/>-  Sensible annotates subscript and superscript text in the table with `[^...]` and `[_...]`, respectively. This parameter doesn't support annotating text in multi-line cells. |                                                              |
|                                 |                                                              | ***TROUBLESHOOT PROMPT***                                    |                                                              |
| llmEngine                       | object                                                       | Configures the LLM engine Sensible uses to answer your prompts.<br/>Configure this parameter to troubleshoot situations in which Sensible correctly identifies the part of the document that contains the answers to your prompts, but the LLM's answer contains problems. For example, Sensible returns an LLM error because the answer isn't properly formatted, or the LLM doesn't follow instructions in your prompt.<br/>Contains a `provider` parameter with the following options:<br/>- If set to `open-ai` (default), Sensible uses OpenAI's GPT-4o.<br/> - If set to `anthropic`, Sensible uses Anthropic's Claude 3 Haiku. |                                                              |
|                                 |                                                              | ***FIND CONTEXT***                                           |                                                              |
| pageHinting                     | boolean. default: true                                       | Includes or removes page metadata for each chunk from the full prompt Sensible inputs to an LLM.<br/>If set to true, then you can add location information to a prompt to narrow down the context's location. For example:<br/>**Location relative to page number and position on page**<br/>- "address in the top left of the first page of the document"<br/> - "What is the medical paid value on the last claim of the second page?"<br/>**Location relative to content in document**<br/>- "total amount in the expense table" <br/>- "phone number after section 2"<br/><br/>Set this to false if page numbers don't add useful information. For example, if your PDF converter automatically applied page numbers to scanned ID cards, set this parameter to false to ignore the page numbers, since their relationship to the cards' text is arbitrary.<br/> |                                                              |
| pageRange                       | object                                                       | Configures the possible page range for finding the context in the document.<br/>If specified, Sensible creates chunks in the page range and ignores other pages. For example, use this parameter to improve performance, or to avoid extracting unwanted data if your prompt has multiple candidate answers.<br/><br/>Contains the following parameters: <br/>`startPage`:  Zero-based index of the page at which Sensible starts creating chunks (inclusive). <br/>`endPage`: Zero-based index of the page at which Sensible stops creating chunks (exclusive). | Sensible ignores this parameter when searching for a field's [anchor](doc:anchor). If you want to exclude the field's anchor using a page range, use the [Page Range](doc:page-range) preprocessor instead. |
|                                 |                                                              | ***CONFIGURE CONTEXT SIZE***                                 |                                                              |
| chunkCount                      | number. default: 5                                           | The number of top-scoring chunks Sensible combines as context as part of the full prompt it submits to an LLM. <br/>Often, chunk count and chunk size are related. For example, if you know that your target data are spread over 7-10 pages, and occupy a small portion of those pages, you can specify a chunk count of 10 and a half-page chunk size. |                                                              |
| chunkSize                       | `0.5`, `1` <br/>default: 0.5                                 | The size of the chunks Sensible splits the document into, as a page fraction. For example, `0.5` specifies each chunk is half a page. <br/>Often, chunk count and chunk size are related. For example, if you know that your target data is contained in one cover page, you can set chunk size to 1 and a chunk count to 1. |                                                              |
| chunkOverlapPercentage          | `0`, `0.25`, `0.5` <br/>default: 0.5                         | The extent to which chunks overlap, as a percentage of the chunks' height. For example, `0.5` specifies each chunk overlaps by half its height.  <br/>Sensible recommends setting a non-zero overlap to avoid splitting data across chunks. Set overlap to 0 solely if you're confident that your document layout doesn't flow across page boundaries and you're using a one-page chunk size. |                                                              |
|                                 |                                                              | ***MISCELLANEOUS***                                          |                                                              |
| contextDescription              |                                                              | Configures context's metadata by overwriting the default context description.<br/>For example:<br/>\- `The below context is an excerpt from a scanned index card that contains botanical information about a single plant species, including phenology information.`<br/>\- `The below context is an excerpt from an email. Assume the sender is always an automated system from an insurance broker.` |                                                              |



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
  "insured_vehicles_table": {
    "columns": [
      {
        "id": "manufacturer",
        "values": [
          {
            "value": "Toyota",
            "type": "string"
          },
          {
            "value": "Honda",
            "type": "string"
          },
          {
            "value": "Volkswagen",
            "type": "string"
          }
        ]
      },
      {
        "id": "year",
        "values": [
          {
            "value": "2010",
            "type": "string"
          },
          {
            "value": "2015",
            "type": "string"
          },
          {
            "value": "2020",
            "type": "string"
          }
        ]
      }
    ],
    "title": {
      "type": "string",
      "value": "Insured vehicles"
    }
  },
  "transactions_table": {
    "columns": [
      {
        "id": "transaction_date",
        "values": [
          {
            "value": "02/19",
            "type": "string"
          },
          {
            "value": "01/03",
            "type": "string"
          }
        ]
      },
      {
        "id": "transaction_description",
        "values": [
          {
            "value": "Paid premium",
            "type": "string"
          },
          {
            "value": "Amount awarded for claim #123456789",
            "type": "string"
          }
        ]
      },
      {
        "id": "amount",
        "values": [
          {
            "source": "-$100.01",
            "value": -100.01,
            "unit": "$",
            "type": "currency"
          },
          {
            "source": "$200.67",
            "value": 200.67,
            "unit": "$",
            "type": "currency"
          }
        ]
      }
    ],
    "title": {
      "type": "string",
      "value": "Transactions for insurance account xxx4567"
    }
  },
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
        "value": "Volkswagen",
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
        "value": "02/19",
        "type": "string"
      },
      "transaction_description": {
        "value": "Paid premium",
        "type": "string"
      },
      "amount": {
        "source": "-$100.01",
        "value": -100.01,
        "unit": "$",
        "type": "currency"
      }
    },
    {
      "transaction_date": {
        "value": "01/03",
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


1. Sensible makes a list of the pages that are most likely to contain your target table. To make the list:
   - Sensible concatenates all your column descriptions with your overall table description. 
   - Sensible splits the document into equal-sized, overlapping chunks. 
   - Sensible scores your concatenated table descriptions against each chunk using a nonconfigurable OpenAI Embeddings API.
   - Sensible gets a list of page numbers from the top-scoring chunks.
2. Sensible extracts all the tables on the pages most likely to contain your table, using the [OCR engine](doc:ocr-engine) specified by the document type. Sensible supports multi-page tables.
3. Sensible scores each table by how well it matches the descriptions you provide of the data you want to extract. To create the score:

   - Sensible concatenates all your column descriptions with your overall table description. 

   - Sensible concatenates a number of the first rows of the table with the table title.  Sensible uses the table title extracted by the table OCR provider, or falls back to using the text in a region above the table if the OCR provider doesn't find a title.

   - Sensible compares the two concatenations using a nonconfigurable OpenAI Embeddings API. 
4. Sensible creates a full prompt for the LLM that includes the top-scoring table, page hinting data, and your prompts. For more information about the full prompt, see [Advanced LLM prompt configuration](doc:prompt#full-prompt). 

   1. If `rewriteTable:false`, the full prompt instructs the LLM (as specified by the LLM Engine parameter) to rewrite or restructure the best-scoring table based on your column descriptions and your overall table description. 
   2. If `rewriteTable: false`, the full prompt instructs the LLM (GPT-4) to rewrite the column headings' IDs, but doesn't otherwise restructure the table.
5. Sensible returns the restructured table.