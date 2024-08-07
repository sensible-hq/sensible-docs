---
title: "Anchor nuances"
hidden: false
---

**Note:** If you're familiar with Sensible, this detailed topic is for you. If you're new to Sensible, see [anchor](doc:anchor).


Anchor syntax
----

At first glance, the following anchors may appear to be different syntaxes for finding the same matching text:



**Anchor 1**

```json
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
```

Versus:

**Anchor 2**

```json
      "anchor": {
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
| ----------- | ------------------------------------------------------------ |

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



Methods filter anchors
-----

In addition to the match conditions you specify (such as `isCaseSensitive`), the method type also influences whether text qualifies as an anchor.

For example, if you specify the Label method, Sensible anchors on text that is a good label candidate. Sensible disqualifies any line as a label that is too far away from other lines, even if it otherwise meets the conditions in the anchor's parameters.

The following example shows two anchors qualified by the Label method:

**Example Config**

```json
{
  "fields": [
    {
      "id": "anchors_candidates_filtered_by_method",
      "anchor": "python",
      "match": "first",
      "method": {
        "id": "label",
        "position": "right"
      }
    }
  ]
}
```

**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/ui_filtered_anchor.png)


| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/row_column.pdf) |
| ----------- | ------------------------------------------------------------ |

**Example Output**

The example config returns null, but returns data if you specify the Row method instead.

**Example Notes**

In this example, Sensible filters out the anchor candidates (surrounded by light yellow boxes) because they do not meet the Label method's proximity requirements. The strings "python" are far enough away from other lines that you should use the Row method here instead. 
