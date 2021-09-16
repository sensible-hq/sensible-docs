---
title: "Fingerprint"
hidden: false
---
Improves performance by testing for matching text in a document in order to run or skip a config.  By skipping configs that fail a fingerprint, you can save processing time. This is particularly true if a config contains computationally expensive operations like selective OCR, table recognition, or box recognition methods. 

A fingerprint changes Sensible's default behavior of running *all* the configs in a single document type in order to automatically choose which config's output to return.  For example, if you extract company A and company B quotes, by default Sensible runs both the company A and the company B configs for a given document, then returns the best of the two extractions (i.e., the one with the highest percent of non-null values). 

Parameters
====

A fingerprint consists of an array of tests, where each test is a string, a Match object, or array of Match objects.  For more information, see [Match object](doc:match).

In the Sensible app, configure the following levels of strictness for a document type's fingerprints:

| Strictness level | Description                                                  | If multiple configs' fingerprints pass over 50%              | If no configs' fingerprint passes over 50% or if no configs contain a fingerprint |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| standard         | If any of the configs in the document type contain a fingerprint, then Sensible runs extractions using any configs that pass over 50% of the fingerprint tests | Sensible chooses the output from the passing config that has the highest percentage of non-null values. | Sensible falls back to the default behavior of running extractions for the document using *all* configurations, and returns the one that has the highest percentage of non-null values. |
| strict           | The doc type is required to have at least one config containing a fingerprint. | Sensible chooses the output from the passing config that has the highest percentage of non-null values. | Sensible returns a 400 error.                                |

Examples
====

The following fingerprint tests a vendor-specific config "anyco_life_insurance_quote" in a document type "life insurance quotes". This fingerprint tests that a document is a life insurance quote from Anyco by looking for three known key phrases. 

```json
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

The config preferentially runs only if the fingerprint finds the phrases.  

