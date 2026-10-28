"""Field expects: `<!-- expect {"compare": "fields", ...} -->` checks named fields of one extraction.

The spec is the README's "Field claims" section. These tests were written before the feature: until
it's implemented they fail (the markup is rejected as an unknown compare), not error on import.
"""

import json
import os
import tempfile
import unittest
from unittest import mock

from codetests import errors, markup, record, runner, settings
from codetests.errors import CodeTestError

from tests.fakes import CONFIG, FakeClient, FakeJudge, write_page

# Layout-only config: every field is deterministic, so every field can be claimed
LAYOUT = {"fields": [
    {"id": "stop_match", "anchor": "may 2020", "method": {"id": "column", "stop": {"type": "startsWith", "text": "for up"}}},
    {"id": "count", "anchor": "may 2020", "type": "number", "method": {"id": "column", "tiebreaker": ">"}},
    {"id": "not_found", "anchor": "no such line", "method": {"id": "row"}},
    {"id": "gone", "anchor": "may 2020", "method": {"id": "row"}},
    {"id": "rows", "type": "sections", "range": {"anchor": "may 2020"}, "fields": [
        {"id": "name", "anchor": "name", "method": {"id": "label"}},
    ]},
    {"id": "other", "anchor": "x", "method": {"id": "row"}},
]}

# What Sensible returns for LAYOUT: "not_found" came back null, "gone" isn't in the output at all
ACTUAL = {
    "stop_match": {"type": "string", "value": "1 3 2 4 5"},
    "count": {"source": "5", "value": 5, "type": "number"},
    "not_found": None,
    "rows": [{"name": {"type": "string", "value": "Ann"}}, {"name": {"type": "string", "value": "Bob"}},
             {"name": {"type": "string", "value": "Cy"}}],
    "other": {"type": "string", "value": "ignored"},
}

# A section with a layout field and an LLM field
SECTION_WITH_LLM = {"fields": [
    {"id": "rows", "type": "sections", "range": {"anchor": "x"}, "fields": [
        {"id": "name", "anchor": "name", "method": {"id": "label"}},
        {"method": {"id": "queryGroup", "queries": [{"id": "age", "description": "the person's age"}]}},
    ]},
]}


def fields_expect(fields=None, absent=None):
    expect = {"compare": "fields"}
    if fields is not None:
        expect["fields"] = fields
    if absent is not None:
        expect["absent"] = absent
    return expect


def code_test_page(expect, config=LAYOUT, fixture=None, inline_config=True, output=False):
    """A code test with an expect. The config is the page's inline config, or a fixture marker, or both."""
    parts = ['<!-- code test {"testId": "claims", "description": "field claims"} -->\n',
             "<!-- inline document -->\n\n| Example document | [Download link](https://example.test/row_column.pdf) |\n\n"]
    if inline_config:
        parts.append("<!-- inline config -->\n```json\n" + json.dumps(config, indent=2) + "\n```\n")
    if fixture is not None:
        parts.append("<!-- fixture " + json.dumps(fixture) + " -->\n")
    if output:
        parts.append("<!-- inline output -->\n```json\n" + json.dumps(ACTUAL, indent=2) + "\n```\n")
    parts.append("<!-- expect " + json.dumps(expect) + " -->\n<!-- code test end -->\n")
    return "".join(parts)


def table_page(rows, segment=False):
    """A tagged table with one table row per row entry, and its table test."""
    table = '<!-- table {"tableId": "params"} -->\n| key | value |\n| --- | --- |\n' + "".join(f"| key{i} | value |\n" for i in range(len(rows)))
    header = {"testId": "params_tests", "table": "params", "description": "parameter claims"}
    if segment:
        header["segment_documents_with"] = "fingerprints"
    return (table + "\n<!-- table test " + json.dumps(header) + " -->\n"
            "<!-- inline document -->\n| Example document | [Download link](https://example.test/row_column.pdf) |\n\n"
            + "".join("<!-- row " + json.dumps(row) + " -->\n" for row in rows)
            + "<!-- table test end -->\n")


def fields_row(row_id="stop", config=LAYOUT, expect=None):
    return {"rowId": row_id, "fixture": {"config": config},
            "expect": expect or fields_expect({"stop_match": {"value": "1 3 2 4 5"}})}


