# extra_data PR checklist (docs/extra-data-3320)

## Done

- [x] `extra-data.md` — GEICO example extended with `queryGroup` + `source_ids` semantic comparison (vehicle matching)
- [x] `extra-data.md` — Portfolio extractions section added
- [x] Blog post draft (`drafts/blog-extra-data.md`)
- [x] `create-docs-example` skill updated with upload + live extraction step (Step 5)
- [x] Test scripts: `scripts/test/retrieve.sh` and `scripts/test/extra_data/test_extra_data_example.sh`
- [x] `extra_data.png` pushed to v0

## Blocked on Frances

- [ ] **#3** Unhide doc page — change `hidden: true` → `hidden: false` in `extra-data.md` front matter before merging
- [ ] **#6** Document in-app UI for `extra_data` input/retrieval once that UI ships

## Blocked on eng

- [ ] **#10** Clarify and document what happens when an API key is passed in `extra_data` (rejection behavior)

## Claude to-do

- [ ] **#7** Update `validating-extractions.md`: frame `extra_data` as a specific use case of the pipeline-context pattern — dynamically populating expected values at request time instead of hardcoding them in the config. Cross-link to `extra-data.md`.
- [ ] **#9** Document `extra_data` constraints: 16 KiB record size limit, no nested objects or arrays
- [ ] **#11** Update inline JSON5 comments in config per PR #587
- [ ] **#13** *(deferred)* Add `extra_data` mentions + LLM use case to agentic/LLM docs
- [ ] **#15** Framing: primary frame is **pipeline context** (Option B) — `extra_data` carries caller-supplied context into an extraction step. Validation is one specific use case of this (dynamically passing expected values instead of hardcoding them). Transformation/enrichment is another (e.g. passing in external values to compute sums or derive new fields). Ensure docs, blog post, and crosslinks all reflect this broader framing rather than leading with "validation."

## Testing

- [ ] **#14** Write bash tests that verify every place the OpenAPI spec claims `extra_data` appears in a request or response body actually does so — i.e. smoke-test that the live API matches the spec for each endpoint that should accept or return `extra_data`. First step: pull the OpenAPI spec and enumerate all `extra_data` occurrences to scope what needs testing.

## Known bugs

- [ ] `scripts/upload_pr_extractor.py` URL bug — script generates `g=<stem>` in app URL but golden is uploaded as `<stem>_pdf` (`.` → `_`). Correct URL: `g=extra_data_pdf`.
