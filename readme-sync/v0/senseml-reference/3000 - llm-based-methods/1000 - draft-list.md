---
title: "draft list"
hidden: true
---

TODO: add some wording abt spreadsheets to the intro

|                   |                            |                                                              |
| ----------------- | -------------------------- | ------------------------------------------------------------ |
| detectSpreadsheet | boolean<br/>default: false | Set to true if the document type can include supported spreadsheet [file types](doc:file-types). Enables fast, complete extraction results from large spreadsheets. <br/>If true, then for supported spreadsheet files, Sensible uses an LLM to match your `properties` descriptions to the spreadsheet's column headings, searching in the first four rows of the spreadsheet. It bypasses LLMs to extract all the rows under the specified columns till the end of the spreadsheet. When true, the List method's behavior is similar to the Cell Rows Method, and it can support similarly large spreadsheets. The difference is that instead of using matching text to find column headings, Sensible uses LLMs to find column headings. |
|                   |                            |                                                              |
|                   |                            |                                                              |
|                   |                            |                                                              |



For large spreadsheets with tens of thousands of rows, the Cell Rows field type extracts rows under a specified column-headings row. Sensible extracts rows until the end of the document. The Cell Rows field type is a speedier alternative to general-purpose SenseML methods, which you can use with smaller spreadsheets.

**Notes**:

This method doesn't work with PDFs. You must upload the spreadsheet to Sensible as one of the [supported](doc:file-types) spreadsheet file types.



