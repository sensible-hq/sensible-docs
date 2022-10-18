---
title: "Copy to section"
hidden: false
---
Copies a field into each section in a section group, or from a parent section into each section in a nested section group. 

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value                                 | description                                                  |
| :----------------------- | :------------------------------------ | :----------------------------------------------------------- |
| id (**required**)        | `copy_to_section`                     |                                                              |
| source_id (**required**) | source field ID in the current config | The source ID to copy must be in a field array or section that is one level up in the hierarchy relative to the destination section. For example, in a sections group, copy from the base fields array. In a nested sections group, copy from the parent section group's field array. |

Examples
====

For an example, see [Advanced: Add global information to sections](doc:sections-example-copy-to-section).
