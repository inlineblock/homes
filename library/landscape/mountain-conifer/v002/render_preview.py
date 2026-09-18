import bpy,sys,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[4];sys.path.insert(0,str(R/'tools'))
from common import geometry as g
from common.library import linked_collection,instance
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
g.collection('Asset preview stage');c=linked_collection(R,'landscape','mountain-conifer','v002');instance('Original v002 fir',c,(0,0,0))
for o in c.objects:assert len(o.data.polygons)>0
assert not any(i.filepath for i in bpy.data.images if i.source=='FILE')
assert not any(l.library for l in bpy.data.libraries)
folder=R/'library/landscape/mountain-conifer/v002'
report={'fresh_reopen':True,'mesh_objects':len(c.objects),'mesh_faces':sum(len(o.data.polygons) for o in c.objects),'dependencies':[],'blender':bpy.app.version_string,'ground_origin_m':0}
(folder/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
g.box('Neutral preview floor',(0,0,-.10),(200,200,.20),g.material('Neutral warm ground',(.18,.19,.15),.95))
g.camera('Whole tree portrait',(64,-91,34),(0,0,22),54)
s=bpy.context.scene;s.camera=bpy.data.objects['Whole tree portrait'];s.world.use_nodes=True
n=s.world.node_tree.nodes;l=s.world.node_tree.links;sky=n.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_elevation=math.radians(35);sky.sun_rotation=math.radians(130);l.new(sky.outputs[0],n.get('Background').inputs['Color']);n.get('Background').inputs['Strength'].default_value=.4
s.render.engine='CYCLES';s.cycles.samples=48;s.cycles.use_denoising=True;s.render.resolution_x=1100;s.render.resolution_y=1400;s.render.resolution_percentage=100;s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=-.2
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.render.filepath=str(folder/'preview.png');bpy.ops.render.render(write_still=True)
print('FRESH_REOPEN_AND_PREVIEW_OK',report,flush=True)
