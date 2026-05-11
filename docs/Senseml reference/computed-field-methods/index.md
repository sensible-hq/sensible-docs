---
title: Computed field methods
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Transform extracted data'
  robots: index
next:
  description: ''
---

Computed Field methods transform the output of one or more [Field objects](doc:field-query-object).  Sensible supports several general categories for transforming extracted document data:

* Transform document data with built-in logic
* Transform document data with LLMs
* Transform or validate document data with dynamic external context
* Transform document data with custom logic

## Transform document data with built-in logic

Transform document data with logic using computed fields. Common use cases for logic-based computed fields include:

* Clean raw output:  You can strip out unwanted data, such as extra characters or strings, using a Computed Field method. Or, you can split or join data from different fields.
* Standardize output across configs:  If you extract inconsistently formatted data from different vendors or documents, for example "6 month policy period" versus "six mo. policy duration", you can map to a common format. Consistently formatted output helps your application to handle extractions with fewer checks for corner cases.
* Add metadata: If a document lacks information that you want to include in the extraction, you can add it. 
* Pick only selected choices from radio button groups or other groups.

### Parameters

The following global parameters are common to all logic-based Computed Field methods.

| key                   | value                      | description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| :-------------------- | :------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id (**required**)     | string                     | Sensible uses the ID as the key in the structured key/value output. In the API response, this output is in the `parsed_document` section. To specify fallbacks, use the same ID for multiple Computed Field methods. Succeeding fields act as fallbacks if the first returns null. For example, to capture differences in wording between document revisions, define two fields with the same ID, which use synonymous source ids that may be present or absent in different document revisions. |
| method (**required**) | object                     | The method describes the Computed Field method used to transform fields. This object's ID parameter specifies the method, for example, [Concatenate](doc:concatenate) or [Zip](doc:zip).                                                                                                                                                                                                                                                                                                         |
| type                  | string (default: `string`) | Specifies the type of the output value. For more information about types, see [Field query object](doc:field-query-object).                                                                                                                                                                                                                                                                                                                                                                      |

## Transform document data with LLMs

You can set the output of other fields as the [context](doc:prompt) for other LLM-based fields' prompts. In other words, prompt an LLM to answer questions about other fields' extracted data. Use other fields as context to:

* Reformat or otherwise transform the outputs of other fields.
* Compute or generate new data from the output of other fields
* Narrow down the [context](doc:prompt) for your prompts to a specific part of the document.
* Troubleshoot or simplify complex prompts that aren't performing reliably. Break the prompt into several simpler parts, and chain them together using successive Source ID parameters in the fields array.

To use other fields as context, configure the Source Ids parameter for the [Query Group](doc:query-group) or [List](doc:list#parameters) methods. 

## Transform or validate document data with dynamic external context

Document extraction rarely happens in isolation. Workflows involve multiple documents, upstream systems, and business logic that exists outside any single file. To  For example:

- a mortgage pipeline might need to cross-check a bank statement against figures extracted from a loan application document in the same overall application package. 

- A document LLM agent might need to carry context generated in a previous reasoning step into the next extraction call. 

In such cases, you can provide the external context as an `extra_data` object when you make an extraction call. You can then make that request-time context available in an extraction config so computed fields, including LLM-based methods, can operate on it. For more information, see the [Extra data](doc:extra-data) method.

## Transform document data with custom logic

For advanced computations including custom logic, see [Advanced computed field methods](doc:advanced-computed-field-methods).
