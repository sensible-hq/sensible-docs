# Intro Rewrite Feedback — Residential Appraisal Draft

Source: `drafts/blog-residential-appraisal-reports.md`

## Final accepted intro (use this as the template example)

> If you're building software for mortgage lending or real estate finance, chances are you've encountered the residential appraisal report, also known as Form 1004. A Form 1004 is the standard Fannie Mae and Freddie Mac appraisal form for single-family properties. It captures the subject property's characteristics, a neighborhood analysis, up to nine comparable sales, and the appraiser's final value opinion. Lenders need this data to underwrite loans, manage risk, and meet investor delivery requirements. However, they often lack access to appraisal reports in any format other than PDFs, which makes extracting data a potentially difficult problem.
>
> With Sensible you can easily extract key information out of residential appraisal report PDFs using SenseML, Sensible's hybrid deterministic and LLM-based query language for extracting data from documents. We've written a library of open-source SenseML configurations, so you don't need to write queries from scratch for common documents. From there, your residential appraisal report data is accessible via API, Sensible's UI, or 5,000 other software integrations thanks to Zapier.
>
> In this post, you'll learn to extract appraisal report data using deterministic methods. Because Form 1004 is a government-standardized form, its field positions and label text are consistent across all lenders and appraisers. Therefore, Sensible handles this data extraction through a layout-specific config. Form 1004 reports are well suited to this approach: the form's field positions and label text are fixed by Fannie Mae and Freddie Mac specifications, giving reliable anchor points that deterministic methods extract precisely — no LLM calls, no prompt maintenance overhead. For non-standardized appraisal formats such as narrative appraisals or state-specific hybrid forms, a generalized LLM config handles extraction on day one without per-format configuration. Both run through the same API.

## Structure breakdown

**P1 — Describe the document + problem statement**
- Introduce the document type and its business value
- End with the problem: "However, they often lack access to [document type] in any format other than PDFs, which makes extracting data a potentially difficult problem."
- Do NOT include LLM/deterministic framing here

**P2 — Introduce Sensible (boilerplate, slightly modified)**
- "With Sensible you can easily extract key information out of [document type] PDFs using SenseML, Sensible's **hybrid deterministic and LLM-based** query language for extracting data from documents."
- Note: the standard boilerplate says "query language" but this version adds "hybrid deterministic and LLM-based" — use this phrasing going forward
- Rest of P2 is unchanged boilerplate: library, API/UI/Zapier

**P3 — Post-specific framing: method lead-in + LLM vs. deterministic**
- Opens with: "In this post, you'll learn to extract [doc type] data using [approach]." — states the method upfront
- Follows with: "Because [structural reason], [doc type] is well suited to this approach: [specific structural property], giving reliable anchor points that deterministic methods extract precisely..."
- Includes the complementary method sentence: "For [non-standardized variants], a generalized LLM config handles extraction on day one without per-format configuration. Both run through the same API."
- Key wording: "handles this data extraction" (not "handles this")

## What changed from previous attempts

**Attempt 1** (Claude's first draft): replaced old P2 ("With Sensible...") entirely with framing paragraph. User rejected deletion of boilerplate.

**Attempt 2** (after first feedback): kept boilerplate as P3, inserted framing as new P2. Structure: P1 → P2 (framing) → P3 (boilerplate). User accepted but later wanted the problem statement back in P1 and a lead-in sentence before the framing.

**Final (user-edited)**: P1 (description + problem statement) → P2 (boilerplate, "hybrid deterministic and LLM-based") → P3 (lead-in + framing). The boilerplate now comes BEFORE the framing paragraph, not after.

## Template implication

Update `blog-post-template.md` to show this three-paragraph structure:
1. P1: document description ending with problem statement
2. P2: "With Sensible..." boilerplate with "hybrid deterministic and LLM-based" phrasing
3. P3: "In this post, you'll learn to extract [doc type] data using [approach]. Because [structural reason]..." + LLM vs. deterministic framing + complementary method sentence
