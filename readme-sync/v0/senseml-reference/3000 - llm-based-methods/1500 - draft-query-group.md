---
title: "Query Group"
hidden: true

---



## 

|      |      |      |
| :--- | :--- | :--- |
|      |      |      |
|      |      |      |

## Query group parameters



| key               | value            | description                                                  |
| :---------------- | :--------------- | :----------------------------------------------------------- |
| id (**required**) | `queryGroup`     |                                                              |
| queries           | array of objects | An array of query objects, where each extracts a single fact and outputs a single field. Each query contains the following parameters:<br/>`id` (**required**) - The ID for the extracted field. <br/>`description`  (**required**) - A free-text question about information in the document. For example, `"what's the policy period?"` or `"what's the client's first and last name?"`. For more information about how to write questions (or "prompts"), see [Query Group](https://docs.sensible.so/docs/query-group-tips) extraction tips. |
| multimodalEngine  | object           | Configure this parameter to troubleshoot extracting from complex text layouts and variable font sizes.  This parameter sends an image of the document region containing the data to extract to a multimodal LLM engine.  This bypasses problems that crop up with OCR or direct text extraction caused by formatting such as font size mismatch and lines in between lines.<br/>This object has the following parameters:<br/>`region`: The document region to send to the multimodal LLM. If you specify `"region": "automatic"`, Sensible automatically selects the [context](doc:query-group#notes) as the region.  To manually specify a region relative to the field's anchor, specify the region using the [Region](doc:region) method's parameters, for example:<br/>`"region": { `<br/>          `"start": "below",`<br/>          `"width": 8,`<br/>          `"height": 1.2,`<br/>          `"offsetX": -2.5,`<br/>         `"offsetY": -0.25`<br/>          `}` |
|                   |                  |                                                              |
|                   |                  |                                                              |
|                   |                  |                                                              |
|                   |                  |                                                              |
|                   |                  |                                                              |
|                   |                  |                                                              |
|                   |                  |                                                              |

## Examples

- 
