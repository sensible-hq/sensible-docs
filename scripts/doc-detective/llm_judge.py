"""LLM-as-judge for documented output of LLM-based SenseML methods.

LLM methods (Query Group, List, NLP Table) can return a correct answer that's worded or
formatted differently from the docs, for example "1800-123-4567" instead of "1800 123 4567".
The runner sends only the mismatches that an LLM method produced to a judge model, which
decides per field whether the actual value still supports what the docs show.

The judge's model, prompts, and output schema live in judge/ (see judge/config.json).
DOC_EXAMPLES_JUDGE_MODEL overrides the model.
"""

import json
import os
import re
from string import Template

import anthropic

JUDGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "judge")
LLM_METHODS = {"queryGroup", "list", "nlpTable"}


def load_config():
    """Load judge/config.json and the prompt, template, and schema files it names."""
    with open(os.path.join(JUDGE_DIR, "config.json"), encoding="utf-8") as f:
        config = json.load(f)

    def read(name):
        with open(os.path.join(JUDGE_DIR, config[name]), encoding="utf-8") as f:
            return f.read().strip()

    config["system_prompt"] = read("system_prompt_file")
    config["user_prompt"] = Template(read("user_prompt_file"))
    config["claim_template"] = Template(read("claim_template_file"))
    config["output_schema"] = json.loads(read("output_schema_file"))
    config["type_examples"] = load_type_examples(os.path.join(JUDGE_DIR, config["types_reference_file"]))
    return config


TYPE_NAMES = [
    "Address", "Boolean", "Currency", "Date", "Distance", "Images", "Name", "Number", "Paragraph", "Percentage",
    "Phone Number", "String", "Table", "Weight", "Compose", "Custom", "Replace", "Any", "Accounting Currency",
]


def load_type_examples(path):
    """Map each type ID to its output example in the docs' types reference (types.md).

    A type's section starts at its heading ("# Currency", "## Date"); its output example is the
    section's first code block with a "value" key that isn't a config ("fields").
    """
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        text = f.read()
    heads = [(m.start(), m.group(1).strip()) for m in re.finditer(r"^#{1,2} +(.+)$", text, re.M)]
    examples = {}
    for i, (start, name) in enumerate(heads):
        if name not in TYPE_NAMES:
            continue
        end = next((pos for pos, n in heads[i + 1:] if n in TYPE_NAMES), len(text))
        for block in re.finditer(r"```[a-z]*\n(.*?)```", text[start:end], re.S):
            if '"value"' in block.group(1) and '"fields"' not in block.group(1):
                words = name.split()
                type_id = words[0].lower() + "".join(w.capitalize() for w in words[1:])
                examples[type_id] = re.sub(r"\s+", " ", block.group(1)).strip()
                break
    return examples


CONFIG = load_config()
DEFAULT_JUDGE_MODEL = CONFIG["model"]


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
        self.types = {}  # output key -> {"type": declared type, "sub": {property or column ID: type}}
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
                        self.types[query["id"]] = {"type": query.get("type", "string"), "sub": {}}
                elif "id" in node:
                    self.llm[node["id"]] = method.get("description", "")
                    items = method.get("properties") or method.get("columns") or []
                    self.types[node["id"]] = {
                        "type": node.get("type"),
                        "sub": {item["id"]: item.get("type", "string") for item in items if isinstance(item, dict) and "id" in item},
                    }
            elif "id" in node:
                self.other.add(node["id"])
        for value in node.values():
            self._walk(value)

    def owner(self, path):
        """Return (field ID, kind) for the innermost known field ID on `path`, else (None, None).

        kind is "llm", "layout", or "fallback" (an LLM field and a non-LLM field share the ID).
        """
        for segment in reversed(path):
            if isinstance(segment, str) and (segment in self.llm or segment in self.other):
                if segment in self.llm:
                    return segment, "fallback" if segment in self.other else "llm"
                return segment, "layout"
        return None, None

    def type_for(self, path, expected):
        """Return the declared type for the value at `path` in the documented output `expected`.

        The innermost List property or NLP Table column on the path wins, then the query's or
        field's own type. NLP Table output names columns by value ("columns": [{"id": ...}]), so
        column IDs are read from `expected`. Undeclared types are "string", Sensible's default.
        """
        key, _ = self.owner(path)
        info = self.types.get(key, {"type": None, "sub": {}})
        found = None
        node = expected
        previous = None
        for segment in path:
            if isinstance(segment, str) and segment in info["sub"]:
                found = info["sub"][segment]
            if previous == "columns" and isinstance(segment, int) and isinstance(node, list) and segment < len(node):
                column = node[segment]
                if isinstance(column, dict) and column.get("id") in info["sub"]:
                    found = info["sub"][column["id"]]
            try:
                node = node[segment]
            except (KeyError, IndexError, TypeError):
                node = None
            previous = segment
        return found or info["type"] or "string"

    def route(self, path):
        """Return (output key, prompt, mixed) if an LLM method produced the value at `path`, else None.

        A fallback chain is judged, since the output doesn't say which field produced the value.
        """
        key, kind = self.owner(path)
        if kind in ("llm", "fallback"):
            return key, self.llm[key], kind == "fallback"
        return None


