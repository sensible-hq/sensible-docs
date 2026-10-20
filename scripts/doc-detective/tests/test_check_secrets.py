"""Offline tests for check_secrets.py: the fail-closed leak scan and the coverage rules."""

import base64
import glob
import html
import json
import os
import tempfile
import unittest
import urllib.parse

import check_secrets as cs

# Has characters each encoding changes (" < > &), so every encoded form is distinct
SECRET = 'pw"Ex<am>ple&12345'


class LeakScanTest(unittest.TestCase):
    def scan(self, content, secrets=None, name="report.json"):
        with tempfile.TemporaryDirectory() as out:
            os.makedirs(os.path.join(out, "runs", "x"))
            with open(os.path.join(out, "runs", "x", name), "w", encoding="utf-8") as f:
                f.write(content)
            return cs.scan(out, {"SENSIBLE_TEST_PASSWORD": SECRET} if secrets is None else secrets)

    def test_finds_the_value_in_every_encoding_and_nested_file(self):
        for label, form in [
            ("as written", SECRET),
            ("JSON-escaped", json.dumps(SECRET)[1:-1]),
            ("HTML-escaped", html.escape(SECRET)),
            ("URL-encoded", urllib.parse.quote(SECRET, safe="")),
            ("base64", base64.b64encode(SECRET.encode()).decode()),
        ]:
            with self.subTest(label):
                findings = self.scan(f"keys: {form}")
                self.assertTrue(any(label in what for _, what in findings), findings)

    def test_findings_never_contain_the_value(self):
        findings = self.scan(f"keys: {SECRET}")
        self.assertTrue(findings)
        self.assertFalse(any(SECRET in f"{rel} {what}" for rel, what in findings))

    def test_scrubbed_output_passes(self):
        self.assertEqual(self.scan('{"keys": "********", "Authorization": "Bearer ********"}'), [])

    def test_any_file_type_is_scanned(self):
        self.assertTrue(self.scan(SECRET, name="trace.bin"))

    def test_unregistered_credentials_are_caught(self):
        for label, text in [
            ("Anthropic API key", "sk-ant-api03-" + "a" * 40),
            ("Bearer token", "Authorization: Bearer abcdefghijklmnopqrstuvwxyz0123"),
            ("GitHub token", "ghp_" + "A" * 36),
            ("AWS access key ID", "AKIA" + "ABCDEFGHIJKLMNOP"),
        ]:
            with self.subTest(label):
                findings = self.scan(text, secrets={})
                self.assertTrue(any(label in what for _, what in findings), findings)


class CoverageTest(unittest.TestCase):
    WORKFLOW = """
jobs:
  test:
    steps:
      - name: Run tests
        env:
          SENSIBLE_TEST_PASSWORD: ${{ secrets.SENSIBLE_TEST_PASSWORD }}
          NEW_TOKEN: ${{ secrets.NEW_TOKEN }}
      - name: Check for leaked secrets
        env:
          SENSIBLE_TEST_PASSWORD: ${{ secrets.SENSIBLE_TEST_PASSWORD }}
"""
    PAGE = '<!-- step {"type": {"keys": "$SENSIBLE_TEST_PASSWORD"}} -->\n<!-- step {"type": {"keys": "$NEW_VAR"}} -->\n'
    PAGE_RUNTIME = '<!-- step {"httpRequest": {"url": "$$response.body.id"}} -->\n'

    def coverage(self, workflow=None, page=None, dotenv=None, secrets=("SENSIBLE_TEST_PASSWORD",), public=()):
        with tempfile.TemporaryDirectory() as d:
            paths = {}
            for name, text in (("workflow.yml", workflow), ("page.md", page)):
                if text is not None:
                    paths[name] = os.path.join(d, name)
                    with open(paths[name], "w") as f:
                        f.write(text)
            return cs.coverage(list(secrets), list(public), dotenv or {},
                               [paths["workflow.yml"]] if "workflow.yml" in paths else [],
                               [paths["page.md"]] if "page.md" in paths else [])

    def test_unregistered_workflow_secret(self):
        problems = self.coverage(workflow=self.WORKFLOW)
        self.assertTrue(any("NEW_TOKEN is set from a GitHub secret but isn't in config/secrets.txt" in p for p in problems))

    def test_check_step_must_receive_every_secret(self):
        problems = self.coverage(workflow=self.WORKFLOW, secrets=("SENSIBLE_TEST_PASSWORD", "NEW_TOKEN"))
        self.assertTrue(any("doesn't receive NEW_TOKEN" in p for p in problems), problems)

    def test_missing_check_step(self):
        workflow = self.WORKFLOW.split("      - name: Check for leaked secrets")[0]
        problems = self.coverage(workflow=workflow, secrets=("SENSIBLE_TEST_PASSWORD", "NEW_TOKEN"))
        self.assertTrue(any("there's no \"Check for leaked secrets\" step" in p for p in problems))

    def test_unclassified_page_variable(self):
        problems = self.coverage(page=self.PAGE)
        self.assertEqual(len(problems), 1)
        self.assertIn("$NEW_VAR", problems[0])

    def test_public_variable_is_accepted(self):
        self.assertEqual(self.coverage(page=self.PAGE, public=("NEW_VAR",)), [])

    def test_runtime_expressions_are_not_variables(self):
        self.assertEqual(self.coverage(page=self.PAGE_RUNTIME), [])

    def test_unclassified_dotenv_variable(self):
        problems = self.coverage(dotenv={"SENSIBLE_TEST_PASSWORD": "x", "SOME_KEY": "y"})
        self.assertEqual(len(problems), 1)
        self.assertIn("SOME_KEY", problems[0])

    def test_name_in_both_lists(self):
        problems = self.coverage(secrets=("A_KEY",), public=("A_KEY",))
        self.assertTrue(any("in both" in p for p in problems))


class RepoCoverageTest(unittest.TestCase):
    def test_this_repo_classifies_every_secret(self):
        """The real workflow and docs pages. .env is ignored: it's local."""
        problems = cs.coverage(cs.read_names(cs.SECRETS_FILE), cs.read_names(cs.PUBLIC_FILE), {},
                               cs.workflow_files(), sorted(glob.glob(cs.DOCS_GLOB, recursive=True)))
        self.assertEqual(problems, [])

    def test_covers_every_docs_test_workflow(self):
        names = [os.path.basename(f) for f in cs.workflow_files()]
        self.assertIn("doc-tests-pages.yml", names)

    def test_reads_conditional_secret_values(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as f:
            f.write("""steps:
      - name: Run tests
        env:
          PLAIN: ${{ secrets.PLAIN }}
          CONDITIONAL: ${{ contains(matrix.secrets, 'CONDITIONAL') && secrets.CONDITIONAL || '' }}
          NOT_A_SECRET: ${{ vars.SOMETHING }}
""")
        self.addCleanup(os.remove, f.name)
        self.assertEqual(cs.workflow_secret_env(f.name), {"Run tests": {"PLAIN", "CONDITIONAL"}})

    def test_runner_key_variables_are_registered(self):
        from codetests import settings
        secrets = set(cs.read_names(cs.SECRETS_FILE))
        for name in (settings.SENSIBLE_KEY_VAR, *settings.JUDGE_KEY_VARS):
            self.assertIn(name, secrets)


if __name__ == "__main__":
    unittest.main()
