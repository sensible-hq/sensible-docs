---
title: range
hidden: true
---

|               |        |                                                              |
| ------------- | ------ | ------------------------------------------------------------ |
| externalRange | object | **horizontal sections**:  (Advanced) Enables anchoring on text that's external to the section group range in the sections' field anchors.  The text  can be anywhere in the document. For example, use it with the [Intersection](doc:intersection) method in a section to define a Vertical Anchor parameter.<br/>The external range defines a vertical range in the document similar to the section group's range parameter. Unlike the range parameter, the external range can be repeating (relative to sections) or static (only one instance/nonrepeating) Contains the following parameters:<br/><br/>`anchorIsAbsolute`: (default: true). If true, the external range is nonrepeating and Sensible starts looking at the beginning of the document to define the external range. If false, Sensible starts looking for the external range at the start of each section, to create an array of external ranges. <br/>`anchor`  [Anchor](https://docs.sensible.so/docs/anchor) object. (**todo-requred?**: The start of the external range. For more information about this parameter, see the Anchor parameter in the Range object.  <br/>`stop`: (Match object)**The end of the range** end of the external range. For more information about this parameter, see the Stop parameter in the Range object. **TODO WHAT IF YOU DONT SPECIFY THIS EITHER REPEATING OR NOT REPEATING**<br/>`offsetY`: For information about this parameter, see the Offset Y parameter in the Range object.<br/>`stopOffsetY`: For information about this parameter, see the Stop Offset Y parameter in the Range object.<br/><br/><br/>**vertical sections:** N/A, not allowed for vertical sections. |
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

