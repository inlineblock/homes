"""Room placement and bespoke counters, with linked storage and fixtures."""
import math,bpy
from common import geometry as g
from common.geometry import box,cyl,rod,curve,sphere,F
from common.furnishings import soft,chair,sofa,bed,bowl
from common.shared_assets import place
from common.library import linked_collection,instance
from common.architecture import glass_wall
from pathlib import Path

def furnish(M,CAT,at_level):
    g.collection('04 Furnishings | living sleeping dining and storage')
    box('Main living wool rug',(12,31.5,.045),(20,11,.045),M['linen'],.03)
    sofa('Main living sofa',12,27,M)
    box('Living low stone table',(12,32.7,1.1),(6,3.2,.28),M['stone'],.2)
    for x in [10,14]:box('Stone table foot',(x,32.7,.55),(.65,2.6,1),M['stone'],.05)
    bowl('Living stoneware',11,32.7,1.25,.48,M['porcelain'])
    soft('Main dining oak table',(33,32.3,2.5),(8,3.7,.20),M['oak'],.4)
    for x in [30.5,35.5]:box('Dining trestle',(x,32.3,1.2),(.4,2.5,2.4),M['oak'],.06)
    for x in [30.4,33,35.6]:chair('Dining chair',x,29.5,math.pi,M);chair('Dining chair',x,35.1,0,M)
    bowl('Dining bowl',33,32.3,2.6,.65,M['porcelain'])
    bed('Main primary',54,17.4,6.4,M)
    at_level(bed,-11,'Lower bedroom02',9,32.8,5.2,M)
    at_level(bed,-11,'Lower bedroom03',53,32.9,5.2,M)
    at_level(sofa,-11,'Lower lounge sofa',30,29.5,M)
    box('Lower lounge coffee table',(30,34.5,-9.9),(6,3.2,.28),M['stone'],.2)
    for x in [28,32]:box('Lower table foot',(x,34.5,-10.5),(.6,2.5,.8),M['stone'],.05)
    # Exactly scaled linked wardrobe bays, fronts oriented into rooms with clear use zones.
    for y in [14.2,16.2,18.2,20.2]:place('Primary walk-in shared wardrobe',CAT['wardrobe'],(41.2,y,0),math.pi/2)
    for x in [3,5,7]:place('Bedroom02 shared wardrobe',CAT['wardrobe'],(x,25.2,-11),math.pi)
    for y in [29,31,33]:place('Bedroom03 shared wardrobe',CAT['wardrobe'],(43.4,y,-11),math.pi/2)
    for x in [25.5,27.5]:place('Mudroom coats shared wardrobe',CAT['wardrobe'],(x,10.8,0))
    box('Mudroom oak bench',(30.2,10.8,1.5),(2.0,1.5,.18),M['oak'],.04)
    for x in [29.5,30.9]:box('Mudroom bench leg',(x,10.8,.73),(.16,1.6,1.46),M['oak'])
    # Outdoor dining and lounge sit clear of rear door and deck passage.
    soft('Deck dining table',(32,47.1,2.48),(8,3.7,.2),M['deck'],.3)
    for x in [29.4,34.6]:box('Deck dining base',(x,47.1,1.2),(.35,2.4,2.4),M['deck'],.05)
    for x in [29.4,32,34.6]:chair('Deck dining chair',x,44.2,math.pi,M);chair('Deck dining chair',x,50.0,0,M)
    bowl('Deck ceramics',32,47.1,2.59,.65,M['porcelain'])
    sofa('Deck sofa',11,44.5,M)
    soft('Deck lounge table',(11,49.0,1.1),(5.2,3,.2),M['deck'],.25)
    for x in [9.2,12.8]:box('Deck low table support',(x,49,.55),(.35,2.2,1.1),M['deck'])
    for x in [47,53]:
        soft('Lower patio chaise frame',(x,47,-10.45),(2.8,6.8,.35),M['deck'],.10)
        soft('Lower patio chaise cushion',(x,47,-10.15),(2.65,6.6,.28),M['linen'],.14)
        o=soft('Lower patio raised chaise back',(x,44.7,-9.6),(2.65,2.4,.28),M['linen'],.14);o.rotation_euler.x=.48
    chaise_supports(M)
    from premium import kitchen,primary_bath,fireplace
    kitchen(M,CAT)
    fireplace(M,CAT)
    g.collection('05 Fixtures | bath laundry and service space')
    def bath(prefix,x,y,z,shower=True):
        if shower:
            box(prefix+' shower tray',(x+2,y+5.4,z+.08),(3.7,3.3,.14),M['stone'],.025)
            glass_wall(prefix+' shower screen',(x+.15,y+3.7),(x+2.0,y+3.7),z+7.8,M['glass'],M['dark'],z+.1,1)
            rod(prefix+' shower rail',(x+.25,y+6.9,z+3),(x+.25,y+6.9,z+7.1),.04,M['steel'])
            cyl(prefix+' rain shower',(x+.65,y+6.6,z+7.1),.35,.06,M['steel'])
        place(prefix+' shared vanity cabinet',CAT['base_cabinet'],(x+5.7,y+5.5,z))
        bowl(prefix+' vanity basin',x+5.7,y+5.5,z+2.9,.75,M['porcelain'])
        place('Lower shared bathroom WC',CAT['toilet'],(x+5.4,y+1.65,z),math.pi)
    primary_bath(M,CAT)
    bath('Lower shared bath',42.5,18,-11)
    place('Powder vanity',CAT['base_cabinet'],(26,1.4,0),math.pi)
    bowl('Powder basin',26,1.4,2.9,.6,M['porcelain'])
    place('Powder shared WC',CAT['toilet'],(29.8,1.6,0),math.pi)
    for x in [49,52]:
        box('Lower laundry washer dryer',(x,2,-9.45),(2.6,2.7,3.1),M['porcelain'],.08)
        o=cyl('Laundry glazed drum',(x,3.39,-9.3),.82,.1,M['dark'],48);o.rotation_euler.x=math.pi/2
    box('Lower laundry folding surface',(50.5,2,-7.8),(5.9,2.9,.18),M['oak'],.025)
    for x in [55,57]:place('Lower linen shared storage',CAT['wardrobe'],(x,1.5,-11),math.pi)
    box('Mechanical equipment allowance',(36,3,-7.7),(5,4,6.6),M['dark'],.02)
    box('Service workshop bench',(42,2,-8.4),(6,2.5,.2),M['oak'],.05)
    # Garage work storage leaves the two parking bays and mudroom door usable.
    for x in [3,5,7]:place('Garage shared storage',CAT['wardrobe'],(x,22.6,0))


def chaise_supports(M):
    """Four solid recessed feet connect each outdoor chaise frame to its patio."""
    for obj in list(bpy.context.scene.objects):
        if obj.name.startswith('Patio chaise support'):bpy.data.objects.remove(obj,do_unlink=True)
    g.collection('04 Furnishings | living sleeping dining and storage')
    for cx in [47,53]:
        for dx in [-1.02,1.02]:
            for y in [44.65,49.35]:
                box('Patio chaise support',(cx+dx,y,-10.8825),(.22,.34,.515),M['deck'],.012)
