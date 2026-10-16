---
title: Fingerprint
excerpt: >-
  Learn how fingerprints test documents for matching text, so you can choose the
  config for a standalone document or find each document's pages in a portfolio.
deprecated: false
hidden: false
metadata:
  title: ''
  description: >-
    Learn how fingerprints test documents for matching text, so you can choose
    the config for a standalone document or find each document's pages in a
    portfolio.
  robots: index
next:
  description: ''
---
With fingerprints, you test for matching text in a document to determine:

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
| tests | array, where each element is a string, a [Match](doc:match) object, or a [chained match](doc:fingerprint#chained-matches) | Sensible runs the configs whose fingerprints pass. |

## Examples

The following example tests whether a standalone document is a Wells Fargo checking account statement, for a vendor-specific config in a bank statements document type.

```json
/* Sensible uses JSON5 to support in-line comments */
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
         If a Match object fails, the chained match fails */
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

A fingerprint for portfolios contains a Tests parameter that takes an array of test objects. The following table shows the parameters for each test object:

| key                  | value                                                        | description for portfolios                                   |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| match (**required**) | a string, a [Match object](doc:match), an array of unordered Match objects, or a [chained match](doc:fingerprint#chained-matches) | Specifies the text to match. Sensible uses matches to segment a document's page range in portfolio files. |
| offset               | integer                                                      | Specifies where to start or end the document segment, offset in pages relative to the first or last page defined by the Match parameter. For example, if you specify that the page that contains the phrase "A summary of your rights" is the first page of a segment, and Sensible finds that match on the zero-indexed page 5 of a portfolio:<br/>- specifying `"offset": -1` starts the document segment on page 4 of the portfolio.<br/>- specifying `"offset": 2` starts the document segment on page 7 of the portfolio. |
| page                 | `first`, `last`, `every`, `any`                              | Configure with the following enums:<br/>`first` - The first page of a document segment must meet the match criteria. Use `first` to detect consecutive document segments of the same document type in a portfolio. <br/>`last` - The last page of a document segment must meet the match criteria. <br/>`every` - Every page in the document segment must meet the match criteria. <br/>`any`- Any page in the document segment can meet the criteria. **Note:** Avoid specifying an `any` page test unless other page types fail to segment the portfolio.<br/><br/>Sensible recommends the following page type pairings in fingerprints:<br/>- pair `first` with another page type, such as `every` or `last`.<br/>- pair `last` with a different page type, such as `every`.<br/>- pair `every` with a different page type, such as `last`. |

## Examples

For an example of using fingerprints to extract multiple documents from a portfolio file, see [Multi-document extraction](doc:portfolio#fingerprint-example). 

# Concepts

## Fingerprint syntax conversion

If you use a config in both standalone and portfolio extraction requests, write its fingerprint in the stricter portfolio syntax. Sensible automatically converts between the two syntaxes as follows:

- To convert to portfolio syntax, Sensible expands standalone syntax into a test with `"page": "any"`.
- To convert to standalone syntax, Sensible keeps the value of each test's Match parameter and ignores the Page and Offset parameters.

## Fingerprint scoring

Sensible scores fingerprints differently for standalone documents and for portfolios.

**Standalone documents using standalone syntax**

For the config to pass, Sensible must find 50% or more of the elements, or "matches," in the Tests parameter.

Sensible searches the whole document for each element in the fingerprint. If more than one config passes, Sensible runs all the configs that pass and returns the extraction with the highest score. For information about configuring the strictness with which Sensible runs or skips configs, see [Fingerprint mode](doc:fingerprint-mode).

**Portfolios using portfolio syntax**

To avoid incorrect segmentation, design the fingerprint so that *every* element, or "match," in the Match parameter of *every* test succeeds.

Sensible scores each test on each page of the portfolio. A test classifies a page as its page type, for example `first` or `last`, only if Sensible finds all the elements in the test's Match parameter on that page. A fingerprint that correctly identifies some of the page types and misses others can result in inaccurate segmentation. 

For more information, see [Troubleshooting portfolio fingerprints](doc:fingerprint#troubleshooting-portfolio-fingerprints).

## Chained matches

A *chained match* is an array of Match objects that Sensible scores as one match, no matter how many Match objects it contains. A chained match succeeds only if Sensible finds all its Match objects in order, on separate lines. You write a chained match differently in standalone syntax and in portfolio syntax.

The following table shows syntax and scoring for chained matches and other matches:

| element ('match')                                                                             | standalone syntax for standalone documents                                                   | in this context, scores as:                                                                                                                    | portfolio syntax for portfolios                                         | in this context, scores as:                                                                                                                                                                                                                                                                                        |
| --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| a string or a [Match](doc:match) object, including [Boolean match](doc:match#boolean-matches) | syntax is consistent                                                                         | one match                                                                                                                                      | syntax is consistent                                                    | one match                                                                                                                                                                                                                                                                                                          |
| chained match                                                                                 | flat array of Match objects as an element in the Tests parameter: `"tests": [ [A, B], ... ]` | one match                                                                                                                                      | nested array in a test's Match parameter: `"match": [[ A, B ]]`         | no partial page typing: For example, if two of four Match objects are on one page and two are on the next page, the test passes on neither page.<br/>The test classifies a page only if Sensible finds every Match object on that page, in order, on separate lines.<br />                                         |
| unordered array                                                                               | N/A. Only flat array syntax `[ ]` is valid, and it's always a chained match.                 | N/A</br> (**note:** If you're using portfolio syntax for a standalone document extraction, each element in the flat array scores as one match) | array of Match objects in a test's Match parameter: `"match": [ A, B ]` | no partial page typing: For example, if two of four Match objects are on one page and two are on the next page, the test passes on neither page.<br/>The test classifies a page only if Sensible finds every Match object on that page. Matches can be in any order and don't have to be in separate lines. <br /> |

# Notes


## Troubleshooting portfolio fingerprints

If any element in a test fails on the page the test targets, Sensible doesn't classify the page's type. Sensible still segments the portfolio, but the page ranges can be wrong.

The following scenario shows how incorrect segmentation depends on the test's page type. The example portfolio contains three documents:

- pages 1–2: tax return for 2020
- pages 3–7: Wells Fargo bank statement
- page 8: pay stub

<!-- table test {"testId": "portfolio_failures_tests", "table": "portfolio_failures", "segment_documents_with": "fingerprints", "description": "Each row of the portfolio troubleshooting table"} -->
<!-- inline document -->
| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/portfolio_bank_paystub_tax.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------ |

In the following table:

- Each row represents a separate portfolio extraction of the example portfolio.
- Each extraction specifies one document type that contains one config. The config's fingerprint includes a failing match.

<!-- table {"tableId": "portfolio_failures"} -->
| document | failing test | other tests in the config | effect | result |
| -------- | ------------- | ------------------------- | ------ | ------ |
| tax return, pages 1–2 | a `first` test that contains:<br/>`{"type": "endsWith", "text": "2021"}`<br/><br/>The tax return is for 2020, so the match fails on page 1. | A `last` test that passes on page 2. It has no effect, because no document is open. | Sensible doesn't start the document on that page. If no other test starts the document, Sensible doesn't find it. | Sensible doesn't return a tax return. |
| tax return, pages 1–2 | a `last` test that contains:<br/>`{"type": "includes", "text": "Form 1040-SR"}`<br/><br/>The tax return is a standard Form 1040, not the Form 1040-SR for seniors, so the match fails on page 2. | A `first` test that passes on page 1, so Sensible starts the document there. | Sensible doesn't end the document on that page. The document includes the following pages until another document starts or the portfolio ends. | Sensible returns the tax return as pages 1–8, including the bank statement and the pay stub. |
| bank statement, pages 3–7 | an `every` test that contains:<br/>`{"type": "includes", "text": "Transaction history"}`<br/><br/>The statement's transaction history starts on its second page, so the match fails on page 3. | None. | Sensible leaves that page out of the document. If the page is in the middle of the document, Sensible ends the document on the previous page, which splits the document. | Sensible returns the bank statement as pages 4–7. The pay stub on page 8 fails the `every` test, which ends the document on page 7. |
| bank statement, pages 3–7 | an `every` test that contains:<br/>`{"type": "regex", "pattern": "Page [1245] of 7"}`<br/><br/>The regular expression matches the statement's page numbers except for `Page 3 of 7`, so the match fails on page 5. | None. | Sensible ends the document on the previous page, and starts a new document on the next page where the test passes, which splits the document. | Sensible returns two bank statements, pages 3–4 and pages 6–7. The pay stub on page 8 fails the `every` test, which ends the second statement on page 7. |
| bank statement, pages 3–7 | an `any` test that contains:<br/>`{"type": "includes", "text": "Transaction history"}`<br/><br/>The statement's transaction history starts on its second page, so the match fails on page 3. | None. | Sensible doesn't start the document on that page. The document starts on the first page where the test passes, and continues until another document starts or the portfolio ends. | Sensible returns the bank statement as pages 4–8, including the pay stub, because nothing ends the document. An `any` test doesn't end a document. **Note:** Avoid specifying an `any` page test unless other page types fail to segment the portfolio. |

<!-- row {"rowId": "first_test_fails", "fixture": {"name": "fixture_fp_demo_first_fails"}, "expect": {"compare": "documents", "documents": []}} -->
<!-- row {"rowId": "last_test_fails", "fixture": {"name": "fixture_fp_demo_last_fails"}, "expect": {"compare": "documents", "documents": [["fixture_last_fails", 1, 8]]}} -->
<!-- row {"rowId": "every_test_fails_first_page", "fixture": {"name": "fixture_fp_demo_every_fails"}, "expect": {"compare": "documents", "documents": [["fixture_every_fails", 4, 7]]}} -->
<!-- row {"rowId": "every_test_fails_mid_document", "fixture": {"name": "fixture_fp_demo_every_split"}, "expect": {"compare": "documents", "documents": [["fixture_every_split", 3, 4], ["fixture_every_split", 6, 7]]}} -->
<!-- row {"rowId": "any_test_fails", "fixture": {"name": "fixture_fp_demo_any_fails"}, "expect": {"compare": "documents", "documents": [["fixture_any_fails", 4, 8]]}} -->
<!-- table test end -->

Tests for other document types in the portfolio can hide these errors. For example, if the next document's `first` test passes, Sensible ends the previous document even if its `last` test failed. Design your fingerprints so that every match in every test succeeds. When troubleshooting, test one document type at a time.


## Tips for authoring fingerprints

Use the following tips when you define fingerprints.

### When to use chained matches

A [chained match](doc:fingerprint#chained-matches) is stricter than separate matches, because Sensible must find all its lines in order. Use chained matches in the following situations:

- **Portfolio&#x20;**`first`**&#x20;and&#x20;**`last`**&#x20;tests**: a chained match is less likely to classify a page in another document as the first or last page of this one.
- **Document types with many similar configs**: for example, a document type with many configs for different layouts from the same vendor. A chain of 3–4 lines distinguishes configs whose individual phrases overlap.
- **Strict&#x20;**[Fingerprint mode](doc:fingerprint-mode): if you use strict mode to avoid extracting documents you haven't written a config for, chained matches make each fingerprint less likely to pass for those documents.

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

Sensible runs fingerprints before preprocessors. While you write and troubleshoot fingerprints, comment out any preprocessors, so that the SenseML editor displays the lines of text exactly as Sensible recognizes them when it runs the fingerprint tests.

### Standalone-specific tips

The following tips apply to fingerprints for standalone documents.

**Test and verify fingerprints**

In the Sensible app, you can test fingerprints for standalone documents against multiple reference documents at once. If you write the fingerprints with portfolio syntax, Sensible automatically converts them. For more information, see [Visual troubleshooting in the SenseML editor](doc:color#validate-fingerprints).

### Portfolio-specific tips

The following tips apply to fingerprints for portfolio documents.

**Prefer match arrays to single-match tests**

Unless the document contains highly unusual, characteristic text, put related matches in one test, rather than writing a separate test for each match. A passing single-match test classifies the page even if another single-match test fails on that page, so separate tests are less strict. For example, don't write the following:

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
        /* flat array: In a flat array ("match": [ ]), Sensible searches for each element independently, so the lines can occur in any order on the page, and more than one element can match the same line. They must all occur on the same page to classify the page type. If this fingerprint runs in a standalone-document extraction, Sensible scores each element as one match. For more information, see Fingerprint scoring */
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
        /* In a test's match parameter, a nested array ("match": [[ ]]) is a chained match: each element matches a separate line, and Sensible must find the lines in the same order as in the array. Sensible scores the whole chained match as one match. */
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