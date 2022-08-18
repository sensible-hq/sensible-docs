---
title: "Extraction engine"
hidden: true
---

**Note:** If you're familiar with Sensible, this advanced topic is for you. 

This topic gives an overview of the Sensible's extraction engine, including the order of execution for SenseML, for example, preprocessors, fields, computed fields, and sections.

Read text
---

Transform the bytes of the document into raw text. Determine whether the document needs OCR:

- If the file is an image file (for example, PNG), run OCR.

- If the file is a PDF, the default `OCR_level` behavior is to run OCR if: 
  - The average number of lines per page is less than 10.
  - The font is corrupted (lots of unprintable characters).
  - The text is extensively garbled. Use regular expressions to test for ungarbled text.

- Otherwise, extract embedded text directly from the PDF.

- Return the direct PDF text if possible, and otherwise the OCR output.

Standardize text
----

Take the raw text representation (from OCR or directly from the PDF), clean it, and put it in a standard format for Sensible to use.

- Standardize the text to an array of pages, each containing an array of lines with bounding box data. Also capture transformation metadata (e.g., page rotation).

- Apply non-configurable, global preprocessors (for example, clean up whitespaces, sort lines, merge and deduplicate lines).

  Standardized text output example:

  ```json
  todo add example
  ```

  

Filter configurations with fingerprints
----

Reduce the number of configurations that Sensible runs on the document to improve performance. Without fingerprints, Sensible runs every configuration in the document type. With them, Sensible can test if an "ACME_CO_INSURANCE" config should run on an "ACME_quote.pdf" by examining the PDF's standardized text output for key text like "ACME" and "insurance" and filtering out documents that don't contain the key phrases. 

- Score each configuration against its configured fingerprint tests, if present.  
- Return a set of configurations to create extractions for.

For more information, see [Fingerprints](doc:fingerprint).

```json
todo add example fingerprint
```

Note that fingerprints serve a second purpose for determining document page ranges in portfolio extractions (TODO Links).

Create extractions
----

Extract candidate output for the document using the SenseML configurations in the document type. For the set of configs determined in the previous step, run the config:

**Preprocessors**

- Run any preprocessors (e.g., removeHeaders), in the order in which the user specified them in the SenseML array. Sensible then applies a final global preprocessor to remove repeated whitespaces. 

**Fields**

- Extract fields in the order in which they're written in the SenseML array.  Sensible adds each field to the output array sequentially after extracting it. You can specify fields, computed fields, and sections as sibling arrays, like this:

  ```
  {
   "fields": [],
   "computed_fields": [],
   "sections": []
  }
  ```

  Or you can use the following alternative syntax:

  ```json
  {
      "fields": 
      [
          /* include all fields, computed fields, and sections in one array. Add "type": sections` to sections field IDs,
             otherwise syntax is unchanged. */
      ]
      
  }
  ```

  These syntax alternatives 







- Run computed fields, which transform fields outputt
- Run sections (“documents inside documents”). Cordons off a document range and extract fields or computed fields from it independently. Suited to complex repeating data.

- Return all fields, computed fields, and sections

```json
todo: add a senseML config
```



Score extractions
---




Return results
----





