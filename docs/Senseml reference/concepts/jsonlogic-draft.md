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

Performs a left join on two arrays using a common key, and returns a new array containing elements of both:

```json
"join": [
        /* 1st arg: input array, key to join, optional array name */
        [
         [/* input array A */ ],
          { /* key to join arrays by */ }, 
          /* name for this input array. if unprovided, 
          defaults to tableA */
          "array_A" 
        ],
        /* 2nd arg: input array, key to join, optional array name */
        [
          [/* input array B */ ],
          { /* key to join array by */ },
          /* name for this input array. if unprovided, 
          defaults to tableB */
          "array_B"
        ],
         /* 3rd arg: operation to output a new array using the input arrays, for example,
            use eachKey operation.
            output array is same length as array A
            if an item in array A corresponds to multiple items in array B, operation takes an arbitrary corresponding item from array B */
        {
        }
      ]
```

For example, the following code joins a customers array and an orders array by the customer ID, then creates a new array using elements from both arrays.

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

Selects elements in an array from a starting index up to but not including an ending index. Returns the new array containing the selected elements.

```json
"slice": [
    [ /* array_to_slice */ ],
    /* start_slice_index */,
    /* end_slice_index */
  ]
```

For example:

```json
  "slice": [
    [0, 1, 2, 3, 4],
    /* slice from 1st element up to 2nd-to-last element */
    0,
    -2
  ]
```

returns:

```json
[
  0,
  1,
  2
]
```

