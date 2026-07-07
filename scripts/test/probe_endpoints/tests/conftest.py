import sys
from pathlib import Path
import pytest

# Make probe_endpoints/ importable so tests can import probe_extraction_endpoints
_PROBE_DIR = Path(__file__).parent.parent  # tests/ → probe_endpoints/
sys.path.insert(0, str(_PROBE_DIR))

import probe_extraction_endpoints as probe


@pytest.fixture
def patched_api_key(monkeypatch):
    monkeypatch.setattr(probe, "API_KEY", "k")


@pytest.fixture
def patched_run_dir(tmp_path, monkeypatch):
    run_dir = tmp_path / "run"
    monkeypatch.setattr(probe, "RUN_DIR", run_dir)
    return run_dir
