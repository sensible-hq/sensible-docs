---
title: "Anchor object"
hidden: false
---
An *anchor* is a string, [Match](doc:anchor-object#section-match-object) object, or array of Match objects. Sensible searches first for a text "anchor" because it's a computationally quick and inexpensive way to narrow down the location in the document where you want to extract data. Then, Sensible can use a ["method"](doc:method-object) to expand out from the anchor and grab the data you want.

If you want to be syntactically concise, you can define a simple string anchor like:

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

String anchors are expanded behind the scenes to case-insensitive `includes` matches. The preceding example is expanded automatically as:

```json
      "anchor": {
        "match": {
          "type": "includes",
          "text": "this is a string to anchor on",
        }
      },
```

These are the top-level components of an expanded Anchor object:

Anchor parameters
----


| key                  | values                                 | description                                                  |
| -------------------- | -------------------------------------- | ------------------------------------------------------------ |
| match (**required**) | Match object or array of match objects | See [Match object](doc:anchor-object#section-match-object).  |
| start                | string, Match, or Match array          | Defines a point in the document at which to start searching for  the`match` you define for the anchor.  Not included in the anchor output. (You can capture anchor output with a Passthrough method).<br/> This parameter can be useful if you want to limit your search to a specific section of a document. For example, you can define a `start` that matches a section heading. <br/>Note that lines that "follow" the `start` line are most reliably those that are positioned *below* the start line. Lines to the left are not included, and lines to the right are only considered "following" if they are at exactly the same height as the `start` line on the page. In other words, a line qualifies as "successive" to the `start` line first by its y-axis position and then by its x-axis position. |
| end                  | string, Match, or Match array          | Defines a point in the document at which to stop searching for  the`match` you define for the anchor.  By default, not included in the anchor output. (You can capture anchor output with a Passthrough method).<br/>If unspecified, the anchor searches for matches to the end of the document.  <br/>Note that lines that "precede" the `end` line are most reliably those that are positioned *above* the end line. Lines to the right are not included, and lines to the left are only considered "preceding" if they are at exactly the same height as the `end` line on the page. In other words, a line qualifies as "preceding" the `start` line first by its y-axis position and then by its x-axis position. |
| includeEnd           | boolean                                | Whether to include the text in the matching `end` line in the anchor output. |

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

At first glance, you might thinking the following two anchors are two different syntaxes for the same match:

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

To clarify the difference, the following image shows the different outputs of these anchors:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/anchor_example_1.png)

This example uses the Passthrough method and `"match":all"` to display the full anchor output. It shows that:

- For the `"match_array"` field, Sensible searches for the text in the last array element, and returns that text as an anchor only if it is directly preceded by the other array elements. This explains why the line `Here is a B line again` is not returned as anchor output; this instance is not preceded by `Here is an A line`.  Since we specify `"match":all"`, Sensible does find the other  B line that qualifies: `Here is a B line that is the 2nd occurrence of “B following A” in the doc`.

  See the following image for an illustration: 

  ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/anchor_example_2.png)

- For the `"start_and_match"` field, Sensible starts the anchor search after the first instance of `here is an A line`, and discards anything earlier in the document. Then, the match specifies to find **all** instances of line B after the start match, so it returns four instances.  Notice it does NOT return the very first line B (`Here is a B line sneakily inserted before the intro line`) because that instance precedes the start match. The Stop parameter operates just as the Start parameter does, except it discards everything after the Stop matching line. See the following image for an illustration:

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
      "value": "Here is a B line for a 3rd time."
    },
    {
      "type": "string",
      "value": "Here is a B line that is the 2nd occurrence of “B following A” in the doc"
    }
  ]
}
```



Methods influence matches
-----

In addition to the match conditions you specify (such as `isCaseSensitive`), the method type also influences whether text qualifies for the anchor match.

In other words, if you set a Label method, then Sensible only matches anchor text that is a good candidate for serving as a label. If the text is too far away from any other lines to be used as a label, it won't match, even if all the conditions you set in the Match object itself are otherwise met. 

In the following example, the PDF contains two instances of the string "Python". Even though we set `"match":"last"` in the config, the config only matches the *first* instance of Python. Why? We set a Label method, and only the first instance of Python is close enough to the text below it to qualify as a label for that text ( `"position":"below"`).

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/anchor_match_last_1.png)

 On the other hand, if we set the method to `row`, then both instances of "Python" qualify, and we successfully match the last instance:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/anchor_match_last_2.png)



