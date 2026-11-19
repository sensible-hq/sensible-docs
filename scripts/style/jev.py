"""Client for TypeSafe's Jev judge (POST https://api.typesafe.ai/v1/systemone).

One call judges one piece of text (`state`) against named questions. This module only sends and
receives; scripts/style/judge.py decides what to ask.

Environment:
  TYPESAFE_API_KEY  required for live calls
  JEV_REPLAY=<dir>  answer from recorded responses keyed by a hash of the request; never touches the
                    network, and a missing recording raises JevUnavailable. Several directories,
                    separated by the path separator (":"), are searched in order. With JEV_RECORD
                    also set, a missing recording is fetched live and recorded (refresh only what
                    changed).
  JEV_RECORD=<dir>  save each live response there for later replay

Price: $0.042 per million input tokens; output tokens aren't priced (sensible-docs-gen config/prices.json,
from Frances, 2026-11-02).
"""
import hashlib
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"
INPUT_USD_PER_M = 0.042


class JevUnavailable(RuntimeError):
    """No verdict: no key, a network or HTTP error, or no recorded replay. Never counts as a pass."""


def digest(body: dict) -> str:
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]


def choice_question(ask: str, criteria: dict) -> dict:
    return {"type": "choice", "instructions": ask, "criteria": {str(k): str(v) for k, v in criteria.items()}}


def call(state: str, questions: dict, model: str = MODEL, timeout: int = 90) -> dict:
    """Send one request and return Jev's JSON response."""
    body = {"state": state, "model": model, "questions": questions}
    replay = os.environ.get("JEV_REPLAY")
    if replay:
        name = f"{digest(body)}.json"
        for d in replay.split(os.pathsep):
            if (Path(d) / name).exists():
                return json.loads((Path(d) / name).read_text())
        if not os.environ.get("JEV_RECORD"):
            raise JevUnavailable(f"no recorded response {name} in {replay}")
    key = os.environ.get("TYPESAFE_API_KEY")
    if not key:
        raise JevUnavailable("TYPESAFE_API_KEY isn't set")
    req = urllib.request.Request(API, data=json.dumps(body).encode(), method="POST", headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": "sensible-docs-style"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise JevUnavailable(f"HTTP {e.code}: {e.read()[:300].decode(errors='replace')}") from None
    except (urllib.error.URLError, TimeoutError) as e:
        raise JevUnavailable(f"network: {e}") from None
    record = os.environ.get("JEV_RECORD")
    if record:
        Path(record).mkdir(parents=True, exist_ok=True)
        (Path(record) / f"{digest(body)}.json").write_text(json.dumps(resp, indent=2) + "\n")
    return resp


def cost(usage: dict) -> float:
    return usage.get("input_tokens", 0) * INPUT_USD_PER_M / 1e6
