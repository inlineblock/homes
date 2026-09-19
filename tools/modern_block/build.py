"""Reproducible Modern Block architectural concept, all design dimensions in meters."""
import sys,math,json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(Path(__file__).parent),str(ROOT/'tools')]
import bpy
from mathutils import Vector
from common import geometry as g
from common.library import linked_collection
from common.finish_palette import palette
from common.timber_materials import apply_grain
from utils import *
import design as d
from envelope import build_envelope,wall,cut,roof
HOME=ROOT/'homes'/d.SLUG
for p in ['model','outputs/work','outputs/images','outputs/plans','assets']:(HOME/p).mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
 if c.name!='Collection':bpy.data.collections.remove(c)
M=palette(ROOT)
M['cedar']=material(ROOT,'warm-vertical-cedar','v003');M['roof']=material(ROOT,'charcoal-facade-panel');M['earth']=M['sand']
OPENINGS=build_envelope(ROOT,M)
(HOME/'model/opening-schedule.json').write_text(json.dumps(OPENINGS,indent=2)+'\n')
from interiors import build_interiors,CAMERAS as ICAMERAS
usage=build_interiors(ROOT,M)
# True-size linked recessed fittings with actual ceiling recesses.
g.collection('07 Lighting | recessed and task fixtures')
dl=linked_collection(ROOT,'fixtures','lighting-recessed-downlight-3in','v001')
points=[(x,y,3.265) for x in [12.0,16,20] for y in [2.5,6.0,9.5] if not (d.STAIR_VOID[0]<x<d.STAIR_VOID[2] and d.STAIR_VOID[1]<y<d.STAIR_VOID[3])]
points += [(x,y,6.52) for x,y in [(11.5,2),(15.3,2),(11.5,5.5),(15.3,5.5),(18.5,2),(20.5,2),(18.5,4.3),(12,9),(12,13),(12,16),(19,14),(20.7,16)]]
points += [(-5,y,3.17) for y in [2,7,11]]
for x,y,z in points:
 instance('Recessed ambient fitting',dl,(x,y,z))
 # Concept ceiling housing is 95mm deep; actual lighting products unselected.
 for ceiling in list(bpy.context.scene.objects):
  if ceiling.type!='MESH' or 'ceiling' not in ceiling.name.lower():continue
  bpy.context.view_layer.update();bs=[ceiling.matrix_world@Vector(v) for v in ceiling.bound_box]
  if min(v.x for v in bs)<x+.043 and max(v.x for v in bs)>x-.043 and min(v.y for v in bs)<y+.043 and max(v.y for v in bs)>y-.043 and abs(min(v.z for v in bs)-z)<.1:
   cut(ceiling,(x-.0432,y-.0432,x+.0432,y+.0432),z-.03,z+.1,M)
# Foundation plinths close the gap between the elevated finished floors and grade.
g.collection('08 Structure | foundation plinths')
for label,r in [('Main',d.MAIN),('Guest',d.GUEST),('Garage',d.GARAGE)]:
 x0,y0,x1,y1=r;tag(box(label+' foundation',((x0+x1)/2,(y0+y1)/2,-.48),(x1-x0,y1-y0,.52),M['stone'],.01),'IfcFooting')
