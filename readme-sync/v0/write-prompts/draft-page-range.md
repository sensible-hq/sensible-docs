---
title: "draft page range"
hidden: true
---

| SenseML parameter | value  | config-level description:<br/>configure in [NLP preprocessor](doc:nlp) or in Sensible Instruct configuration settings | method-level description:<br/>configure in a field   |
| :---------------- | :----- | ------------------------------------------------------------ | ---------------------------------------------------- |
| pageRange         | object | Configures the context's range in the document. For details about context and chunks, see the Notes section.<br/>If specified, Sensible creates chunks in the specified page range and ignores other pages.<br/>Contains the following parameters: <br/>`startPage`:  Zero-based index of the first page to include. <br/>`endPage`: Zero-based index of the last page to include.<br/><br/>**Note:** Sensible ignores this parameter when searching for a field's anchor. If you want to affect the field's anchor as well as set the page range for all methods instead of solely LLM-based methods, use the [Page Range](doc:page-range) preprocessor instead.<br/>For example, use this parameter to improve performance, or to avoid returning unwanted matches if your prompt has multiple candidate answers.<br/> | Overrides config-level parameter for a single field. |

TODOs on publish:

- add xlink in NLP preprocessor.

- add to the key/description at ROW D on Prompt page -- "context location or context range or context scope?".

- add xlink to each individual method ref topic

  