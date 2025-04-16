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
| id (**required**)        | `customComputation`               | - This method has access to the  `parsed_document` object at [verbosity](doc:verbosity) = 0. <br/> - This method returns null if you attempt to reference a variable that Sensible can't find in the `parsed_document`.<br/>- This method returns null if calculations include a null. For example, `5 + null field = null`.  If you instead want `5 + null field = 5`, then implement logic to replace nulls with zeros. For an example, see [Example 1](doc:custom-computation#example-1).<br/>-  This method outputs the result of the JsonLogic as a single Sensible field. If the result doesn't conform to Sensible's schema for a field, Sensible transforms the output where possible to conform. For more information, see the Schema example.. TODO LINK. |
| jsonLogic (**required**) | JsonLogic object | Transforms the output of one or more [Field objects](https://docs.sensible.so/docs/field-query-object) using [JsonLogic operations](doc:jsonlogic). |

<sup>1</sup> For an exception to the restricted types that Custom Computation outputs, see the Notes section. 

# Examples

## Schema enforcement

The following example shows how Sensible enforces outputting the results of JsonLogic as a Sensible field:

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
        /* creates field with the Sensible currency type.
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
        recognizes and converts it to a sections group
        Sensible can't recognize arrays in the shape of nested sections */
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
  ]
}
```









## Notes

Outputs `string, number, boolean, null` , arrays of these types, and non-nested section groups. For more information about output types and Sensible [types](doc:types), see [Notes](doc:custom-computation#notes).











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
      "var": "total_unprocessed_claims"
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



