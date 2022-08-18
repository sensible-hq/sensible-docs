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

Reduce the number of configurations that Sensible runs on the document to improve performance. Without fingerprints, Sensible runs every configuration in the document type. With them, Sensible can test if an “ACME_CO_INSURANCE” config should run on an “ACME_quote.pdf” or not. 

For more information, see [Fingerprints](doc:fingerprint).

```json
todo add example
```



Run SenseML
----

Extract candidate output for the document using the SenseML configurations in the document type.

- Determine whether to run a config (test fingerprints if present)
- Run a config: 
  - Run any preprocessors (e.g., removeHeaders)We then apply a final global preprocessor where we remove repeated whitespace
  - Extract the fields in the fields array
  - Run computed fields, which transform fields outputt
  - Run sections (“documents inside documents”). Cordons off a document range and extract fields or computed fields from it independently. Suited to complex repeating data.
- Return all fields, computed fields, and sections



Score extractions
---


Return results
----





