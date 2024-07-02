---
title: "Reviewing extractions"
hidden: false
---

You can configure rules to flag extractions for manual review and correction. Base your rules on [validations](doc:validate-extractions) and [extraction coverage](doc:metrics). Use the Sensible app's **Human review** tab to manually correct the extracted fields, then approve or reject the extraction.

In a document type, in the **Human Review** tab, you can set the criteria for Sensible to flag an extraction for manual review:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_1.png) 

You can enable human review for all documents in a type, or you can set criteria to trigger review. Criteria include:

- [Extraction converage](doc:metrics)

- [Validation](doc:validate-extractions) errors and warnings, if configured. You can select all errors, all warnings, or individual validations. 

  

After you run extractions in the document type, the **Human review** tab displays the document types that contain extractions flagged for review:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_2.png) 


Click a document type to review the flagged extractions:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_3.png) 

You can click a field's value to:

- view the full field value for tables, sections, and other complex fields
- edit the field's value
- view the field's source location highlighted in the document

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_4.png)

You can click the checkmark icon next to each field to mark it approved. When you're done editing field values and approving individual fields, click **Approve Extraction** to remove it from the extractions flagged for review.

You can filter past extractions by review status using the following options:

- in the **Extraction history** tab, use the **Review Status** criterium
- in the Sensible API, use the [List extractions](reference:list-extractions) endpoint with the `review_statuses` parameter.