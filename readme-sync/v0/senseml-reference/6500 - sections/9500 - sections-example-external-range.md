---
title: "Advanced: External anchors for sections"
hidden: false
---

The following example shows extracting repeated fields from a section group, when each section lacks anchoring text. To overcome this limitation, the section group specifies an external range, for anchoring on text external to the sections. Since the external range is vertically aligned with the content in each section, the example uses the [Intersection](doc:intersection) method to specify text in the external range as vertical anchors.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_external_range_2.png)

**Config**

```json
{
  "fields": [],
  /* define section group containing subset of document's claims */
  "sections": [
    {
      "id": "unprocessed_claims_sections",
      /* each section contains unlabeled information.
         the labels are at the beginning of the document
         use the External Range parameter to make these labels
         accessible as vertical anchors inside the sections */
      "range": {
        "externalRange": {
          "start": "Claim contents",
          "end": "unprocessed claims"
        },
        /* include 'claim no' heading above section start */
        "offsetY": -0.5,
        "anchor": {
          /* start looking for claims after first instance of "unprocessed claims" */
          "start": {
            "text": "unprocessed claims",
            "type": "includes",
            "isCaseSensitive": true
          },
          /* each claim section starts with a 9-digit claim number */
          "match": {
            "type": "regex",
            "pattern": "^\\d{10}$"
          },
          /* stop looking for claims before "total" claims */
          "end": {
            "type": "startsWith",
            "text": "total claims",
            "isCaseSensitive": true
          }
        },
        /* each claim ends below "unprocessed claims:". 
           Optional, prevents last section in group 
           from extending to end of document */
        "stop": {
          "type": "includes",
          "text": "unprocessed claims:",
          "isCaseSensitive": true
        }
      },
      /* return each claim as object containing claim # 
      and phone # fields */
      "fields": [
        {
          /* for each field,
             find the intersection of "Claim [number]"
             and on the relevant text in the 
             claim contents external range,
             then adjust width,height, and offsets
            till the green box is centered
             on the target data  */
          "id": "claim_number",
          "type": "number",
          "anchor": {
            "match": {
              "type": "regex",
              "pattern": "Claim \\d",
              "flags": "i"
            }
          },
          "method": {
            "id": "intersection",
            "verticalAnchor": "Claim number",
            "width": 1.5,
            "height": 0.5,
            "offsetY": 0.35
          }
        },
        {
          "id": "claim_date",
          "type": "date",
          "anchor": {
            "match": {
              "type": "regex",
              "pattern": "Claim \\d",
              "flags": "i"
            }
          },
          "method": {
            "id": "intersection",
            "verticalAnchor": "Date of claim",
            "width": 1.5,
            "height": 0.5,
            "offsetY": 0.9
          }
        },
        {
          "id": "phone_number",
          "anchor": {
            "match": {
              "type": "regex",
              "pattern": "Claim \\d",
              "flags": "i"
            }
          },
          "method": {
            "id": "intersection",
            "verticalAnchor": "Phone number",
            "width": 1.5,
            "height": 0.5,
            "offsetY": 0.7
          }
        },
        /* to illustrate section range, output all text in this section */
        {
          "id": "_everything_in_this_section",
          "method": {
            "id": "documentRange",
            "includeAnchor": true
          },
          "anchor": {
            "match": {
              "type": "first"
            }
          }
        }
      ]
    }
  ]
}
```

**Example document**

The following image shows the data extracted by this config for the following example document.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_external_range.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/sections_external_range.pdf) |
| ------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "unprocessed_claims_sections": [
    {
      "claim_number": {
        "source": "1223456789",
        "value": 1223456789,
        "type": "number"
      },
      "claim_date": {
        "source": "09/15/2021",
        "value": "2021-09-15T00:00:00.000Z",
        "type": "date"
      },
      "phone_number": {
        "type": "string",
        "value": "512 409 8765"
      },
      "_everything_in_this_section": {
        "type": "string",
        "value": "Claim contents Claim number Claimant last name Date of claim Phone number Claim 1 1223456789 Diaz 09/15/2021 512 409 8765"
      }
    },
    {
      "claim_number": {
        "source": "9876543211",
        "value": 9876543211,
        "type": "number"
      },
      "claim_date": {
        "source": "09/08/2021",
        "value": "2021-09-08T00:00:00.000Z",
        "type": "date"
      },
      "phone_number": {
        "type": "string",
        "value": "Badawi"
      },
      "_everything_in_this_section": {
        "type": "string",
        "value": "Claim contents Claim number Claimant last name Date of claim Phone number Claim 2 9876543211 Badawi 09/08/2021 Sept unprocessed claims: 2"
      }
    },
    {
      "claim_number": {
        "source": "6785439210",
        "value": 6785439210,
        "type": "number"
      },
      "claim_date": {
        "source": "10/03/2021",
        "value": "2021-10-03T00:00:00.000Z",
        "type": "date"
      },
      "phone_number": {
        "type": "string",
        "value": "505 238 8765"
      },
      "_everything_in_this_section": {
        "type": "string",
        "value": "Claim contents Claim number Claimant last name Date of claim Phone number Claim 1 6785439210 Levy 10/03/2021 505 238 8765 Oct unprocessed claims: 1"
      }
    }
  ]
}
```
