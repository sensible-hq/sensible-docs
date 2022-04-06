---
title: "Verbosity"
hidden: false
---
Configures the verbosity of the Sensible API response. (This setting doesn't control verbosity in the SenseML editor's extraction pane).

Parameters
====

| Possible Values | Description                                                  |
| :-------------- | :----------------------------------------------------------- |
| `0`             | default                                                      |
| `1`             | add `lines` array to field output with `text`, `page`, and `boundingPoly` metadata |
| `3`             | add full entities metadata (anchor, lines, points, regions) plus standardized text. If the standardized text output causes the extraction response to exceed 6MB, as can be the case with large documents, then Sensible returns a `413` error. |

Examples
====

```
{
  "verbosity": 1,
  "fields": []
}  
```