class MarkupCase(unittest.TestCase):
    def check(self, text):
        """Parse the page and check every code test's syntax. Returns {test ID: check_syntax result}."""
        page = markup.parse_page(write_page(self, text))
        return {test_id: markup.check_syntax(test) for test_id, test in page.code_tests.items()}

    def accepted(self, text):
        try:
            return self.check(text)
        except CodeTestError as e:
            self.fail(f"field expect markup was rejected (is the feature implemented?): {e}")

    def assertMalformed(self, text, *messages):
        with self.assertRaises(CodeTestError) as caught:
            self.check(text)
        self.assertEqual(caught.exception.category, "DOCS_MALFORMED")
        for message in messages:
            self.assertIn(message, str(caught.exception))


class FieldExpectMarkupTest(MarkupCase):
    """Valid markup: in a code test and in a table row, with each config source."""

    def test_code_test_with_its_inline_config(self):
        expect = {"stop_match": {"value": "1 3 2 4 5"}, "count": {"value": 5, "type": "number"}}
        checked = self.accepted(code_test_page(fields_expect(expect)))
        self.assertEqual(checked["claims"], (LAYOUT, {"fields": expect, "absent": []}))

    def test_absent_is_read(self):
        checked = self.accepted(code_test_page(fields_expect({"count": {"value": 5}}, absent=["gone"])))
        self.assertEqual(checked["claims"][1], {"fields": {"count": {"value": 5}}, "absent": ["gone"]})

    def test_absent_alone_is_enough(self):
        checked = self.accepted(code_test_page(fields_expect(absent=["gone"])))
        self.assertEqual(checked["claims"][1], {"fields": {}, "absent": ["gone"]})

    def test_code_test_with_a_fixture_config(self):
        page = code_test_page(fields_expect({"stop_match": {"value": "1 3 2 4 5"}}), fixture={"config": LAYOUT}, inline_config=False)
        checked = self.accepted(page)
        self.assertEqual(checked["claims"][0], LAYOUT)

    def test_row_with_a_fixture_config(self):
        page_text = table_page([fields_row()])
        self.accepted(page_text)
        test = markup.parse_page(write_page(self, page_text)).code_tests["params_tests__stop"]
        self.assertEqual((test.compare, test.table, test.row), ("fields", "params", "1: stop"))
        # A config written in the comment isn't a doc type in the test account: nothing to ensure or restore
        self.assertEqual(test.fixtures, [])
        self.assertEqual(markup.check_syntax(test), (LAYOUT, {"fields": {"stop_match": {"value": "1 3 2 4 5"}}, "absent": []}))

    def test_nested_section_with_a_layout_field(self):
        expect = {"rows": [{"name": {"value": "Ann"}}, "[...]"]}
        checked = self.accepted(code_test_page(fields_expect(expect), config=SECTION_WITH_LLM))
        self.assertEqual(checked["claims"][1]["fields"], expect)


