---
title: "Matcher"
hidden: false
---
Matchers are Instructions for matching lines of text in a document. There are three different types of Matches: SimpleMatcher, RegexMatcher, and FirstMatcher. 

 `SimpleMatcher`: Match using strings 
[block:parameters]
{
  "data": {
    "h-0": "key",
    "h-1": "values",
    "h-2": "description",
    "0-0": "text",
    "0-1": "any string",
    "0-2": "The string to match",
    "1-0": "type",
    "1-1": "`equals`, `startsWith`, `endsWith`, `includes`",
    "1-2": "`equals`: Exact match\n`startsWith`: Match at beginning of line\n`endsWIth`: Match at end of line\n`includes`: Match anywhere in line"
  },
  "cols": 3,
  "rows": 2
}
[/block]
`RegexMatcher`: Match using a regex
[block:parameters]
{
  "data": {
    "h-0": "key",
    "h-1": "values",
    "h-2": "description",
    "0-0": "pattern",
    "0-2": "String representation (fully escaped) of the regex pattern",
    "0-1": "valid regex",
    "1-0": "flags",
    "1-1": "regex flags, for example: `\"i\"`, `\"g\"`, `\"m\"`",
    "1-2": "Regex flags (e.g., `\"i\"` for case-insensitive regex matching)",
    "2-0": "type",
    "2-1": "`regex`"
  },
  "cols": 3,
  "rows": 3
}
[/block]
`FirstMatcher`: Utility matcher to just match the first line encountered. Useful in conjunction with, e.g., the `pageFilter` preprocessor
[block:parameters]
{
  "data": {
    "h-0": "key",
    "h-1": "values",
    "h-2": "description",
    "0-0": "type",
    "0-1": "`first`"
  },
  "cols": 3,
  "rows": 1
}
[/block]