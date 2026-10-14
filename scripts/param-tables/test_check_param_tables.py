"""Offline tests for check_param_tables.py, with a small hand-made schema. No network.

Run: python3 -m unittest discover -s scripts/param-tables
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_param_tables as c

SCHEMA = c.Schema({"definitions": {
    "Direction": {"anyOf": [{"type": "string", "const": "right"}, {"type": "string", "const": "left"}]},
    "Row": {"type": "object", "required": ["id"], "additionalProperties": False, "properties": {
        "id": {"type": "string", "const": "row"},
        "position": {"$ref": "#/definitions/Direction"},
        "includeAnchor": {"type": "boolean"},
        "tolerance": {"type": "number"},
        "tiebreaker": {"type": "string"},
    }},
    # Two variants of one method: a parameter is required only if both require it
    "GroupA": {"type": "object", "required": ["id", "queries"], "properties": {
        "id": {"const": "group"}, "queries": {"type": "array"}, "chunkSize": {"type": "number"}}},
    "GroupB": {"type": "object", "required": ["id", "queries", "source_ids"], "properties": {
        "id": {"const": "group"}, "queries": {"type": "array"}, "source_ids": {"type": "array"}}},
    # A method defined inline, behind a URL-encoded $ref
    "Wrapper%3CX%3E": {"anyOf": [{"type": "object", "required": ["id"], "properties": {
        "id": {"const": "inlineMethod"}, "fields": {"type": "array"}}}]},
    "Holder": {"$ref": "#/definitions/Wrapper%3CX%3E"},
    # Types and methods share ids: `paragraph` is both
    "ParagraphConfig": {"type": "object", "properties": {"id": {"const": "paragraph"}}},
    "ParagraphEduction": {"type": "object", "properties": {"id": {"const": "paragraph"}, "allNewlines": {"type": "boolean"}}},
}})

ROW_TABLE = """
| key               | value                              | description |
| ----------------- | ---------------------------------- | ----------- |
| id (**required**) | `row`                              |             |
| includeAnchor     | boolean. default: `false`          | x           |
| position          | `right`, `left`. default: `right`  | x           |
| tolerance         | number in inches. default: 0.08    | x           |
| tiebreaker        | For information about this global parameter, see [Method](doc:method#parameters). | x |
"""


def check(text, filename="page.md", globals_=frozenset({"tiebreaker"})):
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, filename)
        with open(path, "w") as f:
            f.write(text)
        results = c.check_page(path, SCHEMA, set(globals_))
    errors = [e for r in results or [] for e in r["errors"]]
    warnings = [w for r in results or [] for w in r["warnings"]]
    return results, errors, warnings


class CorrectTable(unittest.TestCase):
    def test_correct_table_passes(self):
        results, errors, warnings = check(ROW_TABLE)
        self.assertEqual(len(results), 1)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_page_without_parameter_table_is_skipped(self):
        self.assertIsNone(check("# Just prose\n")[0])


class WrongClaimsFail(unittest.TestCase):
    def test_misspelled_parameter(self):
        _, errors, warnings = check(ROW_TABLE.replace("| includeAnchor ", "| includeAnchr  "))
        self.assertTrue(any("`includeAnchr` isn't a parameter" in e for e in errors))
        self.assertTrue(any("includeAnchor" in w for w in warnings))

    def test_disallowed_value(self):
        _, errors, _ = check(ROW_TABLE.replace("`right`, `left`.", "`right`, `up`."))
        self.assertTrue(any('lists "up"' in e for e in errors))

    def test_wrong_required_flag(self):
        _, errors, _ = check(ROW_TABLE.replace("| includeAnchor ", "| includeAnchor (**required**) "))
        self.assertTrue(any("documented as required, the schema says optional" in e for e in errors))

    def test_wrong_type(self):
        _, errors, _ = check(ROW_TABLE.replace("boolean. default", "number. default"))
        self.assertTrue(any("documented as number, the schema says boolean" in e for e in errors))

    def test_disallowed_default(self):
        _, errors, _ = check(ROW_TABLE.replace("default: `right`", "default: `center`"))
        self.assertTrue(any('default "center" isn\'t an allowed value' in e for e in errors))

    def test_default_of_wrong_type(self):
        _, errors, _ = check(ROW_TABLE.replace("default: 0.08", "default: `wide`"))
        self.assertTrue(any('default "wide" is a string' in e for e in errors))


class GapsWarn(unittest.TestCase):
    def test_missing_row_warns(self):
        text = "\n".join(l for l in ROW_TABLE.splitlines() if not l.startswith("| tolerance"))
        _, errors, warnings = check(text)
        self.assertEqual(errors, [])
        self.assertTrue(any("tolerance" in w for w in warnings))

    def test_unlisted_value_warns(self):
        _, errors, warnings = check(ROW_TABLE.replace("`right`, `left`.", "`right`."))
        self.assertEqual(errors, [])
        self.assertTrue(any('also allows "left"' in w for w in warnings))

    def test_global_parameters_are_not_gaps(self):
        text = "\n".join(l for l in ROW_TABLE.splitlines() if not l.startswith("| tiebreaker"))
        self.assertEqual(check(text)[2], [])


class SchemaShapes(unittest.TestCase):
    def test_variants_merge_properties_and_intersect_required(self):
        labels, props, required = SCHEMA.variants_for("group")
        self.assertEqual(set(props), {"id", "queries", "chunkSize", "source_ids"})
        self.assertEqual(required, {"id", "queries"})

    def test_inline_definition_behind_encoded_ref(self):
        labels, props, _ = SCHEMA.variants_for("inlineMethod")
        self.assertIn("fields", props)

    def test_types_page_prefers_type_definitions(self):
        self.assertIn("allNewlines", SCHEMA.variants_for("paragraph", prefer_types=True)[1])
        self.assertNotIn("allNewlines", SCHEMA.variants_for("paragraph")[1])

    def test_each_table_uses_its_own_id(self):
        two = ROW_TABLE + "\n" + ROW_TABLE.replace("`row`", "`paragraph`").replace("| includeAnchor ", "| allNewlines   ")
        results, _, _ = check(two, filename="types.md")
        self.assertEqual([r["method"] for r in results], ["row", "paragraph"])


class Parsing(unittest.TestCase):
    def rows(self, value):
        text = f"| key | value | description |\n| --- | --- | --- |\n| p | {value} | x |\n"
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "p.md")
            with open(path, "w") as f:
                f.write(text)
            return list(c.parse_tables(path))[0]

    def test_backticked_literal_is_not_a_type_word(self):
        self.assertEqual(self.rows("`number`")["types"], set())

    def test_prose_default_is_ignored(self):
        self.assertIsNone(self.rows("`allCaps`, `firstLetter`. Default: no change to source capitalization")["default"])
        self.assertIsNone(self.rows("object. default: none")["default"])

    def test_values_and_default(self):
        row = self.rows("`right`, `left`. default: `right`")
        self.assertEqual((row["values"], row["default"]), (["right", "left"], "right"))


if __name__ == "__main__":
    unittest.main()
