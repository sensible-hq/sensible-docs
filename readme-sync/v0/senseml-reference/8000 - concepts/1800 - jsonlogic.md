---
title: "JsonLogic extensions"
hidden: false
---

JsonLogic is a library for processing rules written in JSON. A JsonLogic rule is structured as follows: `{ "operator" : ["values" ... ] }`.  For example, `{ "cat" : ["I love", "pie"] }` results in `"I love pie"`. 

Sensible supports both built-in and extended JsonLogic operators.

### Documentation

- For a Sensible-specific tutorial, see [The opinionated guide to JsonLogic for transforming document data](https://www.sensible.so/blog/opinionated-guide-to-jsonlogic-for-transforming-document-data).

- For information about the base built-in JsonLogic operators, see the [documentation](https://jsonlogic.com/operations.html).

-   Sensible supports extended operations available in the Json Logic Engine library.  For more information, see the [documentation](https://json-logic.github.io/json-logic-engine/docs). For example, this engine includes the following extended operations:

    - Array operations: `"length"`, `"get"`. 
    - Miscellaneous operations: `"preserve"`, `"keys"`. 
    - [Higher order operations](https://json-logic.github.io/json-logic-engine/docs/higher): `"every"`, `"eachKey"`



### Syntax tips

- Use dot notation to access properties of an object (by name) or items in an array (by index), for example, `test_table.columns.3.values` to access the 4th column in a table. 
- Double escape dots in field IDs. For example, `"delivery\\.zip\\.code.value"` to reference `87112` in the field `{"delivery.zip.code":{"value":87112}}`. 
- Use traversal notation to access data in hierarchies. For example, from within a section, use `"../"` to access fields in the parent object.
- To evaluate the current context, use `"var":""`.

### Sensible-specific operations

Sensible extends JsonLogic with custom operations. The following table lists these operations and where they're supported:

| Operation                                | [Validations](doc:validate-extractions) | [Custom computation](doc:custom-computation) methods | [Postprocessor](doc:postprocessor) |
| ---------------------------------------- | --------------------------------------- | ---------------------------------------------------- | ---------------------------------- |
| [Exists](doc:jsonlogic#exists)           | ✅                                       | ✅                                                    | ✅                                  |
| [Flatten](doc:jsonlogic#flatten)         | ✅                                       | ✅                                                    | ✅                                  |
| [Log](doc:jsonlogic#log)                 | ✅                                       | ✅                                                    | ✅                                  |
| [Match](doc:jsonlogic#match)             | ✅                                       | ✅                                                    | ✅                                  |
| [Object](doc:jsonlogic#object)           | ✅                                       | ✅                                                    | ✅                                  |
| [Omit fields](doc:jsonlogic#omit-fields) | ✅                                       | ✅                                                    | ✅                                  |
| [Pick Fields](doc:jsonlogic#pick-fields) | ✅                                       | ✅                                                    | ✅                                  |
| [Replace](doc:jsonlogic#replace)         | ✅                                       | ✅                                                    | ✅                                  |

See the following sections for more information.

## Exists

Returns a boolean to indicate if the specified value exists. Returns false if the value is null or undefined.

```json
{
    "exists": JsonLogic
}
```

Most commonly used with the JsonLogic `var` operation to test a field's output. 

Accepts as input:

- a single value, e.g., `{ "exists": { "var": "some_field" } }`)
- an array, in which case it checks the first item only, e.g., `{ "exists": [{ "var": "some_field" },...,] }`

### Examples

See [Validating extractions](doc:validate-extractions#examples).

## Flatten

Takes as input an array that can contain any depth of nested arrays, and returns a single-level array populated with the same values.

### Examples

The following example shows how to flatten a nested array. It also shows how Sensible transforms the JsonLogic output into the [fields](doc:field-query-object) schema when you use Flatten inside the Custom Computation method.

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

The log operation doesn't modify extracted document data. It returns its results as part of the extraction errors. Sensible passes the data wrapped in a log operation to whatever other operations surround it as if "log" were not there. For example `{ "*": [{ "log": ["first multiplication item", { "+": [1, 2] }], 4}] }` returns `12` and a log in the extraction errors with the fields `"message": "first multiplication item"` and `"result": 3`.

To view the results of the Log operation, see the `errors` array of the API extraction response, or see the **Errors** tab of the JSON editor's output pane. 

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
    /* Sensible recommends the Ojbect operation as an alternative to the "eachKey" operation if you don't know the keys in the object before building it */
    "object": 
        [
         /* where the JsonLogic operation returns `[["string", value] ...]`, e.g., map  */
         JsonLogic
        ]
}
```

## Omit fields

Creates a new object that includes all the fields from a source object except those specified. Takes an array of two items:

- an object to get fields from
- an array of field IDs to omit

```json
{
  "omit_fields": [
    sourceObject,
    ["field_id_1", "field_id_2", "field_id_3"]
  ]
}
```

Edge cases:

- The Omit Fields operator returns an empty object if the source object is empty, null, or undefined
- The Omit Fields operator returns the source object if it can't find the specified fields to omit.

### Examples

#### Example 1

As a simplified example, given the following extracted fields:

```json
{
  "field_morning": "good morning",
  "field_afternoon": "good afternoon",
  "field_evening": "good evening"
}
```

if you apply the rule:

```json
{
  "omit_fields": [
    // `"var": ""` returns the current context, in this case, the preceding extracted fields
    { "var": "" },
    // the IDs of the fields to be omitted
    ["field_morning"]
  ]
}
```

the rule outputs:

```json
{
  "field_afternoon": "good afternoon",
  "field_evening": "good evening"
}
```

#### Example 2

The following example shows removing extracted IDs from the [postprocessed](doc:postprocessor) output for a W-2 form.

**Config**

```json
{
  /* output result of omit_fields in `postprocessorOutput` */
  "postprocessor": {
    "type": "jsonLogic",
    "rule": {
      "omit_fields": [
        {
          /*  the source object, `"var": ""`, returns the current context, in this case, all extracted fields */
          "var": ""
        },
        /* the IDs of the fields to omit */
        [
          "employers_id",
          "employees_ssn"
        ]
      ]
    }
  },
  "fields": [
    {
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            "id": "state",
            "description": "state",
            "type": "string"
          },
          {
            "id": "state_wages",
            "description": "state wages",
            "type": "string"
          },
          {
            "id": "state_tax",
            "description": "state income tax",
            "type": "string"
          },
          {
            "id": "employers_id",
            "description": "employers_id",
            "type": "string"
          },
          {
            "id": "employees_ssn",
            "description": "employees_ssn",
            "type": "string"
          }
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/omit_fields.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/omit_fields.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Postprocessor output**

```json
{
  "state": {
    "value": "CA",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "state_wages": {
    "value": "52231.46",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "state_tax": {
    "value": "3461.27",
    "type": "string",
    "confidenceSignal": "confident_answer"
  }
}
```

**Extraction output**

```json
{
  "state": {
    "value": "CA",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "state_wages": {
    "value": "52231.46",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "state_tax": {
    "value": "3461.27",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "employers_id": {
    "value": "12-3456789",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "employees_ssn": {
    "value": "123-45-6789",
    "type": "string",
    "confidenceSignal": "confident_answer"
  }
}
```



## Pick fields

Returns the specified fields. Takes an array of two items:

- an object to get fields from
- an array of field IDs to pick

```json
{
  "pick_fields": [
    sourceObject,
    ["field_id_1", "field_id_2", "field_id_3"]
  ]
}
```

The Pick Fields operator returns an empty object if:

- you pass an empty array as the second argument, or if Sensible can't find the specified field IDs
- the source object is empty, null, or undefined

### Examples

#### Example 1

As a simplified example, given the following extracted fields:

```json
{
  "field_morning": "good morning",
  "field_afternoon": "good afternoon",
  "field_evening": "good evening"
}
```

if you apply the rule:

```json
{
  "pick_fields": [
    // `"var": ""` returns the current context, in this case, the preceding extracted fields
    { "var": "" },
    // the IDs of the fields to be returned by the rule
    ["field_morning", "field_afternoon"]
  ]
}
```

the rule outputs:

```json
{
  "field_morning": "good morning",
  "field_afternoon": "good afternoon"
}
```

#### Example 2

For a complete example, see [Custom computation group](doc:custom-computation-group).

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
