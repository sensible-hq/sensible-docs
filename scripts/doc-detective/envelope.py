"""Regression envelopes for LLM-produced fields.

An envelope is a baseline of what each LLM field's output normally looks like, measured over
several runs of the same example: how often it's null, its output type and JSON type, the format
and length of strings, the format of the source text, the range of numbers, the unit, Sensible's confidence signal, and the
item count of lists and tables. A later run that falls outside the envelope is a signal that the
feature's behavior shifted, even when the LLM judge still passes the answer.

Every measurement is deterministic. No LLM is involved in building or checking an envelope.
"""

import hashlib
import json
import os
import re
from datetime import datetime, timezone

import jsonschema

SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "envelope-schema.json")
with open(SCHEMA_PATH, encoding="utf-8") as f:
    SCHEMA = json.load(f)


class EnvelopeInvalid(Exception):
    pass


def validate(envelope):
    """Raise EnvelopeInvalid unless `envelope` matches envelope-schema.json."""
    try:
        jsonschema.validate(envelope, SCHEMA)
    except jsonschema.ValidationError as e:
        where = "/".join(str(p) for p in e.absolute_path) or "top level"
        raise EnvelopeInvalid(f"{where}: {e.message}")

# Free text (3+ words with letters, or more than 40 characters) gets a length check, not a
# format check. Digit groups don't count as words, so "1800 123 4567" stays structured.
FREE_TEXT_WORDS = 3
FREE_TEXT_LENGTH = 40
# A structured string with more distinct formats than this is treated as free text
MAX_SHAPES = 20
# Lengths may stray this far outside the observed range (a fraction of it, or LENGTH_MIN_SLACK chars)
LENGTH_SLACK = 0.25
LENGTH_MIN_SLACK = 2


def config_hash(config_text):
    return hashlib.sha256(config_text.encode("utf-8")).hexdigest()


def shape(text):
    """Reduce a string to its format: digits become 9, letters a. "1800-123-4567" -> "9999-999-9999"."""
    return re.sub(r"[A-Za-z]", "a", re.sub(r"[0-9]", "9", text))


def is_free_text(text):
    words = [w for w in text.split() if re.search(r"[A-Za-z]", w)]
    return len(words) >= FREE_TEXT_WORDS or len(text) > FREE_TEXT_LENGTH


def observe(value, slot, out):
    """Add observations for one LLM field's output to `out`, keyed by slot.

    A slot is a path with list positions replaced by "*" and NLP Table columns named by ID,
    so every row of a list contributes to the same slots.
    """
    if isinstance(value, dict) and "columns" in value and isinstance(value["columns"], list):
        for column in value["columns"]:
            if isinstance(column, dict):
                observe(column.get("values"), f"{slot}.columns[{column.get('id')}].values", out)
        for key, sub in value.items():
            if key != "columns":
                observe(sub, f"{slot}.{key}", out)
    elif isinstance(value, dict) and ("value" in value or "type" in value):
        typed = value
        obs = out.setdefault(slot, [])
        inner = typed.get("value")
        entry = {
            "null": inner is None,
            "type": typed.get("type"),
            "json_type": type(inner).__name__ if inner is not None else None,
            "unit": typed.get("unit"),
            "confidence": typed.get("confidenceSignal"),
        }
        if isinstance(inner, str):
            entry["length"] = len(inner)
            if is_free_text(inner):
                entry["free_text"] = True
            else:
                entry["shape"] = shape(inner)
        elif isinstance(inner, (int, float)) and not isinstance(inner, bool):
            entry.update(number=inner)
        source = typed.get("source")
        if isinstance(source, str) and not is_free_text(source):
            entry["source_shape"] = shape(source)
        obs.append(entry)
    elif isinstance(value, dict):
        for key, sub in value.items():
            observe(sub, f"{slot}.{key}", out)
    elif isinstance(value, list):
        out.setdefault(f"{slot}#count", []).append({"count": len(value)})
        for item in value:
            observe(item, f"{slot}[*]", out)
    else:
        out.setdefault(slot, []).append({"null": value is None, "type": None, "json_type": type(value).__name__ if value is not None else None})


def observe_output(parsed_document, llm_keys):
    """Observations for every LLM field in one extraction's parsed_document."""
    out = {}
    for key in llm_keys:
        if key in parsed_document:
            observe(parsed_document[key], key, out)
        else:
            out.setdefault(key, []).append({"null": True, "type": None, "json_type": None})
    return out


