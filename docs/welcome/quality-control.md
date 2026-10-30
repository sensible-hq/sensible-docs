---
title: Quality control
excerpt: Learn about quality control options for extracted document data, including
  custom validation, real-time monitoring dashboards, and human review workflows.
deprecated: false
hidden: false
metadata:
  title: ''
  description: Learn about quality control options for extracted document data, including
    custom validation, real-time monitoring dashboards, and human review workflows.
  robots: index
next:
  description: ''
---
Sensible provides the following quality-control options for extracted fields:

| Option                       | Topic                                              | Notes |
| ---------------------------- | -------------------------------------------------- | ----- |
| Custom validation logic      | [Validating extractions](doc:validate-extractions) | Throw errors and warnings for fields based on your custom rules. For example, use a regular expression to throw a `zip code is invalid` error for the field `customer_zip_code`. |
| Monitor in real time         | [Monitoring extraction metrics](doc:metrics)       | In the Sensible app, view aggregate performance summaries, config success, usage per document type, and historic performance for all production deployments. |
| Manual review and correction | [Human review](doc:human-review)                   | Human review lets you set criteria, based on metrics and validations, for flagging extractions. Reviewers correct, approve, or reject flagged extractions in the Sensible app. |
