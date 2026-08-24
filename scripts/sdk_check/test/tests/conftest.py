import sys
from pathlib import Path

_SDK_CHECK_DIR = Path(__file__).parent.parent.parent  # tests/ -> test/ -> sdk_check/
sys.path.insert(0, str(_SDK_CHECK_DIR))
