"""Reproducible Coastal House model. Run from the repository root in Blender."""
import bpy,sys,math,json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(Path(__file__).parent),str(ROOT/'tools')]
from design import *
from common import geometry as g
from common.geometry import box,cyl,rod,area,camera,collection,F
from common.architecture import glass_wall,interior_wall
from common.landscape import tree,shrub,grasses,rock
from common.library import linked_collection,instance
from materials import palette
from openings import sliding
from furniture import kitchen,rooms,soft,chair,bowl
from assets import counter_stool
HOME=ROOT/'homes'/SLUG
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name!='Collection':bpy.data.collections.remove(c)
M=palette(ROOT)
from common.shared_assets import load_catalog,place,dependencies
shared=load_catalog(ROOT,keys=['wardrobe','shrub','paver','grass','olive','oven','dishwasher','cooktop','hood','fridge','bathtub','toilet'])
collection('02 Architecture | enclosed floor')
box('Gross enclosed floor',(34,20,-.23),(68,40,.46),M['stone'],.01)
collection('01 Architecture | exterior and interior walls')
def wall(name,loc,size,mat=None):
    o=box(name,loc,size,mat or M['plaster'],.025);o['ifc_class']='IfcWall';return o
# Front elevation: broad bedroom glazing and a real 4-foot entry.
for a,b in [(0,3),(15,18),(26,28),(39,44),(54,68)]:wall('Front mineral render',((a+b)/2,.20,5.25),(b-a,.40,10.5))
for a,b in [(3,15),(28,39),(44,54)]:
    wall('Front window sill',((a+b)/2,.20,.60),(b-a,.40,1.2))
    wall('Front window head',((a+b)/2,.20,9.75),(b-a,.40,1.5))
    glass_wall('Bedroom picture window',(a,.20),(b,.20),9,M['glass'],M['bronze'],1.2,3)
wall('Front entrance head',(22,.20,9.5),(8,.40,2))
glass_wall('Entry daylight sidelight',(22,.20),(26,.20),8.5,M['glass'],M['bronze'],.10,2)
# Entry leaf open inward against the west reveal; actual passage remains.
door=box('Front pivot entry leaf',(18.13,2.08,4.2),(.16,3.70,8.4),M['oak'],.02);door['ifc_class']='IfcDoor'
rod('Front entry pull',(18.0,3.4,3.5),(18.0,3.4,5),.025,M['bronze'])
# Side walls: high privacy windows in primary bath, full-height glass at living and kitchen.
for x,label in [(0.20,'West'),(67.80,'East')]:
    wall(label+' front side',(x,11.5,5.25),(.40,23,10.5))
    wall(label+' back corner',(x,39.1,5.25),(.40,1.8,10.5))
    wall(label+' glazing head',(x,30.6,10.0),(.40,15.2,1.0))
    if label=='East':wall('Kitchen glazing sill wall',(x,30.6,2.8),(.4,15.2,5.6))
    if label=='East':
        for a,b in [(23,26),(30,35.5)]:wall('Kitchen solid appliance backing',(x,(a+b)/2,7.55),(.4,b-a,3.9))
        for a,b in [(26,30),(35.5,38.2)]:glass_wall('Kitchen high window',(x,a),(x,b),9.5,M['glass'],M['bronze'],5.6,1)
    else:
        wall('Primary bath privacy sill',(x,24.5,2.8),(.4,3,5.6))
        wall('West bath partition pier',(x,26,4.75),(.4,.4,9.5))
        glass_wall('Primary bath high privacy window',(x,23),(x,25.8),9.5,M['glass'],M['bronze'],5.6,1)
        glass_wall(label+' great room glazing',(x,26.2),(x,38.2),9.5,M['glass'],M['bronze'],.10,3)
# Rear wall solids and actual multi-track pocket cavities.
for a,b in [(0,4.5),(40.15,47.85),(63.3,68)]:wall('Rear solid pier',((a+b)/2,40,5.25),(b-a,1.25,10.5))
for a,b,z1,z2 in [(4.5,10,0,9.65),(60,63.3,3.13,8.65)]:
    for y in [39.44,40.56]:wall('Pocket removable cladding skin',((a+b)/2,y,(z1+z2)/2),(b-a,.12,z2-z1),M['oak'])
# Cabinet-height solid wall below serving aperture; header above each opening.
wall('Serving window low wall',(55.5,40,1.42),(15.0,.35,2.84))
wall('Great room structural header concept',(22.3,40,10.05),(35.4,1.25,.90))
wall('Serving window head',(55.6,40,9.61),(15.5,1.25,1.78))
sliding('Great room',DOOR,M);sliding('Serving window',WINDOW,M)
# Fine stone coursing on outer piers; geometric joints remain quiet in daylight.
for a,b in [(0,4.5),(40.3,47.7),(63.4,68)]:
    for row in range(21):
        z=.25+row*.5
        count=math.ceil((b-a)/2.25);w=(b-a)/count
        for i in range(count):box('Limestone facade ashlar', (a+(i+.5)*w,40.65,z),(w-.015,.08,.48),M['stone'],.009)
