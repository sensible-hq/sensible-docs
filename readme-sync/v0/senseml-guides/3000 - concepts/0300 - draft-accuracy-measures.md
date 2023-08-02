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

- **Quality statistics:** Sensible scores each extraction using the number of fields extracted versus those defined in the config and other information. It also aggregates statistics about how configs are performing and how much they're used. 

Quality statistics (separate topic?)
---

You can get individual and aggregate statistics about the quality of extractions.

You can query the following 12 “buckets” of aggregated extraction quality scores:

![image-20230802135848603](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20230802135848603.png)



Sensible calculates the percentage score for each extraction as follows:

`(num of fields - (num of null fields) - (num of fields with validation error) - (0.5 * num of fields with validation warning)) / (num of fields)`

For example, if an extraction A has the following properties:

- num fields defined in the configuration = 20

- num of null fields = 2
- num of fields with validation errors = 1.
- num of fields with validation warnings = 4

Then its quality score is 75%: (20 - 2 - 1 - 2) / 20 = 0.75

