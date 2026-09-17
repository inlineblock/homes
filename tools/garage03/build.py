"""Garage Loft 03: original architecture and equipment visualization."""
import bpy,sys,math,json,random
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools'),str(Path(__file__).parent)]
from design import *
from common import geometry as g
from common.geometry import box,cyl,rod,sphere,collection,material,camera,area,F
from common.materials import palette
from common.architecture import mesh,glass_wall,beam,pitched_plate
from common.library import linked_collection,instance
from common.landscape import tree,shrub,grasses
from assets import lift_asset,pool_asset,car
HOME=ROOT/'homes/garage-loft-03'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name!='Collection':bpy.data.collections.remove(c)
M=palette();M['rubber']=material('Graphite tire rubber',(.017,.019,.02),.8);M['car-glass']=material('Smoked coupe glass',(.035,.065,.074),.16,.5);M['red']=material('Ruby tail lamp',(.42,.009,.006),.22);M['green']=material('Muted garden foliage',(.12,.2,.095),.85)
for slug,key in [('warm-vertical-cedar','cedar'),('charcoal-standing-seam','roof')]:
    path=ROOT/'library/materials'/slug/'v001'/f'{slug}.blend'
    with bpy.data.libraries.load(str(path),link=True) as (src,dst):dst.materials=[src.materials[0]]
    M[key]=dst.materials[0]
lift=lift_asset(ROOT,M);pool=pool_asset(ROOT,M)
pendant=linked_collection(ROOT,'fixtures','opal-globe-pendant');stool=linked_collection(ROOT,'furniture','walnut-counter-stool')

def floor(name,x1,y1,x2,y2,z,thick=.4,mat=None):
    return box(name,((x1+x2)/2,(y1+y2)/2,z-thick/2),(x2-x1,y2-y1,thick),mat or M['concrete'],.008)
def wall(name,x1,y1,x2,y2,z,h,mat=None):
    return box(name,((x1+x2)/2,(y1+y2)/2,z+h/2),(x2-x1,y2-y1,h),mat or M['plaster'],.016)
def set_level(c,level):
    for o in c.objects:o['ifc_storey']=level
