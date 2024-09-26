---
title: "jsonLogic extensions"
hidden: true
---

TODO ON publish: X link from validations, postprocessor, and custom computation to this topic



TODO: add very simple examples to each of these?



Sensible extends [JsonLogic](https://jsonlogic.com/) with custom operations. The following table lists these operations and where they're supported

| Operation                                              | Validations               | Custom computation method | Postprocessor |
| ------------------------------------------------------ | ------------------------- | ------------------------- | ------------- |
| [exists](doc:draft-jsonlogic#exists)                         | ✅                         | ✅                         | ✅             |
| [match](doc:draft-jsonlogic#match)                           | ✅                         | ✅                         | ✅             |
| [replace](doc:draft-jsonlogic#replace)                       | mostly n/a (TODO: true??) | ✅                         | ✅             |
| [object](doc:draft-jsonlogic#object)                         | ❌                         | ❌                         | ✅             |
| [array-with-context](doc:draft-jsonlogic#array-with-context) | ❌                         | ❌                         | ❌             |



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

