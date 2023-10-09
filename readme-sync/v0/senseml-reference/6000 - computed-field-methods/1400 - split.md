---
title: "Split"
hidden: false
---
Returns one of the components of a field's string output after splitting it with a delimiter. Common use cases for this method include discarding unwanted data from a field's output, and splitting output from one field into separate fields.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 

| key                      | value                            | description                                                  |
| :----------------------- | :------------------------------- | :----------------------------------------------------------- |
| id (**required**)        | `split`                          |                                                              |
| source_id (**required**) | a field id in the current config | The id of the field to split into substrings.                |
| separator (**required**) | string                           | The separator to use in the split.                           |
| index                    | integer                          | The zero-based index of the substring to return after the split. If unspecified, returns all the split substrings as an array. |

Examples
====

The following example shows splitting a field's output to extract a first and last name.

**Config**

```json
{
  "fields": [
    {
      "id": "_driver_name_raw",
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
        "source_id": "_driver_name_raw",
        "separator": " ",
        "index": 1
      }
    },
    {
      "id": "driver_name_first",
      "method": {
        "id": "split",
        "source_id": "_driver_name_raw",
        "separator": " ",
        "index": 0
      }
    }
  ],
}
```



**Example document**

The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/split.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/split.pdf) |
| --------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "_driver_name_raw": {
    "type": "string",
    "value": "Petar Petrov"
  },
  "driver_name_last": {
    "value": "Petrov",
    "type": "string"
  },
  "driver_name_first": {
    "value": "Petar",
    "type": "string"
  }
}
```

