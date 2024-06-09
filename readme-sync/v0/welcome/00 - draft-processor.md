---
title: "Processors"
hidden: true
---

A *processor* is an API endpoint that you configure for extracting data from a general category of similar documents, for example, `bank_statments` or `tax_documents`.  You configure extraction templates or leverage our out-of-the-box [library](doc:library-quickstart). 

 In the endpoint, you configure *templates* that define how to extract data from subcategories of documents in the general processor category. The templates contain queries you write in our document-domain specific query language, [SenseML](doc:senseml-reference-introduction).



2do: this image should have /bank_statements endpoint covering both classify and extract 

![image-20240607135147766](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20240607135147766.png)



 For example, a `bank_statements` processor might have a template for bank of america statements, a template for wells fargo templates, and template for chase statements. Leverage our layout-based extraction SenseML methods (2do link) for fast and determinstic extractions for highly structured documents in the processor, and include an LLM-based, generalized template you can [fall back](doc:fallbacks#capture-long-tail-documents-with-fallback-configs) to if you have a long-tail of variable documents that you want to include in the processor. Here's an example of 2 different templates:

- **layout-based template**

- ````json
  {
    "fingerprint": {
      "tests": [
        {
          "text": "bankofamerica",
          "type": "endsWith",
        }
      ]
    },
      {
    "fields": [
      /* LLM-based field */
      {
        "method": {
          "id": "queryGroup",
          "queries": [
            {
              "id": "customer_name",
              "description": "what is the customer name",
              "type": "string"
            }
          ]
        }
      },
      /* layout-based field */
          {
        "id": "customer_address",
        "type": "address",
        "method": {
          "id": "region",
          "start": "left",
          "offsetX": -5.5,
          "offsetY": 0.3,
          "width": 3.2,
          "height": 1.8
        },
        "anchor": {
          "match": {
            "type": "startsWith",
            "text": "customer service information"
          }
        }
      },
    ]
  }
      
  ````

  