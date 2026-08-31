import sys
from pathlib import Path

_DESCRIPTIONS_DIR = Path(__file__).parent.parent.parent  # tests/ → test/ → descriptions/
sys.path.insert(0, str(_DESCRIPTIONS_DIR))
