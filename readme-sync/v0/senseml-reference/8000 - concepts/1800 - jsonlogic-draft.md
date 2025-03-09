---
title: " merge objects"
hidden: true
---

*TODO: style guide:* 

- *operation or operator* 

+ *how to relate that to 'rule' , 'condition' or 'logic'? be consistent across this + other topics*



## Merge objects

For an array of objects, rreturns a signel object containing t all the fields from each object. 

Edge cases:

- *If passed an empty array, it returns an empty object*
- *If passed an array containing a value that is `null` or `undefined`, ignores that value but still returns an object based on object values that were passed*
- *If passed an array containing a value that is not an object, `null`, or `undefined`, throws an error*
- *If passed multiple fields that use the same key, uses the **last** value that is passed for that key (same rules as when spreading JS objects)*

For example:

```json
{ // todo: example w/o eachKey?
  "merge_objects": [
    { "eachKey": { "field1": "hello" } },
    { "eachKey": { "field2": "world" } }
  ]
}

```



returns:

``` json
{
  "field1": "hello",
  "field2": "world"
}
```



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

For a complete example, see TODO TBD.