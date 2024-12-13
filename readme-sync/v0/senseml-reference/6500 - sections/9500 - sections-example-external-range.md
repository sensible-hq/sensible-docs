---
title: "Advanced: External anchors for sections"
hidden: false
---

The following examples show using text external to sections groups as anchors for the section's fields.

One example uses a static external range to anchor on a heading that occurs once in the document. Another example uses a dynamic external range to anchor on irregularly repeating headings interleaved with sections.

Example: static
---

The following example shows extracting repeated fields from a section group, when each section lacks anchoring text. To overcome this limitation, the example accesses anchors outside the sections by defining a single, static external range that occurs at the beginning of the document.

In the following screenshot, the green brackets denote sections, where each section is a claim. The orange brackets denote an external range. The labels for the claims' content is at the start of the document, under the `Claims contents` heading. The example defines an external range for these labels, then uses the [Intersection](doc:intersection) method to specify vertical anchors in the external range.

**Config**

```json
{
  "fields": [
    {
      /* define section group containing document's claims */
      "id": "unprocessed_claims_sections",
      "type": "sections",
      /* each section contains unlabeled information.
         the labels are at the beginning of the document ("Claims contents")
         use the External Range parameter to make these labels
         accessible as vertical anchors inside the sections */
      "range": {
        "externalRange": {
          "anchor": "Claim contents",
          "stop": "unprocessed claims",
          /* Starting from the document beginning, Sensible searches
             for one static external range */
          "anchorIsAbsolute": true
        },
        /* include 'claim no' heading above section start for use as anchoring text*/
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
             then adjust width, height, and offsets
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
            /* anchor on text from the external range */
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
            /* anchor on text from the external range */
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
            /* anchor on text from the external range */
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

Example: Dynamic
---

The following example shows extracting repeated fields from a section group, when each section lacks anchoring text. To overcome this limitation, the example accesses anchors outside the sections. The sections anchor on external ranges that capture page headings, whose alignment changes for odd and even pages.  To avoid misaligned [Intersection](doc:intersection) methods in each section, the example defines dynamic external ranges relative to each section to capture each page's heading.

In the following screenshot, the green brackets denote sections, where each section is a claim. Orange brackets denote external ranges. The labels for the claims' content is at the start of each page, under the `Claims contents` heading. 

**Config**

```json
{
  "fields": [
    {
      /* define section group containing document's claims */
      "id": "claims_sections",
      "type": "sections",
      /* each section (in this case, a claim) contains unlabeled information, such as the claim #.
         the labels are at the top of each page under a "Claims contents" heading
         use the External Range parameter to make these labels
         accessible as vertical anchors for the Intersection method inside the sections */
      "range": {
        "externalRange": {
          /* the alignment of the "Claim contents" labels changes for odd and even pages
           so you can't solely use the first-occurring set of labels. The first-occuring labels are
           misaligned for the claims on even pages. So use anchorIsAboslute: false
           to find a dynamic external range relative to each section. */
          "anchorIsAbsolute": false,
          "anchor": [
            /* Sensible searches for a dynamic external range, beginning from the start of each section.
              Since the external ranges precede each section, use reverse:true to search preceding lines for the
              closest occurence of "Claim contents" */
            {
              "type": "includes",
              "text": "Claim contents",
              "reverse": true
            }
          ],
          // each dynamic external range ends after the heading "Claim #", e.g., Claim 1
          "stop": {
            "type": "regex",
            "pattern": "Claim \\d+",
            "flags": "i"
          },
        },
        "anchor": {
          /* each claim section starts with the heading "Claim #", e.g., "Claim 1" */
          "match": {
            "type": "regex",
            "pattern": "Claim \\d+"
          },
          /* end looking for claims before "total claims" heading */
          "end": {
            "type": "includes",
            "text": "total claims"
          }
        },
        /* each claim ends under the claim date. 
           This prevents last section in group 
           from extending to end of document */
        "stop": {
          "type": "regex",
          "pattern": "\\d{2}/\\d{2}/\\d{4}$"
        },
      },
      /* return each claim as object containing fields such as claim # and phone # */
      "fields": [
        {
          /* for each field,
             find the intersection of "Claim [number]"
             and on the relevant text in the 
             "Claim contents" external range,
             then adjust width, height, and offsets
             till the green box is centered
             on the target data  */
          "id": "claim_number",
          "type": "number",
          "anchor": {
            "match": {
              "type": "regex",
              "pattern": "Claim \\d+",
              "flags": "i"
            }
          },
          "method": {
            "id": "intersection",
            /* anchor on text from the external range */
            "verticalAnchor": "Claim number",
            "width": 1.5,
            "height": 0.5,
            "offsetY": 0.35
          }
        },
        {
          "id": "phone_number",
          "anchor": {
            "match": {
              "type": "regex",
              "pattern": "Claim \\d+",
              "flags": "i"
            }
          },
          "method": {
            "id": "intersection",
            /* anchor on text from the external range */
            "verticalAnchor": "Phone number",
            "width": 1.5,
            "height": 0.5,
            "offsetY": 0.9
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
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sections_external_range_dynamic.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/sections_external_range_dynamic.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "claims_sections": [
    {
      "claim_number": {
        "source": "1223456789",
        "value": 1223456789,
        "type": "number"
      },
      "phone_number": {
        "type": "string",
        "value": "512 409 8765"
      },
      "_everything_in_this_section": {
        "type": "string",
        "value": "Claim contents Claim number Claimant last name Date of claim Phone number September unprocessed claims Claim 1 1223456789 Diaz 09/15/2021 512 409 8765"
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
        "value": "Claim contents Claim number Claimant last name Date of claim Phone number September unprocessed claims Claim 2 9876543211 Badawi 09/08/2021"
      }
    },
    {
      "claim_number": {
        "source": "6785439210",
        "value": 6785439210,
        "type": "number"
      },
      "phone_number": {
        "type": "string",
        "value": "505 238 8765"
      },
      "_everything_in_this_section": {
        "type": "string",
        "value": "Claim contents Claim number Claimant last name Date of claim Phone number September unprocessed claims Claim 1 6785439210 Levy 10/03/2021 505 238 8765"
      }
    }
  ]
}
```

