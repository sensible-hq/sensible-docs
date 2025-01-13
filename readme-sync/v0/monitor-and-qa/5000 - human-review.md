---
title: "Human review"
hidden: false
---

As a reviewer, you can use the Sensible app's **Human review** tab to manually correct extracted document data that's been automatically flagged for review, then approve or reject the extraction. Once you approve or reject, you can't change the status again. 

Click the **Human review** tab to display the document types that contain extractions flagged for review:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_2.png) 


Click a document type to review the flagged extractions:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_3.png) 

View the **Validations** in the left pane to check which fields are failing the review criteria.  For example, in the preceding image, the extracted `year` field is null when it should be 2018, and the `year is not null` validation failed as result.

Click a field's value to:

- view the field's full value for tables, sections, and other complex fields
- edit the field's value
- view the field's source location highlighted in the document

For example, in the following image, the reviewer corrected the `year` field's value and marked it as reviewed by clicking the checkmark to the right of the field: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_4.png)

 When you're done editing and reviewing field values, click **Approve Extraction** or **Reject Extraction** to remove it from the extractions flagged for review.

