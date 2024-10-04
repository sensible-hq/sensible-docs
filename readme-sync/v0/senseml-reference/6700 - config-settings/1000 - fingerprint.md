---
title: "Fingerprint"
hidden: false

---

Fingerprints test for matching text in a document to determine whether it's a good fit for a config or not.  There are two types of fingerprints:

- one for optimizing extraction performance for standalone documents
- one for segmenting portfolio files into separate documents.

If you use a config for both portfolio and standalone versions of the same document, Sensible automatically converts between the two and uses the appropriate fingerprint.

| fingerprints for:                                            | notes                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [standalone documents ](doc:fingerprint#standalone-documents) | Improve performance by testing for matching text in a document before running or skipping a config in a given document type. By skipping configs that fail a fingerprint, you can save processing time. This is relevant if a config contains computationally expensive operations like LLM-based methods, selective OCR, table recognition, or box recognition methods.<br/>To test for matching text at the field level instead of the document type level, specify field fallbacks. For more information, see [Field query object](doc:field-query-object). |
| [portfolios ](doc:fingerprint#portfolios)                    | A portfolio contains multiple documents combined into one file, such as an invoice, a contract, and a tax form. Sensible uses fingerprints to segment a portfolio into documents. Fingerprints test for matching text that characterizes first, last, or other pages for documents in the portfolio. For more information, see [Multi-document extraction](doc:portfolio). |



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

A fingerprint consists of an array of tests, where each test contains a Page parameter and a Match parameter:

```json
"fingerprint": {
    "tests": [
      {
        "page": "every",
        "match": [
          {
            "text": "this text always shows up on every page of the document",
            "type": "includes"
          }
        ]
      },
      {
        "page": "last",
        "match": [
          {
            "text": "this text always shows up on the last page of the document",
            "type": "startsWith"
          }
        ]
      }
    ]
  }
```

 The following table shows parameters for each test for  portfolio documents:

| key                  | value                                                        | description for portfolios                                   |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| match (**required**) | a string, a [Match object](doc:match), or array of Match objects. | Specifies the text to match for the test.                    |
| offset               | integer                                                      | Specifies where to start or end the document segment, offset in pages relative to the first or last page defined by the Match parameter. For example, if you specify that the page that contains the phrase "A summary of your rights" is the first page of a segment, and Sensible finds a match for the first page on the zero-indexed page 3 of a portfolio:<br/>- specifying `"offset": -1` starts the document segment on page 2 of the portfolio.<br/>- specifying `"offset": 1` starts the document segment on page 4 of the portfolio. |
| page                 | `first`, `last`, `every`, `any`                              | Configure with the following enums:<br/>`first` - The first page of a document segment must meet the match criteria.  <br/>`last` - The last page of a document segment must meet the match criteria. If you specify `last`, you must pair it with a different page type, such as `every`. <br/>`every` - Every page in the document segment must meet the match criteria.  If you define this page type, you must pair it with a different page type, such as `last`. <br/>`any`- Any page in the document segment can meet the criteria. <br/>**Notes:** <br/>- For an example see [Multi-document extraction](doc:portfolio). <br/>- If you reuse the same config between portfolios and standalone documents, then for standalone document extractions, Sensible ignores the configured value of this parameter. |

## Tips

Use the following tips when you define fingerprints for portfolios:

#### test criteria

Portfolio fingerprints differ from single-file document fingerprints in the following behaviors:

- If you specify a Match array in a test, then Sensible must find all the matches in the array on the *same* page in the portfolio for the test to pass and for Sensible to identify a page as "first", "last", or another type. In single-file documents, matches can occur anywhere in a document.
- Sensible must find 100% of all matches in all tests to segment a document in a portfolio. In single-file documents, Sensible must find 50% of all matches anywhere in the document by default to give the document a "passing" score.

####  page types

- Only use  `"page": "first"` and  `"page": "last"` if you're confident that these pages will never be omitted from the document.
- If using `"page": "first"` always pair it with another test type such as `"page": "every"` or `"page": "last"`.
- If the first page doesn't contain unique text and the last page does, Sensible recommends specifying a `last` page test and an `every` page test. 
- Avoid specifying an `any` page test unless other page types fail to segment the document.
- If you want to specify fallback matches for the same page type, specify the matches in separate tests. For example, a form has revisions 1 and 2 that have slightly different wordings on the first page. Specify one test with a `first` page type and wording A, and specify a second test with a `first` page type and wording B.

####  text matches

- Sensible runs `fingerprints` before any `preprocessors`. Because of this, make sure to comment out any `preprocessors` before writing `fingerprints` so that the document in the editor displays the lines of text exactly as they will be recognized when the fingerprints tests are ran.

- Unless the document contains a highly unusual and characteristic `string` or `match` object, always use an array of `match` objects, rather than an array of single-match tests.  In other words, don't write the following:

```json
// AVOID THIS SYNTAX
"fingerprint": {
    "tests": [
      {
        "page": "every"
        "match": [
          {
            "text": "NARS",
            "type": "includes",
            "isCaseSensitive": true
          }
        ]
      },
      {
        "page": "every"
        "match": [
          {
            "text": "Name of Insured",
            "type": "includes",
            "isCaseSensitive": true
          }
        ]
      },
    ]
  }
```

  Instead, write the following:

```json
// PREFER THIS SYNTAX
"fingerprint": {
    "tests": [
      {
        "page": "every"
        "match": [
					[
          {
            "text": "NARS",
            "type": "includes",
            "isCaseSensitive": true
          },
          {
            "text": "Name of Insured",
            "type": "includes",
            "isCaseSensitive": true
          },
		  ]
        ]
      }
    ]
  }
```



Examples
---

For an example of using fingerprints to extract multiple documents from a portfolio file, see [Multi-document extraction](doc:portfolio).

Notes
---

For information about configuring fingerprint strictness for standalone documents, see [Fingerprint mode](doc:fingerprint-mode).
