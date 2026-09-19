"""Low pitched coastal envelope and a usable two-car arrival, original concept."""
import math,importlib.util
from common import geometry as g
from common.geometry import box,rod,collection,material,F
from common.architecture import mesh,beam
from common.landscape import grasses,shrub

PITCH=2/12
ROOF_EAVE=10.9
ROOF_RIDGE=ROOF_EAVE+23.75*PITCH
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
    collection('09 Roof | low pitch metal and drainage')
    metal=material('Warm silver standing seam roof',(.36,.385,.37),.4,.65)
    # Two closed, sloping roof plates with a low east-west ridge.
    def plate(name,y1,y2,z1,z2):
        v=[(-2,y1,z1),(70,y1,z1),(70,y2,z2),(-2,y2,z2)]
        o=mesh(name,v+[(x,y,z-.28) for x,y,z in v],[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],metal);o['ifc_class']='IfcRoof'
    plate('Front 2 in 12 roof plane',-3.75,20,ROOF_EAVE,ROOF_RIDGE)
    plate('Rear 2 in 12 roof plane',20,43.75,ROOF_RIDGE,ROOF_EAVE)
    for i in range(49):
        x=-2+i*1.5
        for y,z in [(-3.75,ROOF_EAVE),(43.75,ROOF_EAVE)]:beam('Standing seam rib',(x,y,z+.045),(x,20,ROOF_RIDGE+.045),.045,.075,metal)
    box('Ridge weather cap',(34,20,ROOF_RIDGE+.045),(72.1,.48,.08),metal,.015)
    # Enclosed attic over level ceiling, with original fine oak cladding on gable ends.
    for x in [.2,67.8]:
        o=mesh('Oak clad low gable end',[(x,0,10.5),(x,40,10.5),(x,40,11.245),(x,20,ROOF_RIDGE-.28),(x,0,11.245)],[(0,1,2,3,4)],M['oak']);o['ifc_class']='IfcWall'
    for y in [0,40]:box('Roof attic eave infill',(34,y,10.88),(68,.4,.76),M['oak'],.012)
    box('Continuous warm white ceiling',(34,20,10.48),(71.5,47.2,.06),M['ceiling'],.012)
    for y in [-3.75,43.75]:
        box('Oak roof fascia',(34,y,10.60),(72,.15,.46),M['oak'],.008)
        # U-shaped gutter, with open top and positive roof fall toward it.
        out=y+(-.16 if y<0 else .16)
        # Center-high gutter runs fall 1/16 inch per foot toward each end.
        for end in [-2,70]:
            fall=36/192
            for yy in [out-.16,out+.16]:beam('Gutter sloped upstand',(34,yy,10.53),(end,yy,10.53-fall),.025,.23,metal)
            beam('Gutter sloped base',(34,out,10.41),(end,out,10.41-fall),.32,.025,metal)
        for x in [0,68]:
            rod('Rainwater downpipe',(x,out,10.29),(x,out,.18),.065,metal)
            rod('Concept buried stormwater conveyance',(x,out,-.30),(x+(-12 if x==0 else 12),out,-.30),.12,metal)
            box('Drain inspection grate',(x,out,-.005),(.6,.6,.05),M['dark'],.025)
    for x in [-2,70]:
        for y,z in [(-3.75,ROOF_EAVE),(43.75,ROOF_EAVE)]:beam('Gable barge trim',(x,y,z-.12),(x,20,ROOF_RIDGE-.12),.18,.3,M['oak'])
    entry_canopy(M)
    for i in range(170):box('Rear oak soffit slat',(.1+i*.4,41.90,10.38),(.36,3.65,.10),M['oak'],.007)


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
    roofmat=material('Carport warm silver metal',(.36,.385,.37),.4,.65)
    for x in [73.3,98.7]:
        for y in [-26.7,-5.5]:
            top=9.4+(y+28)/12-.45
            o=box('Carport oak column',(x,y,top/2),(.55,.55,top),M['oak'],.025);o['ifc_class']='IfcColumn'
            box('Carport column steel shoe',(x,y,.22),(.62,.62,.44),M['bronze'],.015)
    for x in [73.3,98.7]:
        o=beam('Carport oak eave beam',(x,-28,8.85),(x,-2,11.0167),.6,.85,M['oak']);o['ifc_class']='IfcBeam'
    # Single 1:12 fall to front gutter. Exact roofing product remains unselected.
    v=[(72.6,-28,9.4),(99.4,-28,9.4),(99.4,-2,11.5667),(72.6,-2,11.5667)]
    o=mesh('Carport pitched standing seam roof',v+[(x,y,z-.22) for x,y,z in v],[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],roofmat);o['ifc_class']='IfcRoof'
    for i in range(19):
        x=72.6+i*26.8/18
        beam('Carport metal roof seam',(x,-28,9.43),(x,-2,11.5967),.045,.06,roofmat)
    for y in [-26.5,-21,-15.5,-10,-3.5]:
        z=9.4+(y+28)/12-.32
        o=box('Carport cross rafter',(86,y,z),(26.8,.28,.42),M['oak'],.012);o['ifc_class']='IfcBeam'
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
