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
<!-- inline document {"from": "first"} -->
<!-- inline config {"fragment": "field"} -->
```json
 {
      /* a comment */
      "method": {"id": "queryGroup", "queries": []}
    },
```
<!-- inline output -->
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
<!-- inline document {"from": "first"} -->
<!-- inline config {"fragment": "field"} -->
```json
{
  "method": {"id": "queryGroup"
  "queries": []}
},
```
<!-- inline output -->
```json
{}
```
<!-- code test end -->
""" + CODE_TEST_PAGE)
        with self.assertRaises(CodeTestError) as caught:
            markup.check_syntax(page.code_tests["t"])
        self.assertRegex(str(caught.exception), r"line [67]\)")

    def test_from_must_name_a_code_test_with_a_link(self):
        self.assertMalformed(CODE_TEST_PAGE.replace("<!-- inline document -->", '<!-- inline document {"from": "nope"} -->'), "names no code test with its own document link")

    def test_test_ids_are_unique_across_ui_and_code_tests(self):
        ui = '<!-- test {"testId": "first"} -->\n<!-- step {"goTo": "https://x.test"} -->\n<!-- test end -->\n'
        self.assertMalformed(ui + CODE_TEST_PAGE, "testId 'first' is used on line 1 and line 4")

    def test_test_ids_are_unique_across_code_tests(self):
        self.assertMalformed(CODE_TEST_PAGE + CODE_TEST_PAGE, "testId 'first' is used on line 1")

    def test_example_markers_must_be_inside_a_code_test(self):
        self.assertMalformed(CODE_TEST_PAGE + "\n<!-- inline output -->\n```json\n{}\n```\n", "is outside any <!-- code test -->")

    def test_example_markers_inside_a_doc_detective_test_are_rejected(self):
        page = CODE_TEST_PAGE.replace("<!-- code test ", "<!-- test ").replace("<!-- code test end -->", "<!-- test end -->")
        self.assertMalformed(page, "wrap a code test in <!-- code test --> instead")

    def test_missing_parts_and_bad_ids(self):
        self.assertMalformed(CODE_TEST_PAGE.replace("<!-- inline output -->", "<!-- not a marker -->"), "missing <!-- inline output -->")
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
<!-- code test {"testId": "seg", "description": "claim", "segment_documents_with": "fingerprints"} -->
<!-- inline document -->
| Example document | [Download link](https://example.test/p.pdf) |
<!-- fixture {"name": "fixture_fp_demo_last_fails"} -->
<!-- expect {"compare": "documents", "documents": [["fixture_last_fails", 1, 8]]} -->
<!-- code test end -->
"""


