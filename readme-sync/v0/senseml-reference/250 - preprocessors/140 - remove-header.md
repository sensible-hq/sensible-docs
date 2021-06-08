---
title: "Remove header"
hidden: false
---


Removes repeated elements at the start of pages in the document. These elements are ignored in the direct text extraction of the page.   

Parameters
----

| key            | value   | description                                                      |
| -------------- | ------ | ------------------------------------------------------------ |
| type (**required**) | `removeHeader` | To recognize a footer, this preprocessor starts at the bottom of the page and moves up the page, stopping as soon as it finds a nonrepeating element.  Page number increments are ignored.   For an example, see the Examples section. |
| startsOnPage | integer. default: 1 | The first page number on which to start checking for repeated elements.  Note this is the page *number* not  the page's zero-based index in the pages array. <br/> |

