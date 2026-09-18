"""Mountain House: road-level living and garage, wooded downhill walkout."""
import bpy,sys,math,json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(Path(__file__).parent),str(ROOT/'tools')]
from design import *
from common import geometry as g
from common.geometry import box,cyl,rod,area,camera,collection,F
from common.architecture import mesh,beam,glass_wall,interior_wall
from common.library import linked_collection,instance
from assets import mats,conifer
from common.furnishings import soft,chair,sofa,bed,bowl
HOME=ROOT/'homes'/SLUG
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name!='Collection':bpy.data.collections.remove(c)
M=mats(ROOT)
from common.shared_assets import load_catalog,place
CAT=load_catalog(ROOT,keys=['grass','shrub','paver','wardrobe','base_cabinet','oven','dishwasher','cooktop','hood','fridge','fireplace','bathtub','toilet'])
def label(o,kind,level=0):
    o['ifc_class']=kind;o['ifc_storey']='Walkout basement' if level<0 else 'Ground floor';return o

def at_level(fn,z,*args):
    before=set(bpy.data.objects);result=fn(*args)
    for o in set(bpy.data.objects)-before:o.location.z+=z*F;o['ifc_storey']='Walkout basement' if z<0 else 'Ground floor'
    return result

collection('02 Architecture | enclosed floors with stair opening')
for level,rects in [(MAIN,MAIN_SLABS),(LOWER,LOWER_SLABS)]:
    for i,(a,b,c,d) in enumerate(rects):label(box('Main floor' if level==0 else 'Walkout floor',((a+c)/2,(b+d)/2,level-.35),(c-a,d-b,.7),M['stone']), 'IfcSlab',level)
collection('01 Architecture | timber envelope and real apertures')
def clad(name,a,b,z0,z1):
    # Continuous backing plus separate vertical timber boards with fine joints.
    x1,y1=a;x2,y2=b;L=math.dist(a,b);ux=(x2-x1)/L;uy=(y2-y1)/L
    sloped=not ux and z1>10 and z0>=0
    if sloped:
        vv=[(x1-.25,y1,z0),(x1+.25,y1,z0),(x2+.25,y2,z0),(x2-.25,y2,z0),(x1-.25,y1,roof_z(y1)),(x1+.25,y1,roof_z(y1)),(x2+.25,y2,roof_z(y2)),(x2-.25,y2,roof_z(y2))]
        label(mesh(name+' sloped backing',vv,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],M['cedar']),'IfcWall',z0)
    else:label(box(name+' backing',((x1+x2)/2,(y1+y2)/2,(z0+z1)/2),(L if ux else .5,L if uy else .5,z1-z0),M['cedar']), 'IfcWall',z0)
    n=math.ceil(L/.49)
    for i in range(n):
        x=x1+ux*(i+.5)*L/n;y=y1+uy*(i+.5)*L/n
        top=roof_z(y) if sloped else z1
        # Offset wood to both faces, with visible exterior relief.
        for side in [-1,1]:
            label(box(name+' cedar board',(x+uy*.266*side,y+ux*.266*side,(z0+top)/2),(L/n-.018 if ux else .05,L/n-.018 if uy else .05,top-z0-.025),M['cedar'],.006),'IfcCovering',z0)
def glazing(name,a,b,base,head,sill=.1,panels=None):
    before=set(bpy.data.objects);glass_wall(name,a,b,base+head,M['glass'],M['dark'],base+sill,panels)
    for o in set(bpy.data.objects)-before:label(o,'IfcWindow',base)
