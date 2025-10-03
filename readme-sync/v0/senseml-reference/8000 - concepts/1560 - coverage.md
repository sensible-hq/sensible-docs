---
title: "Extraction coverage"
hidden: false
---

Extraction coverage measures how fully an extraction captures your target data from the document.  For example, a coverage score of 70% for an extraction with no validation errors means that 30% of output fields are null. A low percentage can indicate a poor-quality extraction. Or, it can indicate that your documents contain sparse data. For example, if you define many target fields to extract from a supplemental insurance form, but applicants leave most of the questions blank, then the form's expected average extraction coverage is much less than 100%.

## Human review criteria

Since coverage success criteria can vary by document type, you can trigger [human review](doc:human-review) based on different coverage ranges for each document type in the Sensible app.

To determine your own coverage criteria, examine your past extractions. For example, if home inspectors typically report about 60 out of your 100 target data points, you can set a range of 60%-100% for your `home_inspection_report` document type to assess extraction success. In contrast, if you find that drivers licenses typically contain all your target data points, you can set a range of 95%-100% or even 100%-100% to assess extraction success for the `drivers_license` document type.

## Coverage formula

Sensible calculates the coverage for each extraction as follows:

`coverage` = (`non-null fields extracted` - `validation penalties` )  ÷  (`total fields extracted`) 

Where:

- `validation penalties` =  sum of [validation](doc:validate-extractions) errors and warnings. Errors are 1 penalty point and warnings are 0.5 points.

For example, if an extraction has the following properties:

- num of non-null fields extracted = 18
- num fields extracted= 20
- num of fields with validation errors = 1
- num of fields with validation warnings = 4

Then its coverage is 75% : (18 - 1 - 2) / 20 = 0.75. 

To view an individual extraction's coverage, click **Dashboard** and scroll to the **Recent** section:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_coverage_1.png)

In the preceding screenshot, get a coverage breakdown by viewing the extraction. You can view the extraction by clicking the extraction date in the **Recent extractions** column or downloading the Excel file.

For example, in the preceding screenshot, you can click  `Sept 25, 2023, 7:30 PM`  in the **Created**  column to count the extracted fields in the SenseML editor and find that the score of `61.1%` means that 33 of 54 total fields output were valid and non-null. Or, you can retrieve the information from the [Sensible API](ref:retrieving-results) or SDK. The following code sample shows an except from an API response with the `validation_summary` used to calculate the `coverage` for the Sept 25 extraction:

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

- Sensible excludes fields listed in the Suppress Output method when calculating the coverage.
- Sensible includes fields output in [sections](doc:sections) when calculating the coverage.
- The overall coverage for a portfolio document is the weighted average of all subdocument coverages.