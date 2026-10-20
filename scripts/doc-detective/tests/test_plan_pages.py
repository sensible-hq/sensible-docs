"""plan_pages.py and config/pages.json: which registered pages a doc-tests-pages.yml run tests."""

import json
import os
import re
import subprocess
import tempfile
import unittest

import plan_pages

from tests.fakes import CODE_TEST_PAGE


class RegistryTest(unittest.TestCase):
    def test_registry_loads(self):
        pages = plan_pages.load()
        self.assertEqual([p["slug"] for p in pages], ["getting_started", "fingerprint", "portfolio"])

    def test_workflow_push_paths_cover_the_registry(self):
        """Every page, every file its tests use, and the tooling must trigger the workflow."""
        with open(os.path.join(plan_pages.check_secrets.REPO_ROOT, plan_pages.WORKFLOW), encoding="utf-8") as f:
            text = f.read()
        block = text[text.index("    paths:"):text.index("  workflow_dispatch:")]
        paths = set(re.findall(r'-\s*"([^"]+)"', block))
        wanted = {p["page"] for p in plan_pages.load()} | {w for p in plan_pages.load() for w in p["watch"]} | set(plan_pages.COMMON_WATCH)
        self.assertEqual(paths, wanted)

    def bad(self, entry, message):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump({"pages": [entry]}, f)
        self.addCleanup(os.remove, f.name)
        with self.assertRaises(ValueError) as caught:
            plan_pages.load(f.name)
        self.assertIn(message, str(caught.exception))

    def test_registry_errors(self):
        ok = {"slug": "x", "title": "X", "page": "docs/document extraction/portfolio.md", "timeout_minutes": 5}
        self.bad({**ok, "slug": "Bad-Slug"}, "must be unique lowercase")
        self.bad({**ok, "page": "docs/no-such-page.md"}, "no page")
        self.bad({**ok, "secrets": ["NOT_REGISTERED"]}, "aren't in config/secrets.txt")
        self.bad({**ok, "colour": "red"}, "unknown fields colour")
        self.bad({**ok, "gate": "yes"}, "true or false")

    def test_matrix_entry_detects_ui_tests(self):
        by_slug = {p["slug"]: plan_pages.matrix_entry(p) for p in plan_pages.load()}
        self.assertTrue(by_slug["getting_started"]["ui_tests"])
        self.assertFalse(by_slug["fingerprint"]["ui_tests"])
        self.assertEqual(by_slug["fingerprint"]["secrets"], ["SENSIBLE_TEST_API_KEY"])


class PlanTest(unittest.TestCase):
    """plan() against a throwaway git repo with two gated pages and one ungated page."""

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.cwd = os.getcwd()
        os.chdir(self.dir.name)
        self.addCleanup(os.chdir, self.cwd)
        for args in (["init", "-q"], ["config", "user.email", "t@example.test"], ["config", "user.name", "t"]):
            self.git(*args)
        self.pages = [
            {**plan_pages.DEFAULTS, "slug": "a", "title": "A", "page": "a.md", "timeout_minutes": 5, "watch": ["fixtures/a/**"]},
            {**plan_pages.DEFAULTS, "slug": "b", "title": "B", "page": "b.md", "timeout_minutes": 5},
            {**plan_pages.DEFAULTS, "slug": "c", "title": "C", "page": "c.md", "timeout_minutes": 5, "gate": False},
        ]
        self.before = self.commit({"a.md": "A.\n" + CODE_TEST_PAGE, "b.md": "B.\n" + CODE_TEST_PAGE, "c.md": "C.\n" + CODE_TEST_PAGE})

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

    def runs(self, files, event="push", wanted="all"):
        after = self.commit(files) if files else self.before
        return {p["slug"]: run for p, run, _ in plan_pages.plan(self.pages, event, self.before, after, wanted)}

    def test_only_the_changed_pages_run(self):
        self.assertEqual(self.runs({"a.md": "A.\n" + CODE_TEST_PAGE.replace("a.pdf", "z.pdf")}), {"a": True, "b": False, "c": False})

    def test_prose_skips_gated_pages_but_not_ungated_ones(self):
        self.assertEqual(self.runs({"a.md": "New prose.\n" + CODE_TEST_PAGE, "c.md": "New prose.\n" + CODE_TEST_PAGE}),
                         {"a": False, "b": False, "c": True})

    def test_a_watched_file_runs_its_page(self):
        self.assertEqual(self.runs({"fixtures/a/x.json": "{}"}), {"a": True, "b": False, "c": False})

    def test_tooling_runs_every_page(self):
        self.assertEqual(self.runs({"scripts/doc-detective/x.py": ""}), {"a": True, "b": True, "c": True})

    def test_schedule_and_dispatch(self):
        self.assertEqual(self.runs({}, "schedule"), {"a": True, "b": True, "c": True})
        self.assertEqual(self.runs({}, "workflow_dispatch"), {"a": True, "b": True, "c": True})
        self.assertEqual(self.runs({}, "workflow_dispatch", "b, c"), {"a": False, "b": True, "c": True})
        with self.assertRaises(ValueError):
            self.runs({}, "workflow_dispatch", "nope")


if __name__ == "__main__":
    unittest.main()
