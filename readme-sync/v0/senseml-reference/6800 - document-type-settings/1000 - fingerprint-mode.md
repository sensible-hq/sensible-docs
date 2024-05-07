---
title: "Fingerprint mode"
hidden: false
---

A [fingerprint](doc:fingerprint) for standalone documents changes Sensible's default behavior of running *all* the configs in a single document type. For example, if you extract company A and company B quotes, by default Sensible runs both the company A and the company B configs for a given document, then returns the extraction with the highest score. 

The following tables show how this default behavior changes when you configure the following levels of strictness for a document type's fingerprints. You can configure strictness in the Sensible app in the document type settings tab.

## Single-document file fingerprints

| Strictness level | Description                                                  | If more than one config's tests pass over 50%                | If no configs' tests passes over 50% or if no configs contain a fingerprint |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| standard         | If any of the configs in the document type contain a fingerprint, then Sensible runs extractions using any configs that pass over 50% of the fingerprint tests. | Sensible chooses the output from the passing config with the highest score | Sensible falls back to the default behavior of running extractions for the document using *all* configurations, and returns the one that has the highest score. |
| strict           | The doc type must have at least one config containing a fingerprint. | Sensible chooses the output from the passing config that has the highest score. | Sensible returns a 400 error.                                |

In the preceding table, Sensible calculates a score as follows:

`classification score` = `num of non-null fields` - `penalties for validation errors or warnings`, where penalties are as follows:

- `validation error penalty` = 1 * `num fields with validation errors`
- `validation warning penalty` = 0.5 * `num of fields with validation warnings`

The classification score is for comparing extractions within a single document type. To compare scores across document types, see [Accuracy measures](doc:accuracy-measures).

## Portfolio fingerprints

When using fingerprints for segmenting portfolio files into documents, Sensible ignores the document type's fingerprint mode setting. 

