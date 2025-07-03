---
title: "Query group"
hidden: true

---




Parameters
=====



|      |      |      |
| :--- | :--- | :--- |
|      |      |      |
|      |      |      |

## Query group parameters



| key              | value  | description                                                  | interactions |
| :--------------- | :----- | :----------------------------------------------------------- | ------------ |
|                  |        |                                                              |              |
|                  |        |                                                              |              |
|                  |        |                                                              |              |
|                  |        |                                                              |              |
|                  |        |                                                              |              |
|                  |        |                                                              |              |
|                  |        |                                                              |              |
| multimodalEngine | object | Configure this parameter to:<br/>- Extract data from images embedded in a document, for example, photos, charts, or illustrations.<br/>- Troubleshoot extracting from complex text layouts, such as overlapping lines, lines between lines, and handwriting. For example, use this as an alternative to the [Signature](doc:signature) method, the [Nearest Checkbox](doc:nearest-checkbox) method, the [OCR engine](doc:ocr-engine), and line [preprocessors](doc:preprocessors).<br/><br/>This parameter sends an image of the document region containing the target data to a multimodal LLM (GPT-4o mini), so that you can ask questions about text and non-text images. This bypasses Sensible's [OCR](doc:ocr) and direct-text extraction processes for the region. <br/>This parameter has the following parameters:<br/><br/>- `region`: The document region to send as an image to the multimodal LLM. Configurable with the following options :<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;- To automatically select top-scoring document chunks as the region, specify `"region": "automatic"`. If you configure this option, then help Sensible locate the region by including queries in the group that target text [lines](doc:lines) near the image you want to extract from. <br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;- To manually specify a region, specify an [anchor](doc:anchor) close to the region you want to capture. Specify the region's dimensions in inches relative to the anchor using the [Region](doc:region) method's parameters, for example:<br/>`"region": { `<br/>          `"start": "below",`<br/>          `"width": 8,`<br/>          `"height": 1.2,`<br/>          `"offsetX": -2.5,`<br/>         `"offsetY": -0.25`<br/>          `}`<br/><br/><br/>- `onlyImages`: boolean. default: false. Configure this to troubleshoot image resolution. If set to true, Sensible sends only the images it detects overlapping the region and omits any [lines](doc:lines) overlapping the region. Sends the images at their original resolution. |              |
|                  |        |                                                              |              |
|                  |        |                                                              |              |
|                  |        |                                                              |              |
|                  |        |                                                              |              |
|                  |        |                                                              |              |
|                  |        |                                                              |              |

