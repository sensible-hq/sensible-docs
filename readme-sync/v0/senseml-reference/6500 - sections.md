---
title: "Sections"
hidden: false
---

Extracts data from a document that contains complex or repeated elements ("sections").  In effect, a "section" defines a repeating document inside a document, with its own fields.

Sensible returns an array of objects corresponding to the sections. The following image shows an example of a document containing repeated "claims" sections:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_1.png)

For the preceding example, you can configure Sensible to return an `unprocessed_claims` array, where each object in the array contains a `claim_number`, `claim_date`, `claimant_last_name`, etc. 

Parameters
====


| key                   | value                                                  | description                                                  |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)     | string                                                 | Identifies a collection of sections to extract in the document area defined by the Range parameter. You can define an array of collections, and you can nest sections inside of other sections. |
| range  (**required**) | object                                                 | Specifies the range of both:<br/>- a collection of repeated sections in an area of the document <br/>- the start and end of each repeated section.<br/>The collection of sections can span nonrepeating text. For example,  in the preceding image, an "unprocessed_claims" collection of sections could span month headings.<br/>Contains these parameters:<br/><br/>**anchor** (**required**): <br/>  &nbsp;&nbsp;&nbsp;&nbsp;**start**: ignores anything in the document before this line. if undefined, the section collection starts at the beginning of the document<br/>    &nbsp;&nbsp;&nbsp;&nbsp;**match** (**required**): specifies the starting line of each repeating section. For example, in the preceding image, specify `"Claim number"`. If the start of the section lacks an easy-to-match line, you can use the Require Stop and Offset Y parameters to match a line other than the starting line.<br/>    &nbsp;&nbsp;&nbsp;&nbsp;**end**: ignores anything in the document after this line. If unspecified, the section collection continues to the end of the document. For example, to extract solely September claims in the preceding image, specify `"October"`.<br/><br/><br/>**stop:** a string, [Match](doc:match) object, or array of Match objects that specifies the end of the repeated section after its anchor. For example, if you specify `"Date of claim"`, then each section ends either when it encounters the next section, or when it encounters the phrase "Date of claim". Sensible ignores any text after the claimant's last name in each repeating element. <br/> If you leave this parameter unspecified, then the last repeating element in the section continues to the end of the document.<br/><br/><br/>**requireStop:**<br/> If true, the section doesn't automatically end when Sensible matches the next starting line. <br/><br/>**offsetY:** specifies the number of inches to offset the start of the section from the anchor match. Normally a section starts at the top boundary of the match line. If you specify Offset Y, the section starts at that top boundary plus the offset. This is useful when the section lacks an easy-to-match first line.<br/> |
| fields (**required**) | array of [Field objects](doc:field-query-object)       |                                                              |
| sections              |                                                        | Specifies sections inside sections. Use this for complex sections that contain nested repeated elements. |
| computed_fields       | array of [Computed fields](doc:computed-field-methods) | Transform the output of the fields.                          |

Examples
====

The following example shows extracting fields repeatedly from a section containing a list of claims:

- It captures Sept and Oct claims by specifying  sections that start with "claim number" and  collection range that starts with "September" and ends with "November".
- From each section, it excludes intervening text that isn't part of a section but that does repeat (`monthly_number_unprocessed_claims`) using a Stop parameter. Instead, it captures this info outside of sections with  `"match:all"`.

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
      "id": "monthly_number_unprocessed_claims",
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
      "id": "unprocessed_sept_oct_claims",
      "range": {
        "anchor": {
          "start": {
            "text": "September",
            "type": "startsWith",
            "isCaseSensitive": true
          },
          "match": {
            "type": "includes",
            "text": "claim number"
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
  "monthly_number_unprocessed_claims": [
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
  "unprocessed_sept_oct_claims": [
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

