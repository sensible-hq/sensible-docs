---
title: "Fingerprint mode"
hidden: false
---

[Fingerprints](doc:fingerprint) test for matching text in a document to determine:

1. the document's subtype for standalone files
2. the document's page range in multi-document, or "portfolio", files.

The Fingerprint Mode configuration option applies to scenario 1, not scenario 2.  You can configure this option in the Sensible app in the document type settings tab.

## Standalone files

Fingerprints improve performance by testing for matching text in a single document before running or skipping a config in a specified document type.  

The Fingerprint Mode configuration option determines the strictness of the tests as follows:

| Are fingerprinted configs present in doctype? | Fingerprint test results                                     | Normal mode                                                  | Strict mode |
| --------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ----------- |
| yes                                           | One or more fingerprinted configs passes.<br/> A config passes if 50% or more of tests in a config match text in document. | - Run extractions for all fingerprinted configs that pass<br/>- Skip extractions for non-fingerprinted configs if present in document type | Same        |
| yes                                           | All fingerprinted configs fail                               | - If non-fingerprinted configs are present, run all *non*-fingerprinted configs and skip fingerprinted configs<br/>- If all configs are fingerprinted, run all configs | 400 error   |
| no                                            | N/A                                                          | Run all configs                                              | 400 error   |

After Sensible runs and skips extractions,  it returns the extraction that ran with the highest-scoring config.  Sensible calculates the score as follows: ` score` = `num of non-null fields` - `penalties for validation errors or warnings`, where penalties are as follows:

- `validation error penalty` = 1 * `num fields with validation errors`

- `validation warning penalty` = 0.5 * `num of fields with validation warnings`

## Portfolio files

Sensible ignores the document type's Fingerprint Mode setting for portfolio files. 

