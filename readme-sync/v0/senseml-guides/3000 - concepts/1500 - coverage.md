---
title: "Extraction coverage"
hidden: true
---

**Note:** If you're familiar with coverage scores, this detailed topic is for you. If you're new to Sensible, see [metrics](doc:metrics).

Extraction coverage is a score that measures how fully an extraction captured all the data in the document. Sensible calculates the coverage score for each extraction as follows:

`coverage score` = (`non-null fields extracted` - `validation penalties` )  ÷  (`total fields extracted`) 

Where:

- `validation penalties` =  sum of [validation](doc:validate-extractions) errors and warnings. Errors are 1 penalty point and warnings are 0.5 points.

For example, if an extraction has the following properties:

- num of non-null fields extracted = 18
- num fields extracted= 20
- num of fields with validation errors = 1
- num of fields with validation warnings = 4

Then its coverage score is 75% : (18 - 1 - 2) / 20 = 0.75. 

To view an individual extraction's coverage score, click **Dashboard** and scroll to the **Recent** section:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_coverage_1.png)

In the preceding screenshot, get a score breakdown by viewing the extraction. You can view the extraction by clicking the extraction date in the **Recent extractions** column or downloading the Excel file.

For example, in the preceding screenshot, you can click  `Sept 25, 2023, 7:30 PM`  in the **Created**  column to count the extracted fields in the SenseML editor and find that the score of `61.1%` means that 33 of 54 total fields output were valid and non-null. Or, you can retrieve the information from the [Sensible API](ref:retrieving-results). The following code sample shows an except from an API response with the `validation_summary` used to calculate the `coverage` for the Sept 25 extraction:

```json
{
	"id": "efe99816-0e5b-11eb-b720-295a6fba723e", // extraction ID
	"validation_summary": {
		"fields": 54, //total fields
		"fields_present": 33, //non-null fields
		"errors": 0, //validation errors and warnings
		"warnings": 0,
		"skipped": 0
	},
	"coverage": 0.611 // extraction coverage score calculated from validation_summary
```

**Notes**

- Sensible excludes fields listed in the Suppress Output method when calculating the coverage score.
- Sensible includes fields output in [sections](doc:sections) when calculating the coverage score.
- The overall coverage score for a portfolio document is the average score of all subdocument outputs.