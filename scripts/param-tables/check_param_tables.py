#!/usr/bin/env python3
"""Check SenseML reference parameter tables against the public SenseML JSON Schema.

Each parameter table (header `key | value | description`) claims, per row: a parameter name,
whether it's required, a type or allowed values, and often a default. This checks those claims
against https://schema.sensible.so/configuration.schema.json. The page needs no test markup: the
table's `id` row (for example `row`) names the schema definition, and global parameters are read
from the Method page's table.

Errors (exit 1):
  - a documented parameter the schema doesn't have
  - a documented allowed value the schema rejects
  - a required flag or type that disagrees with the schema
  - a documented default the schema would reject
Warnings:
  - schema parameters the table doesn't document (and that aren't global parameters)
  - allowed values the schema accepts but the table doesn't list

Defaults themselves can't be checked here: the schema declares none.

Usage:
  check_param_tables.py PAGE [PAGE ...]
  check_param_tables.py --all            every page under docs/Senseml reference/
  --schema PATH_OR_URL                   default: the public schema URL
"""

import argparse
import glob
import json
import os
import re
import sys
import urllib.parse
import urllib.request

SCHEMA_URL = "https://schema.sensible.so/configuration.schema.json"
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REFERENCE = os.path.join(REPO, "docs", "Senseml reference")
METHOD_PAGE = os.path.join(REFERENCE, "field-query-object", "method.md")
NO_DEFAULT = {"none", "null", "infinity", "unspecified", "n/a", "undefined", "no"}
TYPE_WORDS = {"boolean": "boolean", "number": "number", "integer": "number", "string": "string", "array": "array", "object": "object"}


class Schema:
    def __init__(self, data):
        self.defs = data["definitions"]

    def resolve(self, node):
        while isinstance(node, dict) and "$ref" in node:
            # Some generated definition names are URL-encoded in $refs (%3C for <)
            node = self.defs[urllib.parse.unquote(node["$ref"].split("/")[-1])]
        return node

    def variants_for(self, method_id, prefer_types=False):
        """Every object schema whose `id` is const `method_id`: (labels, merged properties, required).

        Some methods have several variants (Query Group with `queries`, or with `source_ids`). A
        parameter is valid if any variant has it, and required only if every variant requires it.
        """
        def has_id(node):
            return isinstance(node, dict) and isinstance(node.get("properties"), dict) \
                and node["properties"].get("id", {}).get("const") == method_id
        found, seen = [], set()

        def walk(node, where):
            if isinstance(node, dict):
                if has_id(node) and id(node) not in seen:
                    seen.add(id(node))
                    found.append((where, node))
                for k, v in node.items():
                    walk(v, f"{where}/{k}")
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    walk(v, f"{where}/{i}")
        for name, d in self.defs.items():
            walk(d, name)
        # Types and methods share the id namespace (`paragraph` is both). types.md describes types.
        preferred = [(w, n) for w, n in found if w.split("/")[0].endswith("Eduction") == prefer_types]
        found = preferred or found
        if not found:
            return [], {}, set()
        props = {}
        for _, node in found:
            for k, v in node["properties"].items():
                props.setdefault(k, v)
        required = set.intersection(*(set(n.get("required", [])) for _, n in found))
        labels = sorted({w if "/" not in w else f"inline in {w.split('/')[0]}" for w, _ in found})
        return labels, props, required

    def definition_for(self, method_id):
        """The object schema whose `id` is const `method_id`.

        Named definitions first (types share the id namespace, so methods before *Eduction types),
        then objects defined inline anywhere in the schema, for example inside an anyOf.
        """
        def has_id(node):
            return isinstance(node, dict) and isinstance(node.get("properties"), dict) \
                and node["properties"].get("id", {}).get("const") == method_id
        named = sorted((name for name, d in self.defs.items() if has_id(d)), key=lambda n: n.endswith("Eduction"))
        if named:
            return named[0], self.defs[named[0]]
        found = []

        def walk(node, where):
            if isinstance(node, dict):
                if has_id(node):
                    found.append((where, node))
                for k, v in node.items():
                    walk(v, f"{where}/{k}")
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    walk(v, f"{where}/{i}")
        for name, d in self.defs.items():
            walk(d, name)
        return (f"inline in {found[0][0].split('/')[0]}", found[0][1]) if found else (None, None)

    def allowed(self, node):
        """(set of allowed constant values or None, set of JSON types)."""
        node = self.resolve(node)
        if "const" in node:
            return {node["const"]}, {type_of(node["const"])}
        if "enum" in node:
            return set(node["enum"]), {type_of(v) for v in node["enum"]}
        options = node.get("anyOf") or node.get("oneOf")
        if options:
            values, types, open_ended = set(), set(), False
            for option in options:
                v, t = self.allowed(option)
                types |= t
                if v is None:
                    open_ended = True
                else:
                    values |= v
            return (None if open_ended else values), types
        t = node.get("type")
        types = set(t) if isinstance(t, list) else {t} if t else set()
        return None, {"number" if x == "integer" else x for x in types}


