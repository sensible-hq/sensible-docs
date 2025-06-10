---
title: "Fingerprint mode"
hidden: true
---

# update: todo: diagram it out??

If the strictness level is standard, and we don't have any matching fingerprints, but we do have one or more no-fingerprint configs, we run those and don't run the failing fingerprint configs. We only run all the configs in the case where they all have fingerprints, they all fail, and the mode is not strict. Here's the annotated code:

```
  if (successes.length > 0) { // We found matching fingerprints, use those, don't use configs with no fingerprints
    return { successes, failed: [...noFingerprints, ...failed] };
  } else if (schema && schema.fingerprint_mode === "strict") { // We didn't find matching fingerprints and we're in strict mode, fail out
    // Error out in strict mode
    throw new NoMatchingFingerprintException();
  }

  if (noFingerprints.length > 0) { // We didn't find matching fingerprints, but we're not in strict mode and we have configs with no fingerprints, use those
    return { successes: noFingerprints, failed };
  }

  // We didn't find matching fingerprints, we're not in strict mode, and we don't have any configs without fingerprints, RUN EVERYTHING!
  return { successes: failed, failed: [] };
```



# end update

[Fingerprints](doc:fingerprint) test for matching text in a document to determine:

1. the document's subtype for standalone files
2. the document's page range in multi-document, or "portfolio", files.

The Fingerprint Mode configuration option applies to scenario 1, not scenario 2.  You can configure this option in the Sensible app in the document type settings tab.

## Standalone files

Fingerprints improve performance by testing for matching text in a single-document document before running or skipping a config in a specified document type.  

The Fingerprint Mode configuration option determines the strictness of the tests as follows:

| Strictness level | Description                                                  | If more than one config's tests pass over 50%                | If no configs' tests pass over 50%                           | If no configs contain a fingerprint                          |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| standard         | If any of the configs in the document type contain a fingerprint, then Sensible runs extractions using any configs that pass over 50% of the fingerprint tests. | Sensible chooses the output from the passing config with the highest score | Sensible ignores the failing configs. Sensible runs all the configs with no fingerprints and chooses the one with the highest score. | Sensible falls back to the default behavior of running extractions for the document using *all* configurations, and returns the one with the highest score. |
| strict           | The doc type must have at least one config containing a fingerprint. | Sensible chooses the output from the passing config that has the highest score. | Sensible returns a 400 error.                                | Sensible returns a 400 error.                                |

In the preceding table, Sensible calculates a score as follows:

` score` = `num of non-null fields` - `penalties for validation errors or warnings`, where penalties are as follows:

- `validation error penalty` = 1 * `num fields with validation errors`
- `validation warning penalty` = 0.5 * `num of fields with validation warnings`

## Portfolio files

Sensible ignores the document type's Fingerprint Mode setting for portfolio files. 

