---
title: Supported file types
excerpt: Extract data from PDF, Word, Excel, CSV, JPEG, PNG, and TIFF files. Support for each file format varies by operation.
deprecated: false
hidden: false
metadata:
  title: ''
  description: Extract data from PDF, Word, Excel, CSV, JPEG, PNG, and TIFF files. Support for each file format varies by operation.
  robots: index
next:
  description: ''
---
## File types

Sensible supports the following file types:

- PDF
- Microsoft Word (DOC and DOCX)
- Spreadsheet formats  (XLSX, XLS, XLSM, XLSB, and CSV)
- Single-page image formats (JPEG, PNG)
- Multi-page image formats (TIFF)

For more information, see the following tables.

**Operation context**

| | PDF | Microsoft Word | Spreadsheet formats | JPEG, PNG | TIFF |
  | --- | --- | --- | --- | --- | --- |
  | **Sensible app's Extract tab** | ✅ | ✅ | ✅ | ✅ | ❌ |
  | **Single-file extraction with SDKs or API** | ✅ | ✅ | ✅<sup>1</sup> | ✅ | ✅ |
  | **Portfolio extraction** | ✅ | ✅ | ❌ | ✅<sup>2</sup> | ❌ |
  | **Email bodies** | ✅ | ✅ | ✅ | ✅ | n/a |
  | **Email attachments** | ✅ | ✅ | ✅ | ✅ | ✅ |
  | **Classification by type with SDKs or API** | ✅ | ✅ | ✅<sup>3</sup> | ✅ | ✅ |

**SenseML extraction method**

| | PDF | Microsoft Word | Spreadsheet formats | JPEG, PNG | TIFF |
  | --- | --- | --- | --- | --- | --- |
  | **Methods that render non-text pixels<sup>4</sup>** | ✅ | ✅ | ❌ | ✅ | ❌ |
  | **NLP Table method,<br/>Fixed Table method<sup>5</sup>** | ✅ | ✅ | ❌ | ✅ | ❌ |
  | **Extraction of text that requires OCR** | ✅ | ✅ | ❌ | ✅ | ✅ |


1. For XLS, XLSM, and XLSB files, use an asynchronous extraction endpoint, such as [Extract from URL](ref:extract-from-url) or [Generate an upload URL](ref:generate-an-upload-url). If you use the synchronous [Extract data from a document](ref:extract-data-from-a-document) endpoint, base64-encode the file in the request body's `document` field instead of sending the file bytes as the request body. Specify spreadsheet content types in lowercase, for example, `application/vnd.ms-excel.sheet.binary.macroenabled.12`. For CSV files, the asynchronous extraction endpoints require the `content_type` body parameter, `text/csv`.
2. If you're processing portfolios and expect a mix of image- and non-image files, then you can process single-page image files as portfolios. Sensible returns the first document it identifies in the image file.
3. Sensible doesn't classify CSV files. To classify XLS, XLSM, or XLSB files with the API, specify the XLSX content type, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`. Sensible detects the file's actual format. The Python SDK classifies these files without changes.
   <!-- Internal note: application/pdf also works for classifying XLS, XLSM, XLSB, and XLSX (checked 2026-11-12; the Python SDK hard-codes application/pdf for every file, which is why it classifies these without changes). CSV labeled application/pdf still isn't classified. Not documented on purpose: this is a workaround, so the footnote names one content type rather than every one that works. Sensible doesn't promise to correct a wrong label. -->
   <!-- code test {"testId": "classify_excel_formats_as_xlsx", "description": "XLS, XLSM, and XLSB classify when sent as XLSX or by the Python SDK, but not with their own content types"} -->
   <!-- fixture {"name": "fixture_spreadsheet_classify"} -->
   <!-- expect {"compare": "classification", "requests": [{"file": "commission_statement.xlsx", "as": "xlsx", "classified": true}, {"file": "commission_statement.xls", "as": "xlsx", "classified": true}, {"file": "commission_statement.xlsm", "as": "xlsx", "classified": true}, {"file": "commission_statement.xlsb", "as": "xlsx", "classified": true}, {"file": "commission_statement.xlsb", "as": "pdf", "classified": true, "label": "as the Python SDK sends it"}, {"file": "commission_statement.xls", "as": "xls", "classified": false}, {"file": "commission_statement.xlsm", "as": "xlsm", "classified": false}, {"file": "commission_statement.xlsb", "as": "xlsb", "classified": false}]} -->
   <!-- code test end -->
   <!-- code test {"testId": "classify_csv_not_supported", "description": "Sensible doesn't classify CSV files"} -->
   <!-- fixture {"name": "fixture_spreadsheet_classify"} -->
   <!-- expect {"compare": "classification", "requests": [{"file": "commission_statement.csv", "as": "csv", "classified": false}, {"file": "commission_statement.csv", "as": "pdf", "classified": false, "label": "as the Python SDK sends it"}]} -->
   <!-- code test end -->
4. Methods that render non-text image pixels include pixel-based methods, such as Box, Checkbox, Nearest Checkbox, and Signature methods, [multimodal](doc:query-group#parameters) LLM-based methods, and image coordinates returned by the Document Range method.
5. As alternatives to these Table methods, use the Fixed Table method or the List method.

## File sizes

Sensible supports the following file sizes:

| Operation                       | Size limit for `/extract/{doc-type}` API endpoint | Size limit for asynchronous calls |
| ------------------------------- | ------------------------------------------------- | --------------------------------- |
| Single-document file extraction | under 4.5MB, or under 30 seconds processing time  | 6 GB                              |
| Portfolio extraction            | n/a                                               | 6 GB                              |
| Classification                  | 4.5 MB                                            | 4.5 MB                            |

## File conversions

* **Word documents**: Sensible converts the document to PDF before processing it.
* **Email bodies**: Sensible converts the body to PDF before processing it.
* **Spreadsheet documents**: All [OCR](doc:ocr) settings are inapplicable for this file type. Sensible extracts text directly from the file without OCR. Sensible represents the text both internally and in the Sensible app's editor as follows:
  * Standardizes the formatting of all text in the file. Each cell contains exactly one [line](doc:lines).
  * Standardizes cell height at 0.25'' tall and cell width at 1''. Overflow text in a cell is still available for extraction but isn't viewable in the Sensible app editor unless you click on a line in the rendered document to view its details. 
  * Standardizes the maximum page height at 15 inches. Sensible splits longer sheets into consecutive pages.