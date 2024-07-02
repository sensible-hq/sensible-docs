---
title: "search summary"
hidden: true
---


|                       |                         |                                                              |
| --------------------: | ----------------------- | ------------------------------------------------------------ |
| searchBySummarization | boolean. default: false | Set this to true if Sensible isn't finding the answer to a propmt, or is finding it in the wrong part of the document as a false positive.<br/>If set to true, then Sensible changes its search behavior and the LLM model used as follows:<br/>This parameter is compatible with documents up to 1,280 pages long. <br/>[Beyond embeddings: Navigating the shift to completions-only RAG](https://www.sensible.so/blog/embeddings-vs-completions-only-rag) |
|                       |                         |                                                              |
|                       |                         |                                                              |

https://dev.sensible.so/editor/?d=summarizer_tests_fr&c=sum_pubmed&g=summarizer_pubmed

**tash**

whatever chunking you select, that's how the summarization is created, so yeah, summarizes on half pages, but if

- 1 page chunk with 0 overlap is the only thing that we recommend...flexibility vs decide for them...
- 'page indice'





**HOW IT WORKS**

- Sensible prompts an LLM (by default TODO which one?) to summarize each chunk content. ( maybe a token overflow problem at 1k pages?). The LLM returns summaries like:
- ```Page 8: This page defines several key terms related to a credit agreement. It includes definitions for "Adjusted Daily Simple SOFR," "Adjusted Term SOFR," "Administrative Agent," and "Administrative Agent Fee Letter. These terms are essential for understanding the roles, responsibilities, and financial metrics within the context of the credit agreement.` 

- Sensible prompts an LLM (todo? which one) with your `description` parameters and asks it to return the top chunk indices most likely to contain the answer to your question, based on the summaries.  KEEP the chunkCount configurability YES TASH likes the configurability.
  -    (TODO: always ALL page summaries? evne if it's 1k page doc ie like 10k words of prompt?).  You can configure the number of page indices returned using the Chunk Count parameter. (todo: but what if it's a half page...) ... it would have a different set of zero-indexed page numbers even if you turn off Page Hinting ... 
  - 10 and over is too large... then we start dropping chunks if we hit token overflow limits

- Sensible prompts an LLM (todo? which one?) to answer the questions in your `description` parameters using the full page text of the top pages as context. (or is it the full chunk text?) 



**summarizing a half page isn't cool; he wishes it were only by the whole page**



EFFECTS on other parameters:

- chunkSize: default is 1, overrides the method's default.
- chunkCount: default is  5  overriding the default of 5 (right? and what would happen if yo uconfigred a different one? **is it not configurable seems like it's not?**?)
- 

paramaeters that get ignored:

- Chunk Scoring Text parameter -ignored
- Multimodal Engine parameter IS TRUE:
  - anchor: no search either embedding or summarization
  - no anchor -- you just have to include other queries in the group that are colocated with the image b/c no chunk scoring parameter 


could do something:

​	-chunkOverlapPercentate: It SHOULD Be ignored but isn't in practice. MUST BE set to 0 (tash to talk to Tony)



unaffected/normal behavior:

- Confidence Signals
- Context Description
- Page Hinting (TODO: i'm guessing this would get used in the 'top page indices' call but not the 'full text context' call?) - Tash: yeah can effect the the 'best pages' , but yes in final prompt potentially. ... YEAH, you could mess up chunks vs page indices if you set half-page chunks ... but if you restrict it to full pages then it solves the problems ... but even if full page restrictions, it doesn't seem great ... could we deprecate it? 
- Page Range -- yeah, it's not gonna summarize anything outside the page range. 



QUESTIONS: 

- summarization:  `gpt-3.5-turbo-0125` (not config now)

- scoring the summarizations:` gpt-4o `  has 128k token limit     (not config now)

- prompt + real context (answering):  answer depends on your LLM_engine (3.5 or anthropic) RIGHT now but eventually maybe it will affect the summarization and scoring down the line? 

RELEVANT VS IRRELEVANT params:

Sensible feeds the pages to a second prompt asking for the 'top ten page indices' (QUESTION: what happens in a 200+ page document when each page is summary is 100 words? what happens in a token overflow situation, what error message is returned?) 

1. QUESTION: 

2. TURN OFF chunkSize - default is 1, can be either 0.5 or 1 (which is global yeah)

3. chunkCount  - relevant???? seems to be

4. TURN OFF chunkOverlapPercentage - expect n/a... yeah it's 0

5. pageRange - expect applicable

6. TURN OFF: chunkScoringText - expect N/A

7. multimodalEngine - expect N/A

8. confidenceSignals - ??

9. contextDescription - expect applicable

10. pageHinting - expect applicable???

    