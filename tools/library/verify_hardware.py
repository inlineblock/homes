"""Fresh-process native, geometry and scale audit; optional CPU studio previews."""
import json
import sys
from pathlib import Path
import bpy
import bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from common import geometry as g
from common.hardware_assets import CATALOG, _bounds

render='--render' in sys.argv
results=[]
for (kind,finish),(category,slug,version) in CATALOG.items():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    folder=ROOT/'library'/category/slug/version
    metadata=json.loads((folder/'asset.json').read_text())
    native=folder/metadata['files']['blender']
    with bpy.data.libraries.load(str(native),link=True) as (src,dst):
        assert len(src.collections)==1,(slug,src.collections)
        dst.collections=[src.collections[0]]
    coll=dst.collections[0]
    bpy.context.scene.collection.children.link(coll)
    lo,hi=_bounds(coll)
    dimensions=[hi[i]-lo[i] for i in range(3)]
    assert all(abs(dimensions[i]-metadata['dimensions_m'][i])<.00001 for i in range(3)),slug
    assert metadata['dependencies']==[],slug
    meshes=[]
    for obj in coll.all_objects:
        assert obj.type=='MESH',(slug,obj.name)
        assert obj.data.materials and obj.data.materials[0],(slug,obj.name)
        mesh=bmesh.new(); mesh.from_mesh(obj.data)
        assert all(edge.is_manifold for edge in mesh.edges),(slug,obj.name,'non-manifold')
        assert mesh.calc_volume()>0,(slug,obj.name,'non-positive volume')
        mesh.free()
        meshes.append(obj.name)
    assert all(abs(obj.scale[i]-1)<.00001 for obj in coll.all_objects for i in range(3)),slug
    assert hi[1] <= (.017 if kind in ['edge-pull','flush-pull'] else .00001), (slug,hi)
    if render:
        stage=g.collection('Preview studio — excluded from published asset')
        scene=bpy.context.scene
        scene.render.engine='CYCLES';scene.cycles.device='CPU'
        scene.cycles.samples=32;scene.cycles.use_denoising=True
        scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
        scene.world=bpy.data.worlds.new('Hardware studio world');scene.world.use_nodes=True
        scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.18,.20,.23,1)
        scene.world.node_tree.nodes['Background'].inputs[1].default_value=.45
        scene.view_settings.view_transform='AgX'
        mid=Vector([(hi[i]+lo[i])/2/g.F for i in range(3)])
        span=max(dimensions)/g.F
        floor=g.material('Preview floor',(.17,.19,.20),.8)
        g.box('Studio floor',(mid.x,0,lo[2]/g.F-.03),(span*12,span*12,.02),floor)
        camera=g.camera('Hardware preview',(mid.x+span*1.15,mid.y-span*2.8,mid.z+span*.9),mid,65)
        camera.data.type='ORTHO';camera.data.ortho_scale=span*g.F*1.65;camera.data.clip_start=.0005
        scene.camera=camera
        # Tiny real objects need correspondingly restrained light power.
        g.area('Large soft key',(mid.x-span,mid.y-span*1.8,mid.z+span*2),mid,4*(span/.5)**2,span*2,(1,.90,.77))
        g.area('Cool edge',(mid.x+span*1.8,mid.y+span*.4,mid.z+span*1.5),mid,3*(span/.5)**2,span*1.4,(.75,.86,1))
        scene.render.filepath=str(folder/'preview.png')
        scene.render.image_settings.file_format='PNG'
        bpy.ops.render.render(write_still=True)
    results.append({'id':metadata['id'],'version':version,'dimensions_m':dimensions,'mesh_count':len(meshes),'closed_positive_volume_meshes':True,'fresh_link_verified':True,'preview_exists':(folder/'preview.png').exists()})
(ROOT/'tools/library/hardware-validation.json').write_text(json.dumps({'blender':bpy.app.version_string,'asset_count':len(results),'validation':results},indent=2)+'\n')
print('HARDWARE_VERIFIED',len(results))
