"""Original concealed kitchen appliances and coordinated range/hood siblings.

All authoring coordinates are meters. Existing ancestors stay immutable.
Build unpublished assets: Blender -b --python tools/library/build_concealed_kitchen_appliances.py -- build
Fresh open/closed review: same command with -- verify --render
"""
import bpy
import json
import math
import sys
import os
from pathlib import Path
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from common import geometry as g
from common.library import linked_collection
GEN='tools/library/build_concealed_kitchen_appliances.py'
SPECS={
 'cream-inset-fridge-freezer-48in':('panel-ready-fridge-48in','Cream inset refrigerator / freezer, 48 inch',[1.2192,.762,2.1336]),
 'cream-inset-dishwasher-24in':('dishwasher-24in','Concealed cream inset dishwasher, 24 inch',[.6096,.6096,.86106]),
 'microwave-drawer-24in':('built-in-oven-30in','Stainless microwave drawer, 24 inch',[.6096,.60,.40]),
 'cream-brass-dual-fuel-range-48in':('dual-fuel-range-48in','Cream and brass dual-fuel range, 48 inch',[1.2192,.70,.9515]),
 'cream-plaster-wall-hood-48in':('wall-hood-36in','Cream plaster capture hood, 48 inch',[1.2192,.6604,.95]),
}
C=None
DEPS={}

