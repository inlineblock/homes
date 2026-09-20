"""Original inset cabinet siblings; immutable pinned collections and operating states.

Blender -b --factory-startup --python tools/library/build_inset_kitchen_cabinets.py
Blender -b --factory-startup --python tools/library/build_inset_kitchen_cabinets.py -- --verify --render
Use --materials-only to publish the cream enamel dependency first.
"""
from pathlib import Path
import bpy,json,sys,math
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from common import geometry as g
from common.library import linked_collection
from common.timber_materials import grain_uv
GEN='tools/library/build_inset_kitchen_cabinets.py'
H=.88;D=.6096;T=.018
ASSETS={
 'cream-inset-drawer-base-24in':(.6096,D,H,'drawer','cream','cabinetry/smoked-oak-drawer-base-2ft'),
 'cream-inset-sink-base-36in':(.9144,D,H,'sink','cream','cabinetry/smoked-oak-sink-base-36in'),
 'cream-inset-waste-pullout-18in':(.4572,D,H,'waste','cream','cabinetry/smoked-oak-waste-pullout-18in'),
 'cream-inset-glazed-upper-36in':(.9144,.3556,.76,'upper','cream',None),
 'cream-inset-pantry-36in':(.9144,D,2.44,'pantry','cream','cabinetry/oak-shelving-2ft'),
 'oak-inset-drawer-base-24in':(.6096,D,H,'drawer','oak','cabinetry/smoked-oak-drawer-base-2ft'),
 'oak-inset-sink-base-36in':(.9144,D,H,'sink','oak','cabinetry/smoked-oak-sink-base-36in'),
 'oak-inset-oven-base-30in':(.8128,D,H,'oven','oak','cabinetry/smoked-oak-oven-base-36in'),
 'oak-inset-island-back-panel-24in':(.6096,.035,H,'back','oak',None),
 'oak-inset-waste-pullout-18in':(.4572,D,H,'waste','oak','cabinetry/smoked-oak-waste-pullout-18in'),
 'oak-inset-microwave-base-24in':(.66,D,H,'microwave','oak','cabinetry/smoked-oak-oven-base-36in'),
 'cream-inset-appliance-garage-48in':(1.2192,.65,1.2,'garage','cream',None),
}
def folder(slug):return ROOT/'library/cabinetry'/slug/'v001'
def jwrite(path,data):path.write_text(json.dumps(data,indent=2)+'\n')
def link_mat(slug):
 path=ROOT/'library/materials'/slug/'v001'/(slug+'.blend')
 with bpy.data.libraries.load(str(path),link=True) as (a,b):b.materials=[a.materials[0]]
 return b.materials[0]
def publish_material():
 f=ROOT/'library/materials/cream-cabinet-enamel/v001';p=f/'cream-cabinet-enamel.blend'
 if p.exists():return
 bpy.ops.wm.read_factory_settings(use_empty=True);m=g.material('Cream cabinet enamel | v001',(.70,.675,.606),.34)
 n=m.node_tree.nodes;l=m.node_tree.links;bs=n.get('Principled BSDF');bs.inputs['Specular IOR Level'].default_value=.32;bs.inputs['Coat Weight'].default_value=.12;bs.inputs['Coat Roughness'].default_value=.36
 tc=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1100;noise.inputs['Detail'].default_value=2;l.new(tc.outputs['Object'],noise.inputs['Vector']);b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.055;b.inputs['Distance'].default_value=.00004;l.new(noise.outputs['Fac'],b.inputs['Height']);l.new(b.outputs['Normal'],bs.inputs['Normal'])
 f.mkdir(parents=True,exist_ok=True);bpy.data.libraries.write(str(p),{m},fake_user=True)
 jwrite(f/'asset.json',{'schema_version':1,'id':'materials/cream-cabinet-enamel','version':'v001','name':'Warm cream satin cabinet enamel','units':'meters','blender':{'material':m.name},'source':{'kind':'original','generator':GEN},'license':'CC-BY-4.0','rights':'Original procedural material; attribution Homes project contributors. Not a commercial coating specification.','dependencies':[],'files':{'blender':p.name,'preview':'preview.png','validation':'validation.json'},'software':{'blender':bpy.app.version_string},'texture_scale':{'coordinates':'Object coordinates in meters','microtexture_scale_per_m':1100,'bump_distance_m':.00004},'placement':'Material only; smooth enamel for cabinet frames and recessed panels, not a plaster surface.'})
 print('PUBLISHED_MATERIAL',p,flush=True)

