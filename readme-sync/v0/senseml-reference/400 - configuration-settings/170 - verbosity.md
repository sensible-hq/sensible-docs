---
title: "Verbosity"
hidden: false
---
Add this setting to a config in order to control the verbosity of the Sensible API response. (This setting does not control verbosity in the SenseML editor's extraction pane).

Parameters
====

| Possible Values | Description                                                  |
| :-------------- | :----------------------------------------------------------- |
| `0`             | default                                                      |
| `1`             | add `lines` array to field output with `text`, `page`, and `boundingPoly` metadata |
| `3`             | add full entities metadata (anchor, lines, points, regions) plus standardized text |

Examples
====

```
{
  "verbosity": 1,
  "fields": []
}  
```

