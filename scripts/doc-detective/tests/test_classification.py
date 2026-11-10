"""Classification claims: files sent to the classify endpoint with a content type."""

import json
import unittest

from codetests import markup, record, runner, settings
from codetests import sensible
from codetests.errors import CodeTestError
from codetests.reports import html, text

from tests.fakes import write_page

# Files that exist in the repo, so check_syntax accepts them
XLSB = "scripts/test/assets/xlsb_sample.xlsb"
CSV = "scripts/test/assets/csv_sample.csv"


FIXTURE = "fixture_spreadsheet_classify"  # committed under scripts/test/probe_endpoints/contract/fixtures/
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

    def test_file_must_exist_in_the_repo(self):
        self.malformed(page([{"file": "scripts/test/assets/missing.xlsb", "content_type": "text/csv", "classified": False}]), "isn't a file in the repo")

    def test_file_cant_leave_the_repo(self):
        self.malformed(page([{"file": "../outside.csv", "content_type": "text/csv", "classified": False}]), "isn't a file in the repo")

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
        self.assertIn(f'/classify?document_types={FIXTURE}"', curl)
        self.assertIn('-H "Content-Type: text/csv" --data-binary @scripts/test/assets/csv_sample.csv', curl)
        self.assertIn("Bearer $SENSIBLE_TEST_API_KEY", curl)
        self.assertIn('-w "\\nHTTP %{http_code}\\n"', curl)

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
        rendered = html.render_code_test(rec)
        lines = "\n".join(text.summary(rec))
        self.assertIn("classification (compared exactly)", lines)
        self.assertIn("csv_sample.csv as text/csv (CSV): page claims not classified; Sensible not classified", lines)
        test = markup.parse_page(write_page(self, page(REQUESTS))).code_tests["classify_formats"]
        self.assertEqual(html.details_label(test, rec), "classify_formats: classification, 1 classified and 1 not")
        self.assertIn("<h3>Classification</h3>", rendered)
        self.assertNotIn("Example document:", rendered)
        self.assertIn('href="../../../scripts/test/assets/csv_sample.csv"', rendered)
        self.assertIn("open in the SenseML editor", rendered)
        self.assertIn("curl -s", rendered)


if __name__ == "__main__":
    unittest.main()


class SpreadsheetReferenceTest(unittest.TestCase):
    def test_fixture_references_can_be_spreadsheets(self):
        refs = markup.fixture_references(FIXTURE)
        self.assertEqual(refs[0]["pdf"], XLSB)

    def test_reference_upload_uses_the_extension_content_type(self):
        self.assertEqual(settings.REFERENCE_CONTENT_TYPES[".xlsb"], "application/vnd.ms-excel.sheet.binary.macroenabled.12")
        self.assertEqual(settings.REFERENCE_CONTENT_TYPES[".pdf"], "application/pdf")
