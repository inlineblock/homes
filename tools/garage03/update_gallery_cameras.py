"""Add gallery cameras without regenerating approved geometry or materials.

Open the native model first. -- --verify reopens/checks the saved camera update
without saving anything. No render or temporary cutaway state is saved here.
"""
import bpy,sys,json,hashlib,array
from mathutils import Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools'),str(Path(__file__).parent)]
from common import geometry as g
from cameras import VIEWS,add_cameras
HOME=ROOT/'homes/garage-loft-03'
NATIVE=HOME/'model/garage-loft-03.blend'
RECEIPT=HOME/'model/gallery-camera-validation.json'
assert Path(bpy.data.filepath).resolve()==NATIVE.resolve(), 'Open the existing Garage Loft native model first'


def content_digest():
    h=hashlib.sha256()
    meshes=set()
    def identity(item):return (item.library.filepath if item.library else '',item.name)
    for o in sorted(bpy.data.objects,key=identity):
        if o.type=='CAMERA':continue
        record={'name':identity(o),'type':o.type,'matrix':[round(v,6) for row in o.matrix_world for v in row],
                'hide_render':o.hide_render,'hide_viewport':o.hide_viewport,
                'data':o.data.name if o.data else None,
                'materials':[slot.material.name if slot.material else None for slot in o.material_slots],
                'instance':o.instance_collection.name if o.instance_collection else None}
        h.update(json.dumps(record,sort_keys=True).encode())
        if o.type=='MESH':meshes.add(o.data)
    for mesh in sorted(meshes,key=identity):
        coords=array.array('f',[0.0])*(len(mesh.vertices)*3)
        mesh.vertices.foreach_get('co',coords)
        h.update(str(identity(mesh)).encode());h.update(coords.tobytes())
        h.update(str((len(mesh.edges),len(mesh.polygons),len(mesh.loops))).encode())
    for m in sorted(bpy.data.materials,key=identity):
        h.update(str(identity(m)).encode())
        if not m.use_nodes:continue
        for n in sorted(m.node_tree.nodes,key=lambda n:n.name):
            values=[]
            for p in n.inputs:
                if not hasattr(p,'default_value'):continue
                v=p.default_value
                try:v=[round(i,6) if isinstance(i,float) else i for i in v]
                except TypeError:pass
                if isinstance(v,float):v=round(v,6)
                if isinstance(v,(str,int,float,bool,list)):values.append([p.name,v])
            h.update(json.dumps([n.name,n.bl_idname,values],sort_keys=True).encode())
    return h.hexdigest()


before=content_digest()
if '--verify' in sys.argv:
    receipt=json.loads(RECEIPT.read_text())
    assert before==receipt['non_camera_content_sha256'], 'Non-camera content changed during save/reopen'
    assert all(name in bpy.data.objects for name,*_ in VIEWS)
    assert bpy.context.scene.camera.name==receipt['saved_default_camera']
    receipt['fresh_native_reopen_verified']=True
    RECEIPT.write_text(json.dumps(receipt,indent=2)+'\n')
    print('GARAGE_CAMERA_REOPEN_VERIFIED',len(VIEWS),flush=True)
else:
    default=bpy.context.scene.camera.name
    g.ACTIVE=bpy.data.collections['16 Lighting and cameras']
    add_cameras(only_missing=True)
    # Recompose the two new views after draft review without moving originals.
    for name,filename,loc,target,lens in VIEWS[6:]:
        o=bpy.data.objects[name];o.location=Vector(loc)*.3048
        o.rotation_euler=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y').to_euler();o.data.lens=lens
        if filename=='08-elevated-approach':o.data.type='ORTHO';o.data.ortho_scale=76*.3048
    after=content_digest()
    assert before==after, 'Only cameras may change in this operation'
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(NATIVE))
    receipt={'scope':'Camera-only gallery expansion; existing geometry, materials, lights and lift stored state preserved',
             'blender':bpy.app.version_string,'non_camera_content_sha256':after,
             'saved_default_camera':default,'named_cameras':[name for name,*_ in VIEWS],
             'non_camera_content_unchanged':True,'fresh_native_reopen_verified':False,
             'ifc':'Existing IFC retained because no building geometry changed; cameras are visualization-only.'}
    RECEIPT.write_text(json.dumps(receipt,indent=2)+'\n')
    print('GARAGE_GALLERY_CAMERAS_SAVED',len(VIEWS),flush=True)
