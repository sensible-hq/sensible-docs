---
title: "copy to section"
hidden: true
---
https://dev.sensible.so/editor/?d=frances_test_playground&c=copy_to_section_computed&g=copy_to_section_loss_run





Copies a field into each section in a section group, or from a parent section into each section in a nested section group. (TODO, image showing this with generic yaml and arrows?)





Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value                                    | description                                        |
| :----------------------- | :--------------------------------------- | :------------------------------------------------- |
| id (**required**)        | `copy_to_section`                        |                                                    |
| source_id (**required**) | array of field IDs in the current config | a list of field `id`s to concatenate in the config |
|                          |                                          |                                                    |

Examples
====

The following example shows using 

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

**Example document**

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
