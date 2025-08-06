---
title: "Match object"
hidden: false

---


Matches are search criteria for matching lines of text in a document. They're valid elements in anchors and other objects. 

See the following sections for more information:

[**Match types**](doc:match#match-types)

- [Global parameters](doc:match#global-parameters)
- [String match](doc:match#simple-match)
- [Regex match](doc:match#regex-match)
- [First match](doc:match#first-match)
- [Boolean matches](doc:match#boolean-matches)
- [Repeat match](doc:match#repeat-match)

[**Match arrays**](doc:match#match-arrays)


Match types
===

Global parameters
----

The following parameters are available to most* types of Match objects. 


| key           | values                  | description                                                  |
| ------------- | ----------------------- | ------------------------------------------------------------ |
| minimumHeight | number                  | The minimum height of the matched line's boundaries, in inches. |
| maximumHeight | number                  | The maximum height of the matched line's boundaries, in inches. |
| reverse       | boolean. default: false | Use in match arrays. Don't set this to true for the first match in the array, except in the External Range parameter for [sections](doc:sections).<br/>  If true, searches for a match in lines that precede the previous match in the array. For example, in an array with matches A and B, if B is a First match with `"reverse":true`, then Sensible matches the first line that *precedes* the line matched by A. For an example, see [Match arrays](doc:match-arrays#reverse-match). |
| xRangeFilter  | object                  | Defines a left-to-right range, or "column", in which to search for a match. This option excludes lines that partially fall outside the column.  Contains the following parameters:<br/>`minX` Specifies the left boundary of the range, in inches from the left edge of the page.<br/>`maxX` Specifies the right boundary of the range, in inches from the left edge of the page. |

*These parameters aren't available as top-level parameters for a Boolean match.

String match
-------

Match using strings.  

**Parameters**

| key                  | values                                                  | description                                                  |
| -------------------- | ------------------------------------------------------- | ------------------------------------------------------------ |
| text  (**required**) | string                                                  | The string to match                                          |
| type (**required**)  | `equals`, `startsWith`, `endsWith`, `includes`          | `equals`: The matching line must equal the string<br/>`startsWith`: Match at beginning of line<br/>`endsWIth`: Match at end of line<br/>`includes`: Match anywhere in line |
| editDistance         | integer. the number of allowed edits for a fuzzy match. | Configure this parameter to allow *fuzzy*, or approximate, string matching. This is useful for OCR text, like poor-quality scans or handwriting. For example, if you configure 3, then Sensible matches `kitten` in the document for `sitting` in the Text parameter.  Sensible implements fuzzy matching using [Levenshtien distance](https://en.wikipedia.org/wiki/Levenshtein_distance). <br/>Sensible recommends avoiding setting this parameter on short matches, like "A:" or "Sub", because an edit distance as low as 2 on a short match can result in a large number of line matches and impact performance. Generally, you increase edit distances values as you increase the length of the text match. See the Examples section for an example. |
| isCaseSensitive      | boolean. Default: false.                                | If true, match the string taking into account upper- and lower-case characters. |

**SYNTAX EXAMPLE**

The following config uses a string match:

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

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/edit_distance.pdf) |
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
| pattern (**required**) | valid  JS regex          | Javascript-flavored regular expression. This parameter doesn't support capturing groups. See the [Regex method](doc:regex) instead.<br/>Double escape special characters since the regex is in a JSON object. For example, `\\s`, not `\s` , to represent a whitespace character.<br/>Sensible throws an error if you specify a pattern that can match an empty string, for example, `.*`. |
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


```json
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

Boolean matches
---

Use Boolean matches to write Boolean logic about your matches.  For example, use the Any match to match an array of synonymous terms if a document contains small wording variations across revisions.

**Parameters**

| key                                        | values                                                       | description                                                  |
| ------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| type (**required**)                        | `any`, `all`, `not`                                          | `any` : Same behavior as Boolean operator "or". Finds a line that meets any of the match conditions in the array.<br/>`all` Same behavior as  Boolean operator "and". Finds a line that meets all of the match conditions in the array.<br/>`not` Same behavior as Boolean operator "not". Finds a line if it doesn't meet the match condition.<br/> |
| matches (**required** for `any` and `all`) | Array of Match objects.  All match types are valid in the array except `first` | Use with `any` and `all`. You can nest Boolean matches using this parameter. |
| match (**required** for `not`)             | Match object. All match types are valid except `first`       | Use with `not`                                               |

**EXAMPLE**

*Config*

```json
{
  "fields": [
    {
      "id": "test_boolean_matches",
      /* to show matching behavior, output all matching
         anchor lines, not just the first match */
      "match": "all",
      "method": {
        /* to show matching behavior, use passthrough
           to output anchor text
           */
        "id": "passthrough"
      },
      "anchor": {
        "match": [
          {
            /* match a line if meets the conditions
               of ANY of the following array of matches */
            "type": "any",
            "matches": [
              /* match a line that includes "special"  */
              {
                "type": "includes",
                "text": "special"
              },
              /* match a line that meets ALL of the conditions:
                 it includes "header" 
                 but NOT "should not" */
              {
                "type": "all",
                "matches": [
                  {
                    "type": "includes",
                    "text": "header"
                  },
                    /* note that "not"  */
                  {
                    "type": "not",
                    "match": {
                      "type": "includes",
                      "text": "should not"
                    }
                  }
                ]
              }
            ]
          }
        ]
      }
    }
  ]
}
```
*Example document*
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/boolean_match.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/boolean_match.pdf) |
| ----------- | ------------------------------------------------------------ |



*Output*

```json
{
  "test_boolean_matches": [
    {
      "type": "string",
      "value": "This is a header."
    },
    {
      "type": "string",
      "value": "This is a special line."
    }
  ]
}
```

## Repeat match

Finds the nth occurrence of a Match object. This is a more concise syntactical alternative to a [match array](doc:match-arrays).

**Parameters**

| key                  | values       | description                                                  |
| -------------------- | ------------ | ------------------------------------------------------------ |
| type (**required**)  | `repeat`     |                                                              |
| times (**required**) | integer      | The number of times the specified match must occur in [succeeding](doc:lines#line-sorting) lines.  For example, if you specify 3, matches the third occurrence of the specified match. |
| match                | Match object | The Match object to find each succeeding line.               |

**EXAMPLE**

The following example shows matching the fifth occurrence of the string "customer account".

*Config*

```json
{
  "fields": [
    
    {
      "id": "repeat_match_test",
      "anchor": {
        "match": [
          {
            /* match the 5th line that starts with "customer account" */
            "type": "repeat",
            "times": 5,
            "match": { "type": "startsWith", "text": "customer account" }
          }
        ]
      },
      "method": { "id": "passthrough" }
    },
  ]
}

```

Sensible automatically expands this match syntax as follows:

```json
      "anchor": {
        "match": [
          { "type": "startsWith", "text": "customer account" },
          { "type": "startsWith", "text": "customer account" },
          { "type": "startsWith", "text": "customer account" },
          { "type": "startsWith", "text": "customer account" },
          { "type": "startsWith", "text": "customer account" },
         
        ]  
      }
```



*Example document*

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/repeat_match.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/repeat_match.pdf) |
| ---------------- | ------------------------------------------------------------ |

*Output*

```json
{
  "repeat_match_test": {
    "type": "string",
    "value": "Customer account # 5 - 98765"
  }
}
```



Match arrays
===

You can create complex matches by using any of the preceding match types in an array. For information, see [match arrays](doc:match-arrays).

