---
title: "(Deprecated) Signature"
hidden: true
---
## Deprecated

This method is deprecated. [LLM-powered methods](doc:instruct) replace this method.

## Description

Returns true if more than 3% of the pixels in the specified region are dark.

| key              | value                                               | description                                                  |
| :--------------- | :-------------------------------------------------- | :----------------------------------------------------------- |
| id               | `signature`                                         |                                                              |
| start            | Direction, one of `above`, `below`, `left`, `right` | A direction specifying where to start relative to the anchor point. `right` starts at the middle of the right edge, `below` starts at the middle of the bottom edge, and so forth |
| offsetX          | number                                              | The offset in inches from the starting point along the X axis. Positive values offset to the right, negative values offset to the left. |
| offsetY          | number                                              | The offset in inches from the starting point along the Y axis. Positive values offset down the page, negative values offset up the page. |
| width            | number                                              | The width in inches of the extraction region                 |
| height           | number                                              | The height in inches of the extraction region                |
| isAbsoluteOffset | `true`, `false`                                     | optional, default false  A flag to make the offsets relative to the top left of the page rather than to the anchor start point |