# Main front: integrated garage, foyer, timber screen and private bath windows.
for a,b in [(0,2),(22,33),(39,47),(57,60)]:clad('Front timber wall',(a,.2),(b,.2),0,10.5)
clad('Primary bath high window sill',(47,.2),(57,.2),0,7)
clad('Primary bath high window head',(47,.2),(57,.2),9.2,10.5)
glazing('Primary bath privacy clerestory',(47,.2),(57,.2),0,9.2,7,3)
clad('Garage door header',(2,.2),(22,.2),8.5,10.5)
for row in range(18):box('Timber sectional garage door',(12,.30,(row+.5)*8.5/18),(19.8,.22,8.5/18-.02),M['cedar'],.008)
for x in [2,22]:box('Garage jamb',(x,.0,4.25),(.13,.16,8.5),M['dark'])
clad('Entry header',(33,.2),(39,.2),8.7,10.5)
glazing('Entry sidelight',(36.7,.17),(39,.17),0,8.7,.05,1)
d=box('Open oak front door',(33.12,1.95,4.25),(.16,3.5,8.5),M['oak'],.02);label(d,'IfcDoor')
rod('Entry pull',(33.0,3.3,3.5),(33.0,3.3,5.2),.025,M['dark'])
# Side elevations with actual daylight openings.
clad('West garage side',(.2,0),(.2,24),0,roof_z(12))
clad('West rear corner',(.2,38),(.2,40),0,roof_z(39))
clad('West fireplace backing',(.2,24),(.2,32),0,roof_z(28))
clad('West living header',(.2,32),(.2,38),9.2,roof_z(35))
glazing('West living panorama',(.2,32),(.2,38),0,9.2,.1,2)
for a,b in [(0,10),(22,29),(33.5,40)]:clad('East timber wall',(59.8,a),(59.8,b),0,roof_z((a+b)/2))
clad('Primary side sill',(59.8,10),(59.8,22),0,2.4)
clad('Primary side head',(59.8,10),(59.8,22),9,roof_z(16))
glazing('Primary forest window',(59.8,10),(59.8,22),0,9,2.4,3)
clad('Side deck door header',(59.8,29),(59.8,33.5),8.5,roof_z(31))
glazing('Side deck door fixed leaf',(59.8,29),(59.8,31),0,8.5,.08,1)
# Rear two opening living bays and raised kitchen picture window.
for a,b in [(0,3),(21,24),(39,42),(58,60)]:clad('Rear timber pier',(a,39.8),(b,39.8),0,roof_z(40))
for a,b in [(3,21),(24,39)]:
    clad('Rear timber transom',(a,39.8),(b,39.8),9.2,roof_z(40))
    w=(b-a)/3
    # Three real stacked sliding leaves at left: 2/3 aperture remains open.
    for i in range(3):glazing('Stacked rear sliding glass',(a,39.5+i*.17),(a+w,39.5+i*.17),0,9.2,.10,1)
    box('Recessed multi-slide track',((a+b)/2,39.8,.015),(b-a,.58,.045),M['dark'])
clad('Kitchen rear sill',(42,39.8),(58,39.8),0,3.3)
clad('Kitchen rear head',(42,39.8),(58,39.8),9.2,roof_z(40))
glazing('Kitchen forest panorama',(42,39.8),(58,39.8),0,9.2,3.3,4)
# Lower walls follow the L-shaped occupied footprint. Front is deliberately buried service area.
for a,b in [((24,0),(60,0)),((24,0),(24,24)),((0,24),(24,24))]:clad('Lower retained envelope',a,b,LOWER,-.7)
clad('Lower west corner',(.2,24),(.2,28),LOWER,-.7)
clad('Lower west rear corner',(.2,38),(.2,40),LOWER,-.7)
clad('Lower west sill',(.2,28),(.2,38),LOWER,LOWER+2)
clad('Lower west head',(.2,28),(.2,38),LOWER+8.5,-.7)
glazing('Lower bedroom02 side daylight',(.2,28),(.2,38),LOWER,8.5,2,3)
clad('Lower east buried',(59.8,0),(59.8,28),LOWER,-.7)
clad('Lower east rear corner',(59.8,38),(59.8,40),LOWER,-.7)
clad('Lower east sill',(59.8,28),(59.8,38),LOWER,LOWER+2)
clad('Lower east head',(59.8,28),(59.8,38),LOWER+8.5,-.7)
glazing('Lower bedroom03 side daylight',(59.8,28),(59.8,38),LOWER,8.5,2,3)
for a,b in [(0,2),(16,20),(39,43),(58,60)]:clad('Lower rear wood pier',(a,39.8),(b,39.8),LOWER,-.7)
for a,b in [(2,16),(20,39),(43,58)]:
    clad('Lower rear timber head',(a,39.8),(b,39.8),LOWER+8.5,-.7)
    if a==20:
        glazing('Walkout lounge glass',(20,39.8),(31,39.8),LOWER,8.5,.1,3)
        glazing('Walkout lounge stacked leaf',(31,39.8),(35,39.8),LOWER,8.5,.1,1)
    else:glazing('Lower bedroom forest glass',(a,39.8),(b,39.8),LOWER,8.5,.4,4)
