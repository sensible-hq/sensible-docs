---
title: "Constant"
hidden: false
---
Adds a key/value pair to an extraction, where the value is a constant that's not necessarily present in the document. This lets you include information, such as vendor or form names, that may be lacking from the document. For example, imagine a vendor solely issues 6-month policy quotes, so they never state the policy duration in the document. Use the Constant method to add `policy_duration_months: 6`. 

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 

| key                  | value      | description                                              |
| :------------------- | :--------- | :------------------------------------------------------- |
| id (**required**)    | `constant` |                                                          |
| value (**required**) | string     | The value to return in the field's key/value pair output |

Examples
====

The following example shows adding a form name and policy duration as constants to a config's output.

**Config**

```json
{
  "fields": [
    {
      "id": "policy_period",
      "anchor": "policy period",
      "method": {
        "id": "documentRange",
        "includeAnchor": true,
        "wordFilters": [
          "policy period"
        ],
        "stop": {
          "text": "for customer",
          "type": "startsWith"
        },
      }
    }
  ],
  "computed_fields": [
    {
      "id": "form_name",
      "method": {
        "id": "constant",
        "value": "quote_auto_insurance_anyco"
      }
    },
      {
        "id": "policy_duration_months",
        "type": "number",
        "method": {
          "id": "constant",
          "value": "6"
        }
      }
    ]
  }
```



**Example document**

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/constant.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf) |
| ------------------------ | ------------------------------------------------------------ |

**Output**

```json
{
  "policy_period": {
    "type": "string",
    "value": "April 14, 2021 - Oct 14, 2021"
  },
  "form_name": {
    "value": "quote_auto_insurance_anyco",
    "type": "string"
  },
  "policy_duration_months": {
    "source": "6",
    "value": 6,
    "type": "number"
  }
}
```

