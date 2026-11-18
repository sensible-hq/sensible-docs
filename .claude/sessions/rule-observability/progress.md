# Rule observability progress

Newest first.

## 2026-11-18: start

- Baseline on v0 (`7d52f49a9`): `check_registry.py` clean (42 rules), fixtures clean, pytest 23 passed and 1 failed. The failure: Frances changed one `sensible-internal-terms` label and removed another in #830, so the stored calibration no longer matches the recordings. Recalibrated in R4.
- Corpus dry run: 385 judge candidates over 170 docs pages, 2.5 minutes, mostly Vale.
- Transcripts: the vale_gate hook has fired only 8 PostToolUse reports so far (from the older `vale-check.sh`); no PreToolUse denials yet. The usage parser is built against those formats plus synthetic cases.
