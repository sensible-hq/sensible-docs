"""LLM-as-judge for documented output of LLM-based SenseML methods.

LLM methods (Query Group, List, NLP Table) can return a correct answer that's worded or
formatted differently from the docs, for example "1800-123-4567" instead of "1800 123 4567".
The runner sends only the LLM fields whose values differ from the docs to a judge model,
which decides per field whether the actual value still supports what the docs show.

The judge is a different model from the one that generated the answer. The generating model
comes from the config's llmEngine provider (default: open-ai), looked up in the tables in
docs/Senseml reference/concepts/llm-models.md.
"""

import json

import anthropic

JUDGE_MODEL = "claude-opus-5"
ALTERNATE_JUDGE_MODEL = "claude-sonnet-5"
# A pass below this confidence is reported as a warning instead
MIN_PASS_CONFIDENCE = 0.7

# From docs/Senseml reference/concepts/llm-models.md. Update both together.
GENERATOR_MODELS = {
    "queryGroup": {
        "default": {"open-ai": "GPT-4o mini", "anthropic": "Claude 4.5 Haiku", "google": "Gemini 3.1 Flash-Lite"},
        "sourceIds": {"open-ai": "GPT-4o mini", "anthropic": "Claude 4.5 Sonnet", "google": "Gemini 3 Flash Preview"},
    },
    "list": {
        "fast": {"open-ai": "GPT-4o mini", "anthropic": "Claude 4.5 Haiku", "google": "Gemini 3.1 Flash-Lite"},
        "thorough": {"open-ai": "GPT-4o", "anthropic": "Claude 4.5 Sonnet", "google": "Gemini 3.1 Flash-Lite"},
        "long": {"open-ai": "GPT-4o mini", "anthropic": "Claude 4.5 Haiku", "google": "Gemini 3.1 Flash-Lite"},
    },
    "nlpTable": {
        "default": {"open-ai": "GPT-4o", "anthropic": "Claude 4.5 Haiku", "google": "Gemini 3.1 Flash-Lite"},
    },
}

# Generating models that are the same model as a judge candidate
SAME_MODEL = {
    "claude-opus-5": {"Claude Opus 5"},
    "claude-sonnet-5": {"Claude Sonnet 5"},
}

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


def llm_fields(config):
    """Map each top-level output key produced by an LLM method to its generator model and prompt."""
    fields = {}
    for field in config.get("fields", []):
        method = field.get("method") or {}
        method_id = method.get("id")
        if method_id not in GENERATOR_MODELS:
            continue
        provider = (method.get("llmEngine") or {}).get("provider", "open-ai").replace("openai", "open-ai")
        if method_id == "queryGroup":
            variant = "sourceIds" if method.get("sourceIds") else "default"
            generator = GENERATOR_MODELS[method_id][variant].get(provider)
            for query in method.get("queries", []):
                fields[query["id"]] = {"method": method_id, "generator": generator, "prompt": query.get("description", "")}
        else:
            variant = (method.get("llmEngine") or {}).get("mode", "fast") if method_id == "list" else "default"
            generator = GENERATOR_MODELS[method_id].get(variant, GENERATOR_MODELS[method_id][next(iter(GENERATOR_MODELS[method_id]))]).get(provider)
            fields[field["id"]] = {"method": method_id, "generator": generator, "prompt": method.get("description", "")}
    return fields


def pick_judge(generators):
    """Return a judge model that differs from every generating model."""
    for candidate in (JUDGE_MODEL, ALTERNATE_JUDGE_MODEL):
        if not SAME_MODEL[candidate] & set(generators):
            return candidate
    raise JudgeError(f"no judge model differs from the generating models {sorted(generators)}")


def judge(api_key, claims):
    """Judge claims, each {"path", "prompt", "documented", "observed"}. Returns (judge model, results)."""
    model = pick_judge({c["generator"] for c in claims if c.get("generator")})
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
        response = client.beta.messages.create(
            model=model,
            max_tokens=16000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user}],
            output_config={"format": {"type": "json_schema", "schema": VERDICT_SCHEMA}},
            # On a safety decline, rerun on Anthropic's recommended fallback model
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
    except anthropic.APIStatusError as e:
        raise JudgeError(f"judge request failed ({e.status_code}): {e.message}")
    except anthropic.APIConnectionError as e:
        raise JudgeError(f"couldn't reach the judge: {e}")
    if response.stop_reason == "refusal":
        raise JudgeError("the judge declined to evaluate the claims")
    if response.stop_reason == "max_tokens":
        raise JudgeError("the judge's response was cut off")
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
