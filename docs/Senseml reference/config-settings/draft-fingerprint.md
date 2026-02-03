---
title: Fingerprint
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: 'Document fingerprinting for classification'
  robots: index
next:
  description: ''
---
Fingerprints test for matching text in a document to determine:

1. the document's subtype, or "config", for standalone files
2. a document's page range in multi-document, or "portfolio", files.

See the following table for more information:

| use case                                                     | description                                                                                                                                                                                                                                                                                                                                                                                 | related concepts                                                                                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [standalone documents](doc:fingerprint#standalone-documents) | Improve performance by testing for matching text in a document before running or skipping a "config," or subtype, in a specified document type. By skipping configs that fail a fingerprint, you can save processing time. This is relevant if a config contains computationally expensive operations like LLM-based methods, selective OCR, table recognition, or box recognition methods. | **Fallbacks:** <br/>Fingerprints let you fall back between configs. To fall back between fields *inside* a config, see [Fallback fields](doc:fallbacks). <br/><br/> **Classification**:<br/>Fingerprints let you determine the *subtype* of a standalone document. To determine the type of a standalone document, see [Classifying documents by type](doc:classify). |
| [portfolios](doc:fingerprint#portfolios)                     | A portfolio contains multiple documents combined into one file, such as an invoice, a contract, and a tax form. Sensible uses fingerprints to segment a portfolio into documents. Fingerprints test for matching text that characterizes first, last, or other pages for documents in the portfolio. For more information, see [Multi-document extraction](doc:portfolio).                  | Use LLMs as an alternative to fingerprints to segment [portfolios](doc:portfolio).                                                                                                                                                                                                                                                                                    |

If you use a config for both portfolio and standalone versions of the same document, Sensible automatically converts between the two and uses the appropriate fingerprint.



# Portfolios

## Parameters

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
| page                 | `first`, `last`, `every`, `any`                              | Configure with the following enums:<br/>`first` - The first page of a document segment; Sensible creates a segment split preceding the page that contains the match criteria. Use `first` to detect consecutive document segments of the same document type in a portfolio. <br/>`last` - The last page of a document segment; Sensible creates a segment split following the page that contains the match criteria.  <br/>`every` - Every page in the document segment must meet the match criteria. <br/>`any`- Any page in the document segment can meet the criteria. Avoid specifying an `any` page test unless other page types fail to segment the portfolio.<br/>**Notes:** <br/>- For an example see [Multi-document extraction](doc:portfolio). <br/>- If you reuse the same config between portfolios and standalone documents, then for standalone document extractions, Sensible ignores the configured value of this parameter. |

How it works

The mechanism for splitting the portfolio is (not sure if we want to document this, as they're heuristics and subject to change)

1.- for each page we run the fingerprints of every configuration in every document type specified in the portfolio extraction request.

2.- Then we go from the first to the last page. We keep a list of "potential configurations". On each page:

- if there is at least one "first" match, the previous and current pages are in different documents.
- if there is a match for a configuration that didn't match in the current "potential configurations", the previous and current pages are in different documents.
- if there is some configuration on the current "potential configurations" that has an "every" fingerprint and it doesn't match, the previous and current pages are in different documents.
- if there is at least one "last" match, the current and next pages are in different documents.

3.- This defines a set of page ranges and the potential configurations that can correspond to the document on that page range. We try to extract data from that page range using those configurations and choose the best extraction.

In cases where the configurations correspond to very different documents (so there is no page that matches more than one configuration) I've taken care to keep the same behaviour as before.

## Example of heuristics in action





| Page | Fingerprint matches which config in which document type? (document type/config + fingerprint type) | Split condition?                             | Action                                                       |
| ---- | ------------------------------------------------------------ | -------------------------------------------- | ------------------------------------------------------------ |
| 1    | 1040s/1040_2019 (first)                                      | YES: "first" match                           | start new 'current document/current config'                  |
| 2    | none                                                         | NO                                           | continue 'current document/current config'                   |
| 3    | paystubs/gusto (first)                                       | YES: "first" match                           | end current doc on prev page<br/>start new 'current document/current config' |
| 4    | none                                                         | NO                                           | continue 'current document/config'                           |
| 5    | paystubs/paylocity (every)                                   | YES: new config has been matched             | end current doc on prev. page<br/>start new 'current document/config' |
| 6    | paystubs/paylocity (every)                                   | NO                                           | continue 'current document/config'                           |
| 7    | none                                                         | YES: `every` match for current config failed | end current doc on prev. page. <br/>current documents/configs = null. this page ignored, won't appear in any document range) |
| 8    | none                                                         | NO                                           | page ignored, won't appear in any document range             |
| 9    | bank_statements/boa (first), bank_statments/boa (every)      | YES: "first" match                           | start new current document/config                            |
| 10   | bank_statements/boa (every)                                  | NO                                           |                                                              |
| 11   | none                                                         | YES: "every" match for current config failed | end current document/config on this page.<br/>current docs/configs = null |
| 12   | TODO: show edge case here w/ 2 matching configs here (frm diff. doc types)...worth it to show complexity...? |                                              |                                                              |
| 13   | none                                                         | NO, current doc/config is null               | page ignored, won't appear in any document range             |
| 14   | none. this is the last page of portfolio                     |                                              | page ignored, won't appear in any document range             |

portfolio document types/configs that are tested against in above example:

1040s

​     1040_2018

​      1040_2019

paystubs

​       gusto

​       Paylocity

​       fallback_llm

bank_statments

​       boa

![image-20260202170759080](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20260202170759080.png)

https://claude.ai/chat/8575cee2-0e6c-4497-9c62-c5f978df7bf6 
