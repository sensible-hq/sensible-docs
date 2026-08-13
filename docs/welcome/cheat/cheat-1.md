---
title: Cheatsheet part 1
excerpt: Hello world extraction example
deprecated: false
hidden: true
metadata:
  title: ''
  description: 'Hello world extraction example'
  robots: index
next:
  description: ''
---
# Hello world

## Solution

After you complete the steps in the tutorial, the final config is the following:

```json
{
  "fields": [
    {
      "id": "your_first_extracted_field",
      "anchor": "powerful data",
      "method": {
        "id": "box",
        "position": "right"
      }
    }
  ]
}
```

## Learn more

To learn more about the steps you took in the tutorial, see:

| Link                      | Notes                                                                            |
| ------------------------- | -------------------------------------------------------------------------------- |
| [Anchor](doc:anchor)      | Fundamental concepts.                                                            |
| [Label](doc:label)        | A frequently used extraction method.                                             |
| [Box](doc:box)            | A frequently used extraction method.                                             |
| [Color coding](doc:color) | Explains the colored boxes you see overlaid on the document in the Sensible app. |

## Initial config

To undo all your changes, paste the following config into the left pane of the SenseML editor:

```json
{
  "fields": [
    {
      "id": "your_first_extracted_field",
      "anchor": "hello world",
      "method": {
        "id": "label",
        "position": "below"
      }
    }
  ]
}
```
