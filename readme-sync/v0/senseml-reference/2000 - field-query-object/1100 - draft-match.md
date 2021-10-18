---
title: "Match object"
hidden: false

---


Matches are instructions for matching lines of text in a document. They are valid elements in anchors and other objects. 

See the following sections for more information:

[**Match types**](doc:match#match-types)

- [Global parameters](doc:anchor#global-parameters)
- [Simple match](doc:anchor#simple-match)
- [Regex match](doc:anchor#regex-match)
- [First match](doc:anchor#first-match)
- [Any match](doc:match#any-match)

[**Examples**](doc:match#examples)

- [Match arrays](doc:match#match-arrays) 



Match types
===

Global Parameters
----

The following parameters are available to most types of Match objects:


| key           | values                  | description                                                  | Valid top-level param for Any match | Valid for matches *inside* Any array |
| ------------- | ----------------------- | ------------------------------------------------------------ | ----------------------------------- | ------------------------------------ |
| minimumHeight | number                  | The minimum height of the matched line's boundaries, in inches. | no                                  | yes                                  |
| maximumHeight | number                  | The maximum height of the matched line's boundaries, in inches. | no                                  | yes                                  |
| reverse       | boolean. default: false | If true, searches for a match in lines preceding either 1. the anchor or 2. the last-found match in a match array. For the full definition of "preceding", see [Line sorting](doc:lines#line-sorting). | yes                                 | no                                   |





