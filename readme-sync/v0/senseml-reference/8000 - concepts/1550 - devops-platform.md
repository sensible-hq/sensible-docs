---
title: "Devops platform"
hidden: false
---

See the following image for a high-level overview of Sensible's document data extraction workflow:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/platform_devops.png)

As the preceding image shows, Sensible's workflow contains the following steps: 

1. **Ingest** - In this step, you upload document files to Sensible, and Sensible converts them to a standardized text representation in preparation for extracting structured data. Features include:
   - **File types** - Sensible supports PDFs, Microsoft Word and Excel, and image types such as JPEG. For more information, see [Supported file types](doc:file-types).
   - **File upload methods** - Use Sensible's SDK, API, bulk upload UI ("manual upload"), or Zapier. For more information see [Integrate](doc:integrate).
   - **Optimized OCR** - Sensible represents the whole document in a standardized text format. Sensible optimizes performance by choosing between OCR, including Amazon, Google, and Microsoft OCR, or direct extraction of embedded fonts.  For more information, see [OCR](doc:ocr).
2. **Classify** - Upload the document to a _document type_, or API endpoint you configure. Each document type extracts data from a general category of similar documents, for example, `/extract/bank_statments` or `extract/tax_forms`.  When you upload a document to a document type, Sensible automatically classifies the document into subtypes, for example, `chase_statements` and `wells_fargo` statements for the `bank_statements` document type. You define each subtype using a *config*. A config specifies how to extract data using queries, and how to populate a target output schema. Features include:
   - **Multi-document files** - Sensible splits documents out of a multi-document file (a "PDF portfolio"). For example, Sensible splits a mortgage-application PDF file into tax forms, bank statements, and application forms. For more information, see [Multi-document extractions](doc:portfolio).
   - **Classification granularity** - By default, Sensible automatically classifies by document subtype during the extraction workflow. Prior to extraction, you can classify a document at the document type level using the [classify](doc:classify) endpoints. 
   - **Configurable classification** - Configure Sensible's default subtype classification using _fingerprints_ to improve performance and accuracy. For example, you can use fingerprints to fall back between generalized configs for high-volume documents and layout-specific configs for long-tail documents in a document type. For more information, see [Fingerprints](doc:fingerprint) and [Using fallbacks](doc:fallbacks#capture-long-tail-documents-with-fallback-configs).
3. **Extract** - In this step, Sensible returns the extracted document data. Features include: 
   - **Highly configurable layout- and LLM-based extraction** -  Write SenseML queries to extract data from your custom documents. For more information, see [SenseML reference introduction](doc:senseml-reference-introduction).
   
   - **Out-of-the-box templates** - Sensible provides an open-source library with out-of-the-box support for common business forms, so you can get started extracting from balance sheets, drivers licenses, rent rolls, tax forms, resumes, and more in just minutes. For more information, see [Out-of-the-box extractions](doc:library-quickstart).
   
   - **Structured data** - Sensible returns extracted data as key-value pairs, including complex data like [tables](doc:nlp-table)  or [sections](doc:repeat-layouts). 
   
   - **Traceability for source text** - Use visual overlays in the Sensible app and metadata in the returned JSON to trace extracted data to its source location (or "bounding box coordinates") in the document. For more information, see [Color coding](doc:color) and [Verbosity](doc:verbosity).
   
   - **Validations** - Quality control the data extractions in a document type by writing validations. For example, configure Sensible to throw an error if an extracted zip code is the wrong number of digits. For more information, see [Validating extractions](doc:validate-extractions).
   
   - **Confidence scores**  - For LLM-based extractions, confidence _signals_ offer more nuanced troubleshooting than numerical confidence _scores_, with error messages like `multiple_possible_answers` and `answer_may_be_incomplete`. For more information, see [Qualifying LLM accuracy](doc:confidence).
4. **Monitor** -  Quality control your extractions in production. Features include:
   - **Human review UI** - If extractions contain errors, for example as the result of hard-to-read handwriting, you can configure rules to flag extractions for manual review. A reviewer can correct and approve flagged extractions in the Sensible app's tab. For more information, see [Human review](doc:human-review).  
   - **Metrics dashboard**: View and filter your real-time extraction metrics using the Sensible app's dashboard. For example, view the number of extractions in recent days or filter by which extractions are returning nulls for target data. For more information, see [Monitoring extraction metrics](doc:metrics).
