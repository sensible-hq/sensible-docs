---
title: January 2023
slug: january-2023
date: 2023-01-06
---

In the last month, we introduced a powerful new way to ask a simple question about data in a document and get back an NLP-powered answer, and added the ability to combine multiple document extractions into one Excel spreadsheet. We also improved OCR preprocessors, and made SenseML syntax more concise for a few NLP methods.

## New feature: Ask a free-text question, get document data

Using our new [Question](doc:query) method, you can now ask a simple question in SenseML, like "What's the document date?" and get back an answer. This method works best with questions that have one short answer in the document. This method lets you get started with SenseML quickly, since you don't need to know much about the document's layout.

```
      "method": {
        "id": "question",
        "question": "in the table, what's the comprehensive premium"
        }
```

## New feature: Combine multiple document extractions into one Excel spreadsheet

You can now generate an Excel file from multiple document extractions using the [Get Excel extraction](ref:get-excel-extraction) endpoint.  For example, you can compile documents' data as rows in a single sheet with common column headings.

For more information, see the [SenseML to spreadsheet reference](doc:excel-reference#multi-document-spreadsheet). 

## Feature improvement: Concise syntax for Question and Topic methods with optional anchor

For the natural-language [Question](doc:query) and [Topic](doc:topic) methods, you can now skip specifying an anchor for more concise syntax.  If you specify an anchor, you can narrow Sensible's search down from the whole document to a whole page or page range, depending on the method.

## Feature improvements: OCR engine

You can now select the Amazon OCR engine in the Sensible app, not just in the Sensible API. The engine now detects rotated pages. 

Sensible now skips OCR preprocessors for image-formatted document files. For example, if you have the same business form in multiple file formats, you can now configure an OCR preprocessor for the PDF-formatted instances of the business form, without breaking extractions from TIFF-formatted instances of the business form.
