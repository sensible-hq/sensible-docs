---
title: "Anchor object"
hidden: false
---
An *anchor* is a string, [Match](doc:match) object, or array of Match objects. An anchor is a computationally quick way to narrow down the location of the data you want to extract in a document. After locating the anchor, Sensible uses a ["method"](doc:method) to expand out from the anchor and extract the data you want.

[**Parameters**](doc:anchor#parameters)
[**Examples**](doc:anchor#examples)
[**Notes**](doc:anchor#notes)

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

Behind the scenes, Sensible expands string anchors to case-insensitive `includes` matches. For example, Sensible automatically expands the preceding example as:

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
| start                                           | string, Match object, or Match object array | Start the search for the anchor's Match parameter at a line of text in the document, and ignore all the text that precedes the start line. <br/> The terms "preceding" and "succeeding" primarily mean *above* and *below* the Start line, respectively. For more information, see [Line sorting](doc:lines#line-sorting).<br/>You can extract anchor output with the [Passthrough method](doc:passthrough). |
| end                                             | string, Match, or Match array               | Stop the search for the anchor's Match parameter at a line of text in the document, and ignore all the text that succeeds the End line. <br/> The terms "preceding" and "succeeding" primarily mean *above* and *below* the End line, respectively. For more information, see [Line sorting](doc:lines#line-sorting).<br/>If unspecified, the anchor searches for matches to the end of the document. <br/> |
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
        "start": "My section heading. Start matching at the start of this line",
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

For information about complex anchor syntax, see [Anchor nuances](doc:anchor-nuances).



