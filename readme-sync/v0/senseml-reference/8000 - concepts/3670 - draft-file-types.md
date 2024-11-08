---
title: "Supported file types"
hidden: true
---


3. 

MY TESTS:


|                    | PDF  | Microsoft Word<br/> (DOC and DOCX) | Microsoft Excel<sup>2</sup><br/>(XLSX) | single-page image formats<br/> (JPEG, PNG) | multi-page image formats<br> (TIFF) |
| -------------------------------------- | ---- | ---------------------------------- | --------------------------------------- | --------------------------------------- | --------------------------------------- |
| -                                                            |                       |                                    |                                                              |                                            |                                                              |
|                                                              |                       |                                    |                                                              |                                            |                                                              |
| MY TESTS w null fields on checkbox, nearestCheckbox, box, multimodal | as expected no errors | as expected no errors | unexpected: **no errors** except on MULTIMODAL               | no errors             | **unexpected: no errors** only nulls when field was gonna return null anyway. when field is potentially non-null, then you get the expected errors. |
| *OCR-based methods<sup>2</sup>*                              | ✅                     | ✅                     | ❌                                                            | ✅                     | ❌                                                            |
| My tests w/ null fields on NLP Table (I assume "detectTableStruct" makes no difference) and Fixed Table no stop (**MIcrosoft OCR**) | as expected no errors | as expected no errors | **unexpected**: unsupported image type on NLP TABLE BUT NONE on Fixed Table w/ No Stop | as expected no errors | **unexpected**: unsupported image type on NLP TABLE BUT NONE on Fixed Table w/ No Stop, even though it did return null |
| *misc*                                                       |                       |                       |                                                              |                       |                                                              |
| Fixed Table w Stop (Amazon table recognition)                |                       |                       | null + error message   (unsupported image type)              | as expected no errors | null + error message   (unsupported image type)              |