def folder(slug):return ROOT/'library/appliances'/slug/'v001'
def write(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def box(name,loc,size,mat,bevel=.002):return g.box(name,[v/g.F for v in loc],[v/g.F for v in size],mat,bevel/g.F)
def rod(name,a,b,r,mat):return g.rod(name,[v/g.F for v in a],[v/g.F for v in b],r/g.F,mat)
def cyl(name,loc,r,h,mat):return g.cyl(name,[v/g.F for v in loc],r/g.F,h/g.F,mat,32)

def dependency(asset_id):
 p=ROOT/'library'/asset_id/'v001';m=json.loads((p/'asset.json').read_text())
 DEPS[asset_id]={'id':asset_id,'version':'v001','path':str(p/m['files']['blender'])}
 return p/m['files']['blender']

def material(asset_id,name=None):
 p=dependency(asset_id)
 with bpy.data.libraries.load(str(p),link=True) as (src,dst):
  selected=name or src.materials[0];assert selected in src.materials,(asset_id,selected,src.materials)
  dst.materials=[selected]
 return dst.materials[0]

def source_materials():
 names={'steel':'Original appliance brushed stainless','dark':'Original appliance graphite enamel','glass':'Original appliance low-tint glass','marks':'Original appliance etched control marks'}
 M={k:material('appliances/built-in-oven-30in',v) for k,v in names.items()}
 M['cream']=material('materials/cream-cabinet-enamel','Cream cabinet enamel | v001')
 M['brass']=material('materials/aged-brass','Aged brass | v001')
 return M

def ancestor(parent,keep=None):
 global C
 p=ROOT/'library/appliances'/parent/'v001';m=json.loads((p/'asset.json').read_text())
 with bpy.data.libraries.load(str(p/m['files']['blender']),link=False) as (src,dst):
  name=m.get('blender',{}).get('collection',m.get('collection'))
  if not name:
   assert len(src.collections)==1,src.collections
   name=src.collections[0]
  dst.collections=[name]
 C=dst.collections[0];bpy.context.scene.collection.children.link(C);g.ACTIVE=C
 if keep is not None:
  for o in list(C.all_objects):
   if not keep(o):bpy.data.objects.remove(o,do_unlink=True)
 return C

def blank():
 global C
 C=g.collection('Appliance assembly');return C

def hinge(name,loc,axis,amount,kind='rotation'):
 o=bpy.data.objects.new(name,None);C.objects.link(o);o.location=loc
 o['motion_kind']=kind;o['motion_axis']=axis;o['open_value']=amount;o['closed_location']=list(loc)
 return o

def attach(objects,parent):
 bpy.context.view_layer.update()
 for o in objects:
  world=o.matrix_world.copy();o.parent=parent;o.matrix_world=world
 bpy.context.view_layer.update()

def hardware(name,slug,loc,vertical=False,parent=None):
 dependency('hardware/'+slug);coll=linked_collection(ROOT,'hardware',slug,'v001')
 o=bpy.data.objects.new(name,None);o.instance_type='COLLECTION';o.instance_collection=coll;C.objects.link(o);o.location=loc
 if vertical:o.rotation_euler.y=math.pi/2
 o['asset_id']='hardware/'+slug;o['asset_version']='v001'
 if parent:attach([o],parent)
 return o

def inset_panel(name,cx,y,z0,z1,width,M):
 # The backing is 7mm behind its surrounding stile/rail faces.
 rail=.055
 box(name+' recessed painted field',(cx,y+.008,(z0+z1)/2),(width-.106,.018,z1-z0-.102),M['cream'],.003)
 for xx in [cx-width/2+rail/2,cx+width/2-rail/2]:box(name+' inset stile',(xx,y,(z0+z1)/2),(rail,.032,z1-z0),M['cream'],.002)
 for z in [z0+rail/2,z1-rail/2]:box(name+' inset rail',(cx,y,z),(width-.11,.032,rail),M['cream'],.002)
 # Fine internal beading is part of the edited appliance panel, not an overlay texture.
 for xx in [cx-width/2+rail+.004,cx+width/2-rail-.004]:box(name+' inner bead',(xx,y-.001,(z0+z1)/2),(.007,.021,z1-z0-.11),M['cream'],.0015)
 for z in [z0+rail+.004,z1-rail-.004]:box(name+' inner bead',(cx,y-.001,z),(width-.118,.021,.007),M['cream'],.0015)

def fridge(M):
 ancestor('panel-ready-fridge-48in',lambda o:any(t in o.name for t in ['oak side','oak top','ventilation']))
 for o in C.all_objects:
  if o.type=='MESH' and ('oak' in o.name):o.data.materials.clear();o.data.materials.append(M['cream']);o.name=o.name.replace('oak','painted')
 # Retained published side/top geometry is supplemented by real hollow compartments.
 box('Cold case rear enclosure',(0,.36,1.075),(1.177,.042,2.108),M['dark'])
 box('Cold compartment rear liner',(0,.331,1.12),(1.123,.016,1.94),M['cream'])
 box('Cold compartment bottom liner',(0,.025,.146),(1.14,.606,.03),M['cream'])
 box('Cold compartment top liner',(0,.025,2.072),(1.14,.606,.03),M['cream'])
 for x in [-.565,0,.565]:box('Cold compartment insulated division',(x,.025,1.11),(.026 if x else .040,.606,1.916),M['cream'])
 for x in [-.577,.577]:box('Cold case front gasket stile',(x,-.337,1.118),(.022,.018,1.945),M['dark'])
 for z in [.152,2.083]:box('Cold case front gasket rail',(0,-.337,z),(1.17,.018,.023),M['dark'])
 for side in [-1,1]:
  cx=side*.291
  for z in [.49,.84,1.19,1.54,1.88]:
   box('Cold compartment clear shelf',(cx,.045,z),(.518,.516,.008),M['glass'],.001)
   rod('Cold shelf front stainless edge',(cx-.259,-.213,z),(cx+.259,-.213,z),.003,M['steel'])
  for z in [.185,.335]:
   box('Cold storage bin base',(cx,.03,z),(.50,.45,.008),M['glass'])
   box('Cold storage bin front',(cx,-.193,z+.055),(.50,.009,.11),M['glass'])
   for xx in [cx-.25,cx+.25]:box('Cold storage bin side',(xx,.03,z+.055),(.009,.45,.11),M['glass'])
  hx=side*.599;door=hinge(('Left freezer' if side<0 else 'Right refrigerator')+' door hinge',(hx,-.389,.145),'Z',side*110)
  before=set(C.objects)
  inset_panel('Cold door lower',side*.3015,-.397,.145,.903,.595,M)
  inset_panel('Cold door upper',side*.3015,-.397,.907,2.1196,.595,M)
  box('Cold door inner insulated liner',(side*.3015,-.371,1.1323),(.567,.018,1.955),M['cream'])
  for z in [.55,.92,1.30,1.68]:
   box('Cold door bin floor',(side*.3015,-.296,z),(.49,.112,.012),M['glass'])
   box('Cold door bin retaining rail',(side*.3015,-.237,z+.065),(.49,.012,.13),M['glass'])
   for xx in [side*.3015-.245,side*.3015+.245]:box('Cold door bin end',(xx,-.296,z+.065),(.012,.112,.13),M['cream'])
  attach(set(C.objects)-before,door)
  hardware('Cold door aged brass appliance pull','appliance-pull-aged-brass-24in',(side*.086,-.413,1.30),True,door)
 return {'compartments':2,'door_panels_per_leaf':2,'glass_shelves':10,'door_storage_bins':8,'cold_storage_bins':4}

def dishwasher(M):
 ancestor('dishwasher-24in',lambda o:'recessed toe kick' in o.name)
 width=.60198
 for x in [-.284,.284]:box('Dishwasher insulated side shell',(x,.012,.466),(.030,.585,.79),M['dark'])
 box('Dishwasher insulated back',(0,.291,.466),(.54,.027,.79),M['dark'])
 for z in [.101,.843]:box('Dishwasher insulated horizontal shell',(0,.012,z),(.568,.585,.036),M['dark'])
 for x in [-.263,.263]:box('Dishwasher stainless tub side',(x,.021,.477),(.012,.529,.709),M['steel'])
 box('Dishwasher stainless tub back',(0,.279,.477),(.514,.013,.709),M['steel'])
 for z in [.134,.821]:box('Dishwasher stainless tub horizontal',(0,.015,z),(.514,.54,.012),M['steel'])
 for z in [.305,.595]:
  for xx in [-.222,.222]:
   rod('Dishwasher wire rack side',(xx,-.216,z),(xx,.218,z),.0032,M['steel'])
   rod('Dishwasher rack rim',(xx,-.216,z+.082),(xx,.218,z+.082),.0032,M['steel'])
  for i in range(13):
   yy=-.216+i*.0362;rod('Dishwasher wire rack crossbar',(-.222,yy,z),(.222,yy,z),.0027,M['steel'])
   for xx in [-.145,0,.145]:rod('Dishwasher rack upright tine',(xx,yy,z),(xx,yy+.008,z+.074),.002,M['steel'])
  for xx in [-.249,.249]:rod('Dishwasher rack slide',(xx,-.22,z-.011),(xx,.24,z-.011),.006,M['dark'])
 cyl('Dishwasher sump filter',(0,.055,.145),.053,.01,M['dark'])
 rod('Dishwasher lower wash arm',(-.19,.045,.177),(.19,.045,.177),.012,M['dark'])
 door=hinge('Dishwasher bottom hinge',(0,-.303,.092),'X',90)
 before=set(C.objects)
 # All three decorative panels belong to this single functional drop-down door.
 for i,(z0,z1) in enumerate([(.101,.347),(.352,.598),(.603,.849)]):
  inset_panel('Dishwasher false drawer '+str(i+1),0,-.311,z0,z1,width,M)
 box('Dishwasher door stainless inner liner',(0,-.282,.47),(.559,.020,.734),M['steel'])
 box('Dishwasher concealed top control deck',(0,-.289,.852),(.553,.048,.018),M['dark'])
 for x in [-.20,-.12,-.04]:box('Dishwasher top-edge control',(x,-.291,.862),(.045,.022,.002),M['marks'],.0005)
 box('Dishwasher internal detergent dispenser',(.125,-.265,.23),(.13,.028,.12),M['dark'])
 attach(set(C.objects)-before,door)
 for i,z in enumerate([.284,.535,.786]):hardware('Dishwasher false drawer brass pull '+str(i+1),'bar-pull-aged-brass-6in',(0,-.327,z),False,door)
 return {'functional_doors':1,'decorative_drawer_faces':3,'dish_racks':2,'tub_is_hollow':True}

def microwave(M):
 blank()
 # New dimensional and mechanical sibling: source oven materials are linked,
 # while the 24-inch enclosure and drawer are newly authored at true size.
 for xx in [-.293,.293]:box('Microwave fixed side casing',(xx,.012,.2),(.023,.575,.40),M['steel'])
 for z in [.010,.390]:box('Microwave fixed horizontal casing',(0,.012,z),(.567,.575,.020),M['steel'])
 box('Microwave fixed rear casing',(0,.290,.2),(.567,.02,.36),M['steel'])
 box('Microwave upper control bezel',(0,-.299,.353),(.6096,.034,.094),M['steel'])
 box('Microwave dark control strip',(.076,-.318,.353),(.401,.010,.060),M['dark'],.003)
 for x in [-.036,.035,.106]:box('Microwave illustrative display mark',(x,-.324,.357),(.047,.002,.006),M['marks'],.001)
 for x in [-.229,.230]:box('Microwave drawer touch button',(x,-.324,.348),(.041,.002,.022),M['marks'],.002)
 for xx in [-.282,.282]:
  for z in [.09,.24]:rod('Microwave fixed telescopic rail',(xx,-.241,z),(xx,.221,z),.006,M['steel'])
 drawer=hinge('Microwave drawer carriage',(0,0,0),'Y',-.38,'translation');before=set(C.objects)
 # Open-topped real cavity moves outward with the front fascia.
 box('Microwave moving bowl bottom',(0,-.005,.055),(.50,.472,.012),M['steel'])
 for xx in [-.250,.250]:box('Microwave moving bowl side',(xx,-.005,.160),(.014,.472,.21),M['steel'])
 for yy in [-.234,.224]:box('Microwave moving bowl end',(0,yy,.160),(.50,.014,.21),M['steel'])
 box('Microwave drawer front backing',(0,-.301,.165),(.6096,.033,.290),M['steel'])
 box('Microwave dark glass drawer face',(0,-.322,.168),(.522,.010,.226),M['dark'],.006)
 box('Microwave front lower trim',(0,-.331,.029),(.594,.019,.028),M['steel'])
 for xx in [-.230,.230]:rod('Microwave handle mounting',(xx,-.329,.256),(xx,-.370,.256),.008,M['steel'])
 rod('Microwave stainless drawer pull',(-.246,-.373,.256),(.246,-.373,.256),.010,M['steel'])
 attach(set(C.objects)-before,drawer)
 return {'drawer_travel_m':.38,'open_topped_cavity':True,'clear_cavity_concept_m':[.486,.444,.19]}

def cream_range(M):
 ancestor('dual-fuel-range-48in')
 for o in C.all_objects:
  if o.type!='MESH':continue
  n=o.name.lower()
  if any(t in n for t in ['side shell','control fascia','door stainless stile','door stainless rail','low rear riser']):
   o.data.materials.clear();o.data.materials.append(M['cream'])
  elif ('control dial' in n and 'bezel' not in n) or 'handle' in n or 'brass-colored ring' in n:
   o.data.materials.clear();o.data.materials.append(M['brass'])
 for o in C.all_objects:
  if o.type=='EMPTY' and 'door hinge' in o.name:
   o['motion_kind']='rotation';o['motion_axis']='X';o['open_value']=90;o['closed_location']=list(o.location)
 return {'gas_burners':6,'electric_griddle':1,'independent_electric_oven_cavities':2,'preserved_ancestor_geometry':True}

def hood(M):
 blank();M['plaster']=material('materials/warm-limestone-plaster')
 w=1.2192;dep=.6604
 # Hollow tapered shell: no bottom polygon blocks the capture inlet.
 outer=[(-w/2,-dep/2,.075),(w/2,-dep/2,.075),(w/2,dep/2,.075),(-w/2,dep/2,.075),(-.28,.015,.65),(.28,.015,.65),(.28,.3302,.65),(-.28,.3302,.65)]
 data=bpy.data.meshes.new('Hood tapered plaster shell');data.from_pydata(outer,[],[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);data.update()
 obj=bpy.data.objects.new('Hood hollow tapered plaster canopy',data);C.objects.link(obj);obj.data.materials.append(M['plaster']);mod=obj.modifiers.new('Noncombustible concept shell thickness','SOLIDIFY');mod.thickness=.025;mod.offset=-1
 for xx in [-w/2+.022,w/2-.022]:box('Hood lower plaster side',(xx,0,.0375),(.044,dep,.075),M['plaster'],.008)
 for yy in [-dep/2+.022,dep/2-.022]:box('Hood lower plaster rim',(0,yy,.0375),(w-.088,.044,.075),M['plaster'],.008)
 for xx in [-.266,.266]:box('Hood upper plaster side',(xx,.1726,.7875),(.028,.3152,.275),M['plaster'],.005)
 for yy in [.029,.3162]:box('Hood upper plaster front or rear',(0,yy,.7875),(.504,.028,.275),M['plaster'],.005)
 # Four separate cap pieces leave the 254mm square duct socket truly open.
 for x0,x1,y0,y1 in [(-.28,-.127,.015,.3302),(.127,.28,.015,.3302),(-.127,.127,.015,.033),(-.127,.127,.287,.3302)]:
  box('Hood top cap around duct port',((x0+x1)/2,(y0+y1)/2,.938),(x1-x0,y1-y0,.024),M['plaster'],.002)
 cassette=hinge('Hood removable filter cassette',(0,0,0),'Z',-.18,'translation');before=set(C.objects)
 for xx in [-.54,.54]:box('Hood stainless filter edge',(xx,0,.04),(.012,.53,.027),M['steel'])
 for yy in [-.259,.259]:box('Hood stainless filter edge',(0,yy,.04),(1.07,.012,.027),M['steel'])
 for i in range(24):box('Hood removable baffle',(i*.043-.4945,0,.040),(.018,.50,.023),M['steel'],.004)
 attach(set(C.objects)-before,cassette)
 for xx in [-.552,.552]:cyl('Hood underside task lens',(xx,-.224,.021),.022,.012,M['glass'])
 return {'capture_width_m':w,'capture_depth_m':dep,'duct_socket_m':{'center':[0,.160,.950],'width':.254,'depth':.254},'filter_removal_drop_m':.18}

BUILDERS={'cream-inset-fridge-freezer-48in':fridge,'cream-inset-dishwasher-24in':dishwasher,'microwave-drawer-24in':microwave,'cream-brass-dual-fuel-range-48in':cream_range,'cream-plaster-wall-hood-48in':hood}

def pose(col,fraction):
 for o in col.all_objects:
  if 'motion_kind' not in o:continue
  axis='XYZ'.index(o['motion_axis'])
  if o['motion_kind']=='rotation':o.rotation_euler[axis]=math.radians(o['open_value'])*fraction
  else:
   o.location=o['closed_location'];o.location[axis]+=o['open_value']*fraction
 bpy.context.view_layer.update()

def bounds(col):
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();points=[]
 def visit(obj,transform):
  if obj.type=='MESH':
   ev=obj.evaluated_get(dg);mesh=ev.to_mesh()
   points.extend(transform@v.co for v in mesh.vertices);ev.to_mesh_clear()
  if obj.instance_type=='COLLECTION' and obj.instance_collection:
   offset=Matrix.Translation(-obj.instance_collection.instance_offset)
   for child in obj.instance_collection.all_objects:visit(child,transform@offset@child.matrix_world)
 for o in col.all_objects:visit(o,o.matrix_world)
 return {'min':[round(min(v[i] for v in points),7) for i in range(3)],'max':[round(max(v[i] for v in points),7) for i in range(3)]}

def swept(col):
 samples=[]
 for i in range(56):pose(col,i/55);samples.append(bounds(col))
 pose(col,0)
 return {'min':[round(min(s['min'][i] for s in samples)-.001,6) for i in range(3)],'max':[round(max(s['max'][i] for s in samples)+.001,6) for i in range(3)]}

def open_collection(closed,slug):
 opened=bpy.data.collections.new(slug+' | open v001')
 bpy.context.scene.collection.children.link(opened)
 mapping={}
 for obj in closed.all_objects:
  cp=obj.copy();cp.parent=None;opened.objects.link(cp);cp.matrix_world=obj.matrix_world.copy();mapping[obj]=cp
 bpy.context.view_layer.update()
 for obj,cp in mapping.items():
  if obj.parent in mapping:
   cp.parent=mapping[obj.parent];cp.matrix_parent_inverse=cp.parent.matrix_world.inverted();cp.matrix_world=obj.matrix_world.copy()
 pose(opened,1)
 opened['asset_id']='appliances/'+slug;opened['asset_version']='v001';opened['operating_state']='open/service'
 return opened


def installation(slug):
 if 'fridge' in slug:return {'clear_opening_concept_m':[1.232,.80,2.15],'rear_service_reserve_m':.03,'front_person_space_m':1.22,'side_hinge_relief_m_each':.23,'services':['Electrical supply','Optional water connection','Unobstructed recessed toe ventilation and anti-tip restraint']}
 if 'dishwasher' in slug:return {'clear_opening_concept_m':[.610,.635,.880],'counter_underside_min_m':.880,'front_person_space_m':1.0,'services':['Water supply, drainage and electrical access from adjacent sink bay','No opaque cabinet carcass or false drawer occupies the appliance bay']}
 if 'microwave' in slug:return {'clear_opening_concept_m':[.620,.625,.415],'support_base_required':True,'front_person_space_m':.90,'suggested_bottom_above_floor_m':.40,'services':['Selected-product power, cooling openings and isolation','Drawer reach, landing counter and child-safety review']}
 if 'range' in slug:return {'clear_opening_concept_m':[1.232,.76,.96],'rear_service_reserve_m':.06,'front_person_space_m':1.0,'fuel':'Gas burners; two electric ovens and electric griddle','services':['Selected-product electrical/gas isolation, anti-tip restraint and heat clearances','Full-width ducted extraction and unresolved make-up-air needs']}
 return {'mounting':'Noncombustible host wall and independent structural support','suggested_bottom_above_floor_m':1.79,'capture_clearance_above_pot_support_m':.8385,'services':['Continuous host duct from the top socket to outdoors','Selected appliance compatibility, capture airflow, heat clearances and make-up air unverified']}

def publish(slug):
 global DEPS
 target=folder(slug);path=target/(slug+'.blend')
 if path.exists():raise RuntimeError('Refusing to modify existing published version: '+str(path))
 bpy.ops.wm.read_factory_settings(use_empty=True);DEPS={}
 M=source_materials();features=BUILDERS[slug](M);C.name=slug+' | v001';C['asset_id']='appliances/'+slug;C['asset_version']='v001';C['front_direction']='-Y';C['concept_only']=True
 pose(C,0);closed=bounds(C);pose(C,1);opened=bounds(C);pose(C,0);sweep=swept(C)
 target.mkdir(parents=True,exist_ok=True)
 opened_collection=open_collection(C,slug)
 assert bounds(opened_collection)==opened,(bounds(opened_collection),opened)
 bpy.context.scene.collection.children.unlink(opened_collection)
 deps=[]
 for asset_id,dep in DEPS.items():
  deps.append({**dep,'path':os.path.relpath(dep['path'],target)})
 parent,title,nominal=SPECS[slug]
 method=('Append and recolor the actual published ancestor geometry, retaining full-size cavities, grates and hinges.' if 'range' in slug else 'Append published casing/top/ventilation pieces, replacing solid interior and plain faces with true compartments and articulated doors.' if 'fridge' in slug else 'Append the actual published toe recess; replace opaque enclosure and plain face with a hollow tub, wire racks and one articulated paneled door.' if 'dishwasher' in slug else 'Reuse pinned published oven materials; original 24-inch drawer enclosure and mechanism replace the 30-inch oven architecture.' if 'microwave' in slug else 'New full-width hollow 48-inch shell and removable baffles, derived from the published 36-inch hood concept; source appliance materials retained.')
 metadata={'schema_version':1,'id':'appliances/'+slug,'version':'v001','name':title,'units':'meters','dimensions_m':[round(closed['max'][i]-closed['min'][i],7) for i in range(3)],'bounds_m':closed,'nominal_case_m':{'width':nominal[0],'depth':nominal[1],'height':nominal[2]},'blender':{'collection':C.name,'operating_collections':{'open':opened_collection.name}},'placement':{'origin':'Bottom/floor center XY at Z=0','front_direction':'-Y','up':'Z','allowed_scaling':'Rigid placement and rotation only; no appliance or hardware scaling.'},'features':features,'operating_envelope':{'modeled_state':'Closed by default; articulated native mechanisms tested in full-open or service state','mechanisms':[{'object':o.name,'kind':o['motion_kind'],'axis':o['motion_axis'],'open_value':o['open_value'],'value_units':'degrees' if o['motion_kind']=='rotation' else 'meters','origin_m':list(o['closed_location'])} for o in C.all_objects if 'motion_kind' in o],'open_bounds_m':opened,'conservative_swept_bounds_m':sweep,'sweep_basis':'All moving assemblies sampled in 55 intervals over their full travel; 1mm padding. Concept geometry, not manufacturer data. Add person and circulation space separately.','host_open_state_checked':False},'installation':{**installation(slug),'host_integration_checked':False,'concept_only':True},'derived_from':{'id':'appliances/'+parent,'version':'v001','path':'../../'+parent+'/v001/'+parent+'.blend','method':method},'dependencies':deps,'source':{'kind':'original-variation','generator':GEN,'command':'Blender --background --python '+GEN+' -- build --slug '+slug},'license':'CC-BY-4.0','rights':'Original Homes project contributor geometry; preserve ancestor attribution. No third-party appliance CAD, trademark, commercial model or product certification.','files':{'blender':path.name,'preview':'preview.png','open_preview':'preview-open.png','validation':'validation.json'},'software':{'blender':bpy.app.version_string},'limitations':['Original concept geometry; selected-product services and installation remain unresolved.','Native asset-only closed/open verification does not establish host circulation or installation approval.']}
 write(target/'asset.json',metadata)
 # Relative remapping happens inside the written library; no preview studio is included.
 bpy.data.libraries.write(str(path),{C,opened_collection},path_remap='RELATIVE_ALL',fake_user=True)
 print('PUBLISHED',slug,closed,flush=True)


def studio(col,slug,opened):
 g.collection('Preview studio - not part of reusable asset')
 floor_mat=g.material('Preview neutral gray',(.24,.255,.25),.8)
 floor=box('Preview ground',(0,0,-.035),(200,200,.06),floor_mat,0)
 is_fridge='fridge' in slug;is_hood='hood' in slug
 if is_fridge:loc=(3.4,-5.8,3.4);target=(0,-.1,1.04);scale=3.3
 elif is_hood:loc=(2.0,-3.5,1.9);target=(0,0,.45);scale=1.9
 else:loc=(1.75,-3,1.95);target=(0,-.13,.43 if 'range' in slug or 'dishwasher' in slug else .19);scale=2.05 if 'range' in slug else 1.78 if 'dishwasher' in slug else 1.38
 if is_hood and opened:loc=(1.7,-3,-1.15);target=(0,0,.3);floor.hide_render=True
 cam=g.camera('Preview camera',[v/g.F for v in loc],[v/g.F for v in target],48);cam.data.type='ORTHO';cam.data.ortho_scale=scale
 scene=bpy.context.scene;scene.camera=cam
 for name,position,energy,size in [('Soft key',(-3,-4,5),650,4),('Broad fill',(4,-1,3),420,3),('Edge',(1,4,4),700,3)]:g.area(name,[v/g.F for v in position],[0,0,.6/g.F],energy,size/g.F,(1,.94,.85))
 if is_hood and opened:g.area('Service underside fill',[0,-1/g.F,-2/g.F],[0,0,.3/g.F],180,2/g.F,(1,.96,.9))
 world=bpy.data.worlds.new('Neutral preview world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.25,.28,.30,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35;scene.world=world
 scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=20;scene.cycles.use_denoising=True
 scene.render.resolution_x=720;scene.render.resolution_y=720;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
 scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.render.film_transparent=False
 scene.render.threads_mode='FIXED';scene.render.threads=6


def verify(slug,render=False):
 target=folder(slug);meta=json.loads((target/'asset.json').read_text());path=target/meta['files']['blender']
 bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False)
 col=bpy.data.collections[meta['blender']['collection']];stored_open=bpy.data.collections[meta['blender']['operating_collections']['open']]
 bpy.context.scene.collection.children.link(col);bpy.context.scene.collection.children.link(stored_open);g.ACTIVE=col
 stored_open_bounds=bounds(stored_open);assert stored_open_bounds==meta['operating_envelope']['open_bounds_m'],stored_open_bounds
 bpy.context.scene.collection.children.unlink(stored_open)
 pose(col,0);closed=bounds(col);pose(col,1);opened=bounds(col);pose(col,0)
 for measured,expected in [(closed,meta['bounds_m']),(opened,meta['operating_envelope']['open_bounds_m'])]:
  assert max(abs(measured[k][i]-expected[k][i]) for k in ['min','max'] for i in range(3))<.00002,(slug,measured,expected)
 libraries=[]
 for lib in bpy.data.libraries:
  assert lib.filepath.startswith('//'),(slug,lib.filepath)
  p=Path(bpy.path.abspath(lib.filepath,library=lib.parent)).resolve();assert p.is_file(),str(p)
  libraries.append({'saved_relative_path':lib.filepath,'resolved_repository_path':str(p.relative_to(ROOT))})
 assert all(all(abs(v-1)<1e-6 for v in o.scale) for o in col.all_objects if o.instance_type=='COLLECTION')
 receipt={'status':'fresh_reopen_pass','blender':bpy.app.version_string,'collection':col.name,'closed_bounds_m':closed,'open_bounds_m':opened,'object_count':len(col.all_objects),'relative_dependencies_resolved':libraries,'all_saved_library_paths_relative':True,'rigid_hardware_scale_verified':True,'explicit_open_collection_verified':True,'host_integration_checked':False,'visual_review':'pending actual preview inspection'}
 if render:
  for state in [0,1]:
   for sc in list(bpy.data.collections):
    if sc.name.startswith('Preview studio'):
     for o in list(sc.objects):bpy.data.objects.remove(o,do_unlink=True)
     bpy.data.collections.remove(sc)
   pose(col,state);studio(col,slug,state);bpy.context.scene.render.filepath=str(target/('preview-open.png' if state else 'preview.png'));bpy.ops.render.render(write_still=True)
  pose(col,0);receipt['rendered_states']=['closed','open/service']
 write(target/'validation.json',receipt);print('VERIFIED',slug,flush=True)


if __name__=='__main__':
 args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['build']
 mode=args[0] if args else 'build';slugs=[args[i+1] for i,value in enumerate(args) if value=='--slug'] if '--slug' in args else list(SPECS)
 for slug in slugs:
  if mode=='build':publish(slug)
  elif mode=='verify':verify(slug,'--render' in args)
  else:raise ValueError(mode)