def box(name,loc,size,mat,bevel=.001,parent=None,grain=True):
 # For the existing vertical-grain oak shader, author long members along local Z
 # then rotate, keeping object-space longitudinal grain along the actual member.
 if mat.library and 'coastal-white-oak' in mat.library.filepath and grain:
  axis=max(range(3),key=lambda i:size[i])
 else:axis=2
 if axis==0:
  o=g.box(name,[x/g.F for x in loc],[size[2]/g.F,size[1]/g.F,size[0]/g.F],mat,bevel/g.F);o.rotation_euler.y=math.pi/2
 elif axis==1:
  o=g.box(name,[x/g.F for x in loc],[size[0]/g.F,size[2]/g.F,size[1]/g.F],mat,bevel/g.F);o.rotation_euler.x=math.pi/2
 else:o=g.box(name,[x/g.F for x in loc],[x/g.F for x in size],mat,bevel/g.F)
 if parent:
  o.parent=parent;o.matrix_parent_inverse=parent.matrix_world.inverted()
 return o

def empty(name,loc,kind,amount):
 o=bpy.data.objects.new(name,None);g.ACTIVE.objects.link(o);o.location=loc;o.empty_display_type='PLAIN_AXES';o.empty_display_size=.06;o['motion_kind']=kind;o['open_amount']=amount;o['motion_axis']='Y translation' if kind=='slide' else 'Z rotation';bpy.context.view_layer.update();return o

def hardware(name,coll,loc,parent=None,vertical=False):
 o=bpy.data.objects.new(name,None);o.instance_type='COLLECTION';o.instance_collection=coll;g.ACTIVE.objects.link(o);o.location=loc
 if vertical:o.rotation_euler.y=math.pi/2
 if parent:o.parent=parent;o.matrix_parent_inverse=parent.matrix_world.inverted()
 return o

def panel(name,x,y,z,w,h,M,parent=None,glazed=False):
 # Moving inset door: 42mm rails/stiles, a true 8mm recessed center and bead.
 r=.042;t=.022
 for xx in [x-w/2+r/2,x+w/2-r/2]:box(name+' stile',(xx,y,z),(r,t,h),M['face'],.0012,parent)
 for zz in [z-h/2+r/2,z+h/2-r/2]:box(name+' rail',(x,y,zz),(w-2*r,t,r),M['face'],.0012,parent)
 iw=w-2*r;ih=h-2*r
 box(name+(' clear glass infill' if glazed else ' recessed center'),(x,y+.008,z),(iw,.006 if glazed else .010,ih),M['glass'] if glazed else M['face'],.0007,parent)
 # A fine applied bead creates an actual highlight around the panel reveal.
 for xx in [x-iw/2+.002,x+iw/2-.002]:box(name+' vertical inset bead',(xx,y-.005,z),(.004,.005,ih),M['face'],.0018,parent)
 for zz in [z-ih/2+.002,z+ih/2-.002]:box(name+' horizontal inset bead',(x,y-.005,zz),(iw-.004,.005,.004),M['face'],.0018,parent)

def drawer_box(name,x,z,w,depth,M,parent):
 lo=z;bh=.15
 box(name+' bottom',(x,.010,lo),(w,depth,.012),M['liner'],.001,parent)
 for xx in [x-w/2+.007,x+w/2-.007]:box(name+' side',(xx,.010,lo+bh/2),(.014,depth,bh),M['liner'],.001,parent)
 for yy in [.010-depth/2+.007,.010+depth/2-.007]:box(name+' end',(x,yy,lo+bh/2),(w-.028,.014,bh),M['liner'],.001,parent)

