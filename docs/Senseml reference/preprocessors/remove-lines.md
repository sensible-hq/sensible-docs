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
Removes lines that match the specified text from all pages in the document. For example, use this preprocessor to remove watermarks. This preprocessor is an alternative to the Remove Header and Remove Footer preprocessors and can remove text that varies in position on the page.

# Parameters

| key                  | value                                               | description                                                  |
| -------------------- | --------------------------------------------------- | ------------------------------------------------------------ |
| type (**required**)  | `removeLines`                                       |                                                              |
| match (**required**) | [Match](doc:match) object or array of Match objects | Sensible removes lines that match the specified text from all pages in the document |

# Examples

The following example shows using two `removeLines` preprocessors to clean up an academic transcript before extraction:

- The first preprocessor removes page number lines (`page 1 of 3`, `page 2 of 3`, etc.) using a regex pattern. Without this, page number lines would appear inline in the extracted text.
- The second preprocessor removes a rotated diagonal watermark using the [angleFilter](doc:match#global-parameters) option. The `angleFilter` targets lines rotated between 30 and 60 degrees.

**Config**

```json
{
  "preprocessors": [
    {
      /* remove "page x of y" lines */
      "type": "removeLines",
      "match": {
        "type": "regex",
        "flags": "i",
        "pattern": "^page\\s\\d+\\sof\\s\\d+$"
      }
    },
    {
      /* remove rotated watermark text (30–60 degrees)  }*/
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
      /* to verify lines were removed, print out document text  */
      "id": "all_text",
      "method": {
        "id": "documentRange",
        "includeAnchor": true,
        "sortLines": "readingOrderLeftToRight"
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

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/remove_lines.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/remove_lines.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "all_text": {
    "type": "string",
    "value": "Fictional University 123 Scholar Way, Fictional City, State 00001 Student Information Field Detail Name Jon E. Doe Student ID 900123456 Major Undeclared Semester: Fall 2024 Course Code Course Title Credits Grade ENG 101 Introduction to 3 B Composition PSY 100 General Psychology 3 A MAT 105 College Algebra 3 C"
  }
}
```
