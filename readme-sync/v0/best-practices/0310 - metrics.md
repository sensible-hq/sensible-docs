---
title: "Monitoring extractions"
hidden: false
---

In the Sensible dashboard, you can view the following metrics about your extractions in real time:

- [Extraction coverage](doc:metrics#extraction-coverage)
- [Most-used configurations](doc:metrics#most-used-configurations)
- [Documents extracted](doc:metrics#documents-extracted)

Extraction coverage
---

Extraction coverage measures how fully an extraction captures your target data from the document. For example, a coverage score of 70% for an extraction with no validation errors means that 30% of output fields are null. A low percentage can indicate a poor-quality extraction. Or, it can indicate that your documents contain sparse data. For example, if you define many target fields to extract from a supplemental insurance form, but applicants leave most of the questions blank, then the form's expected average extraction coverage is much less than 100%.

Since coverage success criteria can vary by document type, you can set your own ranges for each document type in the Sensible app. To set ranges for coverage for past extractions, click **Dashboard** and scroll to the **Extraction coverage** section. In the section, you can filter by:

- extraction coverage range
- extraction ID
- date range
- document type
- extraction batch

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_coverage.png)

In the preceding screenshot, 0 out of 16 extractions that used the `wells_fargo_savings` configuration in the `bank_statements` document type in the past 7 days scored in the coverage range of 60% -100%.

To determine your own coverage criteria, examine your past extractions. For example, if home inspectors typically report about 60 out of your 100 target data points, you can set a range of 60%-100% for your `home_inspection_report` document type to assess extraction success. In contrast, if you find that drivers licenses typically contain all your target data points, you can set a range of 95%-100% or even 100%-100% to assess extraction success for the `drivers_license` document type.

To view an individual extraction's coverage score, click **Dashboard** and scroll to the **Recent** section:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_coverage_1.png)

In the preceding screenshot, the `Sept 25, 2023 7:30 PM` extraction has a coverage score of `61.1%`.

 For more information about how Sensible calculates coverage scores, see [Coverage](doc:coverage).

## Most-used configurations 

To view which configurations were used for past extractions, click **Dashboard** and scroll to the **Most used** section:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_used_1.png)

In the preceding screenshot, the `1040_2018`  configuration was used for 54.7% of extractions in the last 30 days in the `tax_form` document type. If you adjust the filter to include both bank statements and tax forms, you see that it was used for 33% of all extractions across the selected document types:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_used_2.png)


## Documents extracted
To view the number of past extractions you've run by document type, click **Dashboard** and scroll to the **Document extracted** section. You can filter by date range, document types, and extraction coverage:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_count.png)











