---
title: "Methods"
hidden: true
---
Use the following [methods](doc:method)  to extract structured data from documents.

See also [other extraction methods](doc:other-extraction-methods) for extracting data that do not fit into one of the folllowing methods.

| Method                                   | Image                                                        | Notes                                                        |
| ---------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **[Box](doc:box)**                       | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_box.png) | Extracts contents from boxes with continuous borders.        |
| **[Checkbox](doc:checkbox)**             | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_checkbox.png) | Extracts true/false from checkboxes.                         |
| **[Column](doc:column)**                 | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_column.png) | Extracts text aligned in a column, from an anchor down to the bottom of the page. |
| **[Document Range](doc:document-range)** | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_document_range.png) | Extracts paragraphs, or extract image metadata (coordinates). |
| **[Fixed Table](doc:fixed-table)**       | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_fixed_table.png) | Extracts tables where column headings never vary.            |
| **[Intersection](doc:intersection)**     | ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intersection_example_1.png) | Extracts a target line at the intersection of a horizontal line defined by an anchor, and a vertical line defined by a second anchor. |
| **[Invoice](doc:invoice)**               | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_invoice.png) | Extracts an invoice and metadata.                            |
| **[Label](doc:label)**                   | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_label.png) | Extracts a line of text that is proximate to another line.   |
| **[Passthrough](doc:passthrough)**       | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_passthrough_and_regex.png) | Returns anchor text, optionally using RegEx.                 |
| **[Regex](doc:regex)**                   |                                                              | Extracts text matching RegEX. Use RegEx capturing groups in this method to clean up extracted data in combination with the Passthrough method. |
| **[Region](doc:region)**                 | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_region.png) | Extracts data from a rectangular region defined by coordinates. Faster alternative to Box method. |
| **[Row](doc:row)**                       | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_row.png) | Extracts text aligned in a row.                              |
| **[Table](doc:table)**                   | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_table.png) | Extracts a table where column headings vary.                 |
| **[Text Table](doc:text-table)**         | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_text_table.png) | Extracts tables using only text-positioning data (fast but limited). |

