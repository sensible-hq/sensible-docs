---
title: "Preprocessors"
hidden: false
---
Use the following preprocessors to clean up your documents before extracting structured data. Preprocessors execute in the order you define them in an array.



| Preprocessor                           | Image                                                        | Notes                                                        |
| -------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **[Deskew](doc:deskew)**               | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_deskew.png) | Corrects the alignment of PDF documents that are skewed, for example as a result of being photographed at an angle instead of straight on. |
| **[Ligature](doc:ligature)**           | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_ligature.png) | Intelligently replaces Unicode ligatures in a PDF text extraction. |
| **[Merge Lines](doc:merge-lines)**     | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_merge_lines.png) | Corrects oversplit lines.                                    |
| **[OCR](doc:ocr)**                     | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_ocr.png) | Selectively OCRs pages in PDFs containing a mix of digitally generated text and text images (such as scanned text). If the whole PDF is a scan, you don't need to configure this preprocessor. |
| **[Page Filter](doc:page-filter)**     |                                                              | Filters out low-scoring pages given a bag of target terms and stop terms. |
| **[Page Range](doc:page-range)**       |                                                              | Ignores pages outside the start page and end page.           |
| **[Remove Header](doc:remove-header)** | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_remove_header.png) | Removes repeating elements at the top of the page.  Ignores header elements that overlap with the page's main body. |
| **[Remove Footer](doc:remove-footer)** | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_remove_footer.png) | Removes repeating elements at the bottom of the page. Ignores footer elements that overlap with the page's main body. |
| **[Split Lines](doc:split-lines)**     | ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/thumbnail_split_lines.png) | Corrects undersplit lines.                                   |



