"""Original reusable kitchen sink options with true bowls, drain bores and shared faucet.

blender -b --factory-startup --python tools/library/publish_kitchen_sink_options.py
blender -b --factory-startup --python tools/library/publish_kitchen_sink_options.py -- --verify --render
--asset <slug> selects one; all previews use CPU. No home mutation.
"""
from pathlib import Path
import bpy,json,math,sys,hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'tools/library')]
from common import geometry as g
from common.library import linked_collection
from publish_modern_block import box,linked_mat
GEN='tools/library/publish_kitchen_sink_options.py';FAUCET='kitchen-pull-down-mixer-315'
SPECS={
 'wide-undermount-sink-800':{'name':'Wide stainless undermount sink800','w':.800,'d':.450,'depth':.240,'flange':.025,'faucet_y':.285,'cabinet':.9144,'cutout':[.810,.460],'kind':'under'},
 'workstation-sink-860':{'name':'Stainless workstation sink860','w':.860,'d':.450,'depth':.250,'flange':.025,'faucet_y':.285,'cabinet':1.0668,'cutout':[.870,.460],'kind':'workstation'},
 'white-apron-front-sink-32in':{'name':'White glazed apron front sink32in','w':.7428,'d':.4288,'depth':.255,'flange':.035,'faucet_y':.310,'cabinet':.9144,'cutout':[.7528,.4388],'kind':'apron'},
 'compact-prep-sink-400':{'name':'Compact stainless prep sink400','w':.400,'d':.350,'depth':.200,'flange':.025,'faucet_y':.255,'cabinet':.6096,'cutout':[.410,.360],'kind':'prep'},
}
def folder(slug):return ROOT/'library/fixtures'/slug/'v001'
def native(slug):return folder(slug)/(slug+'.blend')
def cname(slug):return ('Shared pull-down kitchen mixer315' if slug==FAUCET else SPECS[slug]['name'])+' | v001'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cylinder(name,loc,r,d,mat):return g.cyl(name,Vector(loc)/g.F,r/g.F,d/g.F,mat,64)
def rod(name,a,b,r,mat):return g.rod(name,Vector(a)/g.F,Vector(b)/g.F,r/g.F,mat)
def mesh(name,verts,faces,mat):
 d=bpy.data.meshes.new(name);d.from_pydata(verts,[],faces);d.update();d.materials.append(mat);o=bpy.data.objects.new(name,d);g.ACTIVE.objects.link(o);return o

def rounds(w,d,r,z,n=8):
 out=[]
 for k,(cx,cy) in enumerate([(w/2-r,d/2-r),(-w/2+r,d/2-r),(-w/2+r,-d/2+r),(w/2-r,-d/2+r)]):
  for i in range(n):a=(k+i/n)*math.pi/2;out.append((cx+r*math.cos(a),cy+r*math.sin(a),z))
 return out

def loop_mesh(name,loops,mat,close=True):
 n=len(loops[0]);faces=[]
 for k in range(len(loops)-1+(1 if close else 0)):
  q=(k+1)%len(loops)
  for i in range(n):faces.append((k*n+i,k*n+(i+1)%n,q*n+(i+1)%n,q*n+i))
 o=mesh(name,[p for loop in loops for p in loop],faces,mat);be=o.modifiers.new('Soft formed edges','BEVEL');be.width=.0007;be.segments=2;o.modifiers.new('Balanced surface normals','WEIGHTED_NORMAL');return o

def bowl(spec,mat):
 w,d,depth,f=spec['w'],spec['d'],spec['depth'],spec['flange'];z=-.0381;t=.003;r=.020;N=32
 circ=lambda radius,zz:[(radius*math.cos(i*math.tau/N),radius*math.sin(i*math.tau/N),zz) for i in range(N)]
 loops=[rounds(w,d,r,z),rounds(w-.05,d-.05,.025,z-depth+.012),circ(.045,z-depth),circ(.045,z-depth-t),rounds(w-.044,d-.044,.028,z-depth+.012-t),rounds(w+.006,d+.006,r+.003,z-t),rounds(w+2*f,d+2*f,.025,z-t),rounds(w+2*f,d+2*f,.025,z)]
 o=loop_mesh('True open sink bowl and flange',loops,mat);o['actual_drain_hole_diameter_m']=.090;o['no_solid_bottom_cap']=True
 # Annular basket reduction and tailpiece keep an actual uninterrupted drain bore.
 drainloops=[circ(.045,z-depth),circ(.046,z-depth-.012),circ(.022,z-depth-.064),circ(.022,z-depth-.110),circ(.018,z-depth-.110),circ(.018,z-depth-.064),circ(.042,z-depth-.012)]
 loop_mesh('Hollow drain basket and tailpiece',drainloops,mat)
 return o

