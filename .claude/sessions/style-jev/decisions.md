# Jev style judge decisions

## JD-001 Built in sensible-docs, not sensible-docs-gen

Frances's call (2026-11-17). The judge reads the specs and registry in this repo. The client is a small rewrite of `sensible-docs-gen/docsgen/jev.py`'s request, replay, and cost logic, without its clearance and backend-code guard, which protect material this repo doesn't send.

## JD-002 Choice questions, not noul

Frances's specs ask multiple-choice questions with criteria, and Jev supports them: a live probe on 2026-11-17 (`jev-1.14.0`) returned `{"choice", "confidence", "probabilities"}` for a `choice` question with a `criteria` map. Choices separate "this is a passive" from "this is an adjective", which a yes-or-no score can't.

## JD-003 Trust is earned by precision and recall on labeled cases, not set by hand

A rule fails a run only with precision >= 0.90, recall >= 0.50, at least 6 cases, and at least 3 labeled violations. Threshold sweeps on the recorded calibration (0.0 to 0.7) moved overall agreement only between 0.66 and 0.72; raising the confidence threshold traded misses for fewer false positives (6 false positives at 0.0, 1 at 0.7). So the 0.70 threshold stays, and trust is judged on precision first. The minimum sample keeps a rule from earning trust on 4 cases.

## JD-004 Jev isn't deterministic

The same request returned 0.35 and then 0.51 confidence for one passive sentence on two runs (`jev-1.14.0`). Tests replay recorded responses. Calibration numbers come from one recorded run and can move a little on a live rerun; rerun `calibrate.py --write` after a spec changes, and commit the new recordings with it.

## JD-005 Detectors send only what the rule needs

Section openers take only the prose directly under a heading, and skip Parameters, Examples, Notes, and Syntax sections. The first live run flagged "A fingerprint for portfolios contains a Tests parameter…", which opens a `## Parameters` section that the detector reached from the heading above it.

## JD-006 Labels are Claude's until Frances reviews them

61 cases across 11 rules, each marked `labeled_by: claude`. Trust computed from them is provisional. Changing a label changes trust on the next `calibrate.py --write`.
