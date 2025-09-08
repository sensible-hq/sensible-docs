---
title: "Pick values"
hidden: false

---

Extracts specified values from a group of fields. For example, extracts the selected boxes from a checkbox group, or extracts all "yes" answers from a group of fields with yes/no/maybe dropdowns.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 

| key                       | value                                                   | description                                                  |
| :------------------------ | :------------------------------------------------------ | :----------------------------------------------------------- |
| id (**required**)         | `pickValues`                                            |                                                              |
| source_ids (**required**) | array of field ids in the current config                | The id of the fields from which to pick values. Returns the fields whose values matches that specified in the Value parameter.<br/>You can use a JavaScript-flavored regular expression to specify all field IDs that contain a pattern.  For example,  to specify all the field IDs containing the text `wage` extracted from a W-2 form, you can write  `"source_ids": { "pattern": ".*wage.*" }`. For more information and an example, see [Example: Chain prompts with regex](doc:query-group#chain-prompts-with-regex). |
| match                     | `one`, `all`. default: `all`                            | `one`:  Select this option for mutually exclusive field groups, for example, a group of radio buttons where the user can select a single item. If no fields in the group have the specified value, or if more than one field has the expected value, then Sensible returns null. <br/><br/> `all`: Returns all fields in the group with the specified value. |
| value                     | null, boolean, string, or string array. default: `True` | The value to pick. Sensible converts checkbox and radio button selection marks to true and false. For example, to pick selected checkboxes, specify `true`.  Or, to return dropdown questions set to "yes", specify `"yes"`.<br/>`null` returns the list of source IDs with null values, for example when Sensible can't find a checkbox. |

The following example shows returning a single value from a radio button group, and two values from a group of dropdowns.

**Config**

```json
{
  "fields": [
    {
      "id": "individual",
      "anchor": "individual",
      "method": {
        "id": "nearestCheckbox",
        "position": "left"
      }
    },
    {
      "id": "partnership",
      "anchor": "partnership",
      "method": {
        "id": "nearestCheckbox",
        "position": "left"
      }
    },
    {
      "id": "llc",
      "anchor": "limited liability",
      "method": {
        "id": "nearestCheckbox",
        "position": "left"
      }
    },
    {
      "id": "income_over_100k",
      "anchor": "in excess of",
      "method": {
        "id": "row"
      }
    },
    {
      "id": "out_of_state_income",
      "anchor": "out-of-state",
      "method": {
        "id": "row"
      }
    },
    {
      "id": "professional_services",
      "anchor": "professional services",
      "method": {
        "id": "row"
      }
    }
  ],
  "computed_fields": [
    {
      "id": "business_classification",
      "method": {
        "id": "pickValues",
        "match": "one",
        "source_ids": [
          "individual",
          "partnership",
          "llc"
        ]
      }
    },
    {
      "id": "income_yes_answers",
      "method": {
        "id": "pickValues",
        "match": "all",
        "value": "yes",
        "source_ids": [
          "income_over_100k",
          "out_of_state_income",
          "professional_services"
        ]
      }
    },
    {
      "id": "cleanup_output",
      "method": {
        "id": "suppressOutput",
        "source_ids": [
          "income_over_100k",
          "out_of_state_income",
          "professional_services",
          "individual",
          "partnership",
          "llc"
        ]
      }
    }
  ]
}
```



**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/pick_values.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/pick_values.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "business_classification": {
    "value": "partnership",
    "type": "string"
  },
  "income_yes_answers": [
    {
      "value": "income_over_100k",
      "type": "string"
    },
    {
      "value": "professional_services",
      "type": "string"
    }
  ]
}
```

