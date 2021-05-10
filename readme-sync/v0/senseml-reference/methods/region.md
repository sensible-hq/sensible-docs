---
title: "Region"
hidden: false
---
Return lines within a given document region, defined in inches as a bounding box

| id                                                           | value                                       | description                                                  |
| ------------------------------------------------------------ | ------------------------------------------- | ------------------------------------------------------------ |
| id                                                           | region                                      |                                                              |
| start                                                        | Direction, either above, below, left, right | A Direction specifying where to start relative to the anchor point. right starts at the middle of the right edge, below starts at the middle of the bottom edge, and so forth |
| offsetX                                                      | number                                      | The offset in inches from the starting point along the X axis |
| offsetY                                                      | number                                      | The offset in inches from the starting point along the Y axis |
| width                                                        | number                                      | The width in inches of the extraction region                 |
| height                                                       | number                                      | The height in inches of the extraction region                |
| isAbsoluteOffset                                             | true, false                                 | optional, default: false                                     |
| A flag to make the offsets relative to the top left of the page rather than to the anchor start point |                                             |                                                              |