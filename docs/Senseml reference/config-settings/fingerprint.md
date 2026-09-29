---
title: Fingerprint
excerpt: Learn how Sensible tests documents for matching text patterns ("fingerprints"). Two distinct use cases: 1. identify document subtypes (e.g. identify wells_fargo in bank_statements doc type) 2. segment multi-document
 portfolios (e.g. find wells_fago bank statement page range in a hundred-page mortgage application PDF that contains other document types) 
deprecated: false
hidden: false
metadata:
  title: ''
  description: Learn how Sensible tests documents for matching text patterns ("fingerprints"). Two distinct use cases: 1. identify document subtypes (e.g. identify wells_fargo in bank_statements doc type) 2. segment multi-document
 portfolios (e.g. find wells_fago bank statement page range in a hundred-page mortgage application PDF that contains other document types) 
  robots: index
next:
  description: ''
---
Fingerprints test for matching text in a document to determine:

1. the document's subtype, or "config", for standalone files
2. the document's page range in multi-document, or "portfolio", files.

See the following table for more information:

| use case                                                     | description                                                  | related concepts                                             | Syntax                                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [standalone documents](doc:fingerprint#standalone-documents) | Improve performance by testing for matching text in a document before running or skipping a "config," or subtype, in a specified document type. By skipping configs that fail a fingerprint, you can save processing time. This is relevant if a config contains computationally expensive operations like LLM-based methods, selective OCR, table recognition, or box recognition methods. | **Fallbacks:** <br/>Fingerprints let you fall back between configs. To fall back between fields *inside* a config, see [Fallback fields](doc:fallbacks). <br/><br/> **Classification**:<br/>Fingerprints let you determine the *subtype* of a standalone document. To determine the type of a standalone document, see [Classifying documents by type](doc:classify). | `fingerprint:`<br/>`tests: [array of strings, Match objects]`</br> TODO: make this look better, write in JSON syntax, |
| [portfolios](doc:fingerprint#portfolios)                     | A portfolio contains multiple documents combined into one file, such as an invoice, a contract, and a tax form. Sensible uses fingerprints to segment a portfolio into documents. Fingerprints test for matching text that characterizes first, last, or other pages for documents in the portfolio. For more information, see [Multi-document extraction](doc:portfolio). | Use LLMs as an alternative to fingerprints to segment [portfolios](doc:portfolio). | TODO fill in abbreviated syntax example                      |


You use different syntaxes to define fingerprints depending on your use case. If you expect that you'll use a config in both standalone and portfolio extraction requests (generally a rare circumstance), Sensible recommends you use the stricter syntax (portfolio syntax) rather than relying on Sensible's automatic conversions between the two syntaxes.  Sensible automatically converts between the two as follows:

-  To convert to portfolio, Sensible automatically expands standalone document syntax for portfolio fingerprints using `"page" : "any"`.  
-  To convert to standalone, Sensible discards all portfolio-specific parameters in each test and only retains the value of the `match` parameter.



# Standalone documents

## Parameters

| key     | value                                                        | description for standalone documents                         |
| ------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `tests` | array or nested array,<br/> where each item is a string, a  [Match](doc:match) object, or array of Match objects. | Choosing an array or nested array affects how Sensible scores an array of Match objects. LEFT OFF: Portfolio fingerprints differ from single-file document fingerprints in the following behaviors:<br/><br/>* If you specify a Match array in a test, then Sensible must find all the matches in the array on the *same* page in the portfolio for the test to pass and for Sensible to identify a page as "first", "last", or another type. In single-file documents, matches can occur anywhere in a document.<br/>* 100% of tests must pass for Sensible to segment a document in a portfolio. In single-file documents, 50% of tests must pass for Sensible to give the document a "passing" score. |

## Examples

The following fingerprint tests a vendor-specific config, `wells_fargo_checking` in a document type, `bank statements`. This fingerprint tests that a document is a Wells Fargo checking account statement by using three tests: an array of Match objects, a Match object, and a string.

```json
/* Sensible uses JSON5 to support in-line comments*/
{
  "fingerprint": {
    /* optional. Sensible skips this config if these tests fail, improving performance when you have multiple configs */
    "tests": [
      /* array of tests; for standalone documents, the config passes if 50% or more of the tests pass */
      /* test 1 passes if Sensible finds all the matches in the array in succeeding lines (can be across multiple pages);
         if array elements are out of order or not all elements are present, it fails */
      [
        {
          "type": "includes",
          "text": "wells fargo"
        },
        {
          "type": "endsWith",
          "text": "page 2"
        },
        {
          "type": "endsWith",
          "text": "page 3"
        }
      ],
      /* test 2 passes if Sensible finds a line that starts with "account" anywhere in the document */
      {
        "type": "startsWith",
        "text": "account"
      },
      /* test 3 passes if Sensible finds a line that includes "checking" anywhere in the document.
         Sensible expands string tests to case-insensitive includes matches */
      "checking"
    ]
  },
  "fields": []
}
```

The config preferentially runs if the fingerprint tests pass.


# Portfolios

## Parameters

A fingerprint contains a `tests` parameter, that takes an array or nested array. For more information, see the preceding standalone parameters.

The following table shows parameters for each item in the `tests` array for  portfolio documents:

| key                  | value                                                        | description for portfolios                                   |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| match (**required**) | a string, a [Match object](doc:match), or array of Match objects. | Specifies the text to match for the test.  If you specify a Match array, all the items in the array must appear on a single page. |
| offset               | integer                                                      | Specifies where to start or end the document segment, offset in pages relative to the first or last page defined by the Match parameter. For example, if you specify that the page that contains the phrase "A summary of your rights" is the first page of a segment, and Sensible finds a match for the first page on the zero-indexed page 3 of a portfolio:<br/>- specifying `"offset": -1` starts the document segment on page 2 of the portfolio.<br/>- specifying `"offset": 1` starts the document segment on page 4 of the portfolio. |
| page                 | `first`, `last`, `every`, `any`                              | Configure with the following enums:<br/>`first` - The first page of a document segment must meet the match criteria. Use `first` to detect consecutive document segments of the same document type in a portfolio. If you specify `first` you must pair it with another test type such as `"page": "every"` or `"page": "last"`. <br/>`last` - The last page of a document segment must meet the match criteria. If you specify `last`, you must pair it with a different page type, such as `every`. <br/>`every` - Every page in the document segment must meet the match criteria.  If you define this page type, you must pair it with a different page type, such as `last`. <br/>`any`- Any page in the document segment can meet the criteria. Avoid specifying an `any` page test unless other page types fail to segment the portfolio.<br/>**Notes:** <br/>- For an example see [Multi-document extraction](doc:portfolio). <br/>- If you reuse the same config between portfolios and standalone documents, then for standalone document extractions, Sensible ignores the configured value of this parameter. |

## Examples

## Syntax example

```json
"fingerprint": {
    "tests": [
      {
        "page": "every",
        "match": [
          {
            "text": "you expect this text always shows up on every page of the document",
            "type": "includes"
          }
        ]
      },
      {
        "page": "last",
        "match": [
          {
            "text": "you expect this text always shows up on the last page of the document",
            "type": "startsWith"
          }
        ]
      }
    ]
  }
```

 ## Example 1

For an example of using fingerprints to extract multiple documents from a portfolio file, see [Multi-document extraction](doc:portfolio).





## Notes

For information about configuring fingerprint strictness for standalone documents, see [Fingerprint mode](doc:fingerprint-mode).



### Tips for authoring fingerprints

Use the following tips when you define fingerprints for portfolios:

#### fallbacks

* If you want to specify alternate, or fallback, matches for the same page type, specify the matches in separate tests. For example, a form has revisions 1 and 2 that have slightly different wordings on the last page.  Specify one test with a `last` page type and wording A, and specify a second test with a `last` page type and wording B.

TODO: verify if this can actually be done?

#### Turn off preprocessors

* Sensible runs `fingerprints` before any `preprocessors`. Because of this behavior, make sure to comment out any `preprocessors` before writing `fingerprints` so that the document in the editor displays the lines of text exactly as Sensible recognizes them when Sensible runs the fingerprint tests.

#### Standalone-specific tips

The following tips apply to fingerprints for  standalone documents.

**test and verify fingerprints**

In the Sensible app, you can verify and test fingerprints for stand-alone documents. If your write the fingerprints with portfolio syntax, Sensible automatically converts them TODO link

#### Portfolio-specific tips

The following tips apply to fingerprints for  portfolio documents.

** Prefer nested match arrays for portfolios**

* Unless the document contains a highly unusual and characteristic `string` or `match` object, always use an array of `match` objects, rather than an array of single-match tests.  In other words, don't write the following:

```json
/* AVOID THIS SYNTAX */
"fingerprint": {
  "tests": [
    /* Each test contains a single match, so Sensible scores each
       phrase independently instead of requiring the phrases together */
    {
      "page": "every",
      "match": [
        {
          "text": "NARS", /* distinctive phrase */
          "type": "includes",
          "isCaseSensitive": true
        }
      ]
    },
    {
      "page": "every",
      "match": [
        {
          "text": "Name of Insured", /* generic phrase. On its own, it can match pages in unrelated documents */
          "type": "includes",
          "isCaseSensitive": true
        }
      ]
    }
  ]
}
```

also avoid:

```json
/* AVOID THIS SYNTAX */
"fingerprint": {
  "tests": [
    {
      "page": "every",
      "match": [
        /* flat array: TODO LEFT OFF */
          {
            "text": "NARS",
            "type": "includes",
            "isCaseSensitive": true
          },
          {
    
            "text": "Name of Insured",
            "type": "includes",
            "isCaseSensitive": true
          }
        ]   
    }
  ]
}
```





  Instead, write the following:

```json
/* PREFER THIS SYNTAX */
"fingerprint": {
  "tests": [
    /* one test that contains a match array, so the test passes only if the lines occur in the document in the order specified by the array */
    {
      "page": "every",
      "match": [[
        /* nested array: enforces stricter criteria: that each element matches a separate line, and Sensible
             must find all the lines in the document in the same order as in the array.
           If you don't use a nested array, Sensible scores "NARS" and
           "Name of Insured", each individually as separate matches appearing in separate lines, in any order in the document. */
        
          /* further nested array behavior LEFT OFF: 
             In a portfolio, Sensible must also find all the lines in the array on a single page.
             In a standalone document, Sensible searches for the lines across multiple pages */
          {
            "text": "NARS",
            "type": "includes",
            "isCaseSensitive": true
          },
          {
    
            "text": "Name of Insured",
            "type": "includes",
            "isCaseSensitive": true
          }
        ]]   
    }
  ]
}
```

TODO add a screenshot