for name,a,b,opens in WALLS:
    interior_wall(name,a,b,opens,M['plaster'],10.4)
    # Timber leaves are parked along the inside wall rather than filling openings.
    ux=(b[0]-a[0])/math.dist(a,b);uy=(b[1]-a[1])/math.dist(a,b)
    for off,w in opens:
        if name=='Primary WC west':loc=(13.73,15.35+(w-.16)/2,3.75);sz=(.13,w-.16,7.5)
        elif name=='Primary bath front':loc=(a[0]+off-(w-.16)/2,a[1]-.27,3.75);sz=(w-.16,.13,7.5)
        elif ux:loc=(a[0]+off+.09,a[1]-w/2,3.75);sz=(.13,w-.16,7.5)
        else:loc=(a[0]+(-w/2 if name in ['Primary east','Bath closet partition'] else w/2),a[1]+off+.09,3.75);sz=(w-.16,.13,7.5)
        o=box(name+' open oak door leaf',loc,sz,M['oak'],.02);o['ifc_class']='IfcDoor'
# Guest laundry rear return leaves corridor mouth open at x56-60.
interior_wall('Laundry rear',(60,16),(68,16),[],M['plaster'],10.4)
# Subtle honed stone modules on interior slab, excluding overall area accounting collection.
collection('07 Finishes | floors and reveals')
for ix in range(17):
    for iy in range(10):
        o=box('Honed limestone floor module',(2+ix*4,2+iy*4,.018),(3.993,3.993,.028),M['stone'],.003);o['ifc_class']='IfcCovering'
from envelope import roof,arrival
roof(M)
# Ground-level terrace integrates slab, trench drain and restrained planting.
collection('06 Landscape | terrace and illustrative coast')
box('Terrace foundation',(34,49,-.30),(74,18,.50),M['stone'],.02)
for ix in range(18):
    for iy in range(4):place('Shared limestone terrace paver',shared['paver'],(-.18+ix*4.02,42.6+iy*4.02,.01))
box('Linear threshold drain',(25,40.84,-.008),(30,.18,.025),M['dark'],.012)
for i in range(151):box('Drain slot cross bridge',(10+i*.2,40.84,.008),(.035,.18,.025),M['steel'],.002)
# Exterior furnishings preserve 4+ ft circulation behind counter seating.
stool=counter_stool(ROOT,M)
pendant=linked_collection(ROOT,'fixtures','opal-globe-pendant')
for x in [50.2,53.7,57.2]:instance('Shared outdoor counter stool',stool,(x,45.0,0),0)
for x in [51.2,54.5,57.8]:instance('Shared island counter stool',stool,(x,26.4,0),math.pi)
# Reused opal light in the quieter entry.
instance('Shared entry opal pendant',pendant,(20,6,9.8))
# Linked conversation furniture provides a destination at the sheltered west end.
outdoor_assets = {slug: linked_collection(ROOT, 'furniture', slug) for slug in
                  ['coastal-outdoor-sofa', 'coastal-outdoor-lounge-chair', 'oak-rounded-coffee-table']}
for name, slug, loc, angle in OUTDOOR_LOUNGE:
    instance(name, outdoor_assets[slug], loc, math.radians(angle))
# Outdoor table farther from sliding doorway, preserving the through route.
terrace_table = linked_collection(ROOT, 'furniture', 'oak-dining-table-8ft')
terrace_chair = linked_collection(ROOT, 'furniture', 'oak-upholstered-dining-chair')
instance('Shared terrace dining table', terrace_table, (32,51.5,0))
for x in [29.7,32,34.3]:
    instance('Shared terrace dining chair shore', terrace_chair, (x,54.2,0))
    instance('Shared terrace dining chair house', terrace_chair, (x,48.8,0),math.pi)
bowl('Outdoor table bowl',32,51.5,2.50,.60,M['porcelain'])
box('Illustrative dune ground',(34,-32.5,-.77),(400,225,1.3),M['sand'])
from common.architecture import mesh
verts=[];faces=[]
for j in range(41):
    y=55+j*2
    for i in range(121):
        x=-140+i*3
        fade=max(0,min(1,(y-57)/10));z=-.6+fade*(.8*math.sin(x*.11+y*.17)+.32*math.sin(x*.31-y*.12))
        if y>82:z-=((y-82)/53)*2.5
        verts.append((x,y,z))
for j in range(40):
    for i in range(120):k=j*121+i;faces.append((k,k+1,k+122,k+121))