def build(slug):
 w,d,h,kind,finish,parentid=ASSETS[slug];c=g.collection(slug+' | v001');c['asset_id']='cabinetry/'+slug;c['asset_version']='v001'
 face=link_mat('cream-cabinet-enamel' if finish=='cream' else 'coastal-white-oak');M={'face':face,'liner':g.material('Original warm cabinet interior',(.58,.535,.433),.64),'dark':g.material('Original recessed toe-kick shadow',(.043,.039,.033),.62),'metal':g.material('Original concealed steel runner',(.25,.26,.26),.32,.7),'bin':g.material('Original graphite waste bin',(.047,.049,.044),.65),'glass':g.material('Original clear display glass',(.90,.94,.93),.08)}
 bs=M['glass'].node_tree.nodes.get('Principled BSDF');bs.inputs['Transmission Weight'].default_value=1;bs.inputs['IOR'].default_value=1.46
 pull=linked_collection(ROOT,'hardware','bar-pull-aged-brass-6in','v001') if kind in ['drawer','waste'] else None
 knob=linked_collection(ROOT,'hardware','round-knob-aged-brass-1p125in','v001') if kind in ['sink','upper','pantry','garage'] else None
 bottom=0 if kind in ['upper','garage'] else .10;front=-d/2;door_y=front+.013;frame_y=front+.012
 if kind=='back':
  panel('Island back inset panel',0,-.0065,h/2,w,h,M)
  box('Island panel rear backing',(0,.012,h/2),(w,.011,h),M['face'])
  return c
 # Carcasses stop behind a proper face frame and leave actual usable interiors.
 for xx in [-w/2+.009,w/2-.009]:box('Cabinet side',(xx,.014,(bottom+h)/2),(.018,d-.028,h-bottom),face,.0015)
 if kind not in ['sink','oven','microwave','garage']:box('Cabinet rear',(0,d/2-.009,(bottom+h)/2),(w-.036,.018,h-bottom),M['liner'])
 box('Cabinet floor',(0,.014,bottom+.009),(w-.036,d-.030,.018),M['liner'])
 if kind not in ['upper','garage']:
  box('Floor-contact recessed toe kick',(0,.040,.05),(w-.036,d-.10,.10),M['dark'])
 if kind in ['upper','pantry','garage']:box('Cabinet top',(0,.014,h-.009),(w-.036,d-.028,.018),face)
 else:
  for yy in [front+(.026 if kind=='sink' else .040),d/2-.018]:box('Counter support rail',(0,yy,h-.009),(w-.036,.020,.018),face)
 # Outer face-frame: 32mm stiles. Oven interface gets slim 18mm stiles.
 sw=.018 if kind in ['oven','microwave'] else .032
 for xx in [-w/2+sw/2,w/2-sw/2]:box('Fixed face frame stile',(xx,frame_y,(bottom+h)/2),(sw,.024,h-bottom),face)
 if kind not in ['oven','microwave']:
  for zz in [bottom+.016,h-.016]:box('Fixed face frame rail',(0,frame_y,zz),(w-2*sw,.024,.032),face)
 innerw=w-2*sw-.005;lo=bottom+.034;hi=h-.034
 if kind=='drawer':
  bay=(hi-lo)/3
  for i in range(3):
   zl=lo+i*bay+.006;zh=lo+(i+1)*bay-.006;mid=(zl+zh)/2
   if i:box('Fixed between-drawer rail',(0,frame_y,lo+i*bay),(w-2*sw,.024,.009),face,.001)
   root=empty('Drawer %d motion'%(i+1),(0,0,0),'slide',-.50)
   panel('Drawer %d inset front'%(i+1),0,door_y,mid,innerw,zh-zl,M,root)
   hardware('Linked aged brass drawer pull',pull,(0,front+.002,mid+.022),root)
   drawer_box('Drawer %d box'%(i+1),0,zl+.025,w-.102,.488,M,root)
   for xx in [-w/2+.069,w/2-.069]:box('Drawer front attachment bracket',(xx,front+.05,zl+.09),(.020,.060,.080),M['metal'],parent=root)
   for xx in [-w/2+.040,w/2-.040]:box('Fixed drawer slide',(xx,.014,zl+.043),(.010,.490,.016),M['metal'])
 elif kind in ['sink','upper','pantry']:
  if kind=='sink':
   split=hi-.13
   panel('Sink fixed inset false front',0,door_y,(split+hi)/2,innerw,hi-split-.005,M)
   hi=split-.005
   box('Sink low rear stretcher',(0,d/2-.009,bottom+.055),(w-.036,.018,.11),M['liner'])
  else:
   levels=[h*.49] if kind=='upper' else [.43,.80,1.17,1.54,1.91,2.24]
   for z in levels:box('Usable shelf deck',(0,.021,z),(w-.046,d-.068,.018),M['liner'])
  for sign in [-1,1]:
   dw=(innerw-.004)/2;xx=sign*(dw/2+.002);hingex=sign*(innerw/2+.020)
   root=empty(('Left' if sign<0 else 'Right')+' door hinge',(hingex,front-.010,lo),'hinge',math.radians(100)*sign)
   if kind=='pantry':
    panel('Pantry continuous inset door',xx,door_y,(lo+hi)/2,dw,hi-lo,M,root)
    box('Pantry door intermediate rail',(xx,door_y,1.26),(dw-.084,.022,.048),face,.0012,root)
    for zz in [1.234,1.286]:box('Pantry middle-rail inset bead',(xx,door_y-.005,zz),(dw-.084,.005,.004),face,.0018,root)
   else:panel('Inset '+kind+' door',xx,door_y,(lo+hi)/2,dw,hi-lo,M,root,kind=='upper')
   hardware('Linked paired aged brass knob',knob,(sign*.046,front+.002,min(1.23,(lo+hi)/2)),root)
 elif kind=='waste':
  root=empty('Waste carriage motion',(0,0,0),'slide',-.52)
  panel('Waste inset front',0,door_y,(lo+hi)/2,innerw,hi-lo,M,root)
  hardware('Linked aged brass waste pull',pull,(0,front+.002,hi-.06),root)
  bw=w-.112;box('Waste carriage deck',(0,.015,.146),(w-.090,.50,.020),M['liner'],parent=root)
  for y in [-.116,.125]:
   bh=.48;bd=.217;bz=.161
   box('Waste bin bottom',(0,y,bz),(bw,bd,.012),M['bin'],parent=root)
   for xx in [-bw/2+.006,bw/2-.006]:box('Waste bin side',(xx,y,bz+bh/2),(.012,bd,bh),M['bin'],parent=root)
   for yy in [y-bd/2+.006,y+bd/2-.006]:box('Waste bin end',(0,yy,bz+bh/2),(bw-.024,.012,bh),M['bin'],parent=root)
  for xx in [-w/2+.069,w/2-.069]:box('Waste front attachment bracket',(xx,front+.05,.185),(.020,.060,.10),M['metal'],parent=root)
  for xx in [-w/2+.035,w/2-.035]:box('Fixed waste runner',(xx,.015,.17),(.012,.5,.025),M['metal'])
 elif kind=='oven':
  # Outer 32-inch housing; 30-inch describes the compatible oven, never a scale.
  box('Oven load support shelf',(0,.010,.136),(w-.036,.56,.018),M['liner'])
  box('Oven upper face rail',(0,frame_y,h-.007),(w-.036,.024,.014),face)
  box('Oven lower inset apron',(0,frame_y,.122),(w-.036,.024,.024),face)
 elif kind=='microwave':
  # A full-size 24-inch drawer unit sits above a separate usable lower inset drawer.
  box('Microwave load support shelf',(0,.010,.431),(w-.036,.56,.018),M['liner'])
  box('Microwave upper face rail',(0,frame_y,h-.007),(w-.036,.024,.014),face)
  root=empty('Lower storage drawer motion',(0,0,0),'slide',-.48)
  panel('Microwave base lower inset drawer',0,door_y,.278,w-.040,.287,M,root)
  localpull=linked_collection(ROOT,'hardware','bar-pull-aged-brass-6in','v001')
  hardware('Linked lower drawer brass pull',localpull,(0,front+.002,.31),root)
  drawer_box('Lower microwave storage drawer',0,.163,w-.102,.488,M,root)
  for xx in [-w/2+.069,w/2-.069]:box('Microwave drawer front attachment bracket',(xx,front+.05,.220),(.020,.060,.080),M['metal'],parent=root)
 elif kind=='garage':
  # Hollow counter-mounted appliance bay with two actual high/low vent slots.
  for za,zb in [(0,.055),(.145,1.05),(1.14,h)]:box('Garage rear vent-separated panel',(0,d/2-.009,(za+zb)/2),(w-.036,.018,zb-za),M['liner'])
  for zz in [.075,.102,.13,1.073,1.10,1.127]:box('Garage rear grille slat',(0,d/2-.009,zz),(w-.06,.014,.008),M['face'])
  box('Appliance garage upper shelf',(0,.019,.86),(w-.046,d-.068,.018),M['liner'])
  # Four leaves pair into bifolds. Outer and intermediate hinges are independent.
  leafw=(innerw-.014)/4
  for sign in [-1,1]:
   xouter=sign*innerw/2
   root=empty(('Left' if sign<0 else 'Right')+' garage outer hinge',(xouter+sign*.020,front-.020,lo),'hinge',math.radians(100)*sign)
   x1=xouter-sign*leafw/2
   panel('Garage outer bifold inset leaf',x1,door_y,(lo+hi)/2,leafw-.003,hi-lo,M,root)
   midx=xouter-sign*(leafw+.004)
   fold=empty(('Left' if sign<0 else 'Right')+' garage folding hinge',(midx,front+.035,lo),'hinge',-math.radians(165)*sign)
   fold.parent=root;fold.matrix_parent_inverse=root.matrix_world.inverted()
   x2=midx-sign*leafw/2
   panel('Garage inner bifold inset leaf',x2,door_y,(lo+hi)/2,leafw-.003,hi-lo,M,fold)
   hardware('Linked garage aged brass knob',knob,(sign*.047,front+.002,.47),fold)
  reserve=bpy.data.objects.new('Host outlet and plug service reservation',None);g.ACTIVE.objects.link(reserve);reserve.location=(0,d/2-.06,.30);reserve.empty_display_type='CUBE';reserve.empty_display_size=.11;reserve.hide_render=True;reserve['clearance_m']=[.22,.12,.18];reserve['basis']='Host installs selected outlet and plug/cord bend space; placeholder does not count as electrical equipment.'
 bpy.context.view_layer.update();return c

