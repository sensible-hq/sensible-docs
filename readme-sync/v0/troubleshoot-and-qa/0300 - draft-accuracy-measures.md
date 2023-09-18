---
title: "dashboard"
hidden: true
---



TODO - start adding screenshots and explaining (+ understanding) dashboard

Quality statistics (separate topic?)
---

You can get individual and aggregate statistics about the quality of extractions.

**Quality buckets**

You can filter extractions by the following 12 “buckets” of aggregated extraction quality scores.  For example, the following image shows that 15 document extractions scored 100% quality scores in a given time range for a given config, and 7 fell into the lowest 0-10% quality bucket.

![image-20230802135848603](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20230802135848603.png)

THIS STUFF IS ALREADY IN THE API:

- [0, 10)

- [10, 20)

- [20, 30)

- [30, 40)

- [40, 50)

- [50, 60)

- [60, 70)

- [70, 80)

- [80, 90)

- [90, 95)

- [95, 100)

- [100] 

  `[` denotes inclusive and `)` denotes exclusive

For example, a document extraction with a quality score of .85, or 85%, falls into the  [80, 90) bucket.

You can view scores in the Sensible app or through the Sensible API. 

**Quality score**

Sensible calculates the quality score for each extraction as follows:

`quality score` = (`non-null fields extracted` - `validation penalities` ) / `total fields defined in config` 

Where:

- `validation penalties` =  sum of validation errors and warnings. Errors are 1 penalty point and warnings are 0.5 points.

For example, if an extraction A has the following properties:

- num fields defined in the configuration = 20

- num of non-null fields = 18
- num of fields with validation errors = 1
- num of fields with validation warnings = 4

Then its quality score is 75% : (18 - 1 - 2) / 20 = 0.75. 

**Notes**

- Sensible excludes fields listed in the Suppress Output method when calculating the quality score.
- The overall quality score for a portfolio document is the average score of all subdocument outputs. The Sensible API returns a `quality_score` for each subdocument as well. TODO check accuracy.

