---
title: "List"
hidden: false
---
Extracts repeating data in a document, such as the work history or skills on a resume, the vehicles on an auto insurance policy, or the line items on an invoice. It can find these facts in paragraphs of free text or in more structured layouts, such as key/value pairs or tables. 

**Advantages**

- Low code. 
- Can reformat or filter extracted data based on your natural-language instructions. 
- Doesn't require an [anchor](doc:anchor).

**Limitations**

- If the target data span more than about a page and a half of the document, Sensible may miss data and truncate the list.
- Less suited to extracting from complex repeating layouts. For alternatives, see the following section. 

**Alternatives**

-   This method is an alternative to the [NLP Table](doc:nlp-table) method, since it can handle non-table layouts.
-   Use this method as a low-code alternative to the [Summarizer](doc:summarizer)  method.
-   For complex repeating layouts, use the [Sections](doc:sections) method.

**How it works**

For more information about how this method works, see [Notes ](doc:nlp-table#notes).

[**Parameters**](doc:list#parameters)
[**Examples**](doc:list#examples)
[**Notes**](doc:list#notes)

Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.


| key                        | value  | description                                                  |
| :------------------------- | :----- | :----------------------------------------------------------- |
| id (**required**)          | `list` | The Anchor parameter is optional for fields that use the Question method. If you specify an anchor, Sensible ignores it. |
| description (**required**) | string | A description of the list's subject matter as a whole.       |
| properties (**required**)  |        | An array of objects with the following parameters: <br/> -`id` (**required**): A user-friendly ID for the data in the extraction output. <br/>  -`description` (**required**):  A natural-language description of the list item that you want to extract. The description can include instructions to reformat or filter the data. For example, provide descriptions like `" transaction amount. return the absolute value"` or `"vehicle make (not model)"`.  <br/> -`type`: The list item's type. For more information, see [types](doc:types). |


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

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/list.pdf) |
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

- Sensible finds the chunks of the document that most likely contain your target data: 
  - Sensible concatenates all your property descriptions with your overall list description. 
  - Sensible splits the document into equal-sized, overlapping chunks. 
  - Sensible scores your concatenated list descriptions against each chunk using the OpenAI Embeddings API.
- Sensible selects a number of the top-scoring chunks and combines them. The chunks can be non-consecutive in the document.
- Sensible inputs the combined chunks to GPT-3 as one context, and instructs it to fill in the lists based on the context.