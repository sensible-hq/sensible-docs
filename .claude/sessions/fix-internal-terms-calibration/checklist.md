# fix-internal-terms-calibration

Claude Code session: fix-internal-terms-calibration, ID 65b8ea5d-12b0-490e-96c1-26d7d0b275d9

- [x] Find why `test_calibration_in_specs_matches_the_recordings` fails on `v0`: #830 relabeled the "S3 bucket" case as `implementation` and removed the "Lambda" case, but the spec's stored calibration still had the old numbers
- [x] Recalibrate `sensible-internal-terms` from the recorded Jev responses (`calibrate.py --write`, offline replay)
- [x] `scripts/style/test`: 24 passed
- [ ] Frances reviews and merges
