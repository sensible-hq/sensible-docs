---
title: "Document type configuration"
hidden: false
---



You can make the following In the document type configuration pane in the Sensible app or using the Sensible API:


OCR engine
-----

Choose one of the following:

| OCR engine          | page limit | notes                                                        |
| ------------------- | ---------- | ------------------------------------------------------------ |
| Microsoft (default) | n/a        | best for typewritten and long documents                      |
| Amazon              | 25         | faster than Microsoft and best for handwriting and short documents |
| Google              | ?          | The Google engine does not merge words into lines automatically. Use the [mergeLines preprocessor](https://docs.sensible.so/docs/merge-lines#handwriting-ocr) in your configurations to do so. |



Fingerprint mode
-----

Choose between **Standard** and **Strict**. FOr more information, see [Fingerprints](doc:fingerprint#notes).