def judge_model():
    return os.environ.get("DOC_EXAMPLES_JUDGE_MODEL") or DEFAULT_JUDGE_MODEL


def format_type(declared):
    """Render a declared type: "currency", or "currency" plus its options in configurable syntax."""
    if isinstance(declared, dict):
        options = {k: v for k, v in declared.items() if k != "id"}
        return declared.get("id", "string") + (f" with options {json.dumps(options, ensure_ascii=False)}" if options else "")
    return str(declared)


def type_example(declared):
    type_id = declared.get("id") if isinstance(declared, dict) else declared
    return CONFIG["type_examples"].get(type_id, "none in the type reference")


def build_user_prompt(claims):
    blocks = [
        CONFIG["claim_template"].substitute(
            path=c["path"],
            prompt=json.dumps(c["prompt"]),
            type=format_type(c.get("type", "string")),
            type_example=type_example(c.get("type", "string")),
            documented_field=json.dumps(c.get("documented_field", c["documented"]), ensure_ascii=False),
            actual_field=json.dumps(c.get("actual_field", c["observed"]), ensure_ascii=False),
            documented=json.dumps(c["documented"], ensure_ascii=False),
            actual=json.dumps(c["observed"], ensure_ascii=False),
        )
        for c in claims
    ]
    return CONFIG["user_prompt"].substitute(claims="\n".join(blocks))


def judge(api_key, claims, model=None):
    """Judge claims, each {"path", "prompt", "documented", "observed"}.

    Returns {"model", "system_prompt", "user_prompt", "raw_output", "results"}, where results
    are in the same order as claims.
    """
    model = model or judge_model()
    exchange = {"model": model, "system_prompt": CONFIG["system_prompt"], "user_prompt": build_user_prompt(claims)}
    client = anthropic.Anthropic(api_key=api_key)
    try:
        response = client.messages.create(
            model=model,
            max_tokens=CONFIG["max_tokens"],
            system=exchange["system_prompt"],
            messages=[{"role": "user", "content": exchange["user_prompt"]}],
            output_config={"format": {"type": "json_schema", "schema": CONFIG["output_schema"]}},
        )
    except anthropic.APIStatusError as e:
        raise JudgeError(f"judge request to {model} failed ({e.status_code}): {e.message}")
    except anthropic.APIConnectionError as e:
        raise JudgeError(f"couldn't reach the judge: {e}")
    if response.stop_reason == "refusal":
        raise JudgeError(f"{model} declined to evaluate the claims")
    if response.stop_reason == "max_tokens":
        raise JudgeError(f"{model}'s response was cut off")
    exchange["model"] = response.model
    exchange["raw_output"] = next(b.text for b in response.content if b.type == "text")
    results = {r["path"]: r for r in json.loads(exchange["raw_output"])["results"]}
    missing = [c["path"] for c in claims if c["path"] not in results]
    if missing:
        raise JudgeError(f"the judge didn't return a verdict for {', '.join(missing)}")
    exchange["results"] = [results[c["path"]] for c in claims]
    return exchange


def classify(result):
    """Return "pass", "warn", or "fail" for one judge result."""
    if result["match"] == "fail":
        return "fail"
    if result["match"] == "pass" and result["confidence"] >= CONFIG["min_pass_confidence"]:
        return "pass"
    return "warn"
