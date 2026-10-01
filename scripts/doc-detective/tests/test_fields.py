import unittest

from codetests import fields, judge

from tests.fakes import CONFIG


class RoutingTest(unittest.TestCase):
    def setUp(self):
        self.index = fields.FieldIndex(CONFIG)

    def test_layout_field_stays_exact(self):
        self.assertEqual(self.index.owner(("policy_number", "value")), ("policy_number", "layout"))
        self.assertFalse(self.index.is_llm(("policy_number", "value")))

    def test_query_group_query_is_llm(self):
        self.assertEqual(self.index.owner(("phone", "value")), ("phone", "llm"))

    def test_list_property_belongs_to_the_list_field(self):
        self.assertEqual(self.index.owner(("vehicles", 0, "make"))[0], "vehicles")

    def test_llm_methods_nested_in_conditionals_and_sections(self):
        self.assertTrue(self.index.is_llm(("_deposits", 0, "amount")))
        self.assertEqual(self.index.owner(("drivers", 0, "driver_age", "value")), ("driver_age", "llm"))
        self.assertFalse(self.index.is_llm(("drivers", 0, "driver_name", "value")))

    def test_fallback_chain_with_an_llm_field_is_judged(self):
        self.assertEqual(self.index.owner(("total", "value")), ("total", "fallback"))
        self.assertTrue(self.index.is_llm(("total", "value")))

    def test_root_level_mismatch_stays_exact(self):
        self.assertFalse(self.index.is_llm(()))


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
        self.index = fields.FieldIndex(self.CONFIG)

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
        self.assertEqual(fields.format_type(declared), 'currency with options {"currencySymbol": "€"}')
        self.assertIn('"unit": "$"', judge.type_example(declared))

    def test_type_examples_come_from_types_md(self):
        examples = judge.CONFIG["type_examples"]
        self.assertEqual(examples["number"], '{ "source": "123456789", "value": 123456789, "type": "number" }')
        self.assertIn('"+18557863246"', examples["phoneNumber"])
        self.assertEqual(judge.type_example("table"), "none in the type reference")


if __name__ == "__main__":
    unittest.main()
