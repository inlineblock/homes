"""Apply gallery cameras only to a saved scene; verify geometry stayed unchanged."""
import bpy, sys, json, hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]; HOME=ROOT/'homes/atrium-01'
sys.path.insert(0,str(Path(__file__).parent))
from design import CAMERAS,FT

def fingerprint():
    rows=[]
    for o in sorted(bpy.context.scene.objects,key=lambda o:o.name):
        if o.type=='CAMERA':continue
        row=[o.name,o.type,[list(v) for v in o.matrix_world],o.hide_render,[m.name if m else None for m in o.data.materials] if o.type=='MESH' else []]
        if o.type=='MESH':row += [[list(v.co) for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons]]
        if o.type=='LIGHT':row += [o.data.type,o.data.energy,list(o.data.color)]
        rows.append(row)
    return hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()

path=HOME/'model/gallery-validation.json'
if '--verify-gallery' in sys.argv:
    report=json.loads(path.read_text());assert fingerprint()==report['non_camera_scene_sha256']
    for name,(loc,target,lens) in CAMERAS.items():
        o=bpy.data.objects[name];assert o.type=='CAMERA' and abs(o.data.lens-lens)<.001
        assert (o.location-Vector(loc)*FT).length<.0001
    report['fresh_reopen_cameras_and_geometry_passed']=True
    path.write_text(json.dumps(report,indent=2)+'\n');print('ATRIUM_GALLERY_REOPEN_PASSED')
else:
    before=fingerprint();coll=bpy.data.collections['10 Lighting and cameras']
    for name,(loc,target,lens) in CAMERAS.items():
        o=bpy.data.objects.get(name)
        if o is None:
            o=bpy.data.objects.new(name,bpy.data.cameras.new(name));coll.objects.link(o)
        o.location=Vector(loc)*FT;o.rotation_euler=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y').to_euler();o.data.lens=lens;o.data.clip_end=500
    assert before==fingerprint()
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    path.write_text(json.dumps({'scope':'Gallery cameras only; approved geometry, materials, lighting and layout retained.','blender':bpy.app.version_string,'non_camera_scene_sha256':before,'cameras':list(CAMERAS),'non_camera_scene_unchanged':True,'fresh_reopen_cameras_and_geometry_passed':False},indent=2)+'\n')
    print('ATRIUM_GALLERY_CAMERAS_SAVED')
