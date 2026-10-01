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


from . import settings

with open(os.path.join(settings.SCHEMAS_DIR, "envelope.schema.json"), encoding="utf-8") as f:
    SCHEMA = json.load(f)
with open(os.path.join(settings.CONFIG_DIR, "envelope.json"), encoding="utf-8") as f:
    CONFIG = json.load(f)


class EnvelopeInvalid(Exception):
    pass


def validate(envelope):
    """Raise EnvelopeInvalid unless `envelope` matches envelope-schema.json."""
    try:
        jsonschema.validate(envelope, SCHEMA)
    except jsonschema.ValidationError as e:
        where = "/".join(str(p) for p in e.absolute_path) or "top level"
        raise EnvelopeInvalid(f"{where}: {e.message}")


# Tuning, from config/envelope.json. Free text (FREE_TEXT_WORDS+ words with letters, or more than
# FREE_TEXT_LENGTH characters) gets a length check, not a format check; digit groups don't count as
# words, so "1800 123 4567" stays structured. A structured string with more than MAX_SHAPES formats
# is treated as free text. Lengths may stray LENGTH_SLACK of the range (at least LENGTH_MIN_SLACK
# characters) outside the observed range.
DEFAULT_RUNS = CONFIG["default_runs"]
FREE_TEXT_WORDS = CONFIG["free_text_words"]
FREE_TEXT_LENGTH = CONFIG["free_text_length"]
MAX_SHAPES = CONFIG["max_shapes"]
LENGTH_SLACK = CONFIG["length_slack"]
LENGTH_MIN_SLACK = CONFIG["length_min_slack"]


def path(test_id):
    return os.path.join(settings.envelopes_dir(), f"{test_id}.json")


def load(test_id):
    """The saved baseline for a test, or None if there isn't one. Raises EnvelopeInvalid if it's malformed."""
    if not os.path.exists(path(test_id)):
        return None
    try:
        with open(path(test_id), encoding="utf-8") as f:
            envelope = json.load(f)
    except ValueError as e:
        raise EnvelopeInvalid(f"not valid JSON ({e})")
    validate(envelope)
    return envelope


def save(envelope):
    validate(envelope)
    os.makedirs(settings.envelopes_dir(), exist_ok=True)
    with open(path(envelope["test_id"]), "w", encoding="utf-8") as f:
        json.dump(envelope, f, indent=2, ensure_ascii=False)
        f.write("\n")


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


def merge(old, new):
    """Combine two envelopes for the same config: counts add, sets combine, ranges widen."""
    if old["config_sha256"] != new["config_sha256"]:
        raise EnvelopeInvalid("can't merge envelopes built from different configs")
    slots = {}
    for slot in sorted(set(old["slots"]) | set(new["slots"])):
        a, b = old["slots"].get(slot), new["slots"].get(slot)
        if a is None or b is None:
            slots[slot] = a or b
            continue
        if "count_min" in a:
            slots[slot] = {"count_min": min(a["count_min"], b["count_min"]), "count_max": max(a["count_max"], b["count_max"])}
            continue
        total = a["observations"] + b["observations"]
        merged = {
            "observations": total,
            "null_rate": round((a["null_rate"] * a["observations"] + b["null_rate"] * b["observations"]) / total, 3),
        }
        for key in ("types", "json_types", "units", "confidence_signals"):
            merged[key] = sorted(set(a[key]) | set(b[key]))
        for key in ("shapes", "source_shapes"):
            if key in a or key in b:
                x, y = a.get(key, []), b.get(key, [])
                if x == "free text" or y == "free text":
                    merged[key] = "free text"
                else:
                    combined = sorted(set(x) | set(y))
                    merged[key] = combined if len(combined) <= MAX_SHAPES else "free text"
        for low, high in (("length_min", "length_max"), ("number_min", "number_max")):
            lows = [s[low] for s in (a, b) if low in s]
            if lows:
                merged[low] = min(lows)
                merged[high] = max(s[high] for s in (a, b) if high in s)
        slots[slot] = merged
    result = {
        "test_id": old["test_id"],
        "runs": old["runs"] + new["runs"],
        "built": old["built"],
        "updated": new["built"],
        "config_sha256": old["config_sha256"],
        "slots": slots,
    }
    validate(result)
    return result


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