def full_bounds(c):
 pts=[]
 def walk(coll,matrix):
  for o in coll.objects:
   transform=matrix@o.matrix_world
   if o.type in ['MESH','CURVE','FONT']:pts.extend(transform@Vector(v) for v in o.bound_box)
   if o.instance_type=='COLLECTION' and o.instance_collection:walk(o.instance_collection,transform)
 from mathutils import Matrix
 bpy.context.view_layer.update();walk(c,Matrix.Identity(4));return [min(p[i] for p in pts) for i in range(3)],[max(p[i] for p in pts) for i in range(3)]

def add_faucet(y):
 c=linked_collection(ROOT,'fixtures',FAUCET);o=bpy.data.objects.new('Pinned shared pull-down mixer',None);o.instance_type='COLLECTION';o.instance_collection=c;g.ACTIVE.objects.link(o);o.location=(0,y,0);o['shared_asset_id']='fixtures/'+FAUCET;o['shared_asset_version']='v001';return o

def publish_faucet():
 if native(FAUCET).exists():print('PRESERVE',FAUCET);return
 bpy.ops.wm.read_factory_settings(use_empty=True);parent=ROOT/'library/fixtures/kitchen-sink-mixer-650/v002/kitchen-sink-mixer-650.blend'
 with bpy.data.libraries.load(str(parent),link=False) as (src,dst):dst.collections=['Stainless sink and mixer']
 c=dst.collections[0];bpy.context.scene.collection.children.link(c);g.ACTIVE=c
 for o in list(c.all_objects):
  if o.name.startswith(('High arch kitchen mixer','Mixer lever')):o.location.y-=.285
  else:bpy.data.objects.remove(o,do_unlink=True)
 steel=c.all_objects[0].data.materials[0];dark=g.material('Mixer outlet and cartridge dark insert',(.025,.03,.03),.4)
 cylinder('Mixer single mounting body',(0,0,.045),.035,.09,steel)
 cylinder('Mixer deck mounting escutcheon',(0,0,.003),.042,.006,steel)
 cylinder('Mixer mounting stem',(0,0,-.0375),.0125,.075,steel)
 cylinder('Mixer under-counter securing nut',(0,0,-.060),.022,.012,steel)
 rod('Mixer integral lever valve arm',(0,0,.055),(.08,0,.055),.018,steel)
 cylinder('Separate pull-down spray head',(0,-.315,.256),.020,.048,steel)
 cylinder('Spray outlet inset',(0,-.315,.231),.016,.002,dark)
 c.name=cname(FAUCET);c['asset_id']='fixtures/'+FAUCET;c['asset_version']='v001';lo,hi=full_bounds(c);folder(FAUCET).mkdir(parents=True,exist_ok=True);bpy.data.libraries.write(str(native(FAUCET)),{c},fake_user=True,path_remap='RELATIVE_ALL')
 meta=base_meta(FAUCET,lo,hi,[]);meta.update({'derived_from':{'id':'fixtures/kitchen-sink-mixer-650','version':'v002','native_sha256':sha(parent),'method':'Append the actual published arch and lever geometry only; normalize base to XY0 and retain original steel material. Add integrated valve arm/body, mounting stem/nut and distinct pull-down head. No source asset mutation.'},'placement':{'origin':'Faucet deck mounting center XY0, finished countertop top Z0','front_direction':'Spout aims -Y; Z up','allowed_scaling':'Rigid placement/rotation only; do not stretch spout reach or mounting hardware'},'installation':{'mounting':'Single35mm conceptual deck bore at XY0; supports a38.1mm countertop in example installs. Stem extends75mm below top; nut envelope44mm diameter atZ-60mm. Selected faucet/product tolerances still govern.','faucet_hole_diameter_m':.035,'spout_projection_from_base_m':.315,'spray_outlet_z_m':.230,'rear_body_clearance_m':.050,'below_counter_clearance_m':.150,'operating_envelope':{'modeled_state':'Static docked spray head; no articulated hose','concept_pullout_reach_m':.450,'lever_clearance_right_m':.120,'basis':'Original conceptual geometry, not a rated extension or manufacturer installation spec','host_checked':False}},'limitations':'Original generic pull-down mixer concept. Hose, counterweight, connectors, cartridge and product performance are unresolved; reserve service space. No certified water-flow or compliance claim.'})
 (folder(FAUCET)/'asset.json').write_text(json.dumps(meta,indent=2)+'\n');print('PUBLISHED',FAUCET,flush=True)

