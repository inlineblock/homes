"""Original metric asset geometry; publish a new version rather than overwriting adoption."""
import bpy,sys,math,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT/'tools'))
from common import geometry as g
from common.geometry import material
from common.materials import noise_material
bpy.ops.wm.read_factory_settings(use_empty=True)
def box(name,loc,size,mat,bevel=0):return g.box(name,[v/.3048 for v in loc],[v/.3048 for v in size],mat,bevel/.3048)
def rod(name,a,b,r,mat):return g.rod(name,[v/.3048 for v in a],[v/.3048 for v in b],r/.3048,mat)
def mesh(name,verts,faces,mat):
 d=bpy.data.meshes.new(name);d.from_pydata(verts,[],faces);d.materials.append(mat);d.update();o=bpy.data.objects.new(name,d);g.ACTIVE.objects.link(o);return o
ID='fixtures/rectangular-pool-6x12m';NAME='Rectangular swimming pool with 6 × 12 m water footprint'
coll=g.collection('Rectangular pool 6x12m | shared v001')
plaster=noise_material('Pool pale blue plaster',(.21,.47,.55),(.46,.70,.73),75,.48,.001)
stone=noise_material('Pool ivory coping',(.54,.52,.45),(.72,.70,.63),48,.65,.001)
water=material('Pool water | IOR 1.333',(.30,.72,.80),.08)
p=water.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=.92;p.inputs['IOR'].default_value=1.333
n=water.node_tree.nodes;l=water.node_tree.links;t=n.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=38;t.inputs['Detail'].default_value=2;b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.16;b.inputs['Distance'].default_value=.018;l.new(t.outputs['Fac'],b.inputs['Height']);l.new(b.outputs['Normal'],p.inputs['Normal'])
v=n.new('ShaderNodeVolumeAbsorption');v.inputs['Color'].default_value=(.23,.65,.73,1);v.inputs['Density'].default_value=.12;l.new(v.outputs['Volume'],n.get('Material Output').inputs['Volume'])
box('Pool floor',(0,0,-1.68),(6.36,12.36,.20),plaster,.03)
for x in [-3.10,3.10]:box('Pool side shell',(x,0,-.81),(.20,12.4,1.62),plaster,.025)
for y in [-6.10,6.10]:box('Pool end shell',(0,y,-.81),(6,.20,1.62),plaster,.025)
for x in [-3.16,3.16]:box('Coping long side',(x,0,.035),(.32,12.64,.07),stone,.022)
for y in [-6.16,6.16]:box('Coping end',(0,y,.035),(6,.32,.07),stone,.022)
for i in range(4):
 h=1.38-i*.29;box('Submerged entry step %02d'%i,(-1.5,-5.775+i*.42,-1.58+h/2),(2.85,.44,h),plaster,.018)
box('Transparent water volume',(0,0,-.855),(5.998,11.998,1.45),water)
meta={'placement':{'origin':'Water footprint center XY; host deck datum Z=0. Shell reaches Z=-1.78 m. Coping top Z=0.07 m.','front_direction':'Entry steps at -Y end; long axis Y; Z up','allowed_variation':'Rigid placement and Z rotation only. Do not stretch pool geometry.'},'mounting':'Host excavates shell footprint 6.4 x 12.4 m to below -1.78 m; deck and landscape must not intersect water volume.','clearances':{'suggested_deck_clearance_m':1.5,'basis':'Concept circulation allowance; site-specific barrier, drain, equipment, structure and pool safety design unresolved.','host_checked':False},'modeled_state':'Static water, shell, coping and submerged entry steps. No operational hydraulics or diving equipment.','product_status':'Original illustrative assembly, not a commercially engineered pool.'}

bpy.context.view_layer.update()
pts=[o.matrix_world@Vector(c) for o in coll.all_objects if o.type=='MESH' for c in o.bound_box]
lo=[min(p[i] for p in pts) for i in range(3)];hi=[max(p[i] for p in pts) for i in range(3)]
coll['asset_id']=ID;coll['asset_version']='v001'
folder=Path(__file__).parent;native=folder/(ID.split('/')[-1]+'.blend')
assert not native.exists(),'Published versions are immutable; choose a new version.'
bpy.data.libraries.write(str(native),{coll},fake_user=True)
meta.update({'schema_version':1,'id':ID,'version':'v001','name':NAME,'units':'meters','dimensions_m':[round(b-a,6) for a,b in zip(lo,hi)],'bounds_m':{'min':lo,'max':hi},'dependencies':[],'source':{'kind':'original','generator':str(Path(__file__).relative_to(ROOT)),'command':'blender --background --factory-startup --python '+str(Path(__file__).relative_to(ROOT))},'license':'CC-BY-4.0','rights':'Original geometry and embedded procedural materials; attribution Homes project contributors','software':{'blender':bpy.app.version_string},'files':{'blender':native.name,'preview':'preview.png','validation':'validation.json','preview_renderer':'review.py'}})
(folder/'asset.json').write_text(json.dumps(meta,indent=2)+'\n')
print('ASSET_PUBLISHED',ID,len(coll.all_objects),meta['dimensions_m'])
