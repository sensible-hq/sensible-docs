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



| key  | value | description |
| :--- | :---- | :---------- |
|      |       |             |
|      |       |             |
|      |       |             |
|      |       |             |
|      |       |             |
|      |       |             |
|      |       |             |
|      |       |             |
|      |       |             |
|      |       |             |

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
