---
title: "Remove page"
hidden: true
---

TODO: add to index

Removes pages that match the specified text. 

Parameters
----


| key                  | value              | description                                                  |
| -------------------- | ------------------ | ------------------------------------------------------------ |
| type (**required**)  | string             | "pageFilter"                                                 |
| match (**required**) | Match object       | Sensible removes each pages that contain this match. **questions: what if there were a match array, where item 0 matches page 2 and item 1 matches page 3 -- would we remove page 3? or would you have to have everything in the array be on the same page, then use a pageOffset?  **  To remove a single page offset from the first page of the document, rather than offset from matched text,` specify `"match": { "type": "first" }`. |
| matchAll             | boolean            | If true, removes all pages containing the line specified by the Match parameter. |
| pageOffset           | number. default: 0 | The zero-indexed number of the page to remove, counting from the page number of the text matched by the Match parameter. |

 ## Examples

2do/todo