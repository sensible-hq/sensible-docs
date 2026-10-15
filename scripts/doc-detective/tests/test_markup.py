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
