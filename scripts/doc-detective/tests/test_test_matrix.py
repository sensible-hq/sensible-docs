"""The test matrix (test_matrix.py): generated from markup, test-pages.json, and saved results."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest

import test_matrix
from codetests import settings

from tests.fakes import write_page

PAGE = """<!-- test {"testId": "app_open_tab", "description": "Open the Document Types tab"} -->
<!-- step {"goTo": {"url": "https://app.sensible.so/"}} -->
<!-- test end -->

<!-- code test {"testId": "extract_example", "description": "The documented output | with a pipe"} -->
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


class RealFileTest(unittest.TestCase):
    def test_matrix_is_up_to_date(self):
        with open(test_matrix.MATRIX_FILE, encoding="utf-8") as f:
            self.assertEqual(f.read(), test_matrix.render(),
                             "TEST-MATRIX.md is out of date. Run: python3 scripts/doc-detective/test_matrix.py")

    def test_slug_matches_saved_report_names(self):
        self.assertEqual(test_matrix.slug("docs/Senseml reference/concepts/file-types.md"), "docs-senseml-reference-concepts-file-types")


class MatrixTest(unittest.TestCase):
    def setUp(self):
        self.page = os.path.relpath(write_page(self, PAGE), settings.REPO_ROOT)
        self.reports = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.reports)
        self.entry = {"page": self.page, "priority": 3}

    def rows(self):
        return [l for l in test_matrix.render([self.entry], self.reports).splitlines() if l.startswith("| ") and "`" in l]

    def test_one_row_per_test_with_kind_and_escaped_claim(self):
        rows = self.rows()
        self.assertEqual(len(rows), 2)
        self.assertIn("| 3 (on demand) | `app_open_tab` | UI | Open the Document Types tab |", rows[0])
        self.assertIn("| documented output | The documented output \\| with a pipe |", rows[1])
        self.assertTrue(all(r.endswith("| none saved |") for r in rows))

    def test_saved_results_show_status_commit_and_report(self):
        name = test_matrix.slug(self.page)
        with open(os.path.join(self.reports, f"{name}.json"), "w") as f:
            json.dump({"report": f"{name}.html", "tested_at": "2026-11-11 10:00 UTC", "commit": "abc123456",
                       "uncommitted": True, "tests": {"app_open_tab": "pass"}}, f)
        rows = self.rows()
        self.assertIn("pass, 2026-11-11, commit abc123456 (uncommitted changes), [report](", rows[0])
        self.assertIn("not in that run", rows[1])

    def test_save_writes_each_tests_status_and_provenance(self):
        output = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, output)
        os.makedirs(os.path.join(output, "code-tests"))
        with open(os.path.join(output, "code-tests", "extract_example.json"), "w") as f:
            json.dump({"test_id": "extract_example", "status": "warn"}, f)
        path = test_matrix.save(self.page, output_dir=output, reports_dir=self.reports)
        with open(path) as f:
            saved = json.load(f)
        # No Doc Detective results: the UI test didn't run, which fails the page
        self.assertEqual(saved["tests"], {"app_open_tab": "not run", "extract_example": "warn"})
        self.assertEqual(saved["overall"], "fail")
        self.assertEqual(saved["report"], f"{test_matrix.slug(self.page)}.html")
        self.assertEqual(saved["commit"], subprocess.run(["git", "rev-parse", "--short=9", "HEAD"], capture_output=True,
                                                          text=True, cwd=settings.REPO_ROOT).stdout.strip())
        self.assertTrue(saved["tested_at"].endswith(" UTC"))


if __name__ == "__main__":
    unittest.main()
