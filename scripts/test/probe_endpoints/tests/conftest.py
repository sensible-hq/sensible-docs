import sys
from pathlib import Path

# Make probe_endpoints/ importable so tests can import probe_extraction_endpoints
_PROBE_DIR = Path(__file__).parent.parent  # tests/ → probe_endpoints/
sys.path.insert(0, str(_PROBE_DIR))
