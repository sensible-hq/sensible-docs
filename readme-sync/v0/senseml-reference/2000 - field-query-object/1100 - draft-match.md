---
title: "Match object"
hidden: true

---

Matches are instructions for matching lines of text in a document. They're  valid elements in anchors and other objects. 



See the following sections for more information:

[**Match types**](doc:match#match-types)

- [Global parameters](doc:anchor#global-parameters)
- [Simple match](doc:anchor#simple-match)
- [Regex match](doc:anchor#regex-match)
- [First match](doc:anchor#first-match)
- [Any match](doc:match#any-match)

- 



Match types
===

Global parameters
----

The following parameters are available to most types of Match objects:


| key           | values | description                                                  |
| ------------- | ------ | ------------------------------------------------------------ |
| minimumHeight | number | The minimum height of the matched line's boundaries, in inches. Not valid as a top-level parameter for an Any match, but valid for individual matches in the Any match. |
| maximumHeight | number | The maximum height of the matched line's boundaries, in inches.  Not valid as a top-level parameter for an Any match, but valid for individual matches in the Any match. |
|               |        |                                                              |