# Private room partitions and actual 3ft+ doors.
for z,walls in [(MAIN,MAIN_WALLS),(LOWER,LOWER_WALLS)]:
    for name,a,b,ops in walls:
        before=set(bpy.data.objects);at_level(interior_wall,z,name,a,b,ops,M['plaster'],10.1)
        for o in set(bpy.data.objects)-before:label(o,'IfcWall',z)
        length=math.dist(a,b);ux=(b[0]-a[0])/length;uy=(b[1]-a[1])/length
        for off,w in ops:
            loc=(a[0]+ux*(off+.10)+uy*(w/2)*(-1 if name=='Primary west' and off==10.3 else 1),a[1]+uy*(off+w-.10 if name=='Mudroom east' and off==1.8 else off+.10)+ux*(w/2)*(-1 if name in ['Lower utility rear','Primary bath rear','Primary WC rear'] else 1),z+3.75)
            label(box(name+' open door',loc,(.13 if ux else w-.18,w-.18 if ux else .13,7.5),M['oak'],.015),'IfcDoor',z)
# Garage wall separation and lower slab perimeter concrete are conceptual assemblies.
collection('07 Finishes | wood floors and exposed plinth')
for a,b,c,d in MAIN_SLABS:
    if b==0:
        box('Main oak floor finish',((max(a,24)+c)/2,(b+d)/2,.012),(c-max(a,24),d-b,.025),M['oak'])
    else:box('Main oak floor finish',((a+c)/2,(b+d)/2,.012),(c-a,d-b,.025),M['oak'])
for a,b,c,d in LOWER_SLABS:box('Lower oak floor finish',((a+c)/2,(b+d)/2,LOWER+.012),(c-a,d-b,.025),M['oak'])
box('Rear charcoal foundation plinth',(30,40,-11.45),(60,.5,.6),M['dark'],.02)
box('Main continuous ceiling',(30,20,10.18),(60,40,.16),M['ceiling'])
# Structurally legible timber deck: broad rear terrace and side return.
collection('08 Structure | elevated timber deck and stair')
for a,b,c,d in DECKS:
    label(box('Deck structural zone',((a+c)/2,(b+d)/2,-.55),(c-a,d-b,.8),M['dark']), 'IfcSlab')
    count=math.ceil((d-b)/.48)
    for j in range(count):label(box('Thermo ash spaced deck board',((a+c)/2,b+(j+.5)*(d-b)/count,-.065),(c-a,(d-b)/count-.018,.13),M['deck'],.008),'IfcCovering')
for x in [2,20,40,58,67]:
    top=-.7;bottom=grade(x,53.4)
    label(box('Rear deck timber post',(x,53.4,(top+bottom)/2),(.78,.78,top-bottom),M['cedar'],.035),'IfcColumn',LOWER)
    box('Deck post steel shoe',(x,53.4,bottom+.17),(.87,.87,.34),M['dark'],.012)
    for direction in [-1,1]:label(beam('Deck timber knee brace',(x,53.4,-4),(x+direction*2.5,53.4,-.85),.38,.38,M['cedar']),'IfcBeam',LOWER)
label(box('Rear deck continuous beam',(34,53.4,-.94),(68,.78,1.1),M['cedar'],.02),'IfcBeam')
for y in [20,36]:
    z=grade(67,y);label(box('Side deck support post',(67,y,(z-.7)/2),(.78,.78,-.7-z),M['cedar'],.025),'IfcColumn',LOWER)
def guard(name,a,b,base=0):
    L=math.dist(a,b);n=math.ceil(L/5);ux=(b[0]-a[0])/L;uy=(b[1]-a[1])/L
    for i in range(n+1):
        x=a[0]+(b[0]-a[0])*i/n;y=a[1]+(b[1]-a[1])*i/n
        label(box(name+' slim post',(x,y,base+1.75),(.115,.115,3.5),M['dark'],.01),'IfcRailing')
    for i in range(n):
        x=a[0]+(b[0]-a[0])*(i+.5)/n;y=a[1]+(b[1]-a[1])*(i+.5)/n
        label(box(name+' clear infill',(x,y,base+1.72),(L/n-.15 if ux else .025,L/n-.15 if uy else .025,3.13),M['glass']),'IfcRailing')
    label(beam(name+' timber cap',(*a,base+3.5),(*b,base+3.5),.18,.20,M['deck']),'IfcRailing')
for a,b in [((.2,40),(.2,53.8)),((.2,53.8),(67.8,53.8)),((67.8,18.2),(67.8,53.8)),((60,18.2),(67.8,18.2))]:guard('Deck edge',a,b)
# Partial pergola over outdoor dining, retaining an open sky lounge to its west.
for x in [22,42]:
    for y in [40.8,52.8]:label(box('Pergola timber post',(x,y,5.1),(.55,.55,10.2),M['cedar'],.02),'IfcColumn')
    label(box('Pergola main beam',(x,46.8,10.25),(.5,13.7,.75),M['cedar'],.025),'IfcBeam')
