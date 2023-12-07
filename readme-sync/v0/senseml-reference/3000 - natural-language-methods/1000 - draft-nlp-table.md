---
title: "NLP Table"
hidden: true
---


Parameters
====


| key               | value  | description                                                  |
| :---------------- | :----- | :----------------------------------------------------------- |
| pageSpanThreshold | object | Configure the Page Span Threshold parameter for multi-page table edge cases.<br/>By default, Sensible detects multi-page tables by checking if the table is near the top or bottom of the page. If it is, Sensible searches previous and succeeding pages for continuations of the table. This default behavior fails when intervening, non-table text introduces a large vertical space between a multi-page table and the top or bottom of a page. Examples of non-table text include footnotes and text box inserts. To allow for such large spaces, configure the following parameters:<br/>- `top`: number. default: 0.4. Sensible searches the previous page for a continuation of a multi-page table if the table starts in the top 40% of the page by. Change the percent using this parameter.<br/>-  `bottom`: number. default: 0.8. Sensible searches the next page for a continuation of a multi-page table if the table ends in the bottom 20% of the page. Change the percent using this parameter.<br/>Sensible continues merging the multi-page table until the Page Span Threshold conditions are no longer met, or until Sensible encounters LLM token limits. |
|                   |        |                                                              |
|                   |        |                                                              |
|                   |        |                                                              |
|                   |        |                                                              |
|                   |        |                                                              |
|                   |        |                                                              |
|                   |        |                                                              |
|                   |        |                                                              |
|                   |        |                                                              |


6. 