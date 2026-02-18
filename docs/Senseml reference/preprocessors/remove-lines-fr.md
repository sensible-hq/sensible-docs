---
title: Remove lines
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Remove lines matching a pattern from all pages in a document'
  robots: index
next:
  description: ''
---
Removes lines that match the specified text from all pages in the document. For example, use this preprocessor to remove watermarks.

# Parameters

| key                  | value                                               | description                                                  |
| -------------------- | --------------------------------------------------- | ------------------------------------------------------------ |
| type (**required**)  | `removeLines`                                       |                                                              |
| match (**required**) | [Match](doc:match) object or array of Match objects | Sensible removes all lines that contain the text specified by the Match parameter. |

# Examples

The following example shows using two `removeLines` preprocessors together to clean up an academic transcript before extraction:

- The first preprocessor removes page number lines (`page 1 of 3`, `page 2 of 3`, etc.) using a regex pattern. Without this, page number lines would appear inline in the extracted text.
- The second preprocessor removes a rotated diagonal watermark ("This is Not an Official Transcript") using the [angleFilter](doc:match#global-parameters) option. The `angleFilter` targets only lines rotated between 30 and 60 degrees, so horizontal body text is unaffected.

**Config**

```json
{
  "preprocessors": [
    {
      /* remove "page x of y" lines */
      "type": "removeLines",
      "match": {
        "type": "regex",
        "pattern": "^page \\d+ of \\d+$"
      }
    },
    {
      /* remove rotated watermark text (30–60 degrees) */
      "type": "removeLines",
      "match": {
        "type": "regex",
        "pattern": ".",
        "angleFilter": {
          "minAngle": 30,
          "maxAngle": 60
        }
      }
    }
  ],
  "fields": [
    {
      /* to verify lines were removed, print out document text */
      "id": "all_text",
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
```

**Example document**

The following image shows the first page of the example document. Note the `page 1 of 3` line at the bottom, which is removed by the first preprocessor.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/remove_lines.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/remove_lines.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "all_text": {
    "type": "string",
    "value": "Academic History Fictional Example Transcript Create Date: 06/19/2025 10:47:25 General Information Student: García, Ana López PID: A12345678 Student Level: UN College: Fictional College Major: Computer Science Intended Degree: Bachelor of Arts Cumulative Summary Grade Option UC-Crdts Attm Crdts Pssd UC-GPA Crdts UC-Grade Points UC-GPA Letter 73.00 71.00 69.00 201.20 2.915 P/NP 12.00 16.00 0.00 0.00 0.000 TOTAL 85.00 87.00 69.00 201.20 2.915 ..."
  }
}
```