for i in range(18):box('Open pergola timber slat',(32,40.2+i*.78,10.70),(22,.21,.38),M['cedar'],.015)
# U stair: two 10-riser flights, a real middle landing, clear main floor opening.
for i in range(9):
    z=LOWER+(i+1)*RISE;y=STAIR_START+(i+.5)*TREAD
    label(box('Lower stair tread',(26,y,z-.08),(3.7,TREAD+.04,.16),M['oak'],.012),'IfcStairFlight',LOWER)
    z=-5.5+(i+1)*RISE;y=STAIR_LANDING-(i+.5)*TREAD
    label(box('Upper stair tread',(30,y,z-.08),(3.7,TREAD+.04,.16),M['oak'],.012),'IfcStairFlight')
label(box('Stair intermediate landing',(28,STAIR_LANDING+2.2,-5.64),(7.7,4.4,.28),M['oak'],.012),'IfcSlab',LOWER)
# Simple closed risers preserve tread sequence.
for x,startz,sign in [(26,LOWER,1),(30,-5.5,-1)]:
    for i in range(10):
        y=STAIR_START+i*TREAD if sign==1 else STAIR_LANDING-i*TREAD
        box('Stair closed timber riser',(x,y,startz+i*RISE+RISE/2),(3.7,.08,RISE),M['oak'])
for a,b in [((32,12),(32,27)),((24,27),(32,27)),((24,12),(28,12))]:guard('Stair opening guard',a,b)
for x,z1,z2,y1,y2 in [(24.2,-7.7,-2.2,12,20.25),(31.8,3.3,-2.2,12,20.25)]:rod('Stair continuous handrail',(x,y1,z1),(x,y2,z2),.075,M['oak'])
# Roof: low mono-pitch with deep wood soffit, real standing seams and frontal runoff.
collection('09 Roof | wood soffit and low standing seam')
x1,x2,y1,y2=-2.5,62.5,-3,43
verts=[(x1,y1,roof_z(y1)+.45),(x2,y1,roof_z(y1)+.45),(x2,y2,roof_z(y2)+.45),(x1,y2,roof_z(y2)+.45)]
label(mesh('Standing seam roof plate',verts+[(x,y,z-.32) for x,y,z in verts],[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],M['roof']),'IfcRoof')
verts=[(x1,y1,roof_z(y1)),(x2,y1,roof_z(y1)),(x2,y2,roof_z(y2)),(x1,y2,roof_z(y2))]
mesh('Timber soffit plane',verts,[(3,2,1,0)],M['cedar'])
for x in range(-2,63):beam('Roof raised standing seam',(x,y1,roof_z(y1)+.47),(x,y2,roof_z(y2)+.47),.04,.10,M['roof'])
for a,b in [((x1,y1),(x2,y1)),((x2,y1),(x2,y2)),((x2,y2),(x1,y2)),((x1,y2),(x1,y1))]:beam('Deep timber roof fascia',(*a,roof_z(a[1])+.06),(*b,roof_z(b[1])+.06),.18,.5,M['cedar'])
box('Front roof gutter',(30,-3.22,10.28),(65,.38,.35),M['dark'],.025)
for x in [-2,62]:rod('Roof downpipe',(x,-3.3,10.1),(x,-3.3,.5),.11,M['dark']);rod('Roof discharge elbow',(x,-3.3,.5),(x,-4.3,.25),.11,M['dark'])
# Furniture and utility program.
from interior import furnish
furnish(M,CAT,at_level)
from details import install
install(ROOT,M)
# Original forest and actual hillside; shared understory collections at grade.
from site_model import site
site(ROOT,M,CAT)
from site_finish import finish_site
finish_site(ROOT,M)
collection('10 Lighting and cameras')
world=bpy.data.worlds.new('Clear mountain afternoon');bpy.context.scene.world=world;world.use_nodes=True
n=world.node_tree.nodes;l=world.node_tree.links;sky=n.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_elevation=math.radians(31);sky.sun_rotation=math.radians(65);sky.sun_size=math.radians(1.5);sky.air_density=.85;sky.dust_density=.3;l.new(sky.outputs[0],n.get('Background').inputs['Color']);n.get('Background').inputs['Strength'].default_value=.35
for x in [12,32,51]:area('Warm living daylight bounce',(x,35,9),(x,26,1),350,10,(1,.91,.78))
area('Sheltered patio soft daylight',(45,55,-2),(40,40,-6),500,18,(.9,.95,1))
area('Lower lounge daylight bounce',(30,36,-2),(30,28,-10),450,12,(1,.91,.78))
views={'01 Forest rear':((109,114,24),(30,29,1),43),'02 Road arrival':((89,-94,25),(30,8,3),46),'03 Deck living':((64,65,7.5),(29,39,5),28),'04 Walkout patio':((67,76,-5),(30,38,-5),35),'05 Hillside section':((118,72,24),(30,24,-.5),48),'06 Kitchen':((39,27,6),(52,36,4.5),23),'07 Primary bath':((43,8.5,6.5),(54.5,5,3.5),19),'08 Kitchen appliances':((40,37.3,6.2),(54,29.1,4.1),24)}
for name,args in views.items():camera(name,*args)
from refinements import polish
polish(ROOT,M,clad,glazing)
from common.timber_materials import apply_grain
apply_grain([M['cedar'],M['deck']])
for o in bpy.context.scene.objects:
    if o.type=='CURVE' and not o.library:
        # Keep the four refined faucet outlets open; other curved solids are capped.
        o.data.use_fill_caps=not o.name.startswith(('Primary vanity faucet','Refined Lower shared bath faucet','Refined Powder faucet'))
