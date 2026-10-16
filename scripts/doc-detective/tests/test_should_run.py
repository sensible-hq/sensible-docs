"""should_run.decide: a push that changed only a page's prose skips the docs-test run."""

import os
import subprocess
import tempfile
import unittest

import should_run

from tests.fakes import CODE_TEST_PAGE

PAGE = "docs/page.md"
TABLE = """
<!-- table test {"testId": "tt", "table": "claims", "segment_documents_with": "fingerprints"} -->
<!-- inline document -->
| Example document | [Download link](https://example.test/p.pdf) |

<!-- table {"tableId": "claims"} -->
| claim | result |
| ----- | ------ |
| first | none |

<!-- row {"rowId": "first_row", "fixture": {"name": "fixture_fp_demo_first_fails"}, "expect": {"compare": "documents", "documents": []}} -->
<!-- table test end -->
"""


class DecideTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.cwd = os.getcwd()
        os.chdir(self.dir.name)
        self.addCleanup(os.chdir, self.cwd)
        self.git("init", "-q")
        self.git("config", "user.email", "t@example.test")
        self.git("config", "user.name", "t")
        self.before = self.commit({PAGE: "Intro.\n" + CODE_TEST_PAGE + TABLE})

    def git(self, *args):
        return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout.strip()

    def commit(self, files):
        for path, text in files.items():
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "c")
        return self.git("rev-parse", "HEAD")

    def decide(self, files):
        after = self.commit(files)
        return should_run.decide(PAGE, self.before, after, ["tooling/**"])

    def page(self, text):
        return {PAGE: text}

    def test_prose_only_skips(self):
        self.assertEqual(self.decide(self.page("New intro, and **bold**.\n" + CODE_TEST_PAGE + TABLE.replace("| first | none |", "| first claim | none at all |")))[0], False)

    def test_changed_test_markup_runs(self):
        changes = [
            CODE_TEST_PAGE.replace('{"fields": []}', '{"fields": [1]}'),  # config
            CODE_TEST_PAGE.replace("a.pdf", "b.pdf"),  # document
            CODE_TEST_PAGE.replace("{}", '{"x": 1}'),  # documented output
        ]
        for i, new in enumerate(changes):
            with self.subTest(i):
                self.assertEqual(self.decide(self.page("Intro.\n" + new + TABLE))[0], True)

    def test_changed_expectation_or_row_count_runs(self):
        self.assertTrue(self.decide(self.page("Intro.\n" + CODE_TEST_PAGE + TABLE.replace('"documents": []', '"documents": [["fixture_x", 1, 2]]')))[0])

    def test_added_table_row_runs(self):
        self.assertTrue(self.decide(self.page("Intro.\n" + CODE_TEST_PAGE + TABLE.replace("| first | none |", "| first | none |\n| second | two |")))[0])

    def test_watched_file_runs_and_other_files_dont(self):
        self.assertTrue(self.decide({"tooling/x.py": "x"})[0])
        self.before = self.git("rev-parse", "HEAD")
        self.assertEqual(self.decide({"other/x.md": "x", PAGE: "Intro 2.\n" + CODE_TEST_PAGE + TABLE})[0], False)

    def test_prose_above_an_inline_sample_skips(self):
        from tests.test_samples import PORTFOLIO
        self.before = self.commit(self.page("Intro.\n" + PORTFOLIO))
        self.assertEqual(self.decide(self.page("A longer intro.\n\nWith a new paragraph.\n" + PORTFOLIO))[0], False)
        self.before = self.git("rev-parse", "HEAD")
        self.assertTrue(self.decide(self.page("A longer intro.\n\nWith a new paragraph.\n" + PORTFOLIO.replace('"text": "anyco"', '"text": "anyco ltd"', 1)))[0])

    def test_broken_markup_runs(self):
        self.assertTrue(self.decide(self.page("Intro.\n" + CODE_TEST_PAGE.replace("<!-- code test end -->", "")))[0])

    def test_no_previous_commit_runs(self):
        self.assertTrue(should_run.decide(PAGE, "0" * 40)[0])


if __name__ == "__main__":
    unittest.main()
