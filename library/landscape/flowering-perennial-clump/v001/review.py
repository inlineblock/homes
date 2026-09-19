"""Fresh-link validation and actual native preview; Cycles CPU only."""
import bpy,json,sys,math
from pathlib import Path
from mathutils import Vector
folder=Path(__file__).parent;meta=json.loads((folder/'asset.json').read_text())
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(folder/meta['files']['blender']),link=True) as (a,b):b.collections=[a.collections[0]]
coll=b.collections[0];bpy.context.scene.collection.children.link(coll)
bpy.context.view_layer.update();pts=[o.matrix_world@Vector(c) for o in coll.all_objects if o.type=='MESH' for c in o.bound_box]
lo=[min(p[i] for p in pts) for i in range(3)];hi=[max(p[i] for p in pts) for i in range(3)];dims=[b-a for a,b in zip(lo,hi)]
assert all(abs(a-b)<.00001 for a,b in zip(dims,meta['dimensions_m']))
assert all(o.data.materials and all(m is not None for m in o.data.materials) for o in coll.all_objects if o.type=='MESH')
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.use_denoising=True;s.render.resolution_x=700;s.render.resolution_y=560;s.render.resolution_percentage=100
s.world=bpy.data.worlds.new('Preview world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.55,.63,.70,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.7
extent=max(dims[:2]);target=Vector((0,0,(lo[2]+hi[2])/2));pos=Vector((extent*.94,-extent*1.14,extent*.95))
data=bpy.data.cameras.new('Preview');o=bpy.data.objects.new('Preview',data);s.collection.objects.link(o);o.location=pos;data.type='ORTHO';data.ortho_scale=max(extent,dims[2])*1.75;o.rotation_euler=(target-pos).to_track_quat('-Z','Y').to_euler();s.camera=o
ld=bpy.data.lights.new('Soft daylight','AREA');ld.energy=45*extent**2;ld.shape='DISK';ld.size=extent*.9;light=bpy.data.objects.new('Soft daylight',ld);s.collection.objects.link(light);light.location=(extent*.2,-extent*.4,extent*1.6)
s.view_settings.view_transform='AgX';s.render.filepath=str(folder/'preview.png');s.render.image_settings.file_format='PNG';bpy.ops.render.render(write_still=True)
report={'fresh_process_link':True,'software':bpy.app.version_string,'collection':coll.name,'mesh_objects':len([o for o in coll.all_objects if o.type=='MESH']),'measured_dimensions_m':dims,'bounds_m':{'min':lo,'max':hi},'dimensions_match_manifest':True,'materials_resolve':True,'native_preview_rendered':True,'preview_pixels_reviewed':False,'host_integration_checked':False}
(folder/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('ASSET_REOPENED',meta['id'])
