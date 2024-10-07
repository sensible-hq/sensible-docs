---
title: "jsonLogic extensions"
hidden: true
---

TODO ON publish: X link from validations, postprocessor, and custom computation to this topic

TODO: add very simple examples to each of these?

TODO: update all my "jsonlogic" links to this topic, including this one: custom-computation#sensible-operations 

INtroduce the CONCEPT of JSONLOGIC, refer reader to the ops page, and note the docs limits?



JsonLogic is a library for processing rules written in JSON. A JsonLogic rule is structured as follows: `{ "operator" : ["values" ... ] }`.  For example, `{ "cat" : ["I love", "pie"] }` results in `"I love pie"`. For more information about JsonLogic operators, see the [documentation](https://jsonlogic.com/operations.html).

Sensible extends [JsonLogic](https://jsonlogic.com/) with custom operations. The following table lists these operations and where they're supported:

| Operation                                                    | [Validations](doc:validate-extractions) | [Custom computation](doc:custom-computation) method | [Postprocessor](doc:postprocessor) |
| ------------------------------------------------------------ | --------------------------------------- | --------------------------------------------------- | ---------------------------------- |
| [Exists](doc:jsonlogic#exists)                         | ✅                                       | ✅                                                   | ✅                                  |
| [Match](doc:jsonlogic#match)                           | ✅                                       | ✅                                                   | ✅                                  |
| [Replace](doc:jsonlogic#replace)                       | ✅                                       | ✅                                                   | ✅                                  |
| [Object](doc:jsonlogic#object)                         | ❌                                       | ❌                                                   | ✅                                  |
| [Array With Context](doc:jsonlogic#array-with-context) | ?                                       | ?                                                   | ✅                                  |
| [Flatten](doc:jsonlogic#flatten)                       | ?                                       | ?                                                   | ✅                                  |



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

Takes as input an array that can contain nested arrays, and returns a single-level array populated with the same values.  This operation is similar to a [merge](https://jsonlogic.com/operations.html#merge) except that it's recursive to any depth. For example,  `{ "flatten": [1, [2, 3], [4, [5, 6, 7]]] }` returns `[1, 2, 3, 4, 5, 6, 7]`.

## Array With Context

The `"array_with_context"` operator is a convenience for shortening jsonLogic syntax when you write loops that operate on arrays. It allows you to access parent variables inside nested loops.

Takes as an input an array (or an operation that evaluates to an array), and returns a new array of objects with the following shape: 

```json
[
    {
        "item": "passed_in_array_item",
        "context": "current_value"
    },
    {
        "item": "passed_in_array_item",
        "context": "current_value"
    },
    ....
]
```

where:

- `item` is the item from the passed-in array

- `context` is the data in JsonLogic's context at the time of creation, e.g., the result of a  `"var"` operation on the current item in a loop

  

**Example**





![image-20241007114155231](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20241007114155231.png)

For example, say you extract an array of product names,  `"product_names" : ["basic_term_life", "dental"]`  from the preceding table along with other data.       

As part of a larger goal of transforming extracted data, you're looping through products for each customer. In the loop, you want to keep track of the employee name for each product. 

If you use the operation:

```json
{ "array_with_context": ["basic_term_life", "dental"l] }
```

when in the current loop iteration,  `{ "var" : ["employee_name.value"] }`   evaluates to the current data  `"Smith, Zoe"`, you'll get as output: 



```json
[
  { "item": "basic_term_life", "context": "Smith, Zoe" },
  { "item": "dental", "context": "Smith, Zoe" },
]
```







