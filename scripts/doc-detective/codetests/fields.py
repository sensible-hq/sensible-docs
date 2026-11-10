"""What a config says about its fields: which output keys LLM methods produce, and their declared types."""

import json
import os
import re

LLM_METHODS = {"queryGroup", "list", "nlpTable"}

# Type headings in the docs' types reference (types.md)
TYPE_NAMES = [
    "Address", "Boolean", "Currency", "Date", "Distance", "Images", "Name", "Number", "Paragraph", "Percentage",
    "Phone Number", "String", "Table", "Weight", "Compose", "Custom", "Replace", "Any", "Accounting Currency",
]


class FieldIndex:
    """Which output keys LLM methods produce, wherever they sit in the config, and their types.

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
        """(field ID, kind) for the innermost known field ID on `path`, or (None, None).

        kind is "llm", "layout", or "fallback" (an LLM field and a non-LLM field share the ID).
        """
        for segment in reversed(path):
            if isinstance(segment, str) and (segment in self.llm or segment in self.other):
                if segment in self.llm:
                    return segment, "fallback" if segment in self.other else "llm"
                return segment, "layout"
        return None, None

    def is_llm(self, path):
        """Whether an LLM method produced the value at `path`. A fallback chain counts: the output
        doesn't say which field in the chain produced the value."""
        return self.owner(path)[1] in ("llm", "fallback")

    def declared_type(self, key):
        return self.types.get(key, {}).get("type") or "string"

    def type_for(self, path, expected):
        """The declared type for the value at `path` in the documented output `expected`.

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


def format_type(declared):
    """Render a declared type: "currency", or "currency" plus its options in configurable syntax."""
    if isinstance(declared, dict):
        options = {k: v for k, v in declared.items() if k != "id"}
        return declared.get("id", "string") + (f" with options {json.dumps(options, ensure_ascii=False)}" if options else "")
    return str(declared)


def type_id(declared):
    return declared.get("id") if isinstance(declared, dict) else declared


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
                examples[words[0].lower() + "".join(w.capitalize() for w in words[1:])] = re.sub(r"\s+", " ", block.group(1)).strip()
                break
    return examples
