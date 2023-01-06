---
title: "Extracting handwriting"
hidden: false
---

This topic contains tips and tricks for extracting handwriting:

- **Choosing an OCR engine:** Choose Google OCR. To configure OCR, click the gear icon for the Document Type and select **Google**: 

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/merge_lines_ocr_1.png)

  

- **Defining regions:** Handwriting can occupy an unpredictable region or even overlap other lines. Rather than defining a large region to contain the handwriting, Sensible recommends defining a region with a small height and long width that runs through the middle of the handwriting. The following image shows this approach: 

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/handwriting_1.png) 

  For more information about how Sensible determines whether to extract a line that partially overlaps a region, see [Region](doc:region).

- **Correcting for vertical misalignment:** Jitter in the vertical positions of handwritten lines can cause Sensible to incorrectly sort lines that a human reader interprets as following left to right. The Sort Lines parameter corrects this problem by sorting lines by their likely reading order. For more information, see [Sort Lines example](doc:method#sort-line-example).







