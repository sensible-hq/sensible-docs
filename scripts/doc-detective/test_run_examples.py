"""Offline tests for run_examples.py and llm_judge.py. No API keys or network needed.

Run: python3 -m unittest discover -s scripts/doc-detective
"""

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import run_examples as r  # first: it adds the local .deps folder to the import path
import llm_judge

CONFIG = {
    "fields": [
        {"id": "policy_number", "anchor": "policy number", "method": {"id": "box"}},
        {"method": {"id": "queryGroup", "queries": [{"id": "phone", "description": "customer service phone"}]}},
        {"id": "vehicles", "method": {"id": "list", "description": "insured vehicles", "properties": []}},
        {
            "method": {
                "id": "conditional",
                "condition": {"exists": {"var": "phone"}},
                "fieldsOnPass": [{"id": "_deposits", "method": {"id": "list", "description": "deposits"}}],
            }
        },
        {
            "id": "drivers",
            "method": {"id": "sections"},
            "fields": [
                {"id": "driver_name", "anchor": "name", "method": {"id": "label"}},
                {"method": {"id": "queryGroup", "queries": [{"id": "driver_age", "description": "driver's age"}]}},
            ],
        },
        # Fallback chain: a Row field, then a Query Group with the same ID
        {"id": "total", "anchor": "total", "method": {"id": "row"}},
        {"method": {"id": "queryGroup", "queries": [{"id": "total", "description": "total amount"}]}},
    ]
}


class RoutingTest(unittest.TestCase):
    def setUp(self):
        self.index = llm_judge.FieldIndex(CONFIG)

    def test_layout_field_stays_exact(self):
        self.assertIsNone(self.index.route(("policy_number", "value")))

    def test_query_group_query_is_judged(self):
        self.assertEqual(self.index.route(("phone", "value")), ("phone", "customer service phone", False))

    def test_list_property_routes_to_the_list_field(self):
        self.assertEqual(self.index.route(("vehicles", 0, "make"))[0], "vehicles")

    def test_llm_method_nested_in_conditional_is_judged(self):
        self.assertEqual(self.index.route(("_deposits", 0, "amount"))[0], "_deposits")

    def test_llm_field_in_section_is_judged(self):
        self.assertEqual(self.index.route(("drivers", 0, "driver_age", "value"))[0], "driver_age")

    def test_layout_field_in_section_stays_exact(self):
        self.assertIsNone(self.index.route(("drivers", 0, "driver_name", "value")))

    def test_fallback_chain_with_an_llm_field_is_judged_and_flagged(self):
        self.assertEqual(self.index.route(("total", "value")), ("total", "total amount", True))

    def test_root_level_mismatch_stays_exact(self):
        self.assertIsNone(self.index.route(()))


