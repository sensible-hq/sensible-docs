---
title: "Method object"
hidden: true
---

A

|                 |                             |                                                              |
| --------------- | --------------------------- | ------------------------------------------------------------ |
|                 |                             |                                                              |
|                 |                             |                                                              |
|                 |                             |                                                              |
|                 |                             |                                                              |
|                 |                             |                                                              |
|                 |                             |                                                              |
|                 |                             |                                                              |
|                 |                             |                                                              |
| **typeFilters** | array of [Types](doc:types) | Filters out the specified types from the method results. For example, for a target box containing a delivery date, a street address, and delivery notes, you can filter out the lines containing Date and Address types in order to extract the delivery notes. Note that less strict types, such as Name and Currency types, are less useful in this filter than stricter types such as the Phone Number type. |

Examples
====

The following example shows using the Types Filter parameter to extract delivery notes from a box.

**Config**

```json
{
  "fields": [
    {
      "id": "delivery_notes",
      "type": "string",
      "anchor": "delivery information",
      "method": {
        "id": "box",
        "offsetY": 1,
        "typeFilters": [
          "address",
          {
            "id": "date",
            "format": "%b_%D_%y"
          }
        ]
      }
    }
  ]
}
```

**PDF**
The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/types_filter.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/types_filter.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "delivery_notes": {
    "type": "string",
    "value": "Please leave package at door"
  }
}
```



