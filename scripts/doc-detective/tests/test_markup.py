import unittest

from codetests import markup
from codetests.errors import CodeTestError

from tests.fakes import CODE_TEST_PAGE, write_page


class PageTest(unittest.TestCase):
    def parse(self, text):
        return markup.parse_page(write_page(self, text))

    def assertMalformed(self, text, message):
        with self.assertRaises(CodeTestError) as caught:
            self.parse(text)
        self.assertEqual(caught.exception.category, "DOCS_MALFORMED")
        self.assertIn(message, str(caught.exception))

    def test_reads_ui_tests_and_code_tests(self):
        page = self.parse('<!-- test {"testId": "ui_one", "description": "sign in"} -->\n<!-- step {"goTo": "https://x.test"} -->\n<!-- test end -->\n' + CODE_TEST_PAGE)
        self.assertEqual([(t.test_id, t.description, t.line) for t in page.ui_tests], [("ui_one", "sign in", 1)])
        first = page.code_tests["first"]
        self.assertEqual((first.document_url, first.description, first.config), ("https://example.test/a.pdf", "first test", '{"fields": []}'))

    def test_fragment_is_wrapped_and_document_is_reused(self):
        page = self.parse(CODE_TEST_PAGE + """
<!-- code test {"testId": "second"} -->
<!-- example document {"from": "first"} -->
<!-- example config {"fragment": "field"} -->
```json
 {
      /* a comment */
      "method": {"id": "queryGroup", "queries": []}
    },
```
<!-- example output -->
```json
{}
```
<!-- code test end -->
""")
        second = page.code_tests["second"]
        self.assertEqual((second.document_url, second.document_from, second.fragment), ("https://example.test/a.pdf", "first", True))
        self.assertIn("/* a comment */", second.config)
        self.assertTrue(second.config.startswith('{\n  "fields": ['))
        config, _ = markup.check_syntax(second)
        self.assertEqual(config["fields"][0]["method"]["id"], "queryGroup")

    def test_fragment_syntax_errors_point_at_the_doc_line(self):
        page = self.parse("""<!-- code test {"testId": "t"} -->
<!-- example document {"from": "first"} -->
<!-- example config {"fragment": "field"} -->
```json
{
  "method": {"id": "queryGroup"
  "queries": []}
},
```
<!-- example output -->
```json
{}
```
<!-- code test end -->
""" + CODE_TEST_PAGE)
        with self.assertRaises(CodeTestError) as caught:
            markup.check_syntax(page.code_tests["t"])
        self.assertRegex(str(caught.exception), r"line [67]\)")

    def test_from_must_name_a_code_test_with_a_link(self):
        self.assertMalformed(CODE_TEST_PAGE.replace("<!-- example document -->", '<!-- example document {"from": "nope"} -->'), "names no code test with its own document link")

    def test_test_ids_are_unique_across_ui_and_code_tests(self):
        ui = '<!-- test {"testId": "first"} -->\n<!-- step {"goTo": "https://x.test"} -->\n<!-- test end -->\n'
        self.assertMalformed(ui + CODE_TEST_PAGE, "testId 'first' is used on line 1 and line 4")

    def test_test_ids_are_unique_across_code_tests(self):
        self.assertMalformed(CODE_TEST_PAGE + CODE_TEST_PAGE, "testId 'first' is used on line 1")

    def test_example_markers_must_be_inside_a_code_test(self):
        self.assertMalformed(CODE_TEST_PAGE + "\n<!-- example output -->\n```json\n{}\n```\n", "is outside any <!-- code test -->")

    def test_example_markers_inside_a_doc_detective_test_are_rejected(self):
        page = CODE_TEST_PAGE.replace("<!-- code test ", "<!-- test ").replace("<!-- code test end -->", "<!-- test end -->")
        self.assertMalformed(page, "wrap a code test in <!-- code test --> instead")

    def test_missing_parts_and_bad_ids(self):
        self.assertMalformed(CODE_TEST_PAGE.replace("<!-- example output -->", "<!-- not a marker -->"), "missing <!-- example output -->")
        self.assertMalformed(CODE_TEST_PAGE.replace('"testId": "first"', '"testId": "First-Test"'), "must be lowercase letters")
        self.assertMalformed(CODE_TEST_PAGE.replace('"testId": "first", ', '"testId": "first" '), "isn't valid JSON")


