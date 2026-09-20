"""Compare protected pergola doors against a supplied earlier native model.

Blender --factory-startup --background --python tools/coastal04/verify_pergola_door.py -- /path/to/baseline.blend
Only the receipt is written; neither native source is saved.
"""
import bpy,sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HOME=ROOT/'homes/coastal-house'
FRAMES=[1,20,40,60,80,100,120]
PREFIXES=('Great room','Verandah','Pocket removable cladding skin','Linear threshold drain','Drain slot cross bridge','Rear solid pier','Shared limestone facade full panel','Limestone facade bespoke perimeter cut')
def capture(path):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    scene=bpy.context.scene
    result={}
    for frame in FRAMES:
        scene.frame_set(frame);bpy.context.view_layer.update()
        row={}
        for obj in scene.objects:
            if not obj.name.startswith(PREFIXES):continue
            item={'matrix':[[round(v,6) for v in r] for r in obj.matrix_world],'kind':obj.type,'materials':[m.name if m else None for m in getattr(obj.data,'materials',[])]}
            if obj.type=='MESH':item['vertices']=[[round(v,6) for v in vertex.co] for vertex in obj.data.vertices]
            if obj.instance_collection:item['collection']=obj.instance_collection.name
            row[obj.name]=item
        result[str(frame)]=row
    return result
baseline=Path(sys.argv[sys.argv.index('--')+1]).resolve()
current=HOME/'model/coastal-house.blend'
assert hashlib.sha256(baseline.read_bytes()).hexdigest()=='a756a73244ffad0c723389a411a6f43aa104298b188a1f7d3a8f2fe8a1b519ce', 'Baseline must be the native file from commit 8062ca6'
a=capture(baseline);b=capture(current)
assert a==b,'Protected door/pergola geometry or materials changed'
receipt={'baseline_native_sha256':hashlib.sha256(baseline.read_bytes()).hexdigest(),'current_native_sha256':hashlib.sha256(current.read_bytes()).hexdigest(),'baseline_revision':'8062ca646412ed79eebd4588a22aaa0176602f69','sampled_frames':FRAMES,'protected_objects_per_frame':len(b['1']),'geometry_transforms_materials_identical':True,'scope':'Retractable pergola door components, tracks, pocket skins, surrounding limestone, drain and pergola; geometric comparison, not product or structural approval.'}
(HOME/'model/pergola-door-validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PERGOLA_DOOR_UNCHANGED',len(b['1']),'objects across',len(FRAMES),'frames')
