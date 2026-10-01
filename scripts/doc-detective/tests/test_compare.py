import unittest

from codetests import compare, jsonish

ACTUAL = {"id": "abc-123", "created": "2026-10-01T10:00:00Z", "status": "COMPLETE",
          "rows": [{"n": 1}, {"n": 2}, {"n": 3}, {"n": 4}], "flag": True, "count": 1, "extra": True}


class CompareTest(unittest.TestCase):
    def diffs(self, documented):
        return compare.diffs(jsonish.parse_block(documented, trailing_commas=False), ACTUAL)

    def test_matches(self):
        for documented in [
            '{"status": "COMPLETE"}',                        # keys the docs leave out are ignored
            '{"created": "...", "status": "COMPLETE"}',      # "..." value
            '{"created": ..., "status": "COMPLETE"}',        # bare ... value
            '{"status": "COMPLETE",\n  ...\n}',              # bare ... member
            '{\n  ...,\n  "status": "COMPLETE"}',            # leading bare ... member
            '{"rows": [{"n": 1}, {"n": 2}, ...]}',           # array prefix
            '{"rows": [{"n": 1}, ..., {"n": 4}]}',           # array first ... last
            '{"rows": [{"n": 1}, /* more rows */ ...]}',     # ... with a comment
            '{"id": "…"}',                                   # unicode ellipsis
            '{"count": 1.0}',                                # 1 and 1.0 are the same number
        ]:
            with self.subTest(documented):
                self.assertEqual(self.diffs(documented), [])

    def test_mismatches(self):
        for documented in [
            '{"status": "FAILED"}',
            '{"rows": [{"n": 9}, ...]}',
            '{"rows": [{"n": 1}, ..., {"n": 9}]}',
            '{"rows": [{"n": 1}, {"n": 2}, {"n": 3}]}',      # a full array must match in length
            '{"rows": [{"n":1},{"n":2},{"n":3},{"n":4},{"n":5}, ...]}',
            '{"nope": 1}',
            '{"status": "COMPLETE..."}',                     # ... inside a longer string is data
            '{"flag": 1}',                                   # true isn't 1
            '{"count": true}',
        ]:
            with self.subTest(documented):
                self.assertTrue(self.diffs(documented))

    def test_tail_diff_path_points_at_the_docs_index(self):
        (diff,) = self.diffs('{"rows": [{"n": 1}, ..., {"n": 9}]}')
        self.assertEqual(compare.describe(diff), "$.rows[2].n: expected 9, got 4")

    def test_missing_keys_and_fixes(self):
        expected = {"a": {"value": "x", "source": "$1"}, "b": 1}
        found = compare.diffs(expected, {"a": {"value": "y", "source": "$1"}})
        self.assertEqual([compare.describe(d) for d in found], ['$.a.value: expected "x", got "y"', "$.b: missing from actual output"])
        self.assertEqual(compare.apply_fixes(expected, found), {"a": {"value": "y", "source": "$1"}})
        self.assertEqual(expected["b"], 1)

    def test_coverage_notes(self):
        notes = compare.coverage(jsonish.parse_block('{"rows": [{"n": 1}, ...], "id": "..."}'), ACTUAL)
        self.assertEqual(notes["abbreviated"], [(("rows",), 1, 4)])
        self.assertEqual(notes["skipped"], [("id",)])
        self.assertEqual(sorted(notes["extra_top_level"]), ["count", "created", "extra", "flag", "status"])

    def test_typed_field_path(self):
        expected = {"premium": {"source": "$100", "value": 100, "type": "currency"}}
        self.assertEqual(compare.typed_field_path(expected, ("premium", "source")), ("premium",))
        self.assertEqual(compare.typed_field_path({"x": 1}, ("x",)), ("x",))


if __name__ == "__main__":
    unittest.main()