def make_open(c):
 out=bpy.data.collections.new(c.name.replace(' | v001',' | open v001'));bpy.context.scene.collection.children.link(out);copies={}
 for o in c.objects:
  dup=o.copy();out.objects.link(dup);copies[o]=dup
 for o,dup in copies.items():
  if o.parent in copies:dup.parent=copies[o.parent];dup.matrix_parent_inverse=o.matrix_parent_inverse.copy()
  if o.get('motion_kind')=='slide':dup.location.y+=o['open_amount']
  elif o.get('motion_kind')=='hinge':dup.rotation_euler.z+=o['open_amount']
 out['asset_id']=c['asset_id'];out['asset_version']='v001';out['operating_state']='Open concept review';return out

def evaluated_points(c,matrix=Matrix.Identity(4)):
 points=[];dg=bpy.context.evaluated_depsgraph_get()
 for o in c.objects:
  transform=matrix@o.matrix_world
  if o.type=='MESH':
   ev=o.evaluated_get(dg);me=ev.to_mesh();points.extend(transform@v.co for v in me.vertices);ev.to_mesh_clear()
  elif o.instance_type=='COLLECTION' and o.instance_collection:points.extend(evaluated_points(o.instance_collection,transform))
 return points

def bounds(c):
 bpy.context.view_layer.update();p=evaluated_points(c);return [min(v[i] for v in p) for i in range(3)],[max(v[i] for v in p) for i in range(3)]

