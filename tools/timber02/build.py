"""Timber Courtyard 02: exterior-led native scene from the user's reference."""
import bpy,sys,math,random,json,argparse
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(Path(__file__).parent))
from design import *
from common import geometry as g
from common.geometry import box,cyl,sphere,rod,area,camera,collection,material,F
from common.materials import palette,noise_material
from common.architecture import mesh,pitched_plate,beam,glass_wall,interior_wall
from common.landscape import tree,shrub,grasses,rock
from common.library import linked_collection,instance,publish_material
random.seed(84)
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-home',type=Path,help='Write an isolated review build instead of the current home.')
parser.add_argument('--render',action='store_true')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
HOME=args.output_home.resolve() if args.output_home else ROOT/'homes/timber-courtyard-02'
(HOME/'model').mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name!='Collection':bpy.data.collections.remove(c)
M=palette()
cedar=noise_material('Thermally toned cedar',(.105,.039,.013),(.36,.18,.068),3.4,.55,.0006,(8,8,.24))
M['cedar']=publish_material(ROOT,'warm-vertical-cedar',cedar,{'name':'Warm vertical cedar','board_module_m':.1524,'nominal_board_width_inches':6,'gap_m':.004,'description':'Original procedural timber shader; pair with six-inch board geometry.'})
metal=noise_material('Charcoal standing-seam metal',(.045,.055,.058),(.085,.096,.102),90,.38,.0002)
M['roof']=publish_material(ROOT,'charcoal-standing-seam',metal,{'name':'Charcoal standing-seam metal','seam_spacing_m':.3048,'raised_seam_height_m':.03048,'description':'Original procedural coated-metal shader; roof meshes use twelve-inch seam spacing.'})
M['mulch']=noise_material('Fine dark bark mulch',(.025,.019,.009),(.11,.073,.036),100,1,.015)
M['green']=material('Deep garden foliage',(.035,.10,.024),.67)
M['silver']=material('Silver sage foliage',(.15,.21,.12),.7)
M['grass']=material('Bronze green grasses',(.22,.25,.085),.65)
M['maple']=material('Burgundy maple foliage',(.24,.035,.022),.58)
M['granite']=noise_material('Weathered garden stone',(.15,.16,.135),(.38,.37,.30),12,.85,.02)
collection('02 Architecture | floors')
for x1,y1,x2,y2 in SLABS:box('Enclosed floor',((x1+x2)/2,(y1+y2)/2,-.22),(x2-x1,y2-y1,.44),M['concrete'],.015)
collection('01 Architecture | walls and glazing')
def clad(name,a,b,height,openings):
    """Vertical boards omit apertures and follow the local roof profile."""
    length=math.dist(a,b);ux=(b[0]-a[0])/length;uy=(b[1]-a[1])/length
    n=math.ceil(length/.5);step=length/n
    for i in range(n):
        pos=(i+.5)*step;x=a[0]+ux*pos;y=a[1]+uy*pos;h=height(x) if callable(height) else height
        intervals=[(0,h)]
        for start,width,sill,head in openings:
            if start<=pos<=start+width:intervals=[(0,sill),(head,h)]
        for z1,z2 in intervals:
            if z2-z1<=0:continue
            box(name+' cedar board',(x,y,(z1+z2)/2),((step-.012) if ux else .20,(step-.012) if uy else .20,z2-z1),M['cedar'],.006)
    for start,width,sill,head in openings:
        p=(a[0]+ux*start,a[1]+uy*start);q=(a[0]+ux*(start+width),a[1]+uy*(start+width))
        glass_wall(name+' window',p,q,head,M['glass'],M['black'],sill)