# Linked natural landscape and usable court.
g.collection('12 Landscape | planted forecourt and pool')
keys={'tree':('landscape','broad-canopy-oak','v001'),'grass':('landscape','ornamental-grass-clump','v002'),'shrub':('landscape','sage-shrub','v002'),'paver':('surfaces','honed-limestone-paver-4ft','v001'),'pool':('fixtures','courtyard-pool-4x8m','v001'),'louver':('openings','timber-pivot-louver-1800x3000','v001'),'chaise':('furniture','slatted-outdoor-chaise','v001'),'outdoor_sofa':('furniture','coastal-outdoor-sofa','v001'),'outdoor_chair':('furniture','coastal-outdoor-lounge-chair','v001')}
assets={k:linked_collection(ROOT,*v) for k,v in keys.items()}
site=box('Illustrative site grade',(5,8,-.73),(300,300,.4),M['earth'],.02)
# Excavation removes solid earth inside the swimming basin.
cut(site,(2.75,8.75,7.25,17.25),-2,.2,M)
# Raised court deck uses perimeter regions rather than a slab across the basin.
for name,r in [('Lanai',d.LANAI),('West pool walk',(0,5,2.68,20)),('East pool walk',(7.32,5,10,20)),('Pool entry deck',(2.68,5,7.32,8.68)),('Pool far deck',(2.68,17.32,7.32,20))]:
 x0,y0,x1,y1=r;box(name+' terrace substrate',((x0+x1)/2,(y0+y1)/2,-.28),(x1-x0,y1-y0,.56),M['stone'],.012)
 # Full linked tile modules, host-cut perimeter strips with same physical shader.
 step=1.225
 for ix in range(math.ceil((x1-x0)/step)):
  for iy in range(math.ceil((y1-y0)/step)):
   w=min(1.2192,x1-(x0+ix*step));h=min(1.2192,y1-(y0+iy*step))
   if min(w,h)<.01:continue
   x=x0+ix*step+w/2;y=y0+iy*step+h/2
   if abs(w-1.2192)<.002 and abs(h-1.2192)<.002:instance('Terrace linked limestone paver',assets['paver'],(x,y,.005))
   else:box('Terrace boundary-cut paver',(x,y,-.01),(w,h,.03),M['stone'],.003)
instance('Courtyard pool',assets['pool'],(5,13,0))
# Stepping path through gravel from anonymous street edge to both entrances.
for x0 in [4.2,20.45]:
 for i in range(0 if x0==4.2 else 1,5):instance('Front garden stepping paver',assets['paver'],(x0,-2.2-i*1.40,-.48))
for x,y,s in [(3,-6.3,1.08),(-10,1,.92),(25,21,1.1)]:instance('Mature courtyard canopy',assets['tree'],(x,y,-.53),.22,s)
rng=random.Random(20260919)
for i in range(560):
 x=rng.uniform(-12,26);y=rng.uniform(-10,24)
 # Keep house/court, driveway, front path and stair landings free.
 occupied=(-8.8<x<22.7 and -.7<y<20.8) or (18.5<x<22.4 and -3<y<0)
 path=(abs(x-4.2)<.9 or abs(x-20.45)<1.2) and y<0
 driveway=x<-8 and y>10
 if occupied or path or driveway:continue
 k='shrub' if i%3==0 else 'grass';instance('Forecourt native concept planting',assets[k],(x,y,-.53),rng.random()*6.28,rng.uniform(.75,1.1))
from site_context import enrich_site
site_review=enrich_site(ROOT,M,assets)
# Small planted courtyard beds create living texture without blocking the pool walk.
for x,y,w,h in [(1.35,6.8,2.1,2.8),(5,19.1,3.8,1.3)]:
 box('Courtyard planted ground',(x,y,.025),(w,h,.07),M['grass'],.04)
 for i in range(18):
  px=x+rng.uniform(-w/2+.15,w/2-.15);py=y+rng.uniform(-h/2+.15,h/2-.15)
  instance('Courtyard grasses',assets['grass'],(px,py,.07),rng.random()*6.28,rng.uniform(.45,.75))
# Garage side court and road; neutral unmarked context.
box('Side arrival drive',(-12.7,15,-.20),(9.5,14,.15),M['stone'],.02)
box('Illustrative road',(5,-13,-.6),(68,4.5,.12),M['roof'])
# Clear two-car envelopes in garage, shown as subdued schematic vehicle bodies.
for y in [14.05,17.85]:
 # These are dimension reservations, intentionally not detailed generic car assets.
 obj=box('Parking reservation 4.8x1.9m',(-3.6,y,-.075),(4.8,1.9,.018),M['dark']);obj['reservation']='Vehicle footprint, not a car model';obj.hide_render=True
