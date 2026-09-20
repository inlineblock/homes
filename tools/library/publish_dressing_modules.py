"""Reusable premium dressing and open prep-storage modules; immutable original assets.

blender -b --factory-startup --python tools/library/publish_dressing_modules.py
blender -b --factory-startup --python tools/library/publish_dressing_modules.py -- --verify --render
Use --asset <slug> to select one package. Preview rendering is CPU-only.
"""
from pathlib import Path
import bpy,json,math,sys,hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'tools/library')]
from common import geometry as g
from common.timber_materials import grain_uv
from publish_modern_block import box,bounds,linked_mat
GEN='tools/library/publish_dressing_modules.py'
SPECS={
 'oak-open-double-hang-2ft':('cabinetry','Open oak double hanging bay',(.6096,.6096,2.4384),'double'),
 'oak-open-long-hang-2ft':('cabinetry','Open oak long hanging bay',(.6096,.6096,2.4384),'long'),
 'oak-dressing-drawers-shelves-2ft':('cabinetry','Oak dressing drawers and folded shelves',(.6096,.641,.2+2.2384),'drawers'),
 'oak-shoe-tower-2ft':('cabinetry','Open oak shoe tower',(.6096,.4064,2.1336),'shoes'),
 'oak-ventilated-hamper-2ft':('cabinetry','Oak ventilated pullout hamper',(.6096,.642,.87122),'hamper'),
 'full-length-bronze-mirror-24x72':('fixtures','Full length bronze mirror 24x72',(.6096,.03,1.8288),'mirror'),
 'oak-full-height-bookcase-2ft':('cabinetry','Oak full height bookcase 2ft',(.6096,.6096,3.048),'bookcase'),
 'smoked-oak-open-island-base-36in':('cabinetry','Smoked oak open island base 36in',(.9144,.6096,.87122),'island'),
}
def folder(slug):return ROOT/'library'/SPECS[slug][0]/slug/'v001'
def collection_name(slug):return SPECS[slug][1]+' | v001'
def native(slug):return folder(slug)/(slug+'.blend')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rod(name,a,b,r,mat):return g.rod(name,Vector(a)/g.F,Vector(b)/g.F,r/g.F,mat)
def curve(name,points,r,mat):return g.curve(name,[Vector(x)/g.F for x in points],r/g.F,mat)
def parent_path(slug):return ROOT/'library/cabinetry'/slug/'v001'/(slug+'.blend')
def append(path):
 with bpy.data.libraries.load(str(path),link=False) as (src,dst):
  names=[x for x in src.collections if not any(w in x.lower() for w in ('studio','preview'))];assert len(names)==1,names;dst.collections=names
 c=dst.collections[0];bpy.context.scene.collection.children.link(c);return c

def palette():
 return {'oak':linked_mat('coastal-white-oak'), 'dark':g.material('Dressing graphite plinth',(.032,.035,.032),.65), 'metal':g.material('Dressing rail satin bronze',(.13,.10,.065),.32,.8), 'linen':g.material('Dressing warm ivory linen',(.54,.49,.40),.92), 'olive':g.material('Dressing muted olive textile',(.12,.15,.10),.92), 'blue':g.material('Dressing ink blue textile',(.027,.04,.05),.90), 'shoe':g.material('Dressing warm taupe suede',(.105,.074,.046),.85)}

def shell(M,w=.6096,d=.6096,h=2.4384):
 for x in [-w/2+.009,w/2-.009]:box('Dressing oak side',(x,0,h/2),(.018,d,h),M['oak'],.0015)
 box('Dressing oak back',(0,d/2-.009,h/2),(w-.036,.018,h),M['oak'],.001)
 box('Dressing recessed plinth',(0,.025,.05),(w-.04,d-.07,.10),M['dark'],.001)
 for z in [.109,h-.009]:box('Dressing deck',(0,0,z),(w-.036,d-.036,.018),M['oak'],.001)

def wardrobe_parent(slug,M):
 p=parent_path('oak-wardrobe-2ft');c=append(p);g.ACTIVE=c
 for ob in list(c.all_objects):
  if any(t in ob.name.lower() for t in ['hanging rail','upper shelf','hinged oak door','door pull','pull mount']):bpy.data.objects.remove(ob,do_unlink=True)
 for ob in c.all_objects:
  if ob.type=='MESH' and any('oak' in m.name.lower() for m in ob.data.materials if m):ob.data.materials.clear();ob.data.materials.append(M['oak'])
 return c,[{'id':'cabinetry/oak-wardrobe-2ft','version':'v001','native_sha256':sha(p),'method':'Append actual published collection; retain carcass, top/bottom and toe kick. Remove old closed doors, pulls, upper shelf and rail, then install the stated open dressing equipment.'}]