def publish():
 publish_material()
 if '--materials-only' in sys.argv:return
 for slug,(w,d,h,kind,finish,parentid) in ASSETS.items():
  if '--asset' in sys.argv and slug!=sys.argv[sys.argv.index('--asset')+1]:continue
  f=folder(slug);path=f/(slug+'.blend')
  if path.exists():print('PRESERVED',slug,flush=True);continue
  bpy.ops.wm.read_factory_settings(use_empty=True);c=build(slug);lo,hi=bounds(c);motions=[{'object':o.name,'kind':o['motion_kind'],'axis':o['motion_axis'],'open_amount':o['open_amount'],'hinge_or_origin_m':list(o.location)} for o in c.objects if o.get('motion_kind')];op=make_open(c);olo,ohi=bounds(op)
  f.mkdir(parents=True,exist_ok=True);bpy.data.libraries.write(str(path),{c,op},fake_user=True,path_remap='RELATIVE_ALL')
  mat='cream-cabinet-enamel' if finish=='cream' else 'coastal-white-oak';deps=[{'id':'materials/'+mat,'version':'v001','path':'../../../materials/'+mat+'/v001/'+mat+'.blend'}]
  if kind in ['drawer','waste','microwave']:deps+=[{'id':'hardware/bar-pull-aged-brass-6in','version':'v001','path':'../../../hardware/bar-pull-aged-brass-6in/v001/bar-pull-aged-brass-6in.blend'}]
  if kind in ['sink','upper','pantry','garage']:deps+=[{'id':'hardware/round-knob-aged-brass-1p125in','version':'v001','path':'../../../hardware/round-knob-aged-brass-1p125in/v001/round-knob-aged-brass-1p125in.blend'}]
  install={'mounting':'Floor supported; host countertop excluded' if kind not in ['upper','back','garage'] else 'Bottom-center wall-mount origin; host fixing/backing required' if kind=='upper' else 'Counter-mounted appliance garage, bottomZ0; host fixing and outlets required' if kind=='garage' else 'Bottom-center decorative island panel; host rear support required','nominal_carcass_dimensions_m':[w,d,h],'countertop_top_m':h+.020 if kind not in ['upper','pantry','back','garage'] else None,'operating_envelope':{'closed_collection':c.name,'open_collection':op.name,'motions':motions,'open_bounds_m':{'min':olo,'max':ohi},'reserve_operator_depth_m':.80,'basis':'Original measured closed/open concept geometry, no manufacturer mechanism selected','host_open_state_checked':False},'services':['Host must check neighboring doors/drawers, approach, anchorage, support, moisture detailing and actual product selection.']}
  if kind=='sink':install.update(countertop_cutout_m=[.664,.464],sink_bowl_reserve={'compatible_id':'fixtures/kitchen-sink-mixer-650','version':'v002','mounting_center_xy_m':[0,-.03],'below_counter_depth_m':.218,'cavity':'Open top/rear, no drawers or shelves in bowl and plumbing envelope'})
  if kind=='oven':install.update(appliance_opening_m={'width':w-.036,'bottom_z':.145,'top_z':.862,'depth':.58,'rear':'Open, continue services beyond carcass'},compatible_appliance={'id':'appliances/built-in-oven-30in','version':'v001','suggested_origin_m':[0,0,.148]},naming='30in is compatible appliance width. Housing is32in/.8128m wide to preserve full-size oven body and clearances.')
  if kind=='microwave':install.update(appliance_opening_m={'width':.624,'bottom_z':.440,'top_z':.862,'rear':'Open; service reserve beyond cabinet'},compatible_appliance={'id':'appliances/microwave-drawer-24in','version':'v001','nominal_size_m':[.6096,.60,.40],'suggested_origin_m':[0,0,.447],'installation_fit':'0.624m clear width,7mm support gap and15mm top gap at agreed origin; native component fit separately recorded'})
  if kind=='garage':install['operating_envelope']['required_sequence']=['Open both outer hinges from0to100degrees while each folding hinge stays0','Then fold inner leaves from0to165degrees; reverse this sequence to close','Do not drive all four hinge angles proportionally at once: opposite inner leaves can meet during motion']
  if kind=='garage':install.update(appliance_bay_clear_m=[w-.064,d-.05,.83],bifold_leaf_width_m=(w-.083)/4,ventilation='Two actual rear slotted grille bands atZ.055..145and1.05..1.14m; no rated ventilation capacity',outlet_reserve_m={'center':[0,d/2-.06,.30],'box':[.22,.12,.18]},counter_mount='Z0 is host countertop, not floor')
  meta={'schema_version':1,'id':'cabinetry/'+slug,'version':'v001','name':slug.replace('-',' ').title(),'units':'meters','dimensions_m':[hi[i]-lo[i] for i in range(3)],'bounds_m':{'min':lo,'max':hi},'blender':{'collection':c.name,'operating_collections':{'open':op.name}},'placement':{'origin':'Bottom-center at floor or mounting plane Z=0','front_direction':'-Y; width along X; Z up','allowed_scaling':'Rigid placement and Z rotation only; do not stretch'},'installation':install,'dependencies':deps,'derived_from':{'id':parentid,'version':'v001','basis':'Original rebuilt dimensional/functional sibling: retained parent interface intent, added true face frames, inset beaded panels, articulated fronts and linked finish/hardware; not a private copy of parent meshes'} if parentid else None,'source':{'kind':'original-variation' if parentid else 'original','generator':GEN,'command':'blender -b --factory-startup --python '+GEN+' -- --asset '+slug},'software':{'blender':bpy.app.version_string},'license':'CC-BY-4.0','rights':'Original Homes project geometry; attribution Homes project contributors. No manufacturer CAD or selected product compliance claim.','files':{'blender':path.name,'preview':'preview.png','open_preview':'preview-open.png','validation':'validation.json'}}
  jwrite(f/'asset.json',meta);print('PUBLISHED',slug,meta['dimensions_m'],flush=True)

