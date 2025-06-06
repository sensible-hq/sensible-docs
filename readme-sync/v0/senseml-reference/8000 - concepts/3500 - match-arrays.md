---
title: "Match arrays"
hidden: false
---

**Note:** If you're familiar with Sensible, this detailed topic is for you. If you're new to Sensible, see [match](doc:match).



Sensible matches the last element in a Match array if:

- Each array element targets a separate successive line in the document. 
- The matches specified in the array occur in the document in the same order as in the array. For more information about line ordering, see [Lines](doc:lines).

This example creates an Anchor line using the last element in the array:

```json
{
  "fields": [
    {
      "id": "match_array",
      "anchor": {
        "start": "My section heading to start matching on",
        "end": "My footer text to stop matching on",
        "includeEnd": true,
        "match": 
          [
            {
              "type": "includes",
              "text": "finds anchor if you match this string in a line",
            },
            {
              "type": "startsWith",
              "text": "followed by the first occurrence of this string in another line",
            },
                          {
              "type": "regex",
              "pattern": ".*create an Anchor line out of this last match",
            },
          ]      
      },
      "method": {
        "id": "label",
        "position": "below"
      }
    }
  ]
}
```

Reverse match arrays
---

Use the Reverse parameter when a difficult-to-match target line precedes an easy-to-match line. You can match the easy line, then set `"reverse:true"` to search preceding lines until you match the difficult line. 

**Config**

```json
{
  "fields": [
    {
      "id": "reverse_example",
      "anchor": {
        "match": [
          {
            "type": "startsWith",
            "text": "section header"
          },
          {
            "type": "startsWith",
            "text": "an unusual line"
          },
          {
            "type": "startsWith",
            "text": "a common line",
            "reverse": true
          }
        ]
      },
      "method": {
        "id": "label",
        "position": "below",
        "textAlignment": "hangingIndent"
      }
    }
  ]
}
```



**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/reverse_1.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/reverse.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "reverse_example": {
    "type": "string",
    "value": "Target data"
  }
}
```

**Notes**

In a reverse match array, Sensible searches for anchor candidates in sequence, and rules out overlapping match arrays. The following image illustrates this behavior for the example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/reverse_2.png)

## Nuances: Match arrays versus Anchor start 

Match arrays have a different effect from a start-and-match combination. For example, at first glance, the following anchors may appear to be different syntaxes for finding the same matching text:

**Anchor 1**

```json
      "anchor": {
        // match array
        "match": [
          {
            "type": "startsWith",
            "text": "here is an A line"
          },
          {
            "type": "startsWith",
            "text": "here is a B line"
          }
        ]
      },
```

Versus:

**Anchor 2**

```json
      "anchor": {
        // same matches, same sequence, but in Start and Match parameters
        "start": {
          "type": "startsWith",
          "text": "here is an A line"
        },
        "match": {
          "type": "startsWith",
          "text": "here is a B line"
        }
    
```

The difference between these two is:

- anchor 1 finds an instance of line B preceded by line A.
- anchor 2 searches after the first instance of line A for a line B, and discards anything earlier in the document. 

To clarify the difference,  consider a simple document with the following content:

```
EXAMPLE DOCUMENT

Here is a B line sneakily inserted before the intro line.

Here is an intro line

Here is an A line.

Here is an A line again.

Here is a B line.

Here is a B line again.

Here is a C line.

Here is a B line for the 4th time.

Here is an A line for the 3rd time.

Here is a C line again

Here is a B line that is the 2nd occurrence of “B following A” in the doc

Here is an ending line.
```



For **Anchor 1**, Sensible anchors on the last Match array element if it's preceded by the other array elements in order.  `"match":all"` finds two anchors. See the following image for an illustration: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/anchor_2.png)

- For **Anchor 2**, Sensible searches after the first instance of `here is an A line`, and discards anything earlier in the document. `"match":all"` finds four anchors. Notice it doesn't anchor on the first line B (`Here is a B line sneakily inserted before the intro line`) because that instance precedes the start match. See the following image for an illustration:

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/anchor_3.png)

Try out this example in the Sensible app using the following document and config:

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/anchor.pdf) |
| ---------------- | ------------------------------------------------------------ |

This example uses the following config:

```json
{
  "fields": [
    {
      "id": "match_array",
      "match": "all",
      "anchor": {
        "match": [
          {
            "type": "startsWith",
            "text": "here is an A line"
          },
          {
            "type": "startsWith",
            "text": "here is a B line"
          }
        ]
      },
      "method": {
        "id": "passthrough"
      }
    },
    {
      "id": "start_and_match",
      "match": "all",
      "anchor": {
        "start": {
          "type": "startsWith",
          "text": "here is an A line"
        },
        "match": {
          "type": "startsWith",
          "text": "here is a B line"
        }
      },
      "method": {
        "id": "passthrough"
      }
    }
  ]
}
```

And the output of this example is:

```json
{
  "match_array": [
    {
      "type": "string",
      "value": "Here is a B line."
    },
    {
      "type": "string",
      "value": "Here is a B line that is the 2nd occurrence of “B following A” in the doc"
    }
  ],
  "start_and_match": [
    {
      "type": "string",
      "value": "Here is a B line."
    },
    {
      "type": "string",
      "value": "Here is a B line again."
    },
    {
      "type": "string",
      "value": "Here is a B line for the 4th time."
    },
    {
      "type": "string",
      "value": "Here is a B line that is the 2nd occurrence of “B following A” in the doc"
    }
  ]
}
```
