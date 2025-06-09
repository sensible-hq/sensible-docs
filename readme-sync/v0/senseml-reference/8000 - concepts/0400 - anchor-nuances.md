---
title: "Anchor variables"
hidden: false
---

**Note:** If you're familiar with Sensible, this detailed topic is for you. If you're new to Sensible, see [anchor](doc:anchor).

This topic covers defining and reusing anchor definitions for concise syntax

## Reuse anchor variables

You can reuse anchors by defining them and then referring to them as variables. For example, reuse a complex anchor for concise syntax:

```json
  "fields": [
    {
      /* declare the named anchor variable for later reuse */
      "type": "anchorDefinition",
      "name": "liability_workers_comp",
      "anchor": {
        "start":{"text":"Certificate of liability insurance","type":"equals"},
        "match":{"text":"workers compensation","type":"equals"},
        "end":{"type":"equals","text":"the acord name and logo are registered marks of acord"}
      }
    },
    {
      /* extract text from a box 1.15" to the right of the named anchor  */
      "id": "subrogation_waived",
      "method": {
        "id": "box",
        "offsetX": 1.15,
        "position": "right"
      },
      "anchor": {
        "ref": "liability_workers_comp"
      }
    },
    {
      /* extract text from a box 0.07" to the left of the named anchor  */
      "id": "insurer_letter",
      "method": {
        "id": "box",
        "offsetX": -0.07,
        "position": "left"
      },
      "anchor": {
        "ref": "liability_workers_comp"
      }
    },
```

You can define named anchors in a [Conditional](doc:conditional) method and refer to them in subsequent fields:

```json
{
  "fields": [
    {
      /* is the form in English or Spanish? */
      "id": "language",
      "anchor": "Customer language spoken: ",
      "method": {
        "id": "label",
        "position": "right"
      }
    },
    {
      /* if the form is in English ...  */  
      "method": {"id": "conditional",
      "condition": {"==": [{"var": "language.value"}, "english"]},
      "fieldsOnPass": [
    {
      /* declare the named anchor in English  */
      "type": "anchorDefinition",
      "name": "customer_id_anchor",
      "anchor": "customer ID number"
    },
    ], "fieldsOnFail": [{
      /* otherwise declare it in Spanish */  
      "type": "anchorDefinition",
      "name": "customer_id_anchor",
      "anchor": "identificación del cliente"
    }]}},
    {
      "id": "customer_id",
      "anchor": {
        /* use the named anchor to extract the customer ID in either language  */
        "ref": "customer_id_anchor"
      },
      "method": {
        "id": "label",
        "position": "right"
      }
    }
  ]
}
```

