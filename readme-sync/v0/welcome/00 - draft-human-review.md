---
title: "Human review"
hidden: true
---

You can configure rules to trigger review for extractions that fail validations or have missing null data. Using our review UI in the Sensible app to manually correct the extraction then approve or reject it.

In a document type, in the **Human Review** tab, you can set the criteria for Sensible to flag an extraction for manual review:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_1.png) 

You can enable human review for all documents in a type, or you can set criteria to trigger review. Criteria include:

- Extraction converage (2do link to /metrics)

- Validation errors and warnings, if configured. You can select all errors, all warnings, or choose which ones you want on an individual basis. 

  

After you run extractions in the document type, the **Human review** tab displays the document types that contain extractions flagged for review:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_2.png) 



The flagged extractions are organized by document type. Click a document type to review the flagged extractions:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_3.png) 

You can click a field's value to view its source location highlighted in the document and to edit the value:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/human_review_4.png)

You can click the checkmark icon next to each field to mark it approved. When you're done editing field values, click **Approve Extraction** to remove it from the extractions flagged for review.

You can filter by review status for extractions in the **Extraction history** tab using the **Review Status** criterium, and in the Sensible API by the reference/list-extractions by the `review_status` parameter.