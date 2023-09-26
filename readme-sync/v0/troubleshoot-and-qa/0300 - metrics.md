---
title: "Metrics"
hidden: true
---

In the Sensible dashboard, you can view the following metrics about your past extractions:

- Extraction coverage
- Most-used configurations
- Extractions count



Extraction coverage
---

Extraction coverage is a score that measures how fully an extraction captured all the data in the document. For example, a coverage score of 70% for an extraction with no validation errors means that 30% of fields were null. A low percentage can indicate a poor-quality extraction, or it can indicate that a document type is sparsely filled out. For example, supplemental forms in insurance applications or supplemental schedules in tax forms can return many nulls, since these forms are often left blank.

**View extraction coverage**

To view an individual extraction's coverage score, click **Dashboard** and scroll to the **Recent** section:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_coverage_1_.png)

To view aggregate coverage for a configuration's past extractions, click **Dashboard** and scroll to the **Extraction coverage** section:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_coverage_.png)



 through the Sensible API's extraction endpoints, or get daily coverage using the [statistics](ref:statistics) endpoint.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_count.png)

**Coverage calculation**

 Sensible calculates the coverage score for each extraction as follows:

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







![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_coverage.png)



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_coverage.png)





TODO - start adding screenshots and explaining (+ understanding) dashboard

Quality statistics (separate topic?)
---

You can get individual and aggregate statistics about the quality of extractions.

**Quality buckets**

You can filter extractions by the following 12 “buckets” of aggregated extraction quality scores.  For example, the following image shows that 15 document extractions scored 100% quality scores in a given time range for a given config, and 7 fell into the lowest 0-10% quality bucket.



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

