---
title: "Methods"
hidden: 
---
Use the following  [methods](doc:method)  to extract structured data from documents. 





## Layout-based methods

| Method                                       | Image                                                        | Notes                                                        |
| -------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **[Box](doc:box)**                           | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/box_1099.png) | Extracts contents from boxes with continuous borders.        |
| **[Checkbox](doc:checkbox)**                 | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main//readme-sync/assets/v0/images/final/checkbox.png) | Extracts true/false for the selection status of  checkboxes. |
| **[Column](doc:column)**                     | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/column.png) | Extracts text aligned in a column, from an anchor down to the bottom of the page. |
| **[Document Range](doc:document-range)**     | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/documentrange_sworn.png) | Extracts text in a range, or extract image metadata (coordinates).  Simpler alternative to the advanced [Paragraph](doc:paragraph) method. |
| **[Fixed Table](doc:fixed-table)**           | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/fixed_table.png) | Extracts tables where column headings never vary.            |
| **[Intersection](doc:intersection)**         | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intersection_1.png) | Extracts a target line at the intersection of a horizontal line defined by an anchor, and a vertical line defined by a second anchor. |
| **[Label](doc:label)**                       | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/labels.png) | Extracts a line of text that's proximate to another line.    |
| [**Nearest Checkbox**](doc:nearest-checkbox) | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/nearest_checkbox.png) | Extracts true/false for the selection status of the checkbox nearest to the anchor. |
| [**Paragraph**](doc:paragraph)               | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/paragraph.png) | Extracts paragraphs that partially span the page width, for example from columnar layouts. |
| **[Passthrough](doc:passthrough)**           | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/passthrough.png) | Extracts anchor text, optionally using RegEx.                |
| **[Regex](doc:regex)**                       |                                                              | Extracts text matching RegEx. Use RegEx capturing groups in this method to clean up extracted data in combination with the Passthrough method. |
| **[Region](doc:region)**                     | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/region_ssn.png) | Extracts data from a rectangular region defined by coordinates. Faster alternative to Box method. |
| **[Row](doc:row)**                           | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/row.png) | Extracts text aligned in a row.                              |
| **[Signature](doc:signature)**               |                                                              | Extracts true/false for the signed status of  a region.      |
| **[Text Table](doc:text-table)**             | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/text_table.png) | Extracts tables using solely text-positioning data (fast but limited). |

## Large language model (LLM)-based methods

See [LLM-based methods](doc:llm-based-methods).

