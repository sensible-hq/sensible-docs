---
title: "Accuracy measures"
hidden: false
---

You can measure the accuracy of data that Sensible extracts from a document in the following ways:


- **Logical validations**:  Write validations in [JsonLogic](https://jsonlogic.com/) to check that fields extracted from documents meet your conditions. For example, configure Sensible to return errors if a quoted rate is null, a broker's email isn't in string@string format, or if a zip code has more than 5 digits.  For more information, see [Validate extractions](doc:validate-extractions).  
- **OCR confidence scores**: Get a score for the quality of text images. For example, check that text in a scanned or photographed document isn't blurry or illegible.  For more information, see [Validate extractions](doc:validate-extractions).  
- **Confidence signals**: For data extracted by large language models (LLMs), Sensible asks the LLM to report any uncertainties it has about the accuracy of the extracted data. For example, an LLM can report that it found multiple answer candidates. For more information, see [Qualifying LLM accuracy](doc:confidence).

- **Extraction coverage:**  A score that measures how fully an extraction captured all the data in the document. It's a percentage comparing non-null, [validated](doc:validate-extractions) fields to total fields returned by a config for a document. For example, a coverage score of 70% for an extraction with no validation errors means that 30% of fields were null. For more information, see [Monitoring extraction metrics](doc:metrics).
