---
title: "Match object"
hidden: false
---


Matches are instructions for matching lines of text in a document. They are valid elements in anchors and other objects. 

There are three different types of Match objects, including simple, regex, and first matches.  The following parameters are available to all types of Match objects:

[**Parameters**](doc:match#section-parameters)
[**Examples**](doc:match#section-examples)

Parameters
===

Global Match Parameters
----


| key           | values | description                                                  |
| ------------- | ------ | ------------------------------------------------------------ |
| minimumHeight | number | The minimum height of the matched line's boundaries, in inches. |
| maximumHeight | number | The maximum height of the matched line's boundaries, in inches. |



See the following sections for more information about each match type:

- [Simple matcher](doc:anchor#section-simple-match)
- [Regex match](doc:anchor#section-regex-match)
- [First match](doc:anchor#section-first-match)

You can define match arrays. See [Match arrays](doc:match#section-match-arrays) 
The *type* of method you use can determine whether text qualifies for a match or not. See [Methods influence matches](doc:anchor#section-methods-influence-matches).





Simple Match Parameters
-------

Match using strings.

**Parameters**

| key  | values                                         | description                                                  |
| ---- | ---------------------------------------------- | ------------------------------------------------------------ |
| text | string                                         | The string to match                                          |
| type | `equals`, `startsWith`, `endsWith`, `includes` | `equals`: The matching line must exactly contain the string<br/>`startsWith`: Match at beginning of line<br/>`endsWIth`: Match at end of line<br/>`includes`: Match anywhere in line |

For an example, see the following Examples section.


Regex Match Parameters
-----

Match using a regular expression.

**Parameters**

| key                    | values                   | description                                                  |
| ---------------------- | ------------------------ | ------------------------------------------------------------ |
| pattern (**required**) | valid  JS regex          | Javascript-flavored regular expression. Capturing groups are not supported (see the [Regex method](doc:regex) instead).  Note you have to double escape characters, since the regex is contained in a JSON object (for example, `\\s`, not `\s` , to represent a whitespace character). |
| flags                  | JS-flavored regex flags. | Flags to apply to the regex. for example: "i" for case-insensitive, "g", "m", etc. |
| type (**required**)    | `regex`                  |                                                              |

For an example, see the [Passthrough method example](doc:passthrough).





First match Parameters
------

This is a convenience match to find the first line encountered. 

**Parameters**

| key  | values  | description                                                  |
| ---- | ------- | ------------------------------------------------------------ |
| type | `first` | Matches the first line encountered, usually on a specified page. |

For an example, see the following examples section.



Examples
====

Simple match
---

```json
  {
  "fields": [
    {
      "id": "simple_label",
      "anchor": {
        "match": {
          "type": "startsWith",
          "text": "The line must start with this text",
        }
      },
      "method": {
        "id": "label",
        "position": "below"
      }
    }
  ]
} 


```

First match
----
This example grabs all the lines in the document after the first line:


```
{
  "fields": [
    {
      "id": "all_lines_in_doc",
      "anchor": {
        "match": {
          "type": "first",
        }
      },
      "method": {
        "id": "documentRange"
      }
    }
  ],
}
```

Match for OCR processor
----


The following example performs OCR only on a set page range. It's useful to narrow the page range, since OCR is slow and computationally expensive. For example, some document types may have inserted scans on specific known pages, so you need to OCR only those pages and let Sensible perform direct text extraction on all other pages:

```json
{
  "preprocessors": [
    {
      "type": "ocr",
      "match": {
        "type": "first"
      },
      "pageOffset": 7
    },
  ],
  "fields": [
    {
      "id": "some_key",
      "anchor":  "some string",
      "method": {
        "id": "label",
        "position":"above"
      }
    }
  ],
}
```



Match arrays
----

For an array of Match objects, all matches must be found to successfully create an anchor.  Each Match object must target a separate successive line. In other words, the second match starts its search in the line after the line matched by the first Match object in the array, and so on.  Sensible searches for the text in the last array element, and anchors on that text only if it is preceded by the other array elements in order, with no intervening repetitions of matches.

```json
{
  "fields": [
    {
      "id": "simple_label",
      "anchor": {
        "start": "My section heading to start matching on",
        "end": "My footer text to stop matching on",
        "includeEnd": true,
        "match": 
          [
            {
              "type": "includes",
              "text": "Only finds anchor if you match this string in a line...",
            },
            {
              "type": "startsWith",
              "text": "...Followed by the 1st occurrence of this string in another line",
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



