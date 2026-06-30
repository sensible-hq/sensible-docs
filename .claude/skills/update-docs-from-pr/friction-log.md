# update-docs-from-pr friction log

## Run: PR #3351 + #3375 (region: asImage, percentOverlapX/Y)

### 1. Loose paraphrasing instead of verbatim copy

**What happened:** When adding `percentOverlapX` and `percentOverlapY` to the region parameter table, Claude rewrote the descriptions rather than copying the existing wording from `intersection.md`, where these same parameters are already documented. Required two interruptions to correct.

**First correction:** "I want you to more precisely copy the wording of the percentOverlap params in intersection for this. don't be loose the way you were just now."

**Second correction (id row):** "I prefer you keep the original wording but add 'by default' like 'where "contained" by default means...' — Configure these thresholds with the Percent Overlap X and Percent Overlap Y parameters."

**Rule:** When wording already exists in another doc for the same parameter (confirmed to share the same underlying implementation), copy it precisely. Only adapt what's structurally required (e.g., dropping an opening clause that's intersection-specific). Do not paraphrase.

---

### 2. Vale style check failed

**What happened:** Vale MCP server (`mcp__vale__check_file`) was not available as a callable tool (not in deferred tool list). Fallback to CLI `vale` also failed:

```
[E100] [loadStyles] Runtime error
style 'Google' does not exist on StylesPath
```

**Result:** Step 5 (style check) was not completed. Files were not checked before committing.

**Root cause:** Vale is not configured correctly in this environment — `StylesPath` does not contain the Google style. Needs investigation.
