---
title: "List"
hidden: true
---
Extracts a table based on your natural-language description of the data you want to extract.

Use this method as a low-code alternative to layout-based Table methods, such as [Text Table](doc:text-table).

**Advantages**

- 

**Limitations**

- 

**Alternatives**

-   [NLP table] 
-   ?? question?
-  [Sections](doc:sections#examples).

**How it works**

For more information about how this method works, see [Notes ](doc:nlp-table#notes).

[**Parameters**](doc:nlp-table#parameters)  TODO THESE LINKS
[**Examples**](doc:nlp-table#examples)
[**Notes**](doc:nlp-table#notes)

Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.


| key                 | value  | description                                                  |
| :------------------ | :----- | :----------------------------------------------------------- |
| id (**required**)   | `list` | TODO true?? The Anchor parameter is optional for fields that use this method. If you don't specify an anchor, Sensible searches the whole document for the table.<br/>If you specify an anchor, Sensible ignores any tables before the anchor and starts searching for candidate tables after the anchor. In detail, Sensible ignores a table if 1. it occurs on a page previous to the page containing the anchor, or 2. if on the same page, it ignores the table if the table's lower boundary is higher on the page than the lower boundary of the anchor line. |
| description         | string | A description of the list's subject matter as a whole.       |
| TODO (**required**) | array  | An array of objects with the following parameters: <br/> -`id` (**required**): A user-friendly ID for the column in the extraction output. <br/>  -`description` (**required**):  A natural-language description of the data you want to extract from the column. The description can include instructions to reformat or filter the column's data. For example, provide descriptions like `" transaction amount. return the absolute value"` or `"vehicle make (not model)"`.  <br/> -`type`: The table cell's type. For more information, see [types](doc:types). <br/>  -`isRequired` (default false): If true, Sensible omits a row if its cell is empty in this column, or if the contents don't match the value you specify in this column's Type parameter. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for *all* columns, even if the row had content under other columns. |


Examples
====

The following example shows using the NLP Table method to extract information from tables about insured vehicles and insurance transactions.

**Config**

```json
{
  "fields": [
    {
      "id": "cars",
      "type": "table",
      "method": {
        "id": "list",
        "description": "cars info",
        "properties": [
          {
            "id": "brand",
            "description": "brand"
          },
          {
            "id": "make",
            "description": "make"
          },
          {
            "id": "model_year",
            "description": "model year"
          },
          {
            "id": "vin",
            "description": "vin"
          }
        ]
      }
    },
    {
      "id": "premiums",
      "type": "table",
      "method": {
        "id": "list",
        // insurance info
        "description": "insurance info for each vehicle",
        "properties": [
          /*{
            "id": "uninsured limit",
            "description": "uninsured motorist property damage limit"
          },
          {
            "id": "uninsured deductible",
            "description": "uninsured motorist property damage deductible"
          },
          */
          {
            "id": "uninsured motorist premium",
            "description": "uninsured motorist property damage premium"
          },
          {
            "id": "roadside assistance",
            "description": "roadside assistance premium"
          },
          {
            "id": "total coverage premium",
            "description": "total vehicle coverage premium"
          },
          {
            "id": "total 6 month policy premium",
            "description": "total 6 month policy premium"
          },
        ]
      }
      // todo: field for limits and deductibles for each vehicle??
    }
  ],
  "computed_fields": [
    {
      "id": "cars_zipped",
      "method": {
        "id": "zip",
        "source_ids": [
          "cars",
        ]
      }
    },
    {
      "id": "premiums_zipped",
      "method": {
        "id": "zip",
        "source_ids": [
          "premiums",
        ]
      }
    },
    {
      "id": "hide_fields",
      "method": {
        "id": "suppressOutput",
        "source_ids": [
          "cars",
          "premiums"
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/TODO.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/TODO.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "cars_zipped": [
    {
      "brand": {
        "value": "Mercedes-Benz",
        "type": "string"
      },
      "make": {
        "value": "S600",
        "type": "string"
      },
      "model_year": {
        "value": "2003",
        "type": "string"
      },
      "vin": {
        "value": "WDBNG76J73A347865",
        "type": "string"
      }
    },
    {
      "brand": {
        "value": "Subaru",
        "type": "string"
      },
      "make": {
        "value": "Forester",
        "type": "string"
      },
      "model_year": {
        "value": "2006",
        "type": "string"
      },
      "vin": {
        "value": "JF1SG67606H711473",
        "type": "string"
      }
    }
  ],
  "premiums_zipped": [
    {
      "uninsured motorist premium": {
        "value": "$8",
        "type": "string"
      },
      "roadside assistance": {
        "value": "10",
        "type": "string"
      },
      "total coverage premium": {
        "value": "$18",
        "type": "string"
      },
      "total 6 month policy premium": {
        "value": "$283.00",
        "type": "string"
      }
    },
    {
      "uninsured motorist premium": {
        "value": "$5",
        "type": "string"
      },
      "roadside assistance": {
        "value": "12",
        "type": "string"
      },
      "total coverage premium": {
        "value": "$17",
        "type": "string"
      },
      "total 6 month policy premium": {
        "value": "$283.00",
        "type": "string"
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
- Sensible selects a number of the top-scoring chunks and combines them. The chunks can be non-consecutive in the document. TODO: Question: is the number adjustable based on the number of matching 'sections"? TODO look in code
- Sensible inputs the combined chunks to GPT-3 as one context, and instructs it to fill in the lists based on the context.