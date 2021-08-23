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
| start                                           | string, Match object, or Match object array | Start the search for the anchor's Match parameter at a line of text in the document, and ignore all the text that precedes the start line. <br/> The terms "preceding" and "succeeding" primarily mean *above* or *below* the Start line. For more information, see [Line sorting](doc:concepts#line-sorting).<br/>The Start line is never included in anchor output. (You can extract other anchor output with a Passthrough method). |
| end                                             | string, Match, or Match array               | Stop the search for the anchor's Match parameter at a line of text in the document, and ignore all the text that succeeds the End line. <br/> The terms "preceding" and "succeeding" primarily mean *above* or *below* the End line. For more information, see [Line sorting](doc:concepts#line-sorting).<br/>If unspecified, the anchor searches for matches to the end of the document.  <br/> |
| includeEnd                                      | boolean                                     | Whether to include the matching End line in the anchor output. |

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
              "text": "Only finds anchor if you match this string in a line that is between the start and end lines",
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

At first glance, the following anchors may appear to be different syntaxes for finding the same matching text:

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

To clarify the difference,  the following image shows the outputs of these anchors:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/anchor_example_1.png)

This example uses the Passthrough method and `"match":all"` to display the full anchor output. It shows that:

- For the `match_array` field, Sensible anchors on the last Match array element only if it is preceded by the other array elements in order, with no intervening match repetitions.   `"match":all"` finds two anchors. See the following image for an illustration: 

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/anchor_example_2.png)

- For the `start_and_match` field, Sensible searches after the first instance of `here is an A line`, and discards anything earlier in the document.  `"match":all"` finds four anchors. Notice it does NOT return the very first line B (`Here is a B line sneakily inserted before the intro line`) because that instance precedes the start match.  See the following image for an illustration:

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/anchor_example_3.png)

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



Methods qualify anchors
-----

In addition to the match conditions you specify (such as `isCaseSensitive`), the method type also influences whether text qualifies as an anchor.

For example, if you specify the Label method, Sensible only anchors on text that is a good label candidate. Any line that is too far away from other lines to be used as a label is disqualified, even if it otherwise meets the conditions in the anchor's parameters.

In the following image, there are two filtered out "python" strings surrounded by light yellow boxes. They are filtered out because they do not meet the Label method's proximity requirements (the Row method would work here instead):

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/ui_filtered_anchor.png)







