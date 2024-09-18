---
title: "postprocessor n object operator"
hidden: true
---

Define your own custom output schema with a [JsonLogic](https://jsonlogic.com/)-based postprocessor.  For example, use a postprocessor if your app or API consumes data using a pre-existing schema, and you don't want integrate using Sensible's output schema.

In detail, Sensible's `parsed_document` output schema represents extracted document data as follows:

```json
"fields":
[
  {
   "field_key":
    {
     "value": "value_1",
     "type": "string"
    }
  },
    {
   "field_key_2":
    {
     "value": "value_2",
     "type": "string"
    }
  }
]
```

Using a postprocessor, you can transform the extracted data into a custom schema,  for example:

```json
"data":
[
    "custom_object": 
     {
      "field_1": "value_1",
      "field_2": "value_2"
    }
]
```

The postprocessor offers similar data manipulation to the  [Custom Computation](doc:custom-computation) computed field method, but offers greater flexibility because it can output an arbitrary schema instead of a `parsed_document` schema. 

Postprocessor output is available in the `postprocessorOutput` array in the API response and in the `postprocessor` tab in the JSON editor: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/postprocessed_tab.png) 

# Postprocessor types

| Postprocessor | Notes                                  |
| ------------- | -------------------------------------- |
| **JsonLogic** | Define a custom schema using JsonLogic |

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                 | value                                      | description                                                  |
| :------------------ | :----------------------------------------- | :----------------------------------------------------------- |
| type (**required**) | `jsonLogic`                                |                                                              |
| rule                | [JsonLogic](https://jsonlogic.com/) object | Define the custom schema using JsonLogic, including Sensible's [object](doc:custom-computation#object) operator. |

## Examples

## Example 1

**Config**

```json
{
  "postprocessor": {
    "type": "jsonLogic",
    "rule": {
      "object": [
        [
          [
            "data",
            {
              /* specify a schema that's a key-value array  */
              "object": [
                [
                  [
                    "sent_by",
                    /* value for the `sent_by` key is a hardcoded string. */
                    "sensible-api"
                  ],
                  [
                    /* `tax_info` object has two fields, each of which is pulled from the 
                    parsed document */
                    "tax_info",
                    {
                      "object": [
                        [
                          [
                            /* the `var` operator gets a value from the parsed document. 
                        in this case, the `value` property from the `state_tax` field.*/
                            "state_tax",
                            {
                              "var": "state_tax.value"
                            }
                          ],
                          [
                            "state_wages",
                            {
                              "var": "state_wages.value"
                            }
                          ]
                        ]
                      ]
                    }
                  ],
                  [
                    /* `"wage_entries"` is an array. 
                    the array values come entirely from the `map` operation, which returns the value for
                    each item in the parsed document's `all_wage_fields` */
                    "wage_entries",
                    {
                      "map": [
                        {
                          "var": "all_wage_fields"
                        },
                        {
                          "var": "value"
                        }
                      ]
                    }
                  ]
                ]
              ]
            }
          ]
        ]
      ]
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
  "data": {
    "sent_by": "sensible-api",
    "tax_info": {
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





