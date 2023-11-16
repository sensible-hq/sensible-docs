---
title: "Supported file types"
hidden: false
---

Sensible supports the following file types:

### Sensible app

Using the Sensible app, you can extract data from the following file types:

- PDF
- Microsoft Word documents (DOC and DOCX). 

### Sensible SDKs and API

The Sensible SDKs and API support the following file types:

**Extraction** 

single-document file:

- PDF
- Microsoft Word documents (DOC and DOCX)
- image formats (JPEG, PNG, and TIFF)

multi-document file ("portfolio" file):

- PDF
- Microsoft Word documents (DOC and DOCX)

**Classification**

- PDF
- Microsoft Word documents (DOC and DOCX)
- Image formats (JPEG, PNG, and TIFF)

## Notes

- When extracting from image file formats, Sensible ignore OCR or OCR preprocessor settings you configure in the document type or SenseML configuration.
- For DOC and DOCX documents, Sensible converts the document to PDF before processing it to ensure identical processing behavior.
- For TIFF documents, SenseML methods that attempts to return a rendered page returns an error, including:
     - pixel-based methods, such as Box, Checkbox, Signature, and image coordinates returned by the Document Range method
     - Key/Value method
     - Fixed Table and Table methods with the Stop parameter specified. Use the Text Table method as an alternative.

