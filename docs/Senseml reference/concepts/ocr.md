---
title: OCR
excerpt: Optical character recognition overview
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Optical character recognition overview'
  robots: index
next:
  description: ''
---
When you [extract document data with Sensible](doc:getting-started-ai), Sensible automatically performs optical character recognition (OCR) on the document for you, except in advanced cases. If the document doesn't require OCR, Sensible automatically extracts embedded text directly from the document to optimize performance.

For advanced cases, you can configure how Sensible OCRs documents using the following parameters:

| option                                   | configurable for | notes                                                                                                    |
| ---------------------------------------- | ---------------- | -------------------------------------------------------------------------------------------------------- |
| [OCR Level parameter](doc:ocr-level)     | document types   | Use this option to configure the criteria by which Sensible determines if a whole document requires OCR. |
| [OCR preprocessor](doc:ocr-preprocessor) | configs          | Use this option to OCR specified pages or page ranges in a document.                                     |
| [OCR Engine](doc:ocr-engine) parameter   | document types   | Use this option to choose your OCR provider, for example, Amazon, Google, or Microsoft.                  |

For an overview of how Sensible handles OCR for supported [file type](doc:file-types), see the following steps:

1. Sensible converts several file types to PDFs.  For more information, see supported [file types](doc:file-types#file-conversions).
2. For file types that contain embedded text (for example, digital PDFs), Sensible extracts the text directly. If it completes this step, it skips the following steps.
3. For file types that lack embedded text, Sensible transforms the bytes of the document into raw text, and determines whether the document needs OCR:

   * If the file type is an image (for example, PNG), Sensible runs OCR for the whole document, as specified by the document type's OCR Engine parameter.

   * **(Configurable)** if the file is a PDF, Sensible processes the file using heuristics to determine if the whole document needs OCR.  Configure this step using the document type's OCR Level parameter and OCR Engine.
4. **(Configurable)** After additional intervening steps, Sensible applies your configured preprocessors, including the OCR preprocessor. This preprocessor runs for documents that don't trigger whole-document OCR in a previous step. 

## Notes

* For more information about OCR versus embedded text extraction, see [Solving direct text extraction from PDFs](https://www.sensible.so/blog/solving-direct-text-extraction-from-pdfs).

* For information about extracting data from non-text images, such as photographs, charts, or illustrations, see the [Query Group](doc:query-group) method's Multimodal Engine parameter. You can use the LLM-based Multimodal Engine parameter as an alternative to OCR to extract from poor-quality text images, such as handwriting.
