---
title: "Types"
hidden: true

---

**Formats recognized** 

Sensible recognizes paragraphs separated by vertical gaps, or "paragraph breaks." 

Sensible detects paragraph breaks when the vertical gap between two output lines is larger than 40% of the font height of the lower output line. Sensible never detects paragraph breaks at the end of a page. Sensible don't use paragraph margins, for example indentations, to detect paragraph breaks.



**Parameters**

| key                             | value                   | description                                                  |
| ------------------------------- | ----------------------- | ------------------------------------------------------------ |
| id (**required**)               | `paragraph`             |                                                              |
| annotateSuperscriptAndSubscript | Boolean. default: false | When true, Sensible annotates subscript and superscript text with `[^...]` and `[_...]`, respectively. |
| allNewlines                     | Boolean. default: false | When true, Sensible inserts a newline (`\n`) in the output for every line break in the document text, and two newlines (`\n\n`), for every paragraph break.<br/>When false, Sensible inserts a newline for every paragraph break.<br/>For more information about how Sensible detects paragraph breaks, see the preceding **Formats recognized** section. |

