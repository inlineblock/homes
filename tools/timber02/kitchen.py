"""Coordinated Timber kitchen; feet at placement boundary, native assets in meters.

Applied to the existing model by revise_kitchen.py and to a full build by build.py.
Exact-fit counters/enclosure/ceiling are bespoke; repeated equipment is linked.
"""
import math
from pathlib import Path
import bpy
from mathutils import Vector, Matrix
from common import geometry as g
from common.geometry import F, box, rod, area, camera, collection
from common.architecture import glass_wall, interior_wall, pitched_plate, mesh
from common.library import linked_collection, instance
from common.timber_materials import grain_uv
from design import roof_height
ROOT=Path(__file__).resolve().parents[2]
PINS={}
from kitchen_layout import ISLAND, REAR_TOP, EAST_TOP, PANTRY_OPENING, COUNTER_Z

def asset(category,slug,version='v001'):
    PINS[f'{category}/{slug}']=version
    return linked_collection(ROOT,category,slug,version)

def mat(slug,version='v001'):
    PINS['materials/'+slug]=version
    path=ROOT/f'library/materials/{slug}/{version}/{slug}.blend'
    with bpy.data.libraries.load(str(path),link=True) as (a,b):b.materials=[a.materials[0]]
    return b.materials[0]

def remove_prefixes(prefixes):
    for o in list(bpy.data.objects):
        if o.library is None and o.name.startswith(tuple(prefixes)):
            bpy.data.objects.remove(o,do_unlink=True)

