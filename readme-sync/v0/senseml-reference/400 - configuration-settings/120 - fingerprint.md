---
title: "Fingerprint"
hidden: false
---
Tests for matching text in a doc in order to run or skip a config.  By skipping configs that fail a fingerprint, you can improve performance. This is particularly true if a config contains computationally expensive operations like selective OCR, table recognition, or box recognition methods. 

A fingerprint changes Sensible's default behavior of running *all* the configs in a single document type in order to automatically choose which config's output to return.  For example, if you extract company A and company B quotes, by default Sensible runs both the company A and the company B configs for a given document, then returns the best of the two extractions (i.e., the one with the highest percent of non-null values). 

For example, to test a vendor-specific config "anyco_life_insurance_quote" in a document type "life insurance quotes", you might write a fingerprint in the config like:

```json
{
  "fingerprint": {
    "tests": [
      {
        "type": "startsWith",
        "text": "Anyco"
      },
      "info@anyco.com",
      "life insurance quote"
    ]
  },
  "fields": []
}
```

This fingerprint tests that a document is a life insurance quote from Anyco by looking for three known key phrases. The config preferentially runs only if the fingerprint finds the phrases.  

As the previous example shows, a fingerprint consists of an array of tests, where each test is a string, a Match object, or array of Match objects.  For more information, see [Match object](doc:match).

In the Sensible app or  API, configure the following levels of strictness for a document type's fingerprints:

- `standard` - If any of the configs in the document type contain a fingerprint, then Sensible runs extractions using any configs that pass over 50% of the tests:
  -   If multiple configs pass over 50%, then Sensible chooses the output with the highest percentage of non-null values.
  - If no document passes over 50% of a config's fingerprint tests, or if no config contains a fingerprint, then Sensible runs extractions for the document using *all* configurations, and returns the one that has the highest percentage of non-null values.  
- `strict` - The doc type is required to have at least one config containing a fingerprint.
  - If no document passes over 50% of a config's fingerprint tests, or if no config contains a fingerprint in the doc type, Sensible returns a 400 error.
  -  If one or more configs' fingerprint passes, then the behavior is the same as in standard mode. 

