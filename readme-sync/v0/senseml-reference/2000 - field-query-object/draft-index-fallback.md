---
title: "Field query object"
hidden: true
---



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/basic_field.png)

| Parameter         | Value  | Description                                                  |
| ----------------- | ------ | ------------------------------------------------------------ |
| id (**required**) | string | Sensible uses the ID as the key in the structured key/value output. In the API response, this output is in the `parsed_document` section.<br/>To specify fallbacks, use the same ID in multiple fields. Succeeding fields act as fallbacks if the first returns null. For example, to capture differences in wording between document revisions, define two fields with the same ID, which anchor on synonymous text that may be present or absent in different document revisions. Fallback fields can be of any kind. For example, you can fallback from a field, to a computed field, to a section group. Fallbacks don't work across nested structures. For example, you can't fall back from a parent section group's field to a child section group's field.<br/>To determine which fallback returned an extracted value, set the verbosity to level 3 in the configuration to return the `source_field_index` value in the extracted output. This value is the index of the source field in the config's fields array. QUESTION TODO TEST: how are computed fields indexed if it's a'mixed' fields array vs 'separate' fields array? |
|                   |        |                                                              |
|                   |        |                                                              |
|                   |        |                                                              |
|                   |        |                                                              |

- doc:method)
