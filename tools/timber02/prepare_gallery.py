"""Add the gallery cameras without rebuilding or changing the approved design."""
import bpy,sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools'),str(Path(__file__).parent)]
from gallery import install_new_cameras,VIEWS
HOME=ROOT/'homes/timber-courtyard-02'

def design_digest():
    h=hashlib.sha256()
    for o in sorted(bpy.context.scene.objects,key=lambda o:o.name):
        if o.type=='CAMERA':continue
        h.update(str((o.name,o.type,[tuple(v) for v in o.matrix_world],o.hide_render)).encode())
        if o.type=='MESH':
            h.update(str([tuple(v.co) for v in o.data.vertices]).encode());h.update(str([tuple(p.vertices) for p in o.data.polygons]).encode())
        if o.type=='LIGHT':h.update(str((o.data.type,o.data.energy,tuple(o.data.color))).encode())
        h.update(str([s.material.name if s.material else None for s in o.material_slots]).encode())
    return h.hexdigest()

before=design_digest();install_new_cameras();after=design_digest();assert before==after
assert all(bpy.data.objects.get(n) and bpy.data.objects[n].type=='CAMERA' for n in VIEWS)
bpy.ops.wm.save_as_mainfile(filepath=str(HOME/'model/timber-courtyard-02.blend'))
(HOME/'model/gallery-camera-validation.json').write_text(json.dumps({'software':bpy.app.version_string,'camera_count':len(VIEWS),'named_cameras':list(VIEWS),'noncamera_design_hash_before':before,'noncamera_design_hash_after':after,'approved_non_camera_scene_unchanged':True,'scope':'Cameras only: existing mesh geometry, transforms, effective material assignments, lights and render visibility unchanged. Interior remains schematic; this is not a renewed whole-home program review.'},indent=2)+'\n')
print('TIMBER_GALLERY_CAMERAS_SAVED',list(VIEWS),flush=True)
