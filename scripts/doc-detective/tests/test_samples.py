"""Inline fingerprint samples: the page's own configs, run in sample doc types that the report links to."""

import json
import unittest

from codetests import markup, record, runner, settings
from codetests.errors import CodeTestError

from tests.fakes import FakeClient, write_page

FRAGMENT = '''"fingerprint": {
  "tests": [
    /* a comment, as on the page */
    {"page": "first", "match": [{"type": "includes", "text": "anyco"}]}
  ]
},'''

PORTFOLIO = '''<!-- code test {"testId": "pf", "segment_documents_with": "fingerprints"} -->
<!-- inline config {"fragment": "fingerprint", "doc_type": "quotes", "config": "anyco"} -->
```json
''' + FRAGMENT + '''
```
<!-- inline config {"fragment": "fingerprint", "doc_type": "losses", "config": "acme"} -->
```json
''' + FRAGMENT + '''
```
<!-- inline document -->
| Example document | [Download link](https://example.test/p.pdf) |
<!-- inline output -->
```json
{"documents": [{"configuration": "anyco", "startPage": 0, "endPage": 0}, {"configuration": "acme", "startPage": 2, "endPage": 2}]}
```
<!-- expect {"compare": "documents"} -->
<!-- code test end -->
'''

STANDALONE = '''<!-- code test {"testId": "sa"} -->
<!-- inline config -->
```json
{"fingerprint": {"tests": [["a", "b"], "c", "d"]}, "fields": []}
```
<!-- inline document -->
| Example document | [Download link](https://example.test/s.pdf) |
<!-- expect {"compare": "fingerprint", "passes": true, "variants": [{"break": [0], "passes": true}, {"break": [0, 1], "passes": false}]} -->
<!-- code test end -->
'''


class MarkupTest(unittest.TestCase):
    def parse(self, text):
        return markup.parse_page(write_page(self, text))

    def malformed(self, text, message):
        with self.assertRaises(CodeTestError) as caught:
            test = self.parse(text).code_tests
            for t in test.values():
                markup.check_syntax(t)
        self.assertEqual(caught.exception.category, "DOCS_MALFORMED")
        self.assertIn(message, str(caught.exception))

    def test_fingerprint_fragment_is_wrapped(self):
        wrapped = markup.wrap_fingerprint_fragment(FRAGMENT)
        self.assertEqual(json.loads(wrapped.replace("/* a comment, as on the page */", ""))["fields"], [])

    def test_portfolio_samples_and_expected_documents_from_the_output(self):
        test = self.parse(PORTFOLIO).code_tests["pf"]
        self.assertEqual([(c["doc_type"], c["config"]) for c in test.inline_configs], [("quotes", "anyco"), ("losses", "acme")])
        self.assertEqual(markup.check_syntax(test), (None, [["anyco", 1, 1], ["acme", 3, 3]]))

    def test_expected_config_must_be_a_sample(self):
        self.malformed(PORTFOLIO.replace('"configuration": "acme"', '"configuration": "other"'), "name config 'other'")

    def test_sample_syntax_errors_point_at_the_page_line(self):
        page = PORTFOLIO.replace('"text": "anyco"}]}', '"text": "anyco"}]]}', 1)
        bad_line = next(n for n, line in enumerate(page.splitlines(), start=1) if '"anyco"}]]}' in line)
        self.malformed(page, f"line {bad_line})")

    def test_sample_needs_names(self):
        self.malformed(PORTFOLIO.replace(', "config": "anyco"', ""), 'needs "doc_type" and "config"')

    def test_fixtures_and_samples_dont_mix(self):
        self.malformed(PORTFOLIO.replace("<!-- inline document -->", '<!-- fixture {"name": "fixture_fp_demo_last_fails"} -->\n<!-- inline document -->'),
                       "either fixtures or inline configs")

    def test_documents_need_an_expectation(self):
        page = PORTFOLIO.split("<!-- inline output -->")[0] + '<!-- expect {"compare": "documents"} -->\n<!-- code test end -->\n'
        self.malformed(page, "no <!-- inline output --> to take them from")

    def test_standalone_fingerprint(self):
        test = self.parse(STANDALONE).code_tests["sa"]
        config, expect = markup.check_syntax(test)
        self.assertEqual(len(config["fingerprint"]["tests"]), 3)
        self.assertEqual(expect["variants"][1], {"break": [0, 1], "passes": False})

    def test_variant_must_break_an_existing_test(self):
        self.malformed(STANDALONE.replace('"break": [0, 1]', '"break": [3]'), "breaks test 3")

    def test_fingerprint_expect_needs_passes(self):
        self.malformed(STANDALONE.replace('"passes": true, "variants"', '"variants"'), 'needs "passes"')


