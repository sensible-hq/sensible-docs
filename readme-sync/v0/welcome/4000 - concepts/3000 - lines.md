---
title: "Lines"
hidden: false
---



A *line* is a rectangular region containing text.  Multiple lines  (shown as gray boxes) can exist at the same height on the page:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/line_concept.png)

 In other words, a line is set apart from other lines by any type of whitespace,  not just by newlines.


Line sorting
----

Lines are sorted primarily by their height on the page (their y-axis position) and secondarily by their left-to-right position (their x-axis position).

For example, this image shows which lines precede and succeed a target line:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/line_sort_1.png)

However, when text is slightly misaligned vertically (often the case with handwriting), line sorting is less intuitive. In the following image, a human reader may interpret the red line as succeeding the target line, but for Sensible it *precedes* the target line because it is higher on the page:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/line_sort_2.png)

To configure this default sorting behavior, see [the XMajorSort parameter](doc:method).

Line grouping
---

**Label method**

For the Label method, Sensible groups lines together using whitespace and x- and y-axis positions. Sometimes, Sensible's line groups are more restrictive than a human reader might expect. In particular, Sensible groups lines separated by vertical space only if they align at the *left* edge of each line boundary by default:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/line_grouping.png)

To capture multiple unaligned lines, use the Document Range method.
