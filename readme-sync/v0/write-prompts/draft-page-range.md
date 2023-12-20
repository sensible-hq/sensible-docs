---
title: "draft page range"
hidden: true
---

| SenseML parameter | value  | config-level description:<br/>configure in [NLP preprocessor](doc:nlp) or in Sensible Instruct configuration settings | method-level description:<br/>configure in a field   |
| :---------------- | :----- | ------------------------------------------------------------ | ---------------------------------------------------- |
| pageRange         | object | Configures the context's location in the document. For details about context and chunks, see the Notes section.<br/>If specified, Sensible creates chunks only in the specified page range and ignores all other pages. Note that Sensible ignores the page range when searching for a field's anchor.<br/>For example, use this parameter to improve performance, or to avoid returning unwanted matches if your prompt has multiple candidate answers.<br/>Contains the following parameters: <br/>`startPage`: number. The zero-based index of the start page. <br/>`endPage`: number. The zero-based index of the end page. | Overrides config-level parameter for a single field. |

TODOs:

- add xlink in NLP preprocessor.
- add to the key/description at ROW D.
- add xlink to each individual method.. OR! add a section for 'global params' ??? so I dont' ahve to do individual entries anymore?? could do for NLP preprocessor as well.. o wait no i can't because sometimes defaults vary?!?!
- how does this interact w/ anchor? "which is already working"???