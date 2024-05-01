---
title: "OCR engine"
hidden: false
---
Specifies the optical character recognition (OCR) engine for extracting text from images. For information about additional OCR options, see [OCR](doc:ocr).

## Enums

The following table shows the enums available for the OCR Engine parameter. 

| enum      | description                                                  |
| --------- | ------------------------------------------------------------ |
| Amazon    | Default engine for the OCR preprocessor.                     |
| Microsoft | Default engine for document types.<br/>Suited to typewritten documents and large documents up to 50 MB in size. |
| Lazarus   | Faster than Microsoft and produces similar output.           |
| Google    | Faster than Microsoft and suited to handwriting and documents that are 5 pages or fewer. The Google engine doesn't merge words into lines automatically. Use the Merge Lines preprocessor in your configurations to do so. |

**Note:** When Sensible extracts from [portfolios](doc:portfolio), it uses Microsoft OCR, and ignores any OCR settings in the portfolio's document types.
