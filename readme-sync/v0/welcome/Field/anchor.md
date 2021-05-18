---
title: "Anchor"
hidden: true
---
An *anchor* is a string, Match object, or array of match objects. 

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

**Anchor parameters**

| key                  | values                                 | description                                                  |
| -------------------- | -------------------------------------- | ------------------------------------------------------------ |
|                      |                                        |                                                              |
| match (**required**) | Match object or array of match objects | See following section                                        |
| start                | string, Match, or Match array          | Defines a point in the document at which to start searching for  the`match` you define for the anchor.  By default not included in the anchor output. This parameter can be useful if you want to limit your search to a specific section of a document. For example, you can define a `start` that matches a section heading. |
| end                  | string, Match, or Match array          | Defines a point in the document at which to stop searching for  the`match` you define for the anchor.  By default not included in the anchor output. If unspecified, matches to end of document. |
| includeEnd           | boolean                                | Specifies whether to include the text that matches the `end` parameter in the anchor output. |

**Examples**

Here's an example of an Anchor object that uses all these parameters. Its `match` parameter includes an array of Match objects:

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
              "text": "Only match if you find this string in a line...",
            },
            {
              "type": "startsWith",
              "text": "...Followed by the 1st occurence of this string in another line",
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

Matches are instructions for matching lines of text in a document. They are valid elements in anchors. There are three different types of Matches object:

- Simple matcher
- Regex match
- First matcher

For an array of Match objects, all matches must be found to successfully create an anchor.

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

| key                    | values                                                       | description                                                  |
| ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| pattern (**required**) | valid regex                                                  | Javascript-flavored regular expression. Capturing groups are not supported (see the (Regex method)(doc:regex) instead).  Note you have to double escape characters, since the regex is contained in a JSON object (for example, `\\s` not `\s` to represent a whitespace character). |
| flags                  | JS-flavored regex flags, for example: "i", "g", "m"Flags to apply to the regex. for example: "i" for case-insensitive, "g", "m", etc. \| |                                                              |
| type (**required**)    | `regex`                                                      |                                                              |

**Examples**

First match
------

This is a convenience or utility match to  just match the first line encountered. Useful in conjunction with the `pageFilter` preprocessor.

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

This example performs OCR only on a known page (for example, some PDFs may have inserted scans on specific pages, so you need to OCR only those pages and let Sensible perform direct text extraction on all other pages):

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