def base_meta(slug,lo,hi,deps):
 return {'schema_version':1,'id':'fixtures/'+slug,'version':'v001','name':cname(slug),'units':'meters','dimensions_m':[hi[i]-lo[i] for i in range(3)],'bounds_m':{'min':lo,'max':hi},'blender':{'collection':cname(slug)},'dependencies':deps,'license':'CC-BY-4.0','rights':'Original Homes project contributors geometry and procedural finishes; attribution Homes project contributors. No third-party product CAD, photographs or commercial specification.','source':{'kind':'original','generator':GEN,'command':'blender -b --factory-startup --python '+GEN+' -- --asset '+slug},'software':{'blender':bpy.app.version_string},'files':{'blender':slug+'.blend','preview':'preview.png','validation':'validation.json'}}

def publish_sink(slug):
 if native(slug).exists():print('PRESERVE',slug);return
 bpy.ops.wm.read_factory_settings(use_empty=True);s=SPECS[slug];c=g.collection(cname(slug));c['asset_id']='fixtures/'+slug;c['asset_version']='v001'
 # Source steel finish is already shared with the pinned mixer; ceramic remains original fixture finish.
 faucetcol=linked_collection(ROOT,'fixtures',FAUCET)
 steel=next(m for o in faucetcol.all_objects if hasattr(o.data,'materials') for m in o.data.materials if m and 'stainless' in m.name.lower())
 ceramic=g.material('Original soft white glazed sink ceramic',(.74,.73,.68),.20)
 mat=ceramic if s['kind']=='apron' else steel;bowl(s,mat);add_faucet(s['faucet_y'])
 deps=[{'id':'fixtures/'+FAUCET,'version':'v001','path':'../../'+FAUCET+'/v001/'+FAUCET+'.blend'}]
 if s['kind']=='apron':
  # Distinct visible apron has rounded external corners, not an opaque insert inside the bowl.
  box('Rounded exposed apron front',(0,-.260,-.162),(.8128,.076,.300),ceramic,.014)
 if s['kind']=='workstation':
  for y in [-.204,.204]:box('Workstation accessory ledge',(0,y,-.063),(.828,.035,.012),steel,.003)
  oak=linked_mat('coastal-white-oak');deps.append({'id':'materials/coastal-white-oak','version':'v001','path':'../../../materials/coastal-white-oak/v001/coastal-white-oak.blend'})
  board=box('Removable sliding cutting board',(-.242,0,-.0445),(.310,.438,.025),oak,.006);board['removable_accessory']=True;board['allowed_slide_axis']='X';board['accessory_support_plane_z_m']=-.057
  from common.timber_materials import grain_uv
  grain_uv(board)
  # Right-side removable open roll mat, actual spaced rods; center bowl remains visible.
  for i in range(11):o=rod('Removable workstation roll mat rod',(.165+i*.022,-.213,-.048),(.165+i*.022,.213,-.048),.004,steel);o['removable_accessory']=True
 lo,hi=full_bounds(c);folder(slug).mkdir(parents=True,exist_ok=True);bpy.data.libraries.write(str(native(slug)),{c},fake_user=True,path_remap='RELATIVE_ALL')
 meta=base_meta(slug,lo,hi,deps);kind=s['kind'];rim=[s['w']+2*s['flange'],s['d']+2*s['flange']]
 compatible=None # Existing 36in base fails the wider flange/upper-rail interface at this offset.
 meta.update({'placement':{'origin':'Bowl center XY0, finished countertop top Z0; flange is38.1mm below top','front_direction':'-Y; faucet behind bowl at+Y; Z up','allowed_scaling':'Rigid placement/rotation only. These are38.1mm-countertop studies; use separate sink/faucet placements or publish a thickness variant for another worktop.'},'bowl':{'inner_top_opening_m':[s['w'],s['d']],'inner_depth_m':s['depth'],'flange_outer_m':rim,'flange_top_z_m':-.0381,'formed_wall_thickness_m':.003,'true_drain_bore_m':.090,'tailpiece_inner_bore_m':.036,'surface_note':'Original glazed appearance over modeled shell; no fireclay product/wall-thickness performance claim' if kind=='apron' else 'Original formed stainless appearance; gauge and fabrication unselected'},'installation':{'countertop_thickness_m':.0381,'countertop_cutout_m':s['cutout'],'cutout_center_xy_m':[0,0],'apron_cutout_plan_m':{'rear_edge_y':.2194,'side_edges_x':[-.3764,.3764],'widen_at_y':-.2144,'front_throat_edges_x':[-.4114,.4114],'front_throat':'Continue to actual front counter edge; preserve 5mm apron side seam and specified flexible seal. Host dimensions remain unapproved.'} if kind=='apron' else None,'cutout_type':'U-shaped open to front edge, independently supported apron sink' if kind=='apron' else 'Rounded rectangular through-opening,5mm positive reveal per side relative to inner bowl','concept_cutout_corner_radius_m':.025,'faucet_hole_centers_m':[[0,s['faucet_y']]],'faucet_hole_diameter_m':.035,'nominal_minimum_sink_base_width_m':s['cabinet'],'required_clear_width_m':rim[0]+.020,'cabinet_origin_relative_bowl_xy_m':[0,.045],'recommended_counter_depth_m':.780,'example_countertop_center_xy_m':[0,.050],'mounting':'Independent apron support cradle and matching lowered/open front rail required; no compatible apron cabinet is currently provided by this package.' if kind=='apron' else 'Continuous sealed underside support plus selected brackets. Preserve actual bowl/flange clearance and plumbing access; no solid shelf or drawer behind bowl.','compatible_existing_cabinet_candidate':compatible,'host_fit_status':'No compatible cabinet supplied. Nominal width is a planning minimum only; provide the clear rim/bowl volume and services. Existing smoked-oak 36in sink base was rejected for the wide sink because its upper front rail conflicts at the proposed offset. No home adoption.','operating_envelope':{'modeled_state':'Open bowl with docked faucet'+('; removable board left and roll mat right' if kind=='workstation' else ''),'reserve_front_standing_m':.80,'faucet_lever_clearance_right_m':.120,'basis':'Concept geometry/standing assumptions, not accessibility or manufacturer approval','host_checked':False},'service_requirements':['Provide supported worktop openings, sound waterproof sealing, drainage/trap and hot/cold services with removable access.','Drain tailpiece is modeled hollow; trap and functioning plumbing are not included.','Check faucet stem/nut and hose/weight against cabinet rails, disposal and service routes.','Select actual sink, faucet and countertop manufacturer templates before fabrication.']},'accessories':{'board':'Removable310×438×25mm original oak board supported by actual ledges; keep it out for large pots or cleaning','mat':'Removable spaced stainless rod mat; no food-contact or load rating claimed'} if kind=='workstation' else None,'limitations':'Original sink concept; heat, chemical, stain, food-contact, wet-area, fabrication and plumbing suitability remain unverified until products and installation are specified.'})
 meta['installation']['host_keepout_m']={'flange_xy':rim,'flange_z':[-.0411,-.0381],'bowl_depth_below_flange':s['depth']+.003,'minimum_width_clearance_each_side':.010,'instruction':'Keep cabinet rails out of this flange envelope and the sloping bowl shell below it. Keep stem/nut/hose service envelope clear separately; supplied studio supports do not validate cabinet manufacture.'}
 (folder(slug)/'asset.json').write_text(json.dumps(meta,indent=2)+'\n');print('PUBLISHED',slug,meta['dimensions_m'],flush=True)

