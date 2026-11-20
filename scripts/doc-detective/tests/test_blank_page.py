"""Code tests without a document run on a blank page, and --probe-blank finds examples that don't read theirs."""

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

import code_tests
from codetests import markup, record, runner, settings
from codetests.errors import RUNNER_ERROR, CodeTestError
from codetests.reports import text
from codetests.sensible import SensibleClient

from tests.fakes import BLANK_PAGE, FakeClient, write_page

DOCUMENTED = {"greeting": {"value": "I love pie", "type": "string"}}

# A test that names a document, and one that doesn't
WITH_DOCUMENT = """<!-- code test {"testId": "with_document", "description": "names a document"} -->
<!-- inline document -->
| Example document | [Download link](https://example.test/a.pdf) |
<!-- inline config -->
```json
{"fields": [{"id": "greeting", "method": {"id": "customComputation", "jsonLogic": {"cat": ["I love", " pie"]}}}]}
```
<!-- inline output -->
```json
{"greeting": {"value": "I love pie", "type": "string"}}
```
<!-- code test end -->
"""


class BlankDocumentMarkupTest(unittest.TestCase):
    def parse(self, text):
        return markup.parse_page(write_page(self, text))

    def assertMalformed(self, text, message):
        with self.assertRaises(CodeTestError) as caught:
            self.parse(text)
        self.assertEqual(caught.exception.category, "DOCS_MALFORMED")
        self.assertIn(message, str(caught.exception))

    def test_a_test_without_a_document_runs_on_the_blank_page(self):
        test = self.parse(BLANK_PAGE).code_tests["no_document"]
        self.assertEqual((test.document_url, test.blank_document), (settings.BLANK_DOCUMENT_URL, True))
        config, output = markup.check_syntax(test)
        self.assertEqual(output, DOCUMENTED)
        self.assertFalse(self.parse(WITH_DOCUMENT).code_tests["with_document"].blank_document)

    def test_check_syntax_accepts_it(self):
        out = io.StringIO()
        with mock.patch.object(sys, "argv", ["code_tests.py", "--file", write_page(self, BLANK_PAGE), "--check-syntax"]), \
             mock.patch.object(settings, "load_dotenv", lambda *a, **k: None), redirect_stdout(out):
            self.assertEqual(code_tests.main(), 0)
        self.assertIn("PASS no_document  syntax", out.getvalue())

    def test_list_says_it_runs_on_a_blank_page(self):
        out = io.StringIO()
        with mock.patch.object(sys, "argv", ["code_tests.py", "--file", write_page(self, BLANK_PAGE), "--list"]), \
             mock.patch.object(settings, "load_dotenv", lambda *a, **k: None), redirect_stdout(out):
            self.assertEqual(code_tests.main(), 0)
        self.assertIn("no_document  (line 1)  (no document: runs on a blank page)", out.getvalue())

    def test_tests_that_need_a_document_still_require_one(self):
        fixture = """<!-- code test {"testId": "seg", "segment_documents_with": "fingerprints"} -->
<!-- fixture {"name": "fixture_fp_demo_last_fails"} -->
<!-- expect {"compare": "documents", "documents": []} -->
<!-- code test end -->
"""
        self.assertMalformed(fixture, "seg: missing <!-- inline document -->")
        fingerprint = """<!-- code test {"testId": "fp"} -->
<!-- inline config {"fragment": "fingerprint"} -->
```json
"fingerprint": {"tests": [{"type": "includes", "text": "x"}]},
```
<!-- expect {"compare": "fingerprint", "passes": true} -->
<!-- code test end -->
"""
        self.assertMalformed(fingerprint, "fp: missing <!-- inline document -->")

    def test_another_test_cant_reuse_the_blank_page_as_its_document(self):
        reuse = BLANK_PAGE + WITH_DOCUMENT.replace('"with_document"', '"reuse"').replace(
            "<!-- inline document -->\n| Example document | [Download link](https://example.test/a.pdf) |",
            '<!-- inline document {"from": "no_document"} -->')
        self.assertMalformed(reuse, "names no code test with its own document link")

    def test_the_blank_page_is_in_the_repo_at_the_url_path(self):
        self.assertTrue(settings.BLANK_DOCUMENT_URL.endswith("/v0/" + os.path.relpath(settings.BLANK_DOCUMENT_PDF, settings.REPO_ROOT)))
        with open(settings.BLANK_DOCUMENT_PDF, "rb") as f:
            self.assertTrue(f.read().startswith(b"%PDF-"))