# Area-bearing floor meshes: ground around pit, pit base, and upper slab minus opening.
c=collection('02 Architecture | floors')
for name,rect in [('Ground front',(0,0,36,3)),('Ground rear',(0,22,36,28)),('Ground west',(0,3,3,22)),('Ground east',(25,3,36,22))]:floor(name,*rect,0)['ifc_storey']='Ground floor'
x1,y1,x2,y2=PIT
pit=floor('Pit base',x1,y1,x2,y2,-PIT_FRONT_DEPTH,.6);pit['ifc_storey']='Parking pit'
# Slope is a thin separate overlay, not counted again in the projected floor area.
for rect in UPPER_SLABS:floor('Upper floor slab',*rect,UPPER_FLOOR,UPPER_FLOOR-GARAGE_CLEAR,M['concrete'])['ifc_storey']='Game room'
c=collection('03 Pit | concrete enclosure')
wall('Pit west',2.5,3,3,22,-PIT_FRONT_DEPTH,PIT_FRONT_DEPTH)
wall('Pit east',25,3,25.5,22,-PIT_FRONT_DEPTH,PIT_FRONT_DEPTH)
wall('Pit rear',3,22,25,22.5,-PIT_FRONT_DEPTH,PIT_FRONT_DEPTH)
wall('Pit front',3,2.5,25,3,-PIT_FRONT_DEPTH,PIT_FRONT_DEPTH)
# Exact 2 inch fall from rear to front of pit.
pitched_plate('Pit drainage slope',3,25,3,22,-PIT_FRONT_DEPTH,-PIT_FRONT_DEPTH,M['concrete'],.015)
# Roof helper slopes x, so create the drainage plane explicitly along y.
mesh('Pit finished slope',[(3,3,-PIT_FRONT_DEPTH+.012),(25,3,-PIT_FRONT_DEPTH+.012),(25,22,-PIT_REAR_DEPTH),(3,22,-PIT_REAR_DEPTH)],[(0,1,2,3)],M['concrete'])
box('Pit collection channel',(14,3.12,-PIT_FRONT_DEPTH+.025),(21.4,.16,.05),M['black'])
set_level(c,'Parking pit')
c=collection('01 Architecture | lower shell')
wall('West ground wall',0,0,.5,28,0,GARAGE_CLEAR)
wall('Rear ground wall',.5,27.5,36,28,0,GARAGE_CLEAR)
wall('East ground wall',35.5,0,36,27.5,0,GARAGE_CLEAR)
wall('Stair separation',27.5,.5,28,27.5,0,GARAGE_CLEAR)
# Pedestrian entrance is separate from lift access.
wall('Entry left pier',25,0,29.5,.5,0,GARAGE_CLEAR)
wall('Entry right pier',33,0,35.5,.5,0,GARAGE_CLEAR)
wall('Entry lintel',29.5,0,33,.5,8,GARAGE_CLEAR-8)
wall('Garage west pier',.5,0,3,.5,0,GARAGE_CLEAR)
wall('Garage lintel',3,0,25,.5,9,GARAGE_CLEAR-9)
set_level(c,'Ground floor')
c=collection('04 Facade | garage doors')
glass_wall('Wide glazed garage door',(3,.17),(25,.17),8.85,M['glass'],M['black'],.08,6)
for z in [2.25,4.5,6.75]:box('Garage door horizontal rail',(14,.13,z),(22,.14,.1),M['black'])
set_level(c,'Ground floor')
c=collection('05 Entry | timber door and canopy')
wall('Separate stair entry',29.55,.16,32.95,.34,.02,7.95,M['cedar']);box('Entry vertical pull',(32.6,-.02,3.55),(.06,.16,1.65),M['black'],.02)
box('Entry canopy',(30.5,-1.8,8.8),(10.5,4.3,.3),M['roof'],.025)
set_level(c,'Ground floor')
c=collection('06 Architecture | upper shell')
# Front: broad recessed glazing framed by timber; exterior walls keep a 9ft room.
wall('Upper front sill',0,0,28,.5,UPPER_FLOOR,2)
wall('Upper front head',0,0,28,.5,UPPER_FLOOR+8.3,.7)
wall('Upper front end',0,0,1,.5,UPPER_FLOOR+2,6.3)
wall('Upper front east jamb',27,0,28,.5,UPPER_FLOOR+2,6.3)
glass_wall('Game room front glazing',(1,.18),(27,.18),UPPER_FLOOR+8.3,M['glass'],M['black'],UPPER_FLOOR+2,7)
wall('Upper west lower',0,.5,.5,28,UPPER_FLOOR,3)
wall('Upper west head',0,.5,.5,28,UPPER_FLOOR+8.2,.8)
wall('Upper west rear',0,21,.5,28,UPPER_FLOOR+3,5.2)
glass_wall('Game room west glazing',(.18,.5),(.18,21),UPPER_FLOOR+8.2,M['glass'],M['black'],UPPER_FLOOR+3,5)
wall('Upper rear',.5,27.5,36,28,UPPER_FLOOR,9)
wall('Upper east',35.5,0,36,27.5,UPPER_FLOOR,9)
wall('Stair tower front',28,0,35.5,.5,UPPER_FLOOR,9)
set_level(c,'Game room')
c=collection('07 Cladding | cedar and fascia')
# Separate actual boards, following solid parts of the shell.
for i in range(72):
    x=.25+i*.5
    if x<28:
        for z,h in [(UPPER_FLOOR+1,2),(UPPER_FLOOR+8.65,.7)]:box('Cedar board',(x,-.07,z),(.475,.16,h),M['cedar'],.008)
    else:box('Cedar board',(x,-.07,UPPER_FLOOR+4.5),(.475,.16,9),M['cedar'],.008)
