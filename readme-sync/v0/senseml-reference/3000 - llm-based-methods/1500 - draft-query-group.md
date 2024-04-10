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



| key              | value  | description                                                  |
| :--------------- | :----- | :----------------------------------------------------------- |
|                  |        |                                                              |
|                  |        |                                                              |
| multimodalEngine | object | Configure this parameter to:<br/>- Troubleshoot extracting from complex text layouts, such as overlapping lines and lines between lines. Many such layouts can occur as a consequence of handwritten text. For example, use this as an alternative to the [Signature](doc:signature) method. This parameter can also be an alternative to the [Nearest Checkbox](doc:nearest-checkbox) method, or as an alternative to configuring the [OCR engine](doc:ocr-engine) or line [preprocessors](doc:preprocessors).<br/>- Extract from images embedded in a document.<br/><br/>This parameter sends an image of the document region containing the target data to a multimodal LLM engine for extraction.  This bypasses Sensible's OCR and direct-text extraction processes. Note that this option doesn't support confidence signals.<br/><br/>This parameter has the following parameters:<br/>`region`: The document region to send as an image to the multimodal LLM. Configurable with the following options :<br/>- To automatically select the [context](doc:query-group#notes) as the region, specify `"region": "automatic"`. <br/>- To manually specify a region relative to the field's anchor, specify the region using the [Region](doc:region) method's parameters, for example:<br/>`"region": { `<br/>          `"start": "below",`<br/>          `"width": 8,`<br/>          `"height": 1.2,`<br/>          `"offsetX": -2.5,`<br/>         `"offsetY": -0.25`<br/>          `}` |
|                  |        |                                                              |
|                  |        |                                                              |
|                  |        |                                                              |
|                  |        |                                                              |
|                  |        |                                                              |
|                  |        |                                                              |
|                  |        |                                                              |

## Examples

## Multimodal example

The following example shows using a multimodal LLM to extract from a scanned document containing handwriting. For an alternate approach to extracting from this document, see also the [Sort Lines](doc:method#sort-lines-example) example.

**Config**

```json
{
  "preprocessors": [
    /* Returns confidence signals, or LLM accuracy qualifications,
       for all supported fields. Note that confidence signals aren't supported
       for fields using the Multimodal Engine parameter */
    {
      "type": "nlp",
      "confidenceSignals": true
    }
  ],
  "fields": [
    {
      "method": {
        "id": "queryGroup",
        /* Use a multimodal LLM to troubleshoot
           problems with Sensible's default OCR engine and line merging.
           This 1-step option avoids advanced configuration of the defaults.
             */
        "multimodalEngine": {
          /* Automatically selects the "context", or relevant excerpt,
           from the document to send as an image to the multimodal LLM.
             */
          "region": "automatic"
        },
        "queries": [
          {
            "id": "ownership_type",
            "description": "What is the type of ownership?",
            "type": "string"
          },
          {
            "id": "owner_name",
            "description": "What is the full name of the owner?",
            "type": "string"
          }
        ]
      }
    },
    /* Without the multimodal LLM engine, Sensible's default
       OCR, line sorting, and line merging options result 
      in incorrect answers. */
    {
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            "id": "ownership_type_no_multimodal",
            "description": "What is the type of ownership?",
            "type": "string"
          },
          {
            "id": "owner_name_no_multimodal",
            "description": "What is the full name of the owner?",
            "type": "string"
          }
        ]
      }
    }
  ],
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/multimodal.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/xmajor_sort.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "ownership_type": {
    "value": "Natural Person(s)",
    "type": "string"
  },
  "owner_name": {
    "value": "Kyle Murray",
    "type": "string"
  },
  "ownership_type_no_multimodal": {
    "value": "Natural Person(s) UGMA/UTMACustodian Trust",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "owner_name_no_multimodal": {
    "value": "Mylic Cardinals Dr Glendale A2 85305",
    "type": "string",
    "confidenceSignal": "answer_may_be_incomplete"
  }
}
```
