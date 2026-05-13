# extra_data PR checklist (docs/extra-data-3320)

## Done

- [x] `extra-data.md` — GEICO example extended with `queryGroup` + `source_ids` semantic comparison (vehicle matching)
- [x] `extra-data.md` — Portfolio extractions section added
- [x] Blog post draft (`drafts/blog-extra-data.md`)
- [x] `create-docs-example` skill updated with upload + live extraction step (Step 5)
- [x] Test scripts: `scripts/test/retrieve.sh` and `scripts/test/extra_data/test_extra_data_example.sh`
- [x] `extra_data.png` pushed to v0
- [x] Crosslinks added: `validate-extractions.md`, `api-tutorial-async-1.md`, `list.md`, `query-group.md`, `computed-field-methods/index.md`, `llm-based-methods/index.md` (reverted), `extra-data.md`
- [x] Pipeline-context framing applied throughout docs and blog post
- [x] Overview + 4 use-case diagrams rendered and added to docs and blog post

## Claude to-do (pre-merge)

- [ ] **#16** Vale style check — run Vale on all changed docs files and fix any errors before merging
- [ ] **#17** Sync blog post example with `extra-data.md` — compare config, request, and output blocks; they may have drifted from the manual edits pulled in

## Blocked on Frances

- [ ] **#3** Unhide doc page — change `hidden: true` → `hidden: false` in `extra-data.md` front matter before merging
- [ ] **#6** Document in-app UI for `extra_data` input/retrieval once that UI ships

## Blocked on eng

- [ ] **#10** Clarify and document what happens when an API key is passed in `extra_data` (rejection behavior)

## Claude to-do

- [x] **#7** Update `validating-extractions.md`: frame `extra_data` as a specific use case of the pipeline-context pattern — dynamically populating expected values at request time instead of hardcoding them in the config. Cross-link to `extra-data.md`.
- [x] **#9** Document `extra_data` constraints: 16 KiB record size limit, no nested objects or arrays
- [x] **#11** Update inline JSON5 comments in config per PR #587
- [ ] **#13** *(deferred)* Add `extra_data` mentions + LLM use case to agentic/LLM docs
- [x] **#15** Framing: primary frame is **pipeline context** (Option B) — `extra_data` carries caller-supplied context into an extraction step. Validation is one specific use case of this (dynamically passing expected values instead of hardcoding them). Transformation/enrichment is another (e.g. passing in external values to compute sums or derive new fields). Ensure docs, blog post, and crosslinks all reflect this broader framing rather than leading with "validation."

## Testing

- [x] **#14** `scripts/test/extra_data/smoke_test_extra_data.sh` — asserts all 8 spec claims (4 request, 4 response). Run: `SENSIBLE_API_KEY=<key> bash smoke_test_extra_data.sh [document_type]`

## Known bugs

- [ ] `scripts/upload_pr_extractor.py` URL bug — script generates `g=<stem>` in app URL but golden is uploaded as `<stem>_pdf` (`.` → `_`). Correct URL: `g=extra_data_pdf`.
