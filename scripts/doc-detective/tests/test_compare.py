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

    def test_abridgement_mark_matches(self):
        for documented in [
            '{"created": "[...]", "status": "COMPLETE"}',     # whole value
            '{"status": "COMPLETE",\n  [...]\n}',            # object member
            '{\n  [...],\n  "status": "COMPLETE"}',          # leading object member
            '{"rows": [{"n": 1}, {"n": 2}, [...]]}',          # array prefix
            '{"rows": [{"n": 1}, [...], {"n": 4}]}',          # array first [...] last
            '{"rows": [[...]]}',                              # any array
            '{"rows": [...]}',                                # after a colon: an array, items not checked
            '{"id": "abc-[...]"}',                            # start of a string
            '{"id": "[...]-123"}',                            # end of a string
            '{"created": "2026-[...]T10:[...]Z"}',            # several gaps
            '{"id": "abc-[...]123"}',                         # a gap can be empty
            '{"rows": [{"n": 1}, [...]], "id": "abc[...]"}',  # mixed
        ]:
            with self.subTest(documented):
                self.assertEqual(self.diffs(documented), [])

    def test_abridgement_mark_mismatches(self):
        for documented in [
            '{"id": "xyz-[...]"}',                            # wrong start
            '{"id": "[...]-999"}',                            # wrong end
            '{"id": "abc-[...]-123-[...]x"}',                 # shown parts out of place
            '{"count": "1[...]"}',                            # abridged text against a number
            '{"rows": [{"n": 9}, [...]]}',                    # shown item still checked
            '{"rows": [...], "status": "FAILED"}',            # other keys still checked
            '{"status": [...]}',                              # after a colon, [...] still means an array
            '{"status": "COMPLETE..."}',                      # plain ... inside a string is literal
        ]:
            with self.subTest(documented):
                self.assertTrue(self.diffs(documented))

    def test_dot_leaders_are_literal(self):
        dots = {"leader": "Total ........ 3"}
        self.assertEqual(compare.diffs(jsonish.parse_block('{"leader": "Total ........ 3"}'), dots), [])
        self.assertTrue(compare.diffs(jsonish.parse_block('{"leader": "Total ... 3"}'), dots))

    def test_abridged_string_diff_and_coverage(self):
        (diff,) = self.diffs('{"id": "xyz-[...]"}')
        self.assertEqual(compare.describe(diff), '$.id: expected "xyz-[...]", got "abc-123"')
        notes = compare.coverage(jsonish.parse_block('{"id": "abc-[...]", "rows": [{"n": 1}, [...]], "created": "[...]"}'), ACTUAL)
        self.assertEqual(notes["abridged_strings"], [("id",)])
        self.assertEqual(notes["abbreviated"], [(("rows",), 1, 4)])
        self.assertEqual(notes["skipped"], [("created",)])

    def test_mark_inside_a_string_isnt_structural(self):
        self.assertEqual(jsonish.parse_block('{"a": "x [...] y", "b": ["[...]"]}'), {"a": "x [...] y", "b": ["[...]"]})
        self.assertEqual(jsonish.parse_block('{"a": [1, [...]], "b": [...]}'), {"a": [1, jsonish.ELLIPSIS], "b": [jsonish.ELLIPSIS]})

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
