---
title: Introduction
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Welcome to Sensible! If you have any questions, please reach out by chat or [support@sensible.so](mailto:support@sensible.so) and we'd be happy to help you out. 

To get started, see the following endpoints. Or, see other [integration](doc:integrate)  options.

[block:parameters]
{
  "data": {
    "h-0": "Endpoints",
    "h-1": "Links",
    "h-2": "Notes",
    "0-0": "Document extraction (asynchronous)",
    "0-1": "- [Extract doc at a Sensible URL](ref:generate-upload-url) <br/>\n- [Extract doc at your URL](ref:extract-from-url)",
    "0-2": "Takes a document file, such as a PDF, and returns extracted data asynchronously. Use the asynchronous endpoints in production.  You have two options for asynchronously extracting from your document:<br/> - extract a doc at a URL you provide<br/>- upload and extract the doc at a Sensible URL. <br/>You can then call the [Retrieve extraction](ref:retrieving-results)  endpoint to get the results, or specify a webhook for Sensible to push the results to as soon as they're ready.<br/> ",
    "1-0": "Document extraction (synchronous)",
    "1-1": "[Extract data from a document](ref:extract-data-from-a-document)",
    "1-2": "Returns extracted document data synchronously. Use this endpoint for testing.",
    "2-0": "Get Excel from PDFs",
    "2-1": "[Get Excel extraction](ref:get-excel-extraction)",
    "2-2": "Get well-structured Excel files converted from PDF documents. This endpoint also supports documents formatted as images, for example, PNG or JPEG.",
    "3-0": "Portfolio extraction (asynchronous)",
    "3-1": "- [Extract portfolio at a Sensible URL](ref:generate-upload-url-portfolio) <br/> - [Extract portfolio at your URL](ref:extract-from-url-portfolio)",
    "3-2": "Use these endpoints with multiple documents that are packaged into one PDF file (a PDF \"portfolio\").",
    "4-0": "Document type classification",
    "4-1": "[Classify document by type](ref:classify-document-sync)",
    "4-2": "Classifies a document by its similarity to document types you define in your Sensible account."
  },
  "cols": 3,
  "rows": 5,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]