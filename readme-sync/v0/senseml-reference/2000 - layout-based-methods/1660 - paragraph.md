---
title: "Paragraph"
hidden: false
---
Extracts paragraphs in various layouts, including paragraphs in columns and paragraphs that span pages. 

[**Parameters**](doc:document-range#parameters)
[**Examples**](doc:document-range#examples)
[**Notes**](doc:document-range#notes)

Parameters
====

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key               | value       | description                                                  |
| ----------------- | ----------- | ------------------------------------------------------------ |
| id (**required**) | `paragraph` | This method uses document layout, including columns, to detect paragraphs. To format the extracted paragraph with newlines, use in combination with the [Paragraph](doc:types#paragraph) type. |


Examples
====



**Config**

```json
{
  "fields": [
    {
      "id": "repair_completion",
      "anchor": {
        "match": {
          "text": "may not repair",
          "type": "includes"
        }
      },
      "method": {
        "id": "paragraph"
      }
    },
    {
      "id": "lead_warning_spans_pages",
      "type": "paragraph",
      "anchor": {
        "match": [
          {
            "text": "lead warning statement",
            "type": "startsWith"
          }
        ]
      },
      "method": {
        "id": "paragraph"
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/paragraph.png)

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/paragraph_1.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/paragraph.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "repair_completion": {
    "type": "string",
    "value": "1. Tenant may not repair or cause to be repaired any condition, regardless of the cause, without Landlord's permission. All decisions regarding repairs, including the completion of any repair, whether to repair or replace the item, and the selection of contractors, will be at Landlord's sole discretion."
  },
  "lead_warning_spans_pages": {
    "type": "string",
    "value": "LEAD WARNING STATEMENT: Housing built before 1978 may contain lead-based paint. Lead from paint, paint chips, and dust can pose health hazards if not managed properly. Lead exposure is especially harmful to young children and pregnant women. Before renting a home built before 1978, landlords must disclose the presence of any known lead- based paint and/or lead-based paint hazards in the dwelling. Tenants must also receive a federally approved pamphlet on lead poisoning prevention."
  }
}
```



