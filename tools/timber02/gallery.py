"""Named real-scene camera definitions for the current Timber Courtyard gallery."""
from common import geometry as g
from common.geometry import camera
import bpy

VIEWS = {
    '01 Reference exterior': ((31,-81,30),(31,20,4.8),40),
    '02 Elevated courtyard': ((88,-63,59),(30,22,4),43),
    '03 Garden threshold': ((31,-24,6.2),(31,32,6.5),24),
    '04 Plan cutaway': ((31,24,105),(31,24,0),46),
    '05 Living and dining': ((18,44.7,5.5),(30,28,5.5),40),
    '06 Kitchen': ((35.4,33.4,6.0),(45.3,41.3,4.25),24),
    '07 Rear garden': ((31,91,8.5),(31,43,7),22),
}
RENDERS = {
    '01-exterior': ('01 Reference exterior', 'front exterior'),
    '02-elevated': ('02 Elevated courtyard', 'side / elevated site'),
    '03-garden-entry': ('03 Garden threshold', 'courtyard feature'),
    '04-model-plan': ('04 Plan cutaway', 'single-level roof-off model plan'),
    '05-living-dining': ('05 Living and dining', 'View from the living room through courtyard glazing'),
    '06-kitchen': ('06 Kitchen', 'schematic kitchen interior'),
    '07-rear-garden': ('07 Rear garden', 'rear exterior and garden'),
}

def install_new_cameras():
    """Add/update only the three gallery expansion cameras; preserve the scene."""
    g.ACTIVE = next(c for c in bpy.data.collections if c.name.startswith('10 Lighting'))
    for name in list(VIEWS)[4:]:
        existing=bpy.data.objects.get(name)
        if existing is not None:
            assert existing.type=='CAMERA',name
            bpy.data.objects.remove(existing,do_unlink=True)
        camera(name,*VIEWS[name])
