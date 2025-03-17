---
title: " merge objects"
hidden: true
---

*TODO: style guide:* 

- *operation or operator* 

+ *how to relate that to 'rule' , 'condition' or 'logic'? be consistent across this + other topics*



## Merge objects

*devon comments? merge objects:*
**Re: the note in the example, an example without `eachKey` would start with some original data that is then accessed in the example with `var` -*  



For an array of objects, returns a single object containing all the fields from each object. 

Edge cases:

- *If passed an empty array, it returns an empty object*
- *If passed an array containing a value that is `null` or `undefined`, ignores that value but still returns an object based on object values that were passed*
- *If passed an array containing a value that is not an object, `null`, or `undefined`, throws an error*
- *If passed multiple fields that use the same key, uses the **last** value that is passed for that key (same rules as when spreading JS objects)*

For example, simplified:

```json
{ 
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



