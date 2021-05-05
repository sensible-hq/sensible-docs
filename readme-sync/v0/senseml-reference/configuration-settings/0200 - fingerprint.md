---
title: "Fingerprint"
slug: "fingerprint-1"
hidden: false
createdAt: "2021-03-22T21:53:35.136Z"
updatedAt: "2021-04-05T23:44:10.037Z"
---
Key: `fingerprint`

When running an extraction with multiple possible configs, `fingerprint` will only run those configs that pass over 50% of the tests. If no configs with `fingerprint` pass, then the extraction will run with all configs.

Fingerprint consists of an array of [AnchorMatch](ref:anchormatch) objects to test the document against (if any line in the document matches, the test passes).