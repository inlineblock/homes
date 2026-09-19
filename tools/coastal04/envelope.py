"""Layered coastal pavilion envelope and a usable two-car arrival."""
import math,importlib.util
from common import geometry as g
from common.geometry import box,rod,collection,material,F
from common.architecture import mesh,beam
from common.landscape import grasses,shrub

CARPORT=(73,99,-27,-3)

def entry_canopy(M):
    """Warm, legible arrival canopy; concept fall/drain, unengineered fixing."""
    from coastal04.verandah import ENTRY_CANOPY_BOUNDS, ENTRY_CANOPY_POSTS
    from common.timber_materials import grain_uv
    x1,x2,y1,y2=ENTRY_CANOPY_BOUNDS
    wood=M['accent_oak']
    # Two outer columns and an upper wall ledger retain the full walk/crosswalk.
    for x,y in ENTRY_CANOPY_POSTS:
        o=box('Entry canopy timber column',(x,y,4.60),(.50,.50,9.2),wood,.025)
        o['ifc_class']='IfcColumn';grain_uv(o)
        o=box('Entry canopy bronze shoe',(x,y,.20),(.60,.60,.40),M['bronze'],.015);o['ifc_class']='IfcPlate'
    for y in [y1+.55,-.35]:
        o=box('Entry canopy supporting timber beam',((x1+x2)/2,y,9.30),(x2-x1,.50,.50),wood,.018)
        o['ifc_class']='IfcBeam';grain_uv(o)
    for i in range(30):
        o=box('Entry canopy warm timber soffit',(x1+.20+i*.40,(y1+y2)/2,9.54),(.36,y2-y1,.10),wood,.008)
        o['ifc_class']='IfcCovering';grain_uv(o)
    # Thin metal cap falls 1/4 inch per foot to the front gutter.
    zfront,zback=9.67,9.67+(y2-y1)/48
    v=[(x1,y1,zfront),(x2,y1,zfront),(x2,y2,zback),(x1,y2,zback)]
    o=mesh('Entry canopy sloping bronze metal cap',v+[(x,y,z-.075) for x,y,z in v],[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],M['bronze'])
    o['ifc_class']='IfcRoof';o['design_status']='Concept slope and drainage only; assembly and fixings unresolved'
    for x in [x1,x2]:
        beam('Entry canopy thin bronze edge',(x,y1,zfront-.05),(x,y2,zback-.05),.07,.14,M['bronze'])
    for yy in [y1-.04,y1-.30]:
        box('Entry canopy gutter upstand',((x1+x2)/2,yy,zfront-.09),(x2-x1,.025,.18),M['bronze'],.004)
    box('Entry canopy gutter base',((x1+x2)/2,y1-.17,zfront-.17),(x2-x1,.28,.025),M['bronze'],.004)
    rod('Entry canopy downpipe',(27.55,y1-.17,zfront-.17),(27.55,y1-.17,.08),.055,M['bronze'])
    box('Entry canopy drain inspection grate',(27.55,y1-.17,.025),(.50,.50,.04),M['dark'],.01)

def roof(M):
    from pavilion_roof import build as build_pavilion
    build_pavilion(M)
    entry_canopy(M)