def shelf(M,z,w=.573024,d=.54864,y=.018288,name='Dressing usable shelf'):
 return box(name,(0,y,z),(w,d,.019812),M['oak'],.0015)

def garment(M,x,rail_z,long=False,index=0):
 # Original illustrative clothing, not empty rod capacity labels. Garment plane is YZ.
 cloth=[M['linen'],M['olive'],M['blue']][index%3]
 curve('Clothes hanger metal hook',[(x,0,rail_z+.003),(x,0,rail_z+.035),(x,-.02,rail_z+.045),(x,-.037,rail_z+.025),(x,-.023,rail_z-.022)],.0025,M['metal'])
 z=rail_z-.035
 for a,b in [((x,0,z),(x,-.205,z-.11)),((x,-.205,z-.11),(x,.205,z-.11)),((x,.205,z-.11),(x,0,z))]:rod('Oak clothes hanger',a,b,.006,M['oak'])
 drop=1.36 if long else .60
 shape=[(-.04,0),(-.20,-.07),(-.255,-.22),(-.17,-.26),(-.19,-drop),(.19,-drop),(.17,-.26),(.255,-.22),(.20,-.07),(.04,0)]
 # Two slightly rippled fabric faces with real edge thickness and soft corners.
 verts=[]
 for side in [-1,1]:
  verts += [(x+side*.012+.006*math.sin(j*1.9),y,z-.05+zz) for j,(y,zz) in enumerate(shape)]
 n=len(shape);faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
 mesh=bpy.data.meshes.new('Original folded garment mesh');mesh.from_pydata(verts,[],faces);mesh.materials.append(cloth);mesh.update()
 ob=bpy.data.objects.new('Illustrative long garment' if long else 'Illustrative short garment',mesh);g.ACTIVE.objects.link(ob)
 be=ob.modifiers.new('Soft cloth edges','BEVEL');be.width=.006;be.segments=3;ob.modifiers.new('Garment normals','WEIGHTED_NORMAL')
 return ob

def hanging(kind,M):
 levels=[1.00,2.08] if kind=='double' else [2.08]
 for z in levels:
  rod('Dressing usable hanging rail',(-.273,0,z),(.273,0,z),.012,M['metal'])
  for x in [-.274,.274]:box('Rail end support',(x,0,z),(.012,.04,.04),M['metal'],.003)
  for i,x in enumerate([-.21,-.14,-.07,0,.07,.14,.21]):garment(M,x,z,long=kind=='long',index=i)
 for z in ([1.17,2.21] if kind=='double' else [2.21]):shelf(M,z)
 return {'hanging_rail_centers_z_m':levels,'usable_rail_length_m':.546,'illustrative_garments_per_rail':7,'garment_note':'Original modeled garments demonstrate use extents; not a rated capacity or household storage promise. Garments sit within the native carcass depth.','long_garment_drop_m':1.445 if kind=='long' else None,'short_garment_drop_m':.685 if kind=='double' else None}

def drawer_tower(c,M):
 p=parent_path('oak-drawer-base-2ft');src=append(p)
 kept=[]
 for ob in list(src.objects):
  if ob.name.startswith(('Base cabinet drawer front','Drawer box','Drawer side','Drawer recessed')):
   src.objects.unlink(ob);c.objects.link(ob);kept.append(ob)
  else:bpy.data.objects.remove(ob,do_unlink=True)
 bpy.data.collections.remove(src);g.ACTIVE=c
 fronts=sorted([o for o in kept if o.name.startswith('Base cabinet drawer front')],key=lambda o:o.location.z)
 for ob in kept:
  idx=min(range(3),key=lambda i:abs(ob.location.z-fronts[i].location.z));ob['drawer_group']=idx
  if ob.name.startswith(('Base cabinet drawer front','Drawer recessed')):ob.location.y-=.011
 for i,front in enumerate(fronts):
  z=front.location.z;h=front.dimensions.z
  ob=box('Drawer retained geometry rear closure',(0,.266,z),(.524,.015,max(.045,h-.0518)),M['oak'],.001);ob['drawer_group']=i
 for z in [.92,1.32,1.72,2.12]:shelf(M,z)
 for i,z in enumerate([.96,1.36,1.76]):
  for k in range(3):box('Folded clothing example',(-.11 if i%2==0 else .10,0,z+k*.045),(.28,.34,.04),M['linen'] if k%2 else M['olive'],.009)
 return {'id':'cabinetry/oak-drawer-base-2ft','version':'v001','native_sha256':sha(p),'method':'Append actual published drawer fronts, bases, sides and recessed grips; retain size, add missing rear closures, relocate overlay fronts 11 mm forward for the tall carcass. Publish complete tower separately.'}

