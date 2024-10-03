---
title: "Monitoring extraction metrics"
hidden: false
---

In the Sensible dashboard, you can view the following metrics about your extractions in real time:

- [Extraction coverage](doc:metrics#extraction-coverage)
- [Most-used configurations](doc:metrics#most-used-configurations)
- [Documents extracted](doc:metrics#documents-extracted)

For all metrics, you can filter by date range and environments (for example, production or development). If you don't specify an environment, Sensible shows metrics for all metrics by default.

## Documents extracted

To view the number of past extractions you've run by document type, click **Dashboard** and scroll to the **Document extracted** section. In the section, you can filter by:

-  document types
- extraction coverage

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_count.png)

Extraction coverage
---

Extraction coverage measures how fully an extraction captures your target data from the document.  For more information, see [Extraction coverage](doc:coverage).

In this section, you can filter by:

- document type
- extraction coverage percentage ranges

For example, the following screenshot shows filtering by coverage and document type:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_coverage.png)

In the preceding screenshot, 0 out of 16 extractions that used the `wells_fargo_savings` configuration in the `bank_statements` document type in the past 7 days scored in the coverage range of 60% -100%.

To view an individual extraction's coverage score, click **Dashboard** and scroll to the **Recent** section:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_coverage_1.png)

In the preceding screenshot, the `Sept 25, 2023 7:30 PM` extraction has a coverage score of `61.1%`.

## Most-used configurations 

To view which configurations were used for past extractions, click **Dashboard** and scroll to the **Most used** section:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_used_1.png)

In the preceding screenshot, the `1040_2018`  configuration was used for 54.7% of extractions in the last 30 days in the `tax_form` document type. If you adjust the filter to include both bank statements and tax forms, you see that it was used for 33% of all extractions across the selected document types:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/dashboard_used_2.png)

In this section, you can filter by:

- document type

## Recent extractions

To view recent configurations, click **Dashboard** and scroll to the **Recent extraction** section. In the section, you can filter by:

- document type
- configuration
- extraction [coverage](doc:coverage)
- extraction status
- [review](doc:human-review) status
- [batch](doc:quick-extraction#extract-from-multiple-files) ID









