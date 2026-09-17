import bpy,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HOME=ROOT/'homes/timber-courtyard-02';s=bpy.context.scene
links=[]
for lib in bpy.data.libraries:
    assert lib.filepath.startswith('//'),lib.filepath
    assert Path(bpy.path.abspath(lib.filepath)).is_file(),lib.filepath
    links.append(lib.filepath)
assert len(links)==5,links
floor_area=sum(o.dimensions.x*o.dimensions.y/(.3048**2) for o in s.objects if o.name.startswith('Enclosed floor'))
assert abs(floor_area-2400)<.02,floor_area
bed_count=len([o for o in s.objects if ' bed frame' in o.name]);bath_count=len([o for o in s.objects if o.name.endswith(' WC')]);assert bed_count==3 and bath_count==3
report={'reopened_model':True,'scene_objects':len(s.objects),'measured_floor_area_sqft':round(floor_area,2),'modeled_bedrooms':bed_count,'modeled_bathrooms':bath_count,'relative_libraries':links,'status':'Concept geometry verified; architectural engineering unverified'}
(HOME/'model/model-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('TIMBER_VERIFIED',report,flush=True)
try:
    p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
    for d in p.devices:d.use=d.type=='METAL'
    s.cycles.device='GPU'
except Exception:pass
s.cycles.samples=96
for camera,file,cutaway in [('02 Elevated courtyard','02-elevated',False),('03 Garden threshold','03-garden-entry',False),('04 Plan cutaway','04-model-plan',True)]:
    s.camera=bpy.data.objects[camera]
    bpy.data.collections['09 Roof | hide for cutaway'].hide_render=cutaway;bpy.data.collections['08 Structure | cedar'].hide_render=cutaway
    if cutaway:
        s.camera.data.type='ORTHO';s.camera.data.ortho_scale=74*.3048;s.render.resolution_x=1600;s.render.resolution_y=1400
    s.render.filepath=str(HOME/'renders'/f'{file}.png');bpy.ops.render.render(write_still=True);print('RENDER_SAVED',file,flush=True)
