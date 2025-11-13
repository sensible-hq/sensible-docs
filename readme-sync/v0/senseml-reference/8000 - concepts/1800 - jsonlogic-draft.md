---
title: " jsonlogic draft"
hidden: true
---



## Join

https://dev.sensible.so/editor/?d=frances_playground&c=join_jsonlogic&g=linearize_2__1_

// joins two arrays by using a common key
// args:
// - tableA, must resolve to an array
// - fnA, takes an item from tableA and returns the joining key
// - tableB
// - fnB
// - fn, takes [itemA, itemB]
//
// it always return an array of the same length as tableA
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

https://dev.sensible.so/editor/?d=frances_playground&c=slice_jsonlogic&g=linearize_2__1_&v=



```
it("slice", () => {
    expect(apply({ slice: [[0, 1, 2, 3, 4], 1, -2] })).toEqual([1, 2]);
  });
```

