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

    def run_with(self, docs_output, actual, verdict="pass", record=None):
        sent = []

        def fake_judge(key, claims, model=None):
            sent.extend(claims)
            results = [
                {"path": c["path"], "claim": "", "observed": "", "match": verdict, "confidence": 0.9, "reasoning": "stub"}
                for c in claims
            ]
            return {"model": "test-judge", "system_prompt": "SYSTEM", "user_prompt": llm_judge.build_user_prompt(claims),
                    "raw_output": json.dumps({"results": results}), "results": results}

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
                return sent, r.run_example("fake-key", "test", example, record=record), None
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


class RecordTest(unittest.TestCase):
    """What run_example records for the summary and the HTML report."""

    def run_record(self, docs, actual, verdict="pass"):
        record = {"test_id": "test"}
        RunExampleTest.run_with(RunExampleTest(), docs, actual, verdict, record)
        return record

    def test_identical(self):
        docs = {"policy_number": {"value": "1"}, "phone": {"value": "x"}}
        record = self.run_record(docs, docs)
        self.assertEqual(record["overall"], "identical")
        self.assertEqual([f["field"] for f in record["llm_fields"]], ["phone"])
        self.assertEqual(record["llm_fields"][0]["judged"], [])
        self.assertEqual(record["layout"], {"fields": 1, "mismatches": []})
        self.assertNotIn("judge", record)

    def test_left_out_and_abbreviated(self):
        record = self.run_record(
            {"vehicles": [{"make": "A"}, "..."], "policy_number": {"value": "1"}},
            {"vehicles": [{"make": "A"}, {"make": "B"}, {"make": "C"}], "policy_number": {"value": "1", "type": "string"}, "phone": None},
        )
        self.assertEqual(record["overall"], "matches, not identical (docs leave out 1 field and 1 nested key; 1 part marked ... not checked)")
        self.assertEqual(record["not_checked"], ["$.vehicles: docs show 1 of 3 items"])
        self.assertEqual(record["left_out"], {"fields": ["phone"], "nested_keys": 1})

    def test_judged_field_records_the_full_exchange(self):
        record = self.run_record({"phone": {"value": "1800 123 4567"}}, {"phone": {"value": "1800-123-4567"}})
        self.assertEqual(record["overall"], "matches, not identical (1 LLM value differs, decided by the judge)")
        judged = record["llm_fields"][0]["judged"][0]
        self.assertEqual((judged["path"], judged["documented"], judged["actual"], judged["verdict"]), ("$.phone.value", "1800 123 4567", "1800-123-4567", "pass"))
        self.assertEqual(set(record["judge"]), {"model", "system_prompt", "user_prompt", "raw_output"})
        self.assertIn("$.phone.value", record["judge"]["user_prompt"])

    def test_summary_lists_llm_fields_and_counts_layout_fields(self):
        import contextlib, io
        record = self.run_record({"policy_number": {"value": "1"}, "phone": {"value": "a"}}, {"policy_number": {"value": "1"}, "phone": {"value": "b"}})
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            r.print_summary(record)
        text = out.getvalue()
        self.assertIn("LLM field phone: [judge] decided", text)
        self.assertIn("deterministic (an exact comparison) unless it's labeled [judge]", text)
        self.assertIn("Layout fields: 1, all exact match", text)
        self.assertNotIn("policy_number", text)
        self.assertIn('[judge] PASS  $.phone.value: "a" -> "b"', text)


