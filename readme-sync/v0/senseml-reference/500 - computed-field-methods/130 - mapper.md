---
title: "Mapper"
hidden: false
---

Maps output from source fields using a case-sensitive lookup table. A common use case for this method is to standardize output across configs. For example, if you see inconsistently formatted data from different document sources ("6 month policy period" versus "6 mo. policy duration"), you can map those data to a common format using the Mapper method.  Consistently formatted output simplifies your application logic by allowing you to ignore distinctions between document sources.

Parameters
====

| key       | value                                   | description                                                  |
| :-------- | :-------------------------------------- | :----------------------------------------------------------- |
| id        | `mapper`                                |                                                              |
| source_id | a field id in the current configuration | The id of the field to map                                   |
| mappings  | object                                  | An object with mappings from strings or numbers to output strings represented as key/value pairs, e.g., `{ "03/04": "March 4th" }`. Key value pairs are case sensitive. |

Examples
====

The following image shows using a mapper to standardize a time duration:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/mapper_example.png)


You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for Mapper | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/mapper_example.pdf) |
| ---------------------- | ------------------------------------------------------------ |

This example uses the following config:

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
      "id": "premium_period",
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
          "twelve months": "12"
        }
      }
    }
  ]
}
```
