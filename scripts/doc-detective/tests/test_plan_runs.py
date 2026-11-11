"""Which pages a CI run tests: test-pages.json, by priority and trigger (plan_runs.py)."""

import copy
import json
import os
import re
import tempfile
import unittest

import plan_runs


def entry(page, priority, name, **extra):
    return {"page": page, "priority": priority, "name": name, "title": name, "issue_label": f"doc-tests-{name}",
            "watch": [], "timeout_minutes": 10, "ui": False, "propose_fixes": False, "envelope_issue": False, **extra}


ENTRIES = [
    entry("docs/a.md", 1, "a", watch=["assets/pdfs/a.pdf"]),
    entry("docs/b.md", 2, "b"),
    entry("docs/c.md", 3, "c"),
]


def always(page, before, after, watch):
    return True, "the page's tests changed"


def never(page, before, after, watch):
    return False, "only the page's prose changed"


class RealFileTest(unittest.TestCase):
    def test_lists_every_page_with_test_markup(self):
        self.assertEqual(plan_runs.problems(plan_runs.load()), [])

    def test_workflow_crons_match_the_planner(self):
        with open(os.path.join(plan_runs.REPO_ROOT, ".github", "workflows", "doc-tests.yml"), encoding="utf-8") as f:
            crons = set(re.findall(r'-\s*cron:\s*"([^"]+)"', f.read()))
        self.assertEqual(crons, set(plan_runs.SCHEDULES))


class ProblemsTest(unittest.TestCase):
    def repo(self, pages):
        root = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, root)
        for path, text in pages.items():
            os.makedirs(os.path.dirname(os.path.join(root, path)), exist_ok=True)
            with open(os.path.join(root, path), "w", encoding="utf-8") as f:
                f.write(text)
        return root

    def test_unlisted_page_with_markup_fails(self):
        root = self.repo({"docs/a.md": '<!-- code test {"testId": "x"} -->', "docs/plain.md": "no tests"})
        found = plan_runs.problems([], repo_root=root)
        self.assertEqual(len(found), 1)
        self.assertIn("docs/a.md has test markup but isn't in test-pages.json", found[0])

    def test_table_and_ui_tests_count_as_markup(self):
        root = self.repo({"docs/t.md": '<!-- table test {"testId": "x"} -->', "docs/u.md": '<!-- test {"testId": "y"} -->'})
        self.assertEqual(len(plan_runs.problems([], repo_root=root)), 2)

    def test_invalid_entries(self):
        root = self.repo({"docs/a.md": "", "docs/b.md": ""})
        bad = [entry("docs/a.md", 4, "A b"), entry("docs/missing.md", 1, "x"), entry("docs/b.md", True, "y", propose_fixes=True)]
        del bad[1]["watch"]
        found = "\n".join(plan_runs.problems(bad, repo_root=root))
        self.assertIn("priority must be 1, 2, or 3", found)
        self.assertIn("name must be lowercase", found)
        self.assertIn("no such page", found)
        self.assertIn('needs "watch"', found)
        self.assertIn('needs "priority" (int)', found)  # true isn't a priority
        self.assertIn('propose_fixes needs "fix_branch"', found)

    def test_duplicates(self):
        root = self.repo({"docs/a.md": ""})
        found = "\n".join(plan_runs.problems([entry("docs/a.md", 1, "a"), entry("docs/a.md", 2, "a")], repo_root=root))
        self.assertIn("page 'docs/a.md' is used by another entry", found)
        self.assertIn("name 'a' is used by another entry", found)


class PlanTest(unittest.TestCase):
    def names(self, matrix):
        return [e["name"] for e in matrix["include"]]

    def test_weekly_runs_priority_1(self):
        self.assertEqual(self.names(plan_runs.plan(ENTRIES, "schedule", schedule=plan_runs.WEEKLY_CRON)), ["a"])

    def test_monthly_runs_priority_2(self):
        self.assertEqual(self.names(plan_runs.plan(ENTRIES, "schedule", schedule=plan_runs.MONTHLY_CRON)), ["b"])

    def test_unknown_schedule_fails(self):
        with self.assertRaises(SystemExit):
            plan_runs.plan(ENTRIES, "schedule", schedule="0 0 * * *")

    def test_on_demand_by_priority_page_or_all(self):
        self.assertEqual(self.names(plan_runs.plan(ENTRIES, "workflow_dispatch", priority="3")), ["c"])
        self.assertEqual(self.names(plan_runs.plan(ENTRIES, "workflow_dispatch", priority="all")), ["a", "b", "c"])
        self.assertEqual(self.names(plan_runs.plan(ENTRIES, "workflow_dispatch", priority="1", page="docs/c.md")), ["c"])
        with self.assertRaises(SystemExit):
            plan_runs.plan(ENTRIES, "workflow_dispatch", page="docs/nope.md")

    def push(self, changed, decide=always):
        return [e["name"] for e, _ in plan_runs.plan_push(copy.deepcopy(ENTRIES), "a" * 40, "b" * 40, changed=changed, decide=decide)]

    def test_push_runs_the_changed_page_never_priority_3(self):
        self.assertEqual(self.push(["docs/a.md"]), ["a"])
        self.assertEqual(self.push(["docs/c.md"]), [])

    def test_push_runs_on_watched_files_and_tooling(self):
        self.assertEqual(self.push(["assets/pdfs/a.pdf"]), ["a"])
        self.assertEqual(self.push(["scripts/doc-detective/run.sh"]), ["a", "b"])
        self.assertEqual(self.push(["scripts/doc-detective/test-pages.json"]), ["a", "b"])

    def test_push_skips_unrelated_changes_and_prose_only_edits(self):
        self.assertEqual(self.push(["docs/other.md"]), [])
        self.assertEqual(self.push(["docs/a.md"], decide=never), [])

    def test_push_without_a_previous_commit_runs_priority_1_and_2(self):
        runs = plan_runs.plan_push(ENTRIES, "0" * 40, "b" * 40, decide=never)
        self.assertEqual([e["name"] for e, _ in runs], ["a", "b"])


class OutputTest(unittest.TestCase):
    def test_matrix_is_json_with_the_entries(self):
        matrix = plan_runs.plan(ENTRIES, "workflow_dispatch", priority="2")
        self.assertEqual(json.loads(json.dumps(matrix))["include"][0]["page"], "docs/b.md")


if __name__ == "__main__":
    unittest.main()
