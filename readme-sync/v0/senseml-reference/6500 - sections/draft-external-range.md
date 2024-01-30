---
title: range
hidden: true
---

|               |        |                                                              |
| ------------- | ------ | ------------------------------------------------------------ |
| externalRange | object | **horizontal sections**:  (Advanced) Enables anchoring on text that's external to the section group range in the sections' field anchors.  The text  can be anywhere in the document. For example, use it with the [Intersection](doc:intersection) method in a section to define a Vertical Anchor parameter.<br/>The external range defines a vertical range in the document similar to the section group's range parameter. Unlike the range parameter, the external range can be repeating (relative to sections) or static (only one instance/nonrepeating) Contains the following parameters:<br/><br/>`anchorIsAbsolute`: (default: true). If true, the external range is nonrepeating and Sensible starts looking at the beginning of the document to define the external range. Use this option if you want to use a single,stable external range for each section in the section group.<br/> If false, Sensible starts looking for the external range at the start of each section, to create an array of external ranges. Use this option if the external range occurs irregularly in the section group -- for example, a heading at the top of every other page which has content that changes but which you need to use, within the section group, which spans several pages. <br/>`anchor`  [Anchor](https://docs.sensible.so/docs/anchor) object. (**required?**: The start of the external range. For more information about this parameter, see the Anchor parameter in the Range object.  <br/>`stop`: (Match object)**required** end of the external range. For more information about this parameter, see the Stop parameter in the Range object. **TODO WHAT IF YOU DONT SPECIFY THIS EITHER REPEATING OR NOT REPEATING**<br/>`offsetY`: For information about this parameter, see the Offset Y parameter in the Range object.<br/>`stopOffsetY`: For information about this parameter, see the Stop Offset Y parameter in the Range object.<br/><br/><br/>**vertical sections:** N/A, not allowed for vertical sections. |
|               |        |                                                              |
|               |        |                                                              |



https://dev.sensible.so/editor/?d=frances_playground&c=sections_external_range&g=sections_external_range

```
{
  "fields": [],
  /* define section group containing document's claims */
  "sections": [
    {
      "id": "unprocessed_claims_sections",
      /* each section contains unlabeled information.
         the labels are at the beginning of the document ("Claims contents")
         use the External Range parameter to make these labels
         accessible as vertical anchors inside the sections */
      "range": {
        "externalRange": {
          "anchor": "Claim contents",
          "stop": "unprocessed claims",
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



Example 2: Dynamic External Range
---

The following example shows using a dynamic external range to make use of headings as anchors, when the headings occur at irregular and indeterminate intervals spaced out or interleaved with the sections in the sections group. 2do TODO reword

```json
{
  "fields": [],
  /* define section group containing document's claims */
  "sections": [
    {
      "id": "claims_sections",
      /* each section (in this case, a claim) contains unlabeled information, such as the claim #.
         the labels are at the top of each page ("Claims contents")
         use the External Range parameter to make these labels
         accessible as vertical anchors for the Intersection method inside the sections */
      "range": {
        "externalRange": {
          /* the alignment of the "Claim contents" labels changes for odd and even pages
           so you can't solely use the first-occurring set of labels. Those labels are
           misaligned for the claims on even pages. So use anchorIsAboslute: false
           to find a dynamic external range individually for each section. */
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
        "value": "Claim contents Claim number Claimant last name Date of claim Phone number Claim 1 1223456789 Diaz 09/15/2021 512 409 8765"
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
        "value": "Claim contents Claim number Claimant last name Date of claim Phone number Claim 2 9876543211 Badawi 09/08/2021"
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
        "value": "Claim contents Claim number Claimant last name Date of claim Phone number Claim 3 6785439210 Levy 10/03/2021 505 238 8765"
      }
    }
  ]
}
```
