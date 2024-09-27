---
title: "jsonLogic extensions"
hidden: true
---

TODO ON publish: X link from validations, postprocessor, and custom computation to this topic



TODO: add very simple examples to each of these?

TODO: update all my "jsonlogic" links to this topic, including this one: custom-computation#sensible-operations 

INtroduce the CONCEPT of JSONLOGIC, refer reader to the ops page, and note the docs limits?

Sensible extends [JsonLogic](https://jsonlogic.com/) with custom operations. The following table lists these operations and where they're supported:

| Operation                                                    | [Validations](doc:validate-extractions) | [Custom computation](doc:custom-computation) method | [Postprocessor](doc:postprocessor) |
| ------------------------------------------------------------ | --------------------------------------- | --------------------------------------------------- | ---------------------------------- |
| [Exists](doc:draft-jsonlogic#exists)                         | ✅                                       | ✅                                                   | ✅                                  |
| [Match](doc:draft-jsonlogic#match)                           | ✅                                       | ✅                                                   | ✅                                  |
| [Replace](doc:draft-jsonlogic#replace)                       | mostly n/a (TODO: true??)               | ✅                                                   | ✅                                  |
| [Object](doc:draft-jsonlogic#object)                         | ❌                                       | ❌                                                   | ✅                                  |
| [Array With Context](doc:draft-jsonlogic#array-with-context) | ?                                       | ?                                                   | ✅                                  |
| [Flatten](doc:draft-jsonlogic#flatten)                       | ?                                       | ?                                                   | ✅                                  |



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



### Examples

See [Postprocessor](doc:postprocessor#examples). 



## Flatten

takes in an array that may contain nested arrays, returns a single-level array populated with all the same values.

- Example: `{ "flatten": [[1, [2, 3], [4, [5, 6]]] }` will return: `[1, 2, 3, 4, 5, 6]` 

### Examples

## Array With Context

The `"array_with_context"` operator is a convenience for shortening jsonLogic syntax when you write loops that operate on arrays.

takes in an array (or something that evaluates to an array, like the result of another rule), returns a new array of objects with an `item` and `context` property, where `item` is the item from the passed-in array and `context` is the data in JsonLogic's context at the time of creation (it's what you would get if you used `{ var: "" }`). TODO: test this, not sure what this means exactly

- Example: `{ "array_with_context": [1, 2, 3, 4] }` when  the current data is `{ "customer_name": "Your Name" }` will return TODO rewrite this to be more real world:

```
[
  { "item": 1, "context": { "customer_name": "Your Name" } },
  { "item": 2, "context": { "customer_name": "Your Name" } },
  { "item": 3, "context": { "customer_name": "Your Name" } },
  { "item": 4, "context": { "customer_name": "Your Name" } }
]
```

## Flatten

  : takes in an array that may contain nested arrays to any depth, returns a single-level array populated with all the same values. It's similar to a [merge](https://jsonlogic.com/operations.html#merge) except it's recursive.

  - Example: `{ "flatten": [1, [2, 3], [4, [5, 6, 7]]] }` will return: `[1, 2, 3, 4, 5, 6, 7]` TODO test this!

### Examples

TBOD
