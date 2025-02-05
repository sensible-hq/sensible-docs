---
title: "JsonLogic extensions"
hidden: false
---

JsonLogic is a library for processing rules written in JSON. A JsonLogic rule is structured as follows: `{ "operator" : ["values" ... ] }`.  For example, `{ "cat" : ["I love", "pie"] }` results in `"I love pie"`. 

Sensible supports both built-in and extended JsonLogic operators.

### Documentation

- For a Sensible-specific tutorial, see [The opinionated guide to JsonLogic for transforming document data](https://www.sensible.so/blog/opinionated-guide-to-jsonlogic-for-transforming-document-data).

- For information about the base built-in JsonLogic operators, see the [documentation](https://jsonlogic.com/operations.html).


### Syntax tips

- Double escape dots in field IDs. For example, `"delivery\\.zip\\.code"` to reference the field `"delivery.zip.code": 87112`. 
- Use dot notation to access properties of an object (by name) or items in an array (by index), for example, `test_table.columns.3.values` to access the 4th column in a table. 
- Use traversal notation to access data in hierarchies. For example, from within a section, use `"../"` to access fields in the parent object.
- To evaluate the current context, use `"var":""`.

### Extended operations


  Sensible supports extended operations available in the Json Logic Engine library.  For more information, see the [documentation](https://json-logic.github.io/json-logic-engine/docs). For example, this engine includes (but is not limited to) the following extended operations:

  - Array operations: `"length"`, `"get"`. 
  - Miscellaneous operations: `"preserve"`, `"keys"`. 
  - [Higher order operations](https://json-logic.github.io/json-logic-engine/docs/higher): `"every"`, `"eachKey"`
  
  Sensible also extends JsonLogic with custom operations. The following table lists these operations and where they're supported:

| Operation                        | [Validations](doc:validate-extractions) | [Custom computation](doc:custom-computation) method | [Postprocessor](doc:postprocessor) |
| -------------------------------- | --------------------------------------- | --------------------------------------------------- | ---------------------------------- |
| [Exists](doc:jsonlogic#exists)   | ✅                                       | ✅                                                   | ✅                                  |
| [Flatten](doc:jsonlogic#flatten) | ✅                                       | ✅                                                   | ✅                                  |
| [Log](doc:jsonlogic#log)         | ✅                                       | ✅                                                   | ✅                                  |
| [Match](doc:jsonlogic#match)     | ✅                                       | ✅                                                   | ✅                                  |
| [Object](doc:jsonlogic#object)   | ✅                                       | ✅                                                   | ✅                                  |
| [Replace](doc:jsonlogic#replace) | ✅                                       | ✅                                                   | ✅                                  |

See the following sections for more information.

## Exists

Returns a boolean to indicate if the specified value exists.

```json
{
    "exists": JsonLogic
}
```

Most commonly used with the JsonLogic `var` operation to test that an output value isn't null. Returns true if the value being evaluated is neither null nor undefined. Can take an array (where it will check the first item only) or a single value (e.g., `{ "exists": [{ "var": "some_field" }] }` or `{ "exists": { "var": "some_field" } }`).

### Examples

See [Validating extractions](doc:validate-extractions#examples).

## Flatten

Takes as input an array that can contain any depth of nested arrays, and returns a single-level array populated with the same values.

### Examples

The following example uses Flatten, and also shows how JsonLogic output may be reshaped when used as part of custom computation.

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
     custom computation wraps the returned output
     in value/type syntax, i.e., `{ "value": 1, "type": "number" },
     { "value": 2, "type": "number" }, ... ]` */
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

## Log

Note that this operation replaces the native [JsonLogic](https://jsonlogic.com/operations.html#log) operation.

Takes as input an array, where the first argument is the log message and the second is a JsonLogic expression you want to evaluate. 

```json
{
    "log": [
        "log message",
         JsonLogic
    ]
}
```

The log operation doesn't modify extracted document data. It returns its results as part of the extraction errors. The data wrapped in a log operation will be passed to whatever other operations surround it as if "log" were not there. For example `{ "*": [{ "log": ["first multiplication item", { "+": [1, 2] }], 4}] }` will return a result of 12, and will show a log in the extraction errors with the fields `"message": "first multiplication item"` and `"result": 3`.

To view the results of the Log operation, see the `errors` array of the API extraction response, or in the **Errors** tab of the JSON editor's output pane. 

### Examples

See [Advanced: Transform sections data](doc:sections-example-copy-to-section).

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

### Examples


## Replace

Returns a modified string.

One of the following syntaxes:

```json
{
    "replace": {
        "source": JsonLogic,
        "find": string, // or JsonLogic that evaluates to string
        "replace": string // or JsonLogic that evaluates to string
    }
}
```

Or:

```json
{
    "replace": {
        "source": JsonLogic,
        "find_regex": regex,
        "replace": string, // or JsonLogic that evaluates to string
        "flags": "i" // optional
    }
}
```

Where `regex` is a Javascript-flavored regular expression. Double escape special regex characters, since the regex is in a JSON object (for example, `\\s`, not `\s`, to represent a whitespace character). This operation supports:

- regex capturing groups
- regex flags, such as `i` for case insensitive. 

### Examples

 See [Custom Computation](doc:custom-computation#examples).
