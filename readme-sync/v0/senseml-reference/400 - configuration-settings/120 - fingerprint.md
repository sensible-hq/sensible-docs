---
title: "Fingerprint"
hidden: false
---
If you create multiple configs for a document type, Sensible automatically chooses which config's output to return. Behind the scenes, Sensible runs extractions for a document using all the configs you define in the doc type, then chooses the extraction from the config that has the highest percentage of non-null values.

You can configure this default behavior and potentially boost performance by adding a fingerprint to a config. A fingerprint tests for matching text before deciding to run or skip a config for a doc.  This can save you processing time, particularly if a config contains computationally expensive operations like selective OCR (incluing the Table and Fixed Table methods) or box recognition methods (like Box or Checkbox).  Instead of running all configs in a doc type, Sensible can quickly test a doc using a fingerprint and choose to run or skip the config up front.

For example, if you have a vendor-specific config, "anyco_life_insurance_quote" in the document type "life insurance quotes", you might write a fingerprint in the config like:

```json
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
```

This fingerprint tests that a document is a life insurance quote from Anyco by looking for three known key phrases.  



As the previous example shows, a fingerprint consists of an array of tests, where each test is a Match object or array of Match objects. A test passes if all the matches defined for the test are found in the doc.  For more information, see [Match object](doc:anchor-object#section-match-object).

In the Sensible app or  API, configure the following levels of strictness for a document type's fingerprints:

- `standard` - If any of the configs in the document type contain a fingerprint, then Sensible runs extractions using the config for which a document passes over 50% of the config's fingerprint tests.  If multiple configs pass over 50%, then choose the output with the highest percentage of non-null values. If no document passes over 50% of a config's tests, or if no config contains a fingerprint, then Sensible runs extractions for the document using all configurations, and returns the one that has the highest percentage of non-null values.  
- `strict` - If no document passes over 50% of a config's fingerprint tests, Sensible returns a 400 error. If one or more config's fingerprint passes, or if no configs contain fingerprints, then the behavior is the same as in standard mode.

