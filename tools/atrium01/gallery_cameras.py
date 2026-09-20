"""Read-only fresh native camera check; build.py applies cameras.py definitions."""
import bpy, sys, json, hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]; HOME=ROOT/'homes/atrium-01'
sys.path.insert(0,str(Path(__file__).parent))
from cameras import CAMERAS
from design import FT
native=HOME/'model/atrium-01.blend'
assert Path(bpy.data.filepath).resolve()==native.resolve()
checks=[]
for name,(loc,target,lens) in CAMERAS.items():
    obj=bpy.data.objects[name]
    assert obj.type=='CAMERA' and abs(obj.data.lens-lens)<.001
    assert (obj.location-Vector(loc)*FT).length<.0001
    direction=(Vector(target)-Vector(loc)).normalized()
    actual=obj.rotation_euler.to_matrix()@Vector((0,0,-1))
    assert (actual-direction).length<.0001
    checks.append({'name':name,'location_m':list(obj.location),'lens_mm':obj.data.lens})
receipt={'scope':'Fresh read-only camera check of the coordinated architectural revision.',
'blender_version':bpy.app.version_string,'source_blend_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),
'fresh_reopen_cameras_passed':True,'cameras':checks,
'render_state_exceptions':{'04-cutaway':'Roof and principal structure hidden for plan visibility; never saved.',
'14-primary-privacy':'Paired opaque bedroom shade collections lowered; never saved.'}}
(HOME/'model/gallery-validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('ATRIUM_GALLERY_REOPEN_PASSED',len(checks))