# Lanai center-pivot louvered leaves; two operating states rendered from same camera.
g.collection('08 Structure | lanai and louver screens')
for x in [.1,2,4,6,8,9.9]:tag(box('Lanai slender steel post',(x,0,1.65),(.09,.09,3.3),M['dark'],.01),'IfcColumn')
for i in range(5):
 obj=instance('Pivot screen '+str(i+1),assets['louver'],(1+i*2,0,.12),math.radians(75));obj['operating_state']='Open 75 degrees';obj['closed_z_rotation']=0.0;obj['open_z_rotation']=math.radians(75)
# Lanai furniture leaves 1.05m unobstructed behind leaf sweep.
instance('Lanai sofa',assets['outdoor_sofa'],(4.9,3.9,0),math.pi)
instance('Lanai lounge chair',assets['outdoor_chair'],(1.8,3.6,0),-.5)
for y in [10.3,14.2]:instance('Pool chaise',assets['chaise'],(1.35,y,.01),0)
# Private covered upper balcony over the pool-side terrace, sized independently.
g.collection('08 Structure | covered upper balcony')
box('Balcony floor',(8.5,13,3.48),(3,8,.24),M['stone'],.012)
for x,y in [(7,9),(7,17)]:tag(box('Balcony slender support',(x,y,3.3),(.12,.12,6.6),M['dark'],.01),'IfcColumn')
roof('Covered balcony',(6.9,9,10,17.1),6.65,M,'Upper floor')
for a,b in [((7,9),(7,17)),((7,9),(10,9)),((7,17),(10,17))]:
 wall('Balcony glass guard',a,b,3.6,1.06,M['glass'],.016,'Upper floor');rod('Balcony guard cap',(a[0],a[1],4.67),(b[0],b[1],4.67),.016,M['bronze'])
