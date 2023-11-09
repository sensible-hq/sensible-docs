---
title: "Supported file types"
hidden: true
---



### Sensible app

Using the Sensible app, you can extract data from the following file types:

- PDFs
-  Microsoft Word documents (DOC and DOCX)

### Sensible API and SDK

The Sensible API and SDKs support the following file types:

**Extract methods**

- PDF
- Microsoft Word documents (DOC and DOCX)
- Image formats (JPEG, PNG, and TIFF)

**Classify methods**

- PDF
- Image formats (JPEG, PNG, and TIFF)

## Notes

- When extracting from image file formats, Sensible ignore OCR or OCR preprocessor settings you configure in the document type or SenseML configuration.
- For TIFF documents, SenseML that attempts to return a rendered page returns an error, including:
        - pixel-based methods, such as Box, Checkbox, Signature, and image coordinates found with the Document Range method
              - Key/Value method
     - Fixed Table and Table methods with the Stop parameter specified. Use the Text Table method as an alternative.