def shoe(M,x,y,z):
 # Shaped toe, sole, heel and open collar with original geometry.
 verts=[];faces=[];sections=[(-.135,.019,.032),(-.11,.047,.048),(-.035,.049,.085),(.07,.043,.12),(.13,.035,.102)]
 for yy,w,h in sections:
  for i in range(12):
   a=2*math.pi*i/12;verts.append((x+w*math.cos(a),y+yy,z+.035+h*.45+h*.45*math.sin(a)))
 for k in range(len(sections)-1):
  for j in range(12):faces.append((k*12+j,k*12+(j+1)%12,(k+1)*12+(j+1)%12,(k+1)*12+j))
 faces.extend([tuple(range(11,-1,-1)),tuple(range(48,60))]);me=bpy.data.meshes.new('Original shoe silhouette');me.from_pydata(verts,[],faces);me.materials.append(M['shoe']);me.update();o=bpy.data.objects.new('Illustrative paired shoe',me);g.ACTIVE.objects.link(o)
 for p in me.polygons:p.use_smooth=True
 box('Shoe sole',(x,y,z+.018),(.09,.267,.021),M['dark'],.009)
 box('Shoe collar opening',(x,y+.076,z+.13),(.045,.065,.008),M['dark'],.008)

def shoes(M):
 shell(M,d=.4064,h=2.1336)
 zs=[.17,.43,.69,.95,1.21,1.47,1.73,1.99]
 for i,z in enumerate(zs):
  shelf(M,z,d=.350,y=0,name='Shoe shelf')
  rod('Shoe shelf toe retaining rail',(-.27,-.168,z+.035),(.27,-.168,z+.035),.006,M['metal'])
  if i in [0,1,2,4,6]:
   for x in [-.20,-.09,.09,.20]:shoe(M,x,0,z+.01)
 return {'shoe_shelf_centers_z_m':zs,'shoe_shelf_depth_m':.35,'illustrative_pairs':10,'capacity_basis':'Two illustrative adult shoe pairs across each shown shelf. Actual footwear sizes, taller boots and chosen shelf positions govern real capacity.'}

def bookcase(M):
 shell(M,h=3.048)
 zs=[.12,.49,.86,1.23,1.60,1.97,2.34,2.71]
 colors=[M['linen'],M['olive'],M['blue'],M['shoe']]
 pages=g.material('Book page edges warm paper',(.65,.61,.50),.95)
 for row,z in enumerate(zs):
  if row:shelf(M,z,name='Full height bookcase shelf')
  for j in range(9):
   w=.033+.004*((j+row)%4);h=.19+.021*((j*3+row)%5);x=-.242+j*.056
   box('Original blank book pages',(x,-.13,z+.012+h/2),(w-.003,.205,h-.004),pages,.001)
   box('Original blank book spine',(x,-.235,z+.012+h/2),(w,.007,h),colors[(j+row)%4],.001)
   for dx in [-w/2,w/2]:box('Original book cover',(x+dx,-.13,z+.012+h/2),(.0015,.215,h),colors[(j+row)%4],.0004)
 return {'shelf_centers_z_m':zs,'clear_shelf_depth_m':.54864,'nominal_height_m':3.048,'capacity_note':'Real shelves extend to the top zone; 72 original blank books demonstrate storage. Upper shelves require a safe reach strategy. No titles, cover scans or third-party content.', 'safe_access_assumption':'Shelves above 1.60 m are occasional/overflow use; host must provide clear stable floor space and a selected safe access platform or stepladder. No shelf climbing or rolling-chair access. Actual reach and equipment storage need household review.', 'ceiling_interface':'Topmost geometry Z=3.048m. Host must measure actual finished ceiling height, erection clearance and scribe/infill. Do not push full-height cabinet through ceiling or occupy service/light recesses.'}

