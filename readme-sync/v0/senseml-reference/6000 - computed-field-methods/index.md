---
title: "Computed field methods"
hidden: false
---
Computed Field methods transform the output of one or more [Field objects](doc:field-query-object).  Sensible supports several broad methods for transforming extracted document data:

- Logic-based computed field methods.
- LLM-based prompts
- Custom logic-based computed field methods 

## Logic-based computed field methods

Common use cases for logic-based computed fields include:

- Clean up raw output:  If the output contains extra characters, strings, etc, you can often use a Computed Field method to strip out the unwanted data. Or, you can split or join data from different fields.
- Standardize output across configs:  If you extract inconsistently formatted data from different vendors or documents, for example "6 month policy period" versus "six mo. policy duration", you can map to a common format. Consistently formatted output helps your application to handle extractions with fewer checks for corner cases.
- Add metadata: If a document lacks information that you want to include in the extraction, you can add it. 
- Pick only selected choices from radio button groups or other groups.

### Parameters


The following global parameters are common to all logic-based Computed Field methods.

| key                   | value                      | description                                                  |
| :-------------------- | :------------------------- | :----------------------------------------------------------- |
| id (**required**)     | string                     | Sensible uses the ID as the key in the structured key/value output. In the API response, this output is in the `parsed_document` section. To specify fallbacks, use the same ID for multiple Computed Field methods. Succeeding fields act as fallbacks if the first returns null. For example, to capture differences in wording between document revisions, define two fields with the same ID, which use synonymous source ids that may be present or absent in different document revisions. |
| method (**required**) | object                     | The method describes the Computed Field method used to transform fields. This object's ID parameter specifies the method, for example, [Concatenate](doc:concatenate) or [Zip](doc:zip). |
| type                  | string (default: `string`) | Specifies the type of the output value. For more information about types, see [Field query object](doc:field-query-object). |

## LLM-based prompts

You can set the output of other fields as the [context](doc:prompt#notes) for other LLM-based fields' prompts. In other words, prompt an LLM to answer questions about other fields' extracted data. Use other fields as context to:

- Reformat or otherwise transform the outputs of other fields.
- Compute or generate new data from the output of other fields
-  Narrow down the [context](doc:prompt#notes) for your prompts to a specific part of the document.
- Troubleshoot or simplify complex prompts that aren't performing reliably. Break the prompt into several simpler parts, and chain them together using successive Source Ids in the fields array.

To transform extracted document data using LLMs, configure the Source Ids parameter for the [Query Group](doc:query-group).

## Custom logic-based computed field methods

For advanced computations including custom logic, see [Advanced computed field methods](doc:advanced-computed-field-methods).