for i in range(56):
    y=.25+i*.5
    box('East cedar board',(36.07,y,UPPER_FLOOR+4.5),(.16,.475,9),M['cedar'],.008)
    for z,h in [(UPPER_FLOOR+1.5,3),(UPPER_FLOOR+8.6,.8)]:box('West cedar board',(-.07,y,z),(.16,.475,h),M['cedar'],.008)
box('Ground-to-loft shadow reveal',(18,-.19,UPPER_FLOOR-.16),(36.5,.35,.26),M['black'])
set_level(c,'Game room')
c=collection('09 Roof | removable')
box('Low roof',(18,14,22.85),(39,31,.7),M['roof'],.025)
box('Roof edge fascia',(18,-1.48,22.91),(39,.1,.88),M['black'],.01)
for x in range(-1,38):box('Roof standing seam',(x,14,23.225),(.045,31,.075),M['roof'])
set_level(c,'Game room')
c=collection('10 Stairs | protected pedestrian route')
# Two enclosed flights, 13 equal risers each. Upper floor has a real opening.
for i in range(12):
    z=(i+1)*STAIR_RISE;y=STAIR_START+(i+.5)*STAIR_TREAD
    box('Lower flight tread',(29.9,y,z-.06),(3.3,STAIR_TREAD,.12),M['walnut'],.025)
    box('Lower flight riser',(29.9,STAIR_START+i*STAIR_TREAD,z-STAIR_RISE/2),(3.3,.08,STAIR_RISE),M['plaster'])
    z=(14+i)*STAIR_RISE;y=STAIR_LANDING_Y-(i+.5)*STAIR_TREAD
    box('Upper flight tread',(33.65,y,z-.06),(3.3,STAIR_TREAD,.12),M['walnut'],.025)
    box('Upper flight riser',(33.65,STAIR_LANDING_Y-i*STAIR_TREAD,z-STAIR_RISE/2),(3.3,.08,STAIR_RISE),M['plaster'])
floor('Stair mid landing',28,STAIR_LANDING_Y,35.5,STAIR_LANDING_Y+4,UPPER_FLOOR/2,.25,M['walnut'])
for a,b in [((31.6,3.5,3.0),(31.6,14.5,UPPER_FLOOR/2+3)),((32,14.5,UPPER_FLOOR/2+3),(32,3.5,UPPER_FLOOR+3))]:
    rod('Stair handrail',a,b,.055,M['black'])
    for j in range(13):
        p=Vector(a).lerp(Vector(b),j/12);rod('Stair baluster',(p.x,p.y,p.z-3),p,.03,M['black'])
# Guard along the open west edge, with top arrival at front; not a fabricated railing detail.
for y in [3.5+i*.75 for i in range(21)]:rod('Upper stair guard',(28.05,y,UPPER_FLOOR),(28.05,y,UPPER_FLOOR+3.5),.025,M['black'])
rod('Upper stair guard cap',(28.05,3.5,UPPER_FLOOR+3.5),(28.05,18.5,UPPER_FLOOR+3.5),.065,M['black'])
set_level(c,'Ground floor')
c=collection('11 Parking | fixed guides and plant')
for x in [4.75,23.25]:
    for y in [11,14]:box('Lift fixed guide column',(x,y,2.15),(.4,.5,15.6),M['black'],.035)
box('Lift hydraulic cabinet',(26.25,24.8,1.75),(1.9,2.5,3.5),M['black'],.06)
box('Lift control station',(26.2,2,3.8),(.75,.25,1),M['steel'],.04)
for i in range(36):box('Pit caution stripe',(3.3+i*.61,2.83,.025),(.32,.3,.025),M['black'] if i%2 else M['terracotta'])
c=collection('12 Parking | moving carriage and cars')
o=instance('Double parking carriage | stored',lift,(*LIFT_CENTER,0));o['lift_moves']=True
paints=[material('Coupe pearl',(.69,.73,.7),.23,.55),material('Coupe forest',(.015,.09,.055),.25,.65),material('Coupe bronze',(.32,.12,.04),.25,.65),material('Coupe graphite',(.07,.08,.09),.25,.65)]
for i,(x,z) in enumerate([(CAR_CENTERS[0],0),(CAR_CENTERS[1],0),(CAR_CENTERS[0],-PLATFORM_SPACING),(CAR_CENTERS[1],-PLATFORM_SPACING)]):
    for o in car('Car '+str(i+1),x,12.5,z,paints[i],M):o['lift_moves']=True
