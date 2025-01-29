---
title: "Custom computation group"
hidden: true
---

TODO before publish:  

- adjust wording for custom comp group ('returns a single field')
- add to the advanced-computed INDEX file
- search on links to doc:custom-computation



Define your own [computed field method](doc:computed-field-methods) using [JsonLogic](doc:jsonlogic). Can return multiple fields.



Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value                             | description                                                  |
| :----------------------- | :-------------------------------- | :----------------------------------------------------------- |
| id (**required**)        | `customComputationGroup`          | - This method has access to the  `parsed_document` object at [verbosity](doc:verbosity) = 0. <br/> - This method doesn't output [Sensible types](doc:types). It outputs `string, number, boolean, null` , or an array of those. For example, adding two currencies results in a number.<br/>- This method returns null if you attempt to reference a variable that Sensible can't find in the `parsed_document`.<br/>- This method returns null if calculations include a null. For example, `5 + null field = null`.  If you instead want `5 + null field = 5`, then implement logic to replace nulls with zeros. |
| jsonLogic (**required**) | JsonLogic object | Transforms the output of one or more [Field objects](https://docs.sensible.so/docs/field-query-object) using [JsonLogic operations](doc:jsonlogic). The output is one or more fields. TODO: update language in custom comp to specify 1 field<br/> Double escape any dots in the field keys (for example, `delivery\\.zip\\.code`). <br/>Use dot notation to access arrays, for example, `test_table.columns.3.values` to access the 4th column in a table. TODO: now we also have traversal syntax examples ... should this note go into the JsonLogic topic and get removed from here + other topics? probably! maybe as a tip? INCLUDE the descriptions too in the json logic topic?<br/> |

Examples
====

See [Advanced: Transform sections data](doc:sections-example-copy-to-section).