for y in [10.6,15]:instance('Balcony lounge chair',assets['outdoor_chair'],(8.4,y,3.6),math.pi/2)
# Human-scale exterior illumination without theatrical exposure.
g.collection('20 Cameras and illumination')
CAMS={
 '13-east-arrival':((38,-18,5.0),(19,6,3),35),
 '01-front-arrival':((28,-34,3.8),(8,3,2.6),43),
 '02-courtyard-pool':((2.1,24,3.1),(11,6,2.8),26),
 '03-roof-and-site':((-30,34,28),(6,9,1.5),42),
 '04-lanai-open':((9,-7,1.8),(4.6,4,1.7),26),
 '05-kitchen':((14.3,12.5,1.62),(12.8,17.2,1.35),21),
 '06-living':((17.8,6.6,1.62),(18.7,3.3,1.25),20),
 '07-primary-bedroom':((16.1,6,5.2),(13.2,2.7,4.65),24),
 '08-primary-bath':((17.4,1.95,5.25),(20,3.8,4.65),20),
 '09-lanai-closed':((9,-7,1.8),(4.6,4,1.7),26),
 '10-pool-and-balcony':((1,19,2.7),(9.8,11.5,3.1),25),
 '12-bath-tub-shower':((17.55,4.4,5.15),(20.2,1.3,4.5),22),
 '11-stair-gallery':((16.1,10,5.2),(20.5,10.7,4.4),22),
}
for name,(loc,target,lens) in CAMS.items():camera(name,loc,target,lens)
world=bpy.data.worlds.new('Neutral late-afternoon sky');world.use_nodes=True;bpy.context.scene.world=world
n=world.node_tree.nodes;l=world.node_tree.links;sky=n.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_elevation=math.radians(42);sky.sun_rotation=math.radians(215);sky.sun_disc=False
sat=n.new('ShaderNodeHueSaturation');sat.inputs['Saturation'].default_value=.35;l.new(sky.outputs['Color'],sat.inputs['Color']);l.new(sat.outputs[0],n.get('Background').inputs['Color']);n.get('Background').inputs['Strength'].default_value=.16
sun=bpy.data.lights.new('Late afternoon soft sun','SUN');sun.energy=3;sun.angle=.1;o=bpy.data.objects.new(sun.name,sun);g.ACTIVE.objects.link(o);o.rotation_euler=(.6,-.45,-.55)
area('Broad front fill',(9,-8,14),(8,5,3),1800,15,(1,.97,.92))
for x,y in [(5,3),(12.5,15),(16,4),(13.2,3),(20,2)]:area('Soft interior bounce',(x,y,2.95 if x!=13.2 else 6.3),(x,y,0 if x!=13.2 else 3.6),85,2.5,(1,.87,.70))
area('Primary bath soft daylight',(20,2,6.2),(19.6,3,4.25),320,3.0,(1,.96,.91))
area('Primary bath vanity light',(18.7,3.9,6.2),(18.7,4.5,4.5),110,1.8,(1,.89,.76))
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_denoising=True;scene.cycles.max_bounces=8;scene.cycles.transmission_bounces=8;scene.cycles.transparent_max_bounces=8
scene.render.resolution_x=1800;scene.render.resolution_y=1200;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=0
scene.camera=bpy.data.objects['01-front-arrival'];scene.render.filepath='//../outputs/work/01-front-arrival.png';scene['bedrooms']=4;scene['concept_stage']='Independent architectural concept with user-authorized creative infill';scene['source_references']='Anonymous visual direction; no identifying source data stored'
apply_grain([M['cedar']])
# Meter-scale assets are linked at true scale except explicitly declared facade adaption and plants.
native=HOME/'model/modern-block.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native))
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath))
bpy.ops.wm.save_as_mainfile(filepath=str(native))
deps=[]
for lib in bpy.data.libraries:
 p=Path(bpy.path.abspath(lib.filepath)).resolve();meta=p.parent/'asset.json'
 if meta.exists():
  a=json.loads(meta.read_text());deps.append({'id':a['id'],'version':a['version'],'path':'../../'+str(p.parent.relative_to(ROOT))+'/'})
meta={'schema_version':1,'id':d.SLUG,'name':'Modern Block','status':'architectural concept; dimensions and unseen layout interpreted','units':'meters','display_units':'feet-inches','bedrooms':4,'bathrooms':3.5,'gross_enclosed_area_sqft':round((d.CONDITIONED_M2+d.GARAGE_M2)/.3048**2,4),'conditioned_gross_area_sqft':round(d.CONDITIONED_M2/.3048**2,1),'garage_area_sqft':round(d.GARAGE_M2/.3048**2,1),'area_basis':'Gross occupied floor plates including wall footprints, minus upper stair void; gross enclosed adds garage. Excludes courtyard, pool, lanai, balcony, roof and exterior terraces. Concept dimensions.','storeys':[{'name':'Ground floor','elevation_m':0},{'name':'Upper floor','elevation_m':3.6}],'software':{'blender':bpy.app.version_string,'bonsai':'0.8.5','ifcopenshell':'0.8.5'},'asset_dependencies':deps,'deliverables':{'presentation_model':'model/modern-block.blend','building_model':'model/modern-block.ifc','gallery':'outputs/README.md','ground_plan':'outputs/plans/ground-floor.png','upper_plan':'outputs/plans/upper-floor.png'},'authoring':{'build':'Blender --background --python tools/modern_block/build.py','render':'Blender --background homes/modern-block/model/modern-block.blend --python tools/modern_block/render.py','plans':'python3 tools/modern_block/draw_plans.py'}}
(HOME/'project.json').write_text(json.dumps(meta,indent=2)+'\n')
from schedule import write_schedule
write_schedule(ROOT, deps)
print('MODERN_BLOCK_SAVED',native,'conditioned_m2',d.CONDITIONED_M2,flush=True)
