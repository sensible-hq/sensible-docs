---
title: "Claims loss run example"
hidden: false
---

The following example shows extracting repeated fields from a section group containing a list of claims:

- It captures Sept and Oct claims by specifying  sections that start with "claim number" and  section group range that starts with "September" and ends with "November".
- From each section, it excludes intervening text that isn't part of a section but that does repeat (`monthly_number_unprocessed_claims`) using a Stop parameter. Instead, it captures this information outside of sections with  `"match:all"`.

**Config**

```json
{
  "fields": [
    {
      "id": "total_unprocessed_claims",
      "type": "number",
      "anchor": "total unprocessed claims",
      "method": {
        "id": "row"
      }
    },
    {
      /* get monthly claims totals 
      with match all (simpler alternative to sections) */
      "id": "monthly_total_unprocessed_claims",
      "match": "all",
      "anchor": {
        "match": {
          "type": "includes",
          "text": "unprocessed claims:",
          "isCaseSensitive": true
        },
        "end": {
          "text": "total claims",
          "type": "startsWith"
        }
      },
      "method": {
        "id": "row",
        "position": "right",
        "includeAnchor": true
      }
    },
    {
      /* define section group containing subset of document's claims */
      "id": "unprocessed_sept_oct_claims_sections",
      "type": "sections",
      "range": {
        "anchor": {
          /* start looking for claims after "September" */
          "start": {
            "text": "September",
            "type": "startsWith",
            "isCaseSensitive": true
          },
          /* each claim section starts with "claim number" */
          "match": {
            "type": "includes",
            "text": "claim number"
          },
          /* stop looking for claims before "November".
             Excludes November claims from output */
          "end": {
            "type": "startsWith",
            "text": "November",
            "isCaseSensitive": true
          }
        },
        /* each claim ends below "date of claim". 
           Optional, prevents last section in group 
           from extending to end of document */
        "stop": {
          "type": "includes",
          "text": "Date of claim",
          "isCaseSensitive": true
        }
      },
      /* return each claim as object containing claim # 
      and phone # fields */
      "fields": [
        {
          "id": "claim_number",
          "type": "number",
          "anchor": {
            "match": {
              "type": "startsWith",
              "text": "Claim number:",
              "isCaseSensitive": true
            }
          },
          "method": {
            "id": "label",
            "position": "right"
          }
        },
        {
          "id": "phone_number",
          "type": "phoneNumber",
          "anchor": {
            "match": {
              "type": "includes",
              "text": "Phone number",
              "isCaseSensitive": true
            }
          },
          "method": {
            "id": "row",
            "position": "right"
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

The following image shows the data extracted by this config for the following example document:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_2.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/sections.pdf) |
| ------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "total_unprocessed_claims": {
    "source": "5",
    "value": 5,
    "type": "number"
  },
  "monthly_total_unprocessed_claims": [
    {
      "type": "string",
      "value": "Sept unprocessed claims: 2"
    },
    {
      "type": "string",
      "value": "Oct unprocessed claims: 1"
    },
    {
      "type": "string",
      "value": "Nov unprocessed claims: 2"
    }
  ],
  "unprocessed_sept_oct_claims_sections": [
    {
      "claim_number": {
        "source": "1223456789",
        "value": 1223456789,
        "type": "number"
      },
      "phone_number": {
        "type": "phoneNumber",
        "source": "512 409 8765",
        "value": "+15124098765"
      },
      "_everything_in_this_section": {
        "type": "string",
        "value": "Claim number: 1223456789 Claimant last name: Diaz Date of claim 09/15/2021 Phone number 512 409 8765"
      }
    },
    {
      "claim_number": {
        "source": "9876543211",
        "value": 9876543211,
        "type": "number"
      },
      "phone_number": null,
      "_everything_in_this_section": {
        "type": "string",
        "value": "Claim number: 9876543211 Claimant last name: Badawi Date of claim 09/08/2021 Phone number"
      }
    },
    {
      "claim_number": {
        "source": "6785439210",
        "value": 6785439210,
        "type": "number"
      },
      "phone_number": {
        "type": "phoneNumber",
        "source": "505 238 8765",
        "value": "+15052388765"
      },
      "_everything_in_this_section": {
        "type": "string",
        "value": "Claim number: 6785439210 Claimant last name: Levy Date of claim 10/03/2021 Phone number 505 238 8765"
      }
    }
  ]
}
```