class SampleClient(FakeClient):
    """Records sample doc types and reference documents; returns scripted portfolio documents and standalone results."""

    def __init__(self, documents=(), standalone=()):
        super().__init__({})
        self.documents, self.standalone = list(documents), list(standalone)
        self.types, self.references, self.published = {}, [], []

    def create_sample_doc_type(self, name, schema=None):
        self.types[name] = schema
        return f"id-{name}"

    def add_reference(self, type_id, name, config, pdf):
        # Like Sensible: a reference document needs its config to exist
        if (type_id, config) not in [(t, c) for t, c, _ in self.published]:
            raise CodeTestError("CONFIG_INVALID", f"Configuration {config} not found")
        self.references.append((type_id, name, config, pdf))

    def publish_config(self, type_id, name, text):
        self.published.append((type_id, name, text))

    def extract_portfolio(self, url, doc_types, document_name, environment=None):
        self.portfolio_types, self.environment = doc_types, environment
        return "e1", self.documents

    def extract_standalone(self, url, doc_type, document_name):
        return self.standalone.pop(0)


class RunnerTest(unittest.TestCase):
    def run_page(self, page, test_id, client):
        test = markup.parse_page(write_page(self, page)).code_tests[test_id]
        rec = runner.run_code_test(test, client)
        record.validate(rec)
        return rec

    def test_portfolio_samples_pass_with_editor_links(self):
        docs = [{"configuration": "anyco", "startPage": 0, "endPage": 0}, {"configuration": "acme", "startPage": 2, "endPage": 2}]
        client = SampleClient(documents=docs)
        rec = self.run_page(PORTFOLIO, "pf", client)
        self.assertEqual(rec["status"], "pass")
        quotes = f"{settings.SAMPLE_DOC_TYPE_PREFIX}pf__quotes"
        self.assertEqual(client.portfolio_types, [quotes, f"{settings.SAMPLE_DOC_TYPE_PREFIX}pf__losses"])
        self.assertEqual(client.environment, settings.ENVIRONMENT)
        self.assertIn("/* a comment, as on the page */", client.published[0][2])  # uploaded as the page shows it
        # The example document isn't from this repo, so there's no reference document; the link opens the config
        self.assertEqual(client.references, [])
        self.assertEqual(rec["segments"]["samples"][0]["editor"], markup.editor_url(quotes, "anyco"))

    def test_repo_example_document_becomes_the_reference_document(self):
        url = settings.DOCS_RAW_PREFIX + "assets/pdfs/portfolio.pdf"
        docs = [{"configuration": "anyco", "startPage": 0, "endPage": 0}, {"configuration": "acme", "startPage": 2, "endPage": 2}]
        client = SampleClient(documents=docs)
        rec = self.run_page(PORTFOLIO.replace("https://example.test/p.pdf", url), "pf", client)
        quotes = f"{settings.SAMPLE_DOC_TYPE_PREFIX}pf__quotes"
        self.assertEqual(client.references[0], (f"id-{quotes}", "portfolio", "anyco", "assets/pdfs/portfolio.pdf"))
        self.assertEqual(rec["segments"]["samples"][0]["editor"], markup.editor_url(quotes, "anyco", "portfolio"))

    def test_portfolio_samples_drift(self):
        rec = self.run_page(PORTFOLIO, "pf", SampleClient(documents=[{"configuration": "anyco", "startPage": 0, "endPage": 2}]))
        self.assertEqual((rec["status"], rec["category"]), ("fail", "SEGMENTS_DRIFT"))

    def test_local_pdf_only_maps_repo_example_documents(self):
        self.assertEqual(markup.local_pdf(settings.DOCS_RAW_PREFIX + "assets/pdfs/portfolio.pdf"), "assets/pdfs/portfolio.pdf")
        for url in ("https://example.test/a.pdf", settings.DOCS_RAW_PREFIX + "assets/pdfs/../../README.md",
                    settings.DOCS_RAW_PREFIX + "assets/pdfs/no_such_file.pdf"):
            self.assertIsNone(markup.local_pdf(url), url)

    def standalone(self, *outcomes):
        return [{"id": f"e{i}", "status": "COMPLETE", "configuration": "sa"} if ok else {"id": f"e{i}", "status": "FAILED", "errors": []}
                for i, ok in enumerate(outcomes)]

    def test_fingerprint_variants_pass(self):
        client = SampleClient(standalone=self.standalone(True, True, False))
        rec = self.run_page(STANDALONE, "sa", client)
        self.assertEqual(rec["status"], "pass")
        self.assertEqual([r["break"] for r in rec["fingerprint"]["runs"]], [[], [0], [0, 1]])
        self.assertTrue(all(schema == {"fingerprint_mode": "strict"} for schema in client.types.values()))
        broken = json.loads(client.published[2][2])["fingerprint"]["tests"]
        self.assertEqual(broken[:2], [runner.NO_MATCH, runner.NO_MATCH])
        self.assertEqual(sorted(client.types), [f"{settings.SAMPLE_DOC_TYPE_PREFIX}sa", f"{settings.SAMPLE_DOC_TYPE_PREFIX}sa__v1", f"{settings.SAMPLE_DOC_TYPE_PREFIX}sa__v2"])
        self.assertEqual(rec["fingerprint"]["runs"][2]["editor"], markup.editor_url(f"{settings.SAMPLE_DOC_TYPE_PREFIX}sa__v2", "sa"))

    def test_fingerprint_that_passes_when_the_page_says_it_fails(self):
        rec = self.run_page(STANDALONE, "sa", SampleClient(standalone=self.standalone(True, True, True)))
        self.assertEqual((rec["status"], rec["category"]), ("fail", "FINGERPRINT_DRIFT"))
        self.assertIn("with tests 0, 1 broken: the page claims it fails, but it passed", rec["message"])

    def test_a_failed_extraction_with_errors_isnt_a_failed_fingerprint(self):
        results = self.standalone(True, True) + [{"id": "e2", "status": "FAILED", "errors": [{"message": "unsupported file"}]}]
        rec = self.run_page(STANDALONE, "sa", SampleClient(standalone=results))
        self.assertEqual(rec["category"], "EXTRACTION_ERROR")


if __name__ == "__main__":
    unittest.main()


class ReportTest(unittest.TestCase):
    def test_restored_fixtures_and_editor_links_show_in_the_html_report(self):
        from codetests.reports import html
        rec = {"test_id": "t", "status": "warn", "document_url": "https://example.test/p.pdf",
               "warnings": [{"source": "fixture", "text": "fixture_x: restored fixture from the committed files (config drifted)"}],
               "segments": {"fixtures": [], "samples": [{"doc_type": "d", "config": "c", "editor": "https://app.sensible.so/editor/?d=x&c=c"}],
                            "document_types": ["x"], "extraction_id": "e1", "expected": [], "actual": []}}
        out = html.render_code_test(rec)
        out = out if isinstance(out, str) else "".join(out)
        self.assertIn("fixture restored", out)
        self.assertIn('href="https://app.sensible.so/editor/?d=x&amp;c=c"', out)
