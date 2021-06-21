---
title: "Anchor object"
hidden: false
---
An *anchor* is a string, [Match](doc:anchor-object#section-match-object) object, or array of Match objects. Sensible searches first for a text "anchor" because it's a computationally quick and inexpensive way to narrow down the location in the document where you want to extract data. Then, Sensible can take action based on that location, such as using a ["method"](doc:method-object) to expand out from the anchor and grab the data you want.

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
|                      |                                        |                                                              |
| match (**required**) | Match object or array of match objects | See [Match object](doc:anchor-object#section-match-object).  |
| start                | string, Match, or Match array          | Defines a point in the document at which to start searching for  the`match` you define for the anchor.  By default not included in the anchor output. This parameter can be useful if you want to limit your search to a specific section of a document. For example, you can define a `start` that matches a section heading. <br/>Note that lines that "follow" the `start` line are most reliably those that are positioned *below* the start line. Lines to the left are not included, and lines to the right are only considered "following" if they are at exactly the same height as the `start` line on the page. In other words a line qualifies as "successive" to the `start` line first by its y-axis position and then by its x-axis position. |
| end                  | string, Match, or Match array          | Defines a point in the document at which to stop searching for  the`match` you define for the anchor.  By default not included in the anchor output. If unspecified, matches to end of document.  <br/>Note that lines that "precede" the `end` line are most reliably those that are positioned *above* the end line. Lines to the right are not included, and lines to the left are only considered "preceding" if they are at exactly the same height as the `end` line on the page. In other words, a line qualifies as "preceding" the `start` line first by its y-axis position and then by its x-axis position. |
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
        "start": "My section heading to start matching on",
        "end": "My footer text to stop matching on",
        "includeEnd": true,
        "match": 
          [
            {
              "type": "includes",
              "text": "Only finds anchor if you match this string in a line that is between the start and end lines (best to ensure start is above and end is below the text).",
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



Match object
====

Matches are instructions for matching lines of text in a document. They are valid elements in anchors and other objects. 

There are three different types of Match objects including simple, regex, and first matches.  The following parameters are available to all types of Match objects:



Global Match Parameters
----


| key           | values | description                                                  |
| ------------- | ------ | ------------------------------------------------------------ |
| minimumHeight | number | The minimum height of the matched line's boundaries, in inches. |
| maximumHeight | number | The maximum height of the matched line's boundaries, in inches. |



See the following sections for more information about each match type:

- [Simple matcher](doc:anchor-object#section-simple-match)
- [Regex match](doc:anchor-object#section-regex-match)
- [First match](doc:anchor-object#section-first-match)
- You can define match arrays. See [Match arrays](doc:anchor-object#section-match-arrays) 
- The *type* of method you use can determine whether text qualifies for a match or not. See [Methods influence matches](doc:anchor-object#section-methods-influence-matches).





Simple Match
-------

Match using strings.

**Parameters**

| key  | values                                         | description                                                  |
| ---- | ---------------------------------------------- | ------------------------------------------------------------ |
| text | string                                         | The string to match                                          |
| type | `equals`, `startsWith`, `endsWith`, `includes` | `equals`: The matching line must exactly contain the string<br/>`startsWith`: Match at beginning of line<br/>`endsWIth`: Match at end of line<br/>`includes`: Match anywhere in line |

**Examples**

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

Regex Match
-----

Match using a regular expression.

**Parameters**

| key                    | values                   | description                                                  |
| ---------------------- | ------------------------ | ------------------------------------------------------------ |
| pattern (**required**) | valid  JS regex          | Javascript-flavored regular expression. Capturing groups are not supported (see the [Regex method](doc:regex) instead).  Note you have to double escape characters, since the regex is contained in a JSON object (for example, `\\s` not `\s` to represent a whitespace character). |
| flags                  | JS-flavored regex flags. | Flags to apply to the regex. for example: "i" for case-insensitive, "g", "m", etc. |
| type (**required**)    | `regex`                  |                                                              |

**Examples**

For an example, see the [Passthrough method example](doc:passthrough).





First match
------

This is a convenience or utility match to find the first line encountered. 

**Parameters**

| key  | values  | description                                                  |
| ---- | ------- | ------------------------------------------------------------ |
| type | `first` | Matches the first line encountered, usually on a specified page. |

**Examples**

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

This example performs OCR only on a known page, which is useful since OCR is slow and computationally expensive. For example, some document types may have inserted scans on specific known pages, so you need to OCR only those pages and let Sensible perform direct text extraction on all other pages:

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

For an array of Match objects, all matches must be found to successfully create an anchor.  Each Match object must target a separate successive line. In other words, the second match starts its search in the line after the line matched by the first Match object in the array, and so on. 

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




Methods influence matches
-----

In addition to the conditions you set in the Match object itself (such as `isCaseSensitive`), the Method type you select in the `id` parameter influences whether text qualifies for the anchor match.

In other words, if you set a Label method, then only text that qualifies as a label matches in the anchor. If the text is too far away from any other lines to be used as a label, it won't match, even if all the conditions you set in the Match object itself are otherwise met. 

In the following example, the PDF contains two instances of the string "Python". Even though we set `"match":"last"` in the config, the config only matches the *first* instance of Python. Why? We set a `label` method, and only the first instance of Python is close enough to the text below it to qualify as a label for that text ( `"position":"below"`).

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/anchor_match_last_1.png)

 On the other hand, if we set the method to `row`, then both instances of "Python" qualify, and we successfully match the last instance:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/anchor_match_last_2.png)



