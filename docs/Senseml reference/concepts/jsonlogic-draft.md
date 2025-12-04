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

## Join

LEFT OFF

[https://dev.sensible.so/editor/?d=frances\_playground\&c=join\_jsonlogic\&g=linearize\_2\_\_1](https://dev.sensible.so/editor/?d=frances_playground\&c=join_jsonlogic\&g=linearize_2__1)\_

// if for an item of tableA there are multiple corresponding items on tableB, function will get called just once (with an arbitrary itemB)

 Joins an array and an by the specified key and returns computed fields for each group:

```json
"join": [
        /* 1st arg: input array, key to join, optional array name */
        [
         [/* input array A */ ],
          { /* key to join arrays by */ }, 
          /* name for this input array. if unprovided, 
          defaults to tableA */
          "" 
        ],
        /* 2nd arg: input array, key to join, optional array name */
        [
          [/* input array B */ ],
          { /* key to join array by */ },
          /* name for this input array. if unprovided, 
          defaults to tableB */
          ""
        ],
         /* 3rd arg: operation to create a new array using the input arrays, for example,
            use eachKey operation.
            new array is same length as array A
            if for an item in array A there are multiple corresponding itmes in array B, operation takes an arbitrary corresponding item from array B */
        {
        }
      ]
```

For example, the following code joins a customers and an orders array by the customer ID, then creates a new array using elements from both arrays.

```json
{
  "fields": [],

  "postprocessor": {
    "type": "jsonLogic",
    "rule": {
      "join": [
        [
          /* 1st input array 
             In practice, you often input an
             array with `{"var":"field_key"}` syntax.
             This example uses `preserve` to input an
             array constant
             as literal JSON rather than JsonLogic*/
          {
            "preserve": [
              {
                "order_description": "office chairs",
                "customer_id": "c1",
                "amount": 50
              },
              {
                "order_description": "ink cartridges",
                "customer_id": "c2",
                "amount": 75
              },
              {
                "order_description": "whiteboards",
                "customer_id": "c3",
                "amount": 30
              },
              {
                "order_description": "desks",
                "customer_id": "c1",
                "amount": 40
              }
            ]
          },
          /* key to join arrays by */
          { "var": "customer_id" },
          /* name for this input array. if unprovided, defaults to tableA */
          "orders_array"
        ],
        [
          /* 2nd input array */
          {
            "preserve": [
              { "id": "c1", "first_name": "Sally", "last_name": "Smith" },
              { "id": "c2", "first_name": "Ahmed", "last_name": "Aamer" }
            ]
          },
          /* key to join array by */
          { "var": "id" },
          /* name for this input array. if unprovided, defaults to tableB */
          "customers_array"
        ],
        {
          /* create a new joined array, where each array element contains parameter values from array 1 and array 2*/
          "eachKey": {
            "order_descrpt": { "var": "orders_array.order_description" },
            "amnt": { "var": "orders_array.amount" },
            "name": {
              /* if first_name is absent for a customer_id, output "Unknown" */
              "if": [
                { "var": "customers_array" },
                { "var": "customers_array.first_name" },
                
                "Unknown"
              ]
            }
          }
        }
      ]
    }
  }
}

```

returns

```json
[
  {
    "order_descrpt": "office chairs",
    "amnt": 50,
    "name": "Sally"
  },
  {
    "order_descrpt": "ink cartridges",
    "amnt": 75,
    "name": "Ahmed"
  },
  {
    "order_descrpt": "whiteboards",
    "amnt": 30,
    "name": "Unknown"
  },
  {
    "order_descrpt": "desks",
    "amnt": 40,
    "name": "Sally"
  }
]
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

