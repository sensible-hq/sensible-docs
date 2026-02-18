---
title: Remove lines
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Remove lines matching a pattern'
  robots: index
next:
  description: ''
---
Removes lines that match a configurable pattern. Unlike the [Remove Header](doc:remove-header) and [Remove Footer](doc:remove-footer) preprocessors, which remove lines relative to a match position, this preprocessor removes the matched lines themselves.

# Parameters

| key                  | value                                               | description                                                                 |
| -------------------- | --------------------------------------------------- | --------------------------------------------------------------------------- |
| type (**required**)  | `removeLines`                                       |                                                                             |
| match (**required**) | [Match](doc:match) object or array of Match objects | Sensible removes all lines that match this criterion across the document.   |

# Examples

## Remove page number lines

The following example removes lines matching the pattern `page N of N` across all pages.

**Config**

```json
{
  "preprocessors": [
    {
      "type": "removeLines",
      "match": {
        "type": "regex",
        "pattern": "^page \\d+ of \\d+$"
      }
    }
  ],
  "fields": [
    {
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
