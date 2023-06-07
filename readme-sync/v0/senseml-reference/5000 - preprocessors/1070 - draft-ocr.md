---
title: "OCR"
hidden: true
---



Parameters
====

|        |                                                              |                                                              |
| ------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| engine | `amazon`,<br/>`google`,<br>`microsoft`,<br/>`lazarus`,<br/>default: `amazon` | Specifies the OCR engine for this preprocessor. This preprocessor overrides the document type's OCR engine for this config.<br/> - Amazon is the default engine for this preprocessor.<br/>- Microsoft is suited to typewritten and long documents. Lazarus is faster than Microsoft and produces similar output.<br/>- Google is faster than Microsoft and suited to handwriting and short documents (25 pages or under). The Google engine doesn't merge words into lines automatically. Use the Merge Lines preprocessor in your configurations to do so. |
|        |                                                              |                                                              |
|        |                                                              |                                                              |
|        |                                                              |                                                              |
|        |                                                              |                                                              |
|        |                                                              |                                                              |