class SyntaxTest(unittest.TestCase):
    def check(self, config="{}", output="{}"):
        return markup.check_syntax(markup.CodeTest("t", "", "doc.md", 1, config=config, config_line=10, output=output, output_line=20))

    def assertRejected(self, message, **blocks):
        with self.assertRaises(CodeTestError) as caught:
            self.check(**blocks)
        self.assertIn(message, str(caught.exception))
        return str(caught.exception)

    def test_configs_allow_comments_and_trailing_commas(self):
        config, _ = self.check(config='{\n  /* c */ "fields": [1,],\n}')
        self.assertEqual(config, {"fields": [1]})

    def test_outputs_allow_comments_and_ellipsis_but_not_trailing_commas(self):
        _, output = self.check(output='{"a": ..., /* c */ "b": 1}')
        self.assertEqual(output["b"], 1)
        message = self.assertRejected("output block: trailing comma", output='{\n  "a": 1,\n}')
        self.assertIn("line 22", message)

    def test_duplicate_keys_nan_and_unclosed_comments(self):
        self.assertRejected('duplicate key "a"', output='{"a": 1, "a": 2}')
        self.assertRejected("NaN isn't valid JSON", output='{"a": NaN}')
        self.assertRejected("unclosed /* comment", config='{\n/* oops\n}')


if __name__ == "__main__":
    unittest.main()


SEGMENT_TEST = """
<!-- code test {"testId": "seg", "description": "claim", "segment": "fingerprints"} -->
<!-- example document -->
| Example document | [Download link](https://example.test/p.pdf) |
<!-- example config {"fixture": "fingerprint_portfolio/fixture_fp_demo_last_fails"} -->
<!-- example output {"compare": "documents", "expect": [["fixture_last_fails", 1, 8]]} -->
<!-- code test end -->
"""


class SegmentTest(unittest.TestCase):
    """Fingerprint claims: fixture configs, a portfolio extraction, and page ranges instead of parsed_document."""

    def parse(self, text):
        return markup.parse_page(write_page(self, text))

    def test_reads_fixtures_and_expected_documents(self):
        test = self.parse(SEGMENT_TEST).code_tests["seg"]
        self.assertEqual((test.segment, test.fixtures, test.compare), ("fingerprints", ["fingerprint_portfolio/fixture_fp_demo_last_fails"], "documents"))
        self.assertEqual(markup.check_syntax(test), (None, [["fixture_last_fails", 1, 8]]))

    def test_expect_must_be_one_based_page_ranges(self):
        test = self.parse(SEGMENT_TEST.replace('[["fixture_last_fails", 1, 8]]', '[["fixture_last_fails", 0, 7]]')).code_tests["seg"]
        with self.assertRaises(CodeTestError) as caught:
            markup.check_syntax(test)
        self.assertIn("1-based", str(caught.exception))

    def test_missing_fixture_is_malformed(self):
        test = self.parse(SEGMENT_TEST.replace("fixture_fp_demo_last_fails", "fixture_no_such")).code_tests["seg"]
        with self.assertRaises(CodeTestError) as caught:
            markup.check_syntax(test)
        self.assertEqual(caught.exception.category, "DOCS_MALFORMED")

    def test_documents_compare_needs_fingerprint_segmentation(self):
        with self.assertRaises(CodeTestError) as caught:
            self.parse(SEGMENT_TEST.replace(', "segment": "fingerprints"', ""))
        self.assertIn('needs "segment": "fingerprints"', str(caught.exception))

    def test_unknown_compare_is_malformed(self):
        with self.assertRaises(CodeTestError) as caught:
            self.parse(SEGMENT_TEST.replace('"compare": "documents"', '"compare": "pages"'))
        self.assertIn("unknown compare", str(caught.exception))

    def test_fixture_names_need_the_prefix(self):
        import os, tempfile, json
        from codetests import settings
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "d"))
            with open(os.path.join(root, "d", "unprefixed.doctype.json"), "w") as f:
                json.dump({"name": "unprefixed", "schema": {}}, f)
            with open(os.path.join(root, "d", "unprefixed.cfg.config.json"), "w") as f:
                json.dump({"fields": []}, f)
            old, settings.TEST_FIXTURES_DIR = settings.TEST_FIXTURES_DIR, root
            try:
                with self.assertRaises(CodeTestError) as caught:
                    markup.fixture_files("d/unprefixed")
            finally:
                settings.TEST_FIXTURES_DIR = old
        self.assertIn("must start with 'fixture_'", str(caught.exception))

    def test_fixture_needs_a_reference_document(self):
        import os, tempfile, json
        from codetests import settings
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "d"))
            with open(os.path.join(root, "d", "fixture_x.doctype.json"), "w") as f:
                json.dump({"name": "fixture_x", "schema": {}}, f)
            with open(os.path.join(root, "d", "fixture_x.fixture_c.config.json"), "w") as f:
                json.dump({"fields": []}, f)
            with open(os.path.join(root, "d", "manifest.json"), "w") as f:
                json.dump({"document_types": [{"doctype": "fixture_x.doctype.json", "configs": [{"name": "fixture_c"}]}]}, f)
            old, settings.TEST_FIXTURES_DIR = settings.TEST_FIXTURES_DIR, root
            try:
                with self.assertRaises(CodeTestError) as caught:
                    markup.fixture_references("d/fixture_x")
            finally:
                settings.TEST_FIXTURES_DIR = old
        self.assertIn("needs at least one reference document", str(caught.exception))

    def test_editor_url(self):
        self.assertEqual(markup.editor_url("fixture_d", "fixture_c", "fixture_g"),
                         "https://app.sensible.so/editor/?d=fixture_d&c=fixture_c&g=fixture_g")


