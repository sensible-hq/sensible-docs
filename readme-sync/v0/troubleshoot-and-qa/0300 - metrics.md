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

Since coverage success criteria can vary by document type, you can set your own ranges for each document type in the Sensible app. To set ranges for coverage for past extractions, click **Dashboard** and scroll to the **Extraction coverage** section. Then configure date range, document type, and coverage filters:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_coverage.png)

In the preceding screenshot, 0 out of 16 extractions that used the `wells_fargo_savings` configuration in the `bank_statements` document type in the past 7 days scored in the coverage range 60% -100%.

By examining past extractions by document type, you can determine your own coverage ranges for each document type. For example, if you know that home inspectors typically fill out 60 to 70 out of 100 of your target fields in their reports, you'd set a range of 60%-100% for your `home_inspection_report` document type to assess extraction success. In contrast, if you know that drivers licenses typically have all your target fields filled out, you'd set a range of 95%-100% or even 100%-100% to assess extraction success for the `drivers_license` document type.

 You can also get daily coverage scores using the Sensible API's [statistics](ref:statistics) endpoint.

For more information about how Sensible calculates coverage scores, see the following section.

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

To view an individual extraction's coverage score, click **Dashboard** and scroll to the **Recent** section:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_coverage_1.png)

In the preceding screenshot, get a score breakdown by viewing the extraction. You can view the extraction by clicking the extraction date in the **Recent extractions** column or downloading the Excel file.

For example, in the preceding screenshot, you can click  `Sept 25, 2023, 7:30 PM`  in the **Created**  column to count the extracted fields in the SenseML editor and find that the score of `61.1%` means that 33 of 54 total fields output were valid and non-null. Or, you can retrieve the information from the [Sensible API](ref:retrieving-results). The following code sample shows an except from an API response with the `validation_summary` used to calculate the `coverage`:

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

- Sensible excludes fields listed in the Suppress Output method when calculating the score.
- Sensible includes fields output in [sections](doc:sections) when calculating the score.
- The overall score for a portfolio document is the average score of all subdocument outputs.

## Most-used 

To view which configurations were used for past extractions, click **Dashboard** and scroll to the **Most used** section:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_used_1.png)

In the preceding screenshot, the `1040_2018`  configuration was used for 54.7% of extractions in the last 30 days in the `tax_form` document type. If you adjust the filter to include bank statements as well as tax forms, you see that it was used for 33% of all extractions across the selected document types:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_used_2.png)


## Past extractions
TODO

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_count.png)











