---
title: "Page filter"
hidden: false
---



Filters out low-scoring pages given a bag of target terms and stop terms. 

Parameters
----


| key                    | value   | description                                                      |
| ---------------------- | ------ | ------------------------------------------------------------ |
| `type` (**required**)  | string | "pageFilter"                                                 |
| `terms` (**required**) | array  | An array of strings with terms to score positively (e.g., `["number of buildings", "no. of buildings"]`) |
| `stopTerms`            | array  | An array of strings with terms to score negatively (e.g., `["comparables"]`) |
| `maxPages`             | number | The maximum number of highest-scoring pages to pass through the filter |

 



