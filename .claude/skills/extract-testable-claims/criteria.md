# Criteria: a claim worth testing

A claim is worth testing when it states **specific Sensible behavior that a config author would rely on, and that a test extraction or a config publish could confirm or contradict**.

It usually falls in one of these kinds:

| kind | examples |
| ---- | -------- |
| default | "default: 0", "If unspecified, defaults to `first`." |
| type or shape | "Match object or Match array", "integer", accepted enum values |
| required | "required unless you specify the Page Lines Limit parameter" |
| compatibility | "You can combine this parameter only with the Engine parameter." |
| empty, null, or missing input | "If you specify an empty array, Sensible OCRs nothing.", "Returns null if the anchor isn't present." |
| scope and order | "OCRs every page", "matches the first", "runs before other preprocessors" |
| restriction | file types, page limits, size limits |
| output | the Output block, output shape or types |

It isn't worth testing when it:

- recommends or advises ("Sensible recommends…", "Use this parameter to…", "Choose text that…");
- defines a term or describes a concept without stating behavior;
- describes the example document ("In the example document, the table is a screenshot.");
- points elsewhere ("For more information, see…");
- generalizes about the world, not Sensible.

A sentence can hold several claims. Split it so each claim states one behavior.

The question Jev answers about each claim (`score_claims.py` sends this text):

> Does the marked claim state specific Sensible behavior that someone writing a SenseML config would rely on, and that running an extraction or publishing a config could confirm or contradict, such as a default value, an accepted value type, whether a parameter is required, which parameters it can be combined with, what happens with null, empty, or missing input, which pages or matches it applies to, or what the output contains? Answer no for advice, recommendations, definitions, descriptions of an example document, and pointers to other pages.