o=mesh('Soft original coastal dune topography',verts,faces,M['sand'])
for face in o.data.polygons:face.use_smooth=True
# Large shallow-sloped shore. The ocean is only an artistic backdrop, not a site claim.
sea=g.material('Soft coastal sea',(.11,.24,.27),.20)
p=sea.node_tree.nodes.get('Principled BSDF');p.inputs['IOR'].default_value=1.333;p.inputs['Transmission Weight'].default_value=.2
n=sea.node_tree.nodes;l=sea.node_tree.links;tc=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=2.2;noise.inputs['Detail'].default_value=2;l.new(tc.outputs['Object'],noise.inputs['Vector']);b=n.new('ShaderNodeBump');b.inputs['Distance'].default_value=.028;b.inputs['Strength'].default_value=.24;l.new(noise.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
box('Illustrative ocean',(34,1500,-.78),(9000,3200,.04),sea)
from gardens import build as gardens
from verandah import build as verandah
arrival(ROOT,M,shared)
verandah(M)
kitchen(M);rooms(M)
from suite import premium_suite
premium_suite(M,shared)
from bath_finishes import finishes as bath_finishes
bath_finishes(M)
# Guest wardrobes are genuine 24-inch-deep storage with paired door fronts.
collection('04 Furnishings | usable bedroom wardrobes')
for y in [3,5,7]:place('Bedroom 02 oak wardrobe',shared['wardrobe'],(39.8,y,0),rotation=-math.pi/2)
for x in [50.7,52.7,54.7]:place('Bedroom 03 oak wardrobe',shared['wardrobe'],(x,14.75,0))
from service import household
household(M,shared)
from appliances import complete_kitchen
complete_kitchen(M,shared)
collection('11 Details | original art and reveals')
box('Original relief art oak frame',(49,16.24,6.0),(7.8,.12,4.4),M['oak'],.02)
box('Original relief art linen field',(49,16.33,6.0),(7.6,.08,4.2),M['linen'],.012)
o=cyl('Original art circular relief',(47.9,16.39,6.3),1.15,.04,M['stone'],64);o.rotation_euler.x=math.pi/2
box('Original art coastal band',(49.7,16.42,5.4),(4.6,.04,.64),M['blue'],.20)
for x in [1.1,42.5,66.7]:
    box('Rear wall light backing',(x,40.78,6.6),(.18,.15,1.3),M['bronze'],.025)
    box('Rear wall light diffuser',(x,40.86,6.6),(.13,.06,1.10),M['glow'],.035)

from lighting_hardware import details as lighting_hardware,dependencies as detail_dependencies
lighting_hardware(ROOT)
from comfort import build as comfort, dependencies as comfort_dependencies
comfort(ROOT,M)
# Grain is aligned to each physical timber member, including new outdoor structure.
from common.timber_materials import grain_uv
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH' and not obj.library and M['accent_oak'] in list(obj.data.materials):
        grain_uv(obj)
collection('10 Lighting and cameras')
world=bpy.data.worlds.new('Bright coastal daylight');bpy.context.scene.world=world;world.use_nodes=True
n=world.node_tree.nodes;l=world.node_tree.links;sky=n.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_elevation=math.radians(39);sky.sun_rotation=math.radians(225);sky.sun_size=math.radians(2.0);sky.air_density=.8;sky.dust_density=.3;l.new(sky.outputs[0],n.get('Background').inputs['Color']);n.get('Background').inputs['Strength'].default_value=.32
# Broad soft fills act as bounced daylight, restrained enough to retain wood and linen texture.
area('Daylight bounce living',(15,36,9.7),(15,27,1),420,12,(.90,.95,1))
area('Daylight bounce dining',(35,36,9.7),(35,26,1),300,10,(.93,.96,1))
area('Daylight bounce kitchen',(55,36,9.7),(55,27,1),500,12,(.93,.96,1))
area('Primary bath diffuse bounce',(10,20,9.5),(10,20,1),180,7,(1,.95,.88))
area('Kitchen warm under hood',(65,32.5,5.9),(66,32.5,3),25,2,(1,.88,.7))
views={
 '01 Terrace open':((87,110,15),(34,28,4.5),38),
 '02 Great room':((25,22.2,5.4),(41,42,4.8),24),
 '03 Serving counter':((43.5,50.0,6.3),(55.1,38.9,4.55),36),
 '04 Serving closed':((43.5,50.0,6.3),(55.1,38.9,4.55),36),
 '05 Terrace closed':((87,110,15),(34,28,4.5),38),
 '06 Front arrival':((102,-110,24),(46,-2,4),35),
 '07 Roof and parking':((132,-105,90),(48,-2,0),38),
 '08 West garden':((-48,72,16),(26,19,5),40),
 '09 Entry hall':((20,2.2,5.5),(26,23,4.8),22),
 '10 Primary bath':((6.6,18.7,5.5),(10.5,23.7,3.8),17),
 '11 Living retreat':((25,37,5.4),(11,29.5,3.8),24),
}
for name,args in views.items():camera(name,*args)
# Install dense linked planting after furniture to avoid repeated scene evaluation during authoring.
garden_counts=gardens(M,shared)
for o in bpy.context.scene.objects:
    if o.type=='CURVE' and not o.library:o.data.use_fill_caps=True
s=bpy.context.scene;s.camera=bpy.data.objects['01 Terrace open'];s.frame_start=1;s.frame_end=120;s.frame_set(120)
s.unit_settings.system='IMPERIAL';s.unit_settings.length_unit='FEET';s.unit_settings.scale_length=1
s.render.engine='CYCLES';s.cycles.samples=512;s.cycles.use_denoising=True;s.cycles.adaptive_threshold=.008;s.cycles.max_bounces=12;s.cycles.transmission_bounces=12;s.cycles.glossy_bounces=6
s.render.resolution_x=3200;s.render.resolution_y=2000;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_depth='8'
s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=-.65
s['home_id']=SLUG;s['gross_enclosed_area_sqft']=AREA;s['bedrooms']=3;s['bathrooms']=2;s['stage']='Architectural concept; site and opening engineering unverified';s['opening_states']='Frame 1 closed; frame 120 fully pocketed'
s.render.filepath='//../outputs/images/01-terrace-open.png'
for screen in bpy.data.screens:
    for ar in screen.areas:
        if ar.type=='VIEW_3D':ar.spaces.active.region_3d.view_perspective='CAMERA'
bpy.ops.wm.save_as_mainfile(filepath=str(HOME/'model/coastal-house.blend'));bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(HOME/'model/coastal-house.blend'))
deps=['materials/woven-oatmeal','materials/olive-linen','materials/warm-limestone-plaster','materials/smoked-oak','furniture/coastal-outdoor-sofa','furniture/coastal-outdoor-lounge-chair','materials/coastal-white-oak','materials/coastal-honed-limestone','furniture/coastal-oak-counter-stool','fixtures/opal-globe-pendant']
meta={'schema_version':1,'id':SLUG,'name':'Coastal House','status':'Detailed visualization and dimensioned architectural concept','units':'meters','display_units':'feet-inches','target_area_sqft':AREA,'gross_enclosed_area_sqft':AREA,'area_basis':'68 x 40 ft exterior floor plate, including walls; excludes carport, terrace, eaves, landscaping and illustrative shore','bedrooms':3,'bathrooms':2,'assumptions':'Single story, 3 bedrooms and 2 baths; entry widened to 8 ft planning width, guest wardrobes added; no actual parcel or orientation supplied.','software':{'blender':bpy.app.version_string,'bonsai':'0.8.5'},'asset_dependencies':[{'id':i,'version':'v001','path':'../../library/'+i+'/v001/'} for i in deps]+dependencies(ROOT,keys=['wardrobe','shrub','paver','grass','olive','oven','dishwasher','cooktop','hood','fridge','bathtub','toilet'])+detail_dependencies()+comfort_dependencies(),'site_concept':{'road':'front/south illustration only','parking':'Detached 26 x 24 ft two-car carport, east side; 26 ft driveway','entry':'6 ft front path plus 4 ft crosswalk behind parked cars','roof':'House 2:12 low standing-seam gable; carport 1:12 mono-pitch; modeled gutters/downpipes, no product/site drainage approval'},'openings':{'dimension_units':'feet','great_room':DOOR,'serving_window':WINDOW,'animation':'Frame 1 closed; frame 120 open. Conceptual six-track door and four-track window; no commercial product specification.'},'deliverables':{'presentation_model':'model/coastal-house.blend','architectural_model':'model/coastal-house.ifc','primary_render':'outputs/images/01-terrace-open.png','floor_plan':'outputs/plans/floor-plan.svg','presentation_sheet':'outputs/plans/design-board.pdf'}}
meta['modeled_planting_counts']=garden_counts
meta['design_direction']='Warm coastal verandah: shaded dining, outdoor conversation area, planted entry court, smoked-oak island and tactile textiles.'
meta['site_concept']['terrace']='32 x 15.15 ft wall-attached slatted timber pergola spanning the full 30 ft sliding wall, west conversation seating and low side screen; shade only, structure unengineered.'
# A material may be shared by several furniture families; list each direct asset once.
meta['asset_dependencies']=list({(d['id'],d['version']):d for d in meta['asset_dependencies']}.values())
(HOME/'project.json').write_text(json.dumps(meta,indent=2)+'\n')
print('COASTAL_MODEL_SAVED',len(s.objects),AREA,flush=True)
