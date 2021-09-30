---
title: "Sections"
hidden: false
---

Extracts data from a document that contains complex or repeated elements ("sections"). 

Sensible returns an array of objects corresponding to the sections. The following image shows an example of a document containing repeated "claims" sections:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_1.png)

For the preceding example, you can configure Sensible to return an `unprocessed_claims` array, where each object in the array contains a `claim_number`, `claim_date`, `claimant_last_name`, etc. 

Parameters
====


| key                   | value                                                  | description                                                  |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)     | string                                                 | Identifies a collection of sections to extract in the document area defined by the Range parameter. You can specify multiple sections, and you can nest sections inside of other sections. |
| range  (**required**) | object                                                 | Specifies the range of both:<br/>- a collection of repeated sections in an area of the document <br/>- the start and end of each repeated section.<br/>The collection of sections can span nonrepeating text.  For example,  in the preceding image, an "unprocessed_claims" collection of sections could span multiple month headings. Contains Anchor and Stop parameters.<br/>To summarize these parameters:<br/><br/>**anchor**: <br/>  &nbsp;&nbsp;&nbsp;&nbsp;**start**: ignore anything in the document before this line. if undefined, the section collection starts at the beginning of the document<br/>    &nbsp;&nbsp;&nbsp;&nbsp;**match** (**required**): defines the start of each repeating section<br/>    &nbsp;&nbsp;&nbsp;&nbsp;**end**: ignore anything in the document after this line. If unspecified, the section collection goes to the end of the doc.<br/>**stop:** defines the end of each repeating section<br/><br/>The following contains more details about these parameters<br/>**anchor** (**required**)-an [Anchor](doc:anchor) or string object that defines the Start, Match, and End parameters for each repeated section anchor. <br/>The **Start parameter** defines the section collection's start. If unspecified, defaults to the start of the document.<br/> The **Match parameter** (**required**) specifies the first line in each repeating element for this element. For example, in the preceding image, specify `"Claim number"`. <br/>The **End parameter** defines the end of the section collection. For example, to extract only September claims in the preceding image, specify `"October"`.<br/> **stop** - a string, [Match](doc:match) object, or array of Match objects that defines the end of the repeated section after its anchor. For example, if you specify `"Date of claim"`, then each section would end either when it encounters the next section, or when it encounters the phrase "Date of claim". Any text in the section after the claimant's last name would be ignored in each repeating element. <br/> If you leave this parameter unspecified, then the last repeating element in the section continues to the end of the document.<br/><br/> |
| fields (**required**) | array of [Field objects](doc:field-query-object)       |                                                              |
| sections              |                                                        | Defines sections inside sections. Use this for complex sections that contain nested repeated elements. |
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

