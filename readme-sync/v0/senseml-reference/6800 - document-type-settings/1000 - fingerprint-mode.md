---
title: "Fingerprint mode"
hidden: false
---

[Fingerprints](doc:fingerprint) test for matching text in a document to determine:

1. the document's subtype for single-document files
2. the document's page range in multi-document files.

The Fingerprint Mode configuration option applies to scenario 1, not to scenario 2.  You can configure this option in the Sensible app in the document type settings tab.

## Single-document file

Fingerprints improve performance by testing for matching text in a single-document document before running or skipping a config in a specified document type.  

The Fingerprint Mode configuration option determines the strictness of the tests as follows:

| Strictness level | Description                                                  | If more than one config's tests pass over 50%                | If no configs' tests passes over 50% or if no configs contain a fingerprint |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| standard         | If any of the configs in the document type contain a fingerprint, then Sensible runs extractions using any configs that pass over 50% of the fingerprint tests. | Sensible chooses the output from the passing config with the highest score | Sensible falls back to the default behavior of running extractions for the document using *all* configurations, and returns the one that has the highest score. |
| strict           | The doc type must have at least one config containing a fingerprint. | Sensible chooses the output from the passing config that has the highest score. | Sensible returns a 400 error.                                |

In the preceding table, Sensible calculates a score as follows:

` score` = `num of non-null fields` - `penalties for validation errors or warnings`, where penalties are as follows:

- `validation error penalty` = 1 * `num fields with validation errors`
- `validation warning penalty` = 0.5 * `num of fields with validation warnings`

## Portfolio file

When using fingerprints for segmenting portfolio files into documents, Sensible ignores the document type's Fingerprint Mode setting. 

