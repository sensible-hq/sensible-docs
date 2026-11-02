import sys
from pathlib import Path

_DOCS_TRIAGE_DIR = Path(__file__).parent.parent.parent  # tests/ → test/ → docs_triage/
sys.path.insert(0, str(_DOCS_TRIAGE_DIR))
