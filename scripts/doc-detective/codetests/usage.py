"""The docs test account's Sensible usage, for reports.

The count comes from Sensible (GET /extractions), not from our own bookkeeping: local runs, CI runs,
and manual use in the app all land in the one test account, so Sensible's list is the source of
truth, and there's nothing to persist between CI runs. Reports call this after the tests run.
"""

import json
import os
from datetime import datetime, timezone

from . import settings


def month_to_date(key, now=None):
    """Extractions in the test account since the 1st of this month (UTC).

    Returns {"since", "extractions", "charged", "test_runs", "other"}. test_runs counts extractions
    named ci__..., which the test runners create."""
    import requests

    now = now or datetime.now(timezone.utc)
    since = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    params = {"start_date": since.strftime("%Y-%m-%dT%H:%M:%SZ"), "end_date": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "limit": 100}
    items = []
    for _ in range(200):  # at most 20,000 extractions; stop instead of looping forever on a bad token
        response = requests.get(f"{settings.API}/extractions", params=params, headers={"Authorization": f"Bearer {key}"}, timeout=60)
        response.raise_for_status()
        body = response.json()
        items += body.get("extractions", [])
        if not body.get("continuation_token"):
            break
        params["continuation_token"] = body["continuation_token"]
    test_runs = sum(str(i.get("document_name") or "").startswith("ci__") for i in items)
    return {
        "since": since.strftime("%Y-%m-%d"),
        "extractions": len(items),
        "charged": sum(i["charged"] for i in items if isinstance(i.get("charged"), (int, float))),
        "test_runs": test_runs,
        "other": len(items) - test_runs,
    }


def budget():
    value = os.environ.get(settings.BUDGET_VAR, "").strip()
    return int(value) if value.isdigit() else None


def save_run(counts):
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    with open(settings.RUN_FILE, "w", encoding="utf-8") as f:
        json.dump(counts, f)


def load_run(output_dir):
    try:
        with open(os.path.join(output_dir, "run.json"), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
