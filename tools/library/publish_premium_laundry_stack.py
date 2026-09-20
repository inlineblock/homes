"""Original generic premium heat-pump laundry stack using documented planning dimensions.

blender -b --factory-startup --python tools/library/publish_premium_laundry_stack.py
blender -b --factory-startup --python tools/library/publish_premium_laundry_stack.py -- --verify --render
No manufacturer CAD, logos or geometry are copied. This is not an approved installation.
"""
from pathlib import Path
import bpy,json,math,hashlib,sys
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'tools/library')]
from common import geometry as g
from publish_modern_block import box,bounds
SLUG='premium-stacked-laundry-596';ID='appliances/'+SLUG;NAME='Premium compact washer and heat-pump dryer stack | v001'
FOLDER=ROOT/'library'/ID/'v001';NATIVE=FOLDER/(SLUG+'.blend');GEN='tools/library/publish_premium_laundry_stack.py'
SOURCES={
 'washer':'https://www.mieleusa.com/product/12864100/w1-front-loading-washing-machine-wxr960-wcs-tdosandintensewash',
 'dryer':'https://www.mieleusa.com/product/12864160/t1-heat-pump-dryer-txr960wp-ecoandsteam',
 'washer_manual':'https://media.miele.com/downloads/c9/f5/00_C7F1383867AF1FD1898B2B80E678C9F5.pdf',
 'dryer_manual':'https://media.miele.com/downloads/03/33/00_C7F13838CDF91FD186920BC33FF60333.pdf',
 'predecessor_stack_height_diagram':'https://www.mieleusa.com/forms2/us/sa/manuals-125.aspx?asDownload=1&mNo=10669410'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cyl(name,loc,r,depth,mat):
 o=g.cyl(name,Vector(loc)/g.F,r/g.F,depth/g.F,mat,64);o.rotation_euler.x=math.pi/2;return o

def torus(name,loc,major,minor,mat):
 bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=64,minor_segments=12,location=loc,rotation=(math.pi/2,0,0));o=g.move(bpy.context.object);o.name=name;o.data.materials.append(mat)
 for p in o.data.polygons:p.use_smooth=True
 return o

def label(text,loc,mat,size=.012):
 curve=bpy.data.curves.new(text,'FONT');curve.body=text;curve.size=size;curve.extrude=.0002;curve.align_x='CENTER';o=bpy.data.objects.new(text,curve);g.ACTIVE.objects.link(o);o.location=loc;o.rotation_euler.x=math.pi/2;o.data.materials.append(mat);return o

