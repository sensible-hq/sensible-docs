---
title: "Zapier overview"
hidden: false

---

Introduction
----

If you're trying to convert a PDF into an Excel spreadsheet, you often find tools that copy the PDF's visual layout into a spreadsheet, with no meaningful relationship between the extracted text and the underlying cells. 

In contrast, Sensible converts document tables, checkboxes, paragraphs, and even complex repeating section layouts into meaningfully labeled column/row pairs and linked sheets. You can convert documents formatted as PDFs, PNGs, TIFFs, and JPEGs.

Prerequisites
----


To get a document's data into a spreadsheet, you must first:

- Configure extractions for a document type, either by authoring an extraction configuration using Sensible, or by using Sensible's [open-source configuration library](https://app.sensible.so/library) for common document types.   

- Run an extraction on a target document that belongs to your configured document type using the [Sensible app](https://app.sensible.so/quick-extraction) (single-document conversion) or the [Sensible API](https://docs.sensible.so/reference/choosing-an-endpoint) (multiple document extraction). 

Compile PDFs into one spreadsheet
----

To combine multiple PDFs  into one multi-document spreadsheet, use the [Sensible API](https://docs.sensible.so/reference/get-excel-extraction).


Next
----

TODO update links?

- For more information about how Sensible converts JSON document extractions to Excel, see [SenseML to spreadsheet reference](doc:excel-reference).
- For a tutorial about converting a PDF to an Excel sheet using the Sensible app, see [Getting started with out-of-the-box extraction](doc:excel-quickstart).
- See the [Getting started with SenseML](doc:getting-started) to learn how to extract from your custom documents or tweak Sensible's [open-source configuration library](https://app.sensible.so/library/).
