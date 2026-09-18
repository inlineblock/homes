"""Publish missing original hardware library versions without overwriting assets."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from common.hardware_assets import publish
publish(ROOT)
print('HARDWARE_PUBLISHED')