class BlankDocumentRunTest(unittest.TestCase):
    def setUp(self):
        envelopes = tempfile.TemporaryDirectory()
        self.addCleanup(envelopes.cleanup)
        patcher = mock.patch.dict(os.environ, {settings.ENVELOPES_DIR_VAR: envelopes.name})
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_runner_extracts_the_blank_page_and_the_record_says_so(self):
        test = markup.parse_page(write_page(self, BLANK_PAGE)).code_tests["no_document"]
        client = FakeClient(DOCUMENTED)
        rec = runner.run_code_test(test, client, judge_key=None)
        record.validate(rec)
        self.assertEqual(rec["status"], "pass", rec.get("message"))
        self.assertEqual(client.urls, [settings.BLANK_DOCUMENT_URL])
        self.assertEqual((rec["document_url"], rec["blank_document"]), (settings.BLANK_DOCUMENT_URL, True))
        self.assertIn("no_document: names no document, so it ran on a blank page", text.summary(rec))


class ProbeBlankTest(unittest.TestCase):
    """code_tests.py --probe-blank, with a fake client: no keys, no network."""

    def probe(self, client, page=WITH_DOCUMENT + BLANK_PAGE, extra=(), env=None):
        out, err = io.StringIO(), io.StringIO()
        env = {settings.SENSIBLE_KEY_VAR: "fake-test-key"} if env is None else env
        with mock.patch.dict(os.environ, env, clear=True), \
             mock.patch.object(settings, "load_dotenv", lambda *a, **k: None), \
             mock.patch.object(code_tests, "SensibleClient", lambda key: client), \
             mock.patch.object(sys, "argv", ["code_tests.py", "--file", write_page(self, page), "--probe-blank", *extra]), \
             redirect_stdout(out), redirect_stderr(err):
            code = code_tests.main()
        return code, out.getvalue(), err.getvalue()

    def test_unchanged_when_the_blank_page_gives_the_documented_output(self):
        client = FakeClient({"greeting": {"value": "something else", "type": "string"}}, by_url={settings.BLANK_DOCUMENT_URL: DOCUMENTED})
        code, out, err = self.probe(client)
        self.assertEqual(code, 0)
        results = json.loads(out)  # stdout is only the JSON
        self.assertEqual([(r["testId"], r["unchanged"]) for r in results], [("with_document", True)])
        self.assertEqual(set(results[0]), {"testId", "unchanged", "detail"})
        self.assertEqual(client.urls, [settings.BLANK_DOCUMENT_URL])  # never the page's own document
        self.assertIn("SKIP no_document: names no document", err)

    def test_changed_when_the_blank_page_gives_empty_values(self):
        client = FakeClient(DOCUMENTED, by_url={settings.BLANK_DOCUMENT_URL: {"greeting": None}})
        code, out, _ = self.probe(client, extra=["--test", "with_document"])
        self.assertEqual(code, 0)
        [result] = json.loads(out)
        self.assertEqual((result["testId"], result["unchanged"]), ("with_document", False))
        self.assertIn("$.greeting", result["detail"])

    def test_cant_run_without_a_key(self):
        code, out, err = self.probe(FakeClient(DOCUMENTED), env={})
        self.assertEqual((code, out), (2, ""))
        self.assertIn(settings.SENSIBLE_KEY_VAR, err)

    def test_cant_run_when_the_blank_page_doesnt_resolve(self):
        code, out, err = self.probe(FakeClient(DOCUMENTED, status=404))
        self.assertEqual((code, out), (2, ""))
        self.assertIn("returned 404", err)

    def test_an_error_is_reported_redacted(self):
        client = FakeClient(DOCUMENTED)
        client.extract = mock.Mock(side_effect=RuntimeError("401 for key fake-test-key"))
        code, out, _ = self.probe(client)
        self.assertEqual(code, 0)
        [result] = json.loads(out)
        self.assertEqual((result["unchanged"], result["error"]), (False, RUNNER_ERROR))
        self.assertNotIn("fake-test-key", out)
        self.assertIn("********", result["detail"])

    def test_respects_the_per_run_extraction_cap(self):
        client = SensibleClient("fake-test-key")
        with mock.patch.object(client, "create_sample_doc_type", return_value="t1"), mock.patch.object(client, "publish_config"), \
             mock.patch.object(client, "add_reference"), mock.patch.object(client, "document_status", return_value=200):
            code, out, _ = self.probe(client, env={settings.SENSIBLE_KEY_VAR: "fake-test-key", settings.MAX_EXTRACTIONS_VAR: "0"})
        self.assertEqual(code, 0)
        [result] = json.loads(out)
        self.assertEqual((result["unchanged"], result["error"]), (False, RUNNER_ERROR))
        self.assertIn("per-run cap is 0", result["detail"])


if __name__ == "__main__":
    unittest.main()
