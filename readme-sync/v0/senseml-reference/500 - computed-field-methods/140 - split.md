---
title: "Split"
hidden: false
---
Returns one of the components of a field's string output after splitting it with a delimiter. Common use cases for this method include discarding unwanted data from a field's output,  or separating output from one field into multiple fields.

Parameters
====
| key       | value         | description                                                  |
| :-------- | :------------ | :----------------------------------------------------------- |
| id        | `split`       |                                                              |
| source_id | id of a field | The id of the field to split                                 |
| separator | string        | The separator to use in the split                            |
| index     | integer       | The zero-based index of the component to return after the split |

Examples
====

The following image shows splitting a field's output to extract a first and last name:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/split_example.png)


You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for Split | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/split_example.pdf) |
| --------------------- | ------------------------------------------------------------ |

This example uses the following config:

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
      "id": "driver_name_first",
      "method": {
        "id": "split",
        "source_id": "_driver_name_raw",
        "separator": ", ",
        "index": 1
      }
    },
    {
      "id": "driver_name_last",
      "method": {
        "id": "split",
        "source_id": "_driver_name_raw",
        "separator": ", ",
        "index": 0
      }
    }
  ],
}
```
