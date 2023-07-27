---
title: "Query"
hidden: true

---

TODO: in query tips, be sure to include a tip about checking the location buton (click "location" next to blah to see the source text) in the "troubleshooting" section, as a sister bullet to the "see confidence signals"? --> and then link out to the 'how it works + limitations' that goes in the query SenseML reference itself

Notes
===

**How Query method works**

For an overview of how this method works, see the following steps:



**How Location highlighting works**

In the Sensible Instruct editor, you can click the output of a query field to view its source text in the document. 

TODO: IMAGE:

For an overview of how Sensible finds the source text in the document on which the LLM based its response to the prompt, see the following steps:

- The LLM returns a response to your prompt.

- Sensible searches in the source document for a line that's a fuzzy match to the response.  For example, if the LLM returns `4387-09-22-33`, Sensible matches the line `Policy Number: 4387-09-22-33` in the document. Sensible implements fuzzy matching using [Levenshtien distance](https://en.wikipedia.org/wiki/Levenshtein_distance).

- Sensible selects the three lines in the document that contain the best fuzzy matches. For each line, Sensible concatenates the preceding and succeeding lines, in case the match spans multiple lines.
- Sensible searches for a fuzzy match in the concatenated lines for the text that the LLM returned.  Sensible returns the best match.
- Sensible highlights the best match in the PDF document in the Sensible Instruct editor or in the SenseML editor.

**Limitations**

Sensible can highlight the incorrect location in the following circumstances:

- If you prompt the LLM to reformat the source text in the document or reformat the text using a [type](doc:types) , then Sensible can fail to find a match or find an inaccurate match.

- If there are multiple candidates fuzzy matches in the document (for example, two instances of `April 7`), Sensible chooses the top-scoring match regardless of its location in the document. Sensible doesn't use page location data to find the match.

- If the LLM returns text that's not in the document, then Sensible can't match that.

  
