"""Offline tests for code tests: no API keys or network. Run from the repo root:

    python3 -m unittest discover -s scripts/doc-detective/tests -t scripts/doc-detective
"""

import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(HERE, ".deps"), HERE]
