---
title: "Postprocessor -- LLM JsonSchema"
hidden: true
---



TODOS:

- experiment with descriptions. what if you make a validating description and the raw data doesn fit it?

- Reword the existing preprocessor to xlink/relate to this one

- new LLM postprocessors category?

- TODO: ask an LLM how it interfaces with Json Schema (+ test its answers in real life w/ chat/claude). like what does it do when raw data fails json schema specs:

  - what are descriptions good for? 

  - what if an LLM can't recognize a speciied type compared to the source data? 
  - what does required do if the required extracted data isn't present?



# rough draft:

Define your own custom output [JSON schema](https://json-schema.org/learn) with an LLM-based postprocessor.  For example, use a postprocessor if your app or API consumes data using a pre-existing schema, and you don't want to integrate using Sensible's output schema.

In detail, Sensible's `parsed_document` API output schema represents extracted document data as typed [fields](doc:field-query-object):

```json
{
"parsed_document": {
        "contract_date": {
            "value": "2023-01-01T00:00:00.000Z",
            "type": "date"
        },
         "customer_name": {
                "type": "string",
                "value": "John Smith"
            }
}
```

Using a postprocessor, you can specify your target JSON schema, and the LLM takes your extracted data and transforms it.  For example, for the  extracted data:

``` json
{
    "eobs": [
        {
            "allowedAmountTotal": {
                "source": "119.00",
                "value": 119,
                "unit": "$",
                "type": "currency"
            },
            "claimNumber": {
                "type": "string",
                "value": "20231111"
            }
        }
    ]
}
```

You can specify:

```json
{
    "postprocessor": {
        "type": "jsonSchema",
        "schema": {
            "type": "object",
            "properties": {
                "allowedAmountTotal": {
                    "type": "integer"
                },
                "claimNumber": {
                    "type": "string",
                    "description": "must always be 8 digits"
                }
            },
            "required": [
                "claimNumber"
            ]
        }
    }
}
```

And the LLM transforms the extracted data to fit your specified JSON schema:

```json
{
    "postprocessorOutput": {
            "allowedAmountTotal": 119,
            "claimNumber": "20231111"
        
    }
}
```

This postprocessor is a low-code, indeterminate alternative to the JsonLogic postprocessor TODO LINK.

Postprocessor output is available in the `postprocessorOutput` object in the API response and in the **postprocessed** tab in the JSON editor: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/ui_postprocessed_tab.png) 

Postprocessor output isn't available in [Excel output](doc:excel-reference).

# Parameters


| key                   | value        | description                                                  |
| :-------------------- | :----------- | :----------------------------------------------------------- |
| type (**required**)   | `jsonSchema` | Specify the target [JSON schema](https://json-schema.org/learn) into which to transform the existing extracted JSON data TDODO word better |
| schema (**required**) | Json  object | Define a custom JSON schema for the LLM to transform your existing extracted data.  TODOs -- update w guidance abt what might happen when raw data fails the json schema specs. |



# Examples

## Example 1

**Config**

```json
{
  "postprocessor": {
    "type": "jsonLogic",
    "rule": {
      /* specify a custom object schema that's a key-value array */
      "eachKey": {
        "tax_summary": {
          /* nest an output object inside another output object with eachKey   */
          "eachKey": {
            /* define a key-value pair object.
            value for the `sent_by` key is a hardcoded string.*/
            "sent_by": "sensible-api",
            /* `state_info` object has two fields, 
            each of which is pulled from the parsed document */
            "state_info": {
              "eachKey": {
                /* the `var` operator gets a value from the parsed document. 
                   in this case, the `value` property from the `state_tax` field.*/
                "state_tax": {
                  "var": "state_tax.value"
                },
                "state_wages": {
                  "var": "state_wages.value"
                }
              }
            },
            /* `"wage_entries"` is an array. 
                the array values come entirely from the `map` operation, which returns the value for
                each item in the parsed document's `all_wage_fields` */
            "wage_entries": {
              "map": [
                {
                  "var": "all_wage_fields"
                },
                {
                  "var": "value"
                }
              ]
            }
          }
        }
      }
    }
  },
  "fields": [
    {
      "id": "state_wages",
      "anchor": {
        "match": "16 State"
      },
      "method": {
        "id": "label",
        "position": "below",
        "textAlignment": "hangingIndent"
      },
      "type": "currency"
    },
    {
      "id": "state_tax",
      "anchor": {
        "match": "17 State"
      },
      "method": {
        "id": "label",
        "position": "below",
        "textAlignment": "hangingIndent"
      },
      "type": "currency"
    },
    {
      "id": "all_wage_fields",
      "match": "all",
      "type": "currency",
      "method": {
        "id": "label",
        "position": "below",
        "textAlignment": "hangingIndent"
      },
      "anchor": {
        "match": {
          "type": "includes",
          "text": "wages"
        }
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/postprocessor.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/postprocessor.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
// POSTPROCESSED OUTPUT

{
  "tax_summary": {
    "sent_by": "sensible-api",
    "state_info": {
      "state_tax": 3438.56,
      "state_wages": 68780.48
    },
    "wage_entries": [
      69780.46,
      77447.24,
      22474.24,
      68780.48
    ]
  }
}

// PARSED DOCUMENT OUTPUT

{
  "state_wages": {
    "source": "68780.48",
    "value": 68780.48,
    "unit": "$",
    "type": "currency"
  },
  "state_tax": {
    "source": "3438.56",
    "value": 3438.56,
    "unit": "$",
    "type": "currency"
  },
  "all_wage_fields": [
    {
      "source": "69780.46",
      "value": 69780.46,
      "unit": "$",
      "type": "currency"
    },
    {
      "source": "77447.24",
      "value": 77447.24,
      "unit": "$",
      "type": "currency"
    },
    {
      "source": "22474.24",
      "value": 22474.24,
      "unit": "$",
      "type": "currency"
    },
    {
      "source": "68780.48",
      "value": 68780.48,
      "unit": "$",
      "type": "currency"
    }
  ]
}

```
