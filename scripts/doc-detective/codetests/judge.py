"""The LLM judge for LLM-produced values that differ from the docs.

LLM methods (Query Group, List, NLP Table) can return a correct answer that's worded or formatted
differently from the docs, for example "1800-123-4567" instead of "1800 123 4567". The judge
decides, per value, whether the actual value still supports what the docs show. Its model,
prompts, and output schema live in config/judge/; DOC_EXAMPLES_JUDGE_MODEL overrides the model.
"""

import json
import os
from string import Template

from . import fields, settings

JUDGE_DIR = os.path.join(settings.CONFIG_DIR, "judge")


def load_config():
    """config/judge/config.json plus the prompt, template, and schema files it names."""
    with open(os.path.join(JUDGE_DIR, "config.json"), encoding="utf-8") as f:
        config = json.load(f)

    def read(name):
        with open(os.path.join(JUDGE_DIR, config[name]), encoding="utf-8") as f:
            return f.read().strip()

    config["system_prompt"] = read("system_prompt_file")
    config["user_prompt"] = Template(read("user_prompt_file"))
    config["claim_template"] = Template(read("claim_template_file"))
    config["output_schema"] = json.loads(read("output_schema_file"))
    config["type_examples"] = fields.load_type_examples(os.path.join(settings.REPO_ROOT, config["types_reference"]))
    return config


CONFIG = load_config()
DEFAULT_MODEL = CONFIG["model"]


class JudgeError(Exception):
    """The judge couldn't decide. `exchange` holds what was sent, for the record."""

    def __init__(self, message, exchange):
        super().__init__(message)
        self.exchange = exchange


def model():
    return os.environ.get(settings.JUDGE_MODEL_VAR) or DEFAULT_MODEL


def type_example(declared):
    return CONFIG["type_examples"].get(fields.type_id(declared), "none in the type reference")


def build_user_prompt(claims):
    """Each claim: path, prompt, type, documented, actual, and the whole documented and actual field."""
    blocks = [
        CONFIG["claim_template"].substitute(
            path=c["path"],
            prompt=json.dumps(c["prompt"]),
            type=fields.format_type(c["type"]),
            type_example=type_example(c["type"]),
            documented=json.dumps(c["documented"], ensure_ascii=False),
            actual=json.dumps(c["actual"], ensure_ascii=False),
            documented_field=json.dumps(c["documented_field"], ensure_ascii=False),
            actual_field=json.dumps(c["actual_field"], ensure_ascii=False),
        )
        for c in claims
    ]
    return CONFIG["user_prompt"].substitute(claims="\n".join(blocks))


def judge(api_key, claims, model_id=None):
    """Judge claims. Returns {"model", "system_prompt", "user_prompt", "raw_output", "results"}, with
    results in the same order as claims. Raises JudgeError, with the exchange so far, if it can't decide."""
    import anthropic

    exchange = {"model": model_id or model(), "system_prompt": CONFIG["system_prompt"], "user_prompt": build_user_prompt(claims), "raw_output": ""}

    def fail(message):
        exchange["raw_output"] = exchange["raw_output"] or f"(no usable output: {message})"
        raise JudgeError(message, exchange)

    client = anthropic.Anthropic(api_key=api_key)
    try:
        response = client.messages.create(
            model=exchange["model"],
            max_tokens=CONFIG["max_tokens"],
            system=exchange["system_prompt"],
            messages=[{"role": "user", "content": exchange["user_prompt"]}],
            output_config={"format": {"type": "json_schema", "schema": CONFIG["output_schema"]}},
        )
    except anthropic.APIStatusError as e:
        fail(f"judge request to {exchange['model']} failed ({e.status_code}): {e.message}")
    except anthropic.APIConnectionError as e:
        fail(f"couldn't reach the judge: {e}")
    if response.stop_reason == "refusal":
        fail(f"{exchange['model']} declined to evaluate the claims")
    if response.stop_reason == "max_tokens":
        fail(f"{exchange['model']}'s response was cut off")
    exchange["model"] = response.model
    exchange["raw_output"] = next((b.text for b in response.content if b.type == "text"), "")
    try:
        results = {r["path"]: r for r in json.loads(exchange["raw_output"])["results"]}
    except (ValueError, KeyError, TypeError) as e:
        fail(f"the judge's output isn't the expected JSON ({e})")
    missing = [c["path"] for c in claims if c["path"] not in results]
    if missing:
        fail(f"the judge didn't return a verdict for {', '.join(missing)}")
    exchange["results"] = [results[c["path"]] for c in claims]
    return exchange


def classify(result):
    """"pass", "warn", or "fail" for one judge result."""
    if result["match"] == "fail":
        return "fail"
    if result["match"] == "pass" and result["confidence"] >= CONFIG["min_pass_confidence"]:
        return "pass"
    return "warn"
