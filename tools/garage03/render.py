"""Render review drafts; native model remains in its complete stored state."""
import bpy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools'),str(Path(__file__).parent)]
from design import PLATFORM_SPACING
from common.geometry import F
HOME=ROOT/'homes/garage-loft-03';OUT=HOME/'outputs/work';OUT.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene
try:
    p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
    for d in p.devices:d.use=d.type=='METAL'
    s.cycles.device='GPU'
except Exception:pass
views=[('01 Exterior','01-exterior'),('02 Game room','02-game-room'),('03 Garage stored','03-garage-stored'),('04 Pit section','04-pit-section'),('05 Raised retrieval','05-raised-retrieval')]
requested=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
for cam,file in views:
    if requested and file not in requested:continue
    s.camera=bpy.data.objects[cam]
    for c in bpy.data.collections:c.hide_render=False
    for o in s.objects:o.hide_render=False
    for o in s.objects:
        if o.get('lift_moves'):o.location.z+=PLATFORM_SPACING*F if file=='05-raised-retrieval' else 0
    if file in ['03-garage-stored','04-pit-section','05-raised-retrieval']:
        bpy.data.collections['04 Facade | garage doors'].hide_render=True
    if file=='04-pit-section':
        for name in ['09 Roof | removable','15 Landscape | site illustration','04 Facade | garage doors','05 Entry | timber door and canopy','07 Cladding | cedar and fascia','06 Architecture | upper shell']:bpy.data.collections[name].hide_render=True
        for name in ['Pit front','Ground front','Garage west pier','Garage lintel','Entry left pier','Entry right pier','Entry lintel','East ground wall']:
            bpy.data.objects[name].hide_render=True
    s.render.filepath=str(OUT/(file+'.png'));bpy.ops.render.render(write_still=True)
    if file=='05-raised-retrieval':
        for o in s.objects:
            if o.get('lift_moves'):o.location.z-=PLATFORM_SPACING*F
    print('GARAGE_DRAFT_RENDERED',file,flush=True)
