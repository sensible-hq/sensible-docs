---
title: "OCR Level"
hidden: true
---
TODO: still true? The OCR level for a given document type is the minimum OCR level amongst its configurations. --> TODO clarify, what does this actually do? isn't it always a function of the config? if you set doc_type, does it override any 'unset' configs (configs without ocr_level) only? 


- 0: no OCR.
 
 If you choose a higher OCR level, Sensible automatically OCRs documents if they contain unmapped fonts or low-quality embedded text likely caused by OCR.
 Further configure OCR behavior as follows:
 
- 2: (Sensible app default) - Sensible averages the number of lines per page in the document, and if it's fewer than 10, Sensible runs OCR on the whole document.
- 4: Sensible always renders the first page and tests it to determine whether to run OCR on the whole document.
- 5: Level 5 is the same as portfolio OCR detection: we iterate through each page and apply OCR level 4 to see if it needs OCR. The purpose of this level is so people can develop configurations using the same OCR detection as in portfolios and avoid inconsistent results.