class SegmentTest(unittest.TestCase):
    """Fingerprint claims: fixture configs, a portfolio extraction, and page ranges instead of parsed_document."""

    def parse(self, text):
        return markup.parse_page(write_page(self, text))

    def test_reads_fixtures_and_expected_documents(self):
        test = self.parse(SEGMENT_TEST).code_tests["seg"]
        self.assertEqual((test.segment_documents_with, test.fixtures, test.compare), ("fingerprints", ["fixture_fp_demo_last_fails"], "documents"))
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
            self.parse(SEGMENT_TEST.replace(', "segment_documents_with": "fingerprints"', ""))
        self.assertIn('needs "segment_documents_with"', str(caught.exception))

    def test_unknown_compare_is_malformed(self):
        with self.assertRaises(CodeTestError) as caught:
            self.parse(SEGMENT_TEST.replace('"compare": "documents"', '"compare": "pages"'))
        self.assertIn('expect needs "compare"', str(caught.exception))

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
                    markup.fixture_files("unprefixed")
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
                    markup.fixture_references("fixture_x")
            finally:
                settings.TEST_FIXTURES_DIR = old
        self.assertIn("needs at least one reference document", str(caught.exception))

    def fixture_root(self, root, doctype_name="fixture_x", pdf="assets/pdfs/a.pdf"):
        """A fixtures folder with one fixture under `root`, which also stands in for the repo root."""
        import os, json
        os.makedirs(os.path.join(root, "fx", "d"))
        os.makedirs(os.path.join(root, "assets", "pdfs"))
        open(os.path.join(root, "assets", "pdfs", "a.pdf"), "w").close()
        open(os.path.join(root, "secret.pdf"), "w").close()
        with open(os.path.join(root, "fx", "d", "fixture_x.doctype.json"), "w") as f:
            json.dump({"name": doctype_name, "schema": {}}, f)
        with open(os.path.join(root, "fx", "d", "fixture_x.fixture_c.config.json"), "w") as f:
            json.dump({"fields": []}, f)
        with open(os.path.join(root, "fx", "d", "manifest.json"), "w") as f:
            json.dump({"document_types": [{"doctype": "fixture_x.doctype.json", "references": [
                {"name": "fixture_ref", "pdf": pdf, "configuration": "fixture_c"}]}]}, f)

    def with_root(self, root, fn):
        import os
        from codetests import settings
        saved = settings.TEST_FIXTURES_DIR, settings.REPO_ROOT, settings.FIXTURE_PDFS_DIR
        settings.TEST_FIXTURES_DIR, settings.REPO_ROOT, settings.FIXTURE_PDFS_DIR = os.path.join(root, "fx"), root, os.path.join(root, "assets", "pdfs")
        try:
            return fn()
        finally:
            settings.TEST_FIXTURES_DIR, settings.REPO_ROOT, settings.FIXTURE_PDFS_DIR = saved

    def test_doctype_name_must_match_its_file_name(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            self.fixture_root(root, doctype_name="invoices_prod")
            with self.assertRaises(CodeTestError) as caught:
                self.with_root(root, lambda: markup.fixture_files("fixture_x"))
        self.assertIn("it must match the file name", str(caught.exception))

    def test_reference_pdf_must_be_under_assets_pdfs(self):
        import tempfile
        for pdf in ("secret.pdf", "assets/pdfs/../../secret.pdf", "/etc/hostname"):
            with tempfile.TemporaryDirectory() as root:
                self.fixture_root(root, pdf=pdf)
                with self.assertRaises(CodeTestError, msg=pdf) as caught:
                    self.with_root(root, lambda: markup.fixture_references("fixture_x"))
            self.assertIn("must be a .pdf under", str(caught.exception))
        with tempfile.TemporaryDirectory() as root:
            self.fixture_root(root)
            self.assertEqual(self.with_root(root, lambda: markup.fixture_references("fixture_x"))[0]["name"], "fixture_ref")

    def test_expect_pages_must_be_ordered_integers(self):
        for documents in ('[["fixture_last_fails", 8, 1]]', '[["fixture_last_fails", true, 8]]'):
            test = self.parse(SEGMENT_TEST.replace('[["fixture_last_fails", 1, 8]]', documents)).code_tests["seg"]
            with self.assertRaises(CodeTestError, msg=documents):
                markup.check_syntax(test)

    def test_fixture_without_expect_is_malformed(self):
        page = SEGMENT_TEST.replace('<!-- expect {"compare": "documents", "documents": [["fixture_last_fails", 1, 8]]} -->', "")
        with self.assertRaises(CodeTestError) as caught:
            self.parse(page)
        self.assertIn("need <!-- expect", str(caught.exception))

    def test_only_one_expect(self):
        page = SEGMENT_TEST.replace("<!-- code test end -->", '<!-- expect {"compare": "documents", "documents": []} -->\n<!-- code test end -->')
        with self.assertRaises(CodeTestError) as caught:
            self.parse(page)
        self.assertIn("more than one <!-- expect -->", str(caught.exception))

    def test_ids_reject_a_trailing_newline(self):
        with self.assertRaises(CodeTestError):
            self.parse(SEGMENT_TEST.replace('"testId": "seg"', '"testId": "seg\\n"'))

    def test_editor_url(self):
        self.assertEqual(markup.editor_url("fixture_d", "fixture_c", "fixture_g"),
                         "https://app.sensible.so/editor/?d=fixture_d&c=fixture_c&g=fixture_g")



TABLE_PAGE = """
<!-- table test {"testId": "tt", "table": "claims", "segment_documents_with": "fingerprints", "description": "each row"} -->
<!-- inline document -->
| Example document | [Download link](https://example.test/p.pdf) |

<!-- table {"tableId": "claims"} -->
| claim | result |
| ----- | ------ |
| first | none |
| second | pages 1-8 |

<!-- row {"rowId": "first_row", "fixture": {"name": "fixture_fp_demo_first_fails"}, "expect": {"compare": "documents", "documents": []}} -->
<!-- row {"rowId": "second_row", "fixture": {"name": "fixture_fp_demo_last_fails"}, "expect": {"compare": "documents", "documents": [["fixture_last_fails", 1, 8]]}} -->
<!-- table test end -->
"""


class TableTestTest(unittest.TestCase):
    """A tagged table and its table test: one row entry per table row, in order."""

    def parse(self, text):
        return markup.parse_page(write_page(self, text))

    def test_rows_expand_into_tests(self):
        page = self.parse(TABLE_PAGE)
        self.assertEqual(list(page.code_tests), ["tt__first_row", "tt__second_row"])
        second = page.code_tests["tt__second_row"]
        self.assertEqual((second.table, second.row, second.document_url), ("claims", "2: second_row", "https://example.test/p.pdf"))
        self.assertEqual(markup.check_syntax(second), (None, [["fixture_last_fails", 1, 8]]))

    def test_row_count_must_match_the_table(self):
        with self.assertRaises(CodeTestError) as caught:
            self.parse(TABLE_PAGE.replace("| second | pages 1-8 |", "| second | pages 1-8 |\n| third | pages 2-3 |"))
        self.assertIn("has 3 row(s) but its test has 2 row entries", str(caught.exception))

    def test_row_without_a_trailing_pipe_still_counts(self):
        with self.assertRaises(CodeTestError) as caught:
            self.parse(TABLE_PAGE.replace("| second | pages 1-8 |", "| second | pages 1-8 |\n| third | pages 2-3"))
        self.assertIn("has 3 row(s) but its test has 2 row entries", str(caught.exception))

    def test_markers_beside_rows_are_malformed(self):
        with self.assertRaises(CodeTestError) as caught:
            self.parse(TABLE_PAGE.replace("<!-- table test end -->", '<!-- expect {"compare": "documents", "documents": []} -->\n<!-- table test end -->'))
        self.assertIn("takes only one <!-- inline document -->", str(caught.exception))

    def test_table_needs_a_test(self):
        with self.assertRaises(CodeTestError) as caught:
            self.parse(TABLE_PAGE.replace('"table": "claims"', '"table": "other"'))
        self.assertIn("no <!-- table {\"tableId\": \"other\"} -->", str(caught.exception))

    def test_tag_without_a_test_is_malformed(self):
        page = TABLE_PAGE.split("<!-- table test end -->")[1] + '<!-- table {"tableId": "lonely"} -->\n| a |\n| - |\n| b |\n'
        with self.assertRaises(CodeTestError) as caught:
            self.parse(page)
        self.assertIn("without a table test: lonely", str(caught.exception))

    def test_tag_must_precede_a_table(self):
        with self.assertRaises(CodeTestError) as caught:
            self.parse(TABLE_PAGE.replace("| claim | result |", "Some text"))
        self.assertIn("isn't followed by a Markdown table", str(caught.exception))


class RenamedMarkupTest(unittest.TestCase):
    """The old #737 markers and the "segment" option fail with a message naming the new markup."""

    def parse(self, text):
        return markup.parse_page(write_page(self, text))

    def test_old_example_markers_name_their_replacement(self):
        with self.assertRaises(CodeTestError) as caught:
            self.parse(CODE_TEST_PAGE.replace("<!-- inline config -->", "<!-- example config -->"))
        self.assertIn("was renamed <!-- inline config -->", str(caught.exception))

    def test_old_segment_option_names_its_replacement(self):
        with self.assertRaises(CodeTestError) as caught:
            self.parse(SEGMENT_TEST.replace('"segment_documents_with"', '"segment"'))
        self.assertIn('"segment" was renamed "segment_documents_with"', str(caught.exception))

    def test_old_row_config_names_its_replacement(self):
        with self.assertRaises(CodeTestError) as caught:
            self.parse(TABLE_PAGE.replace('"fixture": {"name": "fixture_fp_demo_first_fails"}', '"config": {"fixture": "fixture_fp_demo_first_fails"}'))
        self.assertIn('was renamed "fixture"', str(caught.exception))
