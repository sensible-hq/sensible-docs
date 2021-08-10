---
title: "Anchor object"
hidden: false
---
An *anchor* is a string, [Match](doc:match) object, or array of Match objects. An anchor is a computationally quick way to narrow down the location of the data you want to extract in a document. After locating the anchor, Sensible uses a ["method"](doc:method) to expand out from the anchor and extract the data you want.

[**Parameters**](doc:anchor#section-parameters)
[**Examples**](doc:anchor#section-examples)
[**Notes**](doc:anchor#section-notes)

Anchors can be simple or complex. The following example is a simple string anchor:

```json
{
  "fields": [
    {
      "id": "simple_label",
      "anchor": "this is a string to anchor on",
      "method": {
        "id": "label",
        "position": "below"
      }
    }
  ]
} 
```

String anchors are expanded behind the scenes to case-insensitive `includes` matches. Sensible automatically expands the preceding example as:

```json
      "anchor": {
        "match": {
          "type": "includes",
          "text": "this is a string to anchor on",
        }
      },
```

Parameters
----

An Anchor object has the following top-level parameters:


| key                                             | values                                      | description                                                  |
| ----------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------ |
| match (**required**, except for string anchors) | Match object or array of Match objects      | See [Match object](doc:match).                               |
| start                                           | string, Match object, or Match object array | Defines a line of text in the document after which to start searching for the anchor's Match parameter, and ignore all the text that precedes that start line. <br/> The terms "preceding" and "succeeding" primarily mean *above* or *below* the Start line. <br/>The Start line is never included in the anchor output. (You can capture anchor output with a Passthrough method). |
| end                                             | string, Match, or Match array               | Defines a point in the document at which to stop searching for  the`match` you define for the anchor.  By default, not included in the anchor output. (You can capture anchor output with a Passthrough method).<br/>If unspecified, the anchor searches for matches to the end of the document.  <br/>Note that lines that "precede" the `end` line are most reliably those that are positioned *above* the end line. Lines to the right are not included, and lines to the left are only considered "preceding" if they are at exactly the same height as the `end` line on the page. In other words, a line qualifies as "preceding" the `start` line first by its y-axis position and then by its x-axis position. |
| includeEnd                                      | boolean                                     | Whether to include the text in the matching `end` line in the anchor output. |

Examples
----

Here's an example of an Anchor object that uses all these parameters: 

```json
{
  "fields": [
    {
      "id": "simple_label",
      "anchor": {
        "start": "My section heading. Start matching after it",
        "end": "My footer text. Stop matching before it",
        "includeEnd": true,
        "match": 
          [
            {
              "type": "includes",
              "text": "Only finds anchor if you match this string in a line that is between the start and end lines (best to ensure start is above and end is below the text you want to match).",
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





Notes
====

Anchor nuances 
----

At first glance, the following two anchors may appear to be two different syntaxes for finding the same matching text:

```json
      "anchor": {
        "match": [
          {
            "type": "startsWith",
            "text": "here is a first line"
          },
          {
            "type": "startsWith",
            "text": "here is a second line"
          }
        ]
      },
```

Versus:

```json
      "anchor": {
        "start": {
          "type": "startsWith",
          "text": "here is a first line"
        },
        "match": {
          "type": "startsWith",
          "text": "here is a second line"
        }
    
```

To clarify the difference,  the following image shows the outputs of these anchors:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/anchor_example_1.png)

This example uses the Passthrough method and `"match":all"` to display the full anchor output. It shows that:

- For the `"match_array"` field, Sensible searches for the text in the last array element, and anchors on that text only if it is preceded by the other array elements in order, with no intervening repetitions of matches.  Since we specify `"match":all"`, Sensible finds two anchors. See the following image for an illustration of how Sensible matches two B lines: 

  ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/anchor_example_2.png)

- For the `"start_and_match"` field, Sensible searches after the first instance of `here is an A line`, and discards anything earlier in the document. Then, the match specifies to find **all** instances of line B after the start match, so it returns four anchors.  Notice it does NOT return the very first line B (`Here is a B line sneakily inserted before the intro line`) because that instance precedes the start match.  See the following image for an illustration:

  ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/anchor_example_3.png)

You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for anchor syntax | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/anchor_example.pdf) |
| ----------------------------- | ------------------------------------------------------------ |

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

In addition to the match conditions you specify (such as `isCaseSensitive`), the method type also influences whether text qualifies for the anchor match.

In other words, if you set a Label method, then Sensible only matches anchor text that is a good candidate for serving as a label. If the text is too far away from any other lines to be used as a label, it won't match, even if all the conditions you set in the Match object itself are otherwise met. 

In the following image, there are two filtered out "python" strings surrounded by light yellow boxes. They are filtered out because they do not meet the Label method's proximity requirements (the Row method would work here instead):

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/ui_filtered_anchor.png)







