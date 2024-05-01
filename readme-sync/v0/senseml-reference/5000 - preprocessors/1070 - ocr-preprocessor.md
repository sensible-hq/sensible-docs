---
title: "OCR preprocessor"
hidden: false
---

When you [extract document data with Sensible](doc:getting-started-ai), Sensible [automatically OCRs](doc:ocr-level) the document for you, except in advanced cases. This topic covers advanced cases.  For information about additional OCR options, see [OCR](doc:ocr)

Use the OCR preprocessor to selectively OCR pages in a document. This preprocessor is useful when a document contains both embedded text and text images. Selectively OCRing the pages containing text images, rather than the entire document, improves extraction performance. Examples of text images include handwriting and scanned text.

If the whole document is a scan or image file, you don't need to configure this preprocessor. In that case, Sensible automatically OCRs the whole document.

Parameters
====

| key                                                          | value              | description                                                  |
| ------------------------------------------------------------ | ------------------ | ------------------------------------------------------------ |
| type (**required**)                                          | `ocr`              |                                                              |
| match (**required** unless you specify Page Lines Limit parameter) | Match object       | The text relative to which you define the page number to OCR. For example, if you know that the page after the heading "Policy Addendums" is always a scanned image, then you specify: <br>      `"type": "ocr"`,<br/>      `"match": "policy addendums",`<br/>      `"pageOffset": 1`<br/>If there are multiple text matches in the document, matches the first. To specify a second or later match, use a [Match array](doc:match-arrays).<br/> To OCR a single page offset from the first page of the document, rather than offset from matched text, specify `"match": { "type": "first" }`.<br/> |
| matchAll                                                     | boolean            | If true, OCRs all pages containing the line specified by the Match parameter. |
| pageLinesLimit                                               | integer            | Performs OCR on all pages containing the specified number of embedded text lines or fewer. Use this parameter to OCR pages for which no reliable text anchors exist. Sensible recommends specifying a small number relative to the typical number of page lines in the document type, since pages with a small number of embedded lines more likely contain text images. Sensible verifies the qualifying pages contain images before perform OCR, to avoid processing blank pages.<br/> If you specify this in combination with a Match parameter, Sensible OCR all pages that meets any of the match criteria or the number of page lines criteria. |
| pageOffset                                                   | number. default: 0 | The zero-indexed number of the page to OCR, counting from the page number of the text matched by the Match parameter. |
| engine                                                       |                    | See [OCR engine](doc:ocr-engine).                            |

Examples
====

The following config specifies to apply OCR processing to specific pages. The config then outputs all lines of the document (`"id": "all_lines_in_doc"`), to double check that OCR extracted the text on those pages. 

```json
{
  "preprocessors": [
    {
      /* OCR first page of document */
      "type": "ocr",
      "match": { "type": "first" },
    },
    {
      /* OCR fourth page of document */
      "type": "ocr",
      "match": { "type": "first" },
      "pageOffset": 3
    },
    {
      /* OCR all pages containing text 'additional riders'  */
      "type": "ocr",
      "match": "additional riders",
      "matchAll": true,
    },  
      
  ],
  "fields": [
     
    {
      /* check OCR output */
      "id": "all_lines_in_doc",
      "method": {
        "id": "documentRange",
        "includeAnchor": true
      },
      "anchor": {
        "match": {
          "type":"first"
        }
      }
    }
  ],
}
```

