"""Read Doc Detective's results for UI tests, without typed text."""

import glob
import json
import os

ACTIONS = {"goTo", "find", "click", "type", "runShell", "runCode", "httpRequest", "checkLink", "screenshot", "wait"}


def step_summary(step):
    """A step's description, action and target, and result. Never typed text."""
    action = next((k for k in step if k in ACTIONS), "step")
    spec = step.get(action)
    if action == "goTo":
        what = f"go to {spec.get('url', '') if isinstance(spec, dict) else spec}"
    elif action == "type":
        what = f"type into {spec.get('selector', 'the focused element')}" if isinstance(spec, dict) else "type"
    elif action in ("find", "click"):
        if isinstance(spec, dict):
            bits = [spec["selector"]] if spec.get("selector") else []
            if spec.get("elementText"):
                bits.append(f'"{spec["elementText"]}"')
            what = f"{action} " + " with text ".join(bits)
        else:
            what = f'{action} "{spec}"'
    else:
        what = action
    return {
        "description": step.get("description", ""),
        "action": what,
        "result": {"PASS": "pass", "FAIL": "fail"}.get(step.get("result"), "skipped"),
        "message": step.get("resultDescription", ""),
        "seconds": round(step.get("durationMs", 0) / 1000, 1),
    }


def load_results(output_dir):
    """{testId: {"status", "steps", "failed"}} from Doc Detective's newest results file."""
    files = sorted(glob.glob(os.path.join(output_dir, "testResults-*.json")))
    if not files:
        return {}
    with open(files[-1], encoding="utf-8") as f:
        data = json.load(f)
    results = {}
    for spec in data.get("specs", []):
        for test in spec.get("tests", []):
            steps = [step_summary(s) for c in test.get("contexts", []) for s in c.get("steps", [])]
            results[test["testId"]] = {
                "status": "pass" if test.get("result") == "PASS" else "fail",
                "steps": steps,
                "failed": sum(s["result"] == "fail" for s in steps),
            }
    return results


def verify_ui(page, ui_results):
    """Problems where a UI test on the page didn't run, or ran without every step: Doc Detective
    skips tests and steps it can't read, logs a warning, and carries on."""
    problems = []
    for t in page.ui_tests:
        where = f"({page.path}, line {t.line})"
        if t.test_id not in ui_results:
            problems.append(f"{t.test_id}  Doc Detective didn't run this UI test {where}. Check its <!-- test --> and <!-- step --> comments.")
        elif len(ui_results[t.test_id]["steps"]) < t.steps:
            skipped = t.steps - len(ui_results[t.test_id]["steps"])
            problems.append(f"{t.test_id}  Doc Detective skipped {skipped} of its {t.steps} steps {where}. Check the <!-- step --> comments for an invalid action.")
    return problems
