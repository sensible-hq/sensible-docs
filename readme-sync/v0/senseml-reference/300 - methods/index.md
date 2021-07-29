---
title: "Methods"
hidden: false
---
Use the following [methods](doc:method-object)  to extract structured data from documents:



| Method                                   | Image                                                        | Notes                                                        |
| ---------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **[Box](doc:box)**                       | ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_box.png) | Extract contents from boxes with continuous borders.         |
| **[Checkbox](doc:checkbox)**             | ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_checkbox.png) | Extract true/false from checkbox.                            |
| **[Column](doc:column)**                 | ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_column.png) | Extract text aligned in a column, from an anchor down to the bottom of the page. |
| **[Document Range](doc:document-range)** | ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_document_range.png) | Extract paragraphs, or extract image metadata (coordinates). |
| **[Fixed Table](doc:fixed-table)**       | ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_fixed_table.png) | Extract tables whose column headings never vary.             |
| **[Invoice](doc:invoice)**               | ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_invoice.png) | Extract invoice and metadata.                                |
| **[Label](doc:label)**                   | ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_label.png) | Extract a line of text that is proximate to another line.    |
| **[Passthrough](doc:passthrough)**       | ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_passthrough_and_regex.png) | Return anchor text, optionally using RegEx.                  |
| **[Regex](doc:regex)**                   |                                                              | Use RegEx capturing groups to clean up extracted data in combination with the Passthrough method. |
| **[Region](doc:region)**                 | ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_region.png) | Extract data from a rectangular region defined by coordinates. Faster alternative to Box method. |
| **[Row](doc:row)**                       | ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_row.png) | Extract text aligned in a row.                               |
| **[Table](doc:table)**                   | ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_table.png) | Extract a table whose column headings vary.                  |
| **[Text Table](doc:text-table)**         | ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_text_table.png) | Fast but limited table extraction using only text positioning data. |