class TypeTest(unittest.TestCase):
    CONFIG = {"fields": [
        {"method": {"id": "queryGroup", "queries": [
            {"id": "premium", "description": "premium", "type": "currency"},
            {"id": "notes", "description": "notes"},
            {"id": "price_eur", "description": "price", "type": {"id": "currency", "currencySymbol": "€"}},
        ]}},
        {"id": "dinners", "type": "table", "method": {"id": "list", "description": "dinners", "properties": [
            {"id": "dish", "description": "dish"}, {"id": "price", "description": "price", "type": "currency"}]}},
        {"id": "vehicles", "type": "table", "method": {"id": "nlpTable", "description": "vehicles", "columns": [
            {"id": "make", "description": "make"}, {"id": "year", "description": "year", "type": "number"}]}},
    ]}
    DOCS = {"vehicles": {"columns": [{"id": "make", "values": [{"value": "Honda"}]}, {"id": "year", "values": [{"value": 2015}]}]}}

    def setUp(self):
        self.index = llm_judge.FieldIndex(self.CONFIG)

    def test_query_group_query_type(self):
        self.assertEqual(self.index.type_for(("premium", "value"), {}), "currency")

    def test_undeclared_type_is_string(self):
        self.assertEqual(self.index.type_for(("notes", "value"), {}), "string")
        self.assertEqual(self.index.type_for(("dinners", 0, "dish", "value"), {}), "string")

    def test_list_property_type(self):
        self.assertEqual(self.index.type_for(("dinners", 1, "price", "value"), {}), "currency")

    def test_nlp_table_column_type_is_read_from_the_output(self):
        self.assertEqual(self.index.type_for(("vehicles", "columns", 1, "values", 0, "value"), self.DOCS), "number")
        self.assertEqual(self.index.type_for(("vehicles", "columns", 0, "values", 0, "value"), self.DOCS), "string")

    def test_configurable_type_keeps_its_options(self):
        declared = self.index.type_for(("price_eur", "value"), {})
        self.assertEqual(llm_judge.format_type(declared), 'currency with options {"currencySymbol": "\u20ac"}')
        self.assertIn('"unit": "$"', llm_judge.type_example(declared))

    def test_type_examples_come_from_types_md(self):
        examples = llm_judge.CONFIG["type_examples"]
        self.assertEqual(examples["number"], '{ "source": "123456789", "value": 123456789, "type": "number" }')
        self.assertIn('"+18557863246"', examples["phoneNumber"])
        self.assertEqual(llm_judge.type_example("table"), "none in the type reference")

    def test_claim_carries_type_and_whole_field(self):
        sent, _, _ = RunExampleTest().run_with(
            {"phone": {"type": "string", "value": "1800 123 4567"}},
            {"phone": {"type": "string", "value": "1800-123-4567"}},
        )
        claim = sent[0]
        self.assertEqual(claim["type"], "string")
        self.assertEqual(claim["documented_field"], {"type": "string", "value": "1800 123 4567"})
        self.assertEqual(claim["actual_field"], {"type": "string", "value": "1800-123-4567"})
        prompt = llm_judge.build_user_prompt(sent)
        self.assertIn("declared type: string", prompt)
        self.assertIn('whole field as returned: {"type": "string", "value": "1800-123-4567"}', prompt)


class PromptConfigTest(unittest.TestCase):
    def test_prompts_come_from_judge_files(self):
        with open(os.path.join(llm_judge.JUDGE_DIR, "system-prompt.md"), encoding="utf-8") as f:
            self.assertEqual(llm_judge.CONFIG["system_prompt"], f.read().strip())
        prompt = llm_judge.build_user_prompt([{"path": "$.a", "prompt": "p", "documented": "x", "observed": "y"}])
        self.assertIn("- path: $.a", prompt)
        self.assertIn('documented: "x"', prompt)
        self.assertNotIn("$claims", prompt)


class HtmlReportTest(unittest.TestCase):
    def test_report_shows_llm_fields_prompt_and_output_escaped(self):
        import tempfile
        import html_report
        record = RecordTest().run_record({"phone": {"value": "<b>1</b>"}}, {"phone": {"value": "<b>2</b>"}})
        record.update(file="doc.md", document_url="https://example.test/doc.pdf", status="pass")
        with tempfile.TemporaryDirectory() as out:
            os.makedirs(os.path.join(out, "examples"))
            with open(os.path.join(out, "examples", "test.json"), "w") as f:
                json.dump(record, f)
            with open(html_report.render(out), encoding="utf-8") as f:
                page = f.read()
        self.assertIn("<code>phone</code>", page)
        self.assertIn("Full prompt the judge received", page)
        self.assertIn("Full judge output (JSON)", page)
        self.assertIn("&lt;b&gt;1&lt;/b&gt;", page)
        self.assertIn('class="disclaimer"', page)
        self.assertIn("unless it&#x27;s labeled <span class=\"chip judge\"", page)
        self.assertGreaterEqual(page.count('class="chip judge"'), 4)  # disclaimer, field result, reasoning heading, verdict card
        self.assertNotIn("<b>1</b>", page)


