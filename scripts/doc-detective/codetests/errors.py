"""Failure categories, so a report can tell docs bugs from product drift."""

# The docs: markup or code block syntax
DOCS_MALFORMED = "DOCS_MALFORMED"
# The example document's link doesn't resolve
DOCUMENT_UNREACHABLE = "DOCUMENT_UNREACHABLE"
# Sensible rejected the config
CONFIG_INVALID = "CONFIG_INVALID"
# The extraction didn't complete
EXTRACTION_ERROR = "EXTRACTION_ERROR"
# A layout (exact) value in the documented output doesn't match
OUTPUT_DRIFT = "OUTPUT_DRIFT"
# The judge failed an LLM value
LLM_DRIFT = "LLM_DRIFT"
# LLM values differ but there's no judge key
JUDGE_UNAVAILABLE = "JUDGE_UNAVAILABLE"
# The judge was called but couldn't decide (fail closed)
JUDGE_ERROR = "JUDGE_ERROR"
# A saved baseline doesn't match envelope.schema.json, or can't be extended
ENVELOPE_INVALID = "ENVELOPE_INVALID"


class CodeTestError(Exception):
    def __init__(self, category, message):
        super().__init__(f"{category}: {message}")
        self.category = category
