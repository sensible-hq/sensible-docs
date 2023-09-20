---
title: "Fingerprint"
hidden: false

---

Fingerprints test for matching text in a document to determine whether it's a good fit for a config or not.  There are two types of fingerprints:

- one for optimizing extraction performance for standalone documents
- one for segmenting PDF portfolios into separate documents.

If you use a config for both  portfolio and standalone versions of the same document, Sensible automatically converts between the two and uses the appropriate fingerprint.

| fingerprints for:                                            | notes                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [standalone documents ](doc:fingerprint#standalone-documents) | Improve performance by testing for matching text in a document before running or skipping a config in a given document type. By skipping configs that fail a fingerprint, you can save processing time. This is relevant if a config contains computationally expensive operations like selective OCR, table recognition, or box recognition methods. |
| [portfolios ](doc:fingerprint#portfolios)                    | Segment PDF portfolios (multiple documents combined into one PDF) into standalone documents by testing for text that characterizes specified pages for documents in the portfolio. For more information, see [Document portfolios](doc:portfolio). |



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

Notes
---

A fingerprint for standalone documents changes Sensible's default behavior of running *all* the configs in a single document type. For example, if you extract company A and company B quotes, by default Sensible runs both the company A and the company B configs for a given document, then returns the extraction with the highest score. 

The following table shows how this default behavior changes when you configure the following levels of strictness for a document type's fingerprints. You can configure strictness in the Sensible app in the document type settings:

| Strictness level | Description                                                  | If more than one config's tests pass over 50%                | If no configs' tests passes over 50% or if no configs contain a fingerprint |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| standard         | If any of the configs in the document type contain a fingerprint, then Sensible runs extractions using any configs that pass over 50% of the fingerprint tests. | Sensible chooses the output from the passing config with the highest score | Sensible falls back to the default behavior of running extractions for the document using *all* configurations, and returns the one that has the highest score. |
| strict           | The doc type must have at least one config containing a fingerprint. | Sensible chooses the output from the passing config that has the highest score. | Sensible returns a 400 error.                                |

In the preceding table, a classification score is calculated as:

`classification score` = `num of non-null fields` - `penalties for validation errors or warnings`, where penalties are as follows:

- `validation error penalty` = 1 * num fields with validation errors
- `validation warning penalty` = 0.5 * num of fields with validation warnings

The classification score is for comparing the quality of extractions within a single document type. To compare scores across document types, see [Accuracy measures](doc:accuracy-measures).


Portfolios
====

Parameters
---

A fingerprint consists of an array of tests. The following table shows parameters for each test:

| key                  | value                                                        | description                                                  |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| match (**required**) | a string, a [Match object](doc:match), or array of Match objects. | Specifies the text to match for the test.                    |
| offset               | integer                                                      | Specifies where to start or end the document segment, offset in pages relative to the first or last page defined by the Match parameter. For example, if you specify that the page that contains the phrase "A summary of your rights" is the first page of a segment, and Sensible finds a match for the first page on the zero-indexed page 3 of a portfolio:<br/>- specifying `"offset": -1` starts the document segment on page 2 of the portfolio.<br/>- specifying `"offset": 1` starts the document segment on page 4 of the portfolio. |
| page                 | `first`, `last`, `every`, `any`                              | For PDF portfolios (multiple documents combined into one PDF, such as an invoice, a contract, and a tax form), tests for document starts and ends to segment the portfolio into documents. <br/>- Sensible discards orphaned `last` matches. In other words, if you specify `last`, then Sensible must find at least one other fingerprint of a different page type preceding the `last` match in order to recognize the document.  For more information see [Document portfolios](doc:portfolio). <br/>-  If you reuse the same config between portfolios and standalone documents, then for standalone document extractions, Sensible ignores the configured value of this parameter and treats it as  `"page" : "any"`. This way, Sensible avoids strictly matching to extraneous front or back matter (for example, a fax cover page) in single documents. |

Examples
---

For an example of using fingerprints to extract multiple documents combined into one PDF portfolio, see [Document portfolios](doc:portfolio).