def type_of(value):
    return {bool: "boolean", int: "number", float: "number", str: "string", list: "array", dict: "object"}.get(type(value), "null")


def load_schema(source):
    if re.match(r"https?://", source):
        # The schema host rejects Python's default user agent
        request = urllib.request.Request(source, headers={"User-Agent": "sensible-docs param-table check"})
        with urllib.request.urlopen(request, timeout=30) as response:
            return Schema(json.load(response))
    with open(source, encoding="utf-8") as f:
        return Schema(json.load(f))


def strip_markup(text):
    text = re.sub(r"<br\s*/?>", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return text.strip()


def parse_tables(path):
    """Yield parameter rows: {line, name, required, global_ref, values, types, default, raw}."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    in_table = False
    table = -1
    for number, line in enumerate(lines, 1):
        if not line.lstrip().startswith("|"):
            in_table = False
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if [c.lower() for c in cells[:2]] == ["key", "value"]:
            in_table = True
            table += 1
            continue
        if not in_table or re.match(r"^:?-+:?$", cells[0]):
            continue
        key_cell, value_cell = cells[0], cells[1] if len(cells) > 1 else ""
        name = re.sub(r"\*\*\(?(required|deprecated)\)?\*\*|\((\*\*)?required(\*\*)?\)|`", "", key_cell, flags=re.I).strip()
        name = re.sub(r"\s+", " ", name)
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            continue
        value = strip_markup(value_cell)
        global_ref = bool(re.search(r"global parameter|doc:method", value_cell, re.I))
        parts = re.split(r"(?i)\bdefault:\s*", value, maxsplit=1)
        main, default_part = parts[0], (parts[1] if len(parts) > 1 else None)
        values = re.findall(r"`([^`]+)`", main)
        unquoted = re.sub(r"`[^`]*`", "", main)
        types = {TYPE_WORDS[w.lower()] for w in re.findall(r"\b(boolean|number|integer|string|array|object)\b", unquoted, re.I)}
        default = None
        if default_part is not None:
            m = re.match(r"`([^`]+)`|([^\s.,;]+)", default_part.strip())
            default = (m.group(1) or m.group(2)) if m else None
            # Docs conventions for "no default" or "unbounded", not literal values
            if default and default.lower() in NO_DEFAULT:
                default = None
        yield {"table": table, "line": number, "name": name, "required": bool(re.search(r"required", key_cell, re.I)),
               "global_ref": global_ref, "values": values, "types": types, "default": default, "raw": value}


def coerce(token):
    """A documented value as JSON would see it: `false` -> False, `0.08` -> 0.08, else the string."""
    try:
        return json.loads(token)
    except ValueError:
        return token


def global_parameters():
    return {row["name"] for row in parse_tables(METHOD_PAGE)} - {"id"}


def check_page(path, schema, globals_):
    """Check every parameter table on a page. Each table's `id` row names its schema definition."""
    rows = list(parse_tables(path))
    rel = os.path.relpath(path, REPO)
    tables = {}
    for row in rows:
        tables.setdefault(row["table"], []).append(row)
    results = []
    for table_rows in tables.values():
        id_rows = [r for r in table_rows if r["name"] == "id" and len(r["values"]) == 1]
        if not id_rows:
            continue
        results.append(check_table(rel, table_rows, id_rows[0], schema, globals_))
    return results or None


def check_table(rel, rows, id_row, schema, globals_):
    method_id = id_row["values"][0]
    labels, props, required = schema.variants_for(method_id, prefer_types=os.path.basename(rel) == "types.md")
    if not props:
        return {"page": rel, "method": method_id, "definition": None, "rows": len(rows),
                "errors": [f"{rel}:{id_row['line']}: no schema definition with id `{method_id}`"], "warnings": []}
    errors, warnings = [], []
    documented = set()
    for row in rows:
        name = row["name"]
        where = f"{rel}:{row['line']}"
        documented.add(name)
        if name not in props:
            errors.append(f"{where}: `{name}` isn't a parameter of `{method_id}` in the schema")
            continue
        if row["required"] != (name in required):
            errors.append(f"{where}: `{name}` is documented as {'required' if row['required'] else 'optional'}, "
                          f"the schema says {'required' if name in required else 'optional'}")
        if row["global_ref"]:
            continue
        allowed, types = schema.allowed(props[name])
        if row["types"] and types and not (row["types"] & types):
            errors.append(f"{where}: `{name}` is documented as {'/'.join(sorted(row['types']))}, "
                          f"the schema says {'/'.join(sorted(types))}")
        doc_values = [coerce(v) for v in row["values"]]
        if allowed is not None and doc_values and not row["types"]:
            bad = [v for v in doc_values if v not in allowed]
            if bad:
                errors.append(f"{where}: `{name}` lists {', '.join(json.dumps(v) for v in bad)}, "
                              f"which the schema doesn't allow (allowed: {', '.join(json.dumps(v) for v in sorted(allowed, key=str))})")
            missing = allowed - set(doc_values)
            if missing and name != "id":
                warnings.append(f"{where}: `{name}`: the schema also allows {', '.join(json.dumps(v) for v in sorted(missing, key=str))}")
        if row["default"] is not None:
            default = coerce(row["default"])
            if allowed is not None and default not in allowed:
                errors.append(f"{where}: `{name}` default {json.dumps(default)} isn't an allowed value")
            elif allowed is None and types and type_of(default) not in types:
                errors.append(f"{where}: `{name}` default {json.dumps(default)} is a {type_of(default)}, "
                              f"the schema says {'/'.join(sorted(types))}")
    undocumented = sorted(set(props) - documented - globals_)
    if undocumented:
        warnings.append(f"{rel}: schema parameters of `{method_id}` not in the table "
                        f"(and not global): {', '.join(undocumented)}")
    return {"page": rel, "method": method_id, "definition": ", ".join(labels), "rows": len(rows),
            "errors": errors, "warnings": warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pages", nargs="*")
    parser.add_argument("--all", action="store_true", help="Check every page under docs/Senseml reference/")
    parser.add_argument("--schema", default=SCHEMA_URL)
    args = parser.parse_args()
    pages = sorted(glob.glob(os.path.join(REFERENCE, "**", "*.md"), recursive=True)) if args.all else args.pages
    if not pages:
        parser.error("give a page, or --all")
    schema = load_schema(args.schema)
    globals_ = global_parameters()
    checked = skipped = 0
    total_errors = total_warnings = 0
    for page in pages:
        if os.path.basename(page).startswith("draft-") or (args.all and "deprecated-features" in page):
            continue
        results = check_page(page, schema, globals_)
        if results is None:
            skipped += 1
            continue
        checked += 1
        for result in results:
            status = "FAIL" if result["errors"] else ("WARN" if result["warnings"] else "PASS")
            print(f"{status} {result['page']}  (`{result['method']}` -> {result['definition']}, {result.get('rows', 0)} rows)")
            for e in result["errors"]:
                print(f"  error   {e}")
            for w in result["warnings"]:
                print(f"  warning {w}")
            total_errors += len(result["errors"])
            total_warnings += len(result["warnings"])
    print(f"\n{checked} page(s) checked, {skipped} without a method parameter table; "
          f"{total_errors} error(s), {total_warnings} warning(s)")
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
