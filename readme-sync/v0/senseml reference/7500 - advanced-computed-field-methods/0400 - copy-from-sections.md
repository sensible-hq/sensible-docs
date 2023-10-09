---
title: "Copy from sections"
hidden: false
---
Returns an array of the values for a field in a source section group. This is useful for flattening the output of complex nested sections.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                            | value                                            | description |
| :----------------------------- | :----------------------------------------------- | :---------- |
| id (**required**)              | `copy_from_sections`                             |             |
| source_sections (**required**) | The ID of the source section group.              |             |
| source_field (**required**)    | The ID of the source field in the section group. |             |

Examples
====

See [Zip and flatten sections example](doc:sections-example-copy-from-sections).

