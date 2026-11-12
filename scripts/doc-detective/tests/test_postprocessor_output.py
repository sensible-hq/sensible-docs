"""Code tests compare a documented "postprocessorOutput" with the extraction's postprocessorOutput."""

import os
import sys
import tempfile
import types
import unittest
from unittest import mock

from codetests import envelope, fields, record, runner, sensible, settings
from codetests.errors import CONFIG_INVALID, CodeTestError

from tests.fakes import CONFIG, FakeClient, FakeJudge, code_test

PARSED = {"policy_number": {"type": "string", "value": "123"}}
POSTPROCESSED = {"custom_object": {"policy": "123", "count": 2}}


class ActualOutputTest(unittest.TestCase):
    def test_parsed_document_alone_without_a_postprocessor(self):
        self.assertEqual(sensible.actual_output({"parsed_document": PARSED}), PARSED)
        self.assertEqual(sensible.actual_output({"parsed_document": PARSED, "postprocessorOutput": None}), PARSED)

    def test_adds_postprocessor_output_as_a_top_level_key(self):
        result = {"parsed_document": PARSED, "postprocessorOutput": POSTPROCESSED}
        self.assertEqual(sensible.actual_output(result), {**PARSED, "postprocessorOutput": POSTPROCESSED})
        self.assertEqual(result["parsed_document"], PARSED)  # the response isn't changed

    def test_a_scalar_postprocessor_output(self):
        # The XML postprocessor returns a string; a JsonLogic rule can return any JSON value
        self.assertEqual(sensible.actual_output({"parsed_document": {}, "postprocessorOutput": "<a/>"}), {"postprocessorOutput": "<a/>"})
        self.assertEqual(sensible.actual_output({"postprocessorOutput": False}), {"postprocessorOutput": False})

    def test_without_parsed_document(self):
        # keepParsedDocument: false
        self.assertEqual(sensible.actual_output({"postprocessorOutput": POSTPROCESSED}), {"postprocessorOutput": POSTPROCESSED})

    def test_a_field_named_postprocessor_output_is_an_error(self):
        with self.assertRaises(CodeTestError) as caught:
            sensible.actual_output({"parsed_document": {"postprocessorOutput": {"value": 1}}, "postprocessorOutput": 2})
        self.assertEqual(caught.exception.category, CONFIG_INVALID)


class ClientExtractTest(unittest.TestCase):
    """SensibleClient.extract returns actual_output() of the finished extraction."""

    def extract(self, result):
        sdk = mock.Mock()
        sdk.return_value.extract.return_value = {"id": "e1"}
        client = sensible.SensibleClient("key")
        with mock.patch.dict(sys.modules, {"sensibleapi": types.SimpleNamespace(SensibleSDK=sdk)}), \
             mock.patch.object(client, "_wait", return_value={"status": "COMPLETE", "configuration": "t", **result}):
            return client.extract("https://example.test/doc.pdf", "docs_ci_sample_p__t", "t", "ci__t.pdf")

    def test_includes_postprocessor_output(self):
        self.assertEqual(self.extract({"parsed_document": PARSED, "postprocessorOutput": POSTPROCESSED}),
                         {**PARSED, "postprocessorOutput": POSTPROCESSED})

    def test_parsed_document_alone_without_one(self):
        self.assertEqual(self.extract({"parsed_document": PARSED}), PARSED)


