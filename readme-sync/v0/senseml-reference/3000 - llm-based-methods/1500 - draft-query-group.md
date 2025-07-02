---
title: "Query group"
hidden: true

---

## Draft todo:

what does chunk Count mean when OUTLINE set? (same for list)


Parameters
=====



|      |      |      |
| :--- | :--- | :--- |
|      |      |      |
|      |      |      |

## Query group parameters



| key                   | value                                                   | description                                                  | interactions                                                 |
| :-------------------- | :------------------------------------------------------ | :----------------------------------------------------------- | ------------------------------------------------------------ |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |
| multimodalEngine      | object                                                  | Configure this parameter to:<br/>- Extract data from images embedded in a document, for example, photos, charts, or illustrations.<br/>- Troubleshoot extracting from complex text layouts, such as overlapping lines, lines between lines, and handwriting. For example, use this as an alternative to the [Signature](doc:signature) method, the [Nearest Checkbox](doc:nearest-checkbox) method, the [OCR engine](doc:ocr-engine), and line [preprocessors](doc:preprocessors).<br/><br/>This parameter sends an image of the document region containing the target data to a multimodal LLM (GPT-4o mini), so that you can ask questions about text and non-text images. This bypasses Sensible's [OCR](doc:ocr) and direct-text extraction processes for the region. <br/>This parameter has the following parameters:<br/><br/>`region`: The document region to send as an image to the multimodal LLM. Configurable with the following options :<br/><br/>- To automatically select top-scoring document chunks as the region, specify `"region": "automatic"`. If you configure this option, then help Sensible locate the region by including queries in the group that target text near the image you want to extract from. <br/><br/>- To manually specify a region, specify an [anchor](doc:anchor) close to the region you want to capture. Specify the region's dimensions in inches relative to the anchor using the [Region](doc:region) method's parameters, for example:<br/>`"region": { `<br/>          `"start": "below",`<br/>          `"width": 8,`<br/>          `"height": 1.2,`<br/>          `"offsetX": -2.5,`<br/>         `"offsetY": -0.25`<br/>          `}`<br/><br/>`onlyImages`: boolean. default: false. If set to true, Sensible sends only the images it detects in the region and omits any non-image text also in the region. Sends the images in their original resolution rather than the resolution at which Sensible renders the region. |                                                              |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         | ***FIND CONTEXT***                                           |                                                              |
| searchBySummarization | boolean<br/>or<br>`outline`, `page`<br/> default: false | Configure this to troubleshoot situations in which Sensible misidentifies the part of the document that contains the answers to your prompts. <br/>Setting `true` is equivalent to setting `page`.  <br/>This parameter is compatible with documents up to 1,280 pages long.<br/>When you set `page` or `outline`, Sensible uses content [summarization](https://www.sensible.so/blog/embeddings-vs-completions-only-rag) to locate context. Sensible:<br/>1.  prompts an LLM to summarize document content.  If you set `outline`, the LLM generates an outline of the document and summarizes each segment of the outline. If you set `page`, the LLM summarizes each page in the document.<br/>2. prompts a second LLM to return the page indices most relevant to your prompt based on the summaries.<br/>3. extracts the answers to your prompts from those pages' full text.<br/>When you set this to false, Sensible uses the default [approach](doc:prompt) to finding context. | If you set this parameter to a non-false value for a document 5 pages or under in length, Sensible submits the entire document as context, bypassing summarization.<br/> If you set this parameter to a non-false value for a document over 5 pages long, then Sensible sets the Chunk Count parameter to 5 and ignores any configured value.<br/>Note that the LLM Engine parameter doesn't configure the LLMs Sensible uses for locating context. |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |
|                       |                                                         |                                                              |                                                              |

