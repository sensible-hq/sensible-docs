---
title: "Page filter"
hidden: false
---



Filters out low-scoring pages given a bag of target terms and stop terms. 

Parameters
----


| key                    | value   | description                                                      |
| ---------------------- | ------ | ------------------------------------------------------------ |
| type (**required**) | string | "pageFilter"                                                 |
| terms (**required**) | array  | An array of terms to score positively (for example, `["number of buildings", "no. of buildings"]`). For more information about scoring, see [bag of words](doc:bag-of-words). |
| stopTerms            | array  | An array of terms to score negatively (for example, `["comparables"]`). For more information about scoring, see [bag of words](doc:bag-of-words). |
| maxPages             | number | The maximum number of highest-scoring pages to pass through the filter |

 



