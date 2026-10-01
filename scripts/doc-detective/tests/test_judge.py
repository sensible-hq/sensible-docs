import os
import types
import unittest
from unittest import mock

from codetests import judge

CLAIM = {"path": "$.a", "prompt": "p", "type": "string", "documented": "x", "actual": "y",
         "documented_field": {"value": "x"}, "actual_field": {"value": "y"}}


class PromptTest(unittest.TestCase):
    def test_prompts_come_from_the_judge_config_files(self):
        with open(os.path.join(judge.JUDGE_DIR, "system-prompt.md"), encoding="utf-8") as f:
            self.assertEqual(judge.CONFIG["system_prompt"], f.read().strip())
        prompt = judge.build_user_prompt([CLAIM])
        for line in ("- path: $.a", 'documented: "x"', 'actual: "y"', "declared type: string", 'whole field as returned: {"value": "y"}'):
            self.assertIn(line, prompt)
        self.assertNotIn("$claims", prompt)

    def test_classify(self):
        self.assertEqual(judge.classify({"match": "pass", "confidence": 0.9}), "pass")
        self.assertEqual(judge.classify({"match": "pass", "confidence": 0.5}), "warn")
        self.assertEqual(judge.classify({"match": "partial", "confidence": 0.9}), "warn")
        self.assertEqual(judge.classify({"match": "fail", "confidence": 0.99}), "fail")


class JudgeCallTest(unittest.TestCase):
    def call(self, text, stop_reason="end_turn"):
        response = types.SimpleNamespace(stop_reason=stop_reason, model="test-model", content=[types.SimpleNamespace(type="text", text=text)])
        client = mock.Mock()
        client.messages.create.return_value = response
        with mock.patch("anthropic.Anthropic", return_value=client):
            return judge.judge("key", [CLAIM], "test-model")

    def test_returns_the_full_exchange(self):
        exchange = self.call('{"results": [{"path": "$.a", "claim": "c", "observed": "o", "match": "pass", "confidence": 0.9, "reasoning": "r"}]}')
        self.assertEqual(exchange["results"][0]["match"], "pass")
        self.assertEqual(set(exchange), {"model", "system_prompt", "user_prompt", "raw_output", "results"})

    def test_unusable_output_fails_closed_with_the_exchange(self):
        for text, stop, message in [
            ("not json", "end_turn", "isn't the expected JSON"),
            ('{"results": []}', "end_turn", "didn't return a verdict for $.a"),
            ("", "refusal", "declined"),
            ("{", "max_tokens", "cut off"),
        ]:
            with self.subTest(message):
                with self.assertRaises(judge.JudgeError) as caught:
                    self.call(text, stop)
                self.assertIn(message, str(caught.exception))
                self.assertIn("- path: $.a", caught.exception.exchange["user_prompt"])


if __name__ == "__main__":
    unittest.main()
