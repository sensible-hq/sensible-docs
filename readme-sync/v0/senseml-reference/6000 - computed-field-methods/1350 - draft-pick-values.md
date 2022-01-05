---
title: "Pick values"
hidden: true

---

Extract values from a group of fields. For example, extract the selected boxes from a checkbox group, or extract all "yes" answers from a group of fields with a yes/no/maybe dropdowns.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 

| key                       | value                                    | description                                                  |
| :------------------------ | :--------------------------------------- | :----------------------------------------------------------- |
| id (**required**)         | `pickValues`                             |                                                              |
| source_ids (**required**) | array of field ids in the current config | The id of the fields from which to pick. Returns those fields whose value matches that specified in the Value parameter. |
| match                     | `one`, `all`                             | Specifies to return either the first source field with the value specified in the Value parameter, or all fields with the matching value. |
| value                     | null, boolean, string, or string array   | The value to pick. Sensible converts checkbox and radio button selection marks to true and false. For example, to pick selected checkboxes, specify `true`. As another example, to return dropdown questions set to "maybe" in a list of fields, specify `"maybe"`. |

The following example shows TBD

**Config**

```json

```



**PDF**

The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/pick_values.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/pick_values.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json

```