CLAIMS_PAGE = """
| example | claim |
| ------- | ----- |
| A | first claim |
| B | second claim |

<!-- code test {"testId": "t_a", "segment": "fingerprints"} -->
<!-- example document -->
| Example document | [Download link](https://example.test/p.pdf) |
<!-- example config {"fixture": "fingerprint_portfolio/fixture_fp_demo_last_fails"} -->
<!-- example output {"compare": "documents", "expect": [], "row": "A"} -->
<!-- code test end -->

<!-- code test {"testId": "t_b", "segment": "fingerprints"} -->
<!-- example document {"from": "t_a"} -->
<!-- example config {"fixture": "fingerprint_portfolio/fixture_fp_demo_last_fails"} -->
<!-- example output {"compare": "documents", "expect": [], "row": "B"} -->
<!-- code test end -->
"""


class ClaimsTableTest(unittest.TestCase):
    """Tests bind to labeled rows of a claims table; rows can't drift from their tests unnoticed."""

    def parse(self, text):
        return markup.parse_page(write_page(self, text))

    def test_unreviewed_row_fails_until_accepted(self):
        path = write_page(self, CLAIMS_PAGE)
        page = markup.parse_page(path)
        with self.assertRaises(CodeTestError) as caught:
            markup.check_syntax(page.code_tests["t_a"])
        self.assertIn("has no row_sha yet", str(caught.exception))
        self.assertEqual(sorted(markup.accept_rows(page)), ["t_a", "t_b"])
        page = markup.parse_page(path)
        for test in page.code_tests.values():
            markup.check_syntax(test)  # accepted: no error
        self.assertEqual(markup.accept_rows(page), [])

    def test_edited_row_fails(self):
        path = write_page(self, CLAIMS_PAGE)
        markup.accept_rows(markup.parse_page(path))
        with open(path, encoding="utf-8") as f:
            text = f.read().replace("second claim", "changed claim")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        test = markup.parse_page(path).code_tests["t_b"]
        with self.assertRaises(CodeTestError) as caught:
            markup.check_syntax(test)
        self.assertIn("changed since its test was last reviewed", str(caught.exception))

    def test_row_without_a_test_is_malformed(self):
        with self.assertRaises(CodeTestError) as caught:
            self.parse(CLAIMS_PAGE.replace("| B | second claim |", "| B | second claim |\n| C | third claim |"))
        self.assertIn("rows without a test: C", str(caught.exception))

    def test_unknown_row_is_malformed(self):
        with self.assertRaises(CodeTestError) as caught:
            self.parse(CLAIMS_PAGE.replace('"row": "B"', '"row": "Z"'))
        self.assertIn("no claims-table row labeled 'Z'", str(caught.exception))

    def test_row_bound_twice_is_malformed(self):
        with self.assertRaises(CodeTestError) as caught:
            self.parse(CLAIMS_PAGE.replace('"row": "B"', '"row": "A"'))
        self.assertIn("bound to two tests", str(caught.exception))
