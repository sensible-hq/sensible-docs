"""One result shape for every runner (codetests/results.py), and every report and the matrix reading it."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

import test_matrix
from codetests import markup, results, settings
from codetests.reports import html, issue, summary

from tests.fakes import write_page

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGE = """<!-- test {"testId": "app_open_tab", "description": "Open the Document Types tab"} -->
<!-- step {"goTo": {"url": "https://app.sensible.so/"}} -->
<!-- step {"find": {"elementText": "Document types"}} -->
<!-- test end -->

<!-- code test {"testId": "extract_example", "description": "The documented output"} -->
<!-- inline config -->
```json
{"fields": []}
```
<!-- inline output -->
```json
{}
```
<!-- code test end -->
"""

STEP = {"description": "", "action": "go to https://app.sensible.so/", "result": "pass", "message": "", "seconds": 1.0}
UI_PASS = {"status": "pass", "failed": 0, "steps": [STEP, STEP]}
RECORD = {"test_id": "extract_example", "kind": "output", "status": "warn", "overall": "identical", "warnings": [],
          "file": "p.md", "document_url": "", "description": ""}
PARAM_TABLE = {"test_id": "row_parameters", "runner": "param-tables", "kind": "parameter table", "status": "fail",
               "claim": "The Row method's parameter table matches the SenseML schema", "category": "SCHEMA_MISMATCH",
               "message": "tiebreaker: the schema has no such parameter", "warnings": ["position isn't documented"],
               "evidence": [{"label": "SenseML schema", "url": "https://schema.sensible.so/configuration.schema.json"}]}


def write_other(case, items, name="param-tables"):
    output = tempfile.mkdtemp()
    case.addCleanup(shutil.rmtree, output)
    os.makedirs(os.path.join(output, results.RESULTS_DIR))
    with open(os.path.join(output, results.RESULTS_DIR, f"{name}.json"), "w") as f:
        json.dump(items, f)
    return output


class ResultTest(unittest.TestCase):
    def setUp(self):
        self.page = markup.parse_page(write_page(self, PAGE))

    def test_ui_results(self):
        test = self.page.ui_tests[0]
        self.assertEqual(results.from_ui(test, None)["status"], "not run")
        self.assertEqual(results.from_ui(test, UI_PASS)["status"], "pass")
        # Doc Detective skipped a step on the page: fail, even though every step it ran passed
        self.assertEqual(results.from_ui(test, {**UI_PASS, "steps": [STEP]})["status"], "fail")

    def test_code_results(self):
        test = self.page.code_tests["extract_example"]
        self.assertEqual(results.from_record(test, None)["status"], "not run")
        passed = results.from_record(test, RECORD)
        self.assertEqual((passed["status"], passed["kind"], passed["checked"]), ("warn", "output", "documented output vs Sensible: identical"))
        failed = results.from_record(test, {**RECORD, "status": "fail", "category": "OUTPUT_DRIFT", "message": "boom"})
        self.assertEqual((failed["category"], failed["message"]), ("OUTPUT_DRIFT", "boom"))
        for result in (passed, failed):
            results.validate(result)

    def test_page_order_then_other_runners(self):
        found = results.for_page(self.page, {"app_open_tab": UI_PASS}, [RECORD], [PARAM_TABLE])
        self.assertEqual([r["test_id"] for r in found], ["app_open_tab", "extract_example", "row_parameters"])
        self.assertEqual(results.overall(found), "fail")
        self.assertEqual(results.overall(found[:2]), "warn")
        self.assertEqual(results.overall(results.for_page(self.page, {}, [RECORD])), "fail")  # a test that didn't run

    def test_other_runners_results_are_checked(self):
        self.assertEqual(results.load_other(write_other(self, [PARAM_TABLE])), [PARAM_TABLE])
        self.assertEqual(results.load_other(tempfile.gettempdir() + "/no-such-output"), [])
        for bad, why in (([{**PARAM_TABLE, "status": "broken"}], "row_parameters"),
                         ([{**PARAM_TABLE, "runner": "code"}], "reserved"),
                         (PARAM_TABLE, "a list")):
            with self.assertRaises(ValueError) as caught:
                results.load_other(write_other(self, bad))
            self.assertIn(why, str(caught.exception))


class OtherRunnerReportsTest(unittest.TestCase):
    """Another runner's results reach report.html, the CI summary, the issue, the saved results, and the matrix."""

    def setUp(self):
        self.path = write_page(self, PAGE)
        self.page = markup.parse_page(self.path)

    def test_html_summary_and_issue(self):
        out = os.path.join(tempfile.mkdtemp(), "report.html")
        self.addCleanup(shutil.rmtree, os.path.dirname(out))
        html.render(self.path, {"app_open_tab": UI_PASS}, [RECORD], out, other=[PARAM_TABLE])
        with open(out) as f:
            page = f.read()
        self.assertIn('id="row_parameters"', page)
        self.assertIn("SCHEMA_MISMATCH: tiebreaker: the schema has no such parameter", page)
        self.assertIn('href="https://schema.sensible.so/configuration.schema.json"', page)
        self.assertIn("<td>param-tables</td>", page)

        rows = summary.test_rows(self.page, {"app_open_tab": UI_PASS}, [RECORD], [PARAM_TABLE])
        self.assertEqual(rows[-1], ("row_parameters", "param-tables", "fail", ""))
        body = summary.body(self.path, {"app_open_tab": UI_PASS}, [RECORD], other=[PARAM_TABLE])
        self.assertIn("## Docs tests: ❌ Failed", body)
        self.assertIn("`row_parameters` [param-tables] position isn't documented", body)

        self.assertIn("### `row_parameters` (param-tables)", issue.body({}, [], other=[PARAM_TABLE]))

    def test_saved_results_and_matrix(self):
        output = write_other(self, [PARAM_TABLE])
        os.makedirs(os.path.join(output, "code-tests"))
        with open(os.path.join(output, "code-tests", "extract_example.json"), "w") as f:
            json.dump(RECORD, f)
        reports = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, reports)
        with open(test_matrix.save(self.path, output_dir=output, reports_dir=reports)) as f:
            saved = json.load(f)
        self.assertEqual(saved["tests"], {"app_open_tab": "not run", "extract_example": "warn", "row_parameters": "fail"})
        self.assertEqual(saved["other"][0]["kind"], "parameter table")
        matrix = test_matrix.render([{"page": self.path, "priority": 3}], reports)
        row = next(line for line in matrix.splitlines() if "`row_parameters`" in line)
        self.assertIn("parameter table (param-tables)", row)
        self.assertIn("fail,", row)

    def test_report_html_fails_on_another_runners_failure(self):
        output = write_other(self, [PARAM_TABLE])
        run = lambda: subprocess.run([sys.executable, os.path.join(HERE, "report.py"), "html", "--page", self.path, "--output", output],
                                     capture_output=True, text=True)
        failed = run()
        self.assertEqual(failed.returncode, 1, failed.stderr)
        self.assertIn("FAIL row_parameters (param-tables)", failed.stdout)
        write_other_into = os.path.join(output, results.RESULTS_DIR, "param-tables.json")
        with open(write_other_into, "w") as f:
            json.dump([{**PARAM_TABLE, "status": "pass"}], f)
        self.assertEqual(run().returncode, 0)


if __name__ == "__main__":
    unittest.main()
