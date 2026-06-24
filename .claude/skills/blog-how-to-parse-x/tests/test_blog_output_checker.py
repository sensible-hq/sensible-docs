"""Tests for test_blog_output.py — extract_output_block and diff_outputs."""

import json
import pytest
from pathlib import Path

from test_blog_output import extract_output_block, diff_outputs

FIXTURES = Path(__file__).parent / "fixtures"


class TestExtractOutputBlock:
    def test_extracts_output_from_fixture(self):
        result = extract_output_block(FIXTURES / "sample_draft.md")
        assert "departure" in result
        assert result["departure"]["type"] == "date"
        assert result["departure"]["value"] == "2023-03-14T00:00:00.000Z"

    def test_does_not_confuse_json5_block_with_output(self):
        # The json5 config block must NOT be returned — only the plain json block
        result = extract_output_block(FIXTURES / "sample_draft.md")
        assert "fingerprint" not in result
        assert "fields" not in result

    def test_missing_section_exits(self, tmp_path):
        draft = tmp_path / "no_section.md"
        draft.write_text("# A draft\n\nNo putting it all together here.\n")
        with pytest.raises(SystemExit):
            extract_output_block(draft)

    def test_missing_config_end_marker_exits(self, tmp_path):
        draft = tmp_path / "no_marker.md"
        draft.write_text(
            "## Putting it all together\n\n"
            "<!-- CONFIG:START -->\n```json5\n{}\n```\n\n"
            "```json\n{\"foo\": 1}\n```\n"
        )
        with pytest.raises(SystemExit):
            extract_output_block(draft)

    def test_missing_output_block_exits(self, tmp_path):
        draft = tmp_path / "no_output.md"
        draft.write_text(
            "## Putting it all together\n\n"
            "<!-- CONFIG:START -->\n```json5\n{}\n```\n<!-- CONFIG:END -->\n\n"
            "No output block here.\n"
        )
        with pytest.raises(SystemExit):
            extract_output_block(draft)

    def test_invalid_json_in_output_block_exits(self, tmp_path):
        draft = tmp_path / "bad_json.md"
        draft.write_text(
            "## Putting it all together\n\n"
            "<!-- CONFIG:START -->\n```json5\n{}\n```\n<!-- CONFIG:END -->\n\n"
            "```json\n{ not valid json }\n```\n"
        )
        with pytest.raises(SystemExit):
            extract_output_block(draft)


class TestDiffOutputs:
    def test_identical_dicts_produce_no_mismatches(self):
        doc = {"vessel": {"type": "string", "value": "MSC AURORA"}}
        assert diff_outputs(doc, doc) == []

    def test_detects_value_mismatch(self):
        expected = {"vessel": {"type": "string", "value": "MSC AURORA"}}
        actual = {"vessel": {"type": "string", "value": "MSC TITAN"}}
        mismatches = diff_outputs(expected, actual)
        assert len(mismatches) == 1
        assert "vessel.value" in mismatches[0]
        assert "MSC AURORA" in mismatches[0]
        assert "MSC TITAN" in mismatches[0]

    def test_detects_missing_field_in_api(self):
        expected = {"vessel": {"type": "string", "value": "X"}, "departure": None}
        actual = {"vessel": {"type": "string", "value": "X"}}
        mismatches = diff_outputs(expected, actual)
        assert any("MISSING" in m and "departure" in m for m in mismatches)

    def test_detects_extra_field_in_api(self):
        expected = {"vessel": {"type": "string", "value": "X"}}
        actual = {"vessel": {"type": "string", "value": "X"}, "surprise": "bonus"}
        mismatches = diff_outputs(expected, actual)
        assert any("EXTRA" in m and "surprise" in m for m in mismatches)

    def test_handles_list_fields(self):
        expected = {"goods": [{"marks": {"type": "string", "value": "N/M"}}]}
        actual = {"goods": [{"marks": {"type": "string", "value": "N/M"}}]}
        assert diff_outputs(expected, actual) == []

    def test_detects_list_length_mismatch(self):
        expected = {"goods": [{"marks": {"type": "string", "value": "A"}}, {"marks": {"type": "string", "value": "B"}}]}
        actual = {"goods": [{"marks": {"type": "string", "value": "A"}}]}
        mismatches = diff_outputs(expected, actual)
        assert any("LENGTH" in m for m in mismatches)

    def test_detects_value_mismatch_inside_list(self):
        expected = {"goods": [{"weight": {"type": "weight", "value": 100, "unit": "kilograms"}}]}
        actual = {"goods": [{"weight": {"type": "weight", "value": 200, "unit": "kilograms"}}]}
        mismatches = diff_outputs(expected, actual)
        assert any("goods[0].weight.value" in m for m in mismatches)

    def test_detects_type_mismatch(self):
        mismatches = diff_outputs({"x": [1, 2]}, {"x": {"a": 1}})
        assert any("TYPE MISMATCH" in m for m in mismatches)

    def test_nested_match_is_clean(self):
        doc = {
            "departure": {"source": "Mar 14 2023", "value": "2023-03-14T00:00:00.000Z", "type": "date"},
            "goods": [{"marks": {"type": "string", "value": "N/M"}}],
        }
        assert diff_outputs(doc, doc) == []