class RunExampleTest(unittest.TestCase):
    """run_example end to end, with the Sensible API and the judge replaced by stand-ins."""

    def run_with(self, docs_output, actual, verdict="pass"):
        sent = []

        def fake_judge(key, claims, model=None):
            sent.extend(claims)
            return "test-judge", [
                {"path": c["path"], "claim": "", "observed": "", "match": verdict, "confidence": 0.9, "reasoning": "stub"}
                for c in claims
            ]

        class FakeHead:
            status_code = 200

        class FakeSDK:
            def __init__(self, key):
                pass

            def extract(self, **kwargs):
                return {}

            def wait_for(self, request):
                return {"status": "COMPLETE", "parsed_document": actual}

        saved = (r.requests.head, r.ensure_doc_type, r.upload_config, r.SensibleSDK, r.load_key, llm_judge.judge)
        r.requests.head = lambda *a, **k: FakeHead()
        r.ensure_doc_type = lambda key: "type-id"
        r.upload_config = lambda *a, **k: None
        r.SensibleSDK = FakeSDK
        r.load_key = lambda var: "fake-key"
        llm_judge.judge = fake_judge
        example = {
            "config": json.dumps(CONFIG),
            "output": json.dumps(docs_output, indent=2),
            "document_url": "https://example.test/doc.pdf",
            "config_line": 0,
            "output_line": 0,
            "file": "test.md",
        }
        try:
            try:
                return sent, r.run_example("fake-key", "test", example), None
            except r.ExampleError as e:
                return sent, None, e
        finally:
            r.requests.head, r.ensure_doc_type, r.upload_config, r.SensibleSDK, r.load_key, llm_judge.judge = saved

    def test_only_llm_mismatches_reach_the_judge(self):
        docs = {
            "policy_number": {"value": "123"},
            "phone": {"value": "1800 123 4567"},
            "drivers": [{"driver_name": {"value": "Ann"}, "driver_age": {"value": "40"}}],
        }
        actual = {
            "policy_number": {"value": "999"},
            "phone": {"value": "1800-123-4567"},
            "drivers": [{"driver_name": {"value": "Bob"}, "driver_age": {"value": "forty"}}],
            "undocumented": "ignored",
        }
        sent, _, error = self.run_with(docs, actual)
        self.assertEqual([c["path"] for c in sent], ["$.phone.value", "$.drivers[0].driver_age.value"])
        self.assertEqual(error.category, "OUTPUT_DRIFT")
        self.assertIn("$.policy_number.value", str(error))
        self.assertIn("$.drivers[0].driver_name.value", str(error))
        self.assertNotIn("$.phone.value", str(error))

    def test_judge_isnt_called_when_llm_fields_match(self):
        docs = {"policy_number": {"value": "123"}, "phone": {"value": "1800 123 4567"}}
        sent, warnings, error = self.run_with(docs, docs)
        self.assertEqual(sent, [])
        self.assertEqual(warnings, [])
        self.assertIsNone(error)

    def test_judge_fail_is_llm_drift(self):
        sent, _, error = self.run_with({"phone": {"value": "1800 123 4567"}}, {"phone": {"value": "555"}}, verdict="fail")
        self.assertEqual(len(sent), 1)
        self.assertEqual(error.category, "LLM_DRIFT")

    def test_judge_partial_is_a_warning(self):
        sent, warnings, error = self.run_with({"phone": {"value": "1800 123 4567"}}, {"phone": {"value": "1800 123"}}, verdict="partial")
        self.assertIsNone(error)
        self.assertEqual(len(warnings), 1)


class ComparisonSummaryTest(unittest.TestCase):
    def summary(self, docs, actual, exact=(), judged=()):
        import contextlib, io
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            r.print_comparison("test", r.parse_json5(docs), actual, llm_judge.FieldIndex(CONFIG), list(exact), list(judged))
        return out.getvalue()

    def test_identical(self):
        self.assertIn("vs parsed_document: identical", self.summary('{"policy_number": {"value": "1"}}', {"policy_number": {"value": "1"}}))

    def test_subset_lists_what_the_docs_leave_out(self):
        text = self.summary('{"policy_number": {"value": "1"}}', {"policy_number": {"value": "1", "type": "string"}, "phone": None})
        self.assertIn("matches, not identical (docs leave out 1 field and 1 nested key)", text)
        self.assertIn("In parsed_document, not in the docs: phone", text)

    def test_abbreviated_array_and_skipped_value(self):
        text = self.summary('{"vehicles": [{"make": "A"}, ...], "phone": "..."}', {"vehicles": [{"make": "A"}, {"make": "B"}, {"make": "C"}], "phone": "x"})
        self.assertIn("$.vehicles: docs show 1 of 3 items", text)
        self.assertIn("$.phone\n", text)
        self.assertRegex(text, r"phone\s+LLM\s+not checked \(\.\.\.\)")
        self.assertIn("2 parts marked ... not checked", text)

    def test_field_kinds_and_judged_verdicts(self):
        diff = (("phone", "value"), "1", "2")
        text = self.summary('{"policy_number": {"value": "1"}, "phone": {"value": "1"}, "total": {"value": 1}}',
                            {"policy_number": {"value": "1"}, "phone": {"value": "2"}, "total": {"value": 1}},
                            judged=[(diff, "test-judge", {"match": "pass", "confidence": 0.9, "reasoning": "same"}, "pass")])
        self.assertRegex(text, r"policy_number\s+layout\s+exact match")
        self.assertRegex(text, r"phone\s+LLM\s+judged \$\.phone\.value: pass \(0\.90, test-judge\) -> PASS")
        self.assertRegex(text, r"total\s+fallback\s+exact match")
        self.assertIn("$.phone.value: same", text)
        self.assertIn("matches, not identical (1 LLM value differs, decided by the judge)", text)


if __name__ == "__main__":
    unittest.main()
