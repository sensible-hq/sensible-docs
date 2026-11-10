"""Classification claims: files sent to the classify endpoint with a content type."""

import json
import unittest

from codetests import markup, record, runner, settings
from codetests.errors import CodeTestError
from codetests.reports import html, text

from tests.fakes import write_page

# Files that exist in the repo, so check_syntax accepts them
XLSB = "scripts/test/assets/xlsb_sample.xlsb"
CSV = "scripts/test/assets/csv_sample.csv"


def page(requests, extra=""):
    expect = {"compare": "classification", "doc_type_description": "A small test spreadsheet", "requests": requests}
    return (f'<!-- code test {{"testId": "classify_formats", "description": "Which spreadsheets Sensible classifies"}} -->\n'
            f"{extra}<!-- expect {json.dumps(expect)} -->\n<!-- code test end -->\n")


REQUESTS = [
    {"file": XLSB, "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "classified": True},
    {"file": CSV, "content_type": "text/csv", "classified": False, "label": "CSV"},
]


class FakeClassifyClient:
    """Classifies a file as the doc type when its content type is in `classifies`."""

    def __init__(self, classifies):
        self.classifies, self.created, self.deleted, self.sent = classifies, [], [], []
        self.counts = {"requests": 0, "extractions": 0, "by_call": {}}

    def create_temp_doc_type(self, name, schema=None):
        self.created.append((name, schema))
        return "type-id"

    def delete_temp_doc_type(self, type_id):
        self.deleted.append(type_id)

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

    def test_needs_description_and_requests(self):
        self.malformed('<!-- code test {"testId": "c"} -->\n<!-- expect {"compare": "classification", "requests": []} -->\n<!-- code test end -->\n',
                       "needs \"doc_type_description\"")

    def test_request_needs_a_boolean_claim(self):
        self.malformed(page([{"file": XLSB, "content_type": "text/csv", "classified": "no"}]), "needs \"doc_type_description\"")

    def test_unknown_request_key(self):
        self.malformed(page([{"file": XLSB, "content_type": "text/csv", "classified": True, "url": "x"}]), "needs \"doc_type_description\"")

    def test_file_must_exist_in_the_repo(self):
        self.malformed(page([{"file": "scripts/test/assets/missing.xlsb", "content_type": "text/csv", "classified": False}]), "isn't a file in the repo")

    def test_file_cant_leave_the_repo(self):
        self.malformed(page([{"file": "../outside.csv", "content_type": "text/csv", "classified": False}]), "isn't a file in the repo")

    def test_takes_no_inline_document(self):
        doc = "<!-- inline document -->\n| Example document | [Download link](https://example.test/a.pdf) |\n"
        self.malformed(page(REQUESTS, doc), "takes no inline document")


class RunnerTest(unittest.TestCase):
    def run_test(self, classifies):
        test = markup.parse_page(write_page(self, page(REQUESTS))).code_tests["classify_formats"]
        client = FakeClassifyClient(classifies)
        return runner.run_code_test(test, client), client

    def test_pass_records_each_request_and_cleans_up(self):
        rec, client = self.run_test({"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})
        self.assertEqual(rec["status"], "pass", rec.get("message"))
        record.validate(rec)
        name = settings.TEMP_DOC_TYPE_PREFIX + "classify_formats"
        self.assertEqual(client.created, [(name, {"description": "A small test spreadsheet"})])
        self.assertEqual(client.deleted, ["type-id"])
        self.assertEqual([r["actual"] for r in rec["classification"]["runs"]], [True, False])
        self.assertEqual(rec["classification"]["runs"][1]["label"], "CSV")

    def test_drift_fails_and_still_cleans_up(self):
        rec, client = self.run_test({"text/csv"})
        self.assertEqual(rec["status"], "fail")
        self.assertEqual(rec["category"], "CLASSIFICATION_DRIFT")
        self.assertIn("csv_sample.csv sent as text/csv", rec["message"])
        self.assertIn("xlsb_sample.xlsb", rec["message"])
        self.assertEqual(client.deleted, ["type-id"])
        record.validate(rec)

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


if __name__ == "__main__":
    unittest.main()
