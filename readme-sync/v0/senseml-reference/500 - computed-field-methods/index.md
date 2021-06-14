---
title: "Computed Field Methods"
hidden: false
---
Computed field methods take the output of one or more [Field objects](doc:field-query-object), and perform a transformation on that field output. Common use cases for computed fields include:

- Clean up raw output:  If the output contains extra characters, strings, etc, you can often use a Computed Field method to strip out the unwanted data. Or, you can split or join data from different fields.
- Standardize output across configs:  If you extract inconsistently formatted data from different vendors or documents, for example "6 month policy period" versus "6 mo. policy duration", you can map to a common format using a Computed Field method.  Consistently formatted output helps your application to handle extractions with fewer checks for corner cases
- Add metadata: If a PDF lacks information that you want to include in the extraction, you can add it using a Computed Field method. For example, perhaps a vendor *exclusively* issues 6-month policy quotes, so they never state the policy period in the PDF. You can add that information.

Parameters
====
| key               | value                      | description                                                  |
| :---------------- | :------------------------- | :----------------------------------------------------------- |
| id (**required**) | string                     | A string that identifies the field in the output             |
| type              | string (default: `string`) | Set the eduction type. For more information about types, see [Field query object](doc:field-query-object). Doesn't apply to the `summarizer` and `tfidf` computed field methods. |
| method            | a Computed Field method    | The method used to create this field. See the child pages of this topic for the full list of available methods. |