clad('West wing front',(0,.16),(19,.16),roof_height,[(3.4,10.2,1,8.65)])
clad('East wing front',(43,.16),(62,.16),roof_height,[(5.4,10.2,1,8.65)])
clad('West facade',(.15,0),(.15,48),9.68,[(3,8,2,8.5),(25,8,2,8.5),(40,5,4,8.5)])
clad('East facade',(61.85,0),(61.85,48),9.68,[(3,15,.7,8.7),(25,5,5.5,8.5),(35,9,2.5,8.5)])
clad('Rear facade',(0,47.85),(62,47.85),roof_height,[(3,9,4,8.6),(17,36,.15,9.7),(56,3,5,8.5)])
for name,a,b,opens in WALLS:interior_wall(name,a,b,opens,M['plaster'],9.5)
glass_wall('West courtyard gallery',(19,8),(19,32),12.6,M['glass'],M['black'])
glass_wall('East courtyard gallery',(43,8),(43,32),12.6,M['glass'],M['black'])
glass_wall('Front courtyard threshold',(19,8),(43,8),8.75,M['glass'],M['black'])
glass_wall('Front glazed entry',(19,.2),(43,.2),8.75,M['glass'],M['black'])
glass_wall('Rear glazed gable',(19,32),(43,32),12.6,M['glass'],M['black'])
mesh('Gable glass triangle',[(19,32,12.6),(31,32,15.68),(43,32,12.6)],[(0,1,2)],M['glass'])
for x in [19,25,31,37,43]:beam('Gable timber mullion',(x,32,0),(x,32,roof_height(x)-.1),.21,.21,M['cedar'])
for a,b in [((19,32,12.8),(31,32,15.8)),((31,32,15.8),(43,32,12.8))]:beam('Expressed gable truss',a,b,.35,.45,M['cedar'])
for x in [28.2,33.8]:rod('Entry door pull',(x,-.01,3),(x,-.01,4.3),.035,M['black'])

collection('09 Roof | hide for cutaway')
def roof(name,x1,x2,y1,y2,z1,z2):
    pitched_plate(name,x1,x2,y1,y2,z1,z2,M['roof'],.27)
    for i in range(math.ceil(y2-y1)+1):
        y=y1+i
        beam(name+' raised standing seam',(x1,y,z1+.07),(x2,y,z2+.07),.04,.1,M['roof'])
    for y in [y1,y2]:beam(name+' dark fascia',(x1,y,z1-.02),(x2,y,z2-.02),.17,.4,M['roof'])
    for x,z in [(x1,z1),(x2,z2)]:beam(name+' edge trim',(x,y1,z),(x,y2,z),.15,.2,M['roof'])
roof('West shed roof',-1.25,19.3,-1.1,49.1,9.48,13.05)
roof('East shed roof',42.7,63.25,-1.1,49.1,13.05,9.48)
roof('Gable roof left',18.8,31,31,49.1,13,16.15)
roof('Gable roof right',31,43.2,31,49.1,16.15,13)
roof('Low entrance canopy',19,43,-3,8.15,9.15,9.15)
box('Chimney',(51,43,13.7),(2.5,3,4.2),M['granite'],.035)
box('Chimney cap',(51,43,15.87),(2.9,3.4,.22),M['black'],.02)
collection('08 Structure | cedar')
for x in [21,41]:box('Entry canopy cedar post',(x,-2.5,4.45),(.4,.4,8.9),M['cedar'],.018)
for y in [8,20,32]:
    for x1,x2 in [(0,19),(43,62)]:beam('Wing exposed rafter',(x1,y,roof_height(x1)-.37),(x2,y,roof_height(x2)-.37),.28,.46,M['cedar'])
for x in [19,43]:box('Courtyard cedar post',(x,8,6.3),(.32,.32,12.6),M['cedar'],.015)

# The coordinated kitchen is installed after the base architecture and lighting.

collection('04 Furnishings | schematic interior')
box('Dining table',(33.3,41,2.5),(6.8,3.4,.22),M['walnut'],.18)
for x in [30.8,35.8]:
    for y in [40,42]:rod('Dining table leg',(x,y,.1),(x,y,2.45),.1,M['walnut'])
for x in [30.8,33.3,35.8]:
    for y in [38.5,43.5]:
        box('Dining chair',(x,y,1.55),(1.6,1.5,.2),M['fabric'],.08)
        box('Dining chair back',(x,y+(-.6 if y<41 else .6),2.3),(1.6,.15,1.3),M['walnut'],.09)
box('Living rug',(23.5,40,.025),(12,12,.05),M['fabric'])
box('Living sofa base',(23,45,.9),(9.6,3.2,.75),M['fabric'],.22)
box('Living sofa back',(23,46.35,1.8),(9.6,.4,2),M['fabric'],.16)
for x in [19.8,23,26.2]:box('Living sofa cushion',(x,45,1.42),(3.08,2.65,.35),M['white'],.13)
cyl('Round coffee table',(24,40,1.2),1.5,.25,M['walnut'])
for name,x,y,width in [('Bedroom 03',7.5,6.2,5),('Bedroom 02',7.5,28.6,5),('Primary',54.6,9,6.5)]:
    box(name+' bed frame',(x,y,.6),(width+.25,7,.45),M['walnut'],.1)
    box(name+' mattress',(x,y,1.1),(width,6.6,.55),M['fabric'],.16)
    box(name+' headboard',(x,y+3.4,2),(width+.65,.18,3.1),M['cedar'],.04)
    for dx in [-width*.25,width*.25]:box(name+' pillow',(x+dx,y+2.1,1.5),(width*.42,1.6,.25),M['white'],.17)
    for dx in [-width/2-.8,width/2+.8]:box(name+' side table',(x+dx,y+2.3,.9),(1.3,1.3,1.6),M['walnut'],.04)
