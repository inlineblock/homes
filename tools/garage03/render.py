"""Render review drafts; native model remains in its complete stored state."""
import bpy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools'),str(Path(__file__).parent)]
from design import PLATFORM_SPACING
from cameras import VIEWS
from common.geometry import F
HOME=ROOT/'homes/garage-loft-03';OUT=HOME/'outputs/work';OUT.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene
try:
    p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
    for d in p.devices:d.use=d.type=='METAL'
    s.cycles.device='GPU'
except Exception:pass
views=[(name,filename) for name,filename,*_ in VIEWS]
import os
s.cycles.samples=int(os.environ.get('GARAGE_SAMPLES',s.cycles.samples))
s.render.resolution_percentage=int(os.environ.get('GARAGE_RENDER_PERCENT',100))
requested=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
base_objects={o.name:(o.matrix_world.copy(),o.hide_render) for o in s.objects}
base_collections={c.name:c.hide_render for c in bpy.data.collections}
def restore_view_state():
    for name,(matrix,hidden) in base_objects.items():
        o=bpy.data.objects[name];o.matrix_world=matrix.copy();o.hide_render=hidden
    for name,hidden in base_collections.items():bpy.data.collections[name].hide_render=hidden
    bpy.context.view_layer.update()
for cam,file in views:
    if requested and file not in requested:continue
    # The circulation cutaway changes wall transforms; later exterior views
    # must start from the complete saved model, never the preceding cutaway.
    restore_view_state()
    s.camera=bpy.data.objects[cam]
    for c in bpy.data.collections:c.hide_render=False
    for o in s.objects:o.hide_render=False
    for o in s.objects:
        if o.get('lift_moves'):o.location.z+=PLATFORM_SPACING*F if file=='05-raised-retrieval' else 0
    if file in ['03-garage-stored','04-pit-section','05-raised-retrieval']:
        bpy.data.collections['04 Facade | garage doors'].hide_render=True
    if file in ['04-pit-section','06-circulation']:
        for name in ['09 Roof | removable','15 Landscape | site illustration','04 Facade | garage doors','05 Entry | timber door and canopy','07 Cladding | cedar and fascia','06 Architecture | upper shell','18 Finish detail | joinery and lighting','19 Landscape | designed forecourt']:bpy.data.collections[name].hide_render=True
        for name in ['Pit front','Ground front','Garage west pier','Garage lintel','Entry left pier','Entry right pier','Entry lintel','East ground wall']:
            bpy.data.objects[name].hide_render=True
    if file!='06-circulation':
        for name in ['Fixed pedestrian cross aisle','Operator bay marking']:bpy.data.objects[name].hide_render=True
    if file=='04-pit-section':bpy.data.collections['17 Circulation | fixed floor and operator'].hide_render=True
    if file=='06-circulation':
        for c in bpy.data.collections:
            if c.name.startswith(('06 ','07 ','09 ','13 ','14 ')):c.hide_render=True
        for o in s.objects:
            if o.get('ifc_storey')=='Game room':o.hide_render=True
        # Horizontal ground-floor cut: remove upper stair flight to reveal the lobby.
        for o in bpy.data.collections['10 Stairs | protected pedestrian route'].objects:
            if 'Upper' in o.name or 'handrail' in o.name or 'baluster' in o.name:o.hide_render=True
        bpy.data.objects['Internal door head'].hide_render=True
        for name in ['Stair separation front','Stair separation rear']:
            o=bpy.data.objects[name];o.dimensions.z=3*F;o.location.z=1.5*F
        bpy.data.objects['Ground front'].hide_render=False
        for o in s.objects:
            if o.name.startswith('Front access enclosure'):o.hide_render=True
    s.render.filepath=str(OUT/(file+'.png'));bpy.ops.render.render(write_still=True)
    if file=='05-raised-retrieval':
        for o in s.objects:
            if o.get('lift_moves'):o.location.z-=PLATFORM_SPACING*F
    print('GARAGE_DRAFT_RENDERED',file,flush=True)
restore_view_state()
