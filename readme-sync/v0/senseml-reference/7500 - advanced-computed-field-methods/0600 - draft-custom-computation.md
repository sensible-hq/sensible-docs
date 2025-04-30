---
title: "Custom computation"
hidden: true
---

Define your own [computed field method](doc:computed-field-methods) using [JsonLogic](doc:jsonlogic). For example, return the sum of two fields, map arrays, or return a boolean indicating if a field's output is non-null. Returns one field.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value                             | description                                                  |
| :----------------------- | :-------------------------------- | :----------------------------------------------------------- |
| id (**required**)        | `customComputation`               | - This method has access to the  `parsed_document` object at the extraction's level of [verbosity](doc:verbosity).<br/><br/>-  This method outputs the result of the JsonLogic as a single Sensible field. If the result doesn't conform to Sensible's schema for a field, Sensible transforms the output to conform when possible. For more information, see the Schema  enforcement example. TODO LINK.<br/><br/> - This method returns null if you attempt to reference a variable that Sensible can't find in the `parsed_document`.<br/>- This method returns null if calculations include a null. For example, `5 + null field = null`.  If you instead want `5 + null field = 5`, then implement logic to replace nulls with zeros. For an example, see [Example 1](doc:custom-computation#example-1). |
| jsonLogic (**required**) | JsonLogic object | Transforms the output of one or more [Field objects](https://docs.sensible.so/docs/field-query-object) using [JsonLogic operations](doc:jsonlogic). |



# Examples

## Schema enforcement

The following example shows how Sensible enforces outputting the results of JsonLogic as a Sensible field for the Custom Computation method:

**config**

```json
{
  "fields": [
    {
      "id": "enforce_field_schema_1",
      "method": {
        /* to enforce field schema, Sensible wraps boolean constant in a field 
        and recognize it as
        `"type": "boolean" 
        Sensible automatically converts:
        - string, number, boolean, null
        - arrays of these values
        - sections-shaped arrays
        into the Sensible field output schema. See following comments for more examples.
        
        */
        "id": "customComputation",
        "jsonLogic": true
      }
    },
    {
      "id": "enforce_field_schema_2",
      "method": {
        /* wraps number constant array in a field 
        and converts it to an array of values of type "number" */
        "id": "customComputation",
        "jsonLogic": [
          3,
          5
        ]
      }
    },
    {
      "id": "Sensible_typed_field",
      "method": {
        /* creates field with the specified Sensible currency type.
        Sensible enforces Sensible types.
        If you try to output an unsupported type, like
        `"type": "accountID"`, Sensible returns null */
        "id": "customComputation",
        "jsonLogic": {
          "eachKey": {
            "type": "currency",
            "value": 10,
            "unit": "USD",
            "source": "$10"
          }
        }
      }
    },
    {
      "id": "output_sections",
      "method": {
        /*  if you input an array in the shape of a sections group, Sensible 
        recognizes and converts it to a sections group */
        "id": "customComputation",
        "jsonLogic": [
          {
            "eachKey": {
              "claim_number": 2345,
              "description": "slip and fall"
            }
          },
          {
            "eachKey": {
              "claim_number": 6789,
              "description": "collision"
            }
          }
        ]
      }
    },
    {
      "id": "output_nested_sections",
      "method": {
        /*  if you input an array in the shape of a nested sections group, Sensible 
        recognizes and converts it to a nested sections group */
        "id": "customComputation",
        "jsonLogic": {
          /* use `preserve` to input a literal JSON object instead of JsonLogic */
          "preserve": [
            {
              "parentSectionTitle": {
                "type": "string",
                "value": "Heading 1"
              },
              "nestedSections": [
                {
                  "subheading": {
                    "type": "string",
                    "value": "Heading A"
                  }
                },
                {
                  "subheading": {
                    "type": "string",
                    "value": "Heading B"
                  }
                }
              ]
            },
            {
              "parentSectionTitle": {
                "type": "string",
                "value": "Heading 2"
              },
              "nestedSections": [
                {
                  "subheading": {
                    "type": "string",
                    "value": "Heading C"
                  }
                },
                {
                  "subheading": {
                    "type": "string",
                    "value": "Heading D"
                  }
                }
              ]
            }
          ]
        }
      }
    }
  ]
}
```

**Output**

```json
{
  "enforce_field_schema_1": {
    "value": true,
    "type": "boolean"
  },
  "enforce_field_schema_2": [
    {
      "value": 3,
      "type": "number"
    },
    {
      "value": 5,
      "type": "number"
    }
  ],
  "Sensible_typed_field": {
    "type": "currency",
    "value": 10,
    "unit": "USD",
    "source": "$10"
  },
  "output_sections": [
    {
      "claim_number": {
        "value": 2345,
        "type": "number"
      },
      "description": {
        "value": "slip and fall",
        "type": "string"
      }
    },
    {
      "claim_number": {
        "value": 6789,
        "type": "number"
      },
      "description": {
        "value": "collision",
        "type": "string"
      }
    }
  ],
  "output_nested_sections": [
    {
      "parentSectionTitle": {
        "type": "string",
        "value": "Heading 1"
      },
      "nestedSections": [
        {
          "subheading": {
            "type": "string",
            "value": "Heading A"
          }
        },
        {
          "subheading": {
            "type": "string",
            "value": "Heading B"
          }
        }
      ]
    },
    {
      "parentSectionTitle": {
        "type": "string",
        "value": "Heading 2"
      },
      "nestedSections": [
        {
          "subheading": {
            "type": "string",
            "value": "Heading C"
          }
        },
        {
          "subheading": {
            "type": "string",
            "value": "Heading D"
          }
        }
      ]
    }
  ]
}
```