def preview(c,f,lo,hi,filename):
 g.collection('Neutral studio only');s=bpy.context.scene;h=hi[2]-lo[2];span=max(h,hi[0]-lo[0],.9);center=Vector(((hi[0]+lo[0])/2,(hi[1]+lo[1])/2,(hi[2]+lo[2])/2));pos=center+Vector((span*1.4,-span*2.15,span*1.03));cam=g.camera('Native front three-quarter',pos/g.F,center/g.F,55);s.camera=cam
 ground=g.material('Neutral studio ground',(.36,.37,.35),.85);box('Studio ground',(0,0,lo[2]-.035),(100,100,.05),ground)
 g.area('Broad soft key',Vector((-span, -span,span*2.8))/g.F,center/g.F,span*span*380,span*1.7/g.F,(1,.97,.92));g.area('Soft fill',Vector((span,-span*.3,span*1.4))/g.F,center/g.F,span*span*135,span*1.3/g.F,(.92,.96,1))
 s.world=bpy.data.worlds.new('Neutral studio world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=620;s.render.resolution_y=680;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(f/filename);s.view_settings.view_transform='AgX';s.view_settings.exposure=0;bpy.ops.render.render(write_still=True)

def load_for_review(path,name):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 with bpy.data.libraries.load(str(path),link=True) as (a,b):b.collections=[name]
 c=b.collections[0];bpy.context.scene.collection.children.link(c);bpy.context.view_layer.update();return c

def component_fit(slug):
 specs={
  'cream-inset-sink-base-36in':('fixtures/kitchen-sink-mixer-650','v002',(0,-.03,.90)),
  'oak-inset-sink-base-36in':('fixtures/kitchen-sink-mixer-650','v002',(0,-.03,.90)),
  'oak-inset-oven-base-30in':('appliances/built-in-oven-30in','v001',(0,0,.148)),
  'oak-inset-microwave-base-24in':('appliances/microwave-drawer-24in','v001',(0,0,.447)),
 }
 if slug not in specs:return None
 id,version,offset=specs[slug];fp=ROOT/'library'/id/version/(id.split('/')[-1]+'.blend')
 if not fp.exists():return {'checked':False,'reason':'Compatible fixture native file unavailable','id':id,'version':version}
 c=load_for_review(folder(slug)/(slug+'.blend'),slug+' | v001');m=json.loads((fp.parent/'asset.json').read_text())
 with bpy.data.libraries.load(str(fp),link=True) as (a,b):b.collections=[m.get('blender',{}).get('collection',a.collections[0])]
 fixture=b.collections[0];bpy.context.scene.collection.children.link(fixture);bpy.context.view_layer.update()
 def rect(o,off=(0,0,0)):
  pts=[o.matrix_world@Vector(v)+Vector(off) for v in o.bound_box];return [min(v[i] for v in pts) for i in range(3)],[max(v[i] for v in pts) for i in range(3)]
 conflicts=[];checked=[]
 for o in fixture.all_objects:
  if o.type!='MESH':continue
  if 'sink' in id and not(o.name.startswith('Stainless sink bowl bottom') or o.name.startswith('Sink end') or o.name.startswith('Sink side')):continue
  checked.append(o.name);a,b=rect(o,offset)
  for host in c.all_objects:
   if host.type!='MESH':continue
   q,r=rect(host);overlap=[min(b[i],r[i])-max(a[i],q[i]) for i in range(3)]
   if min(overlap)>.0001:conflicts.append([o.name,host.name,overlap])
 assert not conflicts,(slug,conflicts)
 return {'checked':True,'id':id,'version':version,'origin_m':offset,'fixture_meshes_checked':len(checked),'positive_mesh_aabb_intersections':conflicts,'basis':'Actual native rigid component mesh bounds against closed cabinet meshes; countertop, service routes and home installation are separate checks'}

def verify(render):
 if '--asset' not in sys.argv:
  f=ROOT/'library/materials/cream-cabinet-enamel/v001';path=f/'cream-cabinet-enamel.blend';bpy.ops.wm.open_mainfile(filepath=str(path));bpy.ops.wm.read_factory_settings(use_empty=True);c=g.collection('Cream enamel native swatch');m=link_mat('cream-cabinet-enamel');box('Enamel swatch',(0,0,.025),(.50,.35,.05),m,.006);lo,hi=bounds(c)
  if render:preview(c,f,lo,hi,'preview.png')
  jwrite(f/'validation.json',{'fresh_native_reopen':True,'fresh_material_link':True,'dimensions_match_manifest':None,'dimensions_validation_status':'not applicable - material-only asset with no fixed geometry','preview_rendered':(f/'preview.png').exists(),'host_integration_checked':False})
 for slug,(w,d,h,kind,finish,parent) in ASSETS.items():
  if '--asset' in sys.argv and slug!=sys.argv[sys.argv.index('--asset')+1]:continue
  f=folder(slug);path=f/(slug+'.blend');bpy.ops.wm.open_mainfile(filepath=str(path));assert all(lib.filepath.startswith('//') for lib in bpy.data.libraries)
  meta=json.loads((f/'asset.json').read_text());statebounds={}
  for state,name in [('closed',slug+' | v001'),('open',slug+' | open v001')]:
   c=load_for_review(path,name);lo,hi=bounds(c);assert all(Path(bpy.path.abspath(lib.filepath,library=lib.parent)).is_file() for lib in bpy.data.libraries)
   if state=='closed':assert all(abs(hi[i]-lo[i]-meta['dimensions_m'][i])<1e-5 for i in range(3))
   statebounds[state]={'min':lo,'max':hi}
   if render:preview(c,f,lo,hi,'preview.png' if state=='closed' else 'preview-open.png')
  jwrite(f/'validation.json',{'fresh_native_reopen':True,'fresh_closed_and_open_collection_links':True,'relative_dependencies_resolved':True,'dimensions_match_manifest':True,'measured_state_bounds_m':statebounds,'floor_or_mount_contact':abs(statebounds['closed']['min'][2])<.002,'preview_rendered':(f/'preview.png').exists(),'open_preview_rendered':(f/'preview-open.png').exists(),'preview_settings':{'renderer':'Cycles CPU','threads':4,'samples':24},'host_installation_checked':False,'isolated_component_fit':component_fit(slug)})
  print('VERIFIED',slug,flush=True)
if __name__=='__main__':
 if '--verify' in sys.argv:verify('--render' in sys.argv)
 else:publish()