s=bpy.context.scene;s.camera=bpy.data.objects[VIEWS[0][0]];s.unit_settings.system='IMPERIAL';s.unit_settings.length_unit='FEET';s.unit_settings.scale_length=1
s.render.engine='CYCLES';s.cycles.samples=512;s.cycles.use_denoising=True;s.cycles.adaptive_threshold=.008;s.cycles.max_bounces=12;s.cycles.transmission_bounces=12;s.cycles.glossy_bounces=6
s.render.resolution_x=3200;s.render.resolution_y=2000;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=-.35
s['home_id']=SLUG;s['gross_enclosed_area_sqft']=GROSS;s['bedrooms']=3;s['bathrooms']=2.5;s['stage']='Architectural concept; site and engineering unverified';s.render.filepath='//../outputs/images/01-forest-rear.png'
for screen in bpy.data.screens:
    for ar in screen.areas:
        if ar.type=='VIEW_3D':ar.spaces.active.region_3d.view_perspective='CAMERA'
HOME.joinpath('model').mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(HOME/'model/mountain-house.blend'));bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(HOME/'model/mountain-house.blend'))
# Exact linked dependency inventory, including transitive material dependencies.
deps=[]
for lib in bpy.data.libraries:
    p=Path(bpy.path.abspath(lib.filepath)).resolve()
    if p.is_relative_to(ROOT/'library'):
        rel=p.parent.relative_to(ROOT/'library');deps.append({'id':'/'.join(rel.parts[:-1]),'version':rel.parts[-1],'path':'../../library/'+str(rel)+'/'})
meta={'schema_version':1,'id':SLUG,'name':'Mountain House','status':'Detailed visualization and dimensioned architectural concept','units':'meters','display_units':'feet-inches','target_area_sqft':CONDITIONED,'gross_enclosed_area_sqft':GROSS,'conditioned_gross_area_sqft':CONDITIONED,'area_basis':'Main 2280 sqft net of 120 sqft stair opening, plus lower L-shaped 1824 sqft = 4104 sqft gross including walls and 576 sqft garage; conditioned gross 3528 sqft. Deck 1128 sqft, patio, eaves and landscape excluded.','bedrooms':3,'bathrooms':2.5,'storeys':[{'name':'Ground floor','elevation_m':0},{'name':'Walkout basement','elevation_m':LOWER*F}],'assumptions':'Two levels total as requested. Three bedrooms and 2.5 baths chosen for concept; illustrative forest slope and front road, no actual parcel.','software':{'blender':bpy.app.version_string,'bonsai':'0.8.5'},'asset_dependencies':deps,'site_concept':{'road':'Front, at main/garage level','terrain':'Falls through building depth to lower rear walkout; local patio grading bench','parking':'24 x 24 ft integrated garage with 20 ft door and 27 ft approach','deck':'14 ft deep full rear deck, 8 ft east return; partial pergola and shaded walkout patio','roof':'Low mono-pitch; concept gutter/downpipes; product, snow load, drainage and waterproofing unverified'},'deliverables':{'presentation_model':'model/mountain-house.blend','architectural_model':'model/mountain-house.ifc','primary_render':'outputs/images/01-forest-rear.png','floor_plan':'outputs/plans/main-floor.svg','presentation_sheet':'outputs/plans/design-board.pdf'}}
(HOME/'project.json').write_text(json.dumps(meta,indent=2)+'\n');print('MOUNTAIN_MODEL_SAVED',len(s.objects),GROSS,flush=True)
