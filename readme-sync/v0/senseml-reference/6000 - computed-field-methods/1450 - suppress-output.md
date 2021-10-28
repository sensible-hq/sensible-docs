---
title: "Suppress output"
hidden: true

---

**TODO: test example syntax**



Specifies fields to exclude from the extraction output. For example, if you use the field id  `_raw_data` as a source for a `nicely_formatted` [computed field](doc:computed-field-methods), then specify the raw field's id in this method to show only the computed field in the output.

Parameters
====

| key        | value              | description                                                 |
| :--------- | :----------------- | :---------------------------------------------------------- |
| id         | `suppressOutput`   |                                                             |
| source_ids | array of field ids | The id of the fields to exclude from the extraction output. |

The following example shows suppressing a raw "driver's name" field and outputting only the computed split field with the last name.

**Config**

```json
{
  "fields": [
    {
      "id": "_driver_name_first_last_raw",
      "anchor": "name of driver",
      "method": {
        "id": "label",
        "position": "below"
      }
    }
  ],
  "computed_fields": [
    {
      "id": "driver_name_last",
      "method": {
        "id": "split",
        "source_id": "_driver_name_first_last_raw",
        "separator": " ",
        "index": 1
      }
    },
    {
      "id": "hide_fields",
      "method": {
        "id": "suppressOutput",
        "source_ids": [
          "_driver_name_first_last_raw"
        ]
      }
    }
  ]
}
```



**PDF**

The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/suppress_output.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/suppress_output.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "driver_name_last": {
    "value": "Petrov",
    "type": "string"
  }
}
```

