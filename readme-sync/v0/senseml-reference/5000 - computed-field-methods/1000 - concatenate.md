---
title: "Concatenate"
hidden: false
---
Concatenates the output of two or more fields:

- If the fields' outputs are all strings, the output is a single string.
- If any field output is an array, the output is an array if the array lengths match. The output is a string if the array lengths are unequal (using the first element of each array).
- If a string output is present among arrays, its value is repeated for every element of the output.



Parameters
====


| key                       | value                | description                                                  |
| :------------------------ | :------------------- | :----------------------------------------------------------- |
| id (**required**)         | `concat`             |                                                              |
| source_ids (**required**) | array of field IDs   | a list of field `id`s to concatenate in the config           |
| delimiter                 | string. default: " " | The delimiter with which to join the output of the source fields |

Examples
====

The following image shows using the Concat method to concatenate two address fields into one:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/concat.png)


Try out this example in the Sensible app using the following PDF and config:

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/concat.pdf) |
| ---------------------- | ------------------------------------------------------------ |

This example uses the following config:

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
