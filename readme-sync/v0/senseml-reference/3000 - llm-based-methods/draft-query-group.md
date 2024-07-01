---
title: "search summary"
hidden: true

---


|                       |                         |                                                              |
| --------------------- | ----------------------- | ------------------------------------------------------------ |
| searchBySummarization | boolean. default: false | Set this to true if Sensible isn't finding the answer to a propmt, or is finding it in the wrong part of the document as a false positive.<br/>If set to true, then Sensible changes its search behavior and the LLM model used as follows:<br/>This parameter is compatible with documents up to 1,280 pages long. <br/>[Beyond embeddings: Navigating the shift to completions-only RAG](https://www.sensible.so/blog/embeddings-vs-completions-only-rag) |
|                       |                         |                                                              |
|                       |                         |                                                              |

https://dev.sensible.so/editor/?d=summarizer_tests_fr&c=sum_pubmed&g=summarizer_pubmed



**HOW IT WORKS**

- Sensible prompts an LLM (by default TODO which one?) to summarize each page's content. (TODO: what if you specified a chnkSize = 0.5, would it then be summarizing each half page? and if so, would there be 2x as many summarizations, and maybe a token overflow problem at 1k pages?). The LLM returns summaries like:
- ```Page 8: This page defines several key terms related to a credit agreement. It includes definitions for "Adjusted Daily Simple SOFR," "Adjusted Term SOFR," "Administrative Agent," and "Administrative Agent Fee Letter. These terms are essential for understanding the roles, responsibilities, and financial metrics within the context of the credit agreement.` 

- Sensible prompts an LLM (todo? which one) with your `description` parameters and asks it to return the top page indices most likely to contain the answer to your question, based on the page summaries. (TODO: always ALL page summaries? evne if it's 1k page doc ie like 10k words of prompt?).  You can configure the number of page indices returned using the Chunk Count parameter. (todo: but what if it's a half page...)
  - Sensible prompts an LLM (todo? which one?) to answer the questions in your `description` parameters using the full page text of the top pages as context. (or is it the full chunk text?) 

EFFECTS on other parameters:

- chunkSize: default is 1, overrides the method's default.
- chunkCount: default is  5  overriding the default of 5 (right? and what would happen if yo uconfigred a different one? **is it not configurable seems like it's not?**?)
- 

paramaeters that get ignored:

- Chunk Scoring Text parameter
- Multimodal Engine parameter
- chunkOverlapPercentate: it's set to 0 no matter what you do I'm guessing

unaffected/normal behavior:

- Confidence Signals
- Context Descrripton
- Page Hinting (TODO: i'm guessing this would get used in the 'top page indices' call but not the 'full text context' call?)
- Page Range -- could you use this for token overflow problems in large documents?

QUESTIONS:

` gpt-4o ` vs  `gpt-3.5-turbo-0125` 

RELEVANT VS IRRELEVANT params:

Sensible feeds the pages to a second prompt asking for the 'top ten page indices' (QUESTION: what happens in a 200+ page document when each page is summary is 100 words? what happens in a token overflow situation, what error message is returned?) 

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

1. 