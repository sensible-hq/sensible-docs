# doc-test-results session: decisions

| Date | Decision | Why | Who |
| --- | --- | --- | --- |
| 2026-11-11 | O2 and O3 in one PR, stacked on #810 | Frances: "go ahead with the not-dones, maybe in another stacked PR" | Frances |
| 2026-11-11 | Output tests reuse the sample doc type machinery (`samples.create`), with schema `fingerprint_mode: fallback_to_all`, like the shared doc type had | One way to run a page's own configs; same extraction behavior as before | Claude |
| 2026-11-11 | Envelope builds and probes run in the test's sample doc type too, so the shared doc type can go entirely | Keeping it for two side commands would keep all its cleanup code | Claude |
| 2026-11-11 | Results are a projection of records and Doc Detective results, not a replacement for records | Records keep each kind's detail for report.html; results are what every consumer needs to agree on (status, claim, what was checked) | Claude |
| 2026-11-11 | Other runners hand over results as files in `output/results/`, not through a Python API | #749's checker is a standalone script and #744's tests are pytest; a JSON file is the smallest contract either can meet | Claude |
| 2026-11-11 | Saved results keep the `tests` status map and add `other` for other runners' tests | #741's saved file stays readable; the matrix needs other runners' kind and claim, which aren't in any page markup | Claude |
| 2026-11-11 | Adapters for #744 and #749 left to those PRs | Their code isn't in this stack; adding it here would conflict with them | Claude |
