---
title: "Preprocessors"
hidden: false
---
Use the following preprocessors to clean up your documents before extracting structured data. Preprocessors execute in the order you define them in an array.



| Preprocessor                           | Image                                                        | Notes                                                        |
| -------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **[Deskew](doc:deskew)**               | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_deskew.png) | Corrects the alignment of documents that are skewed, for example as a result of being photographed at an angle instead of straight on. |
| **[Ligature](doc:ligature)**           | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_ligature.png) | Intelligently replaces Unicode ligatures with text characters in a text extraction. |
| **[Merge Lines](doc:merge-lines)**     | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/merge_lines_oversplit_1.png) | Corrects oversplit lines.                                    |
| **[Multicolumn](doc:multicolumn)**     | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_multicolumn.png) | Recognize multi-column formats                               |
| **[NLP](doc:nlp)**                     |                                                              | Advanced prompt configuration for each large language model (LLM)-based method in a config. |
| **[OCR](doc:ocr-preprocessor)**        | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_ocr.png) | Selectively OCRs pages in documents containing a mix of digitally generated text and text images (such as scanned text). If the whole PDF is a scan, you don't need to configure this preprocessor. |
| **[Page Range](doc:page-range)**       |                                                              | Ignores pages outside the start page and end page.           |
| **[Remove Header](doc:remove-header)** | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/remove_header_1.png) | Removes repeating elements at the top of the page. Ignores header elements that overlap with the page's main body. |
| **[Remove Footer](doc:remove-footer)** | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/remove_footer_1.png) | Removes repeating elements at the bottom of the page. Ignores footer elements that overlap with the page's main body. |
| **[Remove Page](doc:remove-page)**     | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/remove_page.png) | Removes pages that match the specified text.                 |
| **[Rotate page](doc:rotate-page)**     | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/rotate_page_2.png) | In most cases, Sensible corrects page rotation automatically. If it doesn't, configure this preprocessor. |
| **[Scale](doc:scale)**                 | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_scale.png) | Corrects the size of text in documents whose size varies, for example as a result of being scanned or photographed at different scales. |
| **[Split Lines](doc:split-lines)**     | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/thumbnail_split_lines.png) | Corrects undersplit lines.                                   |



