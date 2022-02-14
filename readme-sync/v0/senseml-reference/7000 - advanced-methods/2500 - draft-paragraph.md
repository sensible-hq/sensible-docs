---
title: "Paragraph"
hidden: true
---
Extracts paragraphs by recognizing various paragraph layouts, including paragraphs in columns and paragraphs that span pages. 



[**Parameters**](doc:document-range#parameters)
[**Examples**](doc:document-range#examples)
[**Notes**](doc:document-range#notes)

Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key               | value       | description                                                  |
| ----------------- | ----------- | ------------------------------------------------------------ |
| id (**required**) | `paragraph` | Prints to console the array of detected "paragraphs". A "paragraph" is a set of lines where each one is not more than 0.5*fontSize below the previous one is considered a paragraph. The anchor can't span multiple lines (this can be a problem if the paragraph 'reflows' and its breaks aren't predictible) |
|                   |             |                                                              |
|                   |             |                                                              |
|                   |             | .                                                            |

Examples
====




Notes
====

paragraphs method vs document range method:
