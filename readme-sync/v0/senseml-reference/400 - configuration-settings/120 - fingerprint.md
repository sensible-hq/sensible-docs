---
title: "Fingerprint"
hidden: false
---
If you create multiple configs for a document type, Sensible automatically chooses which config to run.

You can configure this default behavior by adding a fingerprint to a config. A fingerprint tells the config to test the document for matching text before running an extraction on the document.  For example, if you have a vendor-specific config, "anyco_life_insurance_quote" in the document type "life insurance quotes", you might write a fingerprint in the config like:

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

- `standard` - If any of the configs in the document type contain a fingerprint, then Sensible runs extractions using every config for which a document passes over 50% of the config's fingerprint tests.  If no document passes over 50% of a config's tests, Sensible runs extractions for the document using all configurations.
- `strict` - If no document passes over 50% of a config's fingerprint tests, Sensible returns a 400 error.

Note that as soon as you add a fingerprint to one config in a document type, you change Sensible's default behavior of choosing a single best config. You introduce the possibility that Sensible runs extractions on a single document using several, all, or none of the configs. 

