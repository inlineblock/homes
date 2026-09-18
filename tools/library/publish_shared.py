"""Explicit, non-destructive publisher for original shared collections."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
from common.shared_assets import publish_catalog
publish_catalog(ROOT)
