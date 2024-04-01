---
title: "Copy to section"
hidden: false
---
Copies the output of a field into each section in a section group, or from a parent section into each section in a nested section group. 

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value                                 | description                                                  |
| :----------------------- | :------------------------------------ | :----------------------------------------------------------- |
| id (**required**)        | `copy_to_section`                     |                                                              |
| source_id (**required**) | source field ID in the current config | Copies data from a field that's external to the section group's range to each section in the section group. <br/> The source ID to copy must be in a field array or section that is one level up in the hierarchy relative to the destination section. For example, in a sections group, copy from the base fields array. In a nested sections group, copy from the parent section group's field array. |

Examples
====

For an example, see [Advanced: Transform sections data](doc:sections-example-copy-to-section).
