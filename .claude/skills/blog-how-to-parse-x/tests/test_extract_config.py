"""Tests for extract_config_from_draft.py"""

import pytest
from pathlib import Path
from extract_config_from_draft import extract_config

FIXTURES = Path(__file__).parent / "fixtures"


def test_extracts_config_from_valid_draft(tmp_path):
    output = tmp_path / "out.json"
    extract_config(FIXTURES / "sample_draft.md", output)
    result = output.read_text()
    assert "fingerprint" in result
    assert "departure" in result
    # Should not include the surrounding fence markers
    assert "```" not in result
    assert "CONFIG:START" not in result
    assert "CONFIG:END" not in result


def test_extracted_content_matches_expected(tmp_path):
    output = tmp_path / "out.json"
    extract_config(FIXTURES / "sample_draft.md", output)
    result = output.read_text()
    # The fixture config block starts with the json5 header comment
    assert result.startswith("/* Sensible uses JSON5 to support in-line comments*/")


def test_missing_markers_exits(tmp_path):
    draft = tmp_path / "no_markers.md"
    draft.write_text("# A draft with no CONFIG markers\n\n```json5\n{}\n```\n")
    output = tmp_path / "out.json"
    with pytest.raises(SystemExit):
        extract_config(draft, output)


def test_output_file_is_created(tmp_path):
    output = tmp_path / "subdir" / "out.json"
    output.parent.mkdir()
    extract_config(FIXTURES / "sample_draft.md", output)
    assert output.exists()


def test_only_config_block_extracted_not_other_json5(tmp_path):
    """The individual field sections also have json5 blocks — only the CONFIG block is extracted."""
    output = tmp_path / "out.json"
    extract_config(FIXTURES / "sample_draft.md", output)
    result = output.read_text()
    # The combined block has both fingerprint and fields — verify it's not just the individual block
    assert '"fingerprint"' in result
    assert '"fields"' in result
