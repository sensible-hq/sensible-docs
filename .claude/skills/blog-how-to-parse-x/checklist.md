# blog-parse session checklist

- [x] Add canonical comments to `json5-comments-reference.md` for SenseML params missing from delivery orders post: `flags`, `horizontalAnchor`, `matches`, `pattern`, `wordFilters`
- [x] Template: add new sections from commission statements post (delivery orders and insurance quotes sections already done)
- [x] Use Notion MCP server to push blog post drafts (and revisions) to Notion
- [x] After generating the draft, upload the config and PDF using `scripts/upload_pr_extractor.py` and run live extraction before drafting (Step 4 in SKILL.md)
- [x] In Step 3 (config analysis): summarize ALL fields in the config before selecting examples
- [x] In Step 3 (config analysis): provide explicit reasoning for field selection
- [x] After Step 3 field inventory, pause for user feedback before Step 4
- [x] Add a blog post step for explaining fingerprints when present (Step 5 in SKILL.md; prereq JSON5 comments done)
- [x] Write `test_blog_output.py`: extracts the "Putting it all together" code block from a draft, runs it via the Sensible API against the golden PDF, and diffs the result against the output block in the draft — prints a log of matches/mismatches for review before publishing (layout-based configs are deterministic; flag LLM-based fields separately)
- [x] Add a "Putting it all together" section (template + delivery orders draft done)
- [x] Cross-check individual output blocks against combined output (Step 6.6 in SKILL.md)
- [ ] Code examples may be over-commented: provide guidance on omitting repetitious comments (e.g. don't repeat the same comment for `"type": "startsWith"` on every anchor in the same block)
- [ ] Set a hard line-count limit on individual field code blocks: 75 lines max, enforced by a Python check that strips the "Putting it all together" section by heading and counts lines in each remaining fenced code block. Property rights appraised in the appraisal draft (~73 lines) is the calibration ceiling; comparable sale data (~216 lines) is the violation. For sections fields with many sub-fields, trim to 1-2 most illustrative sub-fields. For deeply nested sections (3+ levels), limit to 1 sub-field. Add the line-limit rule to the template.
- [ ] Update `blog-post-template.md` to show a three-paragraph intro structure (P1 → P2 framing → P3 "With Sensible..." boilerplate). The framing paragraph (P2) is inserted between P1 and the existing boilerplate (P3), not replacing it. Also fix the complementary-method sentence to use "handles this data extraction" not "handles this". See `.claude/skills/blog-how-to-parse-x/intro-rewrite-feedback.md` for the full diff of what was proposed vs. accepted in the appraisal draft.
- [ ] Add blog-specific field selection guidance: avoid demonstrating Sections fields whose sub-fields themselves use Sections (nested sections). The structural wrapper overhead (~40+ lines per level) consumes the code block budget before any field logic appears, and the nesting is too complex to explain concisely in a blog post. Prefer flat top-level fields or single-level Sections. Appraisal draft: dropped `sales_comparison` (nested sections within sections) entirely after failed attempts to trim it. Add this as a constraint in Step 3 field selection in SKILL.md.
- [ ] Compare appraisal Draft v1 vs Draft v4 in Notion to assess intro and field selection evolution. Draft v1: https://app.notion.com/p/38ac7dd4978881eba82ccd8c8819cf4d — Draft v4: https://app.notion.com/p/38ac7dd497888161b4b4e32c11c64249
