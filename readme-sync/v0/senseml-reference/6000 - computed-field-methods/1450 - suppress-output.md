---
title: "Suppress output"
hidden: false

---

Specifies fields to exclude from the extraction output. For example, if you use the field ID  `_raw_data` as a source for a [computed field](doc:computed-field-methods), then specify the raw field's ID in this method to show only the computed field in the output.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 

| key                       | value                                    | description                                                  |
| :------------------------ | :--------------------------------------- | :----------------------------------------------------------- |
| id (**required**)         | `suppressOutput`                         |                                                              |
| source_ids (**required**) | array of field ids in the current config | The id of the fields to exclude from the extraction output.<br/> In advanced use cases, configure [field execution order](doc:field-order) to prevent unintential null output from other computed field methods. For an example, see [Zip sections example](doc:sections-example-zip).<br/>You can use a JavaScript-flavored regular expression to specify all field IDs that contain a pattern.  For example,  to specify all the field IDs containing the text `wage` extracted from a W-2 form, you can write  `"source_ids": { "pattern": ".*wage.*" }`. For more information and an example, see [Example: Chain prompts with regex](doc:query-group#example-chain-prompts-with-regex). |

The following example shows suppressing a raw "driver's name" field and outputting the split last name. 

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



**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/suppress_output.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/suppress_output.pdf) |
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