def machine(index,z0,M):
 prefix='Lower washer' if index==0 else 'Upper heat-pump dryer'
 # Actual open enclosure with removable panels and a round front opening.
 for x in [-.294,.294]:box(prefix+' side panel',(x,.02,z0+.425),(.008,.603,.85),M['white'],.003)
 for z in [.004,.846]:box(prefix+' top or bottom',(0,.02,z0+z),(.58,.603,.008),M['white'],.003)
 box(prefix+' rear enclosure',(0,.3175,z0+.425),(.58,.008,.834),M['white'],.002)
 front=box(prefix+' front sheet with real drum opening',(0,-.2775,z0+.425),(.58,.008,.834),M['white'],.006)
 cutter=cyl('Temporary drum opening',(0,-.28,z0+.38),.197,.08,M['dark'])
 bpy.context.view_layer.objects.active=front;mod=front.modifiers.new('Real circular drum recess','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 # Stainless recessed drum, perforation impressions and dark recessed rim.
 cyl(prefix+' recessed drum back',(0,-.06,z0+.38),.19,.008,M['steel'])
 for yy in [-.255,-.22,-.16,-.10]:torus(prefix+' recessed drum wall',(0,yy,z0+.38),.187,.0035,M['steel'])
 for k in range(28):
  a=k*math.tau/28;cyl(prefix+' drum perforation mark',(.145*math.cos(a),-.066,z0+.38+.145*math.sin(a)),.005,.001,M['dark'])
 door=[]
 door.append(torus(prefix+' movable black door rim',(0,-.3,z0+.38),.21,.007,M['dark']))
 door.append(cyl(prefix+' movable glass',(0,-.3185,z0+.38),.200,.006,M['glass']))
 door.append(box(prefix+' movable door grip',(.172,-.312,z0+.38),(.022,.016,.10),M['dark'],.004))
 for o in door:o['stack_door_index']=index
 box(prefix+' black control display',(.075,-.285,z0+.759),(.27,.009,.056),M['dark'],.003)
 cyl(prefix+' rotary control',(-.196,-.295,z0+.759),.026,.026,M['steel'])
 label('WASH' if index==0 else 'HEAT PUMP DRY',(.075,-.291,z0+.755),M['marks'],.012 if index==0 else .010)
 box(prefix+' lower service access',(0,-.284,z0+.075),(.49,.006,.065),M['white'],.003)
 if index==1:
  for i in range(12):box(prefix+' unblocked heat pump air intake',(-.23+i*.018,-.288,z0+.075),(.008,.004,.038),M['dark'],.001)
 else:
  box(prefix+' detergent service drawer',(-.174,-.285,z0+.666),(.18,.008,.045),M['white'],.003)
 return prefix

def publish():
 if NATIVE.exists():print('PRESERVE',ID);return
 bpy.ops.wm.read_factory_settings(use_empty=True);c=g.collection(NAME);c['asset_id']=ID;c['asset_version']='v001';c['washer_count']=1;c['dryer_count']=1
 M={'white':g.material('Premium laundry satin warm white',(.73,.74,.72),.24,.05),'dark':g.material('Premium laundry graphite controls',(.012,.016,.02),.23,.1),'steel':g.material('Premium laundry brushed stainless',(.36,.38,.40),.25,.8),'glass':g.material('Premium laundry tinted door glass',(.055,.085,.11),.1),'marks':g.material('Premium laundry display marking',(.5,.68,.70),.4)}
 bs=M['glass'].node_tree.nodes.get('Principled BSDF');bs.inputs['Transmission Weight'].default_value=.68;bs.inputs['IOR'].default_value=1.46
 machine(0,0,M);machine(1,.861,M)
 box('Dedicated 11mm conceptual stacking interface',(0,.02,.8555),(.58,.60,.011),M['dark'],.001)
 for x in [-.289,.289]:box('Stacking lateral locating bracket',(x,.02,.864),(.005,.57,.015),M['steel'],.001)
 lo,hi=bounds(c);FOLDER.mkdir(parents=True,exist_ok=True);bpy.data.libraries.write(str(NATIVE),{c},fake_user=True,path_remap='RELATIVE_ALL')
 meta={'schema_version':1,'id':ID,'version':'v001','name':NAME,'units':'meters','dimensions_m':[hi[i]-lo[i] for i in range(3)],'bounds_m':{'min':lo,'max':hi},'blender':{'collection':NAME},'placement':{'origin':'Floor at center of nominal596x643mm complete stack footprint','front_direction':'-Y; width X; Z up','allowed_scaling':'Rigid placement and Z rotation only; no scaling; always keep washer below dryer'},'equipment':{'washer_count':1,'heat_pump_dryer_count':1,'nominal_individual_m':[.596,.643,.850],'geometry_stack_height_m':1.711,'reserved_installation_height_m':1.8,'stacking_bridge_height_m':.011,'brand_status':'Original unbranded geometry, not a manufacturer model or certified stacking system'},'design_basis':{'reference_family':'Miele WXR960 WCS and TXR960WP Eco&Steam with WTV502 no-drawer stack kit','sources':SOURCES,'review_date':'2026-09-20','dimensions_basis':'Current individual product dimensions596W x643D x850H mm and1077mm depth with door open. 1711mm WTV502 stack height is from previous W1/T1 family installation diagram; current pages list compatibleWTV502 but current exact installed height requires final drawing confirmation.','stock':'Dealer inventory unverified. Reference family supports planning; asset does not specify procurement.'},'installation':{'mounting':'Dedicated manufacturer-approved stacking kit and level supported floor required for the actual chosen equipment. Modeled 11mm bridge is a visual interface, not a kit fabrication detail. Reserve1.8m installation height and75mm rear service allowance as concept assumptions until selected drawings.','operating_envelope':{'modeled_state':'Both doors closed; individually poseable geometry, washer and dryer hinges left in this concept','intended_open_angle_degrees':90,'hinges_m':[[-.217,-.30,.38],[-.217,-.30,1.241]],'published_reference_depth_with_door_open_m':1.077,'published_reference_projection_beyond_closed_front_m':.434,'operator_space_beyond_open_door_m':.60,'front_operation_reserve_m':1.034,'basis':'434mm is calculated from current manufacturer1077−643mm depths. Separate600mm human allowance is a concept assumption. Host checks actual whole door sweep, basket, adjacent cabinets and route.','host_open_state_checked':False},'service_requirements':['Current reference units each120V60Hz15A NEMA5-15; resolve appropriate circuits or approved pair adapter with selected manuals and jurisdiction.','Washer shutoffs, drain/trap and leak management must remain accessible; stain sink is not automatically the drain system.','Ventless heat-pump dryer requires heat dissipation and accessible front intake/filter and condensate drain/container; no sealed decorative enclosure.','Preserve whole-machine removal and stacking-kit service access; actual hoses, supplies, vibration and floor capacity need coordination.']},'dependencies':[],'derived_from':None,'source':{'kind':'original geometry from dimensional planning references only','generator':GEN,'command':'blender -b --factory-startup --python '+GEN},'software':{'blender':bpy.app.version_string},'license':'CC-BY-4.0','rights':'Original Homes project contributors geometry and procedural materials. No manufacturer CAD, trademarks, downloaded product images or third-party meshes. Attribution Homes project contributors.','files':{'blender':NATIVE.name,'preview':'preview.png','open_preview':'open-preview.png','validation':'validation.json'},'limitations':'Illustrative stack geometry, not manufacturer-exact appearance, stacking-kit engineering or an installation/code approval.'}
 (FOLDER/'asset.json').write_text(json.dumps(meta,indent=2)+'\n');print('PUBLISHED',ID,meta['dimensions_m'],flush=True)

def open_doors(c):
 for o in c.all_objects:
  idx=o.get('stack_door_index')
  if idx is None:continue
  hinge=Vector((-.217,-.30,.38+idx*.861));o.matrix_world=Matrix.Translation(hinge)@Matrix.Rotation(-math.pi/2,4,'Z')@Matrix.Translation(-hinge)@o.matrix_world
 bpy.context.view_layer.update()

def preview(c):
 g.collection('Laundry preview studio only');floor=g.material('Laundry neutral studio',(.24,.25,.235),.9);box('Studio ground',(0,0,-.03),(200,200,.05),floor)
 s=bpy.context.scene;target=Vector((0,-.02,.85));s.camera=g.camera('Laundry native preview',Vector((1.8,-3.3,2.15))/g.F,target/g.F,55)
 g.area('Laundry soft key',Vector((-2,-3,4))/g.F,target/g.F,700,3/g.F,(1,.98,.94));g.area('Laundry soft fill',Vector((3,1,3))/g.F,target/g.F,400,2/g.F,(.94,.97,1))
 s.world=bpy.data.worlds.new('Laundry studio world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.4
 s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=32;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=3;s.render.resolution_x=800;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.view_settings.view_transform='AgX';s.render.image_settings.file_format='PNG'
 s.render.filepath=str(FOLDER/'preview.png');bpy.ops.render.render(write_still=True);open_doors(c);s.render.filepath=str(FOLDER/'open-preview.png');bpy.ops.render.render(write_still=True)

def verify(render):
 before=sha(NATIVE);bpy.ops.wm.open_mainfile(filepath=str(NATIVE));bpy.ops.wm.read_factory_settings(use_empty=True)
 with bpy.data.libraries.load(str(NATIVE),link=True) as (a,b):assert NAME in a.collections;b.collections=[NAME]
 c=b.collections[0];bpy.context.scene.collection.children.link(c);lo,hi=bounds(c)
 assert all(abs(hi[i]-lo[i]-v)<1e-5 for i,v in enumerate([.596,.643,1.711])),[hi[i]-lo[i] for i in range(3)]
 assert len([o for o in c.all_objects if o.get('stack_door_index')==0])==3;assert len([o for o in c.all_objects if o.get('stack_door_index')==1])==3
 if render:
  bpy.ops.wm.read_factory_settings(use_empty=True)
  with bpy.data.libraries.load(str(NATIVE),link=False) as (a,b):b.collections=[NAME]
  c=b.collections[0];bpy.context.scene.collection.children.link(c);preview(c)
 assert sha(NATIVE)==before
 result={'fresh_native_open':True,'fresh_link':True,'native_sha256':before,'native_preserved_by_review':True,'actual_dimensions_m':[hi[i]-lo[i] for i in range(3)],'washer_count':1,'dryer_count':1,'individual_door_groups':2,'reserved_installation_height_m':1.8,'host_integration_checked':False,'visual_review_pending':True}
 for file in ['preview.png','open-preview.png']:
  if (FOLDER/file).exists():result[file.replace('.png','')+'_sha256']=sha(FOLDER/file)
 (FOLDER/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print('VERIFIED',ID,flush=True)
if __name__=='__main__':
 if '--verify' in sys.argv:verify('--render' in sys.argv)
 else:publish()
