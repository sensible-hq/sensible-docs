---
title: "Fingerprint"
hidden: false

---

Fingerprints test for matching text in a document to determine whether it's a good fit for a config or not.  There are two types of fingerprints:

- one for optimizing extraction performance for standalone documents
- one for segmenting portfolio files into separate documents.

If you use a config for both  portfolio and standalone versions of the same document, Sensible automatically converts between the two and uses the appropriate fingerprint.

| fingerprints for:                                            | notes                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [standalone documents ](doc:fingerprint#standalone-documents) | Improve performance by testing for matching text in a document before running or skipping a config in a given document type. By skipping configs that fail a fingerprint, you can save processing time. This is relevant if a config contains computationally expensive operations like selective OCR, table recognition, or box recognition methods. |
| [portfolios ](doc:fingerprint#portfolios)                    | Segment portfolios (multiple documents combined into one file) into standalone documents by testing for text that characterizes specified pages for documents in the portfolio. For more information, see [Multi-document extraction](doc:portfolio). |



Standalone documents
====

Parameters
---

A fingerprint consists of an array of tests, where each test is a string, a Match object, or array of Match objects. For more information, see [Match object](doc:match).

 Behind the scenes, Sensible automatically expands this simple syntax to syntax for portfolio fingerprints using `"page" : "any"`. 

Examples
---

The following fingerprint tests a vendor-specific config "anyco_life_insurance_quote" in a document type "life insurance quotes". This fingerprint tests that a document is a life insurance quote from Anyco by looking for three known key phrases. 

```
{
  "fingerprint": {
    "tests": [
      {
        "type": "startsWith",
        "text": "anyco"
      },
      "info@anyco.com",
      "life insurance quote"
    ]
  },
  "fields": []
}
```

The config preferentially runs if the fingerprint finds the phrases.  


Portfolios
====

Parameters
---

A fingerprint consists of an array of tests. The following table shows parameters for each test:

| key                  | value                                                        | description                                                  |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| match (**required**) | a string, a [Match object](doc:match), or array of Match objects. | Specifies the text to match for the test.                    |
| offset               | integer                                                      | Specifies where to start or end the document segment, offset in pages relative to the first or last page defined by the Match parameter. For example, if you specify that the page that contains the phrase "A summary of your rights" is the first page of a segment, and Sensible finds a match for the first page on the zero-indexed page 3 of a portfolio:<br/>- specifying `"offset": -1` starts the document segment on page 2 of the portfolio.<br/>- specifying `"offset": 1` starts the document segment on page 4 of the portfolio. |
| page                 | `first`, `last`, `every`, `any`                              | For portfolios (multiple documents combined into one file, such as an invoice, a contract, and a tax form), tests for document starts and ends to segment the portfolio into documents. <br/>- Sensible discards orphaned `last` matches. In other words, if you specify `last`, then Sensible must find at least one other fingerprint of a different page type preceding the `last` match in order to recognize the document.  For more information see [Multi-document extraction](doc:portfolio). <br/>-  If you reuse the same config between portfolios and standalone documents, then for standalone document extractions, Sensible ignores the configured value of this parameter and treats it as  `"page" : "any"`. This way, Sensible avoids strictly matching to extraneous front or back matter (for example, a fax cover page) in single documents. |

Examples
---

For an example of using fingerprints to extract multiple documents combined into one portfolio file, see [Multi-document extraction](doc:portfolio).

Notes
---

For information about configuring fingerprint strictness for a document type, see [Fingerprint mode](doc:fingerprint-mode).
