---
title: "Devops platform"
hidden: true
---

See the following image for a high-level overview of Sensible's document data extraction workflow:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/platform_devops.png)

As the preceding image shows, Sensible's workflow contains the following steps: 

1. **Ingest** - In this step, you upload document files to Sensible, and Sensible converts them to a standardized text representation in preparation for extracting structured data. Features include:
   - **File types** - Supported [file types](doc:file-types) including PDFs, Microsoft Word and Excel, and image types such as JPEG.
   - **File upload methods** - Use our SDK, API, bulk upload UI ("manual upload"), or Zapier. For more information see [Integrate](doc:integrate).
   - **Optimized OCR** - Sensible represents the whole document in a standarized text format. Sensible optimizes performance by choosing between [OCR](doc:ocr), including Amazon, Google, and Microsoft OCR, or direct extraction of embedded fonts. 

2. **Classify** - You upload the document to a _document type_, or API endpoint you configure . Each document type extracts data from a general category of similar documents, for example, `/extract/bank_statments` or `extract/tax_forms`.  From there, Sensible automatically classifies the document by  the highest-scoring extraction *config* in the document type. A config defines how to extract data using queries, and how to populate a target output schema. Features include:

   - **Multi-document files** - Configure Sensible to segment documents bundled into one file (PDF [portfolio](doc:portfolio)). For example, Sensible splits a mortgage application file into tax forms, bank statements, and application forms.
   - **Classification granularity** - By default, Sensible automatically classifies by document subtype during the extraction workflow. Prior to extraction, you can classify a document more broadly into document types using the [classify](doc:classify) endpoints. 
   - **Configurable classification** - Configure Sensible's default classification into document subtypes using _fingerprints_ to improve performance and accuracy. For example, you can leverage [fingerprints](doc:fallbacks#capture-long-tail-documents-with-fallback-configs)  to handle a document type containing both high-volume and long-tail document forms.

3. **Extract** - In this step, Sensible returns the extracted document data. Features include: 

   - **Highly configurable layout- and LLM-based extraction** -  Configure SenseML queries to extract data from your custom documents. For more information, see  [SenseML reference introduction](doc:senseml-reference-introduction).

   - **Out-of-the-box templates** - Sensible provides an open-source [library](doc:library-quickstart) with out-of-the-box support for common business forms, so you can get started extracting from balance sheets, drivers licenses, rent rolls, tax forms, resumes, and more in just minutes.

   - **Structured data** - Sensible returns extracted data as key-value pairs, including complex data like [tables](doc:nlp-table)  or [sections](doc:repeat-layouts). 

   - **Traceability for source text** - Use visual overlays in the Sensible app and metadata in the returned JSON to trace extracted data to its location in the document. For more information, see [Color coding](doc:color) and [Verbosity](doc:verbosity).

   - **Validations** - Quality control the data extractions in a document type by writing validations. For example, configure Sensible to throw an error if an extraction zip code is the wrong number of digits. For more information, see [Validating extractions](doc:validate-extractions).

   - **Confidence scores**  - For LLM-based extractions, confidence _signals_ offer more nuanced troubleshooting than confidence _scores_, with error messages like `multiple_possible_answers` and `answer_may_be_incomplete`. For more information, see [Qualifying LLM accuracy](doc:confidence).

4. **Monitor** -  Monitor and filter in real-time your extraction metrics using the Sensible app's dashboard. For example, view the number of extractions in recent days or filter by which extractions are returning nulls for target data. For more information, see [Monitoring extractions](doc:metrics).

5. **Human review** - If extractions contain errors, for example as the result of hard-to-read handwriting, you can configure rules to flag extractions for manual reviewer. A reviewer can correct and approve flagged extractions in the Sensible app's [Human review](doc:human-review)  tab.
