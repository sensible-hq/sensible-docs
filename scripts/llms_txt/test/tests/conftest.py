import sys
from pathlib import Path

_LLMS_TXT_DIR = Path(__file__).parent.parent.parent  # tests/ → test/ → llms_txt/
sys.path.insert(0, str(_LLMS_TXT_DIR))

import generate  # noqa: E402

FIXTURES = Path(__file__).parent.parent / "fixtures"
SNAPSHOTS = Path(__file__).parent.parent / "snapshots"
