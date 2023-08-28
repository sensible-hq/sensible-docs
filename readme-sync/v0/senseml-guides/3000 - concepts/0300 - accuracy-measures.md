---
title: "Accuracy measures"
hidden: false
---

You can measure the accuracy of data that Sensible extracts from a document in the following ways:




- **Logical validations**:  Write validations in [JsonLogic](https://jsonlogic.com/) to check that fields extracted from documents meet your conditions. For example, configure Sensible to return errors if a quoted rate is null, a broker's email isn't in string@string format, or if a zip code has more than 5 digits.  For more information, see [Validate extractions](doc:validate-extractions).  
- **OCR confidence scores**: Get a score for the quality of text images. For example, check that text in a scanned or photographed document isn't blurry or illegible.  For more information, see [Validate extractions](doc:validate-extractions).  
- **Confidence signals**: For data extracted by large-language models (LLMs), Sensible asks the LLM to report any uncertainties it has about the accuracy of the extracted data. For example, an LLM can report that it found multiple answer candidates. For more information, see [Confidence signals](doc:confidence).

- **Quality scores and statistics:** Sensible scores each extraction using the number of fields extracted versus those defined in the config and other information. It also aggregates statistics about how configs are performing and how much they're used.  For more information, see the following section.

Quality scores
---

You can view an extraction's quality score through the Sensible API's extraction endpoints, or aggregated scores using the [statistics](ref:statistics) endpoint. Sensible calculates the quality score for each extraction as follows:

`quality score` = (`non-null fields extracted` - `validation penalities` ) / `total fields defined in config` 

Where:

- `validation penalties` =  sum of [validation](doc:validate-extractions) errors and warnings. Errors are 1 penalty point and warnings are 0.5 points.

For example, if an extraction A has the following properties:

- num fields defined in the configuration = 20

- num of non-null fields = 18
- num of fields with validation errors = 1
- num of fields with validation warnings = 4

Then its quality score is 75% : (18 - 1 - 2) / 20 = 0.75. 

**Notes**

- Sensible excludes fields listed in the Suppress Output method when calculating the quality score.
- The overall quality score for a portfolio document is the average score of all subdocument outputs.

