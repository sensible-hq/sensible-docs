---
title: "Custom computation group"
hidden: true
---

*TODO before publish:*  

- *adjust wording for custom comp group ('returns a single field')*
- *add to the advanced-computed INDEX file*
- *search on links to doc:custom-computation*
- *move json logic tips from here and custom-computation (assuming all apply) to /jsonlogic topic*

Define your own [computed field method](doc:computed-field-methods) using [JsonLogic](doc:jsonlogic). Can return multiple fields.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 


| key                      | value                             | description                                                  |
| :----------------------- | :-------------------------------- | :----------------------------------------------------------- |
| id (**required**)        | `customComputationGroup`          | - This method has access to the  `parsed_document` object at [verbosity](doc:verbosity) = 0. |
| jsonLogic (**required**) | JsonLogic object | Transforms the output of one or more [Field objects](https://docs.sensible.so/docs/field-query-object) using [JsonLogic operations](doc:jsonlogic). Expects to output an object as the result of the JsonLogic operations. Converts the attributes of the output object to fields. |

Examples
====

See [Advanced: Transform sections data](doc:sections-example-copy-to-section).
