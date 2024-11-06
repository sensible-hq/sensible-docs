---
title: "Anchor object"
hidden: false
---
An *anchor* is a string, [Match](doc:match) object, or array of Match objects. 

An anchor's behavior depends on its field's method:

| Category             | Required? | Notes                                                        |
| -------------------- | --------- | ------------------------------------------------------------ |
| Layout-based methods | required  | An anchor is a computationally quick way to narrow down the rough location of the data you want to extract in a document. After locating the anchor, Sensible uses a layout-based ["method"](doc:method) to spatially expand out from the anchor and extract the data you want. |
| LLM-based methods    | optional  | An anchor is a test for running a field or skipping it. If the anchor is present in the document, Sensible searches the whole document for the target data. If the anchor is missing, Sensible returns null for the field. You can use this behavior to define backup, or  "[fallback](doc:fallbacks)", fields.<br/>For an exception to this behavior, see the [Multimodal Engine](doc:query-group#parameters) parameter. |

[**Parameters**](doc:anchor#parameters)
[**Examples**](doc:anchor#examples)
[**Notes**](doc:anchor#notes)

Define anchors using simple or complex syntax. The following example shows simple syntax:

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
| start                                           | string, Match object, or Match object array | Starts the search for the anchor's Match parameter and for its End parameter at a line of text in the document, and ignores all the text that precedes the start line. <br/> The terms "preceding" and "succeeding" primarily mean *above* and *below* the Start line, respectively. For more information, see [Line sorting](doc:lines#line-sorting).<br/>You can extract anchor output with the [Passthrough method](doc:passthrough). |
| end                                             | string, Match, or Match array               | Stops the search for the anchor's Match parameter before a line of text in the document.  Ignores the End line and all the text that succeeds the End line. <br/> The terms "preceding" and "succeeding" primarily mean *above* and *below* the End line, respectively. For more information, see [Line sorting](doc:lines#line-sorting).<br/>If unspecified, the anchor searches for matches to the end of the document.<br/>If you specify a Start line, Sensible searches for the End line starting at the Start line instead of at the start of the document.<br/> |
| includeEnd                                      | boolean. default: false                     | Whether to include or ignore the End line in the search for the anchor's Match parameter. |

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



