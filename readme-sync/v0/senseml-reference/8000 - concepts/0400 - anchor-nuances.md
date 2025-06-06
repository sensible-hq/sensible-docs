---
title: "Anchor nuances"
hidden: false
---

**Note:** If you're familiar with Sensible, this detailed topic is for you. If you're new to Sensible, see [anchor](doc:anchor).

This topic covers advanced anchor concepts:

- Define and reuse anchor definitions for concise syntax
- Filter anchors by the field's method

For related information about match use in anchors, see [Match arrays](doc:match-arrays).

## Reuse anchors

You can reuse anchors by defining them and then referring to them. For example, reuse a complex anchor for concise syntax:

```json
  "fields": [
    {
      /* declare the anchor definition for later reuse */
      "type": "anchorDefinition",
      "name": "liability_workers_comp",
      "anchor": {
        "start":{"text":"Certificate of liability insurance","type":"equals"},
        "match":{"text":"workers compensation","type":"equals"},
        "end":{"type":"equals","text":"the acord name and logo are registered marks of acord"}
      }
    },
    {
      /* extract text from a box 1.15" to the right of the reused anchor  */
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
      /* extract text from a box 0.07" to the left of the reused anchor  */
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
      /* the value for the customer ID anchor is English */
      "type": "anchorDefinition",
      "name": "customer_id_anchor",
      "anchor": "customer ID number"
    },
    ], "fieldsOnFail": [{
      /* otherwise it's Spanish */  
      "type": "anchorDefinition",
      "name": "customer_id_anchor",
      "anchor": "identificación del cliente"
    }]}},
    {
      "id": "customer_id",
      "anchor": {
        /* refer to the anchor to find the customer ID in either language  */
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

Filter methods by anchors
-----

In addition to the match conditions you specify (such as `isCaseSensitive`), the method type influences whether text qualifies as an anchor.

For example, if you specify the Label method, Sensible anchors on text that is a good label candidate. Sensible disqualifies any line as a label that is too far away from other lines, even if it otherwise meets the conditions in the anchor's parameters.

The following example shows two anchors qualified by the Label method:

**Example Config**

```json
{
  "fields": [
    {
      "id": "anchors_candidates_filtered_by_method",
      "anchor": "python",
      "match": "first",
      "method": {
        "id": "label",
        "position": "right"
      }
    }
  ]
}
```

**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/ui_filtered_anchor.png)


| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/row_column.pdf) |
| ----------- | ------------------------------------------------------------ |

**Example Output**

The example config returns null, but returns data if you specify the Row method instead.

**Example Notes**

In this example, Sensible filters out the anchor candidates (surrounded by light yellow boxes) because they do not meet the Label method's proximity requirements. The strings "python" are far enough away from other lines that you should use the Row method here instead. 
