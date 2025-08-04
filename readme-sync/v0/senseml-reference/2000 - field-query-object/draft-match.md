---
title: "draft"
hidden: true
---

## Repeat match


Matches the specified number of consecutive occurrences of a string.





**Parameters**

| key                  | values   | description                                                  |
| -------------------- | -------- | ------------------------------------------------------------ |
| type (**required**)  | `repeat` |                                                              |
| times (**required**) | integer  | Number of times the string must consecutively occur. TODO: how to say it must be startsWith |

**Example**

```json
{
    "type": "repeat",
    "times": 5,
    "match": {
        "type": "startsWith",
        "text": "Value:"
    }
}
```



expands to:

```json
[
          { "type": "startsWith", "text": "Value:" },
          { "type": "startsWith", "text": "Value:" },
          { "type": "startsWith", "text": "Value:" },
          { "type": "startsWith", "text": "Value:" },
          { "type": "startsWith", "text": "Value:" }
]
```

