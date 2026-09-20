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
    '06 Kitchen': ((35.4,34.0,5.5),(46.8,43,4.7),24),
    '08 Cooking wall': ((42,36.4,5.5),(52.5,43.4,4.6),27),
    '10 Living room': ((31,34,5.5),(23,43,3.7),28),
    '09 Pantry': ((55.0,34.1,5.5),(59.6,43.3,4.0),22),
    '07 Rear garden': ((31,91,8.5),(31,43,7),22),
}
RENDERS = {
    '01-exterior': ('01 Reference exterior', 'front exterior'),
    '02-elevated': ('02 Elevated courtyard', 'side / elevated site'),
    '03-garden-entry': ('03 Garden threshold', 'courtyard feature'),
    '04-model-plan': ('04 Plan cutaway', 'single-level roof-off model plan'),
    '05-living-dining': ('05 Living and dining', 'View from the living room through courtyard glazing'),
    '06-kitchen': ('06 Kitchen', 'coordinated kitchen interior'),
    '08-cooking-wall': ('08 Cooking wall', 'induction cooking, oven and integrated refrigeration'),
    '10-living-room': ('10 Living room', 'furnished living room and timber ceiling'),
    '09-pantry': ('09 Pantry', 'fitted walk-in pantry and appliance storage'),
    '07-rear-garden': ('07 Rear garden', 'rear exterior and garden'),
}

def install_new_cameras():
    """Update named interior/rear detail cameras; preserve the rest of the scene."""
    g.ACTIVE = next(c for c in bpy.data.collections if c.name.startswith('10 Lighting'))
    for name in list(VIEWS)[4:]:
        existing=bpy.data.objects.get(name)
        if existing is not None:
            assert existing.type=='CAMERA',name
            bpy.data.objects.remove(existing,do_unlink=True)
        camera(name,*VIEWS[name])
