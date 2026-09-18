"""Reopen real geometry and check concept floor/asset/stair/route invariants."""
import bpy,sys,json,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(Path(__file__).parent),str(ROOT/'tools')]
from design import *
F=.3048;s=bpy.context.scene;HOME=ROOT/'homes'/SLUG

def bounds(o,matrix=None):
    pts=[(matrix or o.matrix_world)@Vector(v) for v in o.bound_box]
    return [min(p[i]/F for p in pts) for i in range(3)]+[max(p[i]/F for p in pts) for i in range(3)]
# Reserve a full 90-degree swing for the conceptual refrigerator's left leaf.
# An actual selected product may require a larger articulation/service envelope.
fridge=next(o for o in s.objects if o.name.startswith('Shared 48 inch panel ready refrigerator'))
island=bpy.data.objects['Island quartzite worktop'];island_box=bounds(island)
assert fridge.location.x/F-2-island_box[3]>.5,'Refrigerator door swing intersects island end'
libs=[]
for lib in bpy.data.libraries:
    assert lib.filepath.startswith('//'),lib.filepath
    p=Path(bpy.path.abspath(lib.filepath)).resolve();assert p.is_file() and p.is_relative_to(ROOT)
    libs.append(lib.filepath)
floors=[o for o in s.objects if o.type=='MESH' and any(c.name.startswith('02 Architecture') for c in o.users_collection)]
area=sum(o.dimensions.x*o.dimensions.y/F**2 for o in floors)
assert abs(area-GROSS)<.02,area
assert len([o for o in s.objects if ' bed frame' in o.name])==3
storage={}
for prefix in ['Primary walk-in','Bedroom02','Bedroom03']:
    bays=[o for o in s.objects if o.instance_type=='COLLECTION' and o.name.startswith(prefix)]
    assert len(bays)>1,(prefix,len(bays));storage[prefix]=len(bays)*2
# Actual upper floor aperture and stair tread top heights, not labels.
for x in [26,30]:
    for y in [14,18,22]:
        assert not any(bb[0]<x<bb[3] and bb[1]<y<bb[4] and bb[5]>-.1 for bb in map(bounds,floors)),(x,y,'stair opening covered')
lower=sorted(round(bounds(o)[5],3) for o in s.objects if o.name.startswith('Lower stair tread'))
upper=sorted(round(bounds(o)[5],3) for o in s.objects if o.name.startswith('Upper stair tread'))
assert len(lower)==len(upper)==9,(lower,upper)
heights=[LOWER]+lower+[-5.5]+upper+[0]
assert all(abs(b-a-RISE)<.003 for a,b in zip(heights,heights[1:])),heights
# Swept walking routes at each floor. Include linked storage geometry at real transforms.
obstacles=[]
for o in s.objects:
    if o.type not in {'MESH','CURVE'}:continue
    if not any(c.name.startswith(('01 Architecture','03 Kitchen','04 Furnishings','05 Fixtures')) for c in o.users_collection):continue
    obstacles.append((o.name,bounds(o)))
for inst in bpy.context.evaluated_depsgraph_get().object_instances:
    if inst.is_instance and inst.parent and inst.parent.instance_type=='COLLECTION' and any(c.name.startswith(('03 Kitchen','04 Furnishings','05 Fixtures')) for c in inst.parent.users_collection):
        obstacles.append((inst.parent.name+' / '+inst.object.name,bounds(inst.object,inst.matrix_world)))
routes={
 'front entry to dining':(0,[(35.3,-2),(35.3,2),(37.1,3),(37.1,20),(38.8,25),(39.4,30),(39.4,37)]),
 'garage to mudroom':(0,[(20,7.8),(29.7,7.8),(29.7,8.7),(34.8,8.7)]),
 'primary bedroom':(0,[(38,24),(48.5,24)]),
 'primary dressing':(0,[(48.5,24),(47.7,21.5),(47.7,19.6),(44.1,19.6)]),
 'primary bathroom':(0,[(44.1,19.6),(43.7,13),(43.7,9),(48.7,8),(55,7.8)]),
 'primary shower':(0,[(48.7,8),(48.7,3.3)]),
 'primary toilet room':(0,[(43.7,9),(43.7,7.5),(42.55,7.5),(42.55,4.2)]),
 'living to deck':(0,[(19,34),(19,41.7),(19,49)]),
 'lower stair arrival to lounge':(-11,[(26,10),(26,9),(35.7,9),(35.7,16),(39.4,16),(39.4,36),(37,36),(37,42)]),
 'lower bedroom02':(-11,[(39.4,25.8),(22.8,25.8),(22.8,29.05),(19.4,29.05),(15.5,29.05)]),
 'lower bedroom02 wardrobe':(-11,[(15.5,29.05),(15.5,27.8),(5,27.8)]),
 'lower bedroom03':(-11,[(39.4,16),(55.8,16),(55.8,25),(56,27.8),(57.6,27.8)]),
 'kitchen working aisle':(0,[(40.5,35.2),(55.5,35.2),(55.5,31.5)]),
}
failures=[]
for name,(z,points) in routes.items():
    obs=[(name,bb) for name,bb in obstacles if bb[2]<z+6 and bb[5]>z+.3]
    for a,b in zip(points,points[1:]):
        N=max(1,math.ceil(math.dist(a,b)/.16))
        for i in range(N+1):
            x=a[0]+(b[0]-a[0])*i/N;y=a[1]+(b[1]-a[1])*i/N
            for ob,bb in obs:
                dx=max(bb[0]-x,0,x-bb[3]);dy=max(bb[1]-y,0,y-bb[4])
                if math.hypot(dx,dy)<1.25-.02:
                    failures.append((name,ob,round(x,2),round(y,2)));break
            if failures and failures[-1][0]==name:break
        if failures and failures[-1][0]==name:break
assert not failures,failures
plant_count=0
for o in s.objects:
    if o.instance_type=='COLLECTION' and o.instance_collection and o.instance_collection.library and any(v in o.name for v in ['forest grass','forest shrub','conifer','shared fir']):
        x,y,z=[v/F for v in o.location];assert abs(z-grade(x,y))<.02,(o.name,z,grade(x,y));plant_count+=1
assert plant_count>50
report={'native_model_reopened':True,'gross_enclosed_area_sqft':round(area,2),'conditioned_gross_area_sqft':CONDITIONED,'modeled_beds':3,'clothes_storage_widths_ft':storage,'relative_libraries':libs,'stair':{'risers':20,'rise_inches':RISE*12,'tread_inches':TREAD*12,'actual_tread_elevations_checked':True,'main_aperture_clear':True},'circulation':{'swept_diameter_inches':30,'routes':list(routes),'scope':'Concept paths against modeled obstacles; no accessibility/code approval.'},'plants_placed_on_actual_grade':plant_count,'limits':'Illustrative slope and engineering only. No survey, structural, local code, egress opening product or drainage certification.'}
(HOME/'model/model-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('MOUNTAIN_VERIFIED',json.dumps(report),flush=True)
