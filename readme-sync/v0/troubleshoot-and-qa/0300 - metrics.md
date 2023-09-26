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

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_coverage_1.png)

In the preceding screenshot, get a score breakdown by viewing the extraction. You can view the extraction by:

- clicking the extraction date in the **Recent extractions** column
- downloading the Excel file
- retrieving the extraction details by its ID using the [Sensible API](ref:retrieving-results). 

For example, in the preceding screenshot, you can click  `Sept 25, 2023, 7:30 PM`  to count the extracted fields in the SenseML editor and find that the score of `61.1%` means that 33 of 54 total fields output were valid and non-null.

**View aggregate extraction coverage**

To view aggregate coverage for a configuration's past extractions, click **Dashboard** and scroll to the **Extraction coverage** section:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_coverage.png)

In the preceding screenshot, the `wells_fargo_savings` configuration had 0 out of 16 extractions in the past 7 days that scored in the coverage range 60% -100%.

 You can also view see daily coverage scores using the Sensible API's [statistics](ref:statistics) endpoint.

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

To view field counts and validation penalties for an extraction, click the extraction date in the **Created** column in the **Recent extractions** section in the Sensible dashboard.

**Notes**

- Sensible excludes fields listed in the Suppress Output method when calculating the score.
- Sensible includes fields output in [sections](doc:sections) when calculating the score.
- The overall score for a portfolio document is the average score of all subdocument outputs.



## Most-used 



TODO 


## Past extractions
TODO

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_count.png)









![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_count.png)







