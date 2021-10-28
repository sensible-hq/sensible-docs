---
title: "Fingerprint"
hidden: true
---
Fingerprints test for matching text in a document to determine whether it's a good fit for a config or not.  There are two types of fingerprints, one for standalone documents, and one for segmenting PDF portfolios into separate documents. If you use a config for both  "portfolio" and "standalone" versions of the same document, Sensible automatically converts between the two and uses the appropriate fingerprint.

| fingerprints for:                                            | notes                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| standalone documents TODO: link fingerprints-for-standalone-documents | Improve performance by testing for matching text in a document before running or skipping a config in a given document type. By skipping configs that fail a fingerprint, you can save processing time. This is relevant if a config contains computationally expensive operations like selective OCR, table recognition, or box recognition methods. |
| portfolio documents TODO: link fingerprints-for-portfolio-documents | Segment PDF portfolios (multiple documents combined into one PDF) into standalone documents by testing for text that characterizes starting, ending, or every page for documents in the portfolio. For more information, see [Document portfolios](doc:portfolio). |



Fingerprints for standalone documents
====

**Parameters**

A fingerprint consists of an array of tests, where each test is a string, a Match object, or array of Match objects. For more information, see [Match object](doc:match).

 Behind the scenes, Sensible automatically expands this syntax to the syntax for portfolio fingerprints syntax using `"page":"any"`. 

**Examples**

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

**Notes**

A fingerprint for standalone documents changes Sensible's default behavior of running *all* the configs in a single document type. For example, if you extract company A and company B quotes, by default Sensible runs both the company A and the company B configs for a given document, then returns the best of the two extractions (the one with the highest percent of non-null values). 

The following table shows how this default behavior changes when you configure the following levels of strictness for a document type's fingerprints. You can configure strictness in the Sensible app in the document type settings:

| Strictness level | Description                                                  | If more than one config's tests pass over 50%                | If no configs' tests passes over 50% or if no configs contain a fingerprint |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| standard         | If any of the configs in the document type contain a fingerprint, then Sensible runs extractions using any configs that pass over 50% of the fingerprint tests. | Sensible chooses the output from the passing config that has the highest percentage of non-null values. | Sensible falls back to the default behavior of running extractions for the document using *all* configurations, and returns the one that has the highest percentage of non-null values. |
| strict           | The doc type must have at least one config containing a fingerprint. | Sensible chooses the output from the passing config that has the highest percentage of non-null values. | Sensible returns a 400 error.                                |




Fingerprints for portfolio documents
====

**Parameters**

A fingerprint consists of an array of tests. The following table shows parameters for each test:

| key                  | value                                                        | description                                                  |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| match (**required**) | a string, a [Match object](doc:match), or array of Match objects. | Specifies the text to match for the test.                    |
| offset               | integer                                                      | Offset in pages from line defined by the Match parameter to a first or last page defined in the Page parameter. |
| page                 | `first`, `last`, `every`, `any`                              | - For PDF portfolios (multiple documents combined into one PDF, such as an invoice, a contract, and a tax form), tests for document starts and ends to segment the portfolio into documents. For more information see [Document portfolios](doc:portfolio). <br/>-  If you reuse the same config between portfolios and standalone documents, then for standalone document extractions, Sensible ignores the configured value of this parameter and treats it as  `"page":"any"`. This way, Sensible avoids strictly matching to extraneous front or back matter (for example, a fax cover page) in single documents. |

**Examples**

For an example of using fingerprints to extract multiple documents combined into one PDF portfolio, see [Document portfolios](doc:portfolio).
