---
title: "Bag of words"
hidden: true
---

Sensible uses the bag of words approach (measuring the frequency of word occurence) for tasks such as identifying topics or tables in a document. Sensible cleans up strings in Terms and Stop Terms parameters in preparation for the bag of words using:

- stemming - Sensible uses a [Porter stemmer](https://tartarus.org/martin/PorterStemmer/index.html)
- tokenization - Sensible creates tokens by splitting on spaces. This means that you can specify individual words, not phrases, for each term or stop term in an array.