def cut(obj,name,loc,size):
    tool=box(name,loc,size)
    mod=obj.modifiers.new(name,'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=tool
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(tool,do_unlink=True)

def fixture_recess(hosts,fixture):
    """Exact local mounting cutout, with 1mm tolerance at each depth end."""
    bpy.context.view_layer.update()
    tool=box('Temporary power fixture recess',(0,0,0),(.054/F,.054/F,.098/F))
    tool.matrix_world=fixture.matrix_world @ Matrix.Translation((0,.026,0))
    for host in hosts:
        mod=host.modifiers.new('Power mounting cavity','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=tool
        bpy.context.view_layer.objects.active=host
        bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(tool,do_unlink=True)

def countertop(name,bounds,stone,holes=()):
    x1,y1,x2,y2=bounds;thick=1.5/12
    o=box(name,((x1+x2)/2,(y1+y2)/2,3-thick/2),(x2-x1,y2-y1,thick),stone)
    for x,y,w,d in holes:cut(o,name+' opening',(x,y,3),(w,d,.5))
    bevel=o.modifiers.new('Small eased stone arris','BEVEL');bevel.width=.003;bevel.segments=3
    return o

def build_kitchen():
    PINS.clear()
    old=bpy.data.collections.get('03 Kitchen | shared assets')
    if old:
        for o in list(old.objects):bpy.data.objects.remove(o,do_unlink=True)
        bpy.data.collections.remove(old)
    for c in list(bpy.data.collections):
        if c.library is None and c.name.startswith(('03 Kitchen |','03 Pantry |','03 Ceiling |')):
            for o in list(c.objects):bpy.data.objects.remove(o,do_unlink=True)
            bpy.data.collections.remove(c)
    collection('03 Kitchen | coordinated shared assets')
    oak=mat('smoked-oak');stone=mat('coastal-honed-limestone')
    cedar=mat('warm-vertical-cedar');plaster=bpy.data.materials['Warm chalk plaster']
    black=bpy.data.materials['Blackened bronze'];glass=bpy.data.materials['Clear architectural glass']
    drawer=asset('cabinetry','smoked-oak-drawer-base-2ft')
    sinkbase=asset('cabinetry','smoked-oak-sink-base-36in')
    ovenbase=asset('cabinetry','smoked-oak-oven-base-36in')
    waste=asset('cabinetry','smoked-oak-waste-pullout-18in')
    fridge=asset('appliances','smoked-oak-panel-ready-fridge-48in')
    dishwasher=asset('appliances','smoked-oak-panel-ready-dishwasher-24in')
    hob=asset('appliances','induction-cooktop-36in')
    oven=asset('appliances','built-in-oven-30in')
    hood=asset('appliances','wall-hood-36in')
    sink=asset('fixtures','kitchen-sink-mixer-650','v002')
    tile=asset('materials','sage-fluted-tile')
    stool=asset('furniture','walnut-counter-stool')
    # Rear cleanup run. All standard cabinets stand on floor; no solid sink proxy.
    for x in [43.25,45.25,47.25,49.25]:instance('Kitchen rear drawer storage',drawer,(x,46.55,0))
    instance('Kitchen sink base',sinkbase,(40.75,46.55,0))
    instance('Kitchen integrated dishwasher',dishwasher,(38.25,46.55,0))
    sink_y=46.55-.030/F
    countertop('Kitchen garden cleanup worktop',REAR_TOP,stone,[(40.75,sink_y,.664/F,.464/F)])
    instance('Kitchen real sink and mixer',sink,(40.75,sink_y,3))
    box('Kitchen low stone splash',(44.2,47.58,3.18),(14.1,.12,.36),stone,.015)
    # East service wall: wide fridge, two-foot landing/drawers, induction/oven, north landing.
    instance('Kitchen 48 inch refrigerator freezer',fridge,(52.55,39.22,0),-math.pi/2)
    instance('Kitchen cooking landing drawers',drawer,(52.65,42.30,0),-math.pi/2)
    instance('Kitchen open oven housing',ovenbase,(52.65,44.80,0),-math.pi/2)
    instance('Kitchen built in oven',oven,(52.65,44.80,.140/F),-math.pi/2)
    countertop('Kitchen east cooking worktop',EAST_TOP,stone,[(52.65,44.80,1.62,2.88)])
    instance('Kitchen induction stove',hob,(52.65,44.80,3),-math.pi/2)
    instance('Kitchen extraction hood',hood,(52.79,44.80,5.55),-math.pi/2)
    # Continuous original concept duct above hood; termination/product sizing unresolved.
    hood_steel=next(slot.material for ob in hood.all_objects for slot in ob.material_slots if slot.material and 'brushed stainless' in slot.material.name.lower())
    riser_xy=[(52.66,44.24),(53.70,44.24),(53.70,45.36),(52.66,45.36)]
    mesh('Kitchen concealed exhaust riser',[(x,y,8.01) for x,y in riser_xy]+[(x,y,roof_height(x)-.43) for x,y in riser_xy],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],hood_steel)
    area('Kitchen hood task light',(52.20,44.8,5.49),(52.65,44.8,3),28,1.9,(1,.94,.84),shape='RECTANGLE',size_y=1.15)
    for row in range(4):
        for col in range(24):instance('Kitchen sage cooking wall tile',tile,(53.765,41.45+col*.25,3.50+row),-math.pi/2)
    # Exact-fit corner/end fillers keep carcasses separate and close inaccessible voids.
    for name,loc,size in [
        ('Rear end panel',(37.16,46.55,1.43),(.06,2,2.86)),
        ('Corner blank front',(50.8,45.57,1.43),(1.1,.06,2.86)),
        ('East north landing front',(51.63,46.91,1.43),(.06,1.2,2.86)),
        ('Fridge side filler',(52.55,41.27,3.5),(2.5,.08,7)),
    ]:grain_uv(box('Kitchen '+name,loc,size,oak,.008))
    # Island: three drawer modules and a real waste/recycling pullout face the work aisle.
    for x in [40.50,42.50,44.50]:instance('Kitchen island deep drawers',drawer,(x,40.275,0),math.pi)
    instance('Kitchen island waste recycling',waste,(46.25,40.275,0),math.pi)
    countertop('Kitchen island preparation stone',ISLAND,stone)
    grain_uv(box('Kitchen island finished back',(43.25,39.255,1.46),(7.5,.055,2.75),oak,.008))
    for x in [39.46,47.04]:grain_uv(box('Kitchen island supporting end cheek',(x,39.45,1.43),(.063,3.75,2.86),oak,.012))
    for x in [40.0,42.1,44.2,46.3]:box('Kitchen island concealed steel support',(x,38.7,2.81),(.08,2.55,.07),black,.01)
    for x in [40.75,43.25,45.75]:instance('Kitchen island seat',stool,(x,36.95,0),math.pi)
    # Replan pantry access and replace the below-counter glass with a proper solid spandrel.
    architecture=bpy.data.collections['01 Architecture | walls and glazing'];g.ACTIVE=architecture
    remove_prefixes(['pantry-west'])
    interior_wall('pantry-west',(54,32),(54,47.6),[(1.5,3)],plaster,roof_height(54)-.45)
    # Existing rear ribbon glazing spans x17–53; split at the kitchen boundary.
    for o in list(architecture.objects):
        if o.name.startswith('Rear facade window') and o.location.x/F > 15 and o.location.x/F < 54:
            bpy.data.objects.remove(o,do_unlink=True)
    glass_wall('Rear living garden glazing',(17,47.85),(37.0,47.85),9.7,glass,black,.15)
    glass_wall('Rear kitchen garden window',(37.0,47.85),(53,47.85),9.7,glass,black,3.40)
    box('Kitchen insulated spandrel concept',(45.0,47.83,1.70),(16.0,.28,3.40),plaster)
    for i in range(33):box('Kitchen rear cedar spandrel board',(37.25+i*.4845,48.005,1.70),(.472,.09,3.40),cedar,.005)
    # Shelving needs an opaque backing and real fixing support, not a window behind it.
    for o in list(architecture.objects):
        if o.name.startswith('East facade window') and 34.9<=o.location.y/F<=44.1:
            bpy.data.objects.remove(o,do_unlink=True)
    glass_wall('Pantry east clerestory',(61.85,35),(61.85,44),8.5,glass,black,7.25)
    box('Pantry insulated shelf backing',(61.83,38.3,4.875),(.28,12,4.75),plaster)
    for i in range(18):box('Pantry cedar infill board',(62.01,35.25+i*.5,4.875),(.09,.488,4.75),cedar,.005)
    # Door is shown open into pantry, out of the working kitchen.
    grain_uv(box('Kitchen pantry door open',(55.50,33.55,3.65),(2.94,.14,7.30),oak,.01))
    rod('Kitchen pantry door handle',(56.63,33.43,3.2),(56.63,33.43,3.8),.018,black)
    collection('03 Pantry | fitted food and appliance storage')
    shelf=asset('cabinetry','smoked-oak-pantry-shelf-2ft')
    grain_uv(box('Pantry anti tip fixing ledger',(61.63,38.3,6.85),(.21,12,.18),oak,.004))
    for y in [33.3,35.3,37.3,39.3,41.3,43.3]:instance('Pantry food shelf',shelf,(61.03,y,0),-math.pi/2)
    for x in [56.0,58.0,60.0]:instance('Pantry appliance and bulk drawer storage',drawer,(x,46.55,0))
    countertop('Pantry appliance worktop',(54.90,45.425,61.12,47.65),stone)
    # Supported two-foot shelves at east, clear full-width entry/south turning zone.
    collection('03 Ceiling | kitchen and pantry lining')
    for x1,x2 in [(15.18,19),(19,31),(31,43),(43,54),(54,61.6)]:
        y1=32.18; y2=47.65
        for i in range(31):
            ya=y1+i*.5;yb=min(ya+.489,y2)
            if yb<=ya:continue
            o=pitched_plate('Kitchen fitted cedar ceiling board',x1,x2,ya,yb,roof_height(x1)-.34,roof_height(x2)-.34,cedar,.11)
    # Glare-controlled lighting: downlights housed in real holes, plus island/dining features.
    down=asset('fixtures','lighting-recessed-downlight-3in')
    ceiling=bpy.data.collections['03 Ceiling | kitchen and pantry lining']
    for x,y in [(40,44),(48.8,44),(48.8,35.2),(42,35.2),(57.6,36),(57.6,42),(57.6,46)]:
        z=roof_height(x)-.45
        for o in list(ceiling.objects):
            if o.type!='MESH':continue
            w=[o.matrix_world@Vector(c) for c in o.bound_box]
            if min(v.x for v in w)/F<=x<=max(v.x for v in w)/F and min(v.y for v in w)/F-.15<=y<=max(v.y for v in w)/F+.15:
                cut(o,'Downlight service opening',(x,y,z+.08),(.31,.31,.50))
        instance('Kitchen recessed downlight',down,(x,y,z))
        area('Kitchen downward task light',(x,y,z-.07),(x,y,0),34,1.4,(1,.88,.73))
    globe=asset('fixtures','opal-globe-pendant')
    instance('Shared globe over dining',globe,(33.4,41,13.6))
    linear=asset('fixtures','lighting-linear-pendant-4ft')
    instance('Kitchen linear island light',linear,(43.25,39.20,10.5))
    # Actual ceiling-to-canopy support, not an unsupported floating fixture.
    for x in [42.25,44.25]:rod('Kitchen pendant upper suspension',(x,39.20,roof_height(x)-.45),(x,39.20,10.5),.012,black)
    area('Kitchen island light emission',(43.25,39.20,7.82),(43.25,39.20,3),48,3.8,(1,.88,.73),shape='RECTANGLE',size_y=.20)
    # Deliberate service points: concept geometry only, no electrical specification.
    outlet=asset('fixtures','duplex-power-outlet-bronze')
    for x in [43.5,49.2]:
        o=instance('Kitchen garden counter power',outlet,(x,47.52,3.18))
        o.rotation_euler.y=math.pi/2
        fixture_recess([bpy.data.objects['Kitchen low stone splash'],bpy.data.objects['Kitchen insulated spandrel concept']],o)
    o=instance('Pantry appliance counter power',outlet,(55.8,47.75,3.65))
    for wall in list(architecture.objects):
        if wall.type=='MESH' and wall.name.startswith('Rear facade cedar board') and abs(wall.location.x/F-55.8)<.4:
            fixture_recess([wall],o)
    o=instance('Kitchen island end power',outlet,(39.428,38.80,2.625),-math.pi/2)
    fixture_recess([bpy.data.objects['Kitchen island supporting end cheek']],o)
    grain_uv(box('Kitchen island power service cover',(39.63,38.80,2.625),(.045,.30,.41),oak,.006))
    for y in [38.65,38.95]:grain_uv(box('Kitchen island service cover edge',(39.56,y,2.625),(.17,.04,.41),oak,.004))
    # Adjacent furniture must remain plausible in the same interior view.
    g.ACTIVE=bpy.data.collections['04 Furnishings | schematic interior']
    remove_prefixes(['Dining chair','Round coffee table','Living sofa','Dining table'])
    chair=asset('furniture','oak-upholstered-dining-chair')
    coffee=asset('furniture','oak-rounded-coffee-table')
    sofa=asset('furniture','linen-three-seat-sofa')
    instance('Shared supported linen sofa',sofa,(22.0,45.0,0),math.pi)
    table=asset('furniture','oak-dining-table-8ft')
    instance('Shared grounded dining table',table,(32.5,41,0))
    for x in [30.0,32.5,35.0]:
        for y in [38.5,43.5]:instance('Shared supported dining chair',chair,(x,y,0),math.pi if y<41 else 0)
    instance('Shared supported coffee table',coffee,(22.8,40,0))
    g.ACTIVE=bpy.data.collections['10 Lighting and cameras']
    from gallery import VIEWS
    for name in ['06 Kitchen','08 Cooking wall','09 Pantry','10 Living room']:
        loc,target,lens=VIEWS[name]
        o=bpy.data.objects.get(name)
        if o:bpy.data.objects.remove(o,do_unlink=True)
        camera(name,loc,target,lens)
    return dict(PINS)
