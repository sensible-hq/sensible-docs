---
title: "excel examples"
hidden: true
---

The following topic describes how Sensible converts extracted document data to CSV or spreadsheet format. The general principles are:

- `fields` sheet - a sheet that lists fields as key-value dictionary, with the field id as the column heading and value as the row. Eg Box, Label, etc. Fields go here if it:
  
  - has a  single `value` parameter (link in doc to example)
  - has short stringified array output
  - **Example:** The converts to the following Excel sheet:
  -   <iframe src="https://docs.google.com/spreadsheets/d/e/2PACX-1vRJO_nwPRVe84ZdAi-gc6mny0zhRO9iz4nclfEKSBFQWHotARcgUkwfcinpGJTzPM4GIoIvf6PcN7zv/pubhtml?widget=true&amp;headers=false"></iframe>
- `<field_id>` sheet - If  a field has complex or long output, e.g. Table or an array from `"match":"all"` it gets its own sheet:
  
  - output is a table (link to doc examples)
  - output is an array
- sections sheets - Sections have the same patterns as previously mentioned methods, with indexes to handle repeating output. For example, a sheet name can be: `section_group_id.*section_index*.child_group_id.*child_index*.field_id` 



Simple extracted values
---

Fields with a single value convert to a "fields" sheet.  For example, Sensible outputs these fields from [Getting started](doc:getting-started)

```json
{
  "fields": [
    {
      "id": "policy_period",
      "anchor": "policy period",
      "method": {
        "id": "label",
        "position": "right"
      }
    },
    {
      "id": "comprehensive_premium",
      "anchor": "comprehensive",
      "type": "currency",
      "method": {
        "id": "row",
        "tiebreaker": "second"
      }
    }
 }      
```

 to the following CSV:

![image-20220614102120649](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220614102120649.png)

Examples of methods that output single-value output include the following methods where match-all or other array params are disabled:

TODO convert to table, some have examples, some don't??? 

- Box

- Checkbox

- (document range?? passthrough?)

- Intersection

- Invoice `metadata` output

- Label

- Nearest Checkbox

- Regex

- Region

- Row(?)

- **computed**

- Concatenate

- Constant

- Mapper

- (pick values?)

- Split

  

For more examples, see the following: 

| simple fields    | TODO: use when adding docs to topics                         |                                                              |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| anyco            | https://docs.google.com/spreadsheets/d/1S5W9NO-5W51xxif29Aws6sojBiitONUpb-g4-6ANtaA/edit?usp=sharing | [Getting started][getting-started](doc:getting-started#csv-output) |
| invoice metadata | https://docs.google.com/spreadsheets/d/1vIiiFGwLYjT6CLx9BHBZdur9PdZ50lY-G3ae2CoPf9w/edit#gid=0 | [Invoice][doc:invoice#csv-output]                            |
|                  |                                                              |                                                              |
|                  |                                                              |                                                              |
|                  |                                                              |                                                              |
|                  |                                                              |                                                              |
|                  |                                                              |                                                              |
|                  |                                                              |                                                              |
|                  |                                                              |                                                              |

