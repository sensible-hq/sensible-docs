"""report.py summary: the Markdown a CI run shows on its page."""

import unittest

from codetests.reports import summary

from tests.fakes import CODE_TEST_PAGE, write_page


class SummaryTest(unittest.TestCase):
    def record(self, status, **extra):
        return {"test_id": "first", "file": "p.md", "status": status, "warnings": [], "message": "boom", **extra}

    def test_missing_records_count_as_failures(self):
        text = summary.body(write_page(self, CODE_TEST_PAGE), {}, [], report_url="https://example.test/r")
        self.assertIn("## Docs tests: ❌ Failed", text)
        self.assertIn("| `first` | Code test | ❌ Not run |", text)
        self.assertIn("[Open the full HTML report](https://example.test/r)", text)

    def test_pass_and_warnings(self):
        rec = self.record("warn", overall="identical", warnings=[{"source": "fixture", "text": "restored"}])
        text = summary.body(write_page(self, CODE_TEST_PAGE), {}, [rec])
        self.assertIn("## Docs tests: ⚠️ Passed with warnings", text)
        self.assertIn("documented output vs Sensible: identical", text)
        self.assertIn("- `first` [fixture] restored", text)

    def test_failure_details(self):
        rec = self.record("fail", category="RUNNER_ERROR", message="RUNNER_ERROR: boom")
        text = summary.body(write_page(self, CODE_TEST_PAGE), {}, [rec], run_url="https://example.test/run")
        self.assertIn("<summary><code>first</code> failed</summary>", text)
        self.assertIn("FAIL first  RUNNER_ERROR: boom", text)
        self.assertIn("[this run](https://example.test/run)", text)


if __name__ == "__main__":
    unittest.main()
