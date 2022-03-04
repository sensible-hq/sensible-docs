---
title: "Match object"
hidden: true

---




|      |      |      |
| ---- | ---- | ---- |
|      |      |      |
|      |      |      |
|      |      |      |



Simple match
-------

Match using strings.  

**Parameters**

| key                  | values                                                  | description                                                  |
| -------------------- | ------------------------------------------------------- | ------------------------------------------------------------ |
| text  (**required**) | string                                                  | The string to match                                          |
| type (**required**)  | `equals`, `startsWith`, `endsWith`, `includes`          | `equals`: The matching line must equal the string<br/>`startsWith`: Match at beginning of line<br/>`endsWIth`: Match at end of line<br/>`includes`: Match anywhere in line |
| editDistance         | integer. the number of allowed edits for a fuzzy match. | Configure this parameter to allow *fuzzy*, or approximate, string matching. This is especially useful for OCR text, like scanned documents or handwriting. For example, if you configure 3, then Sensible matches `kitten` in the document for `sitting` in the Text parameter.  Sensible implements fuzzy matching using [Levenshtien distance](https://en.wikipedia.org/wiki/Levenshtein_distance). |







