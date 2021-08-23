---
title: "Methods"
hidden: false
---
Use the following [methods](doc:method)  to extract structured data from documents:



| Method                                   | Image                                                        | Notes                                                        |
| ---------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **[Box](doc:box)**                       | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/thumbnail_box.png) | Extract contents from boxes with continuous borders.         |
| **[Checkbox](doc:checkbox)**             | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/thumbnail_checkbox.png) | Extract true/false from checkbox.                            |
| **[Column](doc:column)**                 | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/thumbnail_column.png) | Extract text aligned in a column, from an anchor down to the bottom of the page. |
| **[Document Range](doc:document-range)** | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/thumbnail_document_range.png) | Extract paragraphs, or extract image metadata (coordinates). |
| **[Fixed Table](doc:fixed-table)**       | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/thumbnail_fixed_table.png) | Extract tables whose column headings never vary.             |
| **[Invoice](doc:invoice)**               | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/thumbnail_invoice.png) | Extract invoice and metadata.                                |
| **[Label](doc:label)**                   | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/thumbnail_label.png) | Extract a line of text that is proximate to another line.    |
| **[Passthrough](doc:passthrough)**       | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/thumbnail_passthrough_and_regex.png) | Return anchor text, optionally using RegEx.                  |
| **[Regex](doc:regex)**                   |                                                              | Use RegEx capturing groups to clean up extracted data in combination with the Passthrough method. |
| **[Region](doc:region)**                 | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/thumbnail_region.png) | Extract data from a rectangular region defined by coordinates. Faster alternative to Box method. |
| **[Row](doc:row)**                       | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/thumbnail_row.png) | Extract text aligned in a row.                               |
| **[Table](doc:table)**                   | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/thumbnail_table.png) | Extract a table whose column headings vary.                  |
| **[Text Table](doc:text-table)**         | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/borders/thumbnail_text_table.png) | Fast but limited table extraction using only text positioning data. |

