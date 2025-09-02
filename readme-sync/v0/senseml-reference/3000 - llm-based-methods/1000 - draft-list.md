---
title: "draft list"
hidden: true
---

TODO: add some wording abt spreadsheets to the intro

|                   |                            |                                                              |
| ----------------- | -------------------------- | ------------------------------------------------------------ |
| detectSpreadsheet | boolean<br/>default: false | Set to true for large spreadsheets for faster and more complete responses. If true, Sensible checks if the document from which to extract data is a [spreadsheet file](doc:file-types).  If it is, Sensible uses an LLM to match your `properties` descriptions to the spreadsheet's column headings, searching in the first few rows of the spreadsheet. It then deterministically extracts all the rows under the specified columns till the end of the spreadsheet. |
|                   |                            |                                                              |
|                   |                            |                                                              |
|                   |                            |                                                              |

