---
title: "Sections"
hidden: true
---

Extracts data from a document that contains complex or repeated elements ("sections"). 

Sensible returns an array of objects corresponding to the sections. The following image shows an example of a document containing repeated "claims" sections:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_1.png)

For the preceding example, you can configure Sensible to return a `unprocessed_claims` array, where each object in the array contains a `claim_number`, `claim_date`, `claimant_last_name`, etc. 

Parameters
====


| key                   | value                                                  | description                                                  |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)     | string                                                 | identifies a collection of sections to extract in the document area defined by the Range parameter. You can specify multiple sections, and you can nest sections inside of other sections. |
| range  (**required**) | object                                                 | Specifies to search for a collection of repeated sections in a range, as well as ranges within each section. The collection of sections can span nonrepeating text that does not form a part of a section.  For example,  in the preceding image, an "unprocessed_claims" collection of sections could span multiple month headings. Contains these parameters:<br/><br/>**anchor** (**required**)-an [Anchor](doc:anchor) or string object that defines the start of the section and optionally the end.<br/> For the Match parameter, specify the first line in each repeating element for this element. For example, in the preceding image, specify `"Claim number"`.  <br/> **stop** - a string or [Match](doc:match) object or array of Match objects that defines  the end of the section. In the preceding image, for example, `"Claims totals"`.<br/>- the end of the repeating element within the section. For example, if you specify `"Date of claim"`, then each section would end either when it encounters the next section, or when it encounters the phrase "Date of claim", and so the section would ignore everything past the claimant's last name in each repeating element. <br/> If you leave this parameter unspecified, then the last repeating element in the section continues to the end of the document.<br/> |
| fields (**required**) | array of [Field objects](doc:field-query-object)       | The fields in each repeating element that you want to extract repeatedly as an array.  If the field anchor doesn't correspond to a repeating element, or if it matches to data that falls outside the Range parameter, the field returns null. For example, in the preceding image, you can extract `date_of_claim` and `phone_number` in a section, but you can *only* extract  `total_unprocessed_claims`  in the main fields array, not in a section. |
| sections              |                                                        | Specifies sections inside sections. Use this for complex sections that contain nested repeated elements. |
| computed_fields       | array of [Computed fields](doc:computed-field-methods) | Transform the output of the fields.                          |

Examples
====

The following example shows extracting fields repeatedly from a section containing a list of claims.

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
      "id": "unprocessed_by_month",
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
    }
  ],
  "sections": [
    {
      "id": "unprocessed_claims_sept_oct",
      "range": {
        "anchor": {
          "match": {
            "type": "startsWith",
            "text": "Claim number",
            "isCaseSensitive": true
          },
          "end": {
            "type": "startsWith",
            "text": "November",
            "isCaseSensitive": true
          }
        },
        "stop": {
          "type": "includes",
          "text": "unprocessed claims:",
          "isCaseSensitive": true
        }
      },
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
        }
      ]
    }
  ]
}
```

**PDF**

The following image shows the data extracted by this config for the following example PDF:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_2.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/sections.pdf) |
| ------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "total_unprocessed_claims": {
    "source": "5",
    "value": 5,
    "type": "number"
  },
  "unprocessed_by_month": [
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
  "unprocessed_claims_sept_oct": [
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
      }
    },
    {
      "claim_number": {
        "source": "9876543211",
        "value": 9876543211,
        "type": "number"
      },
      "phone_number": null
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
      }
    }
  ]
}
```

