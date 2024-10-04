---
title: "Postprocessor"
hidden: true
---

> ![img](https://ca.slack-edge.com/T017UPRAE94-U0794D6MU56-6a77bb7ffdda-48)

DevonDevon[Friday at 11:57 AM](https://sensiblehq.slack.com/archives/C0215T9K86P/p1726855039655909?thread_ts=1726764646.424009&cid=C0215T9K86P)

I'd be inclined to clarify in the object operator description description that it's possible for object to take in the result of some other rule, rather than strictly needing the key/value pairs spelled out outright. That may be an unlikely scenario, and it may make it more complicated to think about, so I can also see the argument for not explicitly bringing this up here. (the example is passing object a map rule, where the map results in the right shape: [["some string", some value] ...])Otherwise it all makes sense to me!

---



TODO: mention in docs that schema manipulated output doesn't show up in excel/csv exports since there's no way to map an arbitrary shema to a spreadsheet



Define your own custom output schema with a [JsonLogic](https://jsonlogic.com/)-based postprocessor.  For example, use a postprocessor if your app or API consumes data using a pre-existing schema, and you don't want to integrate using Sensible's output schema.

In detail, Sensible's `parsed_document` output schema represents extracted document data as follows:

```json
{
    "fields": [
        {
            "field_key": {
                "value": "value_1",
                "type": "string"
            }
        },
        {
            "field_key_2": {
                "value": "value_2",
                "type": "string"
            }
        }
    ]
}
```

Using a postprocessor, you can transform the extracted data into a custom schema,  for example:

```json
{
    "data": [
        {
            "custom_object": {
                "field_1": "value_1",
                "field_2": "value_2"
            }
        }
    ]
}
```

The postprocessor offers similar data manipulation to the  [Custom Computation](doc:custom-computation) computed field method, but offers greater flexibility because it supports more [extended jsonLogic operations](doc:draft-jsonlogic) and can output an arbitrary schema instead of outputting fields. 

Postprocessor output is available in the `postprocessorOutput` object in the API response and in the `postprocessor` tab in the JSON editor: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/postprocessed_tab.png) 

# Parameters


| key                 | value                                      | description                                                  |
| :------------------ | :----------------------------------------- | :----------------------------------------------------------- |
| type (**required**) | `jsonLogic`                                | Supports [JsonLogic](https://jsonlogic.com/) and  Sensible's extended JsonLogic [operations](doc:custom-computation#sensible-operations) |
| rule                | [JsonLogic](https://jsonlogic.com/) object | Define the custom schema using Sensible's [object](doc:custom-computation#object) operator and other . For more information, see the following section. |

### Object operator

Returns a JSON object that is an array of key/value pairs. You can nest object operations to build complex custom objects. 

```json
{
    "object": [
        [
         ["desiredKeyName", JsonLogic],
         ["desiredKeyName", JsonLogic]
        ]
    ]
}
```

As a simple example,  

```json
{
    "object": [
        [
            [
                "key_1",
                "string_constant"
            ],
            [
                "another_key",
                {
                    // where the extracted field `account_number` has value `12345`
                    "var": "account_number.value"
                }
            ]
        ]
    ]
}
```

returns:

```json
{
  "key_1": "string_constant",
  "another_key": 12345
}
```

TODO: describe that if the output shape of a jsonlgoic operation is a hash (right word?) ie like map, then you can just input that: 

```json
{
    "object": [
        [
         [ JsonLogic]
         
        ]
    ]
}
```



# Examples

## Example 1

**Config**

```json
{
  "postprocessor": {
    "type": "jsonLogic",
    "rule": {
       /* specify a schema that's a key-value array */
      "object": [
        [
          [
            "tax_summary",
            {
              /* nest an object inside an object   */
              "object": [
                [
                  [
                    /* define a key-value pair */
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
  "tax_summary": {
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

TODO:



#### Example 3

Lastly, here's a contrived but hopefully illustrative example where the value in the `"object"` array comes entirely from another rule:

```json
{
  "object": [
    {
      "map": [
        [{ "var": "name" }, { "var": "occupation" }],
        [{ "var": "value" }, "test value"]
      ]
    }
  ]
}
```

In this case, the `"map"` operation iterates over an array made up of the `name` and `occupation` fields from our document, which might look like this:

```json
[
  { "type": "string", "value": "some name" },
  { "type": "string", "value": "excellent rule writer" }
]
```

For each of the items in that array, the map will return back an array of the item's value and the string "test value", for a result that looks like this:

```json
[
  ["some name", "test value"],
  ["excellent rule editor", "test value"]
]
```

Then, when that gets run through the `"object"` operation, we get a final result of:

```json
{
  "some name": "test value",
  "excellent rule writer": "test value"
}
```
