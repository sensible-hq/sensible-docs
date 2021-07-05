---
title: "Fingerprint"
hidden: false
---
If you create multiple configs for a document type, Sensible automatically chooses which config's output to return. You can configure this default behavior and potentially boost performance by adding a fingerprint to a config.

 A fingerprint tests for matching text before deciding to run or skip a config for a doc.  This is in contrast to the default behavior. By default, Sensible runs extractions for a document using *all* the configs you define for the doc type, then chooses the extraction from the config that has the highest percentage of non-null values. By skipping configs that fail a document's fingerprint, you can save processing time. This is particularly true if a config contains computationally expensive operations like selective OCR (including the Table and Fixed Table methods) or box recognition methods (like Box or Checkbox).  

For example, if you have a vendor-specific config, "anyco_life_insurance_quote" in the document type "life insurance quotes", you might write a fingerprint in the config like:

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

This fingerprint tests that a document is a life insurance quote from Anyco by looking for three known key phrases, and preferentially runs the config only if it finds the phrases.  

As the previous example shows, a fingerprint consists of an array of tests, where each test is a string, a Match object, or array of Match objects. A test passes if all the matches defined for the test are found in the doc.  For more information, see [Match object](doc:match-object).

In the Sensible app or  API, configure the following levels of strictness for a document type's fingerprints:

- `standard` - If any of the configs in the document type contain a fingerprint, then Sensible runs extractions using any configs that pass over 50% of the tests:
  -   If multiple configs pass over 50%, then Sensible chooses the output with the highest percentage of non-null values.
  - If no document passes over 50% of a config's fingerprint tests, or if no config contains a fingerprint, then Sensible runs extractions for the document using *all* configurations, and returns the one that has the highest percentage of non-null values.  
- `strict` - The doc type is required to have at least one config containing a fingerprint.
  - If no document passes over 50% of a config's fingerprint tests, or if no config contains a fingerprint in the doc type, Sensible returns a 400 error.
  -  If one or more configs' fingerprint passes, then the behavior is the same as in standard mode. 