for name,x,y,w,d in [('Bath 02',0,14,9,8),('Bath 03',9,14,6,8),('Primary bath',47,24,8,8)]:
    box(name+' tiled floor',(x+w/2,y+d/2,.03),(w-.3,d-.3,.05),M['stone'])
    box(name+' shower',(x+2,y+2,.1),(3.5,3.5,.18),M['stone'],.02)
    box(name+' vanity',(x+w*.6,y+d-1,1.4),(3,1.8,2.7),M['walnut'],.03)
    sphere(name+' basin',(x+w*.6,y+d-1,2.83),(.8,.5,.1),M['white'])
    sphere(name+' WC',(x+1,y+d-2.4,1.05),(.58,.9,.55),M['white'])

collection('06 Landscape | layered courtyard garden')
box('Landscape ground',(31,15,-.8),(240,240,1),M['mulch'])
box('Courtyard paving',(31,20,-.16),(23.8,23.8,.25),M['stone'],.02)
# Broad axial path; offset planted islands reveal the garden behind the entry.
for y in [-26,-21,-16,-11,-6,11,16,21,26]:box('Large limestone stepping slab',(31,y,-.10),(7.5,4.2,.28),M['stone'],.035)
for x in [23.5,38.6]:box('Courtyard garden bed',(x,20,-.025),(6.4,20,.20),M['mulch'],.2)
tree('Courtyard Japanese maple',24.6,21,10,M['fir'],M['maple'],41)
tree('Courtyard small olive',38.5,25,8,M['fir'],M['silver'],48)
for i,(x,y,h) in enumerate([(-7,8,18),(-12,38,22),(3,60,24),(19,67,23),(40,68,25),(62,58,22),(72,34,21),(76,3,19),(-18,-5,20)]):
    tree('Garden canopy',x,y,h,M['fir'],M['green'] if i%2 else M['leaves'],100+i)
rng=random.Random(33)
for i in range(70):
    if i<30:
        x=rng.uniform(-7,69);y=rng.uniform(-14,-2)
        if 26<x<36:continue
    elif i<48:
        x=rng.choice([rng.uniform(-8,-2),rng.uniform(64,72)]);y=rng.uniform(0,46)
    else:
        x=rng.choice([rng.uniform(21,26),rng.uniform(36,41)]);y=rng.uniform(10,29)
    size=rng.uniform(1.1,2.25);shrub('Layered evergreen',x,y,size,M['silver'] if i%3==0 else M['green'],i+300)
    grasses('Ornamental grass',x+1.5,y-.8,rng.uniform(.8,1.8),M['grass'],i+400)
for i,(x,y,s) in enumerate([(5,-7,2.8),(17,-5,2.2),(43,-8,2.7),(58,-5,3),(25,18,1.9),(37,13,1.5),(-3,20,2.5),(65,30,2.5)]):rock('Garden boulder',x,y,s,M['granite'],i+6)
for row,y in enumerate([-17,-13,-9,-5]):
    for col in range(25):
        x=-6+col*3+rng.uniform(-.5,.5)
        if 26<x<36:continue
        yy=y+rng.uniform(-.6,.6);size=rng.uniform(1.55,2.6)
        shrub('Foreground garden drift',x,yy,size,M['silver'] if col%4==0 else M['green'],800+row*25+col)
        if col%2:grasses('Foreground grass drift',x+1,yy+.3,1.6,M['grass'],1000+row*25+col)
for i in range(20):
    shrub('Background evergreen layer',-6+i*4,54+rng.uniform(-2,2),rng.uniform(3.5,5),M['green'],1200+i)

