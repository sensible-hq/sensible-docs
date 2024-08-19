---
title: "Reviewing extractions"
hidden: false
---

If extractions contain errors, for example as the result of hard-to-read handwriting, you can flag extractions for manual correction by a human reviewer. Flag extractions automatically at scale in production by configuring rules based on [validations](doc:validate-extractions) and [extraction coverage](doc:coverage). Use the Sensible app's **Human review** tab to manually correct the extracted fields, then approve or reject the extraction.

In a document type, in the **Human Review** tab, set the criteria for Sensible to flag an extraction for manual review:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_1.png) 

Enable human review for all documents in a type, or set criteria to trigger review. Criteria include:

- [Extraction coverage](doc:coverage)

- [Validation](doc:validate-extractions) errors and warnings, if configured. Select all errors, all warnings, or individual validations. 

  

After you run extractions in the document type, the **Human review** tab displays the document types that contain extractions flagged for review:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_2.png) 


Click a document type to review the flagged extractions:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_3.png) 

Click a field's value to:

- view the field's full value for tables, sections, and other complex fields
- edit the field's value
- view the field's source location highlighted in the document

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_4.png)

Click the checkmark icon next to each field to mark it approved. When you're done editing field values and approving individual fields, click **Approve Extraction** or **Reject Extraction** to remove it from the extractions flagged for review.

Filter past extractions by review status using the following options:

- in the **Extraction history** tab, use the **Review Status** criterion
- in the Sensible API, use the [List extractions](reference:list-extractions) endpoint with the `review_statuses` parameter.