class RunTest(unittest.TestCase):
    def setUp(self):
        envelopes = tempfile.TemporaryDirectory()
        self.addCleanup(envelopes.cleanup)
        patcher = mock.patch.dict(os.environ, {settings.ENVELOPES_DIR_VAR: envelopes.name})
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_test(self, documented, parsed, postprocessed=None, judge=None, key="fake-key"):
        judge = judge or FakeJudge()
        rec = runner.run_code_test(code_test(documented), FakeClient(parsed, postprocessor_output=postprocessed), judge=judge, judge_key=key)
        record.validate(rec)
        return rec, judge

    def test_documented_postprocessor_output_passes_when_it_matches(self):
        rec, judge = self.run_test({**PARSED, "postprocessorOutput": POSTPROCESSED}, PARSED, POSTPROCESSED)
        self.assertEqual((rec["status"], rec["overall"], judge.claims), ("pass", "identical", []))

    def test_documented_postprocessor_output_fails_with_a_diff(self):
        changed = {"custom_object": {"policy": "999", "count": 2}}
        rec, _ = self.run_test({**PARSED, "postprocessorOutput": POSTPROCESSED}, PARSED, changed)
        self.assertEqual(rec["category"], "OUTPUT_DRIFT")
        self.assertIn('$.postprocessorOutput.custom_object.policy: expected "123", got "999"', rec["message"])

    def test_documented_postprocessor_output_fails_when_there_is_none(self):
        rec, _ = self.run_test({**PARSED, "postprocessorOutput": POSTPROCESSED}, PARSED)
        self.assertEqual(rec["category"], "OUTPUT_DRIFT")
        self.assertIn("$.postprocessorOutput: missing from actual output", rec["message"])

    def test_a_scalar_postprocessor_output(self):
        rec, _ = self.run_test({"postprocessorOutput": "jsonlogic"}, {}, "JsonLOGIC")
        self.assertIn('$.postprocessorOutput: expected "jsonlogic", got "JsonLOGIC"', rec["message"])

    def test_output_without_postprocessor_output_is_unchanged(self):
        before, _ = self.run_test(PARSED, PARSED)
        rec, _ = self.run_test(PARSED, PARSED, postprocessed=None)
        self.assertEqual(rec, before)
        self.assertEqual((rec["status"], rec["overall"]), ("pass", "identical"))
        changed, _ = self.run_test(PARSED, {"policy_number": {"type": "string", "value": "999"}})
        self.assertEqual(changed["category"], "OUTPUT_DRIFT")
        self.assertIn('$.policy_number.value: expected "123", got "999"', changed["message"])

    def test_undocumented_postprocessor_output_is_left_out_not_failed(self):
        rec, _ = self.run_test(PARSED, PARSED, POSTPROCESSED)
        self.assertEqual(rec["status"], "pass")
        self.assertEqual(rec["left_out"]["fields"], ["postprocessorOutput"])

    def test_llm_values_under_postprocessor_output_go_to_the_judge(self):
        # Same rule as parsed_document: a value under a key that's an LLM field's ID is judged
        documented = {"postprocessorOutput": {"phone": {"value": "1800 123 4567"}, "policy": "123"}}
        rec, judge = self.run_test(documented, {}, {"phone": {"value": "1800-123-4567"}, "policy": "123"})
        self.assertEqual([c["path"] for c in judge.claims], ["$.postprocessorOutput.phone.value"])
        self.assertEqual(judge.claims[0]["prompt"], "customer service phone")
        self.assertEqual(rec["status"], "pass")

    def test_envelope_ignores_postprocessor_output(self):
        output = sensible.actual_output({"parsed_document": {"phone": {"value": "1"}}, "postprocessorOutput": {"phone": {"value": "2"}}})
        observed = envelope.observe_output(output, list(fields.FieldIndex(CONFIG).llm))
        self.assertEqual(observed, envelope.observe_output({"phone": {"value": "1"}}, list(fields.FieldIndex(CONFIG).llm)))


class ProbeBlankTest(unittest.TestCase):
    def test_compares_postprocessor_output(self):
        test = code_test({"postprocessorOutput": "jsonlogic"})
        matching = runner.probe_blank(test, FakeClient({}, postprocessor_output="jsonlogic"))
        self.assertEqual(matching["unchanged"], True, matching)
        different = runner.probe_blank(test, FakeClient({}, postprocessor_output="JsonLOGIC"))
        self.assertEqual(different["unchanged"], False)
        self.assertIn("$.postprocessorOutput", different["detail"])


if __name__ == "__main__":
    unittest.main()
