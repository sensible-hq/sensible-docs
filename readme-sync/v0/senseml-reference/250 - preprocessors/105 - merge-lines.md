---
title: "Ligature"
hidden: false
---


Merges nearby lines more aggressively than the built-in line merger

Parameters
----

|                                            |        |                                                              |
| ------------------------------------------ | ------ | ------------------------------------------------------------ |
| key                                        | type   | comment                                                      |
| `type` (**required**)                      | string | "mergeLines"                                                 |
| `directlyAdjacentThreshold` (**required**) | number | Fraction of line height under which two adjacent lines (i.e., horizontally distributed along an x-axis) are merged without a space. For example, at 0.15 two lines are merged without a space in between their contents when they are less than 15% of the line height apart from one another. |
| `adjacentThreshold` (**required**)         | number | Identical to the above, but for mergers with a space in between. |
| `yOverlapThreshold`                        | number | Y overlap is the portion of the joint y-axis range of two lines that is occupied by both lines. For example, if two lines share the same minimum and maximum y-axis values, they will have an overlap of 1. If one line’s extent is from 0 to 10 and the other line’s extent is from 2 to 12 on the y-axis, they will have an overlap of .667 (8 / 12). The yOverlapThreshold is the y overlap above which mergeLines will merge two adjacent lines |
| `minXGapThreshold`                         | number |                                                              |

