---
title: "Overview"
hidden: true
---

Welcome! Sensible is a developer-first platform for extracting structured data from documents, for example, business forms in PDF format. Use Sensible to build document-automation features into your vertical SaaS products. 

intro_SDK_2.png

From any document, you can get back key facts as JSON:

![image-20240610103355889](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20240610103355889.png)

```json
{
    "street_address": {
        "value": "1234 ABC COURT",
        "type": "address"
    },
    "included_appliances": [
        {
            "value": "washers",
            "type": "string"
        },
        {
            "value": "dryers",
            "type": "string"
        },
        {
            "value": "refrigerators",
            "type": "string"
        }
    ]
}
```

Sensible is highly configurable: you can get simple data in minutes by leveraging GPT-4 and other large language models (LLMs), or you can tackle complex and idiosyncratic document formatting with Sensible's powerful visual layout-based rules. By combining layout- and LLM-based extraction methods, Sensible supports the entire document landscape, from consistently laid-out, highly structured business forms to free-form, highly variable legal contracts :

![image-20240605094006233](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20240605094006233.png)

## Devops for document data extraction

See the following image steps for a high-level overivew of Sensible's document data extraction workflow:

![image-20240610110005965](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20240610110005965.png)

As the preceding image shows, Sensible's workflow contains the following steps: (TODO: add links to all of these?)

1. **Ingest:** Convert the document (PDF, Microsoft document, or image) to text.

2. **Classify**: Use a user-defined endpoint to classify the document according to the best-fitting user-configured extraction processor.

3. **Extract** The processor returns the extraction using *SenseML*, a highly configurable document-specific query language that uses both LLMs and layout-based extraction rules. Write the queries yourself, or leverage our open-source library. Write rules in generalized templates for free-form documents like contracts, or in layout-specific templates for high-volume, standardized documents like 1044 tax forms. Optionally validate each extraction using user-configured logical rules. 

For more information, see TODO DEVOPS OVERVIEW LINK.

## Document extraction primitives

Combine the latest in LLM parsing techniques with visual layout-based rules to extract primitives like rows, tables, checkboxes, sections, and more as JSON. Write your extraction rules in *SenseML*, Sensible's document-specific query language.

![image-20240610111353983](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20240610111353983.png)

With SenseML, you can:

- Preprocess documents by correcting layout metadata problems, removing unwanted pages, and more, so that Sensible has a clean, standardized text representation of the document from which to extract structured data in a later step.

- Use "methods" in fields to extract document primitives, like rows, columns, tables, boxes, checkbox status, and more. You can also can parse extracted data types like currencies, dates, addresses, or your custom types.

- Post-process extracted document data with logical validations you write like `extracted zip code is 5 digits`, computations like concat/split, and more.

  

A field is the basic SenseML query unit for extracting a piece of document data. The output of a field is a JSON key-value pair that structures the extracted data. SenseML is a key part of the Sensible devops platform.

Here's a example of a field that extracts a table:

senseml_intro_1.png

![image-20240610111849423](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20240610111849423.png)

For more information about SenseML, see TODO link to SenseML Reference intro.

## Learn more



To use the Sensible platform, you'll:

- **Learn** to extract data, or use out-of-the-box supported document types TODO link to the getting started guides and to SenseML reference
- [**Integrate**](doc:integrate) using Sensible's API, SDKs, quick-extract UI, or other tools
- [**Validate**](doc:validate-extractions) extracted data by writing rules for custom errors like `extracted zip code is invalid format` 
- [**Monitor**](doc:metrics) extracted data in production 
- 2do: link to HUMAN REVIEW once it's live











