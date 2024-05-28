---
title: "(Deprecated) Bag of words"
hidden: true
---

Sensible uses the bag of words approach (measuring the frequency of word occurrence) for tasks such as identifying topics or tables in a document. As part of creating a vocabulary for the bag of words, Sensible processes strings in Terms and Stop Terms parameters using:

- stemming - Sensible uses a [Porter stemmer](https://tartarus.org/martin/PorterStemmer/index.html).
- tokenization - Sensible creates tokens by splitting on spaces.



