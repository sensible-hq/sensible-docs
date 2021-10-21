---
title: "Match object"
hidden: false

---


Matches are instructions for matching lines of text in a document. They're valid elements in anchors and other objects. 

See the following sections for more information:

[**Match types**](doc:match#match-types)

- [Global parameters](doc:anchor#global-parameters)
- [Simple match](doc:anchor#simple-match)
- [Regex match](doc:anchor#regex-match)
- [First match](doc:anchor#first-match)
- [Any match](doc:match#any-match)



Match types
===

Global parameters
----

The following parameters are available to most types of Match objects:


| key           | values | description                                                  |
| ------------- | ------ | ------------------------------------------------------------ |
| minimumHeight | number | The minimum height of the matched line's boundaries, in inches. Not valid as a top-level parameter for an Any match, but valid for individual matches in the Any match. |
| maximumHeight | number | The maximum height of the matched line's boundaries, in inches. Not valid as a top-level parameter for an Any match, but valid for individual matches in the Any match. |



Simple match
-------

Match using strings.  

**Parameters**

| key                  | values                                         | description                                                  |
| -------------------- | ---------------------------------------------- | ------------------------------------------------------------ |
| text  (**required**) | string                                         | The string to match                                          |
| type (**required**)  | `equals`, `startsWith`, `endsWith`, `includes` | `equals`: The matching line must equal the string<br/>`startsWith`: Match at beginning of line<br/>`endsWIth`: Match at end of line<br/>`includes`: Match anywhere in line |

**Example**

The following config uses a simple match:

```json
  {
  "fields": [
    {
      "id": "simple_anchor",
      "anchor": {
        "match": {
          "type": "startsWith",
          "text": "The line to match must start with this text",
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

**Notes**

For even simpler matching syntax in anchors, you can use `"anchor":"some string to match"`. For more information see [Anchor](doc:anchor).

Regex match
-----

Match using a regular expression.

**Parameters**

| key                    | values                   | description                                                  |
| ---------------------- | ------------------------ | ------------------------------------------------------------ |
| type (**required**)    | `regex`                  |                                                              |
| pattern (**required**) | valid  JS regex          | Javascript-flavored regular expression. This parameter doesn't support capturing groups. See the [Regex method](doc:regex) instead.<br/>Double escape special characters since the regex is in a JSON object (for example, `\\s`, not `\s` , to represent a whitespace character. |
| flags                  | JS-flavored regex flags. | Flags to apply to the regex. for example: "i" for case-insensitive. |

**Example**

For an example, see the [Passthrough method example](doc:passthrough).

First match
------

This is a convenience match to find the first line encountered. 

**Parameters**

| key                 | values  | description                                                  |
| ------------------- | ------- | ------------------------------------------------------------ |
| type (**required**) | `first` | Matches the first line encountered, either 1. in the first page of the document or 2.  after the preceding matched line in a match array. |

**Example**

This example matches the first line after a matched line in an array:


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

Any match
---

Matches any of an array of Simple or Regex match objects.

**Parameters**

| key                    | values                                 | description                                                  |
| ---------------------- | -------------------------------------- | ------------------------------------------------------------ |
| type (**required**)    | `any`                                  |                                                              |
| matches (**required**) | array of regex or simple Match objects | Match any of the Match objects in the array. For example, this allows you to match on an array of synonymous terms if a document contains small wording variations across revisions. |

**Example**

```json
{
	"fields": [{
		"anchor": {
			"match": {
				"type": "any",
				"matches": [{
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

Sensible creates an anchor using the last element in a Match array if:

- The other array elements preceed the last element in order.
- Each array element targets a separate successive line.

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
              "type": "includes",
              "text": "followed by the first occurrence of this string in another line",
            },
                          {
              "type": "includes",
              "text": "and create an Anchor line out of this last match",
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



()(http://afdpqwoeihbznxcvsawasldkgh189asdfasdg34t.com)