class FieldExpectMalformedTest(MarkupCase):
    """Invalid markup fails with DOCS_MALFORMED before any network call, naming the problem."""

    def test_fields_must_map_field_ids_to_outputs(self):
        for fields in ([], "stop_match", [["stop_match", 1]]):
            with self.subTest(fields=fields):
                self.assertMalformed(code_test_page(fields_expect(fields)), 'needs "fields"')

    def test_expect_must_name_a_field(self):
        self.assertMalformed(code_test_page(fields_expect({})), "names no fields")
        self.assertMalformed(code_test_page(fields_expect()), "names no fields")

    def test_bare_value_isnt_a_field_output(self):
        # A field's output is an object ({"value": ...}), a list (sections), or null; "5" can never match it
        for value in ("1 3 2 4 5", 5, True):
            with self.subTest(value=value):
                self.assertMalformed(code_test_page(fields_expect({"stop_match": value})), '{"value": ...}', "stop_match")

    def test_absent_must_be_a_list_of_field_ids(self):
        for absent in ("gone", [1], {"gone": True}):
            with self.subTest(absent=absent):
                self.assertMalformed(code_test_page(fields_expect({"count": {"value": 5}}, absent=absent)), '"absent" must be a list of field IDs')

    def test_a_field_cant_be_both_listed_and_absent(self):
        self.assertMalformed(code_test_page(fields_expect({"gone": None}, absent=["gone"])), 'in both "fields" and "absent"', "gone")

    def test_field_must_be_in_the_config(self):
        self.assertMalformed(code_test_page(fields_expect({"stop_mach": {"value": "1"}})), "isn't in the config", "stop_mach")

    def test_absent_field_must_be_in_the_config(self):
        # Otherwise a typo would pass an absent claim
        self.assertMalformed(code_test_page(fields_expect(absent=["gonne"])), "isn't in the config", "gonne")

    def test_field_ids_are_checked_against_a_named_fixtures_config(self):
        row = {"rowId": "named", "fixture": {"name": "fixture_fp_demo_last_fails"}, "expect": fields_expect({"stop_match": {"value": "1"}})}
        self.assertMalformed(table_page([row]), "isn't in the config", "stop_match")

    def test_llm_field_is_rejected(self):
        # Field expects are exact-only; an LLM value belongs in an inline output, where the judge checks it
        self.assertMalformed(code_test_page(fields_expect({"phone": {"value": "1800 123 4567"}}), config=CONFIG), "LLM method", "phone")

    def test_llm_field_claimed_absent_or_null_is_rejected(self):
        self.assertMalformed(code_test_page(fields_expect({"phone": None}), config=CONFIG), "LLM method", "phone")
        self.assertMalformed(code_test_page(fields_expect(absent=["vehicles"]), config=CONFIG), "LLM method", "vehicles")

    def test_llm_field_nested_in_a_section_is_rejected(self):
        expect = {"rows": [{"age": {"value": "40"}}, "[...]"]}
        self.assertMalformed(code_test_page(fields_expect(expect), config=SECTION_WITH_LLM), "LLM method", "age")

    def test_fallback_chain_with_an_llm_field_is_rejected(self):
        self.assertMalformed(code_test_page(fields_expect({"total": {"value": 100}}), config=CONFIG), "LLM method", "total")

    def test_fixture_takes_name_or_config_not_both(self):
        row = fields_row()
        row["fixture"]["name"] = "fixture_fp_demo_last_fails"
        self.assertMalformed(table_page([row]), 'takes "name" or "config"')
        page = code_test_page(fields_expect({"stop_match": {"value": "1"}}), fixture={"name": "fixture_fp_demo_last_fails", "config": LAYOUT}, inline_config=False)
        self.assertMalformed(page, 'takes "name" or "config"')

    def test_fixture_config_must_be_a_config_with_fields(self):
        for config in ({"fingerprint": {"tests": []}}, "fields", {"fields": {"id": "x"}}):
            with self.subTest(config=config):
                self.assertMalformed(table_page([fields_row(config=config)]), 'must be a config object with a "fields" list')

    def test_fixture_config_works_only_with_field_expects(self):
        row = {"rowId": "seg", "fixture": {"config": LAYOUT}, "expect": {"compare": "documents", "documents": []}}
        self.assertMalformed(table_page([row], segment=True), 'works only with compare "fields"')

    def test_field_expect_rejects_portfolio_segmentation(self):
        self.assertMalformed(table_page([fields_row()], segment=True), "single-document extraction")

    def test_field_expect_needs_exactly_one_config(self):
        expect = fields_expect({"stop_match": {"value": "1"}})
        self.assertMalformed(code_test_page(expect, inline_config=False), "needs one config")
        self.assertMalformed(code_test_page(expect, fixture={"config": LAYOUT}), "needs one config")

    def test_field_expect_takes_no_inline_output(self):
        self.assertMalformed(code_test_page(fields_expect({"stop_match": {"value": "1"}}), output=True), "takes no <!-- inline output -->")


class UntestedRowTest(MarkupCase):
    """A parameter table has rows with nothing to check; an untested row entry keeps the row count."""

    def test_untested_row_runs_nothing(self):
        rows = [{"rowId": "id", "untested": "the method's ID; nothing to check"}, fields_row()]
        self.accepted(table_page(rows))
        page = markup.parse_page(write_page(self, table_page(rows)))
        self.assertEqual(list(page.code_tests), ["params_tests__stop"])
        self.assertEqual(page.code_tests["params_tests__stop"].row, "2: stop")

    def test_untested_needs_a_reason(self):
        for reason in ("", True, None):
            with self.subTest(reason=reason):
                self.assertMalformed(table_page([{"rowId": "id", "untested": reason}]), '"untested" needs a reason')

    def test_untested_row_takes_no_fixture_or_expect(self):
        row = fields_row()
        row["untested"] = "not yet"
        self.assertMalformed(table_page([row]), "untested row takes no")


class FieldsDriftCategoryTest(unittest.TestCase):
    def test_fields_drift_is_a_failure_category(self):
        self.assertEqual(getattr(errors, "FIELDS_DRIFT", None), "FIELDS_DRIFT", "codetests/errors.py has no FIELDS_DRIFT")


