# Intro Rewrite Feedback — Residential Appraisal Draft

Source: `drafts/blog-residential-appraisal-reports.md`

## What was proposed (first attempt)

Replace the existing P2 ("With Sensible you can easily extract...") entirely with the new framing paragraph:

> Sensible handles this data extraction through a layout-specific config. Form 1004 reports are well suited to this approach: the form's field positions and label text are fixed by Fannie Mae and Freddie Mac specifications, giving reliable anchor points that deterministic methods extract precisely — no LLM calls, no prompt maintenance overhead. For non-standardized appraisal formats such as narrative appraisals or state-specific hybrid forms, a generalized LLM config handles extraction on day one without per-format configuration. Both run through the same API.

The old "With Sensible you can easily extract..." paragraph would have been deleted.

## What was accepted (user feedback)

User said: "I like the additions but I don't want to delete 'With Sensible you can easily extract key information...' and I want 'handles this...' to be 'handles this data extraction...'"

Final accepted structure — **three intro paragraphs**, not two:

**P2** (new framing paragraph, with "handles this data extraction" wording):
> Sensible handles this data extraction through a layout-specific config. Form 1004 reports are well suited to this approach: the form's field positions and label text are fixed by Fannie Mae and Freddie Mac specifications, giving reliable anchor points that deterministic methods extract precisely — no LLM calls, no prompt maintenance overhead. For non-standardized appraisal formats such as narrative appraisals or state-specific hybrid forms, a generalized LLM config handles extraction on day one without per-format configuration. Both run through the same API.

**P3** (old P2, kept unchanged):
> With Sensible you can easily extract key information out of residential appraisal report PDFs using SenseML, Sensible's query language for extracting data from documents. We've written a library of open-source SenseML configurations, so you don't need to write queries from scratch for common documents. From there, your residential appraisal report data is accessible via API, Sensible's UI, or 5,000 other software integrations thanks to Zapier.

## Template implication

`blog-post-template.md` should clarify:

1. The "Introduce Sensible" boilerplate paragraph ("With Sensible you can easily extract...") is **P3**, not replaced by the framing paragraph. The intro is a three-paragraph structure: P1 (describe the doc type) → P2 (framing paragraph) → P3 (introduce Sensible boilerplate).
2. The framing paragraph uses **"handles this data extraction"** (not "handles this") for the complementary-method sentence.
3. P3 is unchanged boilerplate — the framing paragraph is inserted between P1 and the existing P3, not in place of it.
