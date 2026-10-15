import json
import os
import tempfile
import unittest
from unittest import mock

from codetests import envelope, fields, record, runner, settings

from tests.fakes import CONFIG, FakeClient, FakeJudge, broken_judge, code_test, write_page


class RunnerTestCase(unittest.TestCase):
    def setUp(self):
        # An empty baselines folder, so committed baselines never leak into these tests
        self.envelopes = tempfile.TemporaryDirectory()
        self.addCleanup(self.envelopes.cleanup)
        patcher = mock.patch.dict(os.environ, {settings.ENVELOPES_DIR_VAR: self.envelopes.name})
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_test(self, documented, actual, judge=None, key="fake-key", **kwargs):
        judge = judge or FakeJudge()
        test = kwargs.pop("test", None) or code_test(documented)
        rec = runner.run_code_test(test, FakeClient(actual, **kwargs), judge=judge, judge_key=key)
        record.validate(rec)  # every record matches the schema the reports rely on
        return rec, judge


class JudgeRoutingTest(RunnerTestCase):
    def test_only_llm_mismatches_reach_the_judge(self):
        docs = {"policy_number": {"value": "123"}, "phone": {"value": "1800 123 4567"},
                "drivers": [{"driver_name": {"value": "Ann"}, "driver_age": {"value": "40"}}]}
        actual = {"policy_number": {"value": "999"}, "phone": {"value": "1800-123-4567"},
                  "drivers": [{"driver_name": {"value": "Bob"}, "driver_age": {"value": "forty"}}], "undocumented": "ignored"}
        rec, judge = self.run_test(docs, actual)
        self.assertEqual([c["path"] for c in judge.claims], ["$.phone.value", "$.drivers[0].driver_age.value"])
        self.assertEqual(rec["category"], "OUTPUT_DRIFT")
        self.assertIn("$.policy_number.value", rec["message"])
        self.assertIn("$.drivers[0].driver_name.value", rec["message"])
        self.assertNotIn("$.phone.value", rec["message"])

    def test_judge_isnt_called_when_llm_fields_match(self):
        docs = {"policy_number": {"value": "123"}, "phone": {"value": "1800 123 4567"}}
        rec, judge = self.run_test(docs, docs)
        self.assertEqual((judge.claims, rec["status"], rec["overall"]), ([], "pass", "identical"))
        self.assertNotIn("judge", rec)

    def test_judge_fail_partial_and_missing_key(self):
        docs, actual = {"phone": {"value": "1800 123 4567"}}, {"phone": {"value": "555"}}
        self.assertEqual(self.run_test(docs, actual, FakeJudge("fail"))[0]["category"], "LLM_DRIFT")
        partial, _ = self.run_test(docs, actual, FakeJudge("partial"))
        self.assertEqual((partial["status"], [w["source"] for w in partial["warnings"]]), ("warn", ["judge"]))
        self.assertEqual(self.run_test(docs, actual, key=None)[0]["category"], "JUDGE_UNAVAILABLE")

    def test_claims_carry_the_type_and_whole_field(self):
        _, judge = self.run_test({"phone": {"type": "string", "value": "1800 123 4567"}}, {"phone": {"type": "string", "value": "1800-123-4567"}})
        claim = judge.claims[0]
        self.assertEqual(claim["type"], "string")
        self.assertEqual(claim["documented_field"], {"type": "string", "value": "1800 123 4567"})
        self.assertEqual(claim["actual_field"], {"type": "string", "value": "1800-123-4567"})

    def test_judge_error_fails_closed_and_still_runs_the_envelope(self):
        documented = {"phone": {"type": "string", "value": "1800 123 4567"}}
        test = code_test(documented)
        envelope.save(envelope.build([envelope.observe_output(documented, list(fields.FieldIndex(CONFIG).llm))], test.config, "test"))
        rec, _ = self.run_test(documented, {"phone": {"type": "string", "value": "1800-123-4567"}}, judge=broken_judge, test=test)
        self.assertEqual(rec["category"], "JUDGE_ERROR")
        self.assertIn("output is outside the envelope", rec["message"])
        self.assertEqual(rec["overall"], "undecided: the judge errored")
        self.assertEqual(rec["envelope"]["status"], "outside")
        self.assertEqual(rec["llm_fields"][0]["judged"][0]["verdict"], "error")
        self.assertIn("- path: $.phone.value", rec["judge"]["user_prompt"])

    def test_each_config_is_deleted_after_its_extraction(self):
        test = code_test({})
        client = FakeClient({})
        runner.run_code_test(test, client, judge=FakeJudge(), judge_key="k")
        self.assertEqual((client.uploads, client.deleted), (["test"], ["test"]))

    def test_unreachable_document(self):
        rec, _ = self.run_test({}, {}, status=404)
        self.assertEqual(rec["category"], "DOCUMENT_UNREACHABLE")
        self.assertIn("returned 404", rec["message"])