class UiStepTest(unittest.TestCase):
    def test_steps_show_descriptions_and_never_typed_text(self):
        import html_report
        steps = [
            {"description": "Log into account: enter the password", "type": {"keys": "hunter2", "selector": "input[name=\"password\"]"}, "result": "PASS", "durationMs": 200},
            {"description": "Log into account: click Sign in", "click": {"selector": "form button", "elementText": "Sign in"}, "result": "FAIL", "resultDescription": "Element not found", "durationMs": 5000},
        ]
        summaries = [html_report.step_summary(s) for s in steps]
        self.assertEqual(summaries[0]["action"], 'type into input[name="password"]')
        self.assertEqual(summaries[1]["action"], 'click form button with text "Sign in"')
        page = html_report.render_ui_test({"test_id": "ui", "description": "Sign in", "status": "fail", "steps": summaries, "failed": 1})
        self.assertIn("Log into account: enter the password", page)
        self.assertIn("Element not found", page)
        self.assertNotIn("hunter2", page)


class EnvelopeTest(unittest.TestCase):
    import envelope as env

    def phone(self, value, confidence="confident_answer"):
        return {"phone": {"type": "string", "value": value, "confidenceSignal": confidence}}

    def baseline(self, outputs, keys=("phone",)):
        return self.env.build([self.env.observe_output(o, keys) for o in outputs], "CONFIG", "t")

    def test_shape(self):
        self.assertEqual(self.env.shape("1800-123-4567"), "9999-999-9999")
        self.assertEqual(self.env.shape("Ab 12"), "aa 99")

    def test_within_the_envelope(self):
        base = self.baseline([self.phone("1800 123 4567"), self.phone("1800-123-4567")])
        self.assertEqual(base["slots"]["phone"]["shapes"], ["9999 999 9999", "9999-999-9999"])
        self.assertEqual(self.env.check(base, self.env.observe_output(self.phone("1800-123-4567"), ["phone"])), {})

    def test_new_format_null_and_confidence_breach(self):
        base = self.baseline([self.phone("1800 123 4567")] * 3)
        new_format = self.env.check(base, self.env.observe_output(self.phone("(1800) 123.4567"), ["phone"]))
        self.assertIn("new format", new_format["phone"][0])
        nulled = self.env.check(base, self.env.observe_output({"phone": {"type": "string", "value": None}}, ["phone"]))
        self.assertEqual(nulled["phone"], ["null; never null in the baseline"])
        unsure = self.env.check(base, self.env.observe_output(self.phone("1800 123 4567", "unsure"), ["phone"]))
        self.assertIn("confidence signal unsure", unsure["phone"][0])

    def test_numbers_units_and_types(self):
        money = lambda v, unit="$", typ="currency": {"premium": {"source": str(v), "value": v, "unit": unit, "type": typ}}
        base = self.baseline([money(100), money(110)], ("premium",))
        self.assertEqual(self.env.check(base, self.env.observe_output(money(105), ["premium"])), {})
        self.assertEqual(self.env.check(base, self.env.observe_output(money(900), ["premium"]))["premium"],
                         ["value 900; baseline values ranged from 100 to 110"])
        single = self.baseline([money(100)], ("premium",))
        self.assertIn("value 50; baseline value was always 100", self.env.check(single, self.env.observe_output(money(50), ["premium"]))["premium"])
        self.assertIn("unit €", self.env.check(base, self.env.observe_output(money(100, "€"), ["premium"]))["premium"][0])
        typed = self.env.check(base, self.env.observe_output(money(100, typ="number"), ["premium"]))["premium"]
        self.assertIn("type number", typed[0])
        self.assertEqual(base["slots"]["premium"]["source_shapes"], ["999"])
        source = self.env.check(base, self.env.observe_output({"premium": {"source": "$100", "value": 100, "unit": "$", "type": "currency"}}, ["premium"]))
        self.assertIn("new source format '$999'", source["premium"][0])

    def test_string_length(self):
        text = lambda s: {"summary": {"type": "string", "value": s}}
        sentences = ["The policy covers two vehicles and one driver.", "Covers two vehicles, one driver, and roadside help."]
        base = self.baseline([text(s) for s in sentences], ("summary",))
        self.assertEqual(base["slots"]["summary"]["shapes"], "free text")
        within = "The policy covers two cars and a single driver."
        self.assertEqual(self.env.check(base, self.env.observe_output(text(within), ["summary"])), {})
        self.assertIn("length 5", self.env.check(base, self.env.observe_output(text("short"), ["summary"]))["summary"][0])

    def test_list_and_table_counts(self):
        rows = lambda n: {"vehicles": [{"make": {"type": "string", "value": "Honda"}}] * n}
        base = self.baseline([rows(2), rows(3)], ("vehicles",))
        self.assertIn("vehicles#count", base["slots"])
        self.assertIn("vehicles[*].make", base["slots"])
        self.assertEqual(self.env.check(base, self.env.observe_output(rows(1), ["vehicles"]))["vehicles#count"],
                         ["1 item; baseline item counts ranged from 2 to 3"])
        table = {"t": {"columns": [{"id": "year", "values": [{"type": "number", "value": 2015}]}]}}
        self.assertIn("t.columns[year].values[*]", self.baseline([table], ("t",))["slots"])

    def test_missing_and_stale_baselines(self):
        import tempfile
        index = llm_judge.FieldIndex(CONFIG)
        example = {"config": "CONFIG"}
        with tempfile.TemporaryDirectory() as d:
            saved, r.ENVELOPES_DIR = r.ENVELOPES_DIR, d
            try:
                record = {}
                self.assertEqual(r.check_envelope(record, "t", example, self.phone("1"), index), [])
                self.assertEqual(record["envelope"]["status"], "missing")
                with open(os.path.join(d, "t.json"), "w") as f:
                    json.dump(self.baseline([self.phone("1800 123 4567")]), f)
                record = {}
                warnings = r.check_envelope(record, "t", example, self.phone("(1800) 123.4567"), index)
                self.assertEqual(record["envelope"]["status"], "outside")
                self.assertTrue(warnings[0].startswith("envelope: phone: new format"))
                record = {}
                r.check_envelope(record, "t", {"config": "CHANGED"}, self.phone("1"), index)
                self.assertEqual(record["envelope"]["status"], "stale")
            finally:
                r.ENVELOPES_DIR = saved


