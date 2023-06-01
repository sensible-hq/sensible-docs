---
title: "Accuracy measures"
hidden: true
---

You can measure the accuracy of data extracted from a document in the following ways:




- **Logic validations**:  Write validations in [JsonLogic](https://jsonlogic.com/) to check that fields extracted from documents meet your conditions. For example, configure Sensible to return errors if a quoted rate is null, a broker's email isn't in string@string format, or if a zip code has more than 5 digits.  For more information, see [Validate extractions](doc:validate-extractions).  
- **OCR confidence scores**: Get a score for the quality of text images. For example, check that text in a scanned or photographed document isn't blurry or illegible.  For more information, see [Validate extractions](doc:validate-extractions).  
- **Uncertainties**: 





- ****

-  For deterministic asnwers. Why does Sensible use validation tests rather than confidence intervals? Sensible's extractions are largely deterministic. With the exception of OCR-dependent output, a Sensible config always returns the same output for a given PDF input. Given this, deterministic validation tests are more useful than confidence intervals as measures of extraction quality. 

- OCR confidence scores: For scanned text

- Uncertainties: Sensible asks the LLM to report any issues with its answer. These reports are generative and not 100% accurate, but they tend to be more useful than confidence scores, which in Sensible's experience often fall into either buckets of 100% uncertainty or 0% uncertainty and are therefore not useful for the sort of nuance that is helpul in troubleshooting. Uncertainties provide more nuanced ground for troubleshooting. As the research paper [Teaching models to express their uncertainties in words](https://arxiv.org/pdf/2205.14334.pdf) suggests, Uncertainties may arise from but not limited to: multiple answers, answer not solving the question, answer not in the context, and ambiguous question. Sensible prompts the LLM to return uncertainties as follows. 
