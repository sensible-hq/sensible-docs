---
title: jsonlogic draft
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---



TEST CHANGE

## Join

LEFT OFF

[https://dev.sensible.so/editor/?d=frances\_playground\&c=join\_jsonlogic\&g=linearize\_2\_\_1](https://dev.sensible.so/editor/?d=frances_playground\&c=join_jsonlogic\&g=linearize_2__1)\_

// joins two arrays by using a common key\
// args:\
// - tableA, must resolve to an array\
// - fnA, takes an item from tableA and returns the joining key\
// - tableB\
// - fnB\
// - fn, takes [itemA, itemB]\
//\
// it always return an array of the same length as tableA\
// if for an item of tableA there is no corresponding item on tableB, fn will get [itemA, null]

// if for an item of tableA there are multiple corresponding items on tableB, fn will get called just once (with an arbitrary itemB)

 Groups an array of objects by the specified key and returns computed fields for each group:

```json
"group":
[
 [ /* array_of_objects_to_group */ ],
 "key_to_group_by", 
[[/* field_to_return */ ], [/* field_to_return */ ] ... ] /* specify each field_to_return with syntax ["key", JsonLogic] */
]
```

For example, the following code groups an array of clothes objects by their apparel type:

```
```

## Slice

Selects elements in an array from `start` up to, but not including, `stop`.  Returns the new array containing the selected elements.

For example, slicing 

```json
"slice": [
    [ /* array_to_slice */ ],
    /* start_slice_index */,
    /* end_slice_index */
  ]
```

Example:

```json
  "slice": [
    [0, 1, 2, 3, 4],
    0,
    3
  ]
```

