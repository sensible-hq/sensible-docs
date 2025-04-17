---
title: " style notes"
hidden: true
---

*TODO: style guide:* 

- *operation or operator* 

+ *how to relate that to 'rule' , 'condition' or 'logic'? be consistent across this + other topics*



## Date Shift

Takes a date, a number, and a unit ('days", "months", or "years"), and returns an ISO 8601-formatted date-time string that is the result of adding the number of units to the date.

For example:

```json
{
    "date_shift": [
        "2024-01-02T00:00:00.000Z",
        2,
        "months"
    ]
}
```

returns:

```json
"2024-03-02T00:00:00.000Z"
```

**Notes**:

- date arg supports `Date` type as well as other values that can be cast to dates. TODO: what does Date type mean?   I think it means strings that typescript can succesfful cast in the typescript Date type... which I believe means ISO 8601 format strings , like 

  ```
  date_type_date: {
          source: "10/4/2024",
          value: new Date("10/4/2024"),
          type: "date",
        },
  ```

  

- number arg supports `number` type as well as other values that can be cast to numbers.

- supports use of negative numbers to calculate prior dates.

## Map Object

equivalent to `Object.entries(obj).map( ([key, value]) => ...)`

The custom `mapObject` operator in your `jsonlogic` implementation functions like `Object.entries(obj).map(([key, value]) => ...)`, letting you iterate over an object and apply logic per key-value pair.

LEFT OFF:
why doesn't this work? https://dev.sensible.so/editor/?d=frances_playground&c=map_object&g=postprocessor_llm_humana_1_redact&v=

```json
{
  "fields": [
    {
      "id": "date_shift_1",
      "method": {
        "id": "customComputation",
        "jsonLogic": {
          "mapObject": [
            {
              "key1": 2,
              "key2": 3,
            },
            [
              // rule for the key: leave unchanged
              {
                "var": "key"
              },
              // rule for the value
              {
                "+": [
                  {
                    "var": "value"
                  },
                  4
                ]
              },
            ],
          ]
        }
      }
    },
  ]
}
```







### ✅ What it does:

It takes **two arguments**:

1. An **object** to iterate over.
2. A **rule or set of rules** to apply to each `[key, value]` pair in that object.

The rule(s) you pass are evaluated per *pair*, and the results are collected into an array and returned.

  ```
  mapObject: [
      { var: "obj" },
      [
        { var: "key" },
        { "*": [{ var: "value" }, 2] },
      ],
    ]
  }
  ```









------

### 🔍 Breakdown of Test Cases:

1. **Basic usage with transformation**

   ```
   tsCopyEdit{
     mapObject: [
       { var: "obj" },
       [
         { var: "key" },
         { "*": [{ var: "value" }, 2] },
       ],
     ]
   }
   ```

   ➡️ Transforms to:

   ```
   ts
   
   
   CopyEdit
   [["key1", 2], ["key2", 4], ["key3", 6]]
   ```

2. **Single rule (not in array)**

   ```
   tsCopyEdit{
     mapObject: [{ var: "obj" }, { var: "key" }]
   }
   ```

   ➡️ Extracts only the keys: `["key1", "key2", "key3"]`

3. **Null output for some entries**

   ```
   tsCopyEdit{
     mapObject: [
       { var: "obj" },
       {
         if: [
           { "===": [{ var: "key" }, "key1"] },
           null,
           [
             { var: "key" },
             { "*": [{ var: "value" }, 2] }
           ],
         ],
       },
     ]
   }
   ```

   ➡️ Conditional transformation: `[null, ["key2", 4], ["key3", 6]]`

4. **Single rule in an array**

   ```
   ts
   
   
   CopyEdit
   mapObject: [{ var: "obj" }, [{ var: "key" }]]
   ```

   ➡️ Each result is wrapped in an array: `[["key1"], ["key2"], ["key3"]]`

5. **Multiple rules per entry**

   ```
   tsCopyEditmapObject: [
     { var: "obj" },
     [
       { var: "key" },
       { "*": [{ var: "value" }, 2] },
       { cat: [{ var: "key" }, " testing"] }
     ]
   ]
   ```

   ➡️ Outputs 3 values per entry: `["key1", 2, "key1 testing"]` etc.

6. **Empty object returns empty array**

   ```
   ts
   
   
   CopyEdit
   mapObject: [{ var: "emptyObj" }, [{ var: "key" }, { var: "value" }]]
   ```

   ➡️ `[]`

7. **Invalid args**

   ```
   ts
   
   
   CopyEdit
   mapObject: { var: "obj" }
   ```

   ➡️ Throws `"Invalid args for mapObject"` – must be an array of arguments.

8. **Non-object input**

   ```
   ts
   
   
   CopyEdit
   mapObject: ["not an object", [{ var: "key" }, { var: "value" }]]
   ```

   ➡️ Throws `"Invalid args for mapObject"` – input must be a proper object.

------

### 🧠 Summary

Your `mapObject` operator is a custom JsonLogic extension that brings functional-style `Object.entries().map()` capability to JsonLogic. It supports:

- Single or multiple return values per entry
- Conditionals
- Empty object safety
- Type checks for invalid usage

It makes it easy to transform objects dynamically in JsonLogic rules without manually iterating or restructuring them outside logic.

Want a sample implementation of this custom operator in code?

## Group

 this `group` operation is a **custom JSONLogic function** that's essentially performing a **group-by operation** on an array of objects, and then **running additional logic on each group** to produce a summarized result.

Let’s break it down.

------

### 🔍 `group` Operation - What It Does:

**Signature:**

```

group([array, key, fields])
```

#### **Parameters:**

1. **`array`** – The array of objects you want to group (e.g., `transactions`).
2. **`key`** – The key to group by (e.g., `"date"`).
3. **`fields`** – The list of fields (in JSONLogic) to compute for each group.

------

### 🧠 How It Works:

1. **Run `input[0]`** – evaluates to the array you want to group (e.g., `data.transactions`).
2. **Run `input[1]`** – evaluates to the key to group by (`"date"`).
3. **Group** the array by the value of the `key`, using `JSON.stringify(v[key])` to avoid object identity issues.
4. **For each group:**
   - Set context:
     - `key`: the value of the grouping key
     - `values`: the array of objects in this group
   - Run the provided `fields` logic in this context to produce the result object.

------

### 🧪 The Test Example Explained:

You’re grouping transactions **by `date`**, and for each date, computing:

- The field `"date"` is just set to the group key.
- The `"average"` is computed over the `ending_daily_balance.value` of all items in the group.

#### Breakdown of the logic:

```
jsonCopyEdit"group": [
  { "var": "transactions" },
  "date",
  [
    ["date", { "var": "key" }],
    ["average", { 
      "object": [
        [
          ["type", "currency"],
          ["unit", "$"],
          [
            "value",
            {
              "/": [
                {
                  "reduce": [
                    { "var": "values" },
                    {
                      "+": [
                        { "var": "accumulator" },
                        { "var": "current.ending_daily_balance.value" }
                      ]
                    },
                    0
                  ]
                },
                { "length": { "var": "values" } }
              ]
            }
          ]
        ]
      ]
    }]
  ]
]
```

This calculates the **average ending_daily_balance.value** per date.

------

### ✅ Result:

You end up with:

```
tsCopyEdit[
  {
    date: { value: "7/14", type: "string" },
    average: { value: 2500, unit: "$", type: "currency" }
  },
  {
    date: { value: "7/15", type: "string" },
    average: { value: 4000, unit: "$", type: "currency" }
  }
]
```

------

### ✨ Summary:

The `group` operation:

- Groups an array by a specified field.
- Runs custom logic per group using the key (`key`) and values (`values`) in context.
- Returns an array of results for each group, based on the provided fields logic.

It’s like a very JSONLogic-ish version of SQL’s `GROUP BY ... SELECT`.

Let me know if you want help adapting or extending it!
