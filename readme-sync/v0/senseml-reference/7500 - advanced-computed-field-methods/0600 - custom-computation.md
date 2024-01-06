---
title: "Custom computation"
hidden: true
---

Define your own computed method using JsonLogic. For example, sum two fields, 

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value                                      | description                                                  |
| :----------------------- | :----------------------------------------- | :----------------------------------------------------------- |
| id (**required**)        | `customComputation`                        | Has access to the entire `parsed_document` where [verbosity](doc:verbosity) = 0, so you don't need to specify a list of `source_ids`. Includes access to  field `type`. Will operate on anything that is ``"string", "number", "boolean", "null"` ? or an array of those, and returns the same types.`. TODO doublechekc code:   the output is `BaseType |
| jsonLogic (**required**) | [JsonLogic](https://jsonlogic.com/)  rules | [11:12](https://sensiblehq.slack.com/archives/D03G5KRKWH5/p1703268726812319)   Outputs a computed field by using Boolean, logic, numeric, array, string, and other operations on extracted fields. Supports all [JsonLogic operations](https://jsonlogic.com/operations.html) and extends them with Sensible operations such as `"exists"` and `"match`". For more information about Sensible operations, see  [Validating extractions](doc:validate-extractions#parameters).<br/><br/>Double escape any dots in the field keys (for example for a field ID `delivery.zip.code`, escape as `delivery\\.zip\\.code`). |

Examples
====

Say that you have following document extraction output:

```
{
    "field1": {
        "value": {
            "type": "number",
            "value": 200
        },
        "metadata": []
    },
    "field2": {
        "value": {
            "type": "number",
            "value": 300
        },
        "metadata": []
    },
    "array": {
        "value": [
            {
                "type": "string",
                "value": "Hello"
            },
            {
                "type": "string",
                "value": "World"
            }
        ],
        "metadata": []
    },
    "table": {
        "value": {
            "type": "table",
            "value": [
                {
                    "id": "column1",
                    "values": [
                        {
                            "value": {
                                "type": "number",
                                "value": 100
                            },
                            "metadata": []
                        },
                        {
                            "value": {
                                "type": "number",
                                "value": 200
                            },
                            "metadata": []
                        }
                    ]
                },
                {
                    "id": "column2",
                    "values": [
                        {
                            "value": {
                                "type": "string",
                                "value": "Ben"
                            },
                            "metadata": []
                        },
                        {
                            "value": {
                                "type": "string",
                                "value": "Ten"
                            },
                            "metadata": []
                        }
                    ]
                }
            ],
            "source": ""
        },
        "metadata": []
    },
    "section": {
        "value": {
            "type": "sections",
            "source": "",
            "value": [
                {
                    "value": {
                        "section_field1": {
                            "value": {
                                "type": "number",
                                "value": 1300
                            },
                            "metadata": []
                        },
                        "section_field2": {
                            "value": {
                                "type": "string",
                                "value": "apple"
                            },
                            "metadata": []
                        }
                    }
                },
                {
                    "value": {
                        "section_field1": {
                            "value": {
                                "type": "number",
                                "value": 1500
                            },
                            "metadata": []
                        },
                        "section_field2": {
                            "value": {
                                "type": "string",
                                "value": "orange"
                            },
                            "metadata": []
                        }
                    }
                }
            ]
        },
        "metadata": []
    },
    "distance_miles": {
        "value": {
            "type": "distance",
            "value": 300,
            "unit": "miles"
        },
        "metadata": []
    },
    "distance_km": {
        "value": {
            "type": "distance",
            "value": 300,
            "unit": "kilometers"
        },
        "metadata": []
    }
}
```



Here are examples of operations:

**exists**

```json
    {
          "id": "field1_exists",
          "method": {
            "id": "customComputation",
            "jsonLogic": { exists: [{ var: "field1.value" }] }
            }
          }
        }
      } 
```

You should get:

```
"id": "field1_exists",
"value": true
```



**match**

```json
```



**addition**

```json

    {
          "id": "field1_plus_100",
          "method": {
            "id": "customComputation",
            "jsonLogic": { "+": [{ var: "field1.value" }, 100] }]
            }
          }
        }
      }
```

You should get:

```
"id": "field1_plus_100",
"value": 300
```



**boolean**

```json

    {
          "id": "true_if_field1_is_over_100",
          "method": {
            "id": "customComputation",
            "jsonLogic": { ">": [{ var: "field1.value" }, 100] }
            }
          }
        }
      }
```

You should get:

```json
"id": "true_if_field1_is_over_100",
"value": true
```







**TODO: accumulator**

```json

    {
      "id": "total_indemnity",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "reduce": [
            { "var": "claims" },
            {
              "+": [
                { "var": "current.indemnity_payment.value" },
                { "var": "accumulator" }
              ]
            },
            0
          ]
        }
      }
  
```

TODO/left off:

```json
it("bad variable references evaluate to null", async () => {
    exp = { var: "field1.apple" };
    await check(exp, value(null));
  });

  it("simple arithmetic operations", async () => {
    exp = { "+": [{ var: "field1.value" }, 100] };
    await check(exp, value(300));

    exp = { "-": [{ var: "field1.value" }, { var: "field2.value" }] };
    await check(exp, value(-100));
  });

  it("simple boolean operations", async () => {
    exp = { ">": [{ var: "field1.value" }, 100] };
    await check(exp, value(true));

    exp = { "===": [{ var: "field1.value" }, { var: "field2.value" }] };
    await check(exp, value(false));

    exp = { exists: [{ var: "field1.value" }] };
    await check(exp, value(true));
  });

  it("simple string operations", async () => {
    exp = {
      cat: [{ var: "array.0.value" }, " ", { var: "array.1.value" }],
    };
    await check(exp, value("Hello World"));

    exp = { match: [{ var: "array.1.value" }, "^\\w+$"] };
    await check(exp, value(true));
  });

  it("array operations", async () => {
    exp = { map: [{ var: "array" }, { cat: [{ var: "value" }, "+"] }] };
    await check(exp, value(["Hello+", "World+"]));
  });

  it("tabular operations", async () => {
    exp = {
      map: [
        { var: "table.columns.0.values" },
        { "+": [{ var: "value" }, 100] },
      ],
    };
    await check(exp, value([200, 300]));
  });

  it("section operations", async () => {
    exp = {
      map: [{ var: "section" }, { var: "section_field1.value" }],
    };
    await check(exp, value([1300, 1500]));
  });

  it("conditional logic based on multiple value properties", async () => {
    const expBuilder = (v: string) =>
      ({
        if: [
          { "===": [{ var: `${v}.unit` }, "miles"] },
          { "*": [{ var: `${v}.value` }, 1609] },
          { "*": [{ var: `${v}.value` }, 1000] },
        ],
      } as RulesLogic);
    await check(expBuilder("distance_miles"), value(482700));
    await check(expBuilder("distance_km"), value(300000));
  });
});
```

