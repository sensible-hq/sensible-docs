# Jev style judge checklist

Session: jev-style (Claude Code session `cec011d3-0e56-45f1-aa31-0fc712c29141`)
Worktree: `~/GitHub/sensible-docs-jev-style`, branch `jev-style`, stacked on `style-cleanup`
Repo: `fscelliott/sensible-docs-private-test` only (not upstream)
Design: `design.md` in this directory

- [x] J1 Jev client with record and replay (`scripts/style/jev.py`)
- [x] J2 Machine detectors and verdicts in every judgment spec; `check_registry.py` validates them
- [x] J3 Judge (`scripts/style/judge.py`): detectors, Jev calls, report
- [x] J4 Labeled cases and calibration (`scripts/style/calibrate.py`); results recorded
- [x] J5 Offline tests from recorded responses
- [x] J6 Skills and README wired to the judge
- [x] J7 Push to the private copy and open a PR there
