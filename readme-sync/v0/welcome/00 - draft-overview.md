---
title: "Overview"
hidden: true
---



Welcome! Sensible is a developer-first platform for extracting structured data from documents, for example, business forms in PDF format. Use Sensible to build document-automation features into your vertical SaaS products. 

With Sensible, you can write extraction queries for any document:

![](https://files.readme.io/799bd47-image.png)

And get back key facts as JSON:



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

Sensible is highly configurable. You can extract data in minutes by leveraging GPT-4 and other large language models (LLMs), or you can get fine-grained control with Sensible's powerful visual layout-based rules. By combining layout- and LLM-based extraction methods, Sensible supports the entire document landscape, from consistently laid-out, highly structured business forms to free-form, highly variable legal contracts :

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/document_landscape.png)

## Configurable data extraction

Configure your extractions using_SenseML_, Sensible's document-specific query language. SenseML combines the latest in LLM techniques with visual layout-based rules to extract document primitives like rows, tables, checkboxes, sections, and more as JSON. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/platform_senseml.png)



With SenseML, you can:

- Preprocess documents by correcting layout metadata problems, removing unwanted pages, and more, so that Sensible has a clean, standardized text representation of the document from which to extract structured data in a later step. For more information, see [Preprocessors](doc:preprocessors). 

- Use "methods" to extract document primitives, like rows, columns, tables, boxes, checkbox status, and more. You can also can parse extracted data types like currencies, dates, addresses, or your custom types. For more information, see [Methods](doc:methods). 

- Post-process extracted document data. For example:
  - Write logical [validations](doc:validate-extractions)  like `extracted zip code is 5 digits` in order to throw custom errors and warnings about your extracted data. 
  - Manipulate the extracted data schema with [computed methods](doc:computed-field-methods)  like concat, split, and [custom logic](doc:custom-computation) .
  - Get measures of accuracy for LLMs with [confidence scores](doc:confidence), and get overall measures of extraction completeness with [extraction coverage scores](doc:metrics#extraction-coverage)  . 

A field is the basic SenseML query unit for extracting a piece of document data. The output of a field is a JSON key-value pair that structures the extracted data. SenseML is the basis for Sensible's extraction process.

Here's a example of a field that extracts a table:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/senseml_intro_1.png)

For more information about SenseML, see [SenseML reference introduction](doc:senseml-reference-introduction).

## Devops platform for document data extraction

See the following image for a high-level overview of Sensible's document data extraction workflow:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/platform_devops.png)

As the preceding image shows, Sensible's workflow contains the following steps: 

1. **Ingest** - In this step, you upload document files to Sensible, and Sensible converts them to a standardized text representation in preparation for extracting structured data. Features include:
   - **file types** supported [file types](doc:file-types) including PDFs, Microsoft Word and Excel, and image types such as JPEG.
   - **file upload methods** - Use our SDK, API, bulk upload UI ("manual upload"), or Zapier. For more information see [Integrate](doc:integrate).
   - **Optimized OCR** - Sensible represents the whole document in a standarized text format. Sensible optimizes performance by choosing between [OCR](doc:ocr) or direct extraction of embedded fonts. 

2. **Classify**- You upload the document to a _processor_, or API endpoint you configure . Each processor extracts data from a general category of similar documents, for example, `/extract/bank_statments` or `extract/tax_documents`.  From there, Sensible automatically classifies the document by  the highest-scoring extraction *config* in the processor. A config defines how to extract data  using queries, and how to populate a target output schema. Features include:
   - **multi-document files** Sensible segments files that combine multiple documents into one PDF [portfolio](doc:portfolio). For example, Sensible splits a mortgage application package into tax forms, bank statements, and application forms. To configure segmentation, you define  [fingerprints](doc:fingerprint), or text that characterize first and last pages.
   - **out-of-the-box templates** - Sensible provides an open-source [library](doc:library-quickstart)  of extraction templates with out-of-the-box support for common business forms, so you can get started extracting from balance sheets, drivers licenses, rent rolls, tax forms, resumes, and more in just minutes.
   - **Configurable classification** - You can let Sensible handle classification, or you can use _fingerprints_ to improve performance and accuracy. For example, you can leverage [fingerprints](doc:fallbacks#capture-long-tail-documents-with-fallback-configs)  to handle high-volume forms, and default to auto-scoring to handle a long-tail of more variable documents.
   - **Classification granularity** By default, Sensible automatically classifies by document subtype in the processor during the extraction workflow. Prior to extraction , you can classify a document more broadly into processors using the [classify](doc:classify) endpoints. 

3. **Extract** - In this step, Sensible returns the extracted document data. Features include: 

   - **Highly configurable layout- and LLM-based extraction using SenseML** -  SenseML provides power and flexibility for your custom extraction needs.  You configure queries that return data. For more information, see  [SenseML reference introduction](doc:senseml-reference-introduction).

   - **structured data** Sensible returns extracted data as key-value pairs, including complex data like [tables](doc:nlp-table)  or [sections](doc:repeat-layouts). 

   **metadata for tracing source text** Sensible offers traceability from the extracted text to the source text in the document through visual overlays in the Sensible app and metadata in the returned JSON. For more information, see [Color coding](doc:color) and [Verbosity](doc:verbosity).

   - **validations** Quality control the data extractions in a document type by writing validations. For example, configure Sensible to throw an error if an extraction zip code is the wrong number of digits. For more information, see [Validating extractions](doc:validate-extractions).

   - **confidence scores**  - For LLM-based extractions, confidence _signals_ offer more nuanced troubleshooting than confidence _scores_. They look like error messages like `multiple_possible_answers` and `answer_may_be_incomplete`. For more information, see [Qualifying LLM accuracy](doc:confidence).

4. **Monitor** -  

   - You can monitor and filter in real-time your extractions at scale using the Sensible app's dashboard. For example, view the number of extractions in recent days or filter by which extractions are returning nulls for target data. For more information, see [Monitoring extractions](doc:metrics).

5. **Human review** - 

## Learn more

To use the Sensible platform, you'll:

- Learn  to extract data, or use out-of-the-box supported document types. See [Getting started](doc:draft-getting-started-ai) and [Getting started with layout-based extractions](doc:getting-started).
- [**Integrate**](doc:integrate) using Sensible's API, SDKs, quick-extract UI, or other tools
- [**Validate**](doc:validate-extractions) extracted data by writing rules for custom errors like `extracted zip code is invalid format` 
- [**Monitor**](doc:metrics) extracted data in production 
- [**Review**](doc:human-review) and correct extracted data at the field level using the review UI











