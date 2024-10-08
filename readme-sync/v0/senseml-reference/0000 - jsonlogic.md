---
title: "JsonLogic extensions"
hidden: true
---

JsonLogic is a library for processing rules written in JSON. A JsonLogic rule is structured as follows: `{ "operator" : ["values" ... ] }`.  For example, `{ "cat" : ["I love", "pie"] }` results in `"I love pie"`. For more information about JsonLogic operators, see the [documentation](https://jsonlogic.com/operations.html).

Sensible extends [JsonLogic](https://jsonlogic.com/) with custom operations. The following table lists these operations and where they're supported:

| Operation                        | [Validations](doc:validate-extractions) | [Custom computation](doc:custom-computation) method | [Postprocessor](doc:postprocessor) |
| -------------------------------- | --------------------------------------- | --------------------------------------------------- | ---------------------------------- |
| [Exists](doc:jsonlogic#exists)   | ✅                                       | ✅                                                   | ✅                                  |
| [Match](doc:jsonlogic#match)     | ✅                                       | ✅                                                   | ✅                                  |
| [Replace](doc:jsonlogic#replace) | ✅                                       | ✅                                                   | ✅                                  |
| [Object](doc:jsonlogic#object)   | ❌                                       | ❌                                                   | ✅                                  |
| [Flatten](doc:jsonlogic#flatten) | ✅                                       | ✅                                                   | ✅                                  |

## Exists

Returns a boolean to indicate if the specified value exists.

```json
{
    "exists": [
        JsonLogic
    ]
}
```

Most commonly used with the JsonLogic `var`  operation to test that an output value isn't null. The  `var` operation retrieves extracted field values using field `id` keys. 

### Examples

See [Validating extractions](doc:validate-extractions#examples).

## Match

Returns a boolean to indicate if the specified regular expression matches.

```json
{
    "match": [
        JsonLogic,
        regex
    ]
}
```

 Where `regex` is a Javascript-flavored regular expression.

Double escape special regex characters, since the regex is in a JSON object (for example, `\\s`, not `\s` , to represent a whitespace character). This operation does *not* support regular expression flags such as `i` for case insensitive. 

### Examples

See [Validating extractions](doc:validate-extractions#examples). 

## Replace

Returns a modified string.

One of the following syntaxes:

```json
{
    "replace": {
        "source": JsonLogic,
        "find": JsonLogic
        "replace": JsonLogic
    }
}
```

Or:

```json
{
    "replace": {
        "source": JsonLogic,
        "find_regex": regex
        "replace": JsonLogic,
        "flags": "i" //optional
    }
}
```

Where `regex` is a Javascript-flavored regular expression.  Double escape special regex characters, since the regex is in a JSON object (for example, `\\s`, not `\s` , to represent a whitespace character). This operation supports:

- regex capturing groups
- regex flags, such as `i` for case insensitive. 

### Examples

 See [Custom Computation](doc:custom-computation#examples).

## Object

Returns a JSON object that is an array of key/value pairs. You can nest object operations to build complex custom objects.  One of the following syntaxes:

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

Or:

```json
{
    "object": 
        [
         /* where the JsonLogic operation returns `[["string", value] ...]`, e.g., map  */
         JsonLogic
        ]
}
```

As a simple example,  

```json
{
    "object": [
        [
            [
                "customer_name",
                "Erika Mustermann"
            ],
            [
                "customer_acct",
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
  "customer_name": "Erika Mustermann",
  "customer_acct": 12345
}
```

### Examples

See [Postprocessor](doc:postprocessor#examples). 

## Flatten

Takes as input an array that can contain nested arrays, and returns a single-level array populated with the same values.  This operation is similar to the built-in JsonLogic [merge](https://jsonlogic.com/operations.html#merge) operation, except that it's recursive to any depth. 

### Examples

The following example shows that the Flatten operation's output varies depending on the context.

````json
{
  "fields": [],
  "postprocessor": {
    /* returns a flat array, i.e. [1,2,3,4,5,6,7] */
    "type": "jsonLogic",
    "rule": {
      "flatten": [
        [
          1,
          [
            2,
            3
          ],
          [
            4,
            [
              5,
              6,
              7
            ]
          ]
        ]
      ]
    }
  },
  /* since the output must be a field or fields,
     wraps the returned output in value/type syntax, 
     i.e., `{ "value": 1, "type": "number" }, { "value": 2, "type": "number" }, ... ]` */
  "computed_fields": [
    {
      "id": "flatten_in_custom_comp",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "flatten": [
            [
              1,
              [
                2,
                3
              ],
              [
                4,
                [
                  5,
                  6,
                  7
                ]
              ]
            ]
          ]
        }
      }
    },
  ],
}
````

returns the following:

```json
// in postprocessorOutput
[
  1,
  2,
  3,
  4,
  5,
  6,
  7
]

// in parsed_document
{
  "flatten_in_custom_comp": [
    {
      "value": 1,
      "type": "number"
    },
    {
      "value": 2,
      "type": "number"
    },
    {
      "value": 3,
      "type": "number"
    },
    {
      "value": 4,
      "type": "number"
    },
    {
      "value": 5,
      "type": "number"
    },
    {
      "value": 6,
      "type": "number"
    },
    {
      "value": 7,
      "type": "number"
    }
  ]
}
```

