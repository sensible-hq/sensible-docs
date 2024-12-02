---
title: "Mapper"
hidden: false
---

Maps output from source fields using a case-sensitive lookup table. A common use case for this method is to standardize output across configs. For example, if different documents inconsistently format data ("6 month policy period" versus "6 mo. policy duration"), you can map those data to a common format using the Mapper method. Consistently formatted output simplifies your application logic by allowing you to ignore distinctions between document sources.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 

| key                      | value                                   | description                                                  |
| :----------------------- | :-------------------------------------- | :----------------------------------------------------------- |
| id (**required**)        | `mapper`                                |                                                              |
| source_id (**required**) | a field id in the current configuration | The id of the field to map                                   |
| mappings (**required**)  | object                                  | An object with mappings from strings or numbers to output strings represented as key/value pairs, for example, `{ "03/04": "March 4th" }`. Key value pairs are case sensitive. |
| default                  | string or `null`                        | If a source field exists, but the mapping doesn't exist, Sensible returns the value specified by this parameter. The specified value can be null or it can be a string, for example, `"mapping doesn't exist"`.<br/>If the source field doesn't exist or is null, Sensible ignores this parameter and always returns null. |

Examples
====

The following example shows using a mapper to standardize a time duration.

**Config**


```json
{
  "fields": [
    {
      "id": "_premium_period_raw",
      "anchor": "duration",
      "method": {
        "id": "row"
      }
    }
  ],
  "computed_fields": [
    {
      "id": "premium_period_months",
      "method": {
        "id": "mapper",
        "source_id": "_premium_period_raw",
        "mappings": {
          "ANNUAL": "12",
          "BIANNUAL": "6",
          "MONTHLY": "1",
          "Six months": "6",
          "six months": "6",
          "Twelve months": "12",
          "twelve months": "12",
        },
        "default": "mapping doesn't exist"
      }
    }
  ]
}
```

**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/mapper.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/mapper.pdf) |
| ---------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "_premium_period_raw": {
    "type": "string",
    "value": "Six months"
  },
  "premium_period_months": {
    "value": "6",
    "type": "string"
  }
}
```

