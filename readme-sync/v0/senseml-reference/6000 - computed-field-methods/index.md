---
title: "Computed field methods"
hidden: false
---
Computed Field methods transform the output of one or more [Field objects](doc:field-query-object). Common use cases for computed fields include:

- Clean up raw output:  If the output contains extra characters, strings, etc, you can often use a Computed Field method to strip out the unwanted data. Or, you can split or join data from different fields.
- Standardize output across configs:  If you extract inconsistently formatted data from different vendors or documents, for example "6 month policy period" versus "6 mo. policy duration", you can map to a common format. Consistently formatted output helps your application to handle extractions with fewer checks for corner cases.
- Add metadata: If a PDF lacks information that you want to include in the extraction, you can add it.

The following pages describe Computed Field methods:

- [Concatenate](doc:concatenate)
- [Constant](doc:constant)
- [Mapper](doc:mapper)
- [Split](doc:split)
- [Zip](doc:zip)

Parameters
====

The following global parameters are common to all Computed Field methods.

| key                   | value                      | description                                                  |
| :-------------------- | :------------------------- | :----------------------------------------------------------- |
| id (**required**)     |                            | Sensible uses the ID as the key in the structured key/value output. In the API response, this output is in the `parsed_document` section |
| method (**required**) | object                     | The method describes the Computed Field method used to transform fields. This object's parameters vary depending on the Computed Field method. For more information, see child pages. |
| type                  | string (default: `string`) | Set the eduction type. For more information about types, see [Field query object](doc:field-query-object). |

