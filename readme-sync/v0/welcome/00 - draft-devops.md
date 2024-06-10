---
title: "Overview"
hidden: true
---

See the following image steps for a high-level overivew of Sensible's document data extraction workflow:

![image-20240610110005965](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20240610110005965.png)



Let’s look at each step in detail:

1. **Ingest** - In this step, you upload document files to Sensible, and Sensible converts them to a standardized text representation in preparation for extracting structured data. Features include:

   - **file types** supported [file types](doc:file-types) including PDFs, Microsoft Word and Excel, and image types such as JPEG.
   - **file upload methods** - Use our SDK, API, bulk upload UI ("manual upload"), or Zapier. For more information see [Integrate](doc:integrate).
   - **Optimized OCR** - Sensible represents the whole document in a standarized text format. Sensible optimizes performance by choosing between [OCR](doc:ocr) or direct extraction of embedded fonts. 

2. **Classify**- You upload the document to a *processor*, or API endpoint you configure . Each processor extracts data from a general category of similar documents, for example, `/extract/bank_statments` or `extract/tax_documents`.  From there, Sensible automatically classifies the document by  the highest-scoring extraction *template*  in the processor. A template defines how to extract data and populate a target output schema. Features include:

   - **multi-document files** Sensible segments files that combine multiple documents into one PDF [portfolio](doc:portfolio). For example, Sensible splits a mortgage application package into tax forms, bank statements, and application forms. To configure segmentation, you define  "[fingerprints](doc:fingerprint)", or text that characterize first and last pages.
   - **fallback from layout-specific to general  templates** -  
   - **out of the box templates**

3. **Extract** - In this step, Sensible returns the extracted document data. Features include: 

   - **Highly configurable layout- and LLM-based extraction using SenseML** -  heart of Sensible's power. You configure queries that return data. For example:

     ```
     TODO put in a couple simple LLM n layout based fields
     ```

     

   - For more information, see SenseML Reference Introduction and Processors. TODO links.

   - **structured data** Sensible returns data as key-value pairs. For example:

   - ```json
     [
     "customer_name": {
       "type": "string",
       "value": "JOHN SMITH",
       "confidenceSignal": "confident_answer"
     },
       "customer_address": {
       "type": "address",
       "value": "123 Maine Street",
     },
     ]
     ```

     Or it can return more complex data, like tables or sections. TODO links.

     **metadata for tracing source text** (bounding box stuff...todo check if this is true for LLM-based methods and link to location highlighting, maybe link to colors too) doc:validate-extractions and doc:metrics

     **validations** Quality control the data extractions in a document type by writing validations. For example, configure Sensible to throw an error if an extraction zip code is the wrong number of digits.

     **confidence scores**  - For LLM-based extractions, confidence *signals* offer more nuanced troubleshooting than confidence *scores*. They look like error messages like `multiple_possible_answers` and `answer_may_be_incomplete`.

     

4. **Monitor** -  

   1. You can monitor and filter in real-time your extractions at scale using the Sensible app's dashboard. For example, view the number of extractions in recent days or filter by which extractions are returning nulls for target data. TODO links

     ![image-20240607135835819](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20240607135835819.png)

     

5. Human reivew: TODO add bullet point one it's released









