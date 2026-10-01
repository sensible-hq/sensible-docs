"""LLM-as-judge for documented output of LLM-based SenseML methods.

LLM methods (Query Group, List, NLP Table) can return a correct answer that's worded or
formatted differently from the docs, for example "1800-123-4567" instead of "1800 123 4567".
The runner sends only the mismatches that an LLM method produced to a judge model, which
decides per field whether the actual value still supports what the docs show.

Judge model: DOC_EXAMPLES_JUDGE_MODEL, or DEFAULT_JUDGE_MODEL.
"""

import json
import os

import anthropic

DEFAULT_JUDGE_MODEL = "claude-sonnet-5-5"
# A pass below this confidence is reported as a warning instead
MIN_PASS_CONFIDENCE = 0.7
LLM_METHODS = {"queryGroup", "list", "nlpTable"}

SYSTEM_PROMPT = """You are a documentation accuracy evaluator. You will receive output that documentation \
shows for fields extracted from a document by an LLM, and the actual output from extracting the same \
document with the same configuration today.

For each claim, decide whether the actual value supports what the documentation shows, as a reader \
would understand it:
- pass: the same answer. Differences in formatting, punctuation, whitespace, or equivalent wording \
don't matter, for example "1800 123 4567" and "1800-123-4567".
- fail: a different answer. A different number, date, name, or meaning, or a value that's missing or null.
- partial: overlapping but not the same, for example the actual value includes only part of the \
documented answer, or adds substantive information the documentation doesn't show.

Evaluate only what is documented. Don't assess undocumented fields or behavior."""

VERDICT_SCHEMA = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "claim": {"type": "string"},
                    "observed": {"type": "string"},
                    "match": {"type": "string", "enum": ["pass", "fail", "partial"]},
                    "confidence": {"type": "number"},
                    "reasoning": {"type": "string"},
                },
                "required": ["path", "claim", "observed", "match", "confidence", "reasoning"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["results"],
    "additionalProperties": False,
}


class JudgeError(Exception):
    pass


class FieldIndex:
    """Which output keys LLM methods produce, wherever they sit in the config.

    Walks the whole config, so LLM methods nested in sections, conditionals, or any other
    container count. An LLM method contributes its field ID (List, NLP Table) or its query IDs
    (Query Group); any other method contributes its field ID as a non-LLM field.
    """

    def __init__(self, config):
        self.llm = {}  # output key -> extraction prompt
        self.other = set()
        self._walk(config)

    def _walk(self, node):
        if isinstance(node, list):
            for item in node:
                self._walk(item)
            return
        if not isinstance(node, dict):
            return
        method = node.get("method")
        if isinstance(method, dict) and "id" in method:
            if method["id"] in LLM_METHODS:
                if method["id"] == "queryGroup":
                    for query in method.get("queries", []):
                        self.llm[query["id"]] = query.get("description", "")
                elif "id" in node:
                    self.llm[node["id"]] = method.get("description", "")
            elif "id" in node:
                self.other.add(node["id"])
        for value in node.values():
            self._walk(value)

    def route(self, path):
        """Return (output key, prompt, mixed) if an LLM method produced the value at `path`, else None.

        Decided by the innermost path segment that's a known field ID, so a layout field inside a
        section stays exact while an LLM field inside it is judged. `mixed` is true when a non-LLM
        field shares the ID (a fallback chain): the output doesn't say which one produced the value,
        so it's judged.
        """
        for segment in reversed(path):
            if isinstance(segment, str) and (segment in self.llm or segment in self.other):
                if segment in self.llm:
                    return segment, self.llm[segment], segment in self.other
                return None
        return None


def judge_model():
    return os.environ.get("DOC_EXAMPLES_JUDGE_MODEL") or DEFAULT_JUDGE_MODEL


def judge(api_key, claims, model=None):
    """Judge claims, each {"path", "prompt", "documented", "observed"}. Returns (model, results)."""
    model = model or judge_model()
    lines = []
    for c in claims:
        lines.append(
            f"- path: {c['path']}\n"
            f"  extraction prompt: {json.dumps(c['prompt'])}\n"
            f"  documented: {json.dumps(c['documented'], ensure_ascii=False)}\n"
            f"  actual: {json.dumps(c['observed'], ensure_ascii=False)}"
        )
    user = (
        "Claims to evaluate (one result per path, using the path exactly as given):\n\n"
        + "\n".join(lines)
        + "\n\nFor each claim, return claim (the documented assertion), observed (what the actual output "
        "shows), match, confidence from 0.0 to 1.0, and reasoning."
    )
    client = anthropic.Anthropic(api_key=api_key)
    try:
        response = client.messages.create(
            model=model,
            max_tokens=16000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user}],
            output_config={"format": {"type": "json_schema", "schema": VERDICT_SCHEMA}},
        )
    except anthropic.APIStatusError as e:
        raise JudgeError(f"judge request to {model} failed ({e.status_code}): {e.message}")
    except anthropic.APIConnectionError as e:
        raise JudgeError(f"couldn't reach the judge: {e}")
    if response.stop_reason == "refusal":
        raise JudgeError(f"{model} declined to evaluate the claims")
    if response.stop_reason == "max_tokens":
        raise JudgeError(f"{model}'s response was cut off")
    text = next(b.text for b in response.content if b.type == "text")
    results = {r["path"]: r for r in json.loads(text)["results"]}
    missing = [c["path"] for c in claims if c["path"] not in results]
    if missing:
        raise JudgeError(f"the judge didn't return a verdict for {', '.join(missing)}")
    return response.model, [results[c["path"]] for c in claims]


def classify(result):
    """Return "pass", "warn", or "fail" for one judge result."""
    if result["match"] == "fail":
        return "fail"
    if result["match"] == "pass" and result["confidence"] >= MIN_PASS_CONFIDENCE:
        return "pass"
    return "warn"
