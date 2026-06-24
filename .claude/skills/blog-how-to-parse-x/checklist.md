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
