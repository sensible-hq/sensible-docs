---
title: Remove lines
excerpt: ''
deprecated: false
hidden: true
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
| match (**required**) | [Match](doc:match) object or array of Match objects | Sensible removes all lines that contain the text specified by the Match parameter. TODO: make sure I understand if it's an "included in the line" or 'must match line exactly' sitch. |

# Examples

## Remove page number lines

The following example removes lines matching the pattern `page x of y` across all pages.

**Config**

```json
{
  "preprocessors": [
    {
      "type": "removeLines",
      "match": {
        "type": "regex",
         /* remove all page number lines, e.g., 'page 2 of 5' */
        "pattern": "^page \\d+ of \\d+$"
      }
    }
  ],
  "fields": [
    {
      /* to verify lines were removed, print out the document text */
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

## Remove rotated watermarks

The following example uses the [angleFilter](doc:match#global-parameters) matcher option to remove rotated watermark text (text rotated between 30 and 60 degrees) without matching horizontal body text.

**Config**

```json
{
  "preprocessors": [
    {
      "type": "removeLines",
      "match": {
        /* remove any text rotated 30 to 60 degrees */
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
      /* to verify lines were removed, print out the document text */
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
