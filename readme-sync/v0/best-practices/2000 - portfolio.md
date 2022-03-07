---
title: "Extracting handwriting"
hidden: true

---

This topic contains tips and tricks for extracting handwriting:

- **Choosing an OCR engine** Google OCR instead of Microsoft OCR. To configure OCR, click the gear icon for the Document Type and select **Google**: 

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/merge_lines_ocr_1.png)

  

- **Defining regions** can occupy an unpredictable region or even overlap other lines. Rather than attempting to draw a large region to encapsulate the handwriting, it's sometimes better to draw a box with a small height and long width that runs through the middle of the handwriting, as the following image shows:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/handwriting_1.png) 

  For more information about how Sensible determines whether to extract a line that partially overlaps a region, see [Region](doc:region).

- **Correcting for vertical misalignment** jitter in the vertical positions of handwritten lines can cause Sensible to incorrectly sort lines that a human reader interprets as following left to right. The Sort Lines parameter corrects this problem by sorting lines by their likely reading order. For more information, see [the Sort Lines example](doc:method#sort-line-example).



