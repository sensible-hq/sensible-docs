import glob
import json
import os
import tempfile
import unittest
from unittest import mock

from codetests import envelope, settings


def phone(value, confidence="confident_answer"):
    return {"phone": {"type": "string", "value": value, "confidenceSignal": confidence}}


def baseline(outputs, keys=("phone",), config="CONFIG"):
    return envelope.build([envelope.observe_output(o, keys) for o in outputs], config, "t")


def check(base, output, keys=("phone",)):
    return envelope.check(base, envelope.observe_output(output, keys))


class MeasureTest(unittest.TestCase):
    def test_shape(self):
        self.assertEqual(envelope.shape("1800-123-4567"), "9999-999-9999")
        self.assertEqual(envelope.shape("Ab 12"), "aa 99")

    def test_within_the_envelope(self):
        base = baseline([phone("1800 123 4567"), phone("1800-123-4567")])
        self.assertEqual(base["slots"]["phone"]["shapes"], ["9999 999 9999", "9999-999-9999"])
        self.assertEqual(check(base, phone("1800-123-4567")), {})

    def test_new_format_null_and_confidence_breaches(self):
        base = baseline([phone("1800 123 4567")] * 3)
        self.assertIn("new format", check(base, phone("(1800) 123.4567"))["phone"][0])
        self.assertEqual(check(base, {"phone": {"type": "string", "value": None}})["phone"], ["null; never null in the baseline"])
        self.assertIn("confidence signal unsure", check(base, phone("1800 123 4567", "unsure"))["phone"][0])

    def test_numbers_units_types_and_source_formats(self):
        money = lambda v, unit="$", typ="currency": {"premium": {"source": str(v), "value": v, "unit": unit, "type": typ}}
        base = baseline([money(100), money(110)], ("premium",))
        self.assertEqual(check(base, money(105), ("premium",)), {})
        self.assertEqual(check(base, money(900), ("premium",))["premium"], ["value 900; baseline values ranged from 100 to 110"])
        single = baseline([money(100)], ("premium",))
        self.assertIn("value 50; baseline value was always 100", check(single, money(50), ("premium",))["premium"])
        self.assertIn("unit €; baseline only saw $", check(base, money(100, "€"), ("premium",))["premium"][0])
        self.assertIn("type number", check(base, money(100, typ="number"), ("premium",))["premium"][0])
        self.assertEqual(base["slots"]["premium"]["source_shapes"], ["999"])
        source = check(base, {"premium": {"source": "$100", "value": 100, "unit": "$", "type": "currency"}}, ("premium",))
        self.assertIn("new source format '$999'", source["premium"][0])

    def test_free_text_gets_a_length_check_only(self):
        text = lambda s: {"summary": {"type": "string", "value": s}}
        base = baseline([text("The policy covers two vehicles and one driver."), text("Covers two vehicles, one driver, and roadside help.")], ("summary",))
        self.assertEqual(base["slots"]["summary"]["shapes"], "free text")
        self.assertEqual(check(base, text("The policy covers two cars and a single driver."), ("summary",)), {})
        self.assertIn("length 5", check(base, text("short"), ("summary",))["summary"][0])

    def test_list_and_table_counts(self):
        rows = lambda n: {"vehicles": [{"make": {"type": "string", "value": "Honda"}}] * n}
        base = baseline([rows(2), rows(3)], ("vehicles",))
        self.assertIn("vehicles[*].make", base["slots"])
        self.assertEqual(check(base, rows(1), ("vehicles",))["vehicles#count"], ["1 item; baseline item counts ranged from 2 to 3"])
        table = {"t": {"columns": [{"id": "year", "values": [{"type": "number", "value": 2015}]}]}}
        self.assertIn("t.columns[year].values[*]", baseline([table], ("t",))["slots"])


class MergeTest(unittest.TestCase):
    def test_merge_combines_runs_formats_and_ranges(self):
        old = baseline([phone("1800 123 4567")] * 10)
        merged = envelope.merge(old, baseline([phone("1800-123-4567")] * 2 + [phone("1800 123 4567")] * 8))
        self.assertEqual((merged["runs"], merged["slots"]["phone"]["observations"]), (20, 20))
        self.assertEqual(merged["slots"]["phone"]["shapes"], ["9999 999 9999", "9999-999-9999"])
        self.assertEqual(merged["built"], old["built"])
        self.assertIn("updated", merged)
        self.assertEqual(check(merged, phone("1800-123-4567")), {})

    def test_null_rate_is_reweighted_and_counts_widen(self):
        x = lambda v: envelope.observe_output({"x": v}, ["x"])
        a = envelope.build([x(None)] + [x({"type": "string", "value": "a"})] * 3, "C", "t")
        b = envelope.build([x({"type": "string", "value": "a"})] * 4, "C", "t")
        self.assertEqual(envelope.merge(a, b)["slots"]["x"]["null_rate"], 0.125)
        rows = lambda n: envelope.observe_output({"v": [{"m": {"type": "string", "value": "A"}}] * n}, ["v"])
        merged = envelope.merge(envelope.build([rows(2)], "C", "t"), envelope.build([rows(5)], "C", "t"))
        self.assertEqual(merged["slots"]["v#count"], {"count_min": 2, "count_max": 5})

    def test_merge_refuses_different_configs(self):
        with self.assertRaises(envelope.EnvelopeInvalid):
            envelope.merge(baseline([phone("1")], config="C1"), baseline([phone("1")], config="C2"))


class FileTest(unittest.TestCase):
    def test_committed_baselines_are_valid(self):
        paths = glob.glob(os.path.join(settings.HERE, "envelopes", "*.json"))
        self.assertTrue(paths)
        for path in paths:
            with open(path, encoding="utf-8") as f:
                envelope.validate(json.load(f))

    def test_load_save_and_invalid_files(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.dict(os.environ, {settings.ENVELOPES_DIR_VAR: d}):
            self.assertIsNone(envelope.load("t"))
            envelope.save(baseline([phone("1")]))
            self.assertEqual(envelope.load("t")["runs"], 1)
            with open(envelope.path("t"), "w") as f:
                json.dump(dict(baseline([phone("1")]), runs="ten"), f)
            with self.assertRaises(envelope.EnvelopeInvalid):
                envelope.load("t")


if __name__ == "__main__":
    unittest.main()