class RecordContentTest(RunnerTestCase):
    def test_left_out_and_abbreviated(self):
        rec, _ = self.run_test({"vehicles": [{"make": "A"}, "..."], "policy_number": {"value": "1"}},
                               {"vehicles": [{"make": "A"}, {"make": "B"}, {"make": "C"}], "policy_number": {"value": "1", "type": "string"}, "phone": None})
        self.assertEqual(rec["overall"], "matches, not identical (docs leave out 1 field and 1 nested key; 1 part marked ... not checked)")
        self.assertEqual(rec["not_checked"], ["$.vehicles: docs show 1 of 3 items"])
        self.assertEqual(rec["left_out"], {"fields": ["phone"], "nested_keys": 1})

    def test_judged_field_records_the_full_exchange(self):
        rec, _ = self.run_test({"phone": {"value": "1800 123 4567"}}, {"phone": {"value": "1800-123-4567"}})
        self.assertEqual(rec["overall"], "matches, not identical (1 LLM value differs, decided by the judge)")
        judged = rec["llm_fields"][0]["judged"][0]
        self.assertEqual((judged["path"], judged["documented"], judged["actual"], judged["verdict"]), ("$.phone.value", "1800 123 4567", "1800-123-4567", "pass"))
        self.assertEqual(set(rec["judge"]), {"model", "system_prompt", "user_prompt", "raw_output"})


class EnvelopeCheckTest(RunnerTestCase):
    def test_missing_outside_and_stale(self):
        docs = {"phone": {"type": "string", "value": "1800 123 4567"}}
        test = code_test(docs)
        self.assertEqual(self.run_test(docs, docs, test=test)[0]["envelope"], {"status": "missing"})
        envelope.save(envelope.build([envelope.observe_output(docs, list(fields.FieldIndex(CONFIG).llm))], test.config, "test"))
        outside, _ = self.run_test(docs, {"phone": {"type": "string", "value": "(1800) 123.4567"}}, test=test)
        self.assertEqual((outside["status"], outside["envelope"]["status"]), ("warn", "outside"))
        self.assertEqual([w["text"][:17] for w in outside["warnings"]], ["phone: new format"])
        self.assertEqual(self.run_test(docs, docs)[0]["envelope"]["status"], "within")
        stale = code_test(docs, config={"fields": CONFIG["fields"][:2]})
        self.assertEqual(self.run_test(docs, docs, test=stale)[0]["envelope"]["status"], "stale")

    def test_invalid_baseline_fails_loudly(self):
        docs = {"phone": {"value": "1"}}
        with open(envelope.path("test"), "w") as f:
            json.dump({"runs": "ten"}, f)
        self.assertEqual(self.run_test(docs, docs)[0]["category"], "ENVELOPE_INVALID")

    def test_build_and_extend(self):
        docs = {"phone": {"type": "string", "value": "1800 123 4567"}}
        test = code_test(docs)
        client = FakeClient(docs)
        built = runner.build_envelope(test, client, 3, progress=lambda _: None)
        self.assertEqual((built["runs"], client.extractions), (3, 3))
        client.parsed = {"phone": {"type": "string", "value": "1800-123-4567"}}
        extended = runner.build_envelope(test, client, 2, extend=True, progress=lambda _: None)
        self.assertEqual(extended["runs"], 5)
        self.assertEqual(extended["slots"]["phone"]["shapes"], ["9999 999 9999", "9999-999-9999"])


class ProposeFixTest(RunnerTestCase):
    def test_writes_the_actual_values_into_the_page(self):
        documented = {"premium": {"source": "$100", "value": 100}}
        path = write_page(self, "before\n```json\n" + json.dumps(documented, indent=2) + "\n```\nafter\n")
        text = open(path).read()
        test = code_test(documented, file=path)
        test.output_span = (text.index("{"), text.rindex("}") + 1)
        rec = runner.run_code_test(test, FakeClient({"premium": {"source": "$150", "value": 150}}), judge=FakeJudge(), judge_key="k", fix=True)
        self.assertIn("Proposed fix written to", rec["message"])
        self.assertIn('"source": "$150"', open(path).read())
        self.assertTrue(open(path).read().endswith("```\nafter\n"))


if __name__ == "__main__":
    unittest.main()
