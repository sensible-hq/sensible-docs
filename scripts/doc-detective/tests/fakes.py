"""Stand-ins for the Sensible API and the judge, and helpers to build code tests and pages."""

import json
import os
import tempfile

from codetests import judge as judge_module
from codetests.markup import CodeTest

# A config with LLM fields at every depth the runner has to find
CONFIG = {
    "fields": [
        {"id": "policy_number", "anchor": "policy number", "method": {"id": "box"}},
        {"method": {"id": "queryGroup", "queries": [{"id": "phone", "description": "customer service phone"}]}},
        {"id": "vehicles", "method": {"id": "list", "description": "insured vehicles", "properties": []}},
        {"method": {"id": "conditional", "condition": {"exists": {"var": "phone"}},
                    "fieldsOnPass": [{"id": "_deposits", "method": {"id": "list", "description": "deposits"}}]}},
        {"id": "drivers", "method": {"id": "sections"}, "fields": [
            {"id": "driver_name", "anchor": "name", "method": {"id": "label"}},
            {"method": {"id": "queryGroup", "queries": [{"id": "driver_age", "description": "driver's age"}]}},
        ]},
        # Fallback chain: a Row field, then a Query Group with the same ID
        {"id": "total", "anchor": "total", "method": {"id": "row"}},
        {"method": {"id": "queryGroup", "queries": [{"id": "total", "description": "total amount"}]}},
    ]
}


class FakeClient:
    """Returns `parsed` for every extraction; records what was uploaded."""

    def __init__(self, parsed, status=200):
        self.parsed, self.status, self.uploads, self.deleted, self.extractions = parsed, status, [], [], 0

    def document_status(self, url):
        return self.status

    def upload_config(self, name, text):
        self.uploads.append(name)

    def extract(self, url, config_name, document_name):
        self.extractions += 1
        return self.parsed

    def delete_config(self, name):
        self.deleted.append(name)

    def delete_doc_type(self):
        return True


class FakeJudge:
    """Answers every claim with the same match; records the claims it was sent."""

    def __init__(self, match="pass", confidence=0.9):
        self.match, self.confidence, self.claims = match, confidence, []

    def __call__(self, key, claims, model=None):
        self.claims += claims
        results = [{"path": c["path"], "claim": "c", "observed": "o", "match": self.match, "confidence": self.confidence, "reasoning": "stub"} for c in claims]
        return {"model": "test-judge", "system_prompt": "SYSTEM", "user_prompt": judge_module.build_user_prompt(claims),
                "raw_output": json.dumps({"results": results}), "results": results}


def broken_judge(key, claims, model=None):
    exchange = {"model": "test-judge", "system_prompt": "SYSTEM", "user_prompt": judge_module.build_user_prompt(claims), "raw_output": "(no usable output)"}
    raise judge_module.JudgeError("judge request to test-judge failed (529): overloaded", exchange)


def code_test(documented, config=CONFIG, test_id="test", file="test.md"):
    output = json.dumps(documented, indent=2)
    return CodeTest(test_id=test_id, description="a test", file=file, line=1, config=json.dumps(config),
                    output=output, document_url="https://example.test/doc.pdf")


def write_page(case, text):
    f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
    f.write(text)
    f.close()
    case.addCleanup(os.remove, f.name)
    return f.name


CODE_TEST_PAGE = """<!-- code test {"testId": "first", "description": "first test"} -->
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
<!-- code test end -->
"""
