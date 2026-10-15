import os
import tempfile
import unittest
from unittest import mock

from codetests import runner, settings
from codetests.reports import doc_detective, envelope_issue, html, issue, text, wording

from tests.fakes import CODE_TEST_PAGE, FakeClient, FakeJudge, code_test, write_page


def make_record(documented, actual, match="pass"):
    with tempfile.TemporaryDirectory() as d, mock.patch.dict(os.environ, {settings.ENVELOPES_DIR_VAR: d}):
        return runner.run_code_test(code_test(documented), FakeClient(actual), judge=FakeJudge(match), judge_key="k")


def envelope_record(status, breaches=None, judged=None, verdict_status="pass"):
    return {"test_id": "t", "file": "doc.md", "status": verdict_status,
            "envelope": {"status": status, "runs": 10, "built": "2026-10-01", "breaches": breaches or {}},
            "llm_fields": [{"field": "phone", "judged": judged or []}]}


class TextSummaryTest(unittest.TestCase):
    def test_lists_llm_fields_and_counts_layout_fields(self):
        lines = "\n".join(text.summary(make_record({"policy_number": {"value": "1"}, "phone": {"value": "a"}}, {"policy_number": {"value": "1"}, "phone": {"value": "b"}})))
        self.assertIn("LLM field phone: [judge] decided", lines)
        self.assertIn("Layout fields: 1, all exact match", lines)
        self.assertNotIn("policy_number", lines)
        self.assertIn('[judge] PASS  $.phone.value: "a" -> "b"', lines)
        self.assertIn("[envelope] no baseline yet", lines)

    def test_result_line_names_warning_sources(self):
        rec = {"test_id": "t", "status": "warn", "warnings": [{"source": "envelope", "text": "a"}, {"source": "envelope", "text": "b"}, {"source": "judge", "text": "c"}]}
        self.assertEqual(text.result_line(rec), "PASS t with warnings: 2 [envelope], 1 [judge]")


class WordingTest(unittest.TestCase):
    def test_envelope_sentence_names_the_baseline_size(self):
        self.assertIn("an established 10-result baseline of acceptable variance", wording.envelope_sentence([{"envelope": {"runs": 10}}]))
        self.assertIn("against an established baseline of", wording.envelope_sentence([{"envelope": {"status": "missing"}}]))
        self.assertIn("against an established baseline of", wording.envelope_sentence([{"envelope": {"runs": 10}}, {"envelope": {"runs": 5}}]))

    def test_triage_combinations(self):
        def row(verdict, breaches, status="outside"):
            rec = {"llm_fields": [{"field": "phone", "judged": [{"path": "$.phone.value", "verdict": verdict}]}], "envelope": {"status": status, "breaches": breaches}}
            return wording.triage_rows(rec)[0]
        self.assertIn("Likely a regression", row("fail", {"phone": ["x"]})[3])
        self.assertIn("Fix the docs", row("fail", {}, "within")[3])
        self.assertIn("investigate the output now", row("error", {"phone": ["x"]})[3])
        self.assertIn("the product probably didn't change", row("error", {}, "within")[3])
        self.assertIn("Rebuild the baseline", row("fail", {}, "missing")[3])
        self.assertEqual(row("fail", {"other": ["x"]})[2], "within")


class EnvelopeIssueTest(unittest.TestCase):
    def test_clear_none_and_attention(self):
        self.assertEqual(envelope_issue.decide([envelope_record("within")])["state"], "clear")
        self.assertEqual(envelope_issue.decide([{"test_id": "t"}])["state"], "none")
        result = envelope_issue.decide([envelope_record("outside", {"phone": ["new format 'x'"]}, [{"verdict": "pass"}])], "RUN")
        self.assertEqual(result["state"], "attention")
        self.assertIn("`phone`: new format 'x' (judge passed it: the feature's behavior likely changed)", result["body"])
        self.assertIn('code_tests.py --file "doc.md" --test t --build-envelope 10', result["body"])
        self.assertIn(f"<!-- envelope-fingerprint: {result['fingerprint']} -->", result["body"])

    def test_notes_stale_and_missing(self):
        self.assertIn("judge failed it", envelope_issue.decide([envelope_record("outside", {"phone": ["r"]}, [{"verdict": "fail"}])])["body"])
        self.assertIn("the judge errored", envelope_issue.decide([envelope_record("outside", {"phone": ["r"]}, [{"verdict": "error"}])])["body"])
        self.assertIn("matched the docs exactly", envelope_issue.decide([envelope_record("outside", {"phone": ["r"]})])["body"])
        self.assertIn("baseline is stale", envelope_issue.decide([envelope_record("stale")])["body"])
        self.assertIn("no baseline yet", envelope_issue.decide([envelope_record("missing")])["body"])

    def test_fingerprint_is_stable_and_changes_with_breaches(self):
        a = envelope_issue.decide([envelope_record("outside", {"phone": ["r1"], "phone.x": ["r2"]})], "RUN 1")
        b = envelope_issue.decide([envelope_record("outside", {"phone.x": ["r2"], "phone": ["r1"]})], "RUN 2")
        c = envelope_issue.decide([envelope_record("outside", {"phone": ["r3"]})])
        self.assertEqual(a["fingerprint"], b["fingerprint"])
        self.assertNotEqual(a["fingerprint"], c["fingerprint"])


