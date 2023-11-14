---
title: "OCR engine"
hidden: false
---
For information about the OCR engine options you can set for a document type, see [OCR preprocessor](doc:ocr).

## Enums

The following table shows the enums available for the OCR Engine parameter. 

| enum      | description                                                  |
| --------- | ------------------------------------------------------------ |
| Amazon    | default engine for the OCR preprocessor                      |
| Microsoft | suited to typewritten documents and large documents up to 50 MB in size. Microsoft is the default document type for document types. |
| Lazarus   | faster than Microsoft and produces similar output.           |
| Google    | faster than Microsoft and suited to handwriting and documents that are 5 pages or fewer. The Google engine doesn't merge words into lines automatically. Use the Merge Lines preprocessor in your configurations to do so. |
