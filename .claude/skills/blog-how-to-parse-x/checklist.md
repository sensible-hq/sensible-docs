# blog-parse session checklist

- [ ] JSON5 code examples: leverage specific existing comments from published posts (not generated from scratch)
- [ ] Template: add new sections derived from newer blog posts — commission statements, delivery orders, and insurance quotes
- [ ] Use Notion MCP server to push blog post drafts (and revisions) to Notion
- [ ] After generating the draft, upload the config and PDF to the user's Sensible account using `scripts/upload_pr_extractor.py` (see Step 5 of `create-docs-example` skill) to get real extraction output — replace mocked output blocks in the draft with actual API results
- [ ] In Step 3 (config analysis): summarize ALL fields in the config before selecting examples, not just the ones chosen
- [ ] In Step 3 (config analysis): provide explicit reasoning and evidence for why the selected fields are "interesting" (e.g. method complexity, reader value, uniqueness to the doc type)
- [ ] After Step 3 field inventory + selection reasoning, pause and present to user for feedback before proceeding to Step 4 (extraction) — don't draft until field selection is approved
- [ ] Add a blog post step for explaining fingerprints when present in the config — prereq: add JSON5 inline comments to the existing fingerprints examples in the docs first (so the commenter skill has a source for fingerprint params)
- [ ] Write `scripts/test_blog_output.py`: extracts the "Putting it all together" code block from a draft, runs it via the Sensible API against the golden PDF, and diffs the result against the output block in the draft — prints a log of matches/mismatches for review before publishing (layout-based configs are deterministic; flag LLM-based fields separately)
- [ ] In the blog post draft, include a link to the config in the Sensible app (the URL printed by upload_pr_extractor.py) so the blog writer can visually verify the extraction before publishing
- [ ] Add a "Putting it all together" section near the end: one combined code block with ALL demonstrated fields (plus fingerprint if present in the config) and a single output block for the full extraction — lets readers (and the blog writer) paste and run the whole thing in one shot
- [ ] After writing the "Putting it all together" output, cross-check each individual field's output block against it — the combined output is the source of truth; update any individual blocks that disagree