class FailureIssueTest(unittest.TestCase):
    def test_lists_failed_ui_steps_code_tests_and_triage(self):
        ui = {"app": {"status": "fail", "steps": [{"description": "Log in", "action": "click", "result": "fail", "message": "Element not found"}], "failed": 1}}
        rec = make_record({"phone": {"value": "1800 123 4567"}}, {"phone": {"value": "555"}}, match="fail")
        body = issue.body(ui, [rec], run_url="RUN")
        self.assertIn("**Log in** failed: Element not found", body)
        self.assertIn("### `test` (code test)", body)
        self.assertIn("LLM_DRIFT", body)
        self.assertIn("| `test` | `$.phone.value` | fail | missing |", body)
        self.assertIn("labeled `[judge]`", body)


class VerifyUiTest(unittest.TestCase):
    def test_missing_tests_and_skipped_steps(self):
        from codetests import markup
        page = markup.parse_page(write_page(self, '<!-- test {"testId": "a"} -->\n<!-- step {"goTo": "https://x.test"} -->\n<!-- step {"find": "x"} -->\n<!-- test end -->\n'
                                                   '<!-- test {"testId": "b"} -->\n<!-- step {"goTo": "https://x.test"} -->\n<!-- test end -->\n'))
        step = {"description": "", "action": "go to", "result": "pass", "message": "", "seconds": 0}
        self.assertEqual(doc_detective.verify_ui(page, {"a": {"status": "pass", "steps": [step, step], "failed": 0}, "b": {"status": "pass", "steps": [step], "failed": 0}}), [])
        problems = doc_detective.verify_ui(page, {"a": {"status": "pass", "steps": [step], "failed": 0}})
        self.assertIn("a  Doc Detective skipped 1 of its 2 steps", problems[0])
        self.assertIn("b  Doc Detective didn't run this UI test", problems[1])


class HtmlReportTest(unittest.TestCase):
    def render(self, records, ui_results=None, page_text=None):
        page = write_page(self, page_text or CODE_TEST_PAGE.replace('"first"', '"test"'))
        with tempfile.TemporaryDirectory() as d:
            with open(html.render(page, ui_results or {}, records, os.path.join(d, "report.html")), encoding="utf-8") as f:
                return f.read()

    def test_shows_llm_fields_prompt_and_output_escaped(self):
        page = self.render([make_record({"phone": {"value": "<b>1</b>"}}, {"phone": {"value": "<b>2</b>"}})])
        for expected in ("<code>phone</code>", "Full prompt the judge received", "Full judge output (JSON)", "&lt;b&gt;1&lt;/b&gt;", 'class="disclaimer"', "Code test"):
            self.assertIn(expected, page)
        self.assertIn("unless it&#x27;s labeled <span class=\"chip judge\"", page)
        self.assertGreaterEqual(page.count('class="chip judge"'), 4)  # disclaimer, field result, reasoning heading, verdict card
        self.assertNotIn("<b>1</b>", page)

    def test_only_tests_needing_attention_start_open(self):
        identical = make_record({"phone": {"value": "x"}}, {"phone": {"value": "x"}})
        identical["envelope"] = {"status": "within", "runs": 10, "built": "2026-10-01", "breaches": {}, "slots": {}}
        self.assertFalse(html.needs_attention(identical))
        self.assertIn('<details class="card test" id="test">', html.render_code_test(identical))
        self.assertIn("The judge wasn&#x27;t called", html.render_code_test(identical).replace("wasn't", "wasn&#x27;t"))
        self.assertTrue(html.needs_attention(dict(identical, status="fail", message="m")))
        self.assertTrue(html.needs_attention(dict(identical, envelope={"status": "outside", "runs": 10, "built": "x", "breaches": {}})))

    def test_ui_steps_show_descriptions_never_typed_text_and_unrun_tests(self):
        steps = [
            {"description": "Log into account: enter the password", "type": {"keys": "hunter2", "selector": 'input[name="password"]'}, "result": "PASS", "durationMs": 200},
            {"description": "Log into account: click Sign in", "click": {"selector": "form button", "elementText": "Sign in"}, "result": "FAIL", "resultDescription": "Element not found", "durationMs": 5000},
        ]
        summaries = [doc_detective.step_summary(s) for s in steps]
        self.assertEqual(summaries[0]["action"], 'type into input[name="password"]')
        self.assertEqual(summaries[1]["action"], 'click form button with text "Sign in"')
        ui_page = '<!-- test {"testId": "ui_a", "description": "Sign in"} -->\n<!-- step {"goTo": "https://x.test"} -->\n<!-- test end -->\n' \
                  '<!-- test {"testId": "ui_b", "description": "Never runs"} -->\n<!-- step {"goTo": "https://x.test"} -->\n<!-- test end -->\n'
        page = self.render([], {"ui_a": {"status": "fail", "steps": summaries, "failed": 1}}, ui_page)
        self.assertIn("Log into account: enter the password", page)
        self.assertIn("Element not found", page)
        self.assertNotIn("hunter2", page)
        self.assertIn("Not run", page)
        self.assertIn("Doc Detective didn&#x27;t run this test", page.replace("didn't", "didn&#x27;t"))


if __name__ == "__main__":
    unittest.main()
