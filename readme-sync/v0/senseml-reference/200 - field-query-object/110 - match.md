---
title: "Match object"
hidden: false
---


Matches are instructions for matching lines of text in a document. They are valid elements in anchors and other objects. 

See the following sections for more information:

[**Parameters**](doc:match#parameters)

- [Global parameters](doc:anchor#global-parameters)

- [Simple match parameters](doc:anchor#simple-match-parameters)
- [Regex match parameters](doc:anchor#regex-match-parameters)
- [First match parameters](doc:anchor#first-match-parameters)

[**Examples**](doc:match#section-examples)

- [Match arrays](doc:match#section-match-arrays) 

Parameters
===

Global Parameters
----

The following parameters are available to all types of Match objects:


| key           | values | description                                                  |
| ------------- | ------ | ------------------------------------------------------------ |
| minimumHeight | number | The minimum height of the matched line's boundaries, in inches. |
| maximumHeight | number | The maximum height of the matched line's boundaries, in inches. |



Simple match parameters
-------

Match using strings.

**Parameters**

| key  | values                                         | description                                                  |
| ---- | ---------------------------------------------- | ------------------------------------------------------------ |
| text | string                                         | The string to match                                          |
| type | `equals`, `startsWith`, `endsWith`, `includes` | `equals`: The matching line must exactly contain the string<br/>`startsWith`: Match at beginning of line<br/>`endsWIth`: Match at end of line<br/>`includes`: Match anywhere in line |

The following config uses as simple match:

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


Regex match parameters
-----

Match using a regular expression.

**Parameters**

| key                    | values                   | description                                                  |
| ---------------------- | ------------------------ | ------------------------------------------------------------ |
| pattern (**required**) | valid  JS regex          | Javascript-flavored regular expression. Capturing groups are not supported (see the [Regex method](doc:regex) instead).  Note you have to double escape characters, since the regex is contained in a JSON object (for example, `\\s`, not `\s` , to represent a whitespace character). |
| flags                  | JS-flavored regex flags. | Flags to apply to the regex. for example: "i" for case-insensitive, "g", "m", etc. |
| type (**required**)    | `regex`                  |                                                              |

For an example, see the [Passthrough method example](doc:passthrough).



First match parameters
------

This is a convenience match to find the first line encountered. 

**Parameters**

| key  | values  | description                                                  |
| ---- | ------- | ------------------------------------------------------------ |
| type | `first` | Matches the first line encountered, usually on a specified page. |

This example grabs all the lines in the document:


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
        "id": "documentRange",
        "includeAnchor": true
      }
    }
  ],
}
```


Examples
====

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



