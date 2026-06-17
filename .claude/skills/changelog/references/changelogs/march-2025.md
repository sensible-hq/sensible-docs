---
title: March 2025
slug: march-2025
date: 2025-02-11
---

In the last month, Sensible released a powerful new feature for conditionally executing extraction fields. For very large spreadsheets, Sensible introduced a speedy cell-extraction method. For research papers and other multi-column document layouts, Sensible introduced a new Multicolumn preprocessor. Sensible also released a new confidence signal, `inferred_answer`, for qualifying LLM accuracy; enabled combining single-document and portfolio extractions into a single Excel file, and released advanced output schema manipulation features.

## New feature: Conditional execution for data-extraction fields

With the newly released Conditional method, Sensible introduces conditional logic for executing data-extraction fields. This method extracts alternate sets of fields, depending on a [logical](doc:jsonlogic)  condition. 

```
id: conditional
condition: JsonLogic # condition about already extracted fields. must output a boolean 
fieldsOnPass: [] # fields to extract if the boolean is true
fieldsOnFail: [] # fields to extract if the boolean is false

```

 Use the Conditional method to handle document variations in a document type. For example, you want to extract data from two affiliate banks' statements. The statements' layouts are so similar that you can reuse 90 percent of your SenseML queries to handle both. Rather than authoring two separate configs, you can handle the remaining 10 percent with conditional field execution.

For more information, see the [Conditional](doc:conditional) method.

## New feature: Multicolumn preprocessor

With the new Multicolumn preprocessor, Sensible expands its capacity to extract from research papers and other commonly multicolumn documents. This preprocessor ensures that Sensible sorts lines into columns when present, rather than the default behavior of sorting lines left to right across the page. It's a more powerful and flexible alternative to the existing [Paragraph](doc:paragraph)  method. 

For more information, see the [Multicolumn](doc:multicolumn)  preprocessor.

## Improvements: Combine single-document and portfolio extractions in Excel

When you select a group of document extractions to combine into an Excel spreadsheet, you can now mix [portfolio](doc:portfolio) and single-document extractions in the group. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_march2025_excel.png)

Sensible combines the extractions with metadata about the source documents into one Excel file:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_march2025_excel_2.png)

For more information about how Sensible converts extracted JSON data to Excel, see [SenseML to Excel reference](doc:excel-reference). 

## New feature: Optimize extracting from large spreadsheets

Sensible can now extract rows from large spreadsheets with tens of thousands of rows in seconds. The new Cell Rows field type extracts rows under a specified column-headings row until the end of the document. The Cell Rows field type is a speedier alternative to general-purpose SenseML methods, which you can use with smaller spreadsheets.

For more information, see [Spreadsheet extraction](doc:cell-rows).

## New feature: Qualify LLM accuracy with Inferred Answer confidence signal

Sensible adds nuance to qualifying LLM accuracy with the new `inferred_answer` confidence signal. This signal indicates that the LLM inferred the answer to the prompt rather than finding the exact answer in the document. For example, a document lists subtotals of $15 and $30 but no grand total. If you prompt `what's the grand total?`, the LLM can return `45` along with this confidence signal.

For more information, see [Qualifying LLM accuracy](doc:confidence). 

## New feature: Advanced Omit Fields operation

The newly released Omit Fields operation joins Sensible's extended support for [JsonLogic](doc:jsonlogic)  operations. This operation transforms your output schema by selectively copying a list of fields from one object to another, omitting a list of specified fields.\
For more information, see [Omit Fields](doc:jsonlogic#omit_fields).
