---
title: Fingerprint
excerpt: >-
  Learn how Sensible tests documents for matching text patterns ("fingerprints"). Two distinct use cases: 1. identify document subtypes (for example, identify wells_fargo in bank_statements doc type) 2. segment multi-document portfolios (for example, find wells_fargo bank statement page range in a hundred-page mortgage application PDF that contains other document types)
deprecated: false
hidden: false
metadata:
  title: ''
  description: >-
    Learn how Sensible tests documents for matching text patterns ("fingerprints"). Two distinct use cases: 1. identify document subtypes (for example, identify wells_fargo in bank_statements doc type) 2. segment multi-document portfolios (for example, find wells_fargo bank statement page range in a hundred-page mortgage application PDF that contains other document types)
  robots: index
next:
  description: ''
---
Fingerprints test for matching text in a document to determine:

1. the document's subtype, or "config", for standalone files
2. the document's page range in multi-document files, or "portfolios."

See the following table for more information:

| use case                                                     | description                                                  | related concepts                                             |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [standalone documents](doc:fingerprint#standalone-documents) | Improve performance by testing for matching text in a document before running or skipping a "config," or subtype, in a specified document type. By skipping configs that fail a fingerprint, you can save processing time. This is relevant if a config contains computationally expensive operations like LLM-based methods, selective OCR, table recognition, or box recognition methods. | **Fallbacks:** <br/>Fingerprints let you fall back between configs. To fall back between fields *inside* a config, see [Fallback fields](doc:fallbacks). <br/><br/> **Classification**:<br/>Fingerprints let you determine the *subtype* of a standalone document. To determine the type of a standalone document, see [Classifying documents by type](doc:classify). |
| [portfolios](doc:fingerprint#portfolios)                     | A portfolio contains multiple documents combined into one file, such as an invoice, a contract, and a tax form. Sensible uses fingerprints to segment a portfolio into documents. Fingerprints test for matching text that characterizes first, last, or other pages for documents in the portfolio. For more information, see [Multi-document extraction](doc:portfolio). | Use LLMs as an alternative to fingerprints to segment [portfolios](doc:portfolio). |

You use different fingerprint syntaxes for the two use cases. For more information, see the following sections.

# Standalone documents

## Parameters

The following table shows fingerprint syntax for standalone documents:

| key     | value                                                        | description                                                  |
| ------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `tests` | array, where each element is a string, a [Match](doc:match) object, or a [chained match](doc:fingerprint#chained-matches) | Sensible uses matching text to preferentially run configs in a document type. |

## Examples

The following example is for standalone documents. The fingerprint tests a vendor-specific config, `wells_fargo_checking` in a document type, `bank statements`. This fingerprint tests that a document is a Wells Fargo checking account statement.

```json
/* Sensible uses JSON5 to support in-line comments*/
{
  /* comment out preprocessors until you're done authoring fingerprints, then turn them back on in production
    preprocessors: []
  */ 
  "fingerprint": {
    /* optional. Sensible skips this config if the fingerprint fails, improving performance when you have multiple configs */
    "tests": [
      /* array of tests.
         The fingerprint passes if Sensible finds 50% or more of the elements ('matches') in the tests array. In this example, there are 3 elements in the tests array, so if 2 out of 3 passes, the config passes. The 3 elements are: a chained match, a Match object, and a string. */
      /* The first element is a chained match ([]), so Sensible scores it as one match. The chained match succeeds only if Sensible finds
         all its Match objects in order, on separate lines. The lines can be on different pages.
         If a Match object is missing or out of order, the chained match fails */
      [ 
        {
          "type": "includes",
          "text": "wells fargo"
        },
        {
          "type": "startsWith",
          "text": "statement period"
        },
        {
          "type": "startsWith",
          "text": "transaction history"
        }
      ],
      /* element 2 succeeds if Sensible finds a line that starts with "account" anywhere in the document */
      {
        "type": "startsWith",
        "text": "account"
      },
      /* element 3 succeeds if Sensible finds a line that includes "checking" anywhere in the document.
         Sensible expands a string to a case-insensitive includes match */
      "checking"
    ]
  },
  "fields": []
}
```

The config preferentially runs if the fingerprint passes.


# Portfolios

## Parameters

 A fingerprint for portfolios contains a `tests` parameter that takes an array of test objects. The following table shows the parameters for each test object:

| key                  | value                                                        | description for portfolios                                   |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| match (**required**) | a string, a [Match object](doc:match), an array of unordered Match objects, or a [chained match](doc:fingerprint#chained-matches) | Specifies the text to match. Sensible uses matches to segment a document's page range in portfolio files. |
| offset               | integer                                                      | Specifies where to start or end the document segment, offset in pages relative to the first or last page defined by the Match parameter. For example, if you specify that the page that contains the phrase "A summary of your rights" is the first page of a segment, and Sensible finds that match on the zero-indexed page 5 of a portfolio:<br/>- specifying `"offset": -1` starts the document segment on page 4 of the portfolio.<br/>- specifying `"offset": 2` starts the document segment on page 7 of the portfolio. |
| page                 | `first`, `last`, `every`, `any`                              | Configure with the following enums:<br/>`first` - The first page of a document segment must meet the match criteria. Use `first` to detect consecutive document segments of the same document type in a portfolio. If you specify `first` you must pair it with another test type such as `"page": "every"` or `"page": "last"`. <br/>`last` - The last page of a document segment must meet the match criteria. If you specify `last`, you must pair it with a different page type, such as `every`. <br/>`every` - Every page in the document segment must meet the match criteria. If you define this page type, you must pair it with a different page type, such as `last`. <br/>`any`- Any page in the document segment can meet the criteria. Avoid specifying an `any` page test unless other page types fail to segment the portfolio. |

## Portfolio examples

For an example of using fingerprints to extract multiple documents from a portfolio file, see [Multi-document extraction](doc:portfolio#fingerprint-example). 

# Concepts

## Fingerprint syntax conversion

If you expect that you'll use a config in both standalone and portfolio extraction requests (generally a rare circumstance), Sensible recommends you use the stricter portfolio syntax. Sensible automatically converts between the two syntaxes as follows:

-  To convert to portfolio, Sensible automatically expands standalone document syntax for portfolio fingerprints using `"page" : "any"`.  
-  To convert to standalone, Sensible discards all portfolio-specific parameters in each test and only retains the value of the Match parameter. In detail, it ignores the Page and Offset parameters if specified.

## Fingerprint strictness in standalone documents

For information about configuring fingerprint strictness for standalone documents, see [Fingerprint mode](doc:fingerprint-mode).

## Fingerprint scoring

Sensible scores fingerprints differently for standalone documents and for portfolios.

**Standalone documents using standalone syntax**

50% or more of the elements ("matches") in the `tests` array must succeed for the config to "pass."

Sensible searches the whole document for each element in the fingerprint. If more than one config passes, Sensible runs all the configs that pass and returns the extraction with the highest score. For more information, see [Fingerprint mode](doc:fingerprint-mode).

**Portfolios using portfolio syntax**

To avoid incorrect segmentation, you must design the fingerprint so *each* element ("match") in the `match` parameter of *each* `test` in the fingerprint succeeds.

In detail, Sensible scores each test on each page of the portfolio. A test classifies a given page as a page type (for example, `first` or  `last`) only if Sensible finds all the elements in the test's `match` parameter on that page. A fingerprint that correctly identifies some of the page types and misses others can result in inaccurate segmentation. 

For more information, see [Troubleshooting portfolio fingerprints](doc:fingerprint#troubleshooting-portfolio-fingerprints).

### Chained matches

A *chained match* is an array of Match objects that Sensible scores as one match, no matter how many Match objects it contains. A chained match succeeds only if Sensible finds all its Match objects in order, on separate lines. Write chained matches using different syntax depending on whether they're in standalone or portfolio syntax.

The following table shows syntax and scoring for chained matches and other matches:

| element ('match')                                            | standalone syntax for standalone documents                   | in  this context, scores as:                                 | portfolios syntax for portfolios                             | in this context, scores as:                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| a string or a [Match](doc:match) object, including [Boolean match](doc:match#boolean-matches) | syntax is consistent                                         | one match                                                    | syntax is consistent                                         | one match                                                    |
| chained match                                                | flat array of Match objects as an element in the `tests` array: `"tests":[ [A, B],...]`. | one match                                                    | nested array in a test's `match` parameter: `"match": [[ A, B ]]` | no partial credit: the test classifies a page only if Sensible finds every Match object on that page in successive lines.<br/>For example, if two of four Match objects are on one page and two are on the next page, the test passes on neither page. |
| unordered array                                              | N/A, only flat array syntax ` [ ]` is valid, and Match arrays are always ordered | N/A</br> (**note:** If you're using portfolio syntax for a standalone document extraction, each element in the flat array scores as one match) | array of Match objects in a test's `match` parameter, `"match": [ A, B ]`. | no partial credit: the test classifies a page only if Sensible finds every Match object on that page, in any order and in any lines. <br/>For example, if two of four Match objects are on one page and two are on the next page, the test passes on neither page. |

# Notes


## Troubleshooting portfolio fingerprints

If any element in a test fails on the page the test targets, Sensible doesn't classify the page's type. If Sensible still segments the portfolio, the page ranges can be wrong. 

The following scenario illustrates incorrect segmentation in a portfolio, depending on the test's page type. 

The portfolio contains three documents:

| pages | document                                 |
| ----- | ---------------------------------------- |
| 1–2   | tax return for 2020                      |
| 3–7   | Wells Fargo bank statement               |
| 8     | pay stub                                 |

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/portfolio_bank_paystub_tax.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------ |

In the following table:

- Each row represents a separate portfolio extraction. 
- Each extraction specifies one document type that contains one config. The config's fingerprint includes a failing match.

| document | failing test | other tests in the config | effect | result |
| -------- | ------------- | ------------------------- | ------ | ------ |
| tax return, pages 1–2 | a `first` test that contains:<br/>`{"type": "endsWith", "text": "2021"}`<br/><br/>The tax return is for 2020, so the match fails on page 1. | A `last` test that passes on page 2. It has no effect, because no document is open. | Sensible doesn't start the document on that page. If no other test starts the document, Sensible doesn't find it. | Sensible doesn't return a tax return. |
| tax return, pages 1–2 | a `last` test that contains:<br/>`{"type": "includes", "text": "Form 1040-SR"}`<br/><br/>The tax return is a standard Form 1040, not the Form 1040-SR for seniors, so the match fails on page 2. | A `first` test that passes on page 1, so Sensible starts the document there. | Sensible doesn't end the document on that page. The document includes the following pages until another document starts or the portfolio ends. | Sensible returns the tax return as pages 1–8, including the bank statement and the pay stub. |
| bank statement, pages 3–7 | an `every` test that contains:<br/>`{"type": "includes", "text": "Transaction history"}`<br/><br/>The statement's transaction history starts on its second page, so the match fails on page 3. | None. | Sensible leaves that page out of the document. If the page is in the middle of the document, Sensible ends the document on the previous page, which splits the document. | Sensible returns the bank statement as pages 4–7. The pay stub on page 8 fails the `every` test, which ends the document on page 7. |
| bank statement, pages 3–7 | an `any` test that contains:<br/>`{"type": "includes", "text": "Transaction history"}`<br/><br/>The statement's transaction history starts on its second page, so the match fails on page 3. | None. | Sensible doesn't start the document on that page. The document starts on the first page where the test passes, and continues until another document starts or the portfolio ends. | Sensible returns the bank statement as pages 4–8, including the pay stub, because nothing ends the document. An `any` test doesn't end a document. **Note:** Avoid specifying an `any` page test unless other page types fail to segment the portfolio. |

Tests for other document types in the portfolio can hide these errors. For example, if the next document's `first` test passes, Sensible ends the previous document even if its `last` test failed. Design your fingerprints so that every match in every test succeeds.


## Tips for authoring fingerprints

Use the following tips when you define fingerprints.

### Alternate wordings

If you want to match alternate wordings on the same page, use an `any` [Boolean match](doc:match#boolean-matches) in a single test. For example, a form has revisions 1 and 2 that have slightly different wordings on the last page. Specify one test with a `last` page type and a match that contains wording A and wording B as follows:

```json
"fingerprint": {
  "tests": [
    {
      "page": "first",
      "match": [
        {
          "type": "includes",
          "text": "text that's always on the first page"
        }
      ]
    },
    {
      "page": "last",
      "match": [
        {
          /* the test passes on a page that contains either wording */
          "type": "any",
          "matches": [
            {
              "type": "includes",
              "text": "wording A from revision 1"
            },
            {
              "type": "includes",
              "text": "wording B from revision 2"
            }
          ]
        }
      ]
    }
  ]
}
```

### Turn off preprocessors

Sensible runs fingerprints before preprocessors. Because of this behavior, make sure to comment out any preprocessors while writing and troubleshooting fingerprints so that the document in the SenseML editor displays the lines of text exactly as Sensible recognizes them when Sensible runs the fingerprint tests.

### Standalone-specific tips

The following tips apply to fingerprints for  standalone documents.

**Test and verify fingerprints**

In the Sensible app, you can verify and test fingerprints for standalone documents against multiple reference documents at once. If you write the fingerprints with portfolio syntax, Sensible automatically converts them. For more information, see [Visual troubleshooting in the SenseML editor](doc:color#validate-fingerprints).

### Portfolio-specific tips

The following tips apply to fingerprints for portfolio documents.

**Prefer match arrays to single-match tests**

* Unless the document contains a highly unusual and characteristic `string` or `match` object, always use an array of `match` objects, rather than an array of single-match tests. In other words, don't write the following:

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

Instead, use one of the following alternatives:

```json
/* ALTERNATIVE ONE for portfolios: less strict */
"fingerprint": {
       /* one test that contains an unordered match array, so the array succeeds if the matches are on the same page  */
  "tests": [
    {
      "page": "every",
      "match": [
        /* flat array: In a flat array ("match": [ ]), Sensible searches for each element independently, so the lines can occur in any order on the page, and more than one element can match the same line. They must all occur one the same page to classify the page type. Sensible scores each element in the unordered array as one match. For more information, see Fingerprint scoring */
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

or, for stricter syntax:

```json
/* ALTERNATIVE TWO for portfolios: stricter */
"fingerprint": {
  "tests": [
    /* one test that contains a chained match array, so the array succeeds if the matches are on the same page, with additional criteria */
    {
      "page": "every",
      "match": [[
        /* In a test's match parameter, a nested array ("match": [[ ]]) is a chained match: each element matches a separate line, and Sensible must find the lines in the same order as in the array. Sensible score the whole chained match as one match. */
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

