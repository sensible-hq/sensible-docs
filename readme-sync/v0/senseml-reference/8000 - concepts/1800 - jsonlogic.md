---
title: "JsonLogic extensions"
hidden: false
---

JsonLogic is a library for processing rules written in JSON. A JsonLogic rule is structured as follows: `{ "operator" : ["values" ... ] }`.  For example, `{ "cat" : ["I love", "pie"] }` results in `"I love pie"`. 

Sensible supports both built-in and extended JsonLogic operators:

- For information about built-in JsonLogic operators, see the [documentation](https://jsonlogic.com/operations.html).
- Sensible supports extended operations available in the Json Logic Engine.  For more information, see the [documentation](https://json-logic.github.io/json-logic-engine/docs/math). For example, this engine includes the following extended operations:
  - Array operations: `"length"`, `"get"`. 
  - Miscellaneous operations: `"preserve"`, `"keys"`. 
  - Higher order operations: `"every"`, [`"eachKey"`](https://json-logic.github.io/json-logic-engine/docs/higher). 
-  Sensible extends JsonLogic with custom operations. The following table lists these operations and where they're supported:

| Operation                        | [Validations](doc:validate-extractions) | [Custom computation](doc:custom-computation) method | [Postprocessor](doc:postprocessor) |
| -------------------------------- | --------------------------------------- | --------------------------------------------------- | ---------------------------------- |
| [Exists](doc:jsonlogic#exists)   | ✅                                       | ✅                                                   | ✅                                  |
| [Flatten](doc:jsonlogic#flatten) | ✅                                       | ✅                                                   | ✅                                  |
| [Match](doc:jsonlogic#match)     | ✅                                       | ✅                                                   | ✅                                  |
| [Object](doc:jsonlogic#object)   | ✅                                       | ✅                                                   | ✅                                  |
| [Replace](doc:jsonlogic#replace) | ✅                                       | ✅                                                   | ✅                                  |

See the following sections for more information.

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

## Object

Returns a JSON object that is an array of key/value pairs. You can nest object operations to build complex custom objects.  This operation is an alternative to the  `"eachKey"`  operation. Use the Object operation when the keys in the object you intend to build can vary depending on other operations:


```json
{
    /* Sensible recommends this syntax as an alternative to the "eachKey" operator if you don't know the keys in the object before building it */
    "object": 
        [
         /* where the JsonLogic operation returns `[["string", value] ...]`, e.g., map  */
         JsonLogic
        ]
}
```


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





