---
title: "Supported file types"
hidden: false
---

Sensible supports the following file types:

### Sensible app

Using the Sensible app, you can extract data from the following file types:

- PDF
- Microsoft Word documents (DOC and DOCX)

### Sensible SDKs and API

The Sensible SDKs and API support the following file types:

**Extraction**

single-document file:

- PDF
- Microsoft Word documents (DOC and DOCX)
- pageless image formats (JPEG, PNG)
- paginated image format (TIFF)

multi-document file ("portfolio" file):

- PDF
- Microsoft Word documents (DOC and DOCX)

**Classification**

- PDF
- Image formats (JPEG, PNG, and TIFF)

## Notes

- When extracting from image file formats, Sensible ignore OCR or OCR preprocessor settings you configure in the document type or SenseML configuration.
- For TIFF documents, SenseML that attempts to return a rendered page returns an error, including:
        - pixel-based methods, such as Box, Checkbox, Signature, and image coordinates found with the Document Range method
              - Key/Value method
     - Fixed Table and Table methods with the Stop parameter specified. Use the Text Table method as an alternative.