class DisclaimerTest(unittest.TestCase):
    def test_envelope_sentence_names_the_baseline_size(self):
        import html_report
        self.assertIn("an established 10-result baseline of acceptable variance", html_report.envelope_sentence([{"envelope": {"runs": 10}}]))
        self.assertIn("against an established baseline of", html_report.envelope_sentence([{"envelope": {"status": "missing"}}]))
        self.assertIn("against an established baseline of", html_report.envelope_sentence([{"envelope": {"runs": 10}}, {"envelope": {"runs": 5}}]))


class EnvelopeIssueTest(unittest.TestCase):
    import envelope_issue as ei

    def record(self, status, breaches=None, judged=None):
        return {"test_id": "t", "file": "doc.md", "envelope": {"status": status, "runs": 10, "built": "2026-10-01", "breaches": breaches or {}},
                "llm_fields": [{"field": "phone", "judged": judged or []}]}

    def test_clear_none_and_attention(self):
        self.assertEqual(self.ei.decide([self.record("within")])["state"], "clear")
        self.assertEqual(self.ei.decide([{"test_id": "t"}])["state"], "none")
        result = self.ei.decide([self.record("outside", {"phone": ["new format 'x'"]}, [{"verdict": "pass"}])], "RUN")
        self.assertEqual(result["state"], "attention")
        self.assertIn("`phone`: new format 'x' (**judge passed it**: the feature's behavior likely changed)", result["body"])
        self.assertIn("--build-envelope 10", result["body"])
        self.assertIn(f"<!-- envelope-fingerprint: {result['fingerprint']} -->", result["body"])

    def test_judge_failed_and_exact_match_notes(self):
        failed = self.ei.decide([self.record("outside", {"phone": ["r"]}, [{"verdict": "fail"}])])["body"]
        self.assertIn("judge failed it", failed)
        exact = self.ei.decide([self.record("outside", {"phone": ["r"]})])["body"]
        self.assertIn("matched the docs exactly", exact)

    def test_stale_and_missing_need_attention(self):
        self.assertIn("baseline is stale", self.ei.decide([self.record("stale")])["body"])
        self.assertIn("no baseline yet", self.ei.decide([self.record("missing")])["body"])

    def test_fingerprint_is_stable_and_changes_with_breaches(self):
        a = self.ei.decide([self.record("outside", {"phone": ["r1"], "phone.x": ["r2"]})], "RUN 1")
        b = self.ei.decide([self.record("outside", {"phone.x": ["r2"], "phone": ["r1"]})], "RUN 2")
        c = self.ei.decide([self.record("outside", {"phone": ["r3"]})])
        self.assertEqual(a["fingerprint"], b["fingerprint"])
        self.assertNotEqual(a["fingerprint"], c["fingerprint"])