def hamper(M):
 shell(M,h=.87122)
 # Pullout basket and slatted ventilated front are a movable coherent group.
 move=[]
 def moving(name,loc,size,mat,bevel=.001):
  ob=box(name,loc,size,mat,bevel);ob['hamper_pullout']=True;move.append(ob);return ob
 for x in [-.29,.29]:moving('Hamper slatted front stile',(x,-.308,.48),(.018,.025,.744),M['oak'])
 for z in [.12,.84]:moving('Hamper slatted front rail',(0,-.308,z),(.562,.025,.023),M['oak'])
 for i in range(17):moving('Hamper ventilation slat',(0,-.308,.155+i*.040),(.562,.022,.023),M['oak'],.0015)
 moving('Hamper pullout floor',(0,-.006,.14),(.51,.51,.022),M['oak'])
 for x in [-.245,.245]:moving('Open hamper liner side',(x,-.005,.445),(.01,.45,.57),M['linen'],.003)
 for y in [-.225,.215]:moving('Open hamper liner end',(0,y,.445),(.48,.01,.57),M['linen'],.003)
 moving('Open hamper liner bottom',(0,-.005,.163),(.48,.43,.012),M['linen'])
 for x in [-.27,.27]:box('Hamper fixed runner',(x,0,.18),(.013,.49,.022),M['metal'],.002)
 handle=rod('Hamper bronze pull',(-.095,-.337,.782),(.095,-.337,.782),.006,M['metal']);handle['hamper_pullout']=True
 for x in [-.08,.08]:ob=rod('Hamper pull standoff',(x,-.32,.782),(x,-.337,.782),.005,M['metal']);ob['hamper_pullout']=True
 return {'basket_clear_plan_m':[.47,.43],'basket_clear_height_m':.55,'front_slats':17,'ventilation_gap_m':.017,'basket_note':'Open-top original fabric liner visualization, not selected hardware or washable product specification.'}

def mirror(M):
 w,h=.6096,1.8288
 # Wall-facing back plane Y=0; no hidden stand or imaginary recess.
 bronze=M['metal'];mirror=g.material('True reflective silver mirror',(.91,.92,.92),.018,1)
 box('Mirror backing',(0,-.004,h/2),(w,.008,h),M['dark'],.001)
 for x in [-w/2+.009,w/2-.009]:box('Mirror slim bronze stile',(x,-.015,h/2),(.018,.03,h),bronze,.0018)
 for z in [.009,h-.009]:box('Mirror slim bronze rail',(0,-.015,z),(w-.036,.03,.018),bronze,.0018)
 box('Reflective mirror face',(0,-.010,h/2),(w-.033,.004,h-.033),mirror,.0005)
 return {'reflective_face_m':[w-.033,h-.033],'back_mounting_plane_y_m':0,'frontmost_plane_y_m':-.03,'mirror_material':'Physically reflective metallic silver, not painted gray','mounting_note':'Host supplies wall blocking, glass safety specification and concealed clips; back plane must align with actual finished wall.'}

def island():
 p=parent_path('smoked-oak-drawer-base-2ft');c=append(p);g.ACTIVE=c
 for ob in list(c.objects):
  if ob.name.startswith(('Drawer ','Shared bronze drawer pull')):bpy.data.objects.remove(ob,do_unlink=True);continue
  if ob.type!='MESH':continue
  if 'cabinet side' in ob.name:ob.location.x+=.1524 if ob.location.x>0 else -.1524
  else:
   for v in ob.data.vertices:v.co.x+=.1524 if v.co.x>0 else -.1524
  grain_uv(ob)
 oak=linked_mat('smoked-oak');box('Island open cubby shelf',(0,0,.455),(.8784,.568,.018),oak,.0015)
 box('Island central shelf support',(0,.012,.485),(.018,.55,.746),oak,.001)
 return c,[{'id':'cabinetry/smoked-oak-drawer-base-2ft','version':'v001','native_sha256':sha(p),'method':'Append actual published carcass. Remove drawer assemblies and pulls; widen fixed carcass panels 304.8 mm, preserving thickness, depth and height; add open mid shelf and center support. Regenerate physical wood UVs. No live instance scaling.'}]

def build(slug):
 kind=SPECS[slug][3];M=palette();derived=[];info={}
 if kind in ['double','long','drawers']:
  c,derived=wardrobe_parent(slug,M)
  if kind in ['double','long']:info=hanging(kind,M)
  else:derived.append(drawer_tower(c,M));info={'drawer_count':3,'upper_shelf_centers_z_m':[.92,1.32,1.72,2.12]}
 elif kind=='island':c,derived=island();info={'open_compartments':4,'doors_or_drawers':0,'shelf_center_z_m':.455,'host_countertop_excluded':True}
 else:
  c=g.collection(collection_name(slug))
  if kind=='shoes':info=shoes(M)
  elif kind=='hamper':info=hamper(M)
  elif kind=='mirror':info=mirror(M)
  elif kind=='bookcase':info=bookcase(M)
 c.name=collection_name(slug);c['asset_id']=SPECS[slug][0]+'/'+slug;c['asset_version']='v001';return c,derived,info

