---
title: February 2026
slug: february-2026
date: 2026-02-19
---

In the last month, Sensible added deterministic methods for removing unwanted text from documents and for matching rotated text, such as watermarks. We also added advanced transformation logic for large spreadsheet extractions.

## New feature: Remove Lines preprocessor

With the new [Remove Lines](doc:remove-lines)  preprocessor, you can now remove matched text from all pages in a document.  For example, use this preprocessor to remove watermarks or page numbers. This preprocessor is an alternative to the Remove Header and Remove Footer preprocessors and can remove text that varies in position on the page.

## Improvement: Target rotated text

Use the newly released [Angle Filter](doc:match#global-parameters)  parameter to match angled text based on its degrees of rotation. For an example, see the [Remove Lines](doc:remove-lines#examples)  preprocessor.

## Improvement: Advanced JsonLogic operations in large spreadsheet extractions

With the [Cell Row](doc:cell-rows)  field's new support for the [Custom Computation Group](doc:custom-computation-group)  method, you can now transform multiple fields in each extracted spreadsheet row with more concise syntax and faster performance.

## Improvement: Output document file's page count

With the Get File Metadata method's new Page Count enum, you can output the document's page count to the extraction's `parsed_document` output. For more information, see the [Get File Metadata](doc:get-file-metadata)  method.
