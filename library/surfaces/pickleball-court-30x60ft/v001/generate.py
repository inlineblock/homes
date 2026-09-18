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
ID='surfaces/pickleball-court-30x60ft';NAME='Pickleball court on 30 × 60 foot surface'
coll=g.collection('Pickleball court 30x60ft | shared v001')
base=noise_material('Court warm perimeter asphalt',(.21,.22,.20),(.31,.32,.29),110,.88,.0008)
blue=noise_material('Court blue acrylic',(.025,.21,.37),(.055,.30,.46),130,.85,.0003)
lightblue=material('Court non volley blue',(.065,.34,.50),.83)
white=material('Court white lines',(.85,.87,.84),.6);black=material('Net black powder coat',(.025,.032,.029),.46,.38)
box('Full playing surface',(0,0,-.065),(18.288,9.144,.13),base,.015)
box('Marked court blue',(0,0,.002),(13.4112,6.096,.004),blue)
box('Non volley central zone',(0,0,.006),(4.2672,6.096,.003),lightblue)
for x in [-6.6802,-2.1082,2.1082,6.6802]:box('Court cross line',(x,0,.012),(.0508,6.096,.004),white)
for y in [-3.0226,3.0226]:box('Court side line',(0,y,.012),(13.4112,.0508,.004),white)
for x in [-4.4196,4.4196]:box('Service center line',(x,0,.013),(4.572,.0508,.004),white)
for y in [-3.38,3.38]:rod('Net post',(0,y,.015),(0,y,1.04),.037,black)
# Physical open mesh strands; midpoint net tape dips to 34 in.
for i in range(137):
 y=-3.35+i*6.70/136;top=.8636+.0508*(abs(y)/3.35)**2
 rod('Net vertical mesh',(0,y,.07),(0,y,top),.0012,black)
for z in [.07+i*.046 for i in range(18)]:rod('Net horizontal mesh',(0,-3.35,z),(0,3.35,z),.0012,black)
for i in range(30):
 ya=-3.35+i*6.7/30;yb=ya+6.7/30
 za=.8636+.0508*(abs(ya)/3.35)**2;zb=.8636+.0508*(abs(yb)/3.35)**2
 rod('Net white top tape',(0,ya,za),(0,yb,zb),.018,white)
meta={'placement':{'origin':'Center of play XY; finished playing surface datum Z=0; long axis X and net along Y; Z up.','front_direction':'Symmetrical; long axis X','allowed_variation':'Rigid placement and Z rotation only; no scaling.'},'mounting':'Level prepared base, drainage and perimeter fencing by host.','clearances':{'marked_court_m':[13.4112,6.096],'surface_m':[18.288,9.144],'basis':'USA Pickleball construction guide: 20x44 ft court, 30x60 ft recommended minimum playing surface.','reference_url':'https://usapickleball.org/construction/','host_checked':False},'modeled_state':'Static net and surface lines; no tested sports coating or lighting design.','product_status':'Original illustrative assembly; geometry dimensions do not certify an installed sports facility.'}

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
