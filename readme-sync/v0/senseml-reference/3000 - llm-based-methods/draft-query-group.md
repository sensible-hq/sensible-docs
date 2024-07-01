|                       |                         |                                                              |
| --------------------- | ----------------------- | ------------------------------------------------------------ |
| searchBySummarization | boolean. default: false | Set this to true if Sensible isn't finding the answer to a propmt, or is finding it in the wrong part of the document as a false positive.<br/>If set to true, then Sensible changes its search behavior and the LLM model used as follows:<br/> |
|                       |                         |                                                              |
|                       |                         |                                                              |



**HOW IT WORKS**

1. Sensible prompts an LLM to summarize each page's content **in a batch of page ranges that overlaps by 1 page with tpervious batch** default batch is 7p, no need to mention thatup to 28 page batch? total page limit of x = 1280  for picking top chunks with summarization using gpt-4o
2. Sensible feeds the pages to a second propmt asking for the 'top ten page indices' (QUESTION: what happens in a 200+ page document when each page is summary is 100 words? what happens in a token overflow situation, what error message is returned?) 
   1. QUESTION: 
   2.  chunkSize - default is 1, can be either 0.5 or 1 (which is global yeah)
   3. chunkCount  - relevant???? seems to be
   4. chunkOverlapPercentage - expect n/a... yeah it's 0
   5. pageRange - expect applicable
   6. chunkScoringText - expect N/A
   7. multimodalEngine - expect N/A
   8. confidenceSignals - ??
   9. contextDescription - expect applicable
   10. pageHinting - expect applicable???
   11. 
3. 