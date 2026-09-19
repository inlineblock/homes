"""Original shared Modern Block components; metric geometry, immutable version pins.

/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python tools/library/publish_modern_block.py
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python tools/library/publish_modern_block.py -- --verify --render
"""
from pathlib import Path
import bpy, json, math, random, sys
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from common import geometry as g
from common.materials import noise_material
from common.timber_materials import grain_uv
GEN='tools/library/publish_modern_block.py'
ASSETS={
 'broad-canopy-oak':('landscape','Broad canopy oak | shared v001'),
 'timber-pivot-louver-1800x3000':('openings','Timber pivot louver 1800x3000 | shared v001'),
 'courtyard-pool-4x8m':('fixtures','Courtyard pool 4x8m | shared v001'),
}
def folder(slug):return ROOT/'library'/ASSETS[slug][0]/slug/'v001'
def box(name,loc,size,mat,bevel=0):return g.box(name,[v/g.F for v in loc],[v/g.F for v in size],mat,bevel/g.F)
def mesh(name,verts,faces,materials):
 d=bpy.data.meshes.new(name);d.from_pydata(verts,[],faces);d.update()
 for m in materials:d.materials.append(m)
 o=bpy.data.objects.new(name,d);g.ACTIVE.objects.link(o);return o

def linked_mat(slug,version='v001'):
 path=ROOT/'library/materials'/slug/version/(slug+'.blend')
 with bpy.data.libraries.load(str(path),link=True) as (a,b):b.materials=[a.materials[0]]
 return b.materials[0]

def bounds(c):
 bpy.context.view_layer.update();pts=[o.matrix_world@Vector(v) for o in c.all_objects if o.type in ['MESH','CURVE'] for v in o.bound_box]
 return [min(p[i] for p in pts) for i in range(3)],[max(p[i] for p in pts) for i in range(3)]

def tapered_branch(name,points,radii,mat):
 # Explicit irregular taper rings, continuous fork overlap, real bark surface.
 verts=[];faces=[];n=10
 for i,(p,r) in enumerate(zip(points,radii)):
  p=Vector(p);t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)]);t.normalize();u=t.cross(Vector((0,0,1)))
  if u.length<.01:u=Vector((1,0,0))
  u.normalize();v=t.cross(u).normalized()
  for j in range(n):
   a=2*math.pi*j/n;rr=r*(1+.07*math.sin(j*3+i*.5));verts.append(tuple(p+rr*(math.cos(a)*u+math.sin(a)*v)))
 for i in range(len(points)-1):
  for j in range(n):faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 faces.extend([tuple(range(n-1,-1,-1)),tuple((len(points)-1)*n+j for j in range(n))]);o=mesh(name,verts,faces,[mat])
 for p in o.data.polygons:p.use_smooth=True
 return o

def tree():
 rng=random.Random(31857)
 bark=noise_material('Oak bark | original deeply textured gray umber',(.047,.038,.025),(.14,.12,.079),7,.95,.017)
 leaves=[]
 for i,col in enumerate([(.018,.045,.014),(.031,.070,.024),(.051,.095,.032),(.066,.12,.044),(.09,.14,.052)]):
  m=g.material('Oak leaf tonal family %d'%i,col,.64);p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Subsurface Weight'].default_value=.045;p.inputs['Subsurface Radius'].default_value=(.25,.7,.15);leaves.append(m)
 tapered_branch('Gnarled trunk',[(0,0,.02),(.12,-.04,.65),(.17,.12,1.45),(-.08,.13,2.35),(.0,.08,3.05)],[.49,.40,.35,.29,.21],bark)
 for j in range(7):
  a=j*math.tau/7; tapered_branch('Root flare',[(math.cos(a)*.91,math.sin(a)*.91,.035),(math.cos(a)*.42,math.sin(a)*.42,.15),(.10,.03,.66)],[.035,.14,.19],bark)
 verts=[];faces=[];mat_ids=[]
 def leaf(p,d,length):
  # Petiole joins a folded lanceolate leaf, with midrib ridge and pointed tip.
  d=Vector(d).normalized();u=d.cross(Vector((0,0,1)))
  if u.length<.01:u=Vector((1,0,0))
  u.normalize();normal=d.cross(u).normalized();ang=rng.uniform(-1.1,1.1);u=u*math.cos(ang)+normal*math.sin(ang);normal=d.cross(u).normalized();p=Vector(p);w=length*.29;k=len(verts)
  verts.extend([tuple(p),tuple(p+d*length*.48+u*w),tuple(p+d*length*.53+normal*.009),tuple(p+d*length),tuple(p+d*length*.48-u*w)])
  faces.extend([(k,k+1,k+2),(k+1,k+3,k+2),(k+3,k+4,k+2),(k+4,k,k+2)]);mi=rng.choices(range(5),[.2,.32,.25,.18,.05])[0];mat_ids.extend([mi]*4)
 for i in range(17):
  inner=i>=9
  a=(i-9 if inner else i)*math.tau/(8 if inner else 9)+rng.uniform(-.18,.18);start=Vector((.02,.08,(2.6 if inner else 2.0)+rng.uniform(0,.9)));r=rng.uniform(.9,1.7) if inner else rng.uniform(2.45,3.45);end=Vector((r*math.cos(a),r*math.sin(a),rng.uniform(4.8,5.5) if inner else rng.uniform(3.6,4.9)));mid=start.lerp(end,.47)+Vector((0,0,-.14))
  tapered_branch('Spreading primary limb %02d'%i,[start,mid,end],[.21,.15,.067],bark)
  for j in range(5):
   a2=a+(j-2)*.28+rng.uniform(-.18,.18);base=mid.lerp(end,.30+j*.145);reach=rng.uniform(.7,1.25) if inner else rng.uniform(1.25,2.05);tip=base+Vector((reach*math.cos(a2),reach*math.sin(a2),rng.uniform(.35,1.35)))
   tapered_branch('Secondary crown limb',[base,base.lerp(tip,.50)+Vector((0,0,.13)),tip],[.063,.041,.016],bark)
   for k in range(5):
    a3=a2+(k-2)*.51+rng.uniform(-.2,.2);twigbase=base.lerp(tip,.42+k*.12);length=rng.uniform(.60,1.20);twig=twigbase+Vector((length*math.cos(a3),length*math.sin(a3),rng.uniform(.2,.9)))
    tapered_branch('Foliated fine branch',[twigbase,twigbase.lerp(twig,.5),twig],[.015,.008,.002],bark)
    for q in range(7):
     bud=twigbase.lerp(twig,.22+q*.12);ang=a3+(1 if q%2 else -1)*rng.uniform(.65,1.65);growth=Vector((math.cos(ang),math.sin(ang),rng.uniform(-.25,.7)))*rng.uniform(.22,.43);tip2=bud+growth
     tapered_branch('Leaf bearing twig',[bud,tip2],[.0028,.0006],bark)
     for l in range(11):
      p=bud.lerp(tip2,.12+l*.079);side=1 if l%2 else -1;d=growth.normalized()*.35+Vector((-growth.y,growth.x,0)).normalized()*side*.8+Vector((0,0,rng.uniform(-.20,.40)))
      leaf(p,d,rng.uniform(.10,.17))
 o=mesh('Individual attached dark green leaves',verts,faces,leaves)
 for i,p in enumerate(o.data.polygons):p.material_index=mat_ids[i]
 return {'dependencies':[], 'placement':{'origin':'Trunk base at XY 0,0 and planting grade Z=0; natural root flare extends approximately 75mm below grade','front_direction':'Botanical form has no front; Z up','allowed_scaling':'Uniform 0.9 to 1.1 scale and Z rotation for natural variation; no nonuniform scale'},'mounting':'Plant trunk base at host grade; protect a deliberate root/soil zone and keep canopy clear of openings.','clearances':{'canopy_radius_m':6.1,'root_zone_basis':'Unspecified illustrative planting; arborist assessment required for an actual retained or installed specimen','host_checked':False},'product_status':'Original illustrative broad spreading oak-like botanical geometry. Not a species identification, nursery product, climate suitability statement or model of an actual protected tree.','modeled_state':'Static original trunk, attached branching twigs and individually folded leaves; no billboard textures'}

def louver():
 wood=linked_mat('warm-vertical-cedar','v003');metal=g.material('Louver pivot metal | original dark bronze',(.044,.037,.028),.38,.75)
 # Leaf is centered on its vertical pivot axis; host rotates the linked instance.
 for x in [-.8725,.8725]:box('Timber perimeter stile',(x,0,1.5),(.055,.12,3),wood,.004)
 for z in [.04,2.96]:box('Timber top bottom rail',(0,0,z),(1.69,.12,.08),wood,.004)
 for i in range(22):box('Actual vertical timber louver %02d'%i,(-.817+i*1.634/21,0,1.50),(.042,.105,2.84),wood,.003)
 for z in [.0,3.0]:
  o=g.cyl('Vertical center pivot pin',(0,0,z/g.F),.014/g.F,.03/g.F,metal)
 for o in g.ACTIVE.all_objects:
  if o.type=='MESH' and wood in list(o.data.materials):grain_uv(o)
 return {'dependencies':[{'id':'materials/warm-vertical-cedar','version':'v003','path':'../../../materials/warm-vertical-cedar/v003/warm-vertical-cedar.blend'}], 'placement':{'origin':'Bottom-center vertical pivot axis at XY 0,0, Z=0. Pivot pins project 15mm beyond frame top/bottom.','front_direction':'+Y; closed panel width along X; Z up','allowed_scaling':'Rigid instance placement only. Rotate whole linked collection instance around local Z to open; do not scale panel dimensions.'},'mounting':'Concept center-pivot leaf requires head and sill bearing supports supplied by host. Leaf frame 1.8m wide x3.0m high; host provides >=3.04m clear pin space and suitable fixings.','operating_envelope':{'state':'Closed, leaf lies in XZ plane','intended_angle_degrees':90,'swept_radius_m':.903,'z_min_m':-.015,'z_max_m':3.015,'basis':'Actual closed leaf corner radius sqrt(0.9^2+0.06^2); 90-degree center pivot concept','host_open_state_checked':False},'clearances':{'adjacent_leaf_center_pitch_min_m':1.82,'standing_access_m':.90,'basis':'Concept assumptions; host must check all simultaneous positions, wind locking, pinch protection and cleaning'},'product_status':'Original editable timber solar/privacy screen; no certified facade, wind load or fire rating','modeled_state':'22 individual vertical blades and structural perimeter frame; pins on center axis; whole leaf is movable in host'}

def pool():
 plaster=noise_material('Courtyard pool mineral plaster',(.25,.42,.43),(.44,.61,.60),75,.62,.001)
 stone=linked_mat('coastal-honed-limestone');water=g.material('Courtyard clear water surface | IOR 1.333',(.71,.9,.92),.09)
 p=water.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.333
 n=water.node_tree.nodes;l=water.node_tree.links;t=n.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=34;t.inputs['Detail'].default_value=2;b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.13;b.inputs['Distance'].default_value=.006;l.new(t.outputs['Fac'],b.inputs['Height']);l.new(b.outputs['Normal'],p.inputs['Normal'])
 box('Pool floor',(0,0,-1.55),(4.40,8.4,.2),plaster,.02)
 for x in [-2.1,2.1]:box('Pool side shell',(x,0,-.725),(.20,8.4,1.45),plaster,.01)
 for y in [-4.1,4.1]:box('Pool end shell',(0,y,-.725),(4,.20,1.45),plaster,.01)
 for x in [-2.16,2.16]:box('Coping long side',(x,0,.035),(.32,8.64,.07),stone,.013)
 for y in [-4.16,4.16]:box('Coping end',(0,y,.035),(4,.32,.07),stone,.013)
 for i in range(4):
  h=1.23-i*.28;box('Submerged entry step %02d'%i,(-.91,-3.78+i*.42,-1.45+h/2),(2.12,.44,h),plaster,.015)
 mesh('Clear water single surface at -130mm',[(-1.998,-3.998,-.13),(1.998,-3.998,-.13),(1.998,3.998,-.13),(-1.998,3.998,-.13)],[(0,1,2,3)],[water])
 return {'derived_from':{'id':'fixtures/rectangular-pool-6x12m','version':'v001','source':'library/fixtures/rectangular-pool-6x12m/v001/generate.py','changes':'Distinct 4x8m water footprint, 1.45m clear depth, 2.12m wide submerged steps, linked limestone coping, water is a single transparent surface below coping rather than solid blue geometry'},'dependencies':[{'id':'materials/coastal-honed-limestone','version':'v001','path':'../../../materials/coastal-honed-limestone/v001/coastal-honed-limestone.blend'}],'placement':{'origin':'Water footprint center XY; host deck datum Z=0. Shell bottom -1.65m, coping top +.07m, water -.13m.','front_direction':'Steps at -Y end; long axis Y; Z up','allowed_scaling':'Rigid placement and Z rotation only; do not stretch shell'},'mounting':'Excavate/omit host ground and deck across full 4.4x8.4m shell footprint down to -1.65m. Deck must not fill the visible pool cavity.','clearances':{'suggested_deck_clearance_m':1.5,'basis':'Concept circulation allowance; actual structure, barrier, drainage, hydraulics and safety design unresolved','host_checked':False},'modeled_state':'Open hollow shell with four real submerged steps, separate coping ring and transparent water surface below deck','product_status':'Original schematic pool; not construction documentation or an engineered commercial product'}

BUILD={'broad-canopy-oak':tree,'timber-pivot-louver-1800x3000':louver,'courtyard-pool-4x8m':pool}
def publish():
 for slug,(category,name) in ASSETS.items():
  if '--asset' in sys.argv and slug!=sys.argv[sys.argv.index('--asset')+1]:continue
  f=folder(slug);native=f/(slug+'.blend')
  if native.exists():print('PRESERVE existing',slug,flush=True);continue
  bpy.ops.wm.read_factory_settings(use_empty=True);c=g.collection(name);c['asset_id']=category+'/'+slug;c['asset_version']='v001';meta=BUILD[slug]();lo,hi=bounds(c);f.mkdir(parents=True,exist_ok=True)
  bpy.data.libraries.write(str(native),{c},fake_user=True,path_remap='RELATIVE_ALL')
  meta.update(schema_version=1,id=category+'/'+slug,version='v001',name=name,units='meters',dimensions_m=[hi[i]-lo[i] for i in range(3)],bounds_m={'min':lo,'max':hi},blender={'collection':name},license='CC-BY-4.0',rights='Original Homes project contributor geometry and procedural appearance; attribution Homes project contributors. No listing imagery, third-party mesh or manufacturer CAD.',source={'kind':'original','generator':GEN,'command':'blender -b --factory-startup --python '+GEN+' -- --asset '+slug},software={'blender':bpy.app.version_string},files={'blender':native.name,'preview':'preview.png','validation':'validation.json'})
  (f/'asset.json').write_text(json.dumps(meta,indent=2)+'\n');print('PUBLISHED',slug,meta['dimensions_m'],flush=True)

def preview(c,f,lo,hi):
 g.collection('Isolated neutral native preview');center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3));s=bpy.context.scene;target=center
 if f.parent.name=='courtyard-pool-4x8m':
  # Surround at actual deck datum, with an actual hole; never cover pool cavity.
  m=g.material('Preview surround warm gray',(.40,.40,.37),.9)
  for x in [-5.16,5.16]:box('Open surround side',(x,0,-.075),(5.68,16,.15),m)
  for y in [-6.16,6.16]:box('Open surround end',(0,y,-.075),(4.64,3.68,.15),m)
  target=Vector((0,0,-.2));campos=Vector((9,-12,11.7));lens=46
 else:
  m=g.material('Preview neutral ground',(.40,.41,.39),.92);box('Neutral ground',(0,0,min(lo[2],0)-.035),(span*100,span*100,.05),m)
  campos=center+Vector((span*.84,span*1.5,span*.75));lens=48
 cam=g.camera('Native asset camera',campos/g.F,target/g.F,lens);s.camera=cam
 g.area('Broad soft daylight',Vector((-span,span,span*1.8))/g.F,target/g.F,span*span*105,span*1.2/g.F,(1,.97,.92));g.area('Cool fill',Vector((span,-span,span))/g.F,target/g.F,span*span*28,span/g.F,(.9,.95,1))
 s.world=bpy.data.worlds.new('Neutral world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.55,.58,.62,1);s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45
 s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=20;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=760;s.render.resolution_y=650;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(f/'preview.png');s.view_settings.view_transform='AgX';s.view_settings.exposure=0;bpy.ops.render.render(write_still=True)

def verify(render):
 for slug,(category,name) in ASSETS.items():
  if '--asset' in sys.argv and slug!=sys.argv[sys.argv.index('--asset')+1]:continue
  f=folder(slug);native=f/(slug+'.blend');bpy.ops.wm.open_mainfile(filepath=str(native));assert all(l.filepath.startswith('//') for l in bpy.data.libraries)
  bpy.ops.wm.read_factory_settings(use_empty=True)
  with bpy.data.libraries.load(str(native),link=True) as (a,b):b.collections=[name]
  c=b.collections[0];bpy.context.scene.collection.children.link(c);lo,hi=bounds(c);meta=json.loads((f/'asset.json').read_text());assert all(abs(hi[i]-lo[i]-meta['dimensions_m'][i])<1e-4 for i in range(3));assert all(Path(bpy.path.abspath(l.filepath,library=l.parent)).exists() for l in bpy.data.libraries)
  water_check=None
  if slug=='courtyard-pool-4x8m':
   water=[o for o in c.all_objects if o.name.startswith('Clear water')][0];assert all(abs(v.co.z+.13)<1e-5 for v in water.data.vertices);assert len(water.data.polygons)==1
   water_check={'water_z_m':-.13,'coping_top_m':.07,'water_is_single_surface':True,'open_cavity':True,'host_terrain_hole_checked':False}
  if render:preview(c,f,lo,hi)
  (f/'validation.json').write_text(json.dumps({'fresh_native_open':True,'fresh_link':True,'relative_dependencies_resolve':True,'bounds_m':{'min':lo,'max':hi},'objects':len(c.all_objects),'preview_rendered':(f/'preview.png').exists(),'preview_settings':{'renderer':'Cycles CPU','threads':4,'samples':20,'color_management':'AgX','exposure':0},'pool_cavity_checks':water_check,'host_integration_checked':False},indent=2)+'\n');print('VERIFIED',slug,flush=True)
if __name__=='__main__':
 if '--verify' in sys.argv:verify('--render' in sys.argv)
 else:publish()