class FieldsClient(FakeClient):
    """Temporary doc types for a fixture config: records what was created, published, and deleted."""

    def __init__(self, parsed, extraction_status="COMPLETE"):
        super().__init__(parsed)
        self.extraction_status, self.created, self.published, self.deleted_types = extraction_status, [], [], []

    def create_temp_doc_type(self, name, schema=None):
        self.created.append(name)
        return f"id-{name}"

    def publish_config(self, type_id, name, config_text):
        self.published.append((type_id, name, config_text))

    def extract_standalone(self, url, doc_type, document_name):
        self.extractions += 1
        if self.extraction_status != "COMPLETE":
            return {"id": "e1", "status": self.extraction_status, "errors": [{"message": "boom"}]}
        name = self.published[-1][1] if self.published else ""
        return {"id": "e1", "status": "COMPLETE", "configuration": name, "parsed_document": self.parsed}

    def delete_temp_doc_type(self, type_id):
        self.deleted_types.append(type_id)


class FieldRunCase(unittest.TestCase):
    def setUp(self):
        # An empty baselines folder, so committed baselines never leak into these tests
        self.envelopes = tempfile.TemporaryDirectory()
        self.addCleanup(self.envelopes.cleanup)
        patcher = mock.patch.dict(os.environ, {settings.ENVELOPES_DIR_VAR: self.envelopes.name})
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_page(self, text, client=None, test_id=None):
        try:
            page = markup.parse_page(write_page(self, text))
        except CodeTestError as e:
            self.fail(f"field expect markup was rejected (is the feature implemented?): {e}")
        test = page.code_tests[test_id] if test_id else next(iter(page.code_tests.values()))
        client = client if client is not None else FakeClient(ACTUAL)
        judge = FakeJudge()
        rec = runner.run_code_test(test, client, judge=judge, judge_key="fake-key")
        record.validate(rec)  # every record matches the schema the reports rely on
        # Field expects are exact-only: the judge is never asked
        self.assertEqual(judge.claims, [])
        return rec

    def run_fields(self, fields=None, absent=None):
        return self.run_page(code_test_page(fields_expect(fields, absent)))

    def assertPasses(self, fields=None, absent=None):
        rec = self.run_fields(fields, absent)
        self.assertEqual((rec["status"], rec.get("category"), rec.get("message")), ("pass", None, None))
        return rec

    def assertDrift(self, fields=None, absent=None, *lines):
        rec = self.run_fields(fields, absent)
        self.assertEqual((rec["status"], rec.get("category")), ("fail", "FIELDS_DRIFT"), rec.get("message"))
        for line in lines:
            self.assertIn(line, rec["message"])
        return rec


