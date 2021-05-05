---
title: "PageMatcher"
slug: "pagematcher-1"
hidden: false
createdAt: "2021-05-05T20:51:48.063Z"
updatedAt: "2021-05-05T20:51:48.063Z"
---
Instructions for matching a page with a bag of words. Will resolve to the first line on the matched page
[block:parameters]
{
  "data": {
    "h-0": "key",
    "h-1": "possible values",
    "h-2": "description",
    "0-0": "terms",
    "0-2": "an array of strings with terms to score positively",
    "1-0": "stopTerms",
    "1-2": "optional. An array of strings with terms to score negatively",
    "0-1": "e.g: `[\"qty\", \"quantity\", \"ordered\", \"shipped\", \"ord\"]`",
    "1-1": "e.g: `[\"price\"]`"
  },
  "cols": 3,
  "rows": 2
}
[/block]