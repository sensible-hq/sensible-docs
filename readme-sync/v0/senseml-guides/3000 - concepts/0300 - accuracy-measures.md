---
title: "Accuracy measures"
hidden: false
---

You can measure the accuracy of data that Sensible extracts from a document in the following ways:




- **Logical validations**:  Write validations in [JsonLogic](https://jsonlogic.com/) to check that fields extracted from documents meet your conditions. For example, configure Sensible to return errors if a quoted rate is null, a broker's email isn't in string@string format, or if a zip code has more than 5 digits.  For more information, see [Validate extractions](doc:validate-extractions).  
- **OCR confidence scores**: Get a score for the quality of text images. For example, check that text in a scanned or photographed document isn't blurry or illegible.  For more information, see [Validate extractions](doc:validate-extractions).  
- **Confidence signals**: For data extracted by large-language models (LLMs), Sensible asks the LLM to report any uncertainties it has about the accuracy of the extracted data. For example, an LLM can report "multiple possible answers" or "ambiguous query".  These confidence *signals* are more useful for troubleshooting than confidence *scores*, since confidence scores tend to fall into buckets of 0% or 100% accuracy. Note that LLMs can inaccurately report confidence signals.  For more information about confidence signals, see the research paper [Teaching models to express their uncertainties in words](https://arxiv.org/pdf/2205.14334.pdf).  For more information about troubleshooting confidence signals, see [Query extraction tips](doc:query-tips).
