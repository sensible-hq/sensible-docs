---
title: "Query"
hidden: true

---

TODO: in query tips, be sure to include a tip about checking the location buton (click "location" next to blah to see the source text) in the "troubleshooting" section, as a sister bullet to the "see confidence signals"?



Notes
===

**How Query method works**

For an overview of how this method works, see the following steps:



**How Location highlighting works**



For an overview of how Sensible finds the source text in the document on which the LLM based its response to the prompt, see the following steps:

- Sensible searches for a fuzzy match in the document to the response from the LLM . Sensible implements fuzzy matching using [Levenshtien distance](https://en.wikipedia.org/wiki/Levenshtein_distance).  For example, if the LLM returns `Apr 7th`, Sensible matches `April 7` in the document. (TODO confirm if true?)

- Sensible take the top 3 matches from the fuzzy match and then searches in both direction of these lines to see if the answer spans multiple lines.
- Sensible then takes  the 3 complete multi-line candidate answers to the `answer` and return the best matching one.
- Sensible shows the best match in the PDF document in the Sensible Instruct editor or in the SenseML editor.

**Troulbeshooting location highlighting**

can't find:

- what if you ask it to reformat the date or watheer 
- edit distance stuff for the fuzzy matching -- LIKE that but the starting point doesn't have to be hte start of the line .. additions of all the other characters ... edit distance not the same ... 
- LLM reformatted it
- stuf IN the doc
- document metadata like its wordcount
- takes the closest match ---> takes all c --> so might be the wrong source 
April vs APR -- > might match do a different date 