collection('10 Lighting and cameras')
world=bpy.data.worlds.new('Warm late-afternoon sky');bpy.context.scene.world=world;world.use_nodes=True
n=world.node_tree.nodes;l=world.node_tree.links;sky=n.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_elevation=math.radians(19);sky.sun_rotation=math.radians(135);sky.sun_intensity=.65
l.new(sky.outputs[0],n.get('Background').inputs['Color']);n.get('Background').inputs['Strength'].default_value=.22
light=bpy.data.lights.new('Golden hour sun','SUN');light.energy=2.3;light.color=(1,.77,.51);light.angle=.05;ob=bpy.data.objects.new(light.name,light);g.ACTIVE.objects.link(ob);ob.rotation_euler=(math.radians(38),math.radians(-25),math.radians(-35))
area('Front soft fill',(31,-26,21),(31,20,5),1400,35,(.80,.88,1))
area('Rear living glow',(29,41,11),(31,25,3),360,12,(1,.67,.36))
area('Primary room glow',(55,10,8),(54,-1,4),160,6,(1,.70,.43))
area('Guest room glow',(7,6,8),(7,-1,4),120,5,(1,.70,.43))
from gallery import VIEWS as views
cams={name:camera(name,*args) for name,args in views.items()}
from kitchen import build_kitchen
kitchen_pins=build_kitchen()
s=bpy.context.scene;s.camera=cams['01 Reference exterior'];s.unit_settings.system='IMPERIAL';s.unit_settings.length_unit='FEET';s.unit_settings.scale_length=1
s.render.engine='CYCLES';s.cycles.samples=96;s.cycles.use_denoising=True;s.cycles.max_bounces=8
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
    for d in prefs.devices:d.use=d.type=='METAL'
    s.cycles.device='GPU'
except Exception as e:print('GPU_SETUP',e)
s.render.resolution_x=1800;s.render.resolution_y=1200;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=-.7
s['home_id']='timber-courtyard-02';s['gross_enclosed_area_sqft']=AREA;s['bedrooms']=3;s['bathrooms']=3;s['stage']='Exterior-led concept; coordinated kitchen revision; remaining legacy program unresolved'
for screen in bpy.data.screens:
    for ar in screen.areas:
        if ar.type=='VIEW_3D':ar.spaces.active.region_3d.view_perspective='CAMERA'
(HOME/'outputs/images').mkdir(parents=True,exist_ok=True)
s.render.filepath='//../outputs/images/01-exterior.png'
path=HOME/'model/timber-courtyard-02.blend';bpy.ops.wm.save_as_mainfile(filepath=str(path));bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(path))
deps=['materials/sage-fluted-tile','fixtures/opal-globe-pendant','furniture/walnut-counter-stool','materials/warm-vertical-cedar','materials/charcoal-standing-seam']
manifest={'schema_version':1,'id':'timber-courtyard-02','name':'Timber Courtyard 02','status':'exterior-led concept','units':'meters','display_units':'feet-inches','target_area_sqft':2400,'gross_enclosed_area_sqft':AREA,'area_basis':'62 x 48 ft outer footprint minus 24 x 24 ft courtyard; includes walls','bedrooms':3,'bathrooms':3,'reference_scope':'Exterior appearance only; interior may change','software':{'blender':bpy.app.version_string,'bonsai':'0.8.5'},'asset_dependencies':[{'id':i,'version':'v001','path':'../../library/'+i+'/v001/'} for i in deps],'deliverables':{'presentation_model':'model/timber-courtyard-02.blend','architectural_model':'model/timber-courtyard-02.ifc','primary_render':'outputs/images/01-exterior.png','floor_plan':'outputs/plans/floor-plan.svg','presentation_sheet':'outputs/plans/design-board.pdf'}}
from gallery import RENDERS
pins={i:'v001' for i in deps}|kitchen_pins
# Include the native scene's transitive material/hardware links, too.
for lib in bpy.data.libraries:
    folder=Path(bpy.path.abspath(lib.filepath)).resolve().parent
    asset_meta=json.loads((folder/'asset.json').read_text())
    pins[asset_meta['id']]=asset_meta['version']
import os
manifest['asset_dependencies']=[{'id':i,'version':v,'path':os.path.relpath(ROOT/'library'/i/v,HOME)+'/'} for i,v in sorted(pins.items())]
manifest['deliverables']['rendered_views']={slug:'outputs/images/'+slug+'.png' for slug in RENDERS}
manifest['deliverables']['level_plans']=[{'level':'Ground floor','svg':'outputs/plans/floor-plan.svg','png':'outputs/plans/floor-plan.png','roof_off_model':'outputs/images/04-model-plan.png'}]
(HOME/'project.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('TIMBER_MODEL_SAVED',len(s.objects),'objects',AREA,'sqft',flush=True)
if args.render:
    s.render.filepath=str(HOME/'outputs/images/01-exterior.png');bpy.ops.render.render(write_still=True)