def publish(slug):
 if native(slug).exists():print('PRESERVE',slug,flush=True);return
 bpy.ops.wm.read_factory_settings(use_empty=True);c,derived,info=build(slug);lo,hi=bounds(c);folder(slug).mkdir(parents=True,exist_ok=True)
 bpy.data.libraries.write(str(native(slug)),{c},fake_user=True,path_remap='RELATIVE_ALL')
 kind=SPECS[slug][3];mov=kind in ['drawers','hamper'];travel=.45 if kind=='drawers' else .46 if kind=='hamper' else 0
 deps=[]
 for l in bpy.data.libraries:
  if kind=='mirror':continue
  path=Path(bpy.path.abspath(l.filepath));meta_path=path.parent/'asset.json'
  if meta_path.exists() and ('materials/coastal-white-oak' in str(path) and kind!='island' or 'materials/smoked-oak' in str(path) and kind=='island'):
   m=json.loads(meta_path.read_text());deps.append({'id':m['id'],'version':m['version'],'path':'../../../'+m['id']+'/'+m['version']+'/'+path.name})
 meta={'schema_version':1,'id':SPECS[slug][0]+'/'+slug,'version':'v001','name':collection_name(slug),'units':'meters','dimensions_m':[hi[i]-lo[i] for i in range(3)],'bounds_m':{'min':lo,'max':hi},'blender':{'collection':collection_name(slug)},'placement':{'origin':'Bottom center X at wall mounting plane Y=0, Z=0' if kind=='mirror' else 'Floor center of nominal carcass XY, base Z=0','front_direction':'-Y; width X; up Z','allowed_scaling':'Rigid placement and Z rotation only; no scaling'},'features':info,'installation':{'mounting':'Wall supported mirror; backing plane Y=0' if kind=='mirror' else 'Level supported floor with host anti-tip/wall fixation; no wall-hung claim. Do not overlay separate complete cabinet carcasses.','operating_envelope':{'modeled_state':'Closed movable fronts with open shelving above' if kind=='drawers' else 'Closed ventilated pullout' if kind=='hamper' else 'Open-front fixed storage' if kind!='mirror' else 'Fixed reflective mirror','moving_parts':mov,'intended_front_travel_m':travel,'operator_depth_beyond_open_front_m':.60 if mov else None,'reserve_front_access_m':travel+.60 if mov else .90,'basis':'Original generic geometry and concept standing allowance, not a selected product. Host must test actual movement, opposing fixtures and people/route space.','host_open_state_checked':False},'service_requirements':['Resolve fixing strength, shelf/rail loads, chosen hardware and electrical supply where lighting is added.','Moving drawer/hamper envelope is separate from through-circulation; do not claim two people can pass while open.']},'derived_from':derived[0] if derived else None,'additional_derivations':derived[1:],'dependencies':deps,'source':{'kind':'original derivative' if derived else 'original','generator':GEN,'command':'blender -b --factory-startup --python '+GEN+' -- --asset '+slug},'software':{'blender':bpy.app.version_string},'license':'CC-BY-4.0','rights':'Original Homes project contributors geometry and procedural appearances; attribution Homes project contributors. No manufacturer CAD or third-party content.','files':{'blender':native(slug).name,'preview':'preview.png','validation':'validation.json'},'limitations':'Original concept asset, not a commercially specified system, engineered storage capacity or installation approval. Sample clothes/shoes are illustrative objects, not a household capacity guarantee.'}
 if mov:meta['files']['open_preview']='open-preview.png'
 (folder(slug)/'asset.json').write_text(json.dumps(meta,indent=2)+'\n');print('PUBLISHED',slug,meta['dimensions_m'],flush=True)

def pose_open(c,kind):
 if kind=='drawers':
  for o in c.all_objects:
   if o.get('drawer_group')==2:o.location.y-=.45
 elif kind=='hamper':
  for o in c.all_objects:
   if o.get('hamper_pullout'):o.location.y-=.46
 bpy.context.view_layer.update()

