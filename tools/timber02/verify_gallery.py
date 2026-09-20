"""Fresh native gallery check; deliberately does not render or hide the roof."""
import bpy,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools'),str(Path(__file__).parent)]
from gallery import VIEWS
from mathutils import Vector
HOME=ROOT/'homes/timber-courtyard-02';s=bpy.context.scene
links=[]
for lib in bpy.data.libraries:
    assert lib.filepath.startswith('//'),lib.filepath
    p=Path(bpy.path.abspath(lib.filepath)).resolve();assert p.is_file() and p.is_relative_to(ROOT/'library')
    links.append(lib.filepath)
manifest=json.loads((HOME/'project.json').read_text())
resolved={str(Path(bpy.path.abspath(lib.filepath)).resolve()) for lib in bpy.data.libraries}
for pin in manifest['asset_dependencies']:
    prefix=str((ROOT/'library'/pin['id']/pin['version']).resolve())+'/'
    assert any(path.startswith(prefix) for path in resolved),pin
area=sum(o.dimensions.x*o.dimensions.y/.3048**2 for o in s.objects if o.name.startswith('Enclosed floor'))
assert abs(area-2400)<.02
assert len([o for o in s.objects if ' bed frame' in o.name])==3
assert len([o for o in s.objects if o.name.endswith(' WC')])==3
assert all(bpy.data.objects.get(n) and bpy.data.objects[n].type=='CAMERA' for n in VIEWS)
for name,(loc,target,lens) in VIEWS.items():
    cam=bpy.data.objects[name]
    assert (cam.location-Vector(loc)*.3048).length<1e-5,name
    expected=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y')
    assert abs(abs(cam.rotation_euler.to_quaternion().dot(expected))-1)<1e-5,name
    assert abs(cam.data.lens-lens)<1e-5,name
assert not bpy.data.collections['09 Roof | hide for cutaway'].hide_render
assert not bpy.data.collections['08 Structure | cedar'].hide_render
report={'reopened_model':True,'scene_objects':len(s.objects),'measured_floor_area_sqft':round(area,2),'modeled_bedrooms':3,'modeled_bathrooms':3,'relative_libraries':links,'named_cameras':list(VIEWS),'all_camera_poses_and_lenses_match_source':True,'roof_and_structure_visible_in_saved_native':True,'status':'Current native geometry, library resolution and gallery cameras verified; kitchen operation has a separate review, remaining legacy program and engineering unresolved'}
(HOME/'model/model-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('TIMBER_GALLERY_NATIVE_VERIFIED',report,flush=True)