def rounded_cutter(name,w,d,zcenter,depth,r):
 pts=rounds(w,d,r,zcenter-depth/2);top=rounds(w,d,r,zcenter+depth/2);n=len(pts);faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];return mesh(name,pts+top,faces,g.material('Temporary cutout material',(.2,.2,.2)))
def subtract(obj,cutter):
 bpy.context.view_layer.objects.active=obj;m=obj.modifiers.new('Actual countertop opening','BOOLEAN');m.operation='DIFFERENCE';m.object=cutter;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(cutter,do_unlink=True)

def preview(slug):
 g.collection('Sink preview installation studio only');stone=linked_mat('coastal-honed-limestone');floor=g.material('Neutral sink studio',(.24,.25,.23),.9);box('Studio floor',(0,0,-1),(100,100,.10),floor)
 if slug==FAUCET:
  top=box('Example38mm drilled countertop',(0,-.10,-.01905),(.70,.78,.0381),stone,.001)
  cutter=cylinder('Actual35mm faucet mounting hole',(0,0,-.02),.0175,.15,floor);subtract(top,cutter);target=Vector((0,-.10,.14));pos=Vector((.9,-1.1,.75))
 else:
  s=SPECS[slug];w=s['cabinet']+.12;depth=.78;cy=.05
  top=box('Example38mm countertop with true openings',(0,cy,-.01905),(w,depth,.0381),stone,.001)
  cw,cd=s['cutout'];cut=rounded_cutter('Actual shaped sink opening',cw,cd,0,.20,.025)
  if s['kind']=='apron':
   bpy.data.objects.remove(cut,do_unlink=True)
   # Stepped opening: inner bowl reveal at rear/sides, wider throat only at exposed apron.
   xy=[(-.4114,-.60),(.4114,-.60),(.4114,-.2144),(.3764,-.2144),(.3764,.2194),(-.3764,.2194),(-.3764,-.2144),(-.4114,-.2144)]
   n=len(xy);verts=[(x,y,z) for z in [-.10,.10] for x,y in xy];faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
   cut=mesh('Actual stepped apron sink opening',verts,faces,floor)
  subtract(top,cut);cut=cylinder('Actual35mm faucet bore',(0,s['faucet_y'],-.02),.0175,.15,floor);subtract(top,cut)
  # Simple open studio support keeps underside visible; never implies a supplied cabinet.
  for x in [-w/2+.03,w/2-.03]:box('Studio open display support',(x,.05,-.47),(.035,depth-.06,.86),floor,.002)
  target=Vector((0,0,-.03));pos=Vector((1.25,-1.4,1.3))
 s=bpy.context.scene;s.camera=g.camera('Actual native sink installation preview',pos/g.F,target/g.F,50)
 g.area('Sink soft key',Vector((-2,-2,3))/g.F,target/g.F,800,2.8/g.F,(1,.98,.94));g.area('Sink soft fill',Vector((2,1,2))/g.F,target/g.F,450,2/g.F,(.94,.97,1))
 s.world=bpy.data.worlds.new('Sink studio world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45
 s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=32;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=3;s.render.resolution_x=1000;s.render.resolution_y=800;s.render.resolution_percentage=100;s.view_settings.view_transform='AgX';s.render.image_settings.file_format='PNG';s.render.filepath=str(folder(slug)/'preview.png');bpy.ops.render.render(write_still=True)

def verify(slug,render):
 p=native(slug);before=sha(p);bpy.ops.wm.open_mainfile(filepath=str(p));assert all(l.filepath.startswith('//') for l in bpy.data.libraries)
 bpy.ops.wm.read_factory_settings(use_empty=True)
 with bpy.data.libraries.load(str(p),link=True) as (a,b):assert cname(slug) in a.collections;b.collections=[cname(slug)]
 c=b.collections[0];bpy.context.scene.collection.children.link(c);lo,hi=full_bounds(c);meta=json.loads((folder(slug)/'asset.json').read_text());assert all(abs(hi[i]-lo[i]-meta['dimensions_m'][i])<1e-5 for i in range(3));assert all(Path(bpy.path.abspath(l.filepath)).exists() or Path(bpy.path.abspath(l.filepath,library=l.parent)).exists() for l in bpy.data.libraries)
 tests={}
 if slug!=FAUCET:
  dg=bpy.context.evaluated_depsgraph_get();hit,point,*_=bpy.context.scene.ray_cast(dg,Vector((.008,.006,.1)),Vector((0,0,-1)))
  assert not hit,(slug,'drain bore blocked',point);tests['drain_bore_unobstructed']=True
  # A separate bowl ray must hit the sloped basin, not a top cap.
  hit,point,*_=bpy.context.scene.ray_cast(dg,Vector((0,.11,.1)),Vector((0,0,-1)))
  assert hit and point.z<-.06,(slug,point);tests['bowl_open_below_counter']=True;tests['bowl_test_hit_z_m']=point.z
 if render:preview(slug)
 assert sha(p)==before
 report={'fresh_native_open':True,'fresh_link':True,'relative_dependencies_resolve':True,'native_sha256':before,'native_unchanged_by_review':True,'actual_dimensions_m':[hi[i]-lo[i] for i in range(3)],'tests':tests,'host_integration_checked':False,'preview_scope':'Actual asset in an illustrative38.1mm worktop with real cutouts/faucet bore; studio supports are not a supplied kitchen cabinet','visual_review_pending':True}
 if (folder(slug)/'preview.png').exists():report['preview_sha256']=sha(folder(slug)/'preview.png')
 (folder(slug)/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('VERIFIED',slug,flush=True)
if __name__=='__main__':
 chosen=sys.argv[sys.argv.index('--asset')+1] if '--asset' in sys.argv else None
 if '--verify' in sys.argv:
  for slug in [chosen] if chosen else [FAUCET,*SPECS]:verify(slug,'--render' in sys.argv)
 else:
  if chosen is None or chosen==FAUCET:publish_faucet()
  for slug in [chosen] if chosen and chosen!=FAUCET else ([] if chosen else list(SPECS)):publish_sink(slug)
