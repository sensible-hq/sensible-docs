---
title: "draft - Extraction engine"
hidden: true
---

**notes ** draft is on hold, based on team meeting onboarding slides from aug 2022 as well as notion docs for onboarding devs. publish if there's an audience need for it (hasn't really come up)





**Note:** If you're familiar with Sensible, this advanced topic is for you. 

This topic gives an overview of the Sensible's extraction engine, including the order of execution for SenseML, for example, preprocessors, fields, computed fields, and sections.

0. Convert DOC and DOCX files to PDF.

1. Read text
---

**NOTE: some of this stuff is in the OCR LEVEL TOPIC:**

Transform the bytes of the document into raw text. Determine whether the document needs OCR:

- If the file is an image file (for example, PNG), run OCR.

- If the file is a PDF, the default `OCR_level` behavior is to run OCR if: 
  - The average number of lines per page is less than 10.
  - The font is corrupted (lots of unprintable characters).
  - The text is extensively garbled. Use regular expressions to test for ungarbled text.

- Otherwise, extract embedded text directly from the PDF.

- Return the direct PDF text if possible, and otherwise the OCR output.

2. Standardize text
----

Take the raw text representation (from OCR or directly from the PDF), clean it, and put it in a standard format for Sensible to use.

- Standardize the text to an array of pages, each containing an array of lines with bounding box data. Also capture transformation metadata (e.g., page rotation).

- Apply non-configurable, global preprocessors (for example, clean up whitespaces, sort lines, merge and deduplicate lines).

  Standardized text output example:

  ```json
  todo add example
  ```

  

3. Filter configurations with fingerprints
----

Reduce the number of configurations that Sensible runs on the document to improve performance. Without fingerprints, Sensible runs every configuration in the document type. With them, Sensible can test if an "ACME_CO_INSURANCE" config should run on an "ACME_quote.pdf" by examining the PDF's standardized text output for key text like "ACME" and "insurance" and filtering out documents that don't contain the key phrases. 

- Score each configuration against its configured fingerprint tests, if present.  
- Return a set of configurations to create extractions for.

For more information, see [Fingerprints](doc:fingerprint).

```json
todo add example fingerprint
```

Note that fingerprints serve a second purpose for determining document page ranges in portfolio extractions (TODO Links).

4. Create extractions
----

Extract candidate output for the document using the SenseML configurations in the document type. For the set of configs determined in the previous step, run the SenseML:

**1. Preprocessors**

Run any preprocessors (e.g., removeHeaders), in the order in which the user specified them in the SenseML array. Sensible then applies a final global preprocessor to remove repeated whitespaces. 

**2. Fields**

Extract fields in the order in which they're written in the SenseML array.  Sensible adds each field to the output array sequentially after extracting it. The default order is:

1. Run fields array.
2. Run computed fields, which transform fields output.
3. Run sections (“documents inside documents”). Cordons off a document range and extracts fields or computed fields from it independently. Suited to complex repeating data.

4. Return all fields, computed fields, and sections

This order is configurable. For more information, see [Field Extraction Order] TODO link.



```json
todo: add a senseML config example
```



Score extractions
---

Determine the best extraction, which is the one Sensible returns data from.

Score each configuration's extraction based on how much data it found, and its [validations](doc:validate-extractions):

- For each field that returns non-null data, +1 point
- For each validation error, -1 point.
- For each validation warning, -0.5 points.

The configuration with the highest score wins
Summarize the scores for the end user.

```json
todo: add json example
```




Return results
----

Return the extraction, and other information, to the user as an API response. 

- Use the winning configuration data from the previous step

- Package it with extraction metadata:
  -  Basic metadata (ID, created date, status, document type, environment)
  - Validation list
  - Error list
  - Validation summary
  - Classification summary
  - File metadata

```json
todo: json example
```

INCOMING LINKS:

- merge lines preprocessor?

- zip sections?

  