def arrival(ROOT,M,shared):
    from common.shared_assets import place
    collection('12 Arrival | road driveway paths and planting')
    paving=material('Warm aggregate concrete driveway',(.40,.395,.36),.82)
    asphalt=material('Quiet coastal road asphalt',(.12,.14,.14),.88)
    box('Illustrative front road',(38,-56,-.18),(260,22,.28),asphalt,.01)
    box('Two-car drive apron',(86,-36,-.10),(26,18,.18),paving,.025)
    box('Carport concrete slab',(86,-15,-.10),(26,24,.18),paving,.025)
    # Four-foot crosswalk remains behind parked vehicles, then across the house front.
    box('Protected crosswalk behind parking',(51.5,-2.25,-.025),(69,4.0,.13),M['stone'],.018)
    box('Six-foot front pedestrian path',(20,-24.625,-.025),(6,40.75,.13),M['stone'],.018)
    for y in [-42,-36,-30,-24,-18,-12,-6]:box('Pedestrian path expansion joint',(20,y,.045),(6,.025,.008),M['dark'])
    for x in [73,86,99]:box('Drive expansion joint',(x,-25,.005),(.025,40,.008),M['dark'])
    for y in [-42,-33,-24,-15,-6]:box('Drive transverse joint',(86,y,.006),(26,.025,.008),M['dark'])
    box('Drive threshold drain',(86,-43.5,.002),(25,.23,.025),M['dark'],.008)
    for i in range(121):box('Drive drain grating',(73.7+i*.205,-43.5,.015),(.028,.23,.025),M['steel'])
    # The parking bays are 12 ft wide. Slender posts stay outside car-door zones.
    collection('13 Carport | two sheltered passenger cars')
    roofmat=M['roof_metal']
    for x in [73.3,98.7]:
        for y in [-26.7,-5.5]:
            top=9.4+(y+28)/12-.45
            o=box('Carport oak column',(x,y,top/2),(.55,.55,top),M['accent_oak'],.025);o['ifc_class']='IfcColumn'
            box('Carport column steel shoe',(x,y,.22),(.62,.62,.44),M['bronze'],.015)
    for x in [73.3,98.7]:
        o=beam('Carport oak eave beam',(x,-28,8.85),(x,-2,11.0167),.6,.85,M['accent_oak']);o['ifc_class']='IfcBeam'
    # Single 1:12 fall to front gutter. Exact roofing product remains unselected.
    v=[(72.6,-28,9.4),(99.4,-28,9.4),(99.4,-2,11.5667),(72.6,-2,11.5667)]
    o=mesh('Carport pitched standing seam roof',v+[(x,y,z-.22) for x,y,z in v],[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],roofmat);o['ifc_class']='IfcRoof'
    for i in range(19):
        x=72.6+i*26.8/18
        beam('Carport metal roof seam',(x,-28,9.43),(x,-2,11.5967),.045,.06,roofmat)
    for y in [-26.5,-21,-15.5,-10,-3.5]:
        z=9.4+(y+28)/12-.32
        o=box('Carport cross rafter',(86,y,z),(26.8,.28,.42),M['accent_oak'],.012);o['ifc_class']='IfcBeam'
    for yy in [-28.12,-28.46]:box('Carport gutter upstand',(86,yy,9.2),(27,.025,.24),roofmat,.004)
    box('Carport gutter base',(86,-28.29,9.08),(27,.34,.025),roofmat)
    rod('Carport downpipe',(99,-28.29,9.1),(99,-28.29,.1),.065,roofmat)
    # Reuse the repo's original, unbranded sculpted coupe generator.
    spec=importlib.util.spec_from_file_location('original_coupes',ROOT/'tools/garage03/cars.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    C=dict(M);C.update(black=M['dark'],rubber=material('Car tire rubber',(.015,.017,.017),.72),red=material('Car red tail lamps',(.30,.025,.015),.22))
    C['car-glass']=material('Car smoked glass',(.035,.055,.061),.10,.25)
    for name,x,paint in [('Pearl coastal coupe',79.5,material('Pearl car paint',(.68,.7,.69),.21,.48)),('Graphite coastal coupe',92.5,material('Graphite car paint',(.055,.08,.085),.20,.6))]:mod.car(name,x,-15,0,paint,C)

def garden_detail(M,shared):
    """Front landscape drifts keep both the road walk and carport approaches clear."""
    import random
    from common.shared_assets import place
    collection('12 Arrival | shared layered garden')
    rng=random.Random(441)
    for i in range(75):
        x=rng.choice([rng.uniform(-5,13),rng.uniform(29,67)])
        y=rng.uniform(-40,-7)
        place('Shared front grass drift',shared['grass'],(x,y,-.08),rotation=rng.random()*6.28,scale=rng.uniform(.65,1.05))
        if i%5==0:place('Shared front sage drift',shared['shrub'],(x+1,y,-.08),rotation=rng.random()*6.28,scale=rng.uniform(.7,1.1))
