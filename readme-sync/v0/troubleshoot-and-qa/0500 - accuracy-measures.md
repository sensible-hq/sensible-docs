---
title: "Accuracy measures"
hidden: false
---

You can measure the accuracy of data that Sensible extracts from a document in the following ways:




- **Logical validations**:  Write validations in [JsonLogic](https://jsonlogic.com/) to check that fields extracted from documents meet your conditions. For example, configure Sensible to return errors if a quoted rate is null, a broker's email isn't in string@string format, or if a zip code has more than 5 digits.  For more information, see [Validate extractions](doc:validate-extractions).  
- **OCR confidence scores**: Get a score for the quality of text images. For example, check that text in a scanned or photographed document isn't blurry or illegible.  For more information, see [Validate extractions](doc:validate-extractions).  
- **Confidence signals**: For data extracted by large-language models (LLMs), Sensible asks the LLM to report any uncertainties it has about the accuracy of the extracted data. For example, an LLM can report that it found multiple answer candidates. For more information, see [Confidence signals](doc:confidence).

- **Extraction coverage:**  A score that measures how fully an extraction captured all the data in the document. It's is a percentage comparing non-null to total fields returned by a config for a document. For example, a score of 70% for an extraction means that 30% of fields were null. For more information, see the following section.

Extraction coverage
---

Extraction coverage is a score that measures how fully an extraction captured all the data in the document. A low percentage can indicate a poor-quality extraction, or it can indicate that a document type is sparsely filled out. For example, supplemental forms in insurance applications or supplemental schedules in tax forms can return many nulls, since these forms are often left blank. 

You can view an extraction's coverage through the Sensible API's extraction endpoints, or get daily coverage using the [statistics](ref:statistics) endpoint. Sensible calculates the coverage score for each extraction as follows:

`coverage score` = (`non-null fields extracted` - `validation penalties` )  ÷  (`total fields extracted`) 

Where:

- `validation penalties` =  sum of [validation](doc:validate-extractions) errors and warnings. Errors are 1 penalty point and warnings are 0.5 points.

For example, if an extraction has the following properties:

- num of non-null fields extracted = 18
- num fields extracted= 20
- num of fields with validation errors = 1
- num of fields with validation warnings = 4

Then its coverage score is 75% : (18 - 1 - 2) / 20 = 0.75. 

**Notes**

- Sensible excludes fields listed in the Suppress Output method when calculating the score.
- Sensible includes fields output in [sections](doc:sections) when calculating the score.
- The overall score for a portfolio document is the average score of all subdocument outputs.
