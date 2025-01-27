---
title: "List"
hidden: true
---

TODO before publish:

- 
- any impact on 'prompt' global param table? I don't think you can set it at the NLP preprocessor level right? so no? (any other params in that table that don't show up in the NLP preprocessor also...?)
- IMPACT on notes for '/prompt', `list` and `query-group`. notes are getting ICKY!!! can they be consolidated or simplified?
- DONE add Computed Fields topic mention in addition to Query Group
- Could I have a concept topic called 'Extracted data transformation' and then point out from it to Computed Fields? would that be too hidden??
- **THIS TOPIC**:
- fix intro
- double check i want to use the example i'm using
- figure out interactions
- 


This LLM-based method extracts repeating data in a document based on your description of the list’s overall contents and each individual item. Data such as the work history or skills on a resume, the vehicles on an auto insurance policy, or the line items on an invoice are best suited for this method. 

**TODO: *When you configure the Source Fields parameter, you can chain LLM prompts together. In other words, you can extract data with one prompt, then apply further prompts to the extracted data.***

This method is an alternative to the [NLP Table](doc:nlp-table) method, when the data you want can appear either as a table or as another layout. The List method can find data in paragraphs of free text or in more structured layouts, such as key/value pairs or tables.  

#### Limitations

- Sensible can output lists of different maximum lengths depending on how you configure the LLM Engine and Single LLM Completion [parameters](doc:list#parameters). If the extracted list exceeds the limit, Sensible truncates the list.
- For highly complex repeating layouts, such as insurance loss run documents, use the [Sections](doc:sections) method.

#### Prompt tips

- The list description describes the overall contents for the list, while each property is a single description of an item that repeats in the list.
- You can use location hints to describe the target list's position in the document. For examples of location hints, see [Query Group](doc:query-group) extraction tips.
- For more information about how to write descriptions, or "prompts", see [Query Group](doc:query-group) extraction tips.
- For advanced options, see [Advanced LLM prompt configuration](doc:prompt).

For information about how this method works, see [Notes](doc:nlp-table#notes).

[**Parameters**](doc:list#parameters)
[**Examples**](doc:list#examples)
[**Notes**](doc:list#notes)

Parameters
====

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method. 

**Note** You can configure some of the following parameters in both the [NLP](doc:nlp) preprocessor and in a field's method. If you configure both, the field's parameter overrides the NLP preprocessor's parameter.




| key                        | **value**                                        | description                                                  | interactions                                                 |
| :------------------------- | ------------------------------------------------ | :----------------------------------------------------------- | ------------------------------------------------------------ |
| id (**required**)          | `list`                                           |                                                              |                                                              |
| description (**required**) | string                                           | A prompt describing the list's subject matter as a whole.    |                                                              |
| properties (**required**)  | object                                           | An array of objects with the following parameters: <br/> -`id` (**required**): A user-friendly ID for the data in the extraction output. <br/>  -`description` (**required**):  A prompt describing the list item that you want to extract. You can prompt the LLM to reformat or filter the data. For example, provide prompts like `" transaction amount. return the absolute value"` or `"vehicle make (not model)"`.  <br/> -`type`: The list item's type. For more information, see [types](doc:types). |                                                              |
| llmEngine                  | `fast`, `thorough`, `long`. <br/>default: `fast` | Specifies the LLM model to which Sensible submits the full prompt.<br/>- `fast`:  Sensible uses a faster LLM model (GPT-4o mini) . <br/>- `thorough`: Sensible uses a slower LLM model (GPT-4o)  Sensible can take several minutes to return the list.  Use this option if the Fast parameter results in incomplete extractions for multi-page lists.<br/>- `long`: Sensible uses a faster LLM model (GPT-4o mini). If you set this value, then Sensible can output lists extracted from up to 100 potentially nonconsecutive, 1-page source [chunks](doc:list#notes). Otherwise Sensible by default extracts from 20 1-page chunks. If the list in the document is longer than the number of source chunks, Sensible truncates the list.<br/>For more information, see [Notes](#notes). | If you specify Fast for this parameter, Sensible can submit a smaller number of chunks than specified by the Chunk Count parameter.<br/>If you specify Long for this parameter, Sensible sets the Chunk Count parameter to 100. |
| singleLLMCompletion        | boolean. default: false                          | If Sensible returns incomplete or duplicate results in a list that's under ~20 pages long, set this parameter to True to troubleshoot.<br/> If true, Sensible concatenates the top-scoring chunks into a single batch to send as context to the LLM, instead of batching calls to the LLM. By avoiding splitting context, you can avoid problems such as the LLM failing to recognize the end of one list and the start of another. See Notes for more information.<br/><br/>- The following limits apply:<br/>&nbsp;&nbsp; - If the extracted list exceeds the output limit for a single API response from an LLM engine (~16k tokens or ~20 pages for all supported LLM engines), Sensible truncates the list.<br/>&nbsp;&nbsp;- Rarely, Sensible fails to truncate a list at the token output limit and returns an error. This can happen if the source text in the [context](doc:list#notes) has a very small font size. To avoid this type of error, set this parameter to false. | Don't set this parameter to true if you set the LLM Engine parameter to Long. The Single LLM Completion parameter limits output to ~16k tokens, so it'll truncate longer lists. |
| source_ids                 | array of field IDs in the current config         | If specified, prompts an LLM to extract data from another field's output. For example, if you extract a field `_checking_transactions` and specify it in this parameter, then Sensible searches for the answers to `frequency of deposits?` and `frequency of withdrawals?` in `_checking_transactions`, rather than searching the whole document to locate the [context](doc:prompt#notes) context and answer. Note that the `_checking_transactions` field must precede the `transactions_frequencies` field in the fields array in this example. <br/><br/>Use this parameter to:<br/>-  reformat or otherwise transform the outputs of other fields. <br/> - narrow down the [context](doc:prompt#notes) for your prompts to a specific part of the document. <br/>-  troubleshoot or simplify complex prompts that aren't performing reliably. Break the prompt into several simpler parts, and chain them together using successive Source Ids in the fields array. <br/><br/><br/> | -llmEngine: long isn't so relevant<br/>singleLLMCompletion isn't so relevant?<br/>LET"S see, you'll probably be taking in a max of like 100 pages right? so yeah probably not so relevant?<br/>*If you configure this parameter, then in the query group:<br/>- Sensible doesn't support confidence signals.<br/> |
| searchBySummarization      |                                                  | For information about this parameter, see [Advanced LLM prompt configuration](doc:prompt#parameters) |                                                              |
| contextDescription         |                                                  | For information about this parameter, see [Advanced LLM prompt configuration](doc:prompt#parameters) |                                                              |
| pageHinting                |                                                  | For information about this parameter, see [Advanced LLM prompt configuration](doc:prompt#parameters) |                                                              |
| chunkCount                 |                                                  | For information about this parameter, see [Advanced LLM prompt configuration](doc:prompt#parameters) |                                                              |
| chunkSize                  |                                                  | For information about this parameter, see [Advanced LLM prompt configuration](doc:prompt#parameters) |                                                              |
| chunkOverlapPercentage     |                                                  | For information about this parameter, see [Advanced LLM prompt configuration](doc:prompt#parameters) |                                                              |
| pageRange                  |                                                  | For information about this parameter, see [Advanced LLM prompt configuration](doc:prompt#parameters). |                                                              |



Examples
====

## Example: Extract list

The following example shows using the List method to extract information from a menu about listed menu items.

**Config**

```json
{
  "fields": [
    {
      /* the id is a user-friendly name for the target list */
      "id": "dinners",
      "type": "table",
      "method": {
        "id": "list",
        /* overall description of list's contents */
        "description": "dinner special menu items",
        "properties": [
          {
            /* for each item in the list, provide a user-friendly ID and 
               description of the data you want to extract
               and optional instructions to filter or reformat the data */
            "id": "dinner_description",
            "description": "entree description"
          },
          /* optional: target data is a currency */
          {
            "id": "price",
            "type": "currency",
            "description": "dinner price"
          },
        ]
      }
    },
    {
      "id": "desserts",
      "type": "table",
      "method": {
        "id": "list",
        "description": "dessert special menu items",
        "properties": [
          {
            "id": "dessert_description",
            "description": "dessert description"
          },
          {
            "id": "price",
            "type":"currency",
            "description": "dessert price"
          },
        ]
      }
    },
    /* lists can span roughly a document page, if the list exceeds that,
      Sensible may truncate the extracted list */
    {
      "id": "wines",
      "type": "table",
      "method": {
        "id": "list",
        /* optional: try restricting the list to white wines,
           or try making a new list for liquors and their serving sizes */
        "description": "red wines and white wines (not other drinks such as beers or liquors)",
        "properties": [
          {
            "id": "wine_name",
            "description": "wine brand name"
          },
          {
            "id": "wine_type",
            "description": "wine varietal name (not brand), for example, return 'Red:cabernet savignon' or 'white:varietal not found'"
          },
          {
            "id": "wine_description",
            "description": "wine description"
          },
          {
            "id": "smallest_serving_price",
            "description": "smallest wine serving size and its dollar price, formatted like '6 oz: $11'"
          },
          {
            "id": "second_smallest_serving_price",
            "description": "second-smallest wine serving size and its dollar price, formatted like '6 oz: $11'"
          },
          {
            "id": "bottle_price",
            "type":"currency",
            "description": "price per bottle, in dollars"
          },
        ]
      }
    },
  ],
  "computed_fields": [
    /* optional: for cleaner output, zip each list */
    {
      "id": "dinners_zipped",
      "method": {
        "id": "zip",
        "source_ids": [
          "dinners",
        ]
      }
    },
    {
      "id": "desserts_zipped",
      "method": {
        "id": "zip",
        "source_ids": [
          "desserts",
        ]
      }
    },
    {
      "id": "wines_zipped",
      "method": {
        "id": "zip",
        "source_ids": [
          "wines",
        ]
      }
    },
    /* optional: for cleaner output, remove the source
       fields. */
    {
      "id": "hide_fields",
      "method": {
        "id": "suppressOutput",
        "source_ids": [
          "dinners",
          "desserts",
          "wines"
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/list.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/list.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "dinners_zipped": [
    {
      "dinner_description": {
        "value": "Grilled salmon with almond rice pilaf and spinach with pine nuts",
        "type": "string"
      },
      "price": {
        "source": "$45",
        "value": 45,
        "unit": "$",
        "type": "currency"
      }
    },
    {
      "dinner_description": {
        "value": "Seared beef with fingerling potatoes and asparagus",
        "type": "string"
      },
      "price": {
        "source": "$56",
        "value": 56,
        "unit": "$",
        "type": "currency"
      }
    }
  ],
  "desserts_zipped": [
    {
      "dessert_description": {
        "value": "Cannoli cake with candied lavender",
        "type": "string"
      },
      "price": {
        "source": "$14",
        "value": 14,
        "unit": "$",
        "type": "currency"
      }
    },
    {
      "dessert_description": {
        "value": "Creme brulee",
        "type": "string"
      },
      "price": {
        "source": "$13",
        "value": 13,
        "unit": "$",
        "type": "currency"
      }
    }
  ],
  "wines_zipped": [
    {
      "wine_name": {
        "value": "House white",
        "type": "string"
      },
      "wine_type": {
        "value": "white:varietal not found",
        "type": "string"
      },
      "wine_description": {
        "value": "Dry with citrus notes reminiscent of grapefruit",
        "type": "string"
      },
      "smallest_serving_price": {
        "value": "6 oz: $10",
        "type": "string"
      },
      "second_smallest_serving_price": {
        "value": "9 oz: $16",
        "type": "string"
      },
      "bottle_price": {
        "source": "32",
        "value": 32,
        "unit": "$",
        "type": "currency"
      }
    },
    {
      "wine_name": {
        "value": "Barone Ventoura",
        "type": "string"
      },
      "wine_type": {
        "value": "white:varietal not found",
        "type": "string"
      },
      "wine_description": {
        "value": "Subtle honey notes with floral aromas",
        "type": "string"
      },
      "smallest_serving_price": {
        "value": "6 oz: $12",
        "type": "string"
      },
      "second_smallest_serving_price": {
        "value": "9 oz: $18",
        "type": "string"
      },
      "bottle_price": {
        "source": "40",
        "value": 40,
        "unit": "$",
        "type": "currency"
      }
    },
    {
      "wine_name": {
        "value": "Val Feuillatte",
        "type": "string"
      },
      "wine_type": {
        "value": "white:varietal not found",
        "type": "string"
      },
      "wine_description": {
        "value": "Bold, distinctive spice notes",
        "type": "string"
      },
      "smallest_serving_price": null,
      "second_smallest_serving_price": null,
      "bottle_price": {
        "source": "65",
        "value": 65,
        "unit": "$",
        "type": "currency"
      }
    },
    {
      "wine_name": {
        "value": "House red",
        "type": "string"
      },
      "wine_type": {
        "value": "red:varietal not found",
        "type": "string"
      },
      "wine_description": {
        "value": "A satisfying blend",
        "type": "string"
      },
      "smallest_serving_price": {
        "value": "6 oz: $11",
        "type": "string"
      },
      "second_smallest_serving_price": {
        "value": "9 oz: $17",
        "type": "string"
      },
      "bottle_price": {
        "source": "33",
        "value": 33,
        "unit": "$",
        "type": "currency"
      }
    },
    {
      "wine_name": {
        "value": "Wrath cabernet sauvignon",
        "type": "string"
      },
      "wine_type": {
        "value": "red:cabernet sauvignon",
        "type": "string"
      },
      "wine_description": {
        "value": "Bold with oak notes",
        "type": "string"
      },
      "smallest_serving_price": null,
      "second_smallest_serving_price": null,
      "bottle_price": {
        "source": "62",
        "value": 62,
        "unit": "$",
        "type": "currency"
      }
    },
    {
      "wine_name": {
        "value": "Turbell Estate Pinot noir",
        "type": "string"
      },
      "wine_type": {
        "value": "red:pinot noir",
        "type": "string"
      },
      "wine_description": {
        "value": "Mellow with dark chocolate notes",
        "type": "string"
      },
      "smallest_serving_price": {
        "value": "6 oz: $13",
        "type": "string"
      },
      "second_smallest_serving_price": {
        "value": "9 oz: $18",
        "type": "string"
      },
      "bottle_price": {
        "source": "35",
        "value": 35,
        "unit": "$",
        "type": "currency"
      }
    },
    {
      "wine_name": {
        "value": "Chappellet Shiraz",
        "type": "string"
      },
      "wine_type": {
        "value": "red:shiraz",
        "type": "string"
      },
      "wine_description": {
        "value": "Complex and subtle",
        "type": "string"
      },
      "smallest_serving_price": null,
      "second_smallest_serving_price": null,
      "bottle_price": {
        "source": "72",
        "value": 72,
        "unit": "$",
        "type": "currency"
      }
    }
  ]
}
```



Notes
===

For an overview of how this method works when `"searchBySummarization": false`, see the following steps:

1. Sensible finds the chunks of the document that most likely contain your target data: 

     - Sensible concatenates all your property descriptions with your overall list description. 

     - Sensible splits the document into equal-sized chunks. 

     - Sensible scores your concatenated list descriptions against each chunk.


2. Sensible selects a number of the top-scoring chunks: 
   1. If you specify Thorough or Long for the LLM Engine parameter, the Chunk Count parameter determines the number of top-scoring chunks Sensible selects to submit to the LLM.
   2. If you specify Fast for the LLM Engine parameter,  1. Sensible selects a number of top-scoring chunks as determined by the Chunk Count parameter. 2. To improve performance, Sensible removes chunks that are significantly less relevant from the list of top-scoring chunks. The number of chunks Sensible sumbits to the LLM can therefore be smaller than the number specified by the Chunk Count parameter.
3. To avoid large language model (LLM)'s input token limits, Sensible batches the chunks into groups. The chunks in each page group can come from non-consecutive pages in the document. If you set the Single LLM Completion parameter to True, then Sensible creates a single group that contains all the top-scoring chunks and sets a larger maximum token input limit for the single group (about 120k tokens) than it does for batched groups.
4. For each chunk group, Sensible submits a full prompt to the LLM that includes the chunks as context, page-hinting data, and your prompts. For information about the LLM model, see the LLM Engine parameter. For more information about the full prompt, see [Advanced LLM prompt configuration](doc:prompt). The full prompt instructs the LLM to create a list formatted as a table, based on the context.
5. Sensible concatenates the results from the LLM for each page group and returns a list, formatted as a table.
