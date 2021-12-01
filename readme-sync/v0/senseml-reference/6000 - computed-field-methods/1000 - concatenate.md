---
title: "Concatenate"
hidden: false
---
Concatenates the output of two or more fields:

- If the fields' outputs are all strings, the output is a single string.
- If any field output is an array, the output is an array if the array lengths match. The output is a string if the array lengths are unequal (using the first element of each array).
- If a string output is present among arrays, Sensible repeats its value for every element of the output.



Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                       | value                | description                                                  |
| :------------------------ | :------------------- | :----------------------------------------------------------- |
| id (**required**)         | `concat`             |                                                              |
| source_ids (**required**) | array of field IDs   | a list of field `id`s to concatenate in the config           |
| delimiter                 | string. default: " " | The delimiter with which to join the output of the source fields |

Examples
====

The following example shows using the Concat method to concatenate two address fields into one.

**Config**

```json
{
  "fields": [
    {
      "id": "_recipient_street_address",
      "method": {
        "id": "label",
        "position": "below"
      },
      "anchor": {
        "match": [
          {
            "text": "street address (including apt",
            "type": "startsWith"
          }
        ]
      }
    },
    {
      "id": "_recipient_city_state",
      "method": {
        "id": "label",
        "position": "below"
      },
      "anchor": {
        "match": [
          {
            "text": "city or town, state or province",
            "type": "startsWith"
          }
        ]
      }
    }
  ],
  "computed_fields": [
    {
      "id": "recipient_full_address",
      "method": {
        "id": "concat",
        "source_ids": [
          "_recipient_street_address",
          "_recipient_city_state"
        ],
        "delimiter": "\n"
      }
    }
  ]
}
```

**PDF**

The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/concat.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/concat.pdf) |
| ---------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "_recipient_street_address": {
    "type": "string",
    "value": "123 Anystreet"
  },
  "_recipient_city_state": {
    "type": "string",
    "value": "Anytown, AZ 12345"
  },
  "recipient_full_address": {
    "value": "123 Anystreet\nAnytown, AZ 12345",
    "type": "string"
  }
}
```