def preview(c,slug):
 kind=SPECS[slug][3];g.collection('Dressing preview studio only');ground=g.material('Dressing studio neutral',(.25,.255,.235),.92)
 box('Studio floor',(0,0,-.026),(200,200,.05),ground)
 h=SPECS[slug][2][2];target=Vector((0,-.03,h*.50));pos=Vector((1.9,-4.3,h*.80+1.0)) if h>1 else Vector((1.6,-2.2,1.55))
 if kind=='bookcase':pos=target+(pos-target)*1.17
 s=bpy.context.scene;s.camera=g.camera('Native dressing preview',pos/g.F,target/g.F,55)
 g.area('Soft dressing key',Vector((-2,-3,4))/g.F,target/g.F,800,3/g.F,(1,.98,.94));g.area('Dressing fill',Vector((3,-1,3))/g.F,target/g.F,420,2/g.F,(.94,.97,1))
 s.world=bpy.data.worlds.new('Dressing neutral world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45
 if kind=='mirror':
  box('Mirror reflected studio wall',(0,-6,1.3),(8,.1,2.6),ground)
  # Two geometric studio cards make the reflection unambiguously reflective.
  box('Mirror reflected soft card',(-1,-5.8,1.5),(.7,.08,1.8),g.material('Reflected warm studio card',(.7,.6,.45),.8))
 s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=3
 s.render.resolution_x=720;s.render.resolution_y=960 if h>1 else 720;s.render.resolution_percentage=100;s.view_settings.view_transform='AgX';s.render.image_settings.file_format='PNG'
 s.render.filepath=str(folder(slug)/'preview.png');bpy.ops.render.render(write_still=True)
 if kind in ['drawers','hamper']:pose_open(c,kind);s.render.filepath=str(folder(slug)/'open-preview.png');bpy.ops.render.render(write_still=True)

def verify(slug,render):
 p=native(slug);before=sha(p);bpy.ops.wm.open_mainfile(filepath=str(p));assert all(l.filepath.startswith('//') for l in bpy.data.libraries)
 bpy.ops.wm.read_factory_settings(use_empty=True)
 with bpy.data.libraries.load(str(p),link=True) as (a,b):assert collection_name(slug) in a.collections;b.collections=[collection_name(slug)]
 c=b.collections[0];bpy.context.scene.collection.children.link(c);lo,hi=bounds(c);meta=json.loads((folder(slug)/'asset.json').read_text())
 assert all(abs(hi[i]-lo[i]-meta['dimensions_m'][i])<1e-5 for i in range(3));assert abs(lo[2])<1e-5
 assert all(Path(bpy.path.abspath(l.filepath)).exists() or Path(bpy.path.abspath(l.filepath,library=l.parent)).exists() for l in bpy.data.libraries)
 kind=SPECS[slug][3]
 if kind in ['double','long']:assert not any('hinged oak door' in o.name for o in c.all_objects);assert len([o for o in c.all_objects if o.name.startswith('Dressing usable hanging rail')])==(2 if kind=='double' else 1)
 if kind=='drawers':assert len([o for o in c.all_objects if o.name.startswith('Base cabinet drawer front')])==3
 if kind=='island':assert not any(o.name.startswith('Drawer ') for o in c.all_objects)
 if kind=='mirror':assert abs(hi[1])<1e-5
 if render:
  bpy.ops.wm.read_factory_settings(use_empty=True)
  with bpy.data.libraries.load(str(p),link=False) as (a,b):b.collections=[collection_name(slug)]
  c=b.collections[0];bpy.context.scene.collection.children.link(c);preview(c,slug)
 assert sha(p)==before
 report={'fresh_native_open':True,'fresh_link':True,'relative_dependencies_resolve':True,'native_sha256':before,'native_unchanged_by_review':True,'actual_dimensions_m':[hi[i]-lo[i] for i in range(3)],'origin_checked':True,'objects':len(c.all_objects),'host_integration_checked':False,'preview_settings':{'renderer':'Cycles CPU','threads':3,'samples':24},'visual_review_pending':True}
 for file in ['preview.png','open-preview.png']:
  if (folder(slug)/file).exists():report[file.replace('.png','')+'_sha256']=sha(folder(slug)/file)
 (folder(slug)/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('VERIFIED',slug,flush=True)

if __name__=='__main__':
 slugs=[sys.argv[sys.argv.index('--asset')+1]] if '--asset' in sys.argv else list(SPECS)
 for slug in slugs:
  if '--verify' in sys.argv:verify(slug,'--render' in sys.argv)
  else:publish(slug)
