---
title: "Accuracy and quality measures"
hidden: true
---

Accuracy
---


You can measure the accuracy of data that Sensible extracts from a document in the following ways:


- **Logical validations**:  Write validations in [JsonLogic](https://jsonlogic.com/) to check that fields extracted from documents meet your conditions. For example, configure Sensible to return errors if a quoted rate is null, a broker's email isn't in string@string format, or if a zip code has more than 5 digits.  For more information, see [Validate extractions](doc:validate-extractions).  
- **OCR confidence scores**: Get a score for the quality of text images. For example, check that text in a scanned or photographed document isn't blurry or illegible.  For more information, see [Validate extractions](doc:validate-extractions).  
- **Confidence signals**: For data extracted by large-language models (LLMs), Sensible asks the LLM to report any uncertainties it has about the accuracy of the extracted data. For example, an LLM can report that it found multiple answer candidates. For more information, see [Confidence signals](doc:confidence).

- **Quality scores and statistics:** Sensible scores each extraction using the number of fields extracted versus those defined in the config and other information. It also aggregates statistics about how configs are performing and how much they're used. 

Quality statistics (separate topic?)
---

You can get individual and aggregate statistics about the quality of extractions.

**Quality buckets**

You can filter extractions by the following 12 “buckets” of aggregated extraction quality scores:

![image-20230802135848603](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20230802135848603.png)

- [0, 10)

-  [10, 20)

-  [20, 30)

-  [30, 40)

- [40, 50)

- [50, 60)

-  [60, 70)

-  [70, 80)

-  [80, 90)

-  [90, 95)

-  [95, 100)

- [100] 

  `[` denotes inclusive whereas `)` is exclusive

For example, a document extraction with a quality score of .85, or 85%, falls into the  [80, 90) bucket.

Sensible returns the histogram in the preceding image as an array through the [API](ref:statistics). For example, when the API returns ``"quality_score_histogram":[7,5,3,3,2,1,1,4,7,9,13,15]` , the first and last items in the array  show that on a given day for a given config, 7 extractions scored in the lowest bucket of 0-10%, and 15 scored in the highest bucket of 100%.

From this array, you can calculate other metrics or view them in the Sensible app, for example: 

- total number of extractions in a time period
- doc type / config usage (# of relevant extractions / total extractions)
- daily stats (i.e. the API extractions graph with specific totals per day)
- Configs require attention 

**Quality score**

Sensible calculates the quality score for each extraction as follows:

`quality score` = (`non-null fields extracted` - `validation penalities` )/ `total fields defined in config` 

Where:

- `validation penalties` =  the sum of validation errors and warnings. Errors are 1 penalty point and warnings are 0.5 points.

- Sensible excludes fields listed in the Suppress Output method when calculating this score.

For example, if an extraction A has the following properties:

- num fields defined in the configuration = 20

- num of non-null fields = 18
- num of fields with validation errors = 1
- num of fields with validation warnings = 4

Then its quality score is 75% : (20 - 2 - 1 - 2) / 20 = 0.75. 

This quality score is a normalized [classification score](doc:fingerprint). 

