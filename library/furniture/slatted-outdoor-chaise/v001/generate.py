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
ID='furniture/slatted-outdoor-chaise';NAME='Slatted timber outdoor chaise with reclining back and cushion'
coll=g.collection('Slatted outdoor chaise | shared v001')
wood=noise_material('Outdoor chaise warm timber',(.17,.095,.044),(.36,.22,.11),8,.54,.001,(3,18,.8))
fabric=noise_material('Outdoor chaise woven ivory cushion',(.60,.61,.55),(.82,.82,.74),170,.84,.0007)
metal=material('Chaise dark fitting',(.028,.032,.03),.45,.5)
for x in [-.32,.32]:
 box('Chaise longitudinal frame',(x,0,.30),(.06,1.98,.08),wood,.014)
 for y in [-.77,.72]:box('Chaise grounded leg',(x,y,.15),(.075,.075,.30),wood,.012)
for j in range(16):box('Chaise seat timber slat',(0,-.89+j*.081,.36),(.72,.064,.045),wood,.012)
box('Chaise seat cushion',(0,-.28,.415),(.65,1.27,.08),fabric,.035)
angle=math.radians(31)
# Back reclines toward +Y, with physical support beneath its slats.
for j in range(9):
 t=j*.073;y=.38+t*math.cos(angle);z=.39+t*math.sin(angle)
 o=box('Chaise back timber slat',(0,y,z),(.72,.061,.045),wood,.01);o.rotation_euler.x=angle
back=box('Chaise back cushion',(0,.67,.59),(.65,.70,.075),fabric,.035);back.rotation_euler.x=angle
for x in [-.31,.31]:
 rod('Chaise reclining support',(x,.85,.33),(x,.78,.61),.021,metal)
meta={'placement':{'origin':'Floor center XY at leg bottoms Z=0; reclining head at +Y; Z up','front_direction':'Foot/front toward -Y','allowed_variation':'Rigid placement and Z rotation only; no scaling.'},'mounting':'Four grounded legs on a level hard surface.','clearances':{'side_access_m':.6,'foot_access_m':.8,'basis':'Concept furniture access allowance; not an accessibility certification.','host_checked':False},'operating_envelope':{'state':'Fixed 31-degree recline','motion_modeled':False,'host_open_state_checked':False},'product_status':'Original furniture design; not an identified commercial product.'}

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
