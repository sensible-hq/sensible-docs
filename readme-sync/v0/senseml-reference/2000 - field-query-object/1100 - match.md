---
title: "Match object"
hidden: false

---


Matches are instructions for matching lines of text in a document. They're valid elements in anchors and other objects. 

See the following sections for more information:

[**Match types**](doc:match#match-types)

- [Global parameters](doc:match#global-parameters)
- [Simple match](doc:match#simple-match)
- [Regex match](doc:match#regex-match)
- [First match](doc:match#first-match)
- [Any match](doc:match#any-match)

[**Match arrays**](doc:match#match-arrays)


Match types
===

Global parameters
----

The following parameters are available to most types of Match objects:


| key           | values                  | description                                                  |
| ------------- | ----------------------- | ------------------------------------------------------------ |
| minimumHeight | number                  | The minimum height of the matched line's boundaries, in inches. Not valid as a top-level parameter for an Any match array, but valid for individual matches in the array. |
| maximumHeight | number                  | The maximum height of the matched line's boundaries, in inches. Not valid as a top-level parameter for an Any match array, but valid for individual matches in the array. |
| reverse       | boolean. default: false | Use with match arrays. Don't use with the first match in the array.<br/>  If true, searches for a match in lines that precede the previous match in the array. For example, in an array with matches A and B, if B is a First match with `"reverse":true`, then Sensible matches the first line that *precedes* the line matched by A. For a more detailed example, see [Match arrays](doc:match-arrays#reverse-match). |

Simple match
-------

Match using strings.  

**Parameters**

| key                  | values                                                  | description                                                  |
| -------------------- | ------------------------------------------------------- | ------------------------------------------------------------ |
| text  (**required**) | string                                                  | The string to match                                          |
| type (**required**)  | `equals`, `startsWith`, `endsWith`, `includes`          | `equals`: The matching line must equal the string<br/>`startsWith`: Match at beginning of line<br/>`endsWIth`: Match at end of line<br/>`includes`: Match anywhere in line |
| editDistance         | integer. the number of allowed edits for a fuzzy match. | Configure this parameter to allow *fuzzy*, or approximate, string matching. This is useful for OCR text, like poor-quality scans or handwriting. For example, if you configure 3, then Sensible matches `kitten` in the document for `sitting` in the Text parameter.  Sensible implements fuzzy matching using [Levenshtien distance](https://en.wikipedia.org/wiki/Levenshtein_distance). <br/>Sensible recommends avoiding setting this parameter on short matches, like "A:" or "Sub", because an edit distance as low as 2 on a short match can result in a large number of of line matches and impact performance. Generally, you increase edit distances values as you increase the length of the text match. See the Examples section for an example. |
| isCaseSensitive      | boolean. Default: false.                                | If true, match the string taking into account upper- and lower-case characters. |

**SYNTAX EXAMPLE**

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

For even simpler matching syntax in anchors, you can use `"anchor":"some string to match"`. For more information see [Anchor](doc:anchor).

**EDIT DISTANCE EXAMPLE**

The following example shows setting the Edit Distance parameter on a simple match for a poor-quality photographed document, so that the anchor  `6 City state and ZIP code` matches the incorrect OCR output of  `6 Chi state and ZIP code`. 



*Config*

```json
{
  "fields": [
    {
      "id": "simple_anchor",
    
      "anchor": {
        "match": {
          "editDistance": 3,
          "isCaseSensitive": false,
          "type": "startsWith",
          "text": "6 city state and zip code"
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

*Example document*
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/edit_distance.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/edit_distance.pdf) |
| ----------- | ------------------------------------------------------------ |



*Output*

```json
{
  "simple_anchor": {
    "type": "string",
    "value": "SomeCity, NJ, $70101"
  }
}
```



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

Match arrays
===

You can create complex matches by using any of the preceding match types in an array. For information, see [match arrays](doc:match-arrays).