c=collection('13 Game room | furnishings')
instance('Eight foot pool table',pool,(*POOL_CENTER,UPPER_FLOOR))
# Lounge stays entirely east of the cue-clear envelope (x=17.17).
box('Lounge rug',(22.45,12.9,UPPER_FLOOR+.025),(8.6,10.3,.05),M['fabric'],.06)
for y in [10.2,12.5,14.8]:
    box('Lounge sofa cushion',(25.9,y,UPPER_FLOOR+1.45),(2.5,2.2,.55),M['fabric'],.22)
box('Lounge sofa back',(27.15,12.5,UPPER_FLOOR+2.45),(.5,7.7,2.1),M['fabric'],.2)
box('Lounge coffee table',(22.35,12.5,UPPER_FLOOR+1.15),(3.6,4.5,.2),M['walnut'],.12)
for x in [21.05,23.65]:
    for y in [10.9,14.1]:rod('Coffee table leg',(x,y,UPPER_FLOOR),(x,y,UPPER_FLOOR+1.1),.065,M['black'])
# Media screen on rear wall, clear of table play rectangle.
box('Media screen',(21.8,27.12,UPPER_FLOOR+5.2),(8.4,.15,4.65),M['black'],.1)
box('Media credenza',(21.8,26.4,UPPER_FLOOR+1.25),(9.2,1.75,2.5),M['walnut'],.04)
for x in [4.7,7.2,9.7]:
    box('Refreshment cabinet',(x,26.25,UPPER_FLOOR+1.5),(2.45,2.25,3),M['walnut'],.025)
box('Refreshment counter',(7.2,26.2,UPPER_FLOOR+3.08),(7.6,2.4,.16),M['stone'],.025)
for x in [4.5,7.2,9.9]:instance('Shared walnut counter stool',stool,(x,23.5,UPPER_FLOOR),math.pi)
# Pool-light suspension and original pendants reused from the shared library.
for y in [10.3,14.7]:instance('Shared opal billiard pendant',pendant,(10.5,y,UPPER_FLOOR+8.6))
for i in range(4):rod('Wall cue rack',(1.25+i*.27,26.9,UPPER_FLOOR+1.6),(1.25+i*.27,26.9,UPPER_FLOOR+6.43),.027,M['fir'])
# Small writing/gaming desk in rear stair wing, isolated from cue travel.
box('Gaming desk',(32.5,25.8,UPPER_FLOOR+2.45),(4.8,2.5,.18),M['walnut'],.025)
for x in [30.6,34.4]:box('Gaming desk support',(x,25.8,UPPER_FLOOR+1.2),(.15,2,2.4),M['black'])
set_level(c,'Game room')
c=collection('14 Comfort | dedicated heat pump')
box('Game room heat pump head',(18,27.15,UPPER_FLOOR+7.65),(3.8,.7,1.1),M['white'],.15)
box('Heat pump discharge grille',(18,26.76,UPPER_FLOOR+7.42),(3.3,.025,.18),M['black'],.015)
box('Outdoor heat pump unit',(38,23,1.9),(3.4,1.4,2.7),M['white'],.08)
fan=cyl('Outdoor fan grille',(38,22.26,1.9),1,.06,M['black'],48);fan.rotation_euler.x=math.pi/2
rod('Heat pump line cover',(36.5,24,2),(36.5,24,UPPER_FLOOR+7.5),.065,M['white'])
box('Outdoor equipment pad',(38,23,.22),(4.5,3,.44),M['concrete'],.04)
set_level(c,'Game room')
c=collection('15 Landscape | site illustration')
# Ground ring leaves an actual void under the lift; cutaway hides site pieces.
for rect in [(-90,-80,90,0),(-90,28,90,90),(-90,0,0,28),(36,0,90,28)]:floor('Illustrative site',*rect,-.17,.25,M['soil'])
floor('Driveway',1,-35,27,-.05,-.02,.18,M['concrete'])
for y in [-3,-6.5,-10,-13.5]:floor('Entry paver',29,y,34,y+2.7,.015,.12,M['stone'])
for i,(x,y,h) in enumerate([(-12,17,20),(-14,36,24),(46,34,22),(49,8,18)]):tree('Garden tree',x,y,h,M['fir'],M['green'],80+i)
for i in range(24):
    x=-3.5 if i<12 else 40.8;y=(i%12)*2.9-4
    shrub('Low planting',x,y,1.2+(i%3)*.2,M['green'],i+12)
    grasses('Garden grass',x+1.8,y+.8,1.2,M['leaves'],i+30)
