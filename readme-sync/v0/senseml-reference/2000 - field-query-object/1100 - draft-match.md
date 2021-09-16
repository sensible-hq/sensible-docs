---
title: "DRAFT Match object"
hidden: true
---


Matches are instructions for matching lines of text in a document. They are valid elements in anchors and other objects. 

See the following sections for more information:

[**Match types**](doc:match#match-types)

- [Global parameters](doc:anchor#global-parameters)
- [Simple match](doc:anchor#simple-match)
- [Regex match](doc:anchor#regex-match)
- [First match](doc:anchor#first-match)
- [OR match](doc:match#or-match)

[**Examples**](doc:match#section-examples)

- [Match arrays](doc:match#section-match-arrays) 

TODO: add section for OR MATCH

Match types
===

Global Parameters
----

The following parameters are available to all types of Match objects:


| key           | values | description                                                  |
| ------------- | ------ | ------------------------------------------------------------ |
| minimumHeight | number | The minimum height of the matched line's boundaries, in inches. |
| maximumHeight | number | The maximum height of the matched line's boundaries, in inches. |



Simple match
-------

Match using strings.

**Parameters**

| key  | values                                         | description                                                  |
| ---- | ---------------------------------------------- | ------------------------------------------------------------ |
| text | string                                         | The string to match                                          |
| type | `equals`, `startsWith`, `endsWith`, `includes` | `equals`: The matching line must exactly contain the string<br/>`startsWith`: Match at beginning of line<br/>`endsWIth`: Match at end of line<br/>`includes`: Match anywhere in line |

**Example**

The following config uses as simple match:

```json
  {
  "fields": [
    {
      "id": "simple_anchor_example",
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


Regex match
-----

Match using a regular expression.

**Parameters**

| key                    | values                   | description                                                  |
| ---------------------- | ------------------------ | ------------------------------------------------------------ |
| pattern (**required**) | valid  JS regex          | Javascript-flavored regular expression. Capturing groups are not supported (see the [Regex method](doc:regex) instead).  Remember to double escape special characters since the regex is contained in a JSON object (for example, `\\s`, not `\s` , to represent a whitespace character). |
| flags                  | JS-flavored regex flags. | Flags to apply to the regex. for example: "i" for case-insensitive. |
| type (**required**)    | `regex`                  |                                                              |

**Example**

For an example, see the [Passthrough method example](doc:passthrough).

First match
------

This is a convenience match to find the first line encountered. 

**Parameters**

| key  | values  | description                                                  |
| ---- | ------- | ------------------------------------------------------------ |
| type | `first` | Matches the first line encountered, either in the first page of the document, or after a specified line. |

**Example**

This example matches the first line after a matched line:


```
{
  "fields": [
    {
      "id": "first_line_after_match",
      "anchor": {
        "match": [
          {
            "type": "includes",
            "text": "match this line, then anchor on the first line after it"
          },
          {
            "type": "first"
          }
        ]
      },
      "method": {
        "id": "label",
        "position": "below"
      }
    }
  ],
}
```

OR match parameters
---

Matches any of an array of of match objects.

**Parameters**

| key                  | values                 | description                                                  |
| -------------------- | ---------------------- | ------------------------------------------------------------ |
| match (**required**) | array of Match objects | Match any of the Match objects in the array. For example, this allows you to match on an array of synonymous terms if a document contains small wording variations across revisions. |
| type (**required**)  | `or`                   |                                                              |

**Example**

```json
{
	"fields": [{
		"anchor": {
			"match": {
				"type": "or",
				"matchers": [{
						"type": "equals",
						"text": "load value"
					},
					{
						"type": "equals",
						"text": "cargo value"
					}
				]
			}
		},
		"id": "cargo",
		"method": {
			"id": "passthrough"
		}
	}]
}
```



Examples
====

Match arrays
----

Sensible creates an anchor using the last element in a Match array only if:

- The last element is preceded by the other array elements in order, with no intervening match repetitions.
- Each array element targets a separate successive line.

This example creates an Anchor line using the last element in the array:

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
              "text": "...followed by the 1st occurrence of this string in another line",
            },
                          {
              "type": "startsWith",
              "text": "...and create an Anchor line out of this last match",
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



