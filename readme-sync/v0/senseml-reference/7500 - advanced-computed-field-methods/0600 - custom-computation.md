---
title: "Custom computation"
hidden: false
---

Define your own [computed field method](doc:computed-field-methods) using JsonLogic. For example, return the sum of two fields, or return a boolean indicating if a field's output is non-null.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value                                      | description                                                  |
| :----------------------- | :----------------------------------------- | :----------------------------------------------------------- |
| id (**required**)        | `customComputation`                        | This method has access to the  `parsed_document` object as follows: <br/>- at a depth of [verbosity](doc:verbosity) = 0<br/>- at a depth of one section, in the case of nested sections<br/><br/>This method operates on the following types in the `parsed_document`  object: `string, number, boolean, null` , or on an array of those. Otherwise it returns null. It returns the same types. |
| jsonLogic (**required**) | [JsonLogic](https://jsonlogic.com/) object | Transforms the output of one or more [Field objects](https://docs.sensible.so/docs/field-query-object) using JsonLogic. Supports all [JsonLogic operations](https://jsonlogic.com/operations.html) and extends them with Sensible operations such as `"exists"` and `"match`". For more information about Sensible operations, see  [Validating extractions](doc:validate-extractions#parameters).<br/><br/>Double escape any dots in the field keys (for example for a field ID `delivery.zip.code`, escape as `delivery\\.zip\\.code`). |

Examples
====

The following example shows defining simple custom computed fields.

**Config**

```json
{
  "fields": [
    {
      "id": "field1",
      "type": "currency",
      "method": {
        "id": "query",
        "description": "property damage limit in first table"
      },
    },
    {
      "id": "field2",
      "type": "currency",
      "method": {
        "id": "query",
        "description": "bodily injury limit in first table"
      },
    }
  ],
  "computed_fields": [
    {
      /* is field's value non-null? */
      "id": "field1_exists",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "exists": [
            {
              "var": "field1.value"
            }
          ]
        }
      }
    },
    {
      /* does field's value contain at least one 
         alphanumeric character? */
      "id": "field2_matches_regex",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "match": [
            {
              "var": "field2.value"
            },
            "^\\w+$"
          ]
        }
      }
    },
    {
      /* addition */
      "id": "field1_addition",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "+": [
            {
              "var": "field1.value"
            },
            200
          ]
        }
      }
    }
  ]


```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/add_computed_fields_1.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/add_computed_fields.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "field1": {
    "source": "$5,000",
    "value": 5000,
    "unit": "$",
    "type": "currency"
  },
  "field2": {
    "source": "$3,000",
    "value": 3000,
    "unit": "$",
    "type": "currency"
  },
  "field1_exists": {
    "value": true,
    "type": "boolean"
  },
  "field2_matches_regex": {
    "value": true,
    "type": "boolean"
  },
  "field1_addition": {
    "value": 5200,
    "type": "number"
  }
}
```
