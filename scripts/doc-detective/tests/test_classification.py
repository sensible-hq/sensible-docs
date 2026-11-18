"""Classification claims: files sent to the classify endpoint with a content type."""

import json
import os
import unittest

from codetests import markup, record, runner, settings
from codetests.kinds import classification
from codetests import sensible
from codetests.errors import CodeTestError
from codetests.reports import html, text

from tests.fakes import write_page

# A temporary repo (setUpModule), so the tests don't depend on real fixtures or files. The test files
# are in the fixture's folder, fx/spreadsheets; requests name them relative to it
XLSB = "xlsb_sample.xlsb"
CSV = "csv_sample.csv"
FOLDER = "fx/spreadsheets"
FIXTURE = "fixture_spreadsheet_classify"
_ROOT = None
_SAVED = None


def setUpModule():
    """A temporary repo with the test files and a fixture whose reference document is a spreadsheet."""
    import os
    import tempfile

    global _ROOT, _SAVED
    _ROOT = tempfile.TemporaryDirectory()
    root = _ROOT.name
    os.makedirs(os.path.join(root, "assets", "pdfs"))
    with open(os.path.join(root, "assets", "pdfs", "docs.pdf"), "wb") as f:
        f.write(b"docs pdf")
    folder = os.path.join(root, FOLDER)
    os.makedirs(folder)
    for name in (XLSB, CSV):
        with open(os.path.join(folder, name), "wb") as f:
            f.write(b"test file")
    with open(os.path.join(folder, f"{FIXTURE}.doctype.json"), "w") as f:
        json.dump({"name": FIXTURE, "schema": {"description": "A small test spreadsheet whose cells say hello"}}, f)
    with open(os.path.join(folder, f"{FIXTURE}.fixture_spreadsheet_sample.config.json"), "w") as f:
        json.dump({"fields": []}, f)
    with open(os.path.join(folder, "manifest.json"), "w") as f:
        json.dump({"document_types": [{"doctype": f"{FIXTURE}.doctype.json", "references": [
            {"name": "fixture_xlsb_sample", "file": XLSB, "configuration": "fixture_spreadsheet_sample"}]}]}, f)
    _SAVED = settings.TEST_FIXTURES_DIR, settings.REPO_ROOT, settings.DOCS_PDFS_DIR
    settings.TEST_FIXTURES_DIR, settings.REPO_ROOT, settings.DOCS_PDFS_DIR = os.path.join(root, "fx"), root, os.path.join(root, "assets", "pdfs")


def tearDownModule():
    settings.TEST_FIXTURES_DIR, settings.REPO_ROOT, settings.DOCS_PDFS_DIR = _SAVED
    _ROOT.cleanup()

FIXTURE_MARKER = f'<!-- fixture {{"name": "{FIXTURE}"}} -->\n'


def page(requests, extra=FIXTURE_MARKER):
    expect = {"compare": "classification", "requests": requests}
    return (f'<!-- code test {{"testId": "classify_formats", "description": "Which spreadsheets Sensible classifies"}} -->\n'
            f"{extra}<!-- expect {json.dumps(expect)} -->\n<!-- code test end -->\n")


