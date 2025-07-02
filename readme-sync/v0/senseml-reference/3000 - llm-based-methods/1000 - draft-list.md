---
title: "List"
hidden: true
---

This LLM-based method extracts repeating data in a document based on your description of the list’s overall contents and items. This method is suited to extracting data such as the work history on a resume, the vehicles on an auto insurance policy, or the line items on an invoice.

Use this method when your target data can appear either as a table or as another layout.

For advanced options, see [Advanced LLM prompt configuration](doc:prompt).

This method is an alternative to the [NLP Table](doc:nlp-table) method. 

#### Limitations

- Sensible can output lists of different maximum lengths depending on how you configure the LLM Engine and Single LLM Completion [parameters](doc:list#parameters). If the extracted list exceeds the limit, Sensible truncates the list.
- For highly complex repeating layouts, such as insurance loss run documents, use the [Sections](doc:sections) method.

#### Prompt tips

- The list description describes the overall contents for the list, while each property is a single description of an item that repeats in the list.
- For more information about how to write descriptions, or "prompts", see [Query Group](doc:query-group) extraction tips.

For information about how this method works, see [Notes](doc:list#notes).

[**Parameters**](doc:list#parameters)
[**Examples**](doc:list#examples)
[**Notes**](doc:list#notes)

Parameters
====

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method. 

**Note** You can configure some of the following parameters in both the [NLP](doc:nlp) preprocessor and in a field's method. If you configure both, the field's parameter overrides the NLP preprocessor's parameter.




| key                   | **value**                                               | description                                                  | interactions                                                 |
| :-------------------- | ------------------------------------------------------- | :----------------------------------------------------------- | ------------------------------------------------------------ |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         | ***FIND CONTEXT***                                           |                                                              |
| searchBySummarization | boolean<br/>or<br>`outline`, `page`<br/> default: false | Configure this to troubleshoot situations in which Sensible misidentifies the part of the document that contains the answers to your prompts. <br/>Setting `true` is equivalent to setting `page`.  <br/>This parameter is compatible with documents up to 1,280 pages long.<br/>When you set `page` or `outline`, Sensible uses content [summarization](https://www.sensible.so/blog/embeddings-vs-completions-only-rag) to locate context. Sensible:<br/>1.  prompts an LLM to summarize document content.  If you set `outline`, the LLM generates an outline of the document and summarizes each segment of the outline. If you set `page`, the LLM summarizes each page in the document.<br/>2. prompts a second LLM to return the page indices most relevant to your prompt based on the summaries.<br/>3. extracts the answers to your prompts from those pages' full text.<br/>When you set this to false, Sensible uses the default [approach](doc:prompt) to finding context. | If you set this parameter to a non-false value for a document 5 pages or under in length, Sensible submits the entire document as context, bypassing summarization.<br/> If you set this parameter to a non-false value for a document over 5 pages long, then Sensible sets the Chunk Count parameter to 5 and ignores any configured value.<br/>Note that the LLM Engine parameter doesn't configure the LLMs Sensible uses for locating context. |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |



Examples
====

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

​       

## Example: Extract data from other fields

The following example shows how to prompt an LLM to get repeating data about another field's output.

**Config**

```json
{
  "fields": [
    {
      /* define section group containing businesses */
      "id": "_businesses",
      "type": "sections",
      "range": {
        "anchor": {
          /* each business section starts with "Business #" */
          "match": {
            "type": "regex",
            "pattern": "Business [0-9]"
          }
        }
      },
      /* return each business as object containing names, sales, and selected classification */
      "fields": [
        {
          "id": "name",
          "anchor": "name",
          "method": {
            "id": "passthrough",
          }
        },
        {
          "id": "sales",
          "anchor": "sales",
          "method": {
            "id": "passthrough",
          }
        },
        { /* get checkbox status for 'individual' classification */
          "id": "individual",
          "type": "boolean",
          "method": {
            "id": "nearestCheckbox",
            "position": "left"
          },
          "anchor": "individual"
        },
        { /* get checkbox status for 'parternship' classification */
          "id": "partnernship",
          "type": "boolean",
          "method": {
            "id": "nearestCheckbox",
            "position": "left"
          },
          "anchor": "partnership"
        },
        { /* get checkbox status for 'llc' classification */
          "id": "llc",
          "type": "boolean",
          "method": {
            "id": "nearestCheckbox",
            "position": "left"
          },
          "anchor": "limited"
        },
        {
          /* return the selected classification for the business */
          "id": "selected_classification",
          "method": {
            "id": "pickValues",
            // select match:one for a group of radio buttons where the user can select a single item
            "match": "one",
            "source_ids": [
              "individual",
              "partnership",
              "llc"
            ]
          }
        }
      ]
    },
    /* prompt an LLM to find answers in the `_business` section output */
    {
      "id": "_business_sales",
      "type": "table",
      "method": {
        "id": "list",
        /* use _businesses ID as context for prompts */
        "source_ids": [
          "_businesses"
        ],
        "description": "business attributes",
        "properties": [
          {
            "id": "name",
            /* clean up source output, e.g., transform
            "Name: ACME co" to "AMCE co" */
            "description": "name of the business"
          },
          {
            /* compare sales rankings */
            "id": "sales_rank",
            "description": "relative rank in annual sales compared to other businesses in this context, i.e., return 1st, 2nd, 3rd"
          }
        ]
      }
    },
    {
      /* count instances of individual, parternship, and llc classified businesses */
      "id": "_business_classifications_frequency",
      "type": "table",
      "method": {
        "id": "list",
        "source_ids": [
          /* count instances in the _businesses output */
          "_businesses"
        ],
        "description": "business classifications",
        "properties": [
          {
            "id": "business classification",
            "description": "business classification, ie. llc or solo proprietor"
          },
          {
            "id": "frequency",
            "description": "how many times the business classification was selected"
       
          }
        ]
      }
    },
    /* zip output for more readable results */
    {
      "id": "business_sales",
      "method": {
        "id": "zip",
        "source_ids": [
          "_business_sales",
        ]
      }
    },
    {
      "id": "business_classifications_frequency",
      "method": {
        "id": "zip",
        "source_ids": [
          "_business_classifications_frequency",
        ]
      }
    },
    /* hide source fields for more readable results */
    {
      "id": "clean_output",
      "method": {
        "id": "suppressOutput",
        "source_ids": [
          "_businesses",
          "_business_classifications_frequency",
          "_business_sales"
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/list_source_ids.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/list_source_ids.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "business_sales": [
    {
      "name": {
        "value": "ACME co",
        "type": "string"
      },
      "sales_rank": {
        "value": "2nd",
        "type": "string"
      }
    },
    {
      "name": {
        "value": "Anyco LLM",
        "type": "string"
      },
      "sales_rank": {
        "value": "1st",
        "type": "string"
      }
    },
    {
      "name": {
        "value": "Keystone LLM",
        "type": "string"
      },
      "sales_rank": {
        "value": "3rd",
        "type": "string"
      }
    }
  ],
  "business_classifications_frequency": [
    {
      "business classification": {
        "value": "individual",
        "type": "string"
      },
      "frequency": {
        "value": "1",
        "type": "string"
      }
    },
    {
      "business classification": {
        "value": "llc",
        "type": "string"
      },
      "frequency": {
        "value": "2",
        "type": "string"
      }
    }
  ]
}
```

  

Notes
===

For an overview of how this method's default approach to locating context, see the following steps. 

For alternate approaches, see [Advanced LLM prompt configuration](doc:prompt#full-prompt).

### How it works by default


1. Sensible finds the chunks of the document that most likely contain your target data: 
     - Sensible splits the document into equal-sized chunks. 
     - Sensible scores each chunk by its similarity to the concatenated Description parameters.
     - Sensible selects a number of the top-scoring chunks:
       - If you specify Thorough or Long for the Mode parameter in the LLM Engine parameter, the Chunk Count parameter determines the number of top-scoring chunks Sensible selects to submit to the LLM.
       - If you specify Fast for the Mode parameter,  1. Sensible selects a number of top-scoring chunks as determined by the Chunk Count parameter. 2. To improve performance, Sensible removes chunks that are significantly less relevant from the list of top-scoring chunks. The number of chunks Sensible submits to the LLM can therefore be smaller than the number specified by the Chunk Count parameter.

2. Sensible batches the selected chunks into groups. The chunks in each page group can come from non-consecutive pages in the document.
     - If you set the Single LLM Completion parameter to True, then Sensible creates a single group that contains all the top-scoring chunks and sets a larger maximum token input limit for the single group (about 120k tokens) than it does for batched groups.

3. For each chunk group, Sensible submits a full prompt to an LLM. The full prompt includes the chunks as context, page-hinting data, and your prompts. The full prompt instructs the LLM to create a list formatted as a table, based on the context.
     - You can configure the LLM engine using the LLM Engine parameter. 

4. Sensible concatenates the results from the LLM for each page group and returns a list, formatted as a table.



