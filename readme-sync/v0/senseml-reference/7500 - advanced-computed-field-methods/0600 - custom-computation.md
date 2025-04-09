---
title: "Custom computation"
hidden: false
---

Define your own [computed field method](doc:computed-field-methods) using [JsonLogic](doc:jsonlogic). For example, return the sum of two fields, map arrays, or return a boolean indicating if a field's output is non-null. Returns one field.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value                             | description                                                  |
| :----------------------- | :-------------------------------- | :----------------------------------------------------------- |
| id (**required**)        | `customComputation`               | - This method has access to the  `parsed_document` object at [verbosity](doc:verbosity) = 0. <br/> - This method doesn't output [Sensible types](doc:types).<sup>1</sup> It outputs `string, number, boolean, null` , or an array of those. For example, adding two currencies results in a number.<br/> - This method returns null if you attempt to reference a variable that Sensible can't find in the `parsed_document`.<br/>- This method returns null if calculations include a null. For example, `5 + null field = null`.  If you instead want `5 + null field = 5`, then implement logic to replace nulls with zeros. For an example, see [Example 1](doc:custom-computation#example-1). |
| jsonLogic (**required**) | JsonLogic object | Transforms the output of one or more [Field objects](https://docs.sensible.so/docs/field-query-object) using [JsonLogic operations](doc:jsonlogic).<br/>Outputs one field. |

<sup>1</sup> For an exception to the restricted types that Custom Computation outputs, see the Notes section. 

Examples
====

## Example 1

The following example shows  defining custom computed fields.

**Config**

```json
{
  "fields": [
    {
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            "id": "prop_limit_a",
            "description": "property damage limit in first table (insurer A)",
            "type": "currency"
          },
          {
            "id": "injury_limit_a",
            "description": "bodily injury limit in first table (insurer A)",
            "type": "currency"
          },
          {
            "id": "vehicle_vin_a",
            "description": "vehicle vin for insurer A",
            "type": "number"
          }
        ]
      }
    },
    {
      "id": "table_b",
      "method": {
        "id": "nlpTable",
        "description": "table for insurer B describing insurance limits",
        "columns": [
          {
            "id": "make_and_model",
            "description": "make and model",
            "type": "string"
          },
          {
            "id": "vehicle_vin",
            "description": "vehicle vin",
            "type": "string"
          },
          {
            "id": "policy_effective_date",
            "description": "policy effective date",
            "type": "string"
          },
          {
            "id": "limits",
            "description": "limits",
            "type": "string"
          },
          {
            "id": "dollar_amount_per_limit",
            "description": "dollar amount per limit",
            "type": "string"
          }
        ]
      }
    },
  ],
  "computed_fields": [
    /* check an extracted field is non-null */
    {
      "id": "prop_limit_exists",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "exists": [
            {
              "var": "prop_limit_a.value"
            }
          ]
        }
      }
    },
    /* check a field's value matches a regex */
    {
      "id": "injury_limit_matches_regex",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "match": [
            {
              "var": "injury_limit_a.value"
            },
            "^\\w+$"
          ]
        }
      }
    },
    /* redact the vehicle's VIN using regex replace operation */
    {
      "id": "replace_regex",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "replace": {
            "source": {
              "var": "vehicle_vin_a.value"
            },
            "find_regex": "(\\d{4})(\\d{4})",
            "replace": "xxxx$2",
            "flags": "g"
          }
        }
      }
    },
    /* modify value using JsonLogic in replace operation */
    {
      "id": "replace_var",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "replace": {
            "source": {
              "var": "injury_limit_a.value"
            },
            "find": {
              "var": "injury_limit_a.value"
            },
            "replace": {
              "+": [
                {
                  "var": "prop_limit_a.value"
                },
                200
              ]
            }
          }
        }
      }
    },
    /* perform addition on an extracted field's value */
    {
      "id": "prop_limit_addition",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "+": [
            {
              /* check that prop_limit_a.value is non-null
                 if it's null, replace it with zero.
                 otherwise the operation returns null */
              "if": [
                {
                  "var": "prop_limit_a.value"
                },
                {
                  "var": "prop_limit_a.value"
                },
                0
              ]
            },
            200
          ]
        }
      }
    },
    {
      /* modify a table's column using map */
      "id": "map_table",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          /* perform map operation on each limit in the 'limits' column */
          "map": [
            {
              /* the array to be mapped: the fourth column, titled "limits", in a table
              / Note Sensible uses dot notation to access array elements,
                for example, insurer_b_table.columns.3.values
              */
              "var": "table_b.columns.3.values"
            },
            {
              /* Note it's "cat" for strings, "+" for numbers */
              "cat": [
                {
                  "var": "value"
                },
                // append the word "LIMIT" to each limit description
                " LIMIT"
              ]
            }
          ]
        }
      }
    },
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/add_computed_fields_1.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/add_computed_fields.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "prop_limit_a": {
    "source": "$5,000",
    "value": 5000,
    "unit": "$",
    "type": "currency"
  },
  "injury_limit_a": {
    "source": "$3,000",
    "value": 3000,
    "unit": "$",
    "type": "currency"
  },
  "vehicle_vin_a": {
    "source": "12345678",
    "value": 12345678,
    "type": "number"
  },
  "table_b": {
    "columns": [
      {
        "id": "make_and_model",
        "values": [
          {
            "value": "Honda Accord",
            "type": "string"
          },
          {
            "value": "Honda Accord",
            "type": "string"
          },
          {
            "value": "Honda Accord",
            "type": "string"
          }
        ]
      },
      {
        "id": "vehicle_vin",
        "values": [
          {
            "value": "92343156",
            "type": "string"
          },
          {
            "value": "92343156",
            "type": "string"
          },
          {
            "value": "92343156",
            "type": "string"
          }
        ]
      },
      {
        "id": "policy_effective_date",
        "values": [
          {
            "value": "12/19/20",
            "type": "string"
          },
          {
            "value": "12/19/20",
            "type": "string"
          },
          {
            "value": "12/19/20",
            "type": "string"
          }
        ]
      },
      {
        "id": "limits",
        "values": [
          {
            "value": "Property damage*",
            "type": "string"
          },
          {
            "value": "Bodily injury**",
            "type": "string"
          },
          {
            "value": "Auto only*",
            "type": "string"
          }
        ]
      },
      {
        "id": "dollar_amount_per_limit",
        "values": [
          {
            "value": "$6,000",
            "type": "string"
          },
          {
            "value": "$4,000",
            "type": "string"
          },
          {
            "value": "$1,000",
            "type": "string"
          }
        ]
      }
    ],
    "title": {
      "type": "string",
      "value": "Insurer B"
    },
    "footer": {
      "type": "string",
      "value": "* per person ** per accident"
    }
  },
  "prop_limit_exists": {
    "value": true,
    "type": "boolean"
  },
  "injury_limit_matches_regex": {
    "value": true,
    "type": "boolean"
  },
  "replace_regex": {
    "value": "xxxx5678",
    "type": "string"
  },
  "replace_var": {
    "value": "5200",
    "type": "string"
  },
  "prop_limit_addition": {
    "value": 5200,
    "type": "number"
  },
  "map_table": [
    {
      "value": "Property damage* LIMIT",
      "type": "string"
    },
    {
      "value": "Bodily injury** LIMIT",
      "type": "string"
    },
    {
      "value": "Auto only* LIMIT",
      "type": "string"
    }
  ]
}
```

## Example 2

The following example shows using the Custom Computation method to perform the following operations on data extracted from an claims loss run insurance document:

- Get the total number of claims listed in the document

- Redact the claim IDs

- Sum up the incurred cost for all claims listed

**Config**

```json
{
  "fields": [
    {
      /* use sections to extract repeating data, 
      in this case, claims */
      "id": "claims_sections",
      "type": "sections",
      "range": {
        /* starting line of each claim is "claim number" */
        "anchor": "claim id",
        /* ending line of each claim is "incurred" */
        "stop": "incurred"
      },
      "fields": [
        {
          "id": "raw_claim_id",
          "anchor": "claim id",
          "method": {
            /* target data to extract is a single line 
            to right of anchor line ("claim number") */
            "id": "label",
            "position": "right"
          }
        },
        {
          "id": "incurred_amount",
          "type": "currency",
          "anchor": "incurred",
          "method": {
            /* target data to extract is a single line 
            to right of anchor line ("incurred") */
            "id": "label",
            "position": "right",
          }
        },
        {
          "id": "redacted_id",
          "method": {
            /* use JsonLogic to perform custom
            data transformation */
            "id": "customComputation",
            "jsonLogic": {
              /* the Replace method extends jsonLogic
                 to enable regex find/replace operations  */
              "replace": {
                "source": {
                  /* replace 1st 3 digits in each ID with '***' 
                  to redact it */
                  "var": "raw_claim_id.value"
                },
                "find_regex": ".*(\\d{3})(\\d{7}).*",
                "replace": "***$2",
              }
            }
          }
        },
        /* hide unredacted IDs from output */
        {
          "id": "hide_fields",
          "method": {
            "id": "suppressOutput",
            "source_ids": [
              "raw_claim_id"
            ]
          }
        }
      ],
    },
  ],
  "computed_fields": [
    {
      /* output the number of claims in the document
      by taking the length of the claims array */
      "id": "claim_count",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "var": "claims_sections.length"
        }
      }
    },
    /* get the sum of all incurred dollar
    amounts in the document */
    {
      "id": "total_incurred",
      "method": {
        "id": "customComputation",
        "jsonLogic":
        /* for each incurred_amount value,
           add it to a running total sum
           Note: this syntax is an alternative to the Reduce operation */
        {
          "+": {
            "map": [
              {
                "var": "claims_sections"
              },
              {
                "var": "incurred_amount.value"
              }
            ]
          }
        }
      }
    },
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/blog_custom_computations.png) 

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/blog_custom_computations.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "claims_sections": [
    {
      "incurred_amount": {
        "source": "$3,053",
        "value": 3053,
        "unit": "$",
        "type": "currency"
      },
      "redacted_id": {
        "value": "***3456789",
        "type": "string"
      }
    },
    {
      "incurred_amount": {
        "source": "$251",
        "value": 251,
        "unit": "$",
        "type": "currency"
      },
      "redacted_id": {
        "value": "***6543211",
        "type": "string"
      }
    },
    {
      "incurred_amount": {
        "source": "$985",
        "value": 985,
        "unit": "$",
        "type": "currency"
      },
      "redacted_id": {
        "value": "***5439210",
        "type": "string"
      }
    },
    {
      "incurred_amount": {
        "source": "$581",
        "value": 581,
        "unit": "$",
        "type": "currency"
      },
      "redacted_id": {
        "value": "***5439210",
        "type": "string"
      }
    },
    {
      "incurred_amount": {
        "source": "$771",
        "value": 771,
        "unit": "$",
        "type": "currency"
      },
      "redacted_id": {
        "value": "***5439211",
        "type": "string"
      }
    }
  ],
  "claim_count": {
    "value": 5,
    "type": "number"
  },
  "total_incurred": {
    "value": 5641,
    "type": "number"
  }
}
```

# Notes

As an exception to the Custom Computation's limited [types](doc:types) output, you can output properties of extracted fields, including their `type`, `source`, and `value` by accessing them with `"var": "field_id"` rather than `"var": "field_id.value"` notation. For example, you can copy a  `total_unprocessed_claims` field in the [Claims loss run example](doc:sections-example-loss-run): 

```json
{
  /* field to copy:
  {
    "total_unprocessed_claims": {
      "source": "5",
      "value": 5,
      "type": "number"
    },
  */
  "id": "copy_field_into_this_key",
  "method": {
    "id": "customComputation",
    "jsonLogic": {
      "var": "../total_unprocessed_claims"
    }
  }
}

```

The  Custom Computation method in the preceding code sample returns:

```json
{
      "copy_field_into_this_key": {
        "source": "5",
        "value": 5,
        "type": "number"
      }
```