c=collection('16 Lighting and cameras')
world=bpy.data.worlds.new('Garage garden sky');bpy.context.scene.world=world;world.use_nodes=True
n=world.node_tree.nodes;l=world.node_tree.links;sky=n.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_elevation=math.radians(24);sky.sun_rotation=math.radians(220);l.new(sky.outputs[0],n.get('Background').inputs['Color']);n.get('Background').inputs['Strength'].default_value=.28
area('Upper softbox',(12,9,UPPER_FLOOR+8.4),(12,12,UPPER_FLOOR),1500,12)
area('Garage broad light',(14,8,11.7),(14,14,0),1800,15)
area('Game room fill',(22,21,UPPER_FLOOR+8.4),(17,12,UPPER_FLOOR+2),1100,8)
camera('01 Exterior',(60,-67,34),(18,11,9),45)
camera('02 Game room',(24,2.5,UPPER_FLOOR+6.3),(10.4,15,UPPER_FLOOR+2.5),23)
camera('03 Garage stored',(14,-19,5),(14,14,-1.2),25)
camera('04 Pit section',(56,-53,24),(17,11,5),43)
camera('05 Raised retrieval',(14,-22,9),(14,12,3),25)
s=bpy.context.scene;s.camera=bpy.data.objects['01 Exterior'];s.render.engine='CYCLES';s.cycles.samples=64;s.cycles.use_denoising=True;s.cycles.max_bounces=8
try:
    p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
    for d in p.devices:d.use=d.type=='METAL'
    s.cycles.device='GPU'
except Exception:pass
s.unit_settings.system='IMPERIAL';s.unit_settings.length_unit='FEET';s.unit_settings.scale_length=1
s.render.resolution_x=1800;s.render.resolution_y=1300;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=-.55
s['home_id']='garage-loft-03';s['stage']='Concept; KLAUS planning proxy, not manufacturer installation';s['gross_enclosed_area_sqft']=GROSS_AREA
s['parking_spaces']=4;s['bedrooms']=0;s['bathrooms']=0;s['upper_floor_ft']=UPPER_FLOOR
(HOME/'outputs/work').mkdir(parents=True,exist_ok=True);s.render.filepath='//../outputs/images/01-exterior.png'
bpy.context.preferences.filepaths.save_version=0
path=HOME/'model/garage-loft-03.blend';bpy.ops.wm.save_as_mainfile(filepath=str(path));bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(path))
meta=json.loads((HOME/'project.json').read_text())
meta.update({'gross_enclosed_area_sqft':GROSS_AREA,'footprint_sqft':FOOTPRINT,'upper_floor_projected_slab_sqft':UPPER_SLAB_AREA})
meta['lift'].update({'pit_depth_front_inches':PIT_FRONT_DEPTH*12,'pit_depth_rear_inches':PIT_REAR_DEPTH*12,'garage_clear_height_ft':GARAGE_CLEAR,'car_proxy_ft':[CAR_WIDTH,CAR_LENGTH,CAR_HEIGHT]})
meta['software']['blender']=bpy.app.version_string
(HOME/'project.json').write_text(json.dumps(meta,indent=2)+'\n')
print('GARAGE_SAVED',len(s.objects),flush=True)