class MarkupOptionsTest(unittest.TestCase):
    def write_doc(self, text):
        import tempfile
        f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        f.write(text)
        f.close()
        self.addCleanup(os.remove, f.name)
        return f.name

    FIRST = """<!-- test {"testId": "first"} -->
<!-- example document -->

| Example document | [Download link](https://example.test/a.pdf) |

<!-- example config -->
```json
{"fields": []}
```
<!-- example output -->
```json
{}
```
<!-- test end -->
"""

    def test_fragment_is_wrapped_and_document_is_reused(self):
        doc = self.FIRST + """
<!-- test {"testId": "second"} -->
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
<!-- test end -->
"""
        second = r.parse_examples(self.write_doc(doc))["second"]
        self.assertEqual(second["document_url"], "https://example.test/a.pdf")
        self.assertIn("/* a comment */", second["config"])
        self.assertTrue(second["config"].startswith('{\n  "fields": ['))
        config, _ = r.check_syntax("second", second)
        self.assertEqual(config["fields"][0]["method"]["id"], "queryGroup")

    def test_fragment_syntax_errors_point_at_the_doc_line(self):
        doc = """<!-- test {"testId": "t"} -->
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
<!-- test end -->
""" + self.FIRST
        example = r.parse_examples(self.write_doc(doc))["t"]
        with self.assertRaises(r.ExampleError) as caught:
            r.check_syntax("t", example)
        self.assertRegex(str(caught.exception), r"line [67]\)")

    def test_from_must_name_an_example_with_a_link(self):
        doc = """<!-- test {"testId": "t"} -->
<!-- example document {"from": "nope"} -->
<!-- example config -->
```json
{"fields": []}
```
<!-- example output -->
```json
{}
```
<!-- test end -->
"""
        with self.assertRaises(r.ExampleError) as caught:
            r.parse_examples(self.write_doc(doc))
        self.assertIn("names no example with its own document link", str(caught.exception))


class EnvelopeSchemaTest(unittest.TestCase):
    def test_committed_baselines_are_valid(self):
        import envelope, glob
        paths = glob.glob(os.path.join(r.ENVELOPES_DIR, "*.json"))
        self.assertTrue(paths)
        for path in paths:
            with open(path) as f:
                envelope.validate(json.load(f))

    def test_invalid_baseline_fails_loudly(self):
        import envelope, tempfile
        good = envelope.build([envelope.observe_output({"phone": {"type": "string", "value": "1"}}, ["phone"])], "C", "t")
        bad = dict(good, runs="ten")
        with self.assertRaises(envelope.EnvelopeInvalid):
            envelope.validate(bad)
        with tempfile.TemporaryDirectory() as d:
            saved, r.ENVELOPES_DIR = r.ENVELOPES_DIR, d
            try:
                with open(os.path.join(d, "t.json"), "w") as f:
                    json.dump(bad, f)
                with self.assertRaises(r.ExampleError) as caught:
                    r.check_envelope({}, "t", {"config": "C"}, {"phone": {"value": "1"}}, llm_judge.FieldIndex(CONFIG))
                self.assertEqual(caught.exception.category, "ENVELOPE_INVALID")
            finally:
                r.ENVELOPES_DIR = saved


class CollapseTest(unittest.TestCase):
    def test_only_tests_needing_attention_start_open(self):
        import html_report
        base = {"test_id": "t", "document_url": "https://example.test/a.pdf", "llm_fields": [], "status": "pass", "envelope": {"status": "within", "runs": 10, "built": "2026-10-01T00:00:00Z", "slots": {}}}
        self.assertFalse(html_report.needs_attention(base))
        self.assertTrue(html_report.needs_attention(dict(base, status="fail")))
        self.assertTrue(html_report.needs_attention(dict(base, envelope={"status": "outside", "runs": 10, "built": "x", "breaches": {}})))
        self.assertTrue(html_report.needs_attention(dict(base, llm_fields=[{"field": "p", "kind": "llm", "prompt": "", "judged": [{}]}])))
        self.assertIn('<details class="card test" id="t">', html_report.render_code_test(base))
        self.assertIn('<details class="card test" id="t" open>', html_report.render_code_test(dict(base, status="fail")))

    def test_says_when_the_judge_wasnt_called(self):
        import html_report
        record = {"test_id": "t", "document_url": "https://example.test/a.pdf", "status": "pass", "overall": "identical",
                  "llm_fields": [{"field": "p", "kind": "llm", "prompt": "", "type": "string", "judged": []}]}
        self.assertIn("The judge wasn&#x27;t called", html_report.render_code_test(record).replace("wasn\'t", "wasn&#x27;t"))


if __name__ == "__main__":
    unittest.main()