def build(runs, config_text, test_id):
    """Aggregate observations from several runs into an envelope."""
    slots = {}
    for run in runs:
        for slot, entries in run.items():
            slots.setdefault(slot, []).extend(entries)
    envelope = {}
    for slot, entries in sorted(slots.items()):
        if slot.endswith("#count"):
            counts = [e["count"] for e in entries]
            envelope[slot] = {"count_min": min(counts), "count_max": max(counts)}
            continue
        summary = {
            "observations": len(entries),
            "null_rate": round(sum(e["null"] for e in entries) / len(entries), 3),
            "types": sorted({e["type"] for e in entries if e.get("type")}),
            "json_types": sorted({e["json_type"] for e in entries if e.get("json_type")}),
            "units": sorted({e["unit"] for e in entries if e.get("unit")}),
            "confidence_signals": sorted({e["confidence"] for e in entries if e.get("confidence")}),
        }
        shapes = sorted({e["shape"] for e in entries if "shape" in e})
        if any(e.get("free_text") for e in entries) or len(shapes) > MAX_SHAPES:
            summary["shapes"] = "free text"
        elif shapes:
            summary["shapes"] = shapes
        source_shapes = sorted({e["source_shape"] for e in entries if "source_shape" in e})
        if source_shapes:
            summary["source_shapes"] = source_shapes if len(source_shapes) <= MAX_SHAPES else "free text"
        lengths = [e["length"] for e in entries if "length" in e]
        if lengths:
            summary["length_min"], summary["length_max"] = min(lengths), max(lengths)
        numbers = [e["number"] for e in entries if "number" in e]
        if numbers:
            summary["number_min"], summary["number_max"] = min(numbers), max(numbers)
        envelope[slot] = summary
    built = {
        "test_id": test_id,
        "runs": len(runs),
        "built": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "config_sha256": config_hash(config_text),
        "slots": envelope,
    }
    validate(built)
    return built


def baseline_range(low, high, noun):
    """Describe the baseline's range in words: "baseline values ranged from 50 to 60", "baseline value was always 100"."""
    if low == high:
        return f"baseline {noun} was always {low}"
    return f"baseline {noun}s ranged from {low} to {high}"


JSON_NAMES = {"str": "string", "int": "number", "float": "number", "bool": "boolean", "list": "array", "dict": "object"}


def baseline_saw(values, quote=False):
    """Describe what the baseline saw: "baseline only saw currency", "baseline saw '9999 999 9999' or '9999-999-9999'"."""
    shown = [repr(v) if quote else str(v) for v in values]
    if len(shown) == 1:
        return f"baseline only saw {shown[0]}"
    return f"baseline saw {', '.join(shown[:-1])} or {shown[-1]}"


def check(envelope, observations):
    """Return {slot: [reasons]} for every observation outside the envelope."""
    breaches = {}

    def breach(slot, reason):
        breaches.setdefault(slot, []).append(reason)

    for slot, entries in observations.items():
        baseline = envelope["slots"].get(slot)
        if baseline is None:
            breach(slot, "not seen in any baseline run")
            continue
        if slot.endswith("#count"):
            for e in entries:
                if not baseline["count_min"] <= e["count"] <= baseline["count_max"]:
                    items = "item" if e["count"] == 1 else "items"
                    breach(slot, f"{e['count']} {items}; {baseline_range(baseline['count_min'], baseline['count_max'], 'item count')}")
            continue
        for e in entries:
            if e["null"]:
                if baseline["null_rate"] == 0:
                    breach(slot, "null; never null in the baseline")
                continue
            if e.get("type") and baseline["types"] and e["type"] not in baseline["types"]:
                breach(slot, f"type {e['type']}; {baseline_saw(baseline['types'])}")
            if e.get("json_type") and baseline["json_types"] and e["json_type"] not in baseline["json_types"]:
                breach(slot, f"value is a {JSON_NAMES.get(e['json_type'], e['json_type'])}; "
                             f"{baseline_saw(sorted({JSON_NAMES.get(j, j) for j in baseline['json_types']}))}")
            if e.get("unit") and baseline["units"] and e["unit"] not in baseline["units"]:
                breach(slot, f"unit {e['unit']}; {baseline_saw(baseline['units'])}")
            if e.get("confidence") and baseline["confidence_signals"] and e["confidence"] not in baseline["confidence_signals"]:
                breach(slot, f"confidence signal {e['confidence']}; {baseline_saw(baseline['confidence_signals'])}")
            if "shape" in e and isinstance(baseline.get("shapes"), list) and e["shape"] not in baseline["shapes"]:
                breach(slot, f"new format {e['shape']!r}; {baseline_saw(baseline['shapes'], quote=True)}")
            if "source_shape" in e and isinstance(baseline.get("source_shapes"), list) and e["source_shape"] not in baseline["source_shapes"]:
                breach(slot, f"new source format {e['source_shape']!r}; {baseline_saw(baseline['source_shapes'], quote=True)}")
            if "length" in e and "length_min" in baseline:
                spread = baseline["length_max"] - baseline["length_min"]
                slack = max(LENGTH_MIN_SLACK, round(spread * LENGTH_SLACK), round(baseline["length_max"] * LENGTH_SLACK))
                if not baseline["length_min"] - slack <= e["length"] <= baseline["length_max"] + slack:
                    breach(slot, f"length {e['length']}; {baseline_range(baseline['length_min'], baseline['length_max'], 'length')}")
            if "number" in e and "number_min" in baseline and not baseline["number_min"] <= e["number"] <= baseline["number_max"]:
                breach(slot, f"value {e['number']}; {baseline_range(baseline['number_min'], baseline['number_max'], 'value')}")
    return breaches
