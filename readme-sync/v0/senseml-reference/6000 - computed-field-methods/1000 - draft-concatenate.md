---
title: "draft Concatenate"
hidden: true
---


Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                       | value                                                      | description                                                  |
| :------------------------ | :--------------------------------------------------------- | :----------------------------------------------------------- |
| id (**required**)         | `concat`                                                   |                                                              |
| source_ids (**required**) | array of field IDs in the current config</br>or<br/>object | a list of field `id`s to concatenate in the config<br/>You can use a JavaScript-flavored regular expression to specify all field IDs that contain a pattern.  For example,  to specify all the field IDs containing `wage` from a W-2 form, you can write  `"source_ids": { "pattern": ".*wage.*" }`. For more information about this example, see [Example: Chain prompts with regex](doc:query-group#chain-prompts-with-regex).<br/> When you use regex, Sensible populates the IDs in the array in the same order in which they're defined in the config. Sensible automatically expands your pattern to include string beginning and ending characters. For example, it expands the pattern `".*wage.*"` to `"^.*wage.*$"`. <br/>If you use a regular expression to specify the source IDs, then the field must be in the `fields` array, not the `computed_fields` array. |
|                           |                                                            |                                                              |



```"computed_fields": [

```