class FieldCompareTest(FieldRunCase):
    def test_listed_fields_match_and_others_are_ignored(self):
        rec = self.assertPasses({"stop_match": {"value": "1 3 2 4 5"}, "count": {"value": 5}})
        self.assertEqual(rec["fields"]["mismatches"], [])

    def test_keys_left_out_arent_checked(self):
        self.assertPasses({"count": {"value": 5}})
        self.assertPasses({"count": {"value": 5, "type": "number", "source": "5"}})
        self.assertDrift({"count": {"value": 5, "type": "string"}}, None, '$.count.type: expected "string", got "number"')

    def test_numbers_compare_as_numbers_not_text_or_booleans(self):
        self.assertPasses({"count": {"value": 5.0}})
        self.assertDrift({"count": {"value": "5"}}, None, '$.count.value: expected "5", got 5')
        self.assertDrift({"count": {"value": True}}, None, "$.count.value: expected true, got 5")

    def test_strings_are_exact_including_whitespace_and_case(self):
        for value in ("1 3 2 4  5", "1 3 2 4 5 ", " 1 3 2 4 5", "1 3 2 4 5\n"):
            with self.subTest(value=value):
                self.assertDrift({"stop_match": {"value": value}}, None, "$.stop_match.value: expected")

    def test_null_means_the_field_came_back_null(self):
        self.assertPasses({"not_found": None})
        self.assertDrift({"stop_match": None}, None, '$.stop_match: expected null, got {"type": "string", "value": "1 3 2 4 5"}')

    def test_null_isnt_absent(self):
        self.assertDrift({"gone": None}, None, "$.gone: missing from actual output")

    def test_absent(self):
        self.assertPasses(absent=["gone"])
        self.assertDrift(None, ["not_found"], "$.not_found: expected absent, got null")
        self.assertDrift(None, ["count"], '$.count: expected absent, got {"source": "5", "value": 5, "type": "number"}')

    def test_nested_sections(self):
        self.assertPasses({"rows": [{"name": {"value": "Ann"}}, "[...]"]})
        self.assertPasses({"rows": ["[...]", {"name": {"value": "Cy"}}]})
        self.assertPasses({"rows": [{"name": {"value": "Ann"}}, {"name": {"value": "Bob"}}, {"name": {"value": "Cy"}}]})
        # An array without a mark must match in full
        self.assertDrift({"rows": [{"name": {"value": "Ann"}}, {"name": {"value": "Bob"}}]}, None, "$.rows: expected")
        # A tail item is reported at its index in the expect
        self.assertDrift({"rows": ["[...]", {"name": {"value": "Zed"}}]}, None, '$.rows[1].name.value: expected "Zed", got "Cy"')

    def test_abridgement(self):
        self.assertPasses({"stop_match": {"value": "1 3 [...] 5"}})
        self.assertPasses({"stop_match": {"value": "[...]"}})
        self.assertPasses({"stop_match": "[...]"})  # the field is in the output, with any value
        self.assertPasses({"not_found": "[...]"})  # null counts as in the output
        self.assertDrift({"stop_match": {"value": "9 [...]"}}, None, '$.stop_match.value: expected "9 [...]", got "1 3 2 4 5"')
        self.assertDrift({"gone": "[...]"}, None, "$.gone: missing from actual output")

    def test_failure_reports_each_field_expected_and_got(self):
        rec = self.assertDrift({"stop_match": {"value": "1 3 2 4"}, "gone": {"value": "x"}, "count": {"value": 5}}, ["not_found"],
                               '$.stop_match.value: expected "1 3 2 4", got "1 3 2 4 5"',
                               "$.gone: missing from actual output",
                               "$.not_found: expected absent, got null")
        self.assertNotIn("$.count", rec["message"])
        mismatches = {m["path"]: m for m in rec["fields"]["mismatches"]}
        self.assertEqual(set(mismatches), {"$.stop_match.value", "$.gone", "$.not_found"})
        self.assertEqual(mismatches["$.stop_match.value"], {"field": "stop_match", "path": "$.stop_match.value", "expected": "1 3 2 4", "actual": "1 3 2 4 5"})
        # A side that's absent is left out, so it can't be confused with null
        self.assertEqual(mismatches["$.gone"], {"field": "gone", "path": "$.gone", "expected": {"value": "x"}})
        self.assertEqual(mismatches["$.not_found"], {"field": "not_found", "path": "$.not_found", "actual": None})

    def test_llm_field_fails_before_any_extraction(self):
        client = FakeClient(ACTUAL)
        rec = self.run_page(code_test_page(fields_expect({"phone": {"value": "1800 123 4567"}}), config=CONFIG), client)
        self.assertEqual((rec["status"], rec["category"]), ("fail", "DOCS_MALFORMED"))
        self.assertIn("LLM method", rec["message"])
        self.assertEqual(client.extractions, 0)


class FixtureConfigRunTest(FieldRunCase):
    """A row's fixture config runs in its own temporary doc type, published to development, then deleted."""

    def test_runs_in_a_temporary_doc_type_and_deletes_it(self):
        client = FieldsClient(ACTUAL)
        rec = self.run_page(table_page([{"rowId": "id", "untested": "the method's ID"}, fields_row()]), client)
        self.assertEqual(rec["status"], "pass", rec.get("message"))
        self.assertEqual(len(client.created), 1)
        self.assertTrue(client.created[0].startswith(settings.TEMP_DOC_TYPE_PREFIX + "params_tests__stop"), client.created[0])
        self.assertEqual(json.loads(client.published[0][2]), LAYOUT)
        self.assertEqual(client.deleted_types, [f"id-{name}" for name in client.created])
        self.assertEqual(client.uploads, [])  # not the shared docs_ci_examples doc type
        self.assertEqual(rec["fields"]["extraction_id"], "e1")

    def test_mismatch_fails_and_still_deletes(self):
        client = FieldsClient(ACTUAL)
        rec = self.run_page(table_page([fields_row(expect=fields_expect({"stop_match": {"value": "1 3 2 4"}}))]), client)
        self.assertEqual((rec["status"], rec.get("category")), ("fail", "FIELDS_DRIFT"), rec.get("message"))
        self.assertIn('$.stop_match.value: expected "1 3 2 4", got "1 3 2 4 5"', rec["message"])
        self.assertIn("e1", rec["message"])  # the extraction, to open it in the app
        self.assertEqual(client.deleted_types, [f"id-{name}" for name in client.created])

    def test_failed_extraction_is_an_extraction_error(self):
        client = FieldsClient(ACTUAL, extraction_status="FAILED")
        rec = self.run_page(table_page([fields_row()]), client)
        self.assertEqual((rec["status"], rec.get("category")), ("fail", "EXTRACTION_ERROR"), rec.get("message"))
        self.assertTrue(client.created, "no temporary doc type was created")
        self.assertEqual(client.deleted_types, [f"id-{name}" for name in client.created])


if __name__ == "__main__":
    unittest.main()
