"""The claim-kind registry: every kind is complete, and a new kind needs only its module and schema."""

import glob
import json
import os
import shutil
import tempfile
import types
import unittest
from unittest import mock

import test_matrix
from codetests import kinds, markup, record, runner, settings
from codetests.errors import CodeTestError
from codetests.reports import html, summary, text

from tests.fakes import write_page

INTERFACE = ["NAME", "LABEL", "RECORD_KEY", "parse_expect", "validate", "check", "run", "sample_doc_types",
             "probeable", "shows_document", "text", "html", "details", "checked"]


class RegistryTest(unittest.TestCase):
    def test_every_kind_defines_the_interface(self):
        for name, kind in kinds.KINDS.items():
            for attr in INTERFACE:
                self.assertTrue(hasattr(kind, attr), f"{name} has no {attr}")
            self.assertEqual(kind.NAME, name)

    def test_compares_are_every_kind_but_output(self):
        self.assertEqual(set(kinds.COMPARES), set(kinds.KINDS) - {"output"})

    def test_the_schema_has_every_kind_and_section_and_no_orphans(self):
        schema = record.schema()
        self.assertEqual(schema["properties"]["kind"]["enum"], list(kinds.KINDS))
        for kind in kinds.KINDS.values():
            if kind.RECORD_KEY:
                self.assertIn("properties", schema["properties"][kind.RECORD_KEY])
        files = {os.path.basename(f)[:-len(".schema.json")] for f in glob.glob(os.path.join(settings.SCHEMAS_DIR, "kinds", "*.schema.json"))}
        self.assertEqual(files, {name for name, kind in kinds.KINDS.items() if kind.RECORD_KEY})

    def test_a_record_needs_a_registered_kind(self):
        with self.assertRaises(Exception):
            record.validate({"test_id": "t", "kind": "nope", "description": "", "file": "p.md", "document_url": "", "status": "pass", "warnings": []})


# A made-up kind: "the document has this many pages". It's built here, as a new kind would be in
# codetests/kinds/, and registered only in KINDS (and COMPARES, which kinds/__init__.py derives from it)
def _page_count():
    from codetests.errors import DOCS_MALFORMED
    from codetests.kinds.common import check_document, require_document, require_no_portfolio

    kind = types.SimpleNamespace(NAME="page_count", LABEL="page count", RECORD_KEY="page_count")

    def parse_expect(options, test_id, where):
        if type(options.get("pages")) is not int:
            raise CodeTestError(DOCS_MALFORMED, f"{test_id}: a \"page_count\" expect needs \"pages\" ({where})")
        return options["pages"]

    def validate(test, seen, where):
        require_document(test, seen, where)
        require_no_portfolio(test, where)

    def run(rec, test, client, **_):
        check_document(client, test.document_url)
        rec["page_count"] = {"expected": test.expect, "actual": client.pages}
        if client.pages != test.expect:
            raise CodeTestError("PAGE_COUNT_DRIFT", f"the page claims {test.expect} pages, but the document has {client.pages}")

    kind.__dict__.update(
        parse_expect=parse_expect, validate=validate, check=lambda test: (None, test.expect), run=run,
        sample_doc_types=lambda test: [], probeable=lambda test: False, shows_document=lambda rec: True,
        text=lambda rec: [f"{rec['test_id']}: page count {rec['page_count']['actual']}"] if rec.get("page_count") else [],
        html=lambda rec, links: [f"<h3>Page count</h3><p>{rec['page_count']['actual']}</p>"] if rec.get("page_count") else [],
        details=lambda test, rec: f"{test.test_id}: {test.expect} pages",
        checked=lambda test, rec: f"{test.test_id}: {test.expect} pages",
    )
    return kind


PAGE = """# Example

<!-- code test {"testId": "two_pages", "description": "The example document has two pages"} -->
<!-- inline document -->
[Download the example](https://example.test/doc.pdf)
<!-- expect {"compare": "page_count", "pages": 2} -->
<!-- code test end -->
"""


class Client:
    def __init__(self, pages):
        self.pages = pages

    def document_status(self, url):
        return 200


class NewKindTest(unittest.TestCase):
    def setUp(self):
        kind = _page_count()
        schemas = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, schemas)
        shutil.copytree(settings.SCHEMAS_DIR, schemas, dirs_exist_ok=True)
        with open(os.path.join(schemas, "kinds", "page_count.schema.json"), "w") as f:
            json.dump({"type": "object", "additionalProperties": False, "required": ["expected", "actual"],
                       "properties": {"expected": {"type": "integer"}, "actual": {"type": "integer"}}}, f)
        for patcher in (mock.patch.dict(kinds.KINDS, {"page_count": kind}),
                        mock.patch.object(kinds, "COMPARES", kinds.COMPARES + ("page_count",)),
                        mock.patch.object(settings, "SCHEMAS_DIR", schemas)):
            patcher.start()
            self.addCleanup(patcher.stop)
        self.path = write_page(self, PAGE)

    def test_it_parses_runs_records_and_reports(self):
        page = markup.parse_page(self.path)
        test = page.code_tests["two_pages"]
        self.assertEqual((test.compare, test.expect), ("page_count", 2))

        passed = runner.run_code_test(test, Client(2))
        self.assertEqual((passed["status"], passed["kind"], passed["page_count"]), ("pass", "page_count", {"expected": 2, "actual": 2}))
        record.validate(passed)
        failed = runner.run_code_test(test, Client(3))
        self.assertEqual((failed["status"], failed["category"]), ("fail", "PAGE_COUNT_DRIFT"))
        record.validate(failed)

        self.assertIn("<h3>Page count</h3>", html.render_code_test(passed))
        self.assertIn("two_pages: page count 2", text.summary(passed))
        self.assertEqual(summary.test_rows(page, {}, [passed]), [("two_pages", "Code test", "pass", "two_pages: 2 pages")])
        self.assertEqual(test_matrix.tests(self.path), [("two_pages", "page count", "The example document has two pages", [])])

    def test_its_markup_rules_apply(self):
        with self.assertRaises(CodeTestError) as caught:
            markup.parse_page(write_page(self, PAGE.replace('"pages": 2', '"pages": "two"')))
        self.assertIn('a "page_count" expect needs "pages"', str(caught.exception))
        with self.assertRaises(CodeTestError) as caught:
            markup.parse_page(write_page(self, PAGE.replace("<!-- inline document -->\n", "")))
        self.assertIn("missing <!-- inline document -->", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