REQUESTS = [
    {"file": XLSB, "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "classified": True},
    {"file": CSV, "content_type": "text/csv", "classified": False, "label": "CSV"},
]


class FakeClassifyClient:
    """Classifies a file as the doc type when its content type is in `classifies`."""

    def __init__(self, classifies, restored=()):
        self.classifies, self.ensured, self.sent, self.restored = classifies, [], [], list(restored)
        self.counts = {"requests": 0, "extractions": 0, "by_call": {}}

    def ensure_fixture(self, doctype_file, config_file, references=()):
        self.ensured.append((doctype_file, config_file, [r["name"] for r in references]))
        return FIXTURE, "fixture_spreadsheet_sample", self.restored

    def classify(self, path, content_type, doc_type):
        self.sent.append((path, content_type, doc_type))
        if content_type in self.classifies:
            return 200, json.dumps({"document_type": {"name": doc_type}}), doc_type
        return 400, "Missing request body", ""


class MarkupTest(unittest.TestCase):
    def parse(self, text):
        return markup.parse_page(write_page(self, text)).code_tests

    def malformed(self, text, message):
        with self.assertRaises(CodeTestError) as caught:
            for test in self.parse(text).values():
                markup.check_syntax(test)
        self.assertEqual(caught.exception.category, "DOCS_MALFORMED")
        self.assertIn(message, str(caught.exception))

    def test_parses_requests_without_a_document(self):
        test = self.parse(page(REQUESTS))["classify_formats"]
        self.assertEqual(test.compare, "classification")
        self.assertFalse(test.blank_document)
        self.assertEqual(test.document_url, "")
        _, expect = markup.check_syntax(test)
        self.assertEqual([r["classified"] for r in expect["requests"]], [True, False])

    def test_as_names_a_content_type_by_its_extension(self):
        test = self.parse(page([{"file": XLSB, "as": "xlsx", "classified": True}, {"file": XLSB, "as": "pdf", "classified": True}]))["classify_formats"]
        self.assertEqual([r["content_type"] for r in test.expect["requests"]],
                         ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/pdf"])
        self.assertTrue(all("as" not in r for r in test.expect["requests"]))  # expanded, so runs and reports see the MIME type

    def test_as_must_be_a_known_extension_and_not_beside_content_type(self):
        self.malformed(page([{"file": XLSB, "as": "docx", "classified": True}]), "\"as\": one of pdf, xlsx, xls, xlsm, xlsb, csv")
        self.malformed(page([{"file": XLSB, "as": "xlsx", "content_type": "text/csv", "classified": True}]), "needs only \"requests\"")
        self.malformed(page([{"file": XLSB, "classified": True}]), "needs only \"requests\"")

    def test_needs_requests(self):
        self.malformed(page([]), "needs only \"requests\"")

    def test_request_needs_a_boolean_claim(self):
        self.malformed(page([{"file": XLSB, "content_type": "text/csv", "classified": "no"}]), "needs only \"requests\"")

    def test_unknown_request_key(self):
        self.malformed(page([{"file": XLSB, "content_type": "text/csv", "classified": True, "url": "x"}]), "needs only \"requests\"")

    def test_needs_exactly_one_fixture(self):
        self.malformed(page(REQUESTS, extra=""), "needs exactly one <!-- fixture -->")
        self.malformed(page(REQUESTS, extra=FIXTURE_MARKER * 2), "needs exactly one <!-- fixture -->")

    def test_fixture_must_exist(self):
        self.malformed(page(REQUESTS, extra='<!-- fixture {"name": "fixture_no_such_type"} -->\n'), "no fixture_no_such_type.doctype.json")

    def test_file_must_exist_in_the_fixture_folder(self):
        self.malformed(page([{"file": "missing.xlsb", "content_type": "text/csv", "classified": False}]), f"must be a file in {FOLDER}")

    def test_file_cant_leave_the_fixture_folder(self):
        import os
        with open(os.path.join(settings.REPO_ROOT, ".env"), "w") as f:
            f.write("SECRET=x")
        for name in ("../../.env", "/etc/hostname"):
            self.malformed(page([{"file": name, "content_type": "text/plain", "classified": False}]), f"must be a file in {FOLDER}")
        self.malformed(page([{"docs_pdf": "../../.env", "content_type": "text/plain", "classified": False}]), "must be a file in assets/pdfs")

    def test_symlink_out_of_the_fixture_folder_is_rejected(self):
        import os
        outside = os.path.join(settings.REPO_ROOT, "outside.csv")
        with open(outside, "w") as f:
            f.write("a,b")
        link = os.path.join(settings.REPO_ROOT, FOLDER, "link.csv")
        os.symlink(outside, link)
        self.addCleanup(os.remove, link)
        self.malformed(page([{"file": "link.csv", "content_type": "text/csv", "classified": False}]), f"must be a file in {FOLDER}")

    def test_request_names_exactly_one_file(self):
        self.malformed(page([{"file": XLSB, "docs_pdf": "docs.pdf", "content_type": "text/csv", "classified": False}]), "needs only \"requests\"")
        self.malformed(page([{"content_type": "text/csv", "classified": False}]), "needs only \"requests\"")

    def test_docs_pdf_request(self):
        test = markup.parse_page(write_page(self, page([{"docs_pdf": "docs.pdf", "content_type": "application/pdf", "classified": True}]))).code_tests["classify_formats"]
        rec = runner.run_code_test(test, FakeClassifyClient({"application/pdf"}))
        self.assertEqual(rec["status"], "pass", rec.get("message"))
        self.assertEqual(rec["classification"]["runs"][0]["file"], "assets/pdfs/docs.pdf")

    def test_takes_no_inline_document(self):
        doc = "<!-- inline document -->\n| Example document | [Download link](https://example.test/a.pdf) |\n"
        self.malformed(page(REQUESTS, FIXTURE_MARKER + doc), "takes no inline document")


class RunnerTest(unittest.TestCase):
    def run_test(self, classifies):
        test = markup.parse_page(write_page(self, page(REQUESTS))).code_tests["classify_formats"]
        client = FakeClassifyClient(classifies)
        return runner.run_code_test(test, client), client

    def test_pass_records_each_request_against_the_fixture(self):
        rec, client = self.run_test({"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})
        self.assertEqual(rec["status"], "pass", rec.get("message"))
        record.validate(rec)
        self.assertEqual([e[2] for e in client.ensured], [["fixture_xlsb_sample"]])
        self.assertTrue(all(sent[2] == FIXTURE for sent in client.sent))
        cl = rec["classification"]
        self.assertEqual(cl["fixture"], FIXTURE)
        self.assertIn("app.sensible.so/editor/", cl["editor"])
        self.assertIn("hello", cl["doc_type_description"])  # read from the committed doc type file
        self.assertEqual([r["actual"] for r in cl["runs"]], [True, False])
        self.assertEqual(cl["runs"][1]["label"], "CSV")
        curl = cl["runs"][1]["curl"]
        self.assertIn(f"/classify?document_types={FIXTURE}", curl)
        self.assertIn(f"-H 'Content-Type: text/csv' --data-binary @{FOLDER}/csv_sample.csv", curl)
        self.assertIn('"Authorization: Bearer $SENSIBLE_TEST_API_KEY"', curl)

    def test_drift_fails(self):
        rec, _ = self.run_test({"text/csv"})
        self.assertEqual(rec["status"], "fail")
        self.assertEqual(rec["category"], "CLASSIFICATION_DRIFT")
        self.assertIn("csv_sample.csv sent as text/csv", rec["message"])
        self.assertIn("xlsb_sample.xlsb", rec["message"])
        record.validate(rec)

    def test_restored_fixture_warns(self):
        test = markup.parse_page(write_page(self, page(REQUESTS))).code_tests["classify_formats"]
        rec = runner.run_code_test(test, FakeClassifyClient({"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}, ["config edited"]))
        self.assertEqual(rec["status"], "warn")
        self.assertIn("fixture restored", html.render_code_test(rec))

    def test_reports_render_the_runs(self):
        rec, _ = self.run_test({"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})
        # A report in output/ or reports/ (two folders below scripts/) links to repo files three folders up
        rendered = html.render_code_test(rec, html.Links(os.path.join(settings.REPO_ROOT, "scripts", "doc-detective", "output", "report.html")))
        elsewhere = html.render_code_test(rec, html.Links(os.path.join(settings.REPO_ROOT, "report.html")))
        self.assertIn('href="fx/spreadsheets/csv_sample.csv"', elsewhere)
        lines = "\n".join(text.summary(rec))
        self.assertIn("classification (compared exactly)", lines)
        self.assertIn("csv_sample.csv as text/csv (CSV): page claims not classified; Sensible not classified", lines)
        test = markup.parse_page(write_page(self, page(REQUESTS))).code_tests["classify_formats"]
        self.assertEqual(html.details_label(test, rec), "classify_formats: classification, 1 classified and 1 not")
        self.assertIn("<h3>Classification</h3>", rendered)
        self.assertNotIn("Example document:", rendered)
        self.assertIn(f'href="../../../{FOLDER}/csv_sample.csv"', rendered)
        self.assertIn("open in the SenseML editor", rendered)
        self.assertIn("curl -s", rendered)


if __name__ == "__main__":
    unittest.main()


class SpreadsheetReferenceTest(unittest.TestCase):
    def test_fixture_references_can_be_spreadsheets(self):
        refs = markup.fixture_references(FIXTURE)
        import os
        self.assertEqual(refs[0]["path"], os.path.realpath(os.path.join(settings.REPO_ROOT, FOLDER, XLSB)))

    def test_spreadsheet_content_types(self):
        self.assertEqual(settings.REFERENCE_CONTENT_TYPES[".xlsb"], "application/vnd.ms-excel.sheet.binary.macroenabled.12")
        self.assertEqual(settings.REFERENCE_CONTENT_TYPES[".pdf"], "application/pdf")


class CurlCommandTest(unittest.TestCase):
    def test_values_from_the_page_are_shell_quoted(self):
        import shlex
        curl = classification.curl_command("/classify", "fixture_x", 'text/csv"; rm -rf ~ #', "scripts/doc-detective/fixtures/spreadsheets/types test.csv")
        words = shlex.split(curl)
        self.assertIn('Content-Type: text/csv"; rm -rf ~ #', words)
        self.assertIn("@scripts/doc-detective/fixtures/spreadsheets/types test.csv", words)
        self.assertNotIn("rm", words)


class ClassifyResponseTest(unittest.TestCase):
    """SensibleClient.classify: which responses mean "not classified", and which fail the test."""

    def client(self, status, body):
        class Response:
            def __init__(self):
                self.status_code, self.text, self.ok = status, body if isinstance(body, str) else json.dumps(body), 200 <= status < 300

            def json(self):
                return json.loads(self.text)

        class Client(sensible.SensibleClient):
            def _api(self, method, path, **kwargs):
                self.sent = (method, path, kwargs.get("params"), kwargs.get("headers"))
                return Response()

        return Client("key")

    def classify(self, status, body):
        import os
        client = self.client(status, body)
        return client.classify(os.path.join(settings.REPO_ROOT, FOLDER, CSV), "text/csv", FIXTURE), client

    def test_classified(self):
        (status, _, name), client = self.classify(200, {"document_type": {"name": FIXTURE}})
        self.assertEqual((status, name), (200, FIXTURE))
        self.assertEqual(client.sent, ("POST", "/classify", {"document_types": FIXTURE}, {"Content-Type": "text/csv"}))

    def test_rejections_mean_not_classified(self):
        for status in (400, 415):
            (got, _, name), _ = self.classify(status, "Missing request body")
            self.assertEqual((got, name), (status, ""))

    def test_errors_that_say_nothing_about_the_file_fail(self):
        from codetests.errors import CodeTestError
        for status in (401, 429, 500, 502):
            with self.assertRaises(CodeTestError) as caught:
                self.classify(status, "unavailable")
            self.assertEqual(caught.exception.category, "RUNNER_ERROR")
            self.assertIn(f"HTTP {status}", str(caught.exception))

    def test_a_200_that_isnt_a_classification_fails(self):
        from codetests.errors import CodeTestError
        for body in ("<html>gateway</html>", "[]", "{}", '{"document_type": null}', '{"document_type": {"name": null}}',
                     '{"document_type": {"name": ""}}', '{"document_type": {"name": "other_type"}}'):
            with self.assertRaises(CodeTestError) as caught:
                self.classify(200, body)
            self.assertEqual(caught.exception.category, "RUNNER_ERROR")
