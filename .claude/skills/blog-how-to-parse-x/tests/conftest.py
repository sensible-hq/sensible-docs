import sys
from pathlib import Path

# Make scripts/ importable so upload_and_extract.py can import upload_pr_extractor
_REPO_ROOT = Path(__file__).parent.parent.parent.parent.parent  # tests/ → skill/ → blog-how-to-parse-x/ → skills/ → .claude/ → repo root
sys.path.insert(0, str(_REPO_ROOT / "scripts"))

# Make the skill directory importable
_SKILL = Path(__file__).parent.parent
sys.path.insert(0, str(_SKILL))